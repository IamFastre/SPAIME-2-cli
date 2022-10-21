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
    n  = x.YELLOW+ c.BLINK  + "No one" + x.END
    o  = x.GREEN + c.BOLD   + "O" + x.END
    x  = x.RED   + c.BOLD   + "X" + x.END


ns = [
        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "1" + x.END,
        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "2" + x.END,
        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "3" + x.END,

        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "4" + x.END,
        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "5" + x.END,
        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "6" + x.END,

        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "7" + x.END,
        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "8" + x.END,
        x.GRAY + c.DIM + c.ITALIC + c.BLINK + "9" + x.END,
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

    user1         = {'name': f"{x.LETTUCE}P-1{c.END}", 'mark': None}
    user2         = {'name': f"{x.SKY}P-2{c.END}"    , 'mark': None}
    cpu           = {'name': f"{x.RED}CPU{c.END}"    , 'mark': None}

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
    output.notify(f"Wanna start with {s.x} {x.GRAY}or {s.o}?")

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
            board[0] = c.BOLD + c.URL + c.BLINK + board[0] + x.END
            board[1] = c.BOLD + c.URL + c.BLINK + board[1] + x.END
            board[2] = c.BOLD + c.URL + c.BLINK + board[2] + x.END
        if winnerLine == "r2":
            board[3] = c.BOLD + c.URL + c.BLINK + board[3] + x.END
            board[4] = c.BOLD + c.URL + c.BLINK + board[4] + x.END
            board[5] = c.BOLD + c.URL + c.BLINK + board[5] + x.END
        if winnerLine == "r3":
            board[6] = c.BOLD + c.URL + c.BLINK + board[6] + x.END
            board[7] = c.BOLD + c.URL + c.BLINK + board[7] + x.END
            board[8] = c.BOLD + c.URL + c.BLINK + board[8] + x.END
        if winnerLine == "c1":
            board[0] = c.BOLD + c.URL + c.BLINK + board[0] + x.END
            board[3] = c.BOLD + c.URL + c.BLINK + board[3] + x.END
            board[6] = c.BOLD + c.URL + c.BLINK + board[6] + x.END
        if winnerLine == "c2":
            board[1] = c.BOLD + c.URL + c.BLINK + board[1] + x.END
            board[4] = c.BOLD + c.URL + c.BLINK + board[4] + x.END
            board[7] = c.BOLD + c.URL + c.BLINK + board[7] + x.END
        if winnerLine == "c3":
            board[2] = c.BOLD + c.URL + c.BLINK + board[2] + x.END
            board[5] = c.BOLD + c.URL + c.BLINK + board[5] + x.END
            board[8] = c.BOLD + c.URL + c.BLINK + board[8] + x.END
        if winnerLine == "d1":
            board[0] = c.BOLD + c.URL + c.BLINK + board[0] + x.END
            board[4] = c.BOLD + c.URL + c.BLINK + board[4] + x.END
            board[8] = c.BOLD + c.URL + c.BLINK + board[8] + x.END
        if winnerLine == "d2":
            board[2] = c.BOLD + c.URL + c.BLINK + board[2] + x.END
            board[4] = c.BOLD + c.URL + c.BLINK + board[4] + x.END
            board[6] = c.BOLD + c.URL + c.BLINK + board[6] + x.END


    Left = str(left) + x.END
    board_look = f"""{Left}{x.LETTUCE}=============
{Left}{x.LETTUCE}| {board[0]} {x.LETTUCE}| {board[1]} {x.LETTUCE}| {board[2]} {x.LETTUCE}|
{Left}{x.LETTUCE}|———|———|———|
{Left}{x.LETTUCE}| {board[3]} {x.LETTUCE}| {board[4]} {x.LETTUCE}| {board[5]} {x.LETTUCE}|
{Left}{x.LETTUCE}|———|———|———|
{Left}{x.LETTUCE}| {board[6]} {x.LETTUCE}| {board[7]} {x.LETTUCE}| {board[8]} {x.LETTUCE}|
{Left}{x.LETTUCE}============={c.END}"""

    # Print or return the Board?!
    if not returnBoard:
        if winner['name'] == None:
            output.notify(f"{currentPlayer['name']}{x.GRAY}({currentPlayer['mark']}{x.GRAY})'s Turn:\n")
            print(board_look)
        elif winner['mark'] in (s.x, s.o):
            output.notify(f"{winner['name']}{x.GRAY}({winner['mark']}{x.GRAY}) won!\n")
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
    print(f"\n{x.YELLOW}>>> {x.VIOLET}2-Player or Solo Mode?{c.END}")
    print(f"{x.GRAY}1: {x.GRAY}Solo Mode{c.END}")
    print(f"{x.GRAY}2: {x.GRAY}2P Mode{c.END}")

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
