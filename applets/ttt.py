import os, sys
from os.path import dirname, join, abspath

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from res.colors import *
from res.libs import *
import res.main as rm


class s():
    n  = x.YELLOW+ c.BLINK  + "No one" + x.END
    o  = x.GREEN + c.BOLD   + "o" + x.END
    x  = x.RED   + c.BOLD   + "x" + x.END


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


board = [ns[0],ns[1],ns[2],
         ns[3],ns[4],ns[5],
         ns[6],ns[7],ns[8]]

def renewVars():
    global currentPlayer
    global gameStatus
    global winnerLine
    global winner
    
    currentPlayer = None
    gameStatus    = 'running'
    winnerLine    = None
    winner        = None

renewVars()

p1 = s.x
p2 = s.o
p3 = s.n


def choosePlayer():
    print(f"\n{x.YELLOW}>>> {x.VIOLET}Wanna start with {s.x} {x.VIOLET}or {s.o}?{c.END}")
    choice = input(intake.prompt)
    try:
        choice = rm.choice_check(choice)
    except:
        pass
    allowed = "xo"
    if go_thro(choice.casefold(), allowed):
        if choice.capitalize() in ("X"):
            clear()
            return p1
        elif choice.capitalize() in ("O"):
            clear()
            return p2
    else:
        clear()
        output.invalid()
        return None


def displayBoard(board, returnBoard=False, left=""):
        
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
            
    
    arrow = str(left) + x.END
    board_look = f"""{arrow}{x.LETTUCE}=============
{arrow}{x.LETTUCE}| {board[0]} {x.LETTUCE}| {board[1]} {x.LETTUCE}| {board[2]} {x.LETTUCE}|
{arrow}{x.LETTUCE}|———|———|———|
{arrow}{x.LETTUCE}| {board[3]} {x.LETTUCE}| {board[4]} {x.LETTUCE}| {board[5]} {x.LETTUCE}|
{arrow}{x.LETTUCE}|———|———|———|
{arrow}{x.LETTUCE}| {board[6]} {x.LETTUCE}| {board[7]} {x.LETTUCE}| {board[8]} {x.LETTUCE}|
{arrow}{x.LETTUCE}=============
{c.END}"""

    if not returnBoard:
        if winner == None:
            print(f"{x.YELLOW}>> {currentPlayer}{x.VIOLET}'s Turn:{c.END}\n")
            print(board_look)
        elif winner in (s.x,s.o):
            print(f"{x.YELLOW}>> {winner}{x.VIOLET} won!{c.END}\n")
            print(board_look)
        else:
            print(f"{x.YELLOW}>> {x.VIOLET}It's a tie!{c.END}\n")
            print(board_look)
    elif returnBoard:
        return board_look


def currentPlayerChange(player):
    if player == p1:
        return p2
    else:
        return p1


def check():
    global board
    
    global r1
    global r2
    global r3
    
    global c1
    global c2
    global c3
    
    global d1
    global d2

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
            

    r1 = [board[0],board[1],board[2]]
    r2 = [board[3],board[4],board[5]]
    r3 = [board[6],board[7],board[8]]

    c1 = [board[0],board[3],board[6]]
    c2 = [board[1],board[4],board[7]]
    c3 = [board[2],board[5],board[8]]

    d1 = [board[0],board[4],board[8]]
    d2 = [board[2],board[4],board[6]]

    lines = [r1,r2,r3,c1,c2,c3,d1,d2]

    for line in lines:
        
        if go_thro(line, [s.x]):
            return [p1, "done", lineChecker()]
        
        if go_thro(line, [s.o]):
            return [p2, "done", lineChecker()]
    
    busy_tiles = 0
    
    for num in ns:
        if not num in board:
            busy_tiles += 1
            
    if busy_tiles == 9:
        return [p3, "done", None]
    
    return [None, "running", None]

def play():
    check()
    global board
    global currentPlayer
    global winner

    if   currentPlayer == p1:
        mark = s.x
    elif currentPlayer == p2:
        mark = s.o

    choice = input(intake.prompt)
    try:
        choice = rm.choice_check(choice)
    except:
        pass
    
    allowed = "123456789"
    if go_thro(choice,allowed) and len(choice) == 1:
        choice = int(choice) - 1
        if board[choice] in ns:
            board[choice] = mark
            currentPlayer = currentPlayerChange(currentPlayer)
        else:
            clear()
            output.invalid()
            displayBoard(board)
            play()
    else:
        clear()
        output.invalid()
        displayBoard(board)
        play()
        
def ttt_start():
    global currentPlayer
    global gameStatus
    global winnerLine
    global winner
    global board
    
    board = [ns[0],ns[1],ns[2],
             ns[3],ns[4],ns[5],
             ns[6],ns[7],ns[8]]
    
    renewVars()
    clear()

    while currentPlayer == None:
        currentPlayer = choosePlayer()


    while gameStatus == "running":
        clear()
        displayBoard(board)
        play()
        results = check()
        winner = results[0]
        gameStatus = results[1]
        winnerLine = results[2]
    else:
        clear()
        displayBoard(board)
        finalWinner = winner
        finalBoard = board
        #finalBoard = displayBoard(board, True, left=f"{x.YELLOW}>>{c.END} ")
        enter_continue()
        return [finalWinner, finalBoard]

if __name__ == '__main__':
    ttt_start()