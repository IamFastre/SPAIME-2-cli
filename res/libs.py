import os, sys
from os.path import dirname, join, abspath

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from res.colors import *
import os, time, glob, shutil, pip, subprocess, random


class intake():
    def prompt():
        try:
            if random.randint(1,20) == 1:
                return input(f"{x.VIOLET}\n>{x.GREEN} ")
            return input(f"{x.YELLOW}\n>{x.GREEN} ")
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
        out = f"{c.BOLD}{x.YELLOW}>>>{x.VIOLET} {string}{c.END}"

        if Print:
            print(out)
        else:
            return out

    def option(string1, string2, Print = True):
        """Prints white number with the text."""
        out = f"{x.END}{string1}:{c.END}{x.GRAY} {string2}{c.END}"

        if Print:
            print(out)
        else:
            return out
        
    def warn(string, Print = True):
        """Prints yellow arrows with the text."""
        out = f"{x.YELLOW}>>{x.GRAY} {string}{c.END}"

        if Print:
            print(out)
        else:
            return out
        
    def notify(string, Print = True):
        """Prints violet arrows with the text."""
        out = f"{x.VIOLET}>>{x.GRAY} {string}{c.END}"

        if Print:
            print(out)
        else:
            return out

    def error(string, Print = True):
        """Prints red arrows with the text."""
        out = f"{x.RED}>>{x.GRAY} {string}{c.END}"

        if Print:
            print(out)
        else:
            return out
        
    def success(string, Print = True):
        """Prints green arrows with the text."""
        out = f"{x.GREEN}>>{x.GRAY} {string}{c.END}"

        if Print:
            print(out)
        else:
            return out

    def note(num, pref = "", sign = "E"):
        if sign == "E":
            Sign = f"{x.WHITE}!!:"
        elif sign == "D":
            Sign = f"{x.YELLOW}-"
        else:
            Sign = sign

        if num == 1:
            print(f'''{Sign} {x.GRAY}Type {c.ITALIC}"{x.LETTUCE}{c.DIM}{pref}help{x.END}{x.GRAY}{c.ITALIC}"{c.END}{x.GRAY} to get a list of available commands.{c.END}''')
        else:
            print(f'''{Sign} {x.GRAY}{num}{c.END}''')

def delCache():

    for file in glob.glob('./*/__pycache__'):
        if os.path.exists(file):
            shutil.rmtree(file)

def confirm(string):

    string = str(string)

    print(string + f" {c.YELLOW}({x.GREEN}y{c.YELLOW}/{x.RED}n{c.YELLOW}){c.END}")
    confirmation = intake.prompt()

    if confirmation.casefold() == "y" or confirmation.casefold()== "yes" or confirmation.casefold()== "true":
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
    print(f"{x.YELLOW}>> {x.GRAY}Press Enter to continue...{c.END}")
    try:
        choice = input(f"{c.DIM + c.ITALIC + x.GRAY}")
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
    print(c.END)
    clear()
    return choice


def pipInstall(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])