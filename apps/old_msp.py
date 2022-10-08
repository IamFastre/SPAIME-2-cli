import os, sys
from os.path import dirname, join, abspath

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    
import random, math
    
from res.colors import *
from res.libs import *
import res.main as rm

emptyS = " "
bombS  = x.RED + "*" + x.END
cS = [
    x.GRAY+c.DIM   + "0" + x.END,
    x.LETTUCE      + "1" + x.END,
    x.YELLOW       + "2" + x.END,
    x.ORANGE       + "3" + x.END,
    x.REDANGE      + "4" + x.END,
    x.REDANGE      + "5" + x.END,
    x.neRED        + "6" + x.END,
    x.neRED+c.BOLD + "7" + x.END,
    x.neRED+c.BOLD + "8" + x.END
]

class BOARD:
    def __init__(this, dim = 10, bombs = False):
        this.dim   = dim
        if not bombs:
            bombs = int(this.dim**2/10)
        this.bombs = bombs
        this.map = this.makeMap()
        
        this.dug   = set()
        
    def makeMap(this):
        MAP   = [[emptyS for _ in range(this.dim)] for _ in range(this.dim)]
        BOMBS = 0
        
        while BOMBS < this.bombs:
            Loc  = random.randint(0, this.dim**2 - 1)
            xLoc = Loc // this.dim
            yLoc = Loc %  this.dim
            
            if MAP[xLoc][yLoc] == bombS:
                continue
            
            MAP[xLoc][yLoc] = bombS
            BOMBS += 1
        
        return MAP
    
    def neighborBombs(this, X, Y):
        neighbor = 0
        
        for x in range(X - 1, X + 2):
            for y in range(Y - 1, Y + 2):
                if this.dim > x > -1 and this.dim > y > -1 and this.map[x][y] == bombS:
                    neighbor += 1
        
        return cS[neighbor]
    
    def numerate(this):
        for x in range(0, this.dim):
            for y in range(0, this.dim):
                
                if this.map[x][y] == bombS:
                    continue
                
                this.map[x][y] = this.neighborBombs(x, y) 
        

Board = BOARD()

def displayBoard(board):
    board.numerate()

    lineL = len(board.map) * 4 + 1

    print( x.VIOLET + ("="*lineL) + c.END)

    for row in board.map:
        line = x.VIOLET + "|" + c.END
        for spot in row:
            line = f"{line} {spot} {x.VIOLET}|{c.END}"
        print(line)
        #print("—"*lineL)

    print( x.VIOLET + ("="*lineL) + c.END)

    print(f"{x.YELLOW}>>{x.VIOLET} Board Size: {x.LETTUCE}{board.dim} {x.YELLOW}#{c.END}")
    print(f"{x.YELLOW}>>{x.VIOLET} Bomb Count: {x.LETTUCE}{board.bombs} {bombS}{c.END}")
    
displayBoard(Board)
enterContinue()