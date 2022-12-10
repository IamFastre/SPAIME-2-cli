####################################################################
##                                                                ##
##    Importing important files, modules, packages and so on.     ##
##                                                                ##
####################################################################

import os
import time
import shutil
import pickle
import importlib
import re
import glob
import copy
import random
import math
import subprocess
import pip

from datetime import date, datetime

# Copy thins snippet everywhere please!
import sys
from os.path import abspath, dirname, join
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

# So we can happily fry your device
sys.setrecursionlimit(100_000_000)

# Importing my package files:
from scripts.colors import *
from scripts.codes  import *
from time       import *


####################################################################
#==================================================================#
####################################################################



class intake():
    def prompt(arrow = X0.YELLOW, text = X0.GREEN, arrow2 = X0.VIOLET, text2 = X0.LETTUCE):
        try:
            if random.randint(1,20) == 1:
                return input(f"\n{arrow2}>{text2} ")
            return input(f"\n{arrow}>{text} ")
        except EOFError:
            print()
            output.error("Please don't EOF me...")
            output.error("If you wanna end the app use KeyboardInterrupt or the in-app exit.")
            time.sleep(2)
            delCache()
            return f"I am stupid"
        except KeyboardInterrupt:
            clear()
            output.notify(f"Why so fast? Bye-bye anyway!")
            delCache()
            enterContinue()
            sys.exit(0)


class output():
    """A way of decorating the texts!"""

    def stamp(string, Print = True):
        """Prints violet text with yellow arrows."""
        out = f"{C0.BOLD}{X0.YELLOW}>>>{X0.VIOLET} {string}{C0.END}"

        if Print:
            print(out)
        else:
            return out

    def option(string1, string2, Print = True):
        """Prints white number with the text."""
        out = f"{X0.END}{string1}:{C0.END}{X0.GRAY} {string2}{C0.END}"

        if Print:
            print(out)
        else:
            return out
        
    def warn(string, Print = True):
        """Prints yellow arrows with the text."""
        out = f"{X0.YELLOW}>>{X0.GRAY} {string}{C0.END}"

        if Print:
            print(out)
        else:
            return out
        
    def notify(string, Print = True):
        """Prints violet arrows with the text."""
        out = f"{X0.VIOLET}>>{X0.GRAY} {string}{C0.END}"

        if Print:
            print(out)
        else:
            return out

    def error(string, Print = True):
        """Prints red arrows with the text."""
        out = f"{X0.RED}>>{X0.GRAY} {string}{C0.END}"

        if Print:
            print(out)
        else:
            return out
        
    def success(string, Print = True):
        """Prints green arrows with the text."""
        out = f"{X0.GREEN}>>{X0.GRAY} {string}{C0.END}"

        if Print:
            print(out)
        else:
            return out

    def note(Note, pref = "", sign = "E", Print = True):
        """Prints a note like "!!: {note}"."""
        if sign == "E":
            Sign = f"{X0.WHITE}!!:"
        elif sign == "D":
            Sign = f"{X0.YELLOW}-"
        else:
            Sign = sign
        if Note == 1:
            out = f'''{Sign} {X0.GRAY}Type {C0.ITALIC}"{X0.LETTUCE}{C0.DIM}{pref}help{X0.END}{X0.GRAY}{C0.ITALIC}"{C0.END}{X0.GRAY} to get a list of available commands.{C0.END}'''
        else:
            out = f'''{Sign} {X0.GRAY}{Note}{C0.END}'''

        if Print:
            print(out)
        else:
            return out

def delCache():

    for file in glob.glob('./*/__pycache__'):
        if os.path.exists(file):
            shutil.rmtree(file)

def confirm(string):

    string = str(string)

    print(string + f" {D0.YELLOW}({D0.GREEN}y{D0.YELLOW}/{D0.RED}n{D0.YELLOW}){C0.END}")
    confirmation = intake.prompt()

    if confirmation.casefold() in ("y", "yes", "true", "1"):
        return True
    else:
        return False


def asciiToChar(string):
    string = string.split(" ")
    for element in string:
        index = string.index(element)
        element = int(element)
        element = chr(element)
        string[index] = element
    return "".join(string)


def clear():
    print(C0.END)
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
        
def pause():
    if os.name == 'nt':
        _ = os.system('pause && echo.')
    else:
        _ = os.system('echo "Press any key to continue . . ." && read')
        
        
def copyFiles(dir1, dir2):
    for file in glob.glob(dir1):
        shutil.copy(file, dir2)


def goThro(thing, allowed):
    for i in range(len(thing)):
        if thing[i] in allowed:
            True
        else:
            return False
    return True


def enterContinue(Space=True):
    if Space:
        print()
    print(f"{X0.YELLOW}>> {X0.GRAY}Press Enter to continue...{C0.END}")
    try:
        choice = input(f"{C0.DIM + C0.ITALIC + X0.GRAY}")
    except EOFError:
        print()
        output.error("Please don't EOF me...")
        output.error("If you wanna end the app use KeyboardInterrupt or the in-app exit.")
        time.sleep(2)
        delCache()
        return f"I am stupid"
    except KeyboardInterrupt:
        clear()
        output.notify(f"Why so fast? Bye-bye anyway!")
        delCache()
        enterContinue()
        sys.exit(0)
    print(C0.END)
    clear()
    return choice


def pipInstall(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def curPath():
    return os.path.abspath(os.getcwd())

def folPath(file):
    return os.path.dirname(os.path.abspath(file))

def keyByValue(_dict, _value):
    # This is highly impractical and stupid but I'll do it anyway!
    _key = [i for i in _dict if _dict[i] == _value]

    return _key

def varName(_var):
    # This is highly impractical and stupid too, but I'll do it anyway! Again!
    _name = f'{_var=}'.split('=')[0]
    return _name
