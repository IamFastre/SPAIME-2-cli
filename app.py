import os, sys, atexit

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

from res.main import *


def erase():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

atexit.register(erase)

try:
    run_app()
except:
    erase()
    exit()