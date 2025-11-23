from curses import wrapper
from start_menu import StartScreen

def main(stdscr):
    start_screen = StartScreen(stdscr)
    start_screen.screen()


wrapper(main)