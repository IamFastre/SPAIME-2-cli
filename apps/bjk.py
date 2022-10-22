import os, sys
from os.path import dirname, join, abspath
from time import sleep
from tkinter.font import BOLD

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
numS  = {
    'A': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'X': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
}


def genCards():
    global card
    CARDS = list()
    card  = dict()
    card['#'] = (cardS +'['+ x.neNOIR + '##' + cardS + ']'+ c.END)

    for SUIT in suitS:
        for NUM in numS:
            card[NUM + SUIT] = dict()
            card[NUM + SUIT]['s'] = (cardS +'['+ x.neNOIR + NUM+suitS[SUIT] + cardS + ']'+ c.END)
            card[NUM + SUIT]['v'] = (numS[NUM])
            CARDS.append(card[NUM + SUIT])
    return CARDS


def newVars(deckN = 2):
    global deck
    global player
    global dealer
    global gameRevealed

    gameRevealed = False
    deck   = genCards() * deckN
    random.shuffle(deck)

    player = {'name': c.BOLD + x.LETTUCE + 'Player' + c.END, 'hand': list(), 'hidden': list()}
    dealer = {'name': c.BOLD + x.ORANGE  + 'Dealer' + c.END, 'hand': list(), 'hidden': list()}


def valuate(WHO:list, FULL:bool = False):
    HAND = WHO['hand'] + WHO['hidden'] if FULL else WHO['hand']
    VALUE = 0
    ACES  = 0

    for CARD in HAND:
        if CARD['v'] == 1:
            ACES += 1
            continue
        VALUE += CARD['v']

    for ACE in range(ACES):
        if VALUE <= 10:
            VALUE += 11
        else:
            VALUE += 1

    return VALUE


def hit(HAND:list, DECK:list, N:int = 1):
    for i in range(N):
        LAST = DECK.pop(-1)
        HAND.append(LAST)


def displayHand(WHO):
    HAND   = ""
    HIDDEN = ""

    for CARD in WHO['hand']:
        HAND   += CARD['s'] + " "

    for CARD in WHO['hidden']:
        HIDDEN += card['#'] + " "

    print(f"{WHO['name']} {x.neNOIR}>{x.RED}>{x.neNOIR}> {HAND}{HIDDEN}=> {valuate(WHO)}")


def revealHidden(WHO):
    WHO['hand'] += WHO['hidden']
    WHO['hidden'] = []


def takeAction():
    pass


def startGame(N = 2):
    global gameRevealed

    clear()
    newVars(N)

    hit(player['hand']  , deck, 2)

    hit(dealer['hand']  , deck, 1)
    hit(dealer['hidden'], deck, 1)

    displayHand(player)
    displayHand(dealer)


if __name__ == "__main__":
    startGame()