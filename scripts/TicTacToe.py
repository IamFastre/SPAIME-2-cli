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


class s():
    n  = X0.YELLOW+ C0.BLINK  + "No one" + X0.END
    o  = X0.GREEN + C0.BOLD   + "O" + X0.END
    x  = X0.RED   + C0.BOLD   + "X" + X0.END


ns = [
        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "1" + X0.END,
        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "2" + X0.END,
        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "3" + X0.END,

        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "4" + X0.END,
        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "5" + X0.END,
        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "6" + X0.END,

        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "7" + X0.END,
        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "8" + X0.END,
        X0.GRAY + C0.DIM + C0.ITALIC + C0.BLINK + "9" + X0.END,
]


#==================================================================#


def renewVars():
    global p1
    global p2

    global user1
    global user2
    global cpu

    global currentPlayer
    global winner
    global tied

    global gameMode
    global gameStatus
    global winnerLine

    global board

    p1 = None
    p2 = None

    user1         = {'name': f"{X0.LETTUCE}P-1{C0.END}", 'mark': None}
    user2         = {'name': f"{X0.SKY}P-2{C0.END}"    , 'mark': None}
    cpu           = {'name': f"{X0.RED}CPU{C0.END}"    , 'mark': None}

    currentPlayer = {'name': None                    , 'mark': None} 
    winner        = {'name': None                    , 'mark': None}
    tied          = {'name': 'No one'                , 'mark': None}

    gameMode      = None
    gameStatus    = None
    gameDiff      = None
    winnerLine    = None

    board = [ns[0],ns[1],ns[2],
             ns[3],ns[4],ns[5],
             ns[6],ns[7],ns[8]]
renewVars()


#==================================================================#


def chooseMark():
    output.notify(f"Wanna start with {s.x} {X0.GRAY}or {s.o}?")

    choice = intake.prompt()

    if choice == "exit": print( "\033[1A" + output.notify("Oh, bye. :(", Print=False)); enterContinue(False); clear(); return False

    allowed = "xo12"
    if goThro(choice.casefold(), allowed) and len(choice) == 1:
        if choice.upper() in ("X", "1"):
            clear()
            return s.x
        elif choice.upper() in ("O", "2"):
            clear()
            return s.o
    else:
        clear()
        output.error("Invalid input.\n")
        return None


#==================================================================#


def displayBoard(board, returnBoard=False, left=""):

    # Highlight winner line if game is done.
    if gameStatus == "done":
        if winnerLine == "r1":
            board[0] = C0.BOLD + C0.URL + C0.BLINK + board[0] + X0.END
            board[1] = C0.BOLD + C0.URL + C0.BLINK + board[1] + X0.END
            board[2] = C0.BOLD + C0.URL + C0.BLINK + board[2] + X0.END
        if winnerLine == "r2":
            board[3] = C0.BOLD + C0.URL + C0.BLINK + board[3] + X0.END
            board[4] = C0.BOLD + C0.URL + C0.BLINK + board[4] + X0.END
            board[5] = C0.BOLD + C0.URL + C0.BLINK + board[5] + X0.END
        if winnerLine == "r3":
            board[6] = C0.BOLD + C0.URL + C0.BLINK + board[6] + X0.END
            board[7] = C0.BOLD + C0.URL + C0.BLINK + board[7] + X0.END
            board[8] = C0.BOLD + C0.URL + C0.BLINK + board[8] + X0.END
        if winnerLine == "c1":
            board[0] = C0.BOLD + C0.URL + C0.BLINK + board[0] + X0.END
            board[3] = C0.BOLD + C0.URL + C0.BLINK + board[3] + X0.END
            board[6] = C0.BOLD + C0.URL + C0.BLINK + board[6] + X0.END
        if winnerLine == "c2":
            board[1] = C0.BOLD + C0.URL + C0.BLINK + board[1] + X0.END
            board[4] = C0.BOLD + C0.URL + C0.BLINK + board[4] + X0.END
            board[7] = C0.BOLD + C0.URL + C0.BLINK + board[7] + X0.END
        if winnerLine == "c3":
            board[2] = C0.BOLD + C0.URL + C0.BLINK + board[2] + X0.END
            board[5] = C0.BOLD + C0.URL + C0.BLINK + board[5] + X0.END
            board[8] = C0.BOLD + C0.URL + C0.BLINK + board[8] + X0.END
        if winnerLine == "d1":
            board[0] = C0.BOLD + C0.URL + C0.BLINK + board[0] + X0.END
            board[4] = C0.BOLD + C0.URL + C0.BLINK + board[4] + X0.END
            board[8] = C0.BOLD + C0.URL + C0.BLINK + board[8] + X0.END
        if winnerLine == "d2":
            board[2] = C0.BOLD + C0.URL + C0.BLINK + board[2] + X0.END
            board[4] = C0.BOLD + C0.URL + C0.BLINK + board[4] + X0.END
            board[6] = C0.BOLD + C0.URL + C0.BLINK + board[6] + X0.END


    Left = str(left) + X0.END
    board_look = f"""{Left}{X0.LETTUCE}=============
{Left}{X0.LETTUCE}| {board[0]} {X0.LETTUCE}| {board[1]} {X0.LETTUCE}| {board[2]} {X0.LETTUCE}|
{Left}{X0.LETTUCE}|———|———|———|
{Left}{X0.LETTUCE}| {board[3]} {X0.LETTUCE}| {board[4]} {X0.LETTUCE}| {board[5]} {X0.LETTUCE}|
{Left}{X0.LETTUCE}|———|———|———|
{Left}{X0.LETTUCE}| {board[6]} {X0.LETTUCE}| {board[7]} {X0.LETTUCE}| {board[8]} {X0.LETTUCE}|
{Left}{X0.LETTUCE}============={C0.END}"""

    # Print or return the Board?!
    if not returnBoard:
        if winner['name'] == None:
            output.notify(f"{currentPlayer['name']}{X0.GRAY}({currentPlayer['mark']}{X0.GRAY})'s Turn:\n")
            print(board_look)
        elif winner['mark'] in (s.x, s.o):
            output.notify(f"{winner['name']}{X0.GRAY}({winner['mark']}{X0.GRAY}) won!\n")
            print(board_look)
        else:
            output.notify(f"It's a tie!\n")
            print(board_look)
    elif returnBoard:
        return board_look



def swapPlayer(P1, P2):
    if currentPlayer['name'] == P1['name']:
        return P2
    else:
        return P1


#==================================================================#


def check(p1: dict, p2: dict):
    global board

    global r1
    global r2
    global r3

    global c1
    global c2
    global c3

    global d1
    global d2

    # I couldn't really do it any other way.
    def lineChecker(line):
        if line == r1:
            return "r1"
        if line == r2:
            return "r2"
        if line == r3:
            return "r3"
        if line == c1:
            return "c1"
        if line == c2:
            return "c2"
        if line == c3:
            return "c3"
        if line == d1:
            return "d1"
        if line == d2:
            return "d2"

    # Declaring game lines.
    r1 = [board[0],board[1],board[2]]
    r2 = [board[3],board[4],board[5]]
    r3 = [board[6],board[7],board[8]]

    c1 = [board[0],board[3],board[6]]
    c2 = [board[1],board[4],board[7]]
    c3 = [board[2],board[5],board[8]]

    d1 = [board[0],board[4],board[8]]
    d2 = [board[2],board[4],board[6]]

    lines = [r1,r2,r3,c1,c2,c3,d1,d2]

    # Checks if there's a winner line.
    for line in lines:
        if goThro(line, [p1['mark']]):
            return [p1, "done", lineChecker(line)]

        if goThro(line, [p2['mark']]):
            return [p2, "done", lineChecker(line)]

    # Checks if there's no empty space.
    busy_tiles = 0
    for num in ns:
        if not num in board:
            busy_tiles += 1
    # If yes, then game is tied.
    if busy_tiles == 9:
        return [tied, "done", None]
    # If no check checks, keep going.
    return [winner, "running", None]


#==================================================================#


def userDecide(player):
    global board

    def fail():
        clear()
        displayBoard(board)
        output.error("Invalid input.")
        userDecide(player)

    choice = intake.prompt()

    if choice == "exit": print( "\033[1A" + output.notify("Oh, bye. :(", Print=False)); enterContinue(False); return False

    allowed = "123456789"
    if goThro(choice, allowed) and len(choice):
        choice = int(choice) - 1
        if choice < len(board) and board[choice] in ns:
            board[choice] = player['mark']
        else:
            fail()
    else:
        fail()

#==================================================================#


def cpuDecide(diff="H"):
    global board


    def lineChecker():
        if line == r1:
            return "r1"
        if line == r2:
            return "r2"
        if line == r3:
            return "r3"

        if line == c1:
            return "c1"
        if line == c2:
            return "c2"
        if line == c3:
            return "c3"

        if line == d1:
            return "d1"
        if line == d2:
            return "d2"

    def dup(List):
        for thing in List:
            if List.count(thing) > 1:
                return thing
        return False

    # Declaring game lines.
    r1 = [board[0],board[1],board[2]]
    r2 = [board[3],board[4],board[5]]
    r3 = [board[6],board[7],board[8]]

    c1 = [board[0],board[3],board[6]]
    c2 = [board[1],board[4],board[7]]
    c3 = [board[2],board[5],board[8]]

    d1 = [board[0],board[4],board[8]]
    d2 = [board[2],board[4],board[6]]

    lines = [r1,r2,r3,c1,c2,c3,d1,d2]

    if diff == "H":
        coin = 0.5
        mess = f"This is so easy!"
        dur  = 0.5
    if diff == "M":
        coin = random.random()
        mess = f"Oh, lemme think..."
        dur  = 0.75
    if diff == "E":
        coin = 0
        mess = f"I love pancakes! Huh, what's TicTacToe?"
        dur  = 1

    output.note(mess, sign=cpu['name']+":")
    sleep(dur)

    if coin >= 0.5 and coin:
        # Aggressive behavior.
        for line in lines:
            Dup = dup(line)
            if Dup == cpu['mark'] and goThro(line, ns+[cpu['mark']]):
                for i in range(2):
                    line.remove(Dup)
                choice = ns.index(line[0])
                board[choice] = cpu["mark"]
                return

    if coin <= 0.5 and coin:
        # Defensive behavior.
        for line in lines:
            Dup = dup(line)
            if Dup == user1['mark'] and goThro(line, ns+[user1['mark']]):
                for i in range(2):
                    line.remove(Dup)
                choice = ns.index(line[0])
                board[choice] = cpu["mark"]
                return

    if diff == "H" or diff == "M":
        if board[4] == ns[4]:
            choice = 4
            board[choice] = cpu["mark"]
            return

    while True:
        choice = random.randint(0,8)
        if board[choice] in ns:
            board[choice] = cpu['mark']
            break





#==================================================================#


def duoMode():
    global gameStatus
    global gameMode
    global board
    global currentPlayer
    global winner
    global winnerLine

    renewVars()
    gameStatus = "running"
    gameMode   = "duo"

    clear()
    while currentPlayer['mark'] == None: 
        user1['mark'] = chooseMark()
        user2['mark'] = s.o if user1['mark'] == s.x else s.x

        if user1['mark'] == False: return False

        currentPlayer = user1

    while gameStatus == "running":

        clear()
        displayBoard(board)
        i = userDecide(currentPlayer)
        if i == False: return False

        result     = check(user1, user2)

        winner     = result[0]
        gameStatus = result[1]
        winnerLine = result[2]

        currentPlayer = swapPlayer(user1, user2)

    clear()
    displayBoard(board)
    enterContinue()
    return [winner, board, winnerLine]


#==================================================================#


def soloMode(diff):
    global gameStatus
    global gameMode
    global board
    global currentPlayer
    global winner
    global winnerLine
    global gameDiff

    renewVars()
    gameStatus = "running"
    gameMode   = "solo"
    gameDiff   = diff

    cpu['name'] = f"{diff}-{cpu['name']}"
    clear()
    while currentPlayer['mark'] == None: 
        user1['mark'] = chooseMark()
        cpu['mark']   = s.o if user1['mark'] == s.x else s.x

        if user1['mark'] == False: return False

        currentPlayer = user1 if user1['mark'] == s.x else cpu

    while gameStatus == "running":

        clear()
        displayBoard(board)
        if currentPlayer == user1:
            i = userDecide(currentPlayer)
            if i == False: return False
        else:
            cpuDecide(diff)

        result     = check(user1, cpu)

        winner     = result[0]
        gameStatus = result[1]
        winnerLine = result[2]

        currentPlayer = swapPlayer(user1, cpu)

    clear()
    displayBoard(board)
    enterContinue()
    return [winner, board, winnerLine]

#==================================================================#


def chooseMode():
    print(f"\n{X0.YELLOW}>>> {X0.VIOLET}2-Player or Solo Mode?{C0.END}")
    print(f"{X0.GRAY}1: {X0.GRAY}Solo Mode{C0.END}")
    print(f"{X0.GRAY}2: {X0.GRAY}2P Mode{C0.END}")

    choice = intake.prompt()

    if choice in ("1", "solo"):
        soloMode("E")
        return
    if choice in ("2", "2p"):
        duoMode()
        return
    clear()
    output.error("Invalid input.")
    chooseMode()

#==================================================================#

if __name__ == "__main__":
    clear()
    chooseMode()
