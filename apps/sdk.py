import os, sys
from os.path import dirname, join, abspath
from time import sleep

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import random, math, re

# Importing my modules
from res.colors import *
from res.libs import *

# So we can happily fry your device
sys.setrecursionlimit(100000)


num    = [
    X0.GRAY + C0.BOLD + '0' + X0.END,
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

E = 'X'

v = X0.YELLOW + '│' + X0.END
W = '║'

h = '─'
H = '═'

i = '┼'
I = '╬'

s = [
    '╦',
    '╣',
    '╩',
    '╠',
    ]

c = [
    '╔',
    '╗',
    '╚',
    '╝'
    ]

def displayTable(t:list, left:str = '', right:str = ''):

    tableStyle = f'''
{c[0]}{H*11}{s[0]}{H*11}{s[0]}{H*11}{c[1]}
{left}{W} {t[0][0]} {v} {t[0][1]} {v} {t[0][2]} {W} {t[1][0]} {v} {t[1][1]} {v} {t[1][2]} {W} {t[2][0]} {v} {t[2][1]} {v} {t[2][2]} {W}{right}
{left}{W} {t[0][3]} {v} {t[0][4]} {v} {t[0][5]} {W} {t[1][3]} {v} {t[1][4]} {v} {t[1][5]} {W} {t[2][3]} {v} {t[2][4]} {v} {t[2][5]} {W}{right}
{left}{W} {t[0][6]} {v} {t[0][7]} {v} {t[0][8]} {W} {t[1][6]} {v} {t[1][7]} {v} {t[1][8]} {W} {t[2][6]} {v} {t[2][7]} {v} {t[2][8]} {W}{right}
{left}{s[3]}{H*11}{I}{H*11}{I}{H*11}{s[1]}{right}
{left}{W} {t[3][0]} {v} {t[3][1]} {v} {t[3][2]} {W} {t[4][0]} {v} {t[4][1]} {v} {t[4][2]} {W} {t[5][0]} {v} {t[5][1]} {v} {t[5][2]} {W}{right}
{left}{W} {t[3][3]} {v} {t[3][4]} {v} {t[3][5]} {W} {t[4][3]} {v} {t[4][4]} {v} {t[4][5]} {W} {t[5][3]} {v} {t[5][4]} {v} {t[5][5]} {W}{right}
{left}{W} {t[3][6]} {v} {t[3][7]} {v} {t[3][8]} {W} {t[4][6]} {v} {t[4][7]} {v} {t[4][8]} {W} {t[5][6]} {v} {t[5][7]} {v} {t[5][8]} {W}{right}
{left}{s[3]}{H*11}{I}{H*11}{I}{H*11}{s[1]}{right}
{left}{W} {t[6][0]} {v} {t[6][1]} {v} {t[6][2]} {W} {t[7][0]} {v} {t[7][1]} {v} {t[7][2]} {W} {t[8][0]} {v} {t[8][1]} {v} {t[8][2]} {W}{right}
{left}{W} {t[6][3]} {v} {t[6][4]} {v} {t[6][5]} {W} {t[7][3]} {v} {t[7][4]} {v} {t[7][5]} {W} {t[8][3]} {v} {t[8][4]} {v} {t[8][5]} {W}{right}
{left}{W} {t[6][6]} {v} {t[6][7]} {v} {t[6][8]} {W} {t[7][6]} {v} {t[7][7]} {v} {t[7][8]} {W} {t[8][6]} {v} {t[8][7]} {v} {t[8][8]} {W}{right}
{c[2]}{H*11}{s[2]}{H*11}{s[2]}{H*11}{c[3]}
'''

    return tableStyle


def renewVars():
    global numTable

    numTable = [[E for _ in range(9)] for _ in range(9)]

clear()
renewVars()

for n in range(9):
    for x in range(9):
        numTable[n][x] = num[x + 1]

asd = displayTable(numTable)
print(asd)