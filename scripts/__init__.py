####################################################################
##                                                                ##
##    Importing important files, modules, packages and so on.     ##
##                                                                ##
####################################################################


# Copy thins snippet everywhere please!
import sys
from os.path import abspath, dirname, join
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

# So we can happily fry your device
sys.setrecursionlimit(100_000_000)

# Importing required packages and my scripts
from scripts.__req__     import *
from scripts.content import *

# Importing my package files:
from scripts.libs   import *
from scripts.colors import *
from time           import *

