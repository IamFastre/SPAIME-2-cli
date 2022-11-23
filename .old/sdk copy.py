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
    X0.GRAY + C0.BOLD + '-' + X0.END,
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
    X0.GRAY + C0.BOLD + '-' + X0.END,
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

    def __init__(this, n:int):
        this.table = this.makeTable(n)
        this.update()


    def makeTable(this, n:int):
        table = [ _ for _ in range(81)]
        
        return table


    def update(this):
        t = this.table

        r1 = t[ 0:9 ]
        r2 = t[ 9:18]
        r3 = t[18:27]
        r4 = t[27:36]
        r5 = t[36:45]
        r6 = t[45:54]
        r7 = t[54:63]
        r8 = t[63:72]
        r9 = t[72:81]
        this.rows = [r1, r2, r3, r4, r5, r6, r7, r8, r9]

        c1 = [t[ 0], t[ 9], t[18], t[27], t[36], t[45], t[54], t[63], t[72]]
        c2 = [t[ 1], t[10], t[19], t[28], t[37], t[46], t[55], t[64], t[73]]
        c3 = [t[ 2], t[11], t[20], t[29], t[38], t[47], t[56], t[65], t[74]]
        c4 = [t[ 3], t[12], t[21], t[30], t[39], t[48], t[57], t[66], t[75]]
        c5 = [t[ 4], t[13], t[22], t[31], t[40], t[49], t[58], t[67], t[76]]
        c6 = [t[ 5], t[14], t[23], t[32], t[41], t[50], t[59], t[68], t[77]]
        c7 = [t[ 6], t[15], t[24], t[33], t[42], t[51], t[60], t[69], t[78]]
        c8 = [t[ 7], t[16], t[25], t[34], t[43], t[52], t[61], t[70], t[79]]
        c9 = [t[ 8], t[17], t[26], t[35], t[44], t[53], t[62], t[71], t[80]]
        this.cols = [c1, c2, c3, c4, c5, c6, c7, c8, c9]

        s1 = t[ 0:3 ] + t[ 9:12] + t[18:21]
        s2 = t[ 3:6 ] + t[12:15] + t[21:24]
        s3 = t[ 6:9 ] + t[15:18] + t[24:27]
        s4 = t[27:30] + t[36:39] + t[45:48]
        s5 = t[30:33] + t[39:42] + t[48:51]
        s6 = t[33:36] + t[42:45] + t[51:54]
        s7 = t[54:57] + t[63:66] + t[72:75]
        s8 = t[57:60] + t[66:69] + t[75:78]
        s9 = t[60:63] + t[69:72] + t[78:81]
        this.subs = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


    def print(this):
        this.update()

        print(H*25)
        for i in range(0,9):
            Li = sudoku.rows[i]
            print('| {0} {1} {2} | {3} {4} {5} | {6} {7} {8} |'.format(
                M[Li[0]],M[Li[1]],M[Li[2]],
                M[Li[3]],M[Li[4]],M[Li[5]],
                M[Li[6]],M[Li[7]],M[Li[8]]
                ).replace('|', V))
            if (i+1) % 3 == 0: print(H*25)


    def validateAt(this, s:tuple, n:int):
        this.update()
        T = copy.deepcopy(this.table)

        T[s[0]][s[1]] = N[n]
        return this.validateTable(T)


    def validateTable(this):
        this.update()
        
        for row in this.rows:
            for _ in range(row.count(0)): row.remove(0)

            if len(row) > len(set(row)):
                this.update()
                return False

        for col in this.cols:
            for _ in range(col.count(0)): col.remove(0)

            if len(col) > len(set(col)):
                this.update()
                return False

        for sub in this.subs:
            for _ in range(sub.count(0)): sub.remove(0)

            if len(sub) > len(set(sub)):
                this.update()
                return False

        this.update()
        return True


    def play(this):
        this.update()

        choice = intake.prompt()
        choice = choice.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "")
        Loc = re.split(" *, *", choice)
        print(Loc)
        this.rows[int(Loc[0]) + 1][int(Loc[1])] = int(Loc[2])
        #this.update()


if __name__ == "__main__":
    clear()

    sudoku = Sudoku(50)
    #sudoku.table[0] = 7
    sudoku.update()

    for i in range(9):
        print(sudoku.rows[i])
    sudoku.play()
    clear()
    sudoku.print()
    print(sudoku.validateTable())