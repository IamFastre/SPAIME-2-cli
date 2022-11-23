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


N    = [
    X0.GRAY + C0.BOLD + '.' + X0.END,
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

M    = [
    X0.GRAY + C0.BOLD + '.' + X0.END,
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

V = X0.VIOLET + '|' + X0.END
H = X0.VIOLET + '—' + X0.END


class Sudoku():
    '''Main Sudoku Class'''

    def __init__(this, amnt:int):
        this.table    = this.makeTable()
        this.puzzle   = copy.deepcopy(this.table)
        this.byPlayer = set()
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

        for _ in range(n):
            this.table[random.randint(0,8)][random.randint(0,8)] = 0


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

        c1 = [t[0][0], t[0][1], t[0][2], t[0][3], t[0][4], t[0][5], t[0][6], t[0][7], t[0][8]]
        c2 = [t[1][0], t[1][1], t[1][2], t[1][3], t[1][4], t[1][5], t[1][6], t[1][7], t[1][8]]
        c3 = [t[2][0], t[2][1], t[2][2], t[2][3], t[2][4], t[2][5], t[2][6], t[2][7], t[2][8]]
        c4 = [t[3][0], t[3][1], t[3][2], t[3][3], t[3][4], t[3][5], t[3][6], t[3][7], t[3][8]]
        c5 = [t[4][0], t[4][1], t[4][2], t[4][3], t[4][4], t[4][5], t[4][6], t[4][7], t[4][8]]
        c6 = [t[5][0], t[5][1], t[5][2], t[5][3], t[5][4], t[5][5], t[5][6], t[5][7], t[5][8]]
        c7 = [t[6][0], t[6][1], t[6][2], t[6][3], t[6][4], t[6][5], t[6][6], t[6][7], t[6][8]]
        c8 = [t[7][0], t[7][1], t[7][2], t[7][3], t[7][4], t[7][5], t[7][6], t[7][7], t[7][8]]
        c9 = [t[8][0], t[8][1], t[8][2], t[8][3], t[8][4], t[8][5], t[8][6], t[8][7], t[8][8]]
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

        if n == None: return Subs
        else: return Subs[n % 9]


    def print(this, S:str = 'casual'):

        def expandLine(line):
            return line[0]+line[5:9].join([line[1:5]*(3-1)]*3)+line[9:13]

        line0  = expandLine(f"╔═══╤═══╦═══╗")
        line1  = expandLine(f"║ . │ . ║ . ║")
        line2  = expandLine(f"╟───┼───╫───╢")
        line3  = expandLine(f"╠═══╪═══╬═══╣")
        line4  = expandLine(f"╚═══╧═══╩═══╝")
        left1  =  X0.neNOIR + '    ' + X0.VIOLET
        left2  =  X0.neNOIR + '[{}] ' + X0.VIOLET

        T = copy.deepcopy(this.table)

        if S == 'correct':
            nums   = [ [""]+[X0.END + (M[n] if this.table[this.table.index(row)][row.index(n)] == this.puzzle[this.table.index(row)][row.index(n)] else N[n]) + X0.VIOLET for n in row] for row in this.table ]
        if S == 'casual':
            nums   = [ [""]+[X0.END + (M[n] if (this.table.index(row), row.index(n)) in this.byPlayer else N[n]) + X0.VIOLET for n in row] for row in this.table ]

        print(left1 + ' {} {} {} {} {} {} {} {} {}'.format(*((X0.neNOIR + '[' + str(_) + ']') for _ in list(range(1,10)))) + C0.END)
        print(left1 + line0 + C0.END)
        for r in range(1,9+1):
            print(left2.format(r) +  "".join(n+s for n,s in zip(nums[r-1],line1.split("."))))
            print(left1 + [line2,line3,line4][(r%9==0)+(r%3==0)] + C0.END)

    def validateAt(this, s:tuple, n:int):
        T = copy.deepcopy(this.table)

        T[s[0]][s[1]] = N[n]
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


    def play(this):
        
        choice = intake.prompt()
        choice = choice.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "")
        Loc = re.split(" *, *", choice)

        clear()
        try:    Loc = list(map(int, Loc))
        except: output.error(f"Invalid position, dummy.")
        else:
            X = Loc[1] - 1
            Y = Loc[0] - 1
            N = Loc[2]
            try:    this.table[X][Y] = N; this.byPlayer.add((X,Y)) 
            except: output.error(f"Invalid position, dummy.")


if __name__ == "__main__":
    clear()

    sudoku = Sudoku(1)
    gameRunning = True

    clear()
    print()
    while gameRunning:
        print()
        sudoku.print()
        sudoku.play()