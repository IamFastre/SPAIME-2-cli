import os, sys
from os.path import dirname, join, abspath

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

class c():
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

class x():

    def RGB(r, g, b, background=False):
        return '\33[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

    def HEX(hexcolor, background=False):
        r = int(hexcolor[0:2], base=16)
        g = int(hexcolor[2:4], base=16)
        b = int(hexcolor[4:6], base=16)
        return x.RGB(r, g, b, background)

    END         =  '\33[0m'
    RESET       =  '\33[0m'

    WHITE       =  RGB(255,255,255)
    BLACK       =  RGB(0,0,0)
    YELLOW      =  RGB(226,226,46)
    VIOLET      =  RGB(174,129,255)
    GREEN       =  RGB(166,226,46)
    LETTUCE     =  RGB(144,238,144)
    SKY         =  RGB(160,202,240)
    RED         =  RGB(251,80,83)
    GRAY        =  RGB(145,145,145)
    ORANGE      =  RGB(244,136,17)
    REDANGE     =  RGB(220,67,0)

    WHITEBG     =  RGB(255,255,255, True)
    BLACKBG     =  RGB(0,0,0, True)
    YELLOWBG    =  RGB(226,226,46, True)
    VIOLETBG    =  RGB(174,129,255, True)
    GREENBG     =  RGB(166,226,46, True)
    LETTUCEBG   =  RGB(144,238,144, True)
    SKYBG       =  RGB(160,202,240, True)
    REDBG       =  RGB(251,80,83, True)
    GRAYBG      =  RGB(145,145,145, True)
    ORANGEBG    =  RGB(244,136,17, True)
    REDANGEBG   =  RGB(220,67,0, True)
    
    neRED       =  RGB(153, 50, 51)
    neNOIR      =  RGB(25, 25, 25)
    
    neREDA      =  RGB(153, 50, 51, True) + RGB(153, 50, 51)
    neNOIRA     =  RGB(25, 25, 25, True) + RGB(25, 25, 25)