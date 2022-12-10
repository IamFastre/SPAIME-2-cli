import sys
from os.path import abspath, dirname, join

# Sets path to the app's main folder
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from scripts.libs import *

output.error(f"Haha. {X0.GREEN}it's green")