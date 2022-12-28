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

class s:
    piece = {
        'Empty' : '#',
        'Pawn'  : '♙',
        'Knight': '♞',
        'Bishop': '♝',
        'Rook'  : '♜',
        'Queen' : '♛',
        'King'  : '♚'
    }

    piece1 = {
        'Empty' : '#',
        'Pawn'  : 'P',
        'Knight': 'N',
        'Bishop': 'B',
        'Rook'  : 'R',
        'Queen' : 'Q',
        'King'  : 'K'
    }

MOVES = {
    'Pawn'  : lambda pos1, pos2, face:
    pos2[1] - pos1[1] <= face and pos1[0] == pos2[0],

    'Knight': lambda pos1, pos2:
    abs(pos1[0] - pos2[0]) in (1,2) and abs(pos1[1] - pos2[1]) in (1,2),

    'Bishop': lambda pos1, pos2:
    abs(pos2[0] - pos1[0]) == abs(pos2[1] - pos1[1]),

    'Rook'  : lambda pos1, pos2:
    pos1[0] == pos2[0] or pos1[1] == pos2[1],

    'Queen' : lambda pos1, pos2:
    MOVES['Bishop'](pos1, pos2) or MOVES['Rook'],

    'King'  : lambda pos1, pos2:
    ((pos1[0] - pos2[0]) ** 2 + ( pos1[1] - pos2[1]) ** 2 ) ** 0.5 <= 2 ** 0.5
}

Whites:list = []
Blacks:list = []

# Defining Pieces Class:
class Piece:

    def __init__(this, name:str, color:str) -> None:
        this.name  = name
        this.style = C0.BOLD + color + s.piece[name] + C0.END

        if color == BLACK: Blacks.append(this)
        if color == WHITE: Whites.append(this)

W_EMPTY = Piece(
    name  = 'Empty',
    color = WHITE
)
B_EMPTY = Piece(
    name  = 'Empty',
    color = BLACK
)

# Defining Table Class:
class Table:

    def __init__(this, size:int = 8) -> None:
        this.size  = size
        this.setup, this.board = this.makeBoard()

    def makeBoard(this):

        BOARD = [
                    [
                        (B_EMPTY if (_1+_2) % 2 else W_EMPTY) for _2 in range(this.size)
                    ] for _1 in range(this.size)
                ]

        SETUP = [[0 for _ in range(this.size)] for _ in range(this.size)]

        # Placing Blacks
        for spot in range(this.size):
            SETUP[spot][1] = Piece('Pawn', BLACK)

        SETUP[0][0], SETUP[-1][0] = [Piece('Rook'  , BLACK),] * 2
        SETUP[1][0], SETUP[-2][0] = [Piece('Knight', BLACK),] * 2
        SETUP[2][0], SETUP[-3][0] = [Piece('Bishop', BLACK),] * 2

        SETUP[3][0], SETUP[-4][0] = Piece('Queen', BLACK), Piece('King', BLACK)

        # Placing Whites
        for spot in range(this.size):
            SETUP[spot][6] = Piece('Pawn', WHITE)

        SETUP[0][7], SETUP[-1][7] = [Piece('Rook'  , WHITE),] * 2
        SETUP[1][7], SETUP[-2][7] = [Piece('Knight', WHITE),] * 2
        SETUP[2][7], SETUP[-3][7] = [Piece('Bishop', WHITE),] * 2

        SETUP[3][7], SETUP[-4][7] = Piece('Queen', WHITE), Piece('King', WHITE)


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
                    spot = this.setup[x][y].style
                else:
                    spot = this.board[x][y].style
                print(spot, end=' ')
            print()
        print()


clear()
table = Table()
table.print()

print(MOVES.get('Pawn')((0,0), (0,1), 2))
enterContinue()