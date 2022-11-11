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
        '+': x.GREEN   + '+' + x.VIOLET,
        '-': x.RED     + '-' + x.VIOLET,

        '>': x.LETTUCE + '>' + x.VIOLET,
        '<': x.SKY     + '<' + x.VIOLET,

        ',': x.YELLOW  + ',' + x.VIOLET,
        '.': x.GOLD    + '.' + x.VIOLET,

        '[': x.ORANGE + '[' + x.VIOLET,
        ']': x.ORANGE + ']' + x.VIOLET,
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