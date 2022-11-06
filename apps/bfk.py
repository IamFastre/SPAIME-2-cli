import os, sys


def Interpreter(Program, Input):
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

os.system('cls')

try:
    with open(sys.argv[1], 'r') as File:
        prog = File.read()
except:
    prog = '-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>-----.---[->+++<]>.-[--->+<]>---.+++.------.--------.-[--->+<]>.'

print('Output:')
Interpreter(prog, None)

print('\nMemory:')
print(Tape)