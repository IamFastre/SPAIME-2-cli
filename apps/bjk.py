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


cardS = x.WHITEBG + x.GRAY
suitS = {
    'C': x.neNOIR + c.BOLD + '♣' + c.END,
    'H': x.RED    + c.BOLD + '♥' + c.END,
    'S': x.neNOIR + c.BOLD + '♠' + c.END,
    'D': x.RED    + c.BOLD + '♦' + c.END,
}
numS  = [
    x.neNOIR + 'A',
    x.neNOIR + '2',
    x.neNOIR + '3',
    x.neNOIR + '4',
    x.neNOIR + '5',
    x.neNOIR + '6',
    x.neNOIR + '7',
    x.neNOIR + '8',
    x.neNOIR + '9',
    x.neNOIR + 'X',
    x.neNOIR + 'J',
    x.neNOIR + 'Q',
    x.neNOIR + 'K',
]

def genDeck():
    DECK = []

    for suit in suitS:
        for num in numS:
            DECK.append(cardS +'['+ num+suitS[suit] + cardS + ']'+ c.END)
    return DECK

def shuffle(DECK):
    thing = set(DECK)
    thing = list(thing)
    return thing

deck = genDeck()
deck = shuffle(deck)
decks = ""
clear()
for i in range(len(deck)):
    decks = decks + deck[i] + ", " 
print(decks)
pause()