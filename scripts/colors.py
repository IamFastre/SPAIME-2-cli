import sys
from os.path import abspath, dirname, join

# Sets path to the app's main folder
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))



class C0():

    END         =  '\33[0m'
    RESET       =  '\33[0m'
    BOLD        =  '\33[1m'
    DIM         =  '\33[2m'
    ITALIC      =  '\33[3m'
    URL         =  '\33[4m'
    BLINK       =  '\33[5m'
    BLINK2      =  '\33[6m'
    SELECTED    =  '\33[7m'
    INVISIBLE   =  '\33[8m'
    STRIKE      =  '\33[9m'

class D0():

    BLACK       =  '\33[30m'
    RED         =  '\33[31m'
    GREEN       =  '\33[32m'
    YELLOW      =  '\33[33m'
    BLUE        =  '\33[34m'
    VIOLET      =  '\33[35m'
    BEIGE       =  '\33[36m'
    WHITE       =  '\33[37m'

    BLACKBG     =  '\33[40m'
    REDBG       =  '\33[41m'
    GREENBG     =  '\33[42m'
    YELLOWBG    =  '\33[43m'
    BLUEBG      =  '\33[44m'
    VIOLETBG    =  '\33[45m'
    BEIGEBG     =  '\33[46m'
    WHITEBG     =  '\33[47m'
    
    GRAY        =  '\33[90m'
    RED2        =  '\33[91m'
    GREEN2      =  '\33[92m'
    YELLOW2     =  '\33[93m'
    BLUE2       =  '\33[94m'
    VIOLET2     =  '\33[95m'
    BEIGE2      =  '\33[96m'
    WHITE2      =  '\33[97m'

class X0():

    def RGB(r, g, b, background=False):
        return '\33[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

    def HEX(hexcolor, background=False):
        r = int(hexcolor[0:2], base=16)
        g = int(hexcolor[2:4], base=16)
        b = int(hexcolor[4:6], base=16)
        return X0.RGB(r, g, b, background)

    END         =  '\33[0m'
    RESET       =  '\33[0m'
    C = 9
    WHITE       =  RGB(255,255,255, 0)
    BLACK       =  RGB(0  ,0  ,0  , 0)
    YELLOW      =  RGB(226,226,46 , 0)
    VIOLET      =  RGB(174,129,255, 0)
    GREEN       =  RGB(166,226,46 , 0)
    LETTUCE     =  RGB(144,238,144, 0)
    SKY         =  RGB(160,202,240, 0)
    RED         =  RGB(251,80 ,83 , 0)
    GRAY        =  RGB(145,145,145, 0)
    ORANGE      =  RGB(244,136,17 , 0)
    REDANGE     =  RGB(220,67 ,0  , 0)
    GOLD        =  RGB(255,173,33 , 0)

    WHITEBG     =  RGB(255,255,255, 1)
    BLACKBG     =  RGB(0  ,0  ,0  , 1)
    YELLOWBG    =  RGB(226,226,46 , 1)
    VIOLETBG    =  RGB(174,129,255, 1)
    GREENBG     =  RGB(166,226,46 , 1)
    LETTUCEBG   =  RGB(144,238,144, 1)
    SKYBG       =  RGB(160,202,240, 1)
    REDBG       =  RGB(251,80 ,83 , 1)
    GRAYBG      =  RGB(145,145,145, 1)
    ORANGEBG    =  RGB(244,136,17 , 1)
    REDANGEBG   =  RGB(220,67 ,0  , 1)
    GOLDBG      =  RGB(255,173,33 , 1)
    
    neRED       =  RGB(153,50 ,51 , 0)
    neNOIR      =  RGB(88 ,88 ,88 , 0)

    neREDA      =  RGB(153,50 ,51 , 1) + RGB(153,50 ,51 , 0)
    neNOIRA     =  RGB(25 ,25 ,25 , 1) + RGB(25 ,25 ,25 , 0)