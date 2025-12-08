import os
import sys
from curses import wrapper

SCRIPT_DIR = os.path.dirname(__file__)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from presentation import screen

def main():
    wrapper(screen.main)

if __name__ == "__main__":
    main()
