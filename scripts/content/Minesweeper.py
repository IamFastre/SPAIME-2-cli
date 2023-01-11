import sys
from os.path import abspath, dirname, join

# Sets path to the app's main folder
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '../..')))

from scripts.libs import *



# Declaring spot tiles looks
emptyS = X0.VIOLET + "#" + X0.END
flagS  = X0.SKY    + "F" + X0.END
bombS  = X0.RED    + "*" + X0.END
spS    = X0.VIOLET + "|" + C0.END
nS = [
    X0.GRAY+C0.DIM   + "0" + X0.END,
    X0.GREEN        + "1" + X0.END,
    X0.YELLOW       + "2" + X0.END,
    X0.ORANGE       + "3" + X0.END,
    X0.REDANGE      + "4" + X0.END,
    X0.REDANGE      + "5" + X0.END,
    X0.neRED        + "6" + X0.END,
    X0.neRED+C0.BOLD + "7" + X0.END,
    X0.neRED+C0.BOLD + "8" + X0.END
]
# Declaring Other stuff
gameWon     = False
gameRunning = False

# Declaring a class to:
#     1: Generate a map
#     2: Plant bombs
#    3a: Digging spots
#    3b: Flagging spots
#    3c: Testing if it's a good spot

class BOARD:
    # Declaring a new class would need map dimension & bomb count
    # If None is provided:
    #    Map Dimension: 10
    #    Bomb Count   : 10
    # If only dimension  :
    #    Bomb Count   : (dim**2)/10

    def __init__(this, dim = 10, bombC = None):
        this.dim   = dim

        # Counts Bombs if no int provided
        if bombC == None:
            this.bombC = math.ceil((this.dim ** 2)  / 10)
        else:
            this.bombC = bombC

        this.bombs     = set()
        this.dug       = set()
        this.playerDug = set()
        this.flagged   = set()

        this.map       = this.makeMap()
        this.numerate()

    def __str__(self):
        pass

    def makeMap(this):
        # Generates a map like:
        # [[spot, spot, ... ,spot]
        # ,[spot, ... ,spot]
        # ,  ...
        # ,[spot, ... ,spot]]
        # and plants bomb previously provided

        # Drawing the map like previously explained
        # and resetting bomb count for new boards
        MAP   = [[emptyS for _ in range(this.dim)] for _ in range(this.dim)]
        BOMBS = 0

        # The planting °¬°
        while BOMBS < this.bombC:

            # Getting random (x,y) for the bombs
            Loc  = random.randint(0, this.dim ** 2 - 1)
            xLoc = Loc // this.dim
            yLoc = Loc %  this.dim

            # Continuing to loop if (x,y) is already a bomb
            if MAP[xLoc][yLoc] == bombS:
                continue

            # Actually adding the bomb
            MAP[xLoc][yLoc] = bombS
            this.bombs.add((xLoc,yLoc))
            BOMBS += 1

        return MAP


    def neighborBombs(this, X, Y):
        # Checking if a spot has neighboring bombs and counting them
        neighbor = 0

        for x in range(X - 1, X + 2):
            for y in range(Y - 1, Y + 2):
                if this.dim > x > -1 and this.dim > y > -1 and this.map[x][y] == bombS:
                    neighbor += 1

        return nS[neighbor]


    def dig(this, X, Y, byPlayer = True):
        # Digs the given (x,y)
        # If bomb => lose
        # If not  => reveal

        if byPlayer:
            this.playerDug.add((X,Y))

        if not (X,Y) in this.flagged:
            this.dug.add((X,Y))

            if this.map[X][Y] == bombS:
                return False
            elif nS.index(this.map[X][Y]) > 0:
                return True

            for x in range(X - 1, X + 2):
                for y in range(Y - 1, Y + 2):
                    if this.dim > x > -1 and this.dim > y > -1:
                        if (x,y) in this.dug:
                            continue
                        this.dig(x, y, byPlayer = False)

        return True


    def flag(this, X, Y):
        global mapView

        if (X,Y) in this.flagged:
            this.flagged.remove((X,Y))
        else:
            this.flagged.add((X,Y))

    def numerate(this):
        # Turning the spot into the number of neighboring bombs
        for x in range(0, this.dim):
            for y in range(0, this.dim):

                if this.map[x][y] == bombS:
                    continue

                this.map[x][y] = this.neighborBombs(x, y)


    def print(this, onlyMap = False):

        this.mapView   = [[emptyS for _ in range(this.dim)] for _ in range(this.dim)]

        for _x in range(0, this.dim):
            for _y in range(0, this.dim):
                if (_x,_y) in this.dug:
                    this.mapView[_x][_y] = this.map[_x][_y]
                if (_x, _y) in this.flagged:
                    this.mapView[_x][_y] = flagS

        lineL = len(this.mapView) * 2 + 1

        lineH = f"\n{X0.SKY}x{X0.VIOLET},{X0.LETTUCE}y{C0.END} "
        for i in range(this.dim):
            SO = X0.SKY + " " + str(i) + C0.END
            lineH = lineH + SO

        print(lineH)
        print( X0.VIOLET + "    " + ("_"*lineL) + C0.END)

        II = 0
        for row in this.mapView:
            SI = X0.LETTUCE + "" + str(II) + C0.END
            lineV = X0.VIOLET + SI + (f"   {spS}" if len(str(II)) < 2 else f"  {spS}") + C0.END
            II += 1
            for spot in row:
                lineV = f"{lineV}{spot}{spS}"
            print(lineV)
            #print("—"*lineL)

        print( X0.VIOLET + "    " + ("‾"*lineL) + C0.END)

        if not onlyMap:
            print()
            print(f" "*round((lineL/2) - 2) + "{}[{}MINESWEEPER{}]{}\n".format(X0.YELLOW + C0.BOLD, X0.VIOLET, X0.YELLOW, C0.END))
        output.notify(f"Board Size  : {X0.LETTUCE}{this.dim} {X0.YELLOW}u{C0.END}")
        output.notify(f"Bomb Count  : {X0.LETTUCE}{this.bombC} {bombS}{C0.END}")
        if not onlyMap:
            output.notify(f"Flags to use: {X0.LETTUCE}{this.bombC - len(this.flagged)} {flagS}{C0.END}")


def startGame(SIZE: int, BOMBS: int):
    global gameRunning
    global gameWon
    global BD

    gameRunning = True

    BD = BOARD(SIZE, BOMBS)

    flagC = BD.bombC

    output.warn('Dig by typing: {x-pos,y-pos}. Spaces and brackets are ignored.')

    while gameRunning:

        BD.print()

        choice = intake.prompt()
        if choice == "exit":
            print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
            enterContinue(False)
            clear()
            return
        choice = choice.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "")
        if not ("F" in choice or "f" in choice):
            Loc = re.split(" *, *", choice)

            try:
                Y = int(Loc[0])
                X = int(Loc[1])
            except ValueError:
                clear()
                output.error(f"Invalid position, dummy.")
                continue
            if BD.dim > X >= 0 and BD.dim > Y >= 0:
                if BD.dig(X,Y):
                    clear()
                    output.success("So far so good!")
                    continue
                else:
                    gameRunning = False
                    gameWon     = False
            else:
                clear()
                output.error(f"Invalid position, dummy.")
                continue
        else:
            if "F" in choice:
                Loc = re.split(" *, *", choice.replace("F", ""))
            elif "f" in choice:
                Loc = re.split(" *, *", choice.replace("f", ""))

            try:
                Y = int(Loc[0])
                X = int(Loc[1])
            except ValueError:
                clear()
                output.error(f"Invalid position, dummy.")
                continue
            if BD.dim > X >= 0 and BD.dim > Y >= 0:

                BD.flag(X,Y)

                if BD.flagged == BD.bombs:
                    gameRunning = False
                    gameWon     = True
                clear()
                output.warn("OK, OK!!")
                continue

    clear()
    if gameWon:
        output.success("CONGRATULATIONS! You won!")
    else:
        output.error(f"You lost. :(")

    for _x in range(0, BD.dim):
        for _y in range(0, BD.dim):
            BD.dig(_x,_y, byPlayer = False)

    BD.print()
    enterContinue()


if __name__ == "__main__":
    clear()
    startGame(10, 10)
    print(gameWon, BD.playerDug)
