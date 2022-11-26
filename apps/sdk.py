import os, sys
from os.path import dirname, join, abspath
from time import sleep

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import random, math, re, copy

# Importing my modules
from res.colors import *
from res.libs import *

# So we can happily fry your device
sys.setrecursionlimit(100000)


C1    = [
    X0.YELLOW + C0.BOLD + '•' + X0.END,
    X0.GRAY + C0.BOLD + '1' + X0.END,
    X0.GRAY + C0.BOLD + '2' + X0.END,
    X0.GRAY + C0.BOLD + '3' + X0.END,
    X0.GRAY + C0.BOLD + '4' + X0.END,
    X0.GRAY + C0.BOLD + '5' + X0.END,
    X0.GRAY + C0.BOLD + '6' + X0.END,
    X0.GRAY + C0.BOLD + '7' + X0.END,
    X0.GRAY + C0.BOLD + '8' + X0.END,
    X0.GRAY + C0.BOLD + '9' + X0.END,
         ]

O1    = [
    X0.GRAY + C0.BOLD + '•' + X0.END,
    X0.GOLD + C0.BOLD + '1' + X0.END,
    X0.GOLD + C0.BOLD + '2' + X0.END,
    X0.GOLD + C0.BOLD + '3' + X0.END,
    X0.GOLD + C0.BOLD + '4' + X0.END,
    X0.GOLD + C0.BOLD + '5' + X0.END,
    X0.GOLD + C0.BOLD + '6' + X0.END,
    X0.GOLD + C0.BOLD + '7' + X0.END,
    X0.GOLD + C0.BOLD + '8' + X0.END,
    X0.GOLD + C0.BOLD + '9' + X0.END,
         ]

G1    = [
    X0.GRAY  + C0.BOLD + '•' + X0.END,
    X0.GREEN + C0.BOLD + '1' + X0.END,
    X0.GREEN + C0.BOLD + '2' + X0.END,
    X0.GREEN + C0.BOLD + '3' + X0.END,
    X0.GREEN + C0.BOLD + '4' + X0.END,
    X0.GREEN + C0.BOLD + '5' + X0.END,
    X0.GREEN + C0.BOLD + '6' + X0.END,
    X0.GREEN + C0.BOLD + '7' + X0.END,
    X0.GREEN + C0.BOLD + '8' + X0.END,
    X0.GREEN + C0.BOLD + '9' + X0.END,
         ]

R1    = [
    X0.GRAY + C0.BOLD + '•' + X0.END,
    X0.RED  + C0.BOLD + '1' + X0.END,
    X0.RED  + C0.BOLD + '2' + X0.END,
    X0.RED  + C0.BOLD + '3' + X0.END,
    X0.RED  + C0.BOLD + '4' + X0.END,
    X0.RED  + C0.BOLD + '5' + X0.END,
    X0.RED  + C0.BOLD + '6' + X0.END,
    X0.RED  + C0.BOLD + '7' + X0.END,
    X0.RED  + C0.BOLD + '8' + X0.END,
    X0.RED  + C0.BOLD + '9' + X0.END,
         ]

V = X0.VIOLET + '|' + X0.END
H = X0.VIOLET + '—' + X0.END


class Sudoku():
    '''Main Sudoku Class'''

    def __init__(this, amnt:int):
        this.table    = this.makeTable()
        this.byPlayer = set()
        this.pinched  = set()
        this.timesVal = 0
        this.mistakes = 0
        this.pinchTable(amnt)
        


    def makeTable(this):

        def pattern(r,c): return (3*(r%3)+r//3+c)%9
        def shuffle(s): return random.sample(s,len(s)) 

        rBase = range(3) 

        rows  = [ g*3 + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
        cols  = [ g*3 + c for g in shuffle(rBase) for c in shuffle(rBase) ]

        nums  = shuffle(range(1,3*3+1))

        table = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

        return table


    def pinchTable(this, n:int):

        while n:
            row, col = random.randint(0,8), random.randint(0,8)
            if (row, col) not in this.pinched:
                this.pinched.add((row, col))
                this.table[row][col] = 0
                n -= 1
                


    def rows(this, n = None):
        '''Returns table's rows.'''

        t = copy.deepcopy(this.table)

        r1 = t[0]
        r2 = t[1]
        r3 = t[2]
        r4 = t[3]
        r5 = t[4]
        r6 = t[5]
        r7 = t[6]
        r8 = t[7]
        r9 = t[8]
        Rows = [r1, r2, r3, r4, r5, r6, r7, r8, r9]

        if n == None: return Rows
        else: return Rows[n % 9]

    def cols(this, n = None):
        '''Returns table's columns.'''

        t = copy.deepcopy(this.table)

        c1 = [t[0][0], t[1][0], t[2][0], t[3][0], t[4][0], t[5][0], t[6][0], t[7][0], t[8][0]]
        c2 = [t[0][1], t[1][1], t[2][1], t[3][1], t[4][1], t[5][1], t[6][1], t[7][1], t[8][1]]
        c3 = [t[0][2], t[1][2], t[2][2], t[3][2], t[4][2], t[5][2], t[6][2], t[7][2], t[8][2]]
        c4 = [t[0][3], t[1][3], t[2][3], t[3][3], t[4][3], t[5][3], t[6][3], t[7][3], t[8][3]]
        c5 = [t[0][4], t[1][4], t[2][4], t[3][4], t[4][4], t[5][4], t[6][4], t[7][4], t[8][4]]
        c6 = [t[0][5], t[1][5], t[2][5], t[3][5], t[4][5], t[5][5], t[6][5], t[7][5], t[8][5]]
        c7 = [t[0][6], t[1][6], t[2][6], t[3][6], t[4][6], t[5][6], t[6][6], t[7][6], t[8][6]]
        c8 = [t[0][7], t[1][7], t[2][7], t[3][7], t[4][7], t[5][7], t[6][7], t[7][7], t[8][7]]
        c9 = [t[0][8], t[1][8], t[2][8], t[3][8], t[4][8], t[5][8], t[6][8], t[7][8], t[8][8]]
        Cols = [c1, c2, c3, c4, c5, c6, c7, c8, c9]

        if n == None : return Cols
        else: return Cols[n % 9]

    def subs(this, n = None):
        '''Returns table's subsquares.'''

        t = copy.deepcopy(this.table)

        s1 = [t[0][0], t[0][1], t[0][2], t[1][0], t[1][1], t[1][2], t[2][0], t[2][1], t[2][2]]
        s2 = [t[0][3], t[0][4], t[0][5], t[1][3], t[1][4], t[1][5], t[2][3], t[2][4], t[2][5]]
        s3 = [t[0][6], t[0][7], t[0][8], t[1][6], t[1][7], t[1][8], t[2][6], t[2][7], t[2][8]]
        s4 = [t[3][0], t[3][1], t[3][2], t[4][0], t[4][1], t[4][2], t[5][0], t[5][1], t[5][2]]
        s5 = [t[3][3], t[3][4], t[3][5], t[4][3], t[4][4], t[4][5], t[5][3], t[5][4], t[5][5]]
        s6 = [t[3][6], t[3][7], t[3][8], t[4][6], t[4][7], t[4][8], t[5][6], t[5][7], t[5][8]]
        s7 = [t[6][0], t[6][1], t[6][2], t[7][0], t[7][1], t[7][2], t[8][0], t[8][1], t[8][2]]
        s8 = [t[6][3], t[6][4], t[6][5], t[7][3], t[7][4], t[7][5], t[8][3], t[8][4], t[8][5]]
        s9 = [t[6][6], t[6][7], t[6][8], t[7][6], t[7][7], t[7][8], t[8][6], t[8][7], t[8][8]]
        Subs = [s1, s2, s3, s4, s5, s6, s7, s8, s9]

        p1 = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
        p2 = [(0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)]
        p3 = [(0,6), (0,7), (0,8), (1,6), (1,7), (1,8), (2,6), (2,7), (2,8)]
        p4 = [(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)]
        p5 = [(3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5)]
        p6 = [(3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8)]
        p7 = [(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)]
        p8 = [(6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5)]
        p9 = [(6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)]
        Pos = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

        if   type(n) == type(None): return Subs
        elif type(n) == int:        return Subs[n % 9]
        elif type(n) == tuple:
            for sut in Pos:
                if n in sut:
                    return Subs[Pos.index(sut)]


    def countEmpty(this):
        n = 0
        for row in this.table:
            for spt in row:
                if spt == 0: n += 1
        return n


    def print(this, S:str = 'casual', D:bool = True):
        def expandLine(line):
            return line[0]+line[5:9].join([line[1:5]*(3-1)]*3)+line[9:13]

        line0  = expandLine(f"╔═══╤═══╦═══╗")
        line1  = expandLine(f"║ . │ . ║ . ║")
        line2  = expandLine(f"╟───┼───╫───╢")
        line3  = expandLine(f"╠═══╪═══╬═══╣")
        line4  = expandLine(f"╚═══╧═══╩═══╝")
        left1  =  X0.neNOIR + '    ' + X0.VIOLET
        left2  =  X0.neNOIR + '[{}] ' + X0.VIOLET

        nums = copy.deepcopy(this.table)
        mistakes = 0

        for row in range(len(nums)):
            for col in range(len(nums)):
                val = nums[row][col]

                if S == 'casual':
                    if (row, col) in this.byPlayer:
                        nums[row][col] = O1[val]
                    else:
                        nums[row][col] = C1[val]
                if S == 'validate':
                    if this.rows(row).count(val) > 1 or this.cols(col).count(val) > 1 or this.subs((row,col)).count(val) > 1:
                        nums[row][col] = R1[val]
                        mistakes += 1 if val != 0 else 0
                    else:
                        nums[row][col] = G1[val]

                    this.mistakes = mistakes

        for row in nums: row.insert(0, '')

        #if S == 'validate':
        #    nums   = [ [""]+[X0.END + (M[n] if this.table[this.table.index(row)][row.index(n)] == this.puzzle[this.table.index(row)][row.index(n)] else N[n]) + X0.VIOLET for n in row] for row in this.table ]
        #if S == 'casual':
        #    nums   = [ [""]+[X0.END + (M[n] if (this.table.index(row), row.index(n)) in this.byPlayer else N[n]) + X0.VIOLET for n in row] for row in this.table ]
        #print(nums); enterContinue()

        print()
        print(left1 + ' {} {} {} {} {} {} {} {} {}'.format(*((X0.neNOIR + '[' + str(_) + ']') for _ in list(range(1,10)))) + C0.END)
        print(left1 + line0 + C0.END)
        for r in range(1,9+1):
            print(left2.format(r) +  "".join(str(n) + X0.VIOLET + str(s) for n,s in zip(nums[r-1], line1.split("."))))
            print(left1 + [line2,line3,line4][(r%9==0)+(r%3==0)] + C0.END)
        print(' ' * 18 + "{}[{}SUDOKU{}]{}".format(X0.YELLOW + C0.BOLD, X0.VIOLET, X0.YELLOW, C0.END))
        if D:
            print()
            output.notify(f"Times validated: {this.timesVal} {X0.LETTUCE}V")
            output.notify(f"Empty Spots    : {this.countEmpty()} {X0.YELLOW}•")
            output.notify(f"Mistakes count : {this.mistakes if S == 'validate' else '#'} {X0.RED}•")

    def validateAt(this, s:tuple, n:int):
        T = copy.deepcopy(this.table)

        T[s[0]][s[1]] = C1[n]
        return this.validateTable(T)


    def validateTable(this):

        for row in this.rows():
            for _ in range(row.count(0)): row.remove(0)

            if len(row) > len(set(row)):
                return False

        for col in this.cols():
            for _ in range(col.count(0)): col.remove(0)

            if len(col) > len(set(col)):
                return False

        for sub in this.subs():
            for _ in range(sub.count(0)): sub.remove(0)

            if len(sub) > len(set(sub)):
                return False

        return True


    def play(this, pref):

        choice = intake.prompt()
        choice = choice.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "")
        if choice == "exit":
            print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
            enterContinue(False)
            clear()
            return 'exit'

        if choice.upper() in (pref+'V', pref+'VALIDATE'):
            clear()
            this.timesVal += 1
            output.notify(f"Roger that!")
            this.print('validate')
            this.play(pref)
            return
        if choice.upper() in (pref+'H', pref+'HELP'):
            clear()
            output.notify("Fill a spot by typing: {x-pos,y-pos,number}. Spaces and brackets are ignored.")
            return

        Loc = re.split(" *, *", choice)

        clear()
        try:    Loc = list(map(int, Loc))
        except: output.error(f"Invalid position, dummy.")
        else:
            if len(Loc) == 3:
                X = (Loc[1] - 1) % 9
                Y = (Loc[0] - 1) % 9
                N = Loc[2]
            else:
                output.error(f"Invalid position, dummy.")
                return
            if (X,Y) in this.pinched:
                output.warn("Numbered!")
                this.table[X][Y] = N
                this.byPlayer.add((X,Y)) 
            else: output.error(f"That's the puzzle itself.")


def startGame(n:int = 25, pref:str = '.', game = None):
    global sudoku
    global gameWon
    global plays

    sudoku      = Sudoku(n) if game == None else game
    plays       = 0
    gameRunning = True
    gameWon     = False

    clear()
    output.notify("Fill a spot by typing: {x-pos,y-pos,number}. Spaces and brackets are ignored.")

    while gameRunning:
        if (sudoku.countEmpty() == 0 and len(sudoku.byPlayer) == 0) or (sudoku.countEmpty() == 0 and plays == 0):
            clear()
            output.notify("Game seems already solved!")
            sudoku.print()
            break

        sudoku.print()
        if sudoku.play(pref) == 'exit': return 'exit'
        plays += 1

        if sudoku.validateTable() and sudoku.countEmpty() == 0:
            gameRunning = False
            clear()
            output.success("CONGRATULATIONS! You won!")
            sudoku.print('casual', False)
            gameWon = True
    enterContinue()


if __name__ == "__main__":
    startGame(35)