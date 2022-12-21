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
from scripts.libs   import *
from scripts.colors import *
from time           import *

print('Test')
sleep(0.5)