import os, sys
from os.path import dirname, join, abspath

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from res.colors import *

import os, time, glob, shutil

class intake():
    prompt = f"{x.YELLOW}\n>{x.GREEN} "
    
class output():

    def invalid(string=False):
        if not string:
            print(f"{x.RED}>>{x.GRAY} Invalid Input.{c.END}")
        else:
            print(f"{x.RED}>>{x.GRAY} {string}{c.END}")

def asciiToChar(string):
    string = string.split(" ")
    for element in string:
        index = string.index(element)
        element = int(element)
        element = chr(element)
        string[index] = element
    return "".join(string)

def confirm(string):
    string = str(string)
    print(string + f"{c.YELLOW}({x.GREEN}y{c.YELLOW}/{x.RED}n{c.YELLOW}){c.END}")
    confirmation = input(f"\n{x.YELLOW}>{x.GREEN} ")
    if confirmation.casefold()== "y" or confirmation.casefold()== "yes" or confirmation.casefold()== "true":
        return True
    elif confirmation.casefold()== "n" or confirmation.casefold()== "no" or confirmation.casefold()== "false":
        return False
    else:
        print(f"{x.YELLOW}\n>>> {x.RED}Invalid Input.{c.END}\n")

def clear():
    print(c.END)
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
def pause():
    if os.name == 'nt':
        _ = os.system('pause && echo.')
    else:
        _ = os.system('echo "Press any key to continue . . ." && read')
def copy_files(dir1, dir2):
    for file in glob.glob(dir1):
        shutil.copy(file, dir2)

def go_thro(thing, allowed):
    for i in range(len(thing)):
        if thing[i] in allowed:
            True
        else:
            return False
    return True
def enter_continue():
    print(f"\n{x.YELLOW}>> {x.GRAY}Press Enter to continue...{c.END}")

    choice = input(f"{c.DIM + c.ITALIC + x.GRAY}")
    print(c.END)
    clear()
    return choice