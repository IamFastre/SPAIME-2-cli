import os, sys
from os.path import dirname, join, abspath

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import random, math, re

# Importing my modules
from res.colors import *
from res.libs import *
import res.main as rm

# Declaring spot tiles looks
emptyS = x.VIOLET + "#" + x.END
flagS  = x.SKY    + "F" + x.END
bombS  = x.RED    + "*" + x.END
spS    = x.VIOLET + "|" + c.END
nS = [
    x.GRAY+c.DIM   + "0" + x.END,
    x.GREEN        + "1" + x.END,
    x.YELLOW       + "2" + x.END,
    x.ORANGE       + "3" + x.END,
    x.REDANGE      + "4" + x.END,
    x.REDANGE      + "5" + x.END,
    x.neRED        + "6" + x.END,
    x.neRED+c.BOLD + "7" + x.END,
    x.neRED+c.BOLD + "8" + x.END
]


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
    
    def __init__(this, dim = 10, bombs = None):
        this.dim   = dim
        # Counts Bombs if no int provided
        if bombs == None:
            this.bombs = math.ceil((this.dim ** 2)  / 10)
        else:
            this.bombs = bombs
        this.map = this.makeMap()
        this.numerate()
        this.dug   = set()
    
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
        while BOMBS < this.bombs:
            # Getting random (x,y) for the bombs 
            Loc  = random.randint(0, this.dim ** 2 - 1)
            
            xLoc = Loc // this.dim
            yLoc = Loc %  this.dim
            
            # Continuing to loop if (x,y) is already a bomb
            if MAP[xLoc][yLoc] == bombS:
                continue
            
            # Actually adding the bomb
            MAP[xLoc][yLoc] = bombS
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


    def dig(this, X, Y):
        # Digs the given (x,y)
        # If bomb => lose
        # If not => reveal
        

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
                    this.dig(x, y)

        return True


    def flag(this, X, Y):
        
        pass

    def numerate(this):
        # Turning the spot into the number of neighboring bombs
        for x in range(0, this.dim):
            for y in range(0, this.dim):

                if this.map[x][y] == bombS:
                    continue

                this.map[x][y] = this.neighborBombs(x, y)


    def print(this):
        
        this.mapDis   = [[emptyS for _ in range(this.dim)] for _ in range(this.dim)]
        
        for _x in range(0, this.dim):
            for _y in range(0, this.dim):
                if (_x,_y) in this.dug:
                    this.mapDis[_x][_y] = this.map[_x][_y]
                    

        lineL = len(this.mapDis) * 2 + 1
        
        OO = 0
        for i in range(this.dim):
            SO = x.ORANGE + str(OO) + c.END
                
            
        print( x.VIOLET + "    " + ("_"*lineL) + c.END)

        II = 0
        for row in this.mapDis:
            SI = x.ORANGE + " " + str(II) + c.END
            line = x.VIOLET + SI + f"  {spS}" + c.END
            II += 1
            for spot in row:
                line = f"{line}{spot}{spS}"
            print(line)
            #print("—"*lineL)

        print( x.VIOLET + "    " + ("‾"*lineL) + c.END)
            
        print()
        print(f" "*round((lineL/2) - 2) + "{}[{}MINESWEEPER{}]{}\n".format(x.YELLOW, x.VIOLET, x.YELLOW, c.END))
        #print(f"{x.YELLOW}>>{x.VIOLET} Board Size: {x.LETTUCE}{this.dim}{x.YELLOW}u{c.END}")
        #print(f"{x.YELLOW}>>{x.VIOLET} Bomb Count: {x.LETTUCE}{this.bombs}{bombS}{c.END}")


def startGame():
    gameRunning = True
    
    BD = BOARD(10)
    
    flagC = BD.bombs
    
    output.notify('Dig by typing {x-pos,y-pos}. Spaces are ignored.')
    
    while gameRunning:

        BD.print()

        choice = input(intake.prompt)
        try:
            choice = rm.choice_check(choice)
        except:
            pass

        if not "F" in choice:
            Loc = re.split(" *, *", choice)

            try:
                Y = int(Loc[0])
                X = int(Loc[1])
            except ValueError:
                clear()
                output.invalid(f"Invalid position, dummy.")
                continue
            if BD.dim > X >= 0 and BD.dim > Y >= 0:
                if BD.dig(X,Y):
                    clear()
                    output.success("So far so good!")
                    continue
                else:
                    gameRunning = False
            else:
                clear()
                output.invalid(f"Invalid position, dummy.")
                continue
        else:
            BD.flag()

        for _x in range(0, BD.dim):
            for _y in range(0, BD.dim):
                BD.dig(_x,_y)
    
    clear()
    output.invalid(f"You lost. :(")
    BD.print()


if __name__ == "__main__":
    startGame()