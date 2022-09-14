exec(open(".exec/__homer__.py").read())

from xmlrpc.server import SimpleXMLRPCDispatcher
from res.colors import *

class neRIA():
    def flag(name=False, nsp=0):
        sp = "" 
        for i in range(nsp):
            sp += " "
        print(sp,  x.neREDA,"        {}  {}        ".format( x.neNOIRA, x.neREDA), c.END)
        print(sp,  x.neREDA,"        {}  {}        ".format( x.neNOIRA, x.neREDA), c.END) 
        print(sp, x.neNOIRA,"{}                   {}".format(x.neNOIR,  c.END)     , c.END)
        print(sp,  x.neREDA,"        {}  {}        ".format( x.neNOIRA, x.neREDA), c.END) 
        print(sp,  x.neREDA,"        {}  {}        ".format( x.neNOIRA, x.neREDA), c.END)
        if name:
            print(sp, f"{c.WHITEBG}{x.neNOIR}       ne{x.neRED}RIA        {c.END}")


import time

bar = [
    f'[      {x.neRED}={c.END}]',
    f'[     {x.neRED}={c.END} ]',
    f'[    {x.neRED}={c.END}  ]',
    f'[   {x.neRED}={c.END}   ]',
    f'[  {x.neRED}={c.END}    ]',
    f'[ {x.neRED}={c.END}     ]',
    f'[{x.neRED}={c.END}      ]',
    f'[ {x.neRED}={c.END}     ]',
    f'[  {x.neRED}={c.END}    ]',
    f'[   {x.neRED}={c.END}   ]',
    f'[    {x.neRED}={c.END}  ]',
    f'[     {x.neRED}={c.END} ]'
]
index = 0

def what(function):
    print(function.__name__)


def func():
    print("NOthINg")
    what(func)


# Update the window thingy to update accordingly and idk maybe make it a wider thingy

class morse:

    space     = "/"

    a         = ".-"
    b         = "-..."
    c         = "-.-."
    d         = "-.."
    e         = "."
    f         = "..-."
    g         = "--."
    h         = "...."
    i         = ".."
    j         = ".---"
    k         = "-.-"
    l         = ".-.."
    m         = "--"
    n         = "-."
    o         = "---"
    p         = ".--."
    q         = "--.-"
    r         = ".-."
    s         = "..."
    t         = "-"
    u         = "..-"
    v         = "...-"
    w         = ".--"
    x         = "-..-"
    y         = "-.--"
    z         = "--.."

    one       = ".----"
    two       = "..---"
    three     = "...--" 
    four      = "....-"
    five      = "....."
    six       = "-...."
    seven     = "--..." 
    eight     = "---.." 
    nine      = "----."
    zero      = "-----"

    period    = "-.-.-."
    comma     = "--..--"
    qs_mark   = "..--.."
    ex_mark   = "-.-.--"
    colon     = "---..."
    semicolon = "-.-.-."

    plus      = ".-.-."
    minus     = "-....-"
    equal     = "-...-"

    slash     = "-..-."

    letrs_list = [ " " ,"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2", "3" ,"4" ,"5" ,"6", "7" , "8" ,"9" ,"0" , "."  , "," ,  "?"  ,  "!"  , ":" ,   ";"   ,"+" , "-" , "=" , "/" ]
    morse_list = [space, a , b , c , d , e , f , g , h , i , j , k , l , m , n , o , p , q , r , s , t , u , v , w , x , y , z ,one,two,three,four,five,six,seven,eight,nine,zero,period,comma,qs_mark,ex_mark,colon,semicolon,plus,minus,equal,slash]

    unknown = "?"

    def to(string):
        string = string.casefold()
        morse_array = []

        for letter in string:

            if letter in morse.letrs_list:
                index = morse.letrs_list.index(letter)
                _morse = morse.morse_list[index]
            else:
                _morse = morse.unknown

            morse_array.append(_morse)

        string = " ".join(morse_array)
        return(string)

    def translate(string):
        string = string.split(" ")
        letters_array = []

        for _morse in string:

            if _morse in morse.morse_list:
                index = morse.morse_list.index(_morse)
                letter = morse.letrs_list[index]
            else:
                letter = morse.unknown

            letters_array.append(letter)
        
        string = "".join(letters_array)
        return(string)