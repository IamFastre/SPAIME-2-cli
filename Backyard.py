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

def synHL(Str:str):
    styleD = {
        '+': X0.GREEN   + '+' + X0.VIOLET,
        '-': X0.RED     + '-' + X0.VIOLET,

        '>': X0.LETTUCE + '>' + X0.VIOLET,
        '<': X0.SKY     + '<' + X0.VIOLET,

        ',': X0.YELLOW  + ',' + X0.VIOLET,
        '.': X0.GOLD    + '.' + X0.VIOLET,

        '[': X0.ORANGE + '[' + X0.VIOLET,
        ']': X0.ORANGE + ']' + X0.VIOLET,
    }
    styleL = list(styleD.keys())


    Str = Str.replace(styleL[6], styleD['['])
    Str = Str.replace(styleL[7], styleD[']'])
    Str = Str.replace(styleL[0], styleD['+'])
    Str = Str.replace(styleL[1], styleD['-'])
    Str = Str.replace(styleL[2], styleD['>'])
    Str = Str.replace(styleL[3], styleD['<'])
    Str = Str.replace(styleL[4], styleD[','])
    Str = Str.replace(styleL[5], styleD['.'])

    return Str

print(synHL('++'))