import curses
import time
from enum import Enum


class MenuId(Enum):
    NEW_GAME = 1,
    OLD_GAME = 2,
    EXIT = 3

class StartScreen:
    wave_offsets = [0, 1, 2, 1, 0, -1, -2, -1]

    def __init__(self, stdscr, base_y=10, base_x=10):
        self.stdscr = stdscr
        self.base_y = base_y
        self.base_x = base_x
        self.counter = 0
        self.input_str = ""
        self.get_name = True
        self.command = "Введите имя:"
        self.menu_items = ["Новая игра", "Загрузка старой игры", "Выход"]
        self.current_row = 0

        self.letters = {
            'R': [
                "////  ",
                "/   / ",
                "////  ",
                "/  /  ",
                "/   / "
            ],
            'O': [
                " //// ",
                "/    /",
                "/    /",
                "/    /",
                " //// "
            ],
            'G': [
                " //// ",
                "/     ",
                "/  ///",
                "/    /",
                " //// "
            ],
            'U': [
                "/    /",
                "/    /",
                "/    /",
                "/    /",
                " //// "
            ],
            'E': [
                "//////",
                "/     ",
                "////  ",
                "/     ",
                "//////"
            ],
        }

    def draw_letter(self, art_lines, y, x):
        for i, line in enumerate(art_lines):
            for j, ch in enumerate(line):
                try:
                    if ch == '/':
                        self.stdscr.addch(y + i, x + j, curses.ACS_BLOCK)
                    else:
                        self.stdscr.addch(y + i, x + j, ch)
                except curses.error:
                    pass

    def shift_letters(self, base_y, base_x):
        offsets = []
        for i in range(5):
            idx = (self.counter + i * 2) % len(self.wave_offsets)
            offsets.append(self.wave_offsets[idx])
        letters_order = ['R', 'O', 'G', 'U', 'E']
        for i, letter in enumerate(letters_order):
            self.draw_letter(self.letters[letter], base_y + offsets[i], base_x + i * 7)

    def get_player_name(self, base_y, base_x):
        self.stdscr.addstr(base_y, base_x, self.command)
        self.stdscr.addstr(base_y + 1, base_x, self.input_str + "_")

    def show_menu(self, base_y, base_x):
        for idx, row in enumerate(self.menu_items):
            x = base_x - len(row) // 2 - 5
            y = base_y + idx
            if idx == self.current_row:
                self.stdscr.attron(curses.A_REVERSE)
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.A_REVERSE)
            else:
                self.stdscr.addstr(y, x, row)

    def draw_menu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        self.shift_letters(5, w // 2 - 20)
        if self.get_name:
            self.get_player_name(h - 10, w // 2 - 20)
        else:
            self.show_menu(h - 10, w // 2)
        self.counter = (self.counter + 1) % len(self.wave_offsets)
        self.stdscr.refresh()

    def processing_enter(self):
        if self.get_name:
            if not self.input_str:
                self.command = "Необходимо ввести имя:"
            else:
                self.get_name = False
        else:
            self.go_on = self.current_row + 1

    def screen(self):
        self.stdscr.nodelay(True)
        curses.curs_set(0)

        while True:
            self.draw_menu()

            time_for_sleep = 0.3
            ch = self.stdscr.getch()
            if ch != -1:
                if chr(ch) == 'q':
                    break
                if ch in (10, 13):
                    if self.get_name:
                        if not self.input_str:
                            self.command = "Необходимо ввести имя:"
                        else:
                            self.get_name = False
                    else:
                        break
                elif ch in (8, 127):
                    self.input_str = self.input_str[:-1]
                elif 32 <= ch <= 126:
                    self.input_str += chr(ch)
                elif ch == curses.KEY_UP:
                    self.current_row = (self.current_row - 1) % len(self.menu_items)
                elif ch == curses.KEY_DOWN:
                    self.current_row = (self.current_row + 1) % len(self.menu_items)

                # Исправить на esc!
                if ch == 113:
                    break
                time_for_sleep = 0.1

            time.sleep(time_for_sleep)
        self.stdscr.clear()
        return self.current_row + 1
