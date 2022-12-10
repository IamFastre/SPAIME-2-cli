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


game   = {'status': 'running', 'mode': None}

p1     = {'input': None, 'name': f"{X0.LETTUCE}P-1{C0.END}"}
p2     = {'input': None, 'name': f"{X0.SKY}P-2{C0.END}"}
cpu    = {'input': None, 'name': f"{X0.RED}CPU{C0.END}"}
pN     = {'input': None, 'name': None}
winner = {'input': None, 'name': None}

class s:
    r = f"{C0.DIM}{X0.GRAY}Rock{C0.END}"
    p = f"{X0.WHITE}Paper{C0.END}"
    s = f"{X0.RED}Scissors{C0.END}"


def playerRPC(player):
    print(f"\n{X0.YELLOW}>>> {player['name']}, {X0.VIOLET}Make a choice:{C0.END}")
    print(f"{X0.GRAY}1: {s.r}")
    print(f"{X0.GRAY}2: {s.p}")
    print(f"{X0.GRAY}3: {s.s}")

    choice = intake.prompt()
    if choice == "exit":
        print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
        enterContinue(False)
        clear()
        return False

    if choice in ("r", "1"):
        player['input'] = s.r
        return True
    if choice in ("p", "2"):
        player['input'] = s.p
        return True
    if choice in ("s", "3"):
        player['input'] = s.s
        return True
    clear()
    output.error("Invalid input.")
    playerRPC(player)


def cpuRPC(player):
    choice = str(random.randint(1,3))
    if choice in ("r", "1"):
        player['input'] = s.r
        return
    if choice in ("p", "2"):
        player['input'] = s.p
        return
    if choice in ("s", "3"):
        player['input'] = s.s
        return


def compareRPC(player1,player2):
    n1 = player1
    n2 = player2
    n3 = pN

    c1 = player1['input']
    c2 = player2['input']

    if c1 == s.r and c2 == s.r:
        return n3
    if c1 == s.r and c2 == s.p:
        return n2
    if c1 == s.r and c2 == s.s:
        return n1

    if c1 == s.p and c2 == s.r:
        return n1
    if c1 == s.p and c2 == s.p:
        return n3
    if c1 == s.p and c2 == s.s:
        return n2

    if c1 == s.s and c2 == s.r:
        return n2
    if c1 == s.s and c2 == s.p:
        return n1
    if c1 == s.s and c2 == s.s:
        return n3

def result(player1,player2,winner):

    clear()
    print(f"\n{X0.YELLOW}>>> {player1['name']}{X0.VIOLET} chose {player1['input']}{C0.END}")
    print(f"{X0.YELLOW}>>> {player2['name']}{X0.VIOLET} chose {player2['input']}{C0.END}")
    print("")

    if winner['name'] != None:
        print(f"{X0.YELLOW}>> {winner['name']}{X0.VIOLET} won!{C0.END}")
    else:
        print(f"{X0.YELLOW}>>{X0.VIOLET} It's a tie!{C0.END}")

    enterContinue()

def soloMode():

    global game
    global p1
    global cpu
    global winner

    clear()
    i = playerRPC(p1)
    if i == False:
        return

    cpuRPC(cpu)

    winner = compareRPC(cpu,p1)
    result(p1,cpu,winner)


def duoMode():

    global game
    global p1
    global p2
    global winner

    clear()
    i = playerRPC(p1)
    if i == False:
        return

    clear()
    i = playerRPC(p2)
    if i == False:
        return

    winner = compareRPC(p2,p1)
    result(p1,p2,winner)

def chooseMode():
    print(f"\n{X0.YELLOW}>>> {X0.VIOLET}2-Player or Solo Mode?{C0.END}")
    print(f"{X0.GRAY}1: {X0.GRAY}Solo Mode{C0.END}")
    print(f"{X0.GRAY}2: {X0.GRAY}2P Mode{C0.END}")

    choice = intake.prompt()

    if choice in ("1", "solo"):
        soloMode()
        return
    if choice in ("2", "2p"):
        duoMode()
        return
    clear()
    output.error("Invalid input.")
    chooseMode()

if __name__ == "__main__":
    chooseMode()
