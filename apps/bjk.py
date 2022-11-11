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


cardS = X0.WHITEBG + X0.GRAY
suitS = {
    'C': X0.neNOIR + C0.BOLD + '♣' + C0.END,
    'H': X0.RED    + C0.BOLD + '♥' + C0.END,
    'S': X0.neNOIR + C0.BOLD + '♠' + C0.END,
    'D': X0.RED    + C0.BOLD + '♦' + C0.END,
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
    card['#'] = (cardS +'['+ X0.neNOIR + '##' + cardS + ']'+ C0.END)

    for SUIT in suitS:
        for NUM in numS:
            card[NUM + SUIT] = dict()
            card[NUM + SUIT]['s'] = (cardS +'['+ X0.neNOIR + NUM+suitS[SUIT] + cardS + ']'+ C0.END)
            card[NUM + SUIT]['v'] = (numS[NUM])
            CARDS.append(card[NUM + SUIT])
    return CARDS

PROTO    = genCards()

def newVars(deckN = 2):
    global deck
    global player
    global dealer
    global gameRevealed
    global bet

    gameRevealed = False
    bet = 0

    deck   = genCards() * deckN
    random.shuffle(deck)

    player = {'name': C0.BOLD + X0.GOLD + 'Player' + C0.END, 'hand': list(), 'hidden': list()}
    dealer = {'name': C0.BOLD + X0.GOLD + 'Dealer' + C0.END, 'hand': list(), 'hidden': list()}


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

    print(f"{WHO['name']} {X0.neNOIR}>{X0.RED}>{X0.neNOIR}> {HAND}{HIDDEN}{X0.neNOIR}=> {valuate(WHO)}{C0.END}")


def revealHidden(WHO):
    WHO['hand'] += WHO['hidden']
    WHO['hidden'] = []


def takeAction():

    choice = intake.prompt(arrow=X0.RED,text=X0.neNOIR,arrow2=X0.neNOIR,text2=X0.RED)
    if choice == "exit":
        print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
        enterContinue(False)
        clear()
        return False

    if choice.casefold() in ("h", "hit", "1"):
        return "H"
    if choice.casefold() in ("s", "stand", "2"):
        return "S"
    if choice.casefold() in ("d", "double", "3"):
        return "D"
    if choice.casefold() in ("r", "surrender", "4"):
        return "R"
    return "thisisathrowawaystring"


def check(WHO):
    global gameRevealed
    global bet

    VALUE = valuate(WHO, True)

    if VALUE == 21 and len(WHO['hand'] + WHO['hidden']) == 2:
        revealHidden(WHO)
        gameRevealed = True
        return "jack"
    if VALUE == 21:
        revealHidden(WHO)
        gameRevealed = True
        return "win"
    if VALUE > 21:
        revealHidden(dealer)
        gameRevealed = True
        return "bust"


def compare(WHO1, WHO2):
    VALUE1 = valuate(WHO1, True)
    VALUE2 = valuate(WHO2, True)

    if VALUE1 > 21:
        return WHO2
    if VALUE2 > 21:
        return WHO1

    if VALUE1  > VALUE2:
        return WHO1
    if VALUE1  < VALUE2:
        return WHO2

    if VALUE1 == VALUE2:
        return "tie"


def dealerDecide(soft17 = False):

    while valuate(dealer, True) <= 16 + soft17:
        hit(dealer['hidden'], deck, 1)


def playerJack(BET):
    revealHidden(dealer)
    return BET * 3 / 2 + BET


def playerWon(BET):
    revealHidden(dealer)
    return BET * 2


def playerTied(BET):
    revealHidden(dealer)
    return BET * 1


def playerLost(BET):
    revealHidden(dealer)
    return BET * 0


def startGame(BALANCE:int, N:int=2, SOFT17:bool = False):
    global gameRevealed
    global bet

    def allDisplay(dur = 0.75, con = True):
        print(f"{X0.RED}Balance{X0.neNOIR}: {X0.LETTUCE}{BALANCE}C{C0.END} | {X0.RED}Bet{X0.neNOIR}: {X0.ORANGE}{bet}C{C0.END}")
        print()
        displayHand(dealer)
        displayHand(player)
        print()
        if con:
            print(f"> [{X0.LETTUCE}H{C0.END}] {X0.GOLD}Hit{C0.END}    | [{X0.LETTUCE}S{C0.END}] {X0.GOLD}Stand{C0.END}     <")
            print(f"> [{X0.LETTUCE}D{C0.END}] {X0.GOLD}Double{C0.END} | [{X0.LETTUCE}R{C0.END}] {X0.GOLD}Surrender{C0.END} <")
        sleep(dur)

    clear()
    newVars(N)

    while bet == 0:
        output.notify("How much do you wanna bet on?")
        output.note(f"Balance: {X0.LETTUCE}{BALANCE}C{C0.END}")

        choice = intake.prompt()

        if choice == "exit":
            print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
            enterContinue(False)
            clear()
            return (BALANCE, bet)
        if goThro(choice, "0123456789") and len(choice) > 0:
            if int(choice) <= BALANCE:
                bet = int(choice)
                BALANCE -= bet
            else:
                clear()
                output.error("Insufficient funds.")
                print()
        else:
            clear()
            output.error("Invalid input.")
            print()
        if choice == "0":
            clear()
            output.error("You're wasting my time...")
            print()
    clear()

    hit(player['hand']  , deck, 1)
    clear()
    allDisplay()

    hit(dealer['hand']  , deck, 1)
    clear()
    allDisplay()

    hit(player['hand']  , deck, 1)
    clear()
    allDisplay()

    hit(dealer['hidden'], deck, 1)

    clear()
    while not gameRevealed:

        allDisplay(0)
        if check(dealer) == "jack" and check(player) == "jack":
            clear()
            BALANCE += playerTied(bet)
            output.warn("Push!\n")
            allDisplay(0, 0)
            break
        if check(dealer) == "jack":
            clear()
            BALANCE += playerLost(bet)
            output.error("Lost!\n")
            allDisplay(0, 0)
            break
        if check(player) == "jack":
            clear()
            BALANCE += playerJack(bet)
            output.success("Blackjack!\n")
            allDisplay(0, 0)
            break

        i = takeAction()
        if i == False:
            break

        if i == "H":
            clear()
            hit(player['hand'], deck, 1)
            if check(player) == "win":
                clear()
                BALANCE += playerWon(bet)
                output.success("Win!\n")
                allDisplay(0, 0)
                break
            if check(player) == "bust":
                clear()
                BALANCE += playerLost(bet)
                output.error("Bust!\n")
                allDisplay(0, 0)
                break

        if i == "S":
            clear()

            dealerDecide(SOFT17)
            revealHidden(dealer)

            winner = compare(player, dealer)

            if winner == player:
                clear()
                BALANCE += playerWon(bet)
                output.success("Win!\n")
                allDisplay(0, 0)
                break

            if winner == dealer:
                clear()
                BALANCE += playerLost(bet)
                output.error("Lost!\n")
                allDisplay(0, 0)
                break

            if winner == "tie":
                clear()
                BALANCE += playerTied(bet)
                output.warn("Push!\n")
                allDisplay(0, 0)
                break

        if i == "D":
            clear()

        if i == "R":
            clear()

        if not i in "HSDR":
            clear()
            output.error("Invalid input.\n")
            continue

    enterContinue()
    return (BALANCE, bet)

if __name__ == "__main__":
    startGame(2500)
