import sys
from os.path import abspath, dirname, join

# Sets path to the app's main folder
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from scripts.libs import *

"""
class position:

    def __init__(this, X: int | float, Y: int | float) -> None:
        this.x = X
        this.y = Y

    def __str__(this) -> str:
        return f"{this.x}, {this.y}"

    def __getitem__(this, N: int  | float) -> int | float:

        if N in (0, 'x', 'X'): return this.x
        if N in (1, 'y', 'Y'): return this.y

        raise IndexError("Position is only 2 dimensional.")

    def __eq__(this, __o) -> bool:
        if __o[0] == this[0] and __o[1] == this[1]:
            return True
        return False
"""

# Defining map/2d plane class:
class Map:

    def __init__(this, X, Y, Blank = None) -> None:
        this._x    = X
        this._y    = Y
        this.blank = Blank
        this.map   = this.__generate__(X, Y)


    def __generate__(this, _x, _y) -> list[list[object]]:

        MAP = [[this.blank for _ in range(_y)] for _ in range(_x)]
        return MAP


    def __call__(this, *Position:int) -> object:
        return this.map[Position[0]][Position[1]]

#==================================================================#
#==================================================================#


    @property
    def x(this) -> int:
        return this._x

    @x.setter
    def x(this, _x) -> None:

        if   _x > this.x:
            for _ in range(_x - this.x): this.map.append([this.blank for _1 in range(this.y)])
        elif _x < this.x:
            del this.map[_x:]

        this._x = _x

#==================================================================#

    @property
    def y(this) -> int:
        return this._y

    @y.setter
    def y(this, _y) -> None:

        if   _y > this.y:
            for _ in range(this.x): this.map[_].extend([this.blank for _1 in range(_y - this.y)])
        elif _y < this.y:
            for _ in range(this.x): del this.map[_][_y:]

        this._y = _y

#==================================================================#

    @property
    def size(this) -> int:
        return this.x * this.y
 
    @size.setter
    def size(this, _size:tuple[int]) -> None:
        this.x = _size[0]
        this.y = _size[1]

#==================================================================#
#==================================================================#

    def print(this) -> None:

        for y in range(this.y):
            for x in range(this.x):

                _y = y
                y  = (this.y - y - 1) % this.y

                spot = str(this(x,y))
                y = _y

                print(spot, end=' ')
            print()
        print()

#==================================================================#

    def distance(this) -> float:
        pass

#==================================================================#

    def move(this, pos1:list, pos2:list) -> float:
        x1, y1 = pos1
        x2, y2 = pos2

        this.map[x2][y2] = this.map[x1][y1]
        this.map[x1][y1] = this.blank

    def set(this, thing:object, pos1:list = [], pos2:list = []) -> int:
        """
        Sets position/position range to a certain value:
            • If one is given, set that one spot
            • If both are given, set whole range
            • If both are not given, set the whole map
        """

        i = 0

        # If only pos1 was given
        # It'll set only pos1 to that block
        if pos1 != pos2 == list():

            # Changing that single block
            this.map[pos1[0]][pos1[1]] = thing
            i += 1

        # If both positions were given:
        # It'll make a square of that block
        if pos1 != pos2 != list():

            # Getting the X range
            xMax, xMin = max(pos1[0], pos2[0]), min(pos1[0], pos2[0])

            # Getting the Y range
            yMax, yMin = max(pos1[1], pos2[1]), min(pos1[1], pos2[1])

            # Going though every block in range to change
            for _x in range(xMin, xMax+1):
                for _y in range(yMin, yMax+1):
                    this.map[_x][_y] = thing
                    i += 1

        # If no positions were given
        # It'll just set the whole map to that block
        if pos1 == pos2 == list():

            # Going through every block to change
            for _x in range(len(this.map)):
                for _y in range(len(this.map[_x])):
                    this.map[_x][_y] = thing
                    i += 1

        return i

if __name__ == "__main__":
    clear()
    board:Map = Map(6, 6, '•')
    board.set('#', (0,0), (2,5))
    board.print()

    board.move((0,0), (5,5))
    board.print()





# TODO:-
#// • Set X to Y
#// • Move X1,Y1 to X2,Y2
#  • Stack