import os, sys
from os.path import dirname, join, abspath
from time import sleep

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import random, math, re

# Importing my modules
from res.colors import *
from res.libs import *

# So we can happily fry your device
sys.setrecursionlimit(100000)

Tape    = [0]
Output  = [ ]


def Interpreter(Program:str, Input:str = ''):
    global Output
    global Tape

    p       = 0
    InIndex =  0
    Pointer =  0
    Tape    = [0]
    Output  = [ ]

    while p < len(Program):

        def Cmd():
            return Program[p]        

        if Cmd() == '+':
            Tape[Pointer] += 1
            if Tape[Pointer] > 255: Tape[Pointer] = 0

        if Cmd() == '-':
            Tape[Pointer] -= 1
            if Tape[Pointer] <= -1 : Tape[Pointer] = 255

        if Cmd() == '>':
            Pointer += 1
            if len(Tape) <= Pointer: Tape.append(0)

        if Cmd() == '<':
            Pointer -= 1
            if Pointer < 0: raise SyntaxError("You're going out of memory.")

        if Cmd() == '.':
            print(chr(Tape[Pointer]), end="")

        if Cmd() == ',':
            Tape[Pointer] = ord(Input[InIndex]); InIndex += 1

        if Cmd() == '[':
            if Tape[Pointer] == 0:
                oBrac = 0
                p += 1
                while p < len(Program):
                    if Cmd() == ']' and oBrac == 0:
                        break
                    elif Cmd() == '[': oBrac += 1
                    elif Cmd() == ']': oBrac -= 1
                    p += 1

        if Cmd() == ']':
            if Tape[Pointer] != 0:
                cBrac = 0
                p -= 1
                while p >= 0:
                    if Cmd() == '[' and cBrac == 0:
                        break
                    elif Cmd() == ']': cBrac += 1
                    elif Cmd() == '[': cBrac -= 1
                    p -= 1
        p += 1
    print('')

def readBF():
    
    def do(File):
        with open(folder + File, 'r') as brainF:
            Prog = brainF.read()

        inpCount = Prog.count(',')
        if inpCount > 0:
            clear()
            output.notify('Provide some input! -> {} characters'.format(f'{x.LETTUCE}{c.DIM}{inpCount}{c.END}{x.GRAY}'))

            choice = intake.prompt()
            if choice == "exit":
                print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
                enterContinue(False)
                clear()
                return

        clear()

        output.stamp(File)
        print()

        if inpCount > 0:
            output.notify('Input:')
            print(f'{c.DIM}{c.ITALIC}{x.RED}empty{c.END}' if len(choice) == 0 else choice)
            print()

        output.notify('Output:')
        Interpreter(Prog, choice if inpCount else '')
        print()

        output.notify('Memory:')
        print(Tape)

        enterContinue()

    folder    = './addons/BrainFuck/'
    allFiles  = os.listdir(folder)
    filterReg = re.compile('.*?\.bf?(?!.)')
    bfFiles   = list(filter(filterReg.match, allFiles))
    
    if len(bfFiles) == 0:
        output.error("Seems like there's not much options.")
        output.error("No {0}.bf or {0}.b in /addons/BrainFuck/ directory.".format(f'{c.ITALIC}{c.DIM}file-name{c.END}{x.GRAY}'))

    if len(bfFiles) == 1:
        do(bfFiles[0])

    if len(bfFiles) >  1:
        output.notify("Seems like there's some options.")
        output.notify("Please choose a file:")
        print()
        for everyFile in bfFiles:
            output.note(f"{everyFile}", sign= f"{bfFiles.index(everyFile)}:")

        choice = intake.prompt(arrow=x.VIOLET)
        if choice == "exit":
            print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
            enterContinue(False)
            clear()
            return

        if goThro(choice, '0123456789') and int(choice) < len(bfFiles):
            do(bfFiles[int(choice)])
        else:
            clear()
            output.error('How hard can it be to type a number!')
            print()
            readBF()

def clliBF():

    output.stamp('Ooh, you can write this shit?!')
    output.note(f"Allowed chars: '{x.LETTUCE}><+-.,[]{x.GRAY}' anything else is considered a comment")
    prog = intake.prompt()
    if prog == "exit":
        print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
        enterContinue(False)
        clear()
        return

    clear()
    inpCount = prog.count(',')

    if inpCount > 0:
        clear()
        output.notify('Provide some input! -> {} characters'.format(f'{x.LETTUCE}{c.DIM}{inpCount}{c.END}{x.GRAY}'))
        inp = intake.prompt()
        if inp == "exit":
            print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
            enterContinue(False)
            clear()
            return

    clear()
    output.stamp(prog)
    print()

    if inpCount > 0:
        output.notify('Input:')
        print(f'{c.DIM}{c.ITALIC}{x.RED}empty{c.END}' if len(prog) == 0 else inp)
        print()

    output.notify('Output:')
    Interpreter(prog, inp if inpCount else '')
    print()

    output.notify('Memory:')
    print(Tape)

    enterContinue()


def startApp(Which:str = 'R'):
    '''
    R: Read the .bf files
    C: Command line
    '''

    try:
        clear()
        if   Which == 'R': readBF() # Read addons/BrainFuck files
        elif Which == 'C': clliBF() # Command Line Language Interpreter
    except IndexError:
        print()
        output.notify('Memory:')
        print(Tape)
        print()
        output.error("Oops, I think you might've not added enough input.")
    except SyntaxError:
        print()
        output.notify('Memory:')
        print(Tape)
        print()
        output.error("Oops, I think you might've went out of memory.")

if __name__ == '__main__':
    startApp()