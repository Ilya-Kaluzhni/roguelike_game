import curses


class RulesWindow:
    def __init__(self, stdscr,screen_height, screen_width):
        self.height = 15
        self.width = 21
        self.start_y = screen_height
        self.start_x = screen_width
        self.win = stdscr.subwin(self.height, self.width, self.start_y, self.start_x)
        self.win.box()
        self.btn_w = self.win.derwin(3, 5, 3, (self.width // 2) - 2)
        self.btn_a = self.win.derwin(3, 5, 6, 3)
        self.btn_s = self.win.derwin(3, 5, 6, (self.width // 2) - 2)
        self.btn_d = self.win.derwin(3, 5, 6, self.width - 8)
        self.current_key = None
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.normal_color = curses.color_pair(10)
        self.active_color = curses.color_pair(11)

    def draw_controls(self):
        self.win.erase()
        self.win.box()
        title = 'Управление'
        self.win.addstr(1, (self.width - len(title)) // 2, title)

        for btn in (self.btn_w, self.btn_a, self.btn_s, self.btn_d):
            btn.erase()
            btn.box()

        self.btn_w.addstr(1, 2, 'W', curses.A_BOLD)
        self.btn_a.addstr(1, 2, 'A', curses.A_BOLD)
        self.btn_s.addstr(1, 2, 'S', curses.A_BOLD)
        self.btn_d.addstr(1, 2, 'D', curses.A_BOLD)

        self.win.addstr(2, (self.width // 2) - 2, 'Вверх', curses.A_DIM)
        self.win.addstr(9, 3, 'Влево', curses.A_DIM)
        self.win.addstr(9, (self.width // 2) - 1, 'Низ', curses.A_DIM)
        self.win.addstr(9, self.width - 8, 'Вправо', curses.A_DIM)
        self.win.addstr(11, 3, 'Атака: движение')
        self.win.addstr(12, 3, 'по направлению')
        self.win.addstr(13, 3, 'к противнику')

        self.win.noutrefresh()
        self.btn_w.noutrefresh()
        self.btn_a.noutrefresh()
        self.btn_s.noutrefresh()
        self.btn_d.noutrefresh()

    def _draw_button(self, btn_window, char, active=False):
        color = self.active_color if active else self.normal_color
        btn_window.bkgd(' ', color)
        btn_window.erase()
        btn_window.attron(color)
        btn_window.box()
        btn_window.attroff(color)
        btn_window.addstr(1, 2, char, curses.A_BOLD | color)
        btn_window.noutrefresh()

    def press_btn(self, key_char):
        key_char = chr(key_char).upper()

        if self.current_key and self.current_key != key_char:
            self._draw_button(getattr(self, f'btn_{self.current_key.lower()}'), self.current_key, active=False)

        self.current_key = key_char
        self._draw_button(getattr(self, f'btn_{key_char.lower()}'), key_char, active=True)


# def main(stdscr):
#     curses.curs_set(0)
#     stdscr.clear()
#     start_y, start_x = stdscr.getmaxyx()
#
#     ctrl_win = RulesWindow(stdscr, start_y, start_x)
#     ctrl_win.draw_controls()
#
#     stdscr.getch()
#
#
# if __name__ == "__main__":
#     curses.wrapper(main)
