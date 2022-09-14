import os
try:
    exec(open(".exec/__homer__.py").read())
except:
    print('\33[31m')
    print("I FUCKING HATE MYSELF, OMFG!!!")
    print("some fucking thing went wrong\nplease run the fucking app.py or know what you're doing")
    print('\33[0m')
    os.system('pause')
    exit()


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

currentPlayer = None
gameStatus = 'running'
winner = None

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

    r1 = [board[0],board[1],board[2]]
    r2 = [board[3],board[4],board[5]]
    r3 = [board[6],board[7],board[8]]

    c1 = [board[0],board[3],board[6]]
    c2 = [board[1],board[4],board[7]]
    c3 = [board[2],board[5],board[8]]

    d1 = [board[0],board[4],board[8]]
    d2 = [board[2],board[4],board[6]]

    lines = [r1,r2,r3,c1,c2,c3,d1,d2]

    x_won = [s.x]
    o_won = [s.o]
    tie   = [s.n]

    for line in lines:
        if go_thro(line, x_won):
            return [p1, "done"]
        if go_thro(line, o_won):
            return [p2, "done"]
    
    busy_tiles = 0
    for num in ns:
        if not num in board:
            busy_tiles += 1
    if busy_tiles == 9:
        return [p3, "done"]
    
    return [None, "running"]

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
    global board
    global winner
    
    board = [ns[0],ns[1],ns[2],
             ns[3],ns[4],ns[5],
             ns[6],ns[7],ns[8]]
    
    currentPlayer = None
    gameStatus = 'running'
    winner = None
    
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