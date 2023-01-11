import sys
from os.path import abspath, dirname, join

# Sets path to the app's main folder
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '../..')))

from scripts.libs import *

#TODO:
#* Pawn
#* Knight
#* Bishop
#* Rook
#* Queen
#* King
#♟♞♝♜♛♚♙♘♗♖♕♔

WHITE = X0.WHITE
BLACK = X0.neNOIR

class Style:
    unicodes = {
        'Empty' : '•',
        'Pawn'  : '♙',
        'Knight': '♞',
        'Bishop': '♝',
        'Rook'  : '♜',
        'Queen' : '♛',
        'King'  : '♚'
    }

    initials = {
        'Empty' : '#',
        'Pawn'  : 'P',
        'Knight': 'N',
        'Bishop': 'B',
        'Rook'  : 'R',
        'Queen' : 'Q',
        'King'  : 'K'
    }

MOVES = {
    'Empty' : None,

    'Pawn'  : lambda pos1, pos2, face:
    pos2[1] - pos1[1] <= face and pos1[0] == pos2[0],

    'Knight': lambda pos1, pos2      :
    abs(pos1[0] - pos2[0]) in (1,2) and abs(pos1[1] - pos2[1]) in (1,2),

    'Bishop': lambda pos1, pos2      :
    abs(pos2[0] - pos1[0]) == abs(pos2[1] - pos1[1]),

    'Rook'  : lambda pos1, pos2      :
    pos1[0] == pos2[0] or pos1[1] == pos2[1],

    'Queen' : lambda pos1, pos2      :
    MOVES.Bishop(pos1, pos2) or MOVES.Rook(pos1, pos2),

    'King'  : lambda pos1, pos2      :
    ((pos1[0]-pos2[0])**2 + ( pos1[1]-pos2[1])**2)**0.5 <= 2**0.5
}

Whites:list = []
Blacks:list = []
W_EMPTY = WHITE + Style.unicodes['Empty'] + C0.END
B_EMPTY = BLACK + Style.unicodes['Empty'] + C0.END

# Defining Pieces Class:
class Piece:

    def __init__(this, name:str, color:str, style = Style.unicodes) -> None:
        this.name   = name
        this.move   = MOVES[name]
        this.color  = color
        this.style  = style
        this.sprite = C0.BOLD + color + style[name] + C0.END

        if color == BLACK: Blacks.append(this)
        if color == WHITE: Whites.append(this)

    def highlight(this, color):

        this.sprite = C0.BOLD + color + this.color + this.style[this.name] + C0.END



# Defining Table Class:
class Table:

    def __init__(this, size:int = 8, style:Style = Style.unicodes) -> None:
        this.size  = size
        this.style = style
        this.setup, this.board = this.makeBoard()

    def spot(this, X, Y):
        _x = (this.size - X -1) % this.size
        _y = -Y#(this.size - Y -1) % this.size

        print(_x, _y)

        return this.setup[_y][_x]

    def makeBoard(this):

        BOARD = [
                    [
                        (B_EMPTY if (_1+_2) % 2 else W_EMPTY) for _2 in range(this.size)
                    ] for _1 in range(this.size)
                ]

        SETUP = [[0 for _ in range(this.size)] for _ in range(this.size)]

        # Placing Blacks
        for spot in range(this.size):
            SETUP[spot][1] = Piece('Pawn', BLACK, this.style)

        SETUP[0][0], SETUP[-1][0] = Piece('Rook'  , BLACK, this.style), Piece('Rook'  , BLACK, this.style)
        SETUP[1][0], SETUP[-2][0] = Piece('Knight', BLACK, this.style), Piece('Knight', BLACK, this.style)
        SETUP[2][0], SETUP[-3][0] = Piece('Bishop', BLACK, this.style), Piece('Bishop', BLACK, this.style)

        SETUP[3][0], SETUP[-4][0] = Piece('Queen', BLACK, this.style), Piece('King', BLACK, this.style)

        # Placing Whites
        for spot in range(this.size):
            SETUP[spot][6] = Piece('Pawn', WHITE, this.style)

        SETUP[0][7], SETUP[-1][7] = Piece('Rook'  , WHITE, this.style), Piece('Rook'  , WHITE, this.style)
        SETUP[1][7], SETUP[-2][7] = Piece('Knight', WHITE, this.style), Piece('Knight', WHITE, this.style)
        SETUP[2][7], SETUP[-3][7] = Piece('Bishop', WHITE, this.style), Piece('Bishop', WHITE, this.style)

        SETUP[3][7], SETUP[-4][7] = Piece('Queen', WHITE, this.style), Piece('King', WHITE, this.style)


        return SETUP, BOARD

    def move(this, pos1:tuple, pos2:tuple):
        x1, y1 = pos1
        x2, y2 = pos2

        this.setup[x2][y2] = this.setup[x1][y1]
        this.setup[x1][y1] = 0

    def print(this):

        for y in range(this.size):
            for x in range(this.size):
                if this.setup[x][y]:
                    spot = this.setup[x][y].sprite
                else:
                    spot = this.board[x][y]
                print(spot, end=' ')
            print()
        print()


if __name__ == "__main__":

    clear()
    table = Table(style = Style.initials)

    table.spot (0, 1).highlight(X0.GREENBG)
    table.setup[0][0].highlight(X0.REDBG)
    table.print()

    enterContinue(Clear = 0)
    