import os, sys
from os.path import dirname, join, abspath

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    
import random

from res.colors import *
from res.libs import *



game = {
    'status': 'running',
    'mode': None
}

p1     = {
    'input': None,
    'name': f"{x.LETTUCE}P-1{c.END}"
}
p2     = {
    'input': None,
    'name': f"{x.SKY}P-2{c.END}"
}
cpu    = {
    'input': None,
    'name': f"{x.RED}CPU{c.END}"
}
pN     = {
    'input': None,
    'name': None
}
winner = {
    'input': None,
    'name': None
}
class s:
    r = f"{c.DIM}{c.GRAY}Rock{c.END}"
    p = f"{x.WHITE}Paper{c.END}"
    s = f"{x.RED}Scissors{c.END}"
    

def playerRPC(player):
    print(f"\n{x.YELLOW}>>> {player['name']}, {x.VIOLET}Make a choice:{c.END}")
    print(f"{x.GRAY}1: {s.r}")
    print(f"{x.GRAY}2: {s.p}")
    print(f"{x.GRAY}3: {s.s}")

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
    print(f"\n{x.YELLOW}>>> {player1['name']}{x.VIOLET} chose {player1['input']}{c.END}")
    print(f"{x.YELLOW}>>> {player2['name']}{x.VIOLET} chose {player2['input']}{c.END}")
    print("")
    
    if winner['name'] != None:
        print(f"{x.YELLOW}>> {winner['name']}{x.VIOLET} won!{c.END}")
    else:
        print(f"{x.YELLOW}>>{x.VIOLET} It's a tie!{c.END}")

    enterContinue()
    
def soloMode():
    
    global game
    global p1
    global cpu
    global winner
    
    clear()
    i = playerRPC(p1)
    if not i:
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
    if not i:
        return

    clear()
    i = playerRPC(p2)
    if not i:
        return
    
    winner = compareRPC(p2,p1)
    result(p1,p2,winner)

def chooseMode():
    print(f"\n{x.YELLOW}>>> {x.VIOLET}2-Player or Solo Mode?{c.END}")
    print(f"{x.GRAY}1: {x.GRAY}Solo Mode{c.END}")
    print(f"{x.GRAY}2: {x.GRAY}2P Mode{c.END}")
    
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