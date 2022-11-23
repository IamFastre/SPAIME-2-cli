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


clear()
text = '''
{left}{W} {t[0][0]} {v} {t[0][1]} {v} {t[0][2]} {W} {t[1][0]} {v} {t[1][1]} {v} {t[1][2]} {W} {t[2][0]} {v} {t[2][1]} {v} {t[2][2]} {W}{right}
{left}{W} {t[0][3]} {v} {t[0][4]} {v} {t[0][5]} {W} {t[1][3]} {v} {t[1][4]} {v} {t[1][5]} {W} {t[2][3]} {v} {t[2][4]} {v} {t[2][5]} {W}{right}
{left}{W} {t[0][6]} {v} {t[0][7]} {v} {t[0][8]} {W} {t[1][6]} {v} {t[1][7]} {v} {t[1][8]} {W} {t[2][6]} {v} {t[2][7]} {v} {t[2][8]} {W}{right}
{left}{W} {t[3][0]} {v} {t[3][1]} {v} {t[3][2]} {W} {t[4][0]} {v} {t[4][1]} {v} {t[4][2]} {W} {t[5][0]} {v} {t[5][1]} {v} {t[5][2]} {W}{right}
{left}{W} {t[3][3]} {v} {t[3][4]} {v} {t[3][5]} {W} {t[4][3]} {v} {t[4][4]} {v} {t[4][5]} {W} {t[5][3]} {v} {t[5][4]} {v} {t[5][5]} {W}{right}
{left}{W} {t[3][6]} {v} {t[3][7]} {v} {t[3][8]} {W} {t[4][6]} {v} {t[4][7]} {v} {t[4][8]} {W} {t[5][6]} {v} {t[5][7]} {v} {t[5][8]} {W}{right}
{left}{W} {t[6][0]} {v} {t[6][1]} {v} {t[6][2]} {W} {t[7][0]} {v} {t[7][1]} {v} {t[7][2]} {W} {t[8][0]} {v} {t[8][1]} {v} {t[8][2]} {W}{right}
{left}{W} {t[6][3]} {v} {t[6][4]} {v} {t[6][5]} {W} {t[7][3]} {v} {t[7][4]} {v} {t[7][5]} {W} {t[8][3]} {v} {t[8][4]} {v} {t[8][5]} {W}{right}
{left}{W} {t[6][6]} {v} {t[6][7]} {v} {t[6][8]} {W} {t[7][6]} {v} {t[7][7]} {v} {t[7][8]} {W} {t[8][6]} {v} {t[8][7]} {v} {t[8][8]} {W}{right}
'''
print(
    '\n'.join(        
        re.findall(
            't[\[0-9\]]+',
            text
        )
    )
)
forma = re.findall('t[\[0-9\]]+',text)
print(len(re.findall('t[\[0-9\]]+',text)))

_1 = 0
_2 = []
for i in forma:
    _2.append(i); _1 += 1
    if _1 == 9:
        _1 = 0
        print((f'row{math.floor(forma.index(i)/8)} = [' + (f', '.join(_2)) + ']').replace('t', 'table'))
        _2 = []

clear()
while True:
    t = time.perf_counter()
    i = random.randint(0,9**3)
    if i == 1:
        print(i, 'is one!')
        print(time.perf_counter() - t)
        break