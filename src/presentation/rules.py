import curses


class RulesWindow:
    def __init__(self, stdscr,  screen_height,screen_width):
        self.height = 11
        self.width = 21
        self.start_y = screen_height
        self.start_x = screen_width
        self.win = stdscr.subwin(self.height, self.width, self.start_y, self.start_x)
        self.win.box()
        # Используем derwin для координат внутри self.win
        self.btn_w = self.win.derwin(3, 5, 3, (self.width // 2) - 2)
        self.btn_a = self.win.derwin(3, 5, 6, 3)
        self.btn_s = self.win.derwin(3, 5, 6, (self.width // 2) - 2)
        self.btn_d = self.win.derwin(3, 5, 6, self.width - 8)

    def draw_controls(self):
        self.win.erase()
        self.win.box()
        title = 'Движение'
        self.win.addstr(1, (self.width - len(title)) // 2, title, curses.A_DIM)

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

        self.win.refresh()
        self.btn_w.refresh()
        self.btn_a.refresh()
        self.btn_s.refresh()
        self.btn_d.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    start_y, start_x = stdscr.getmaxyx()

    ctrl_win = RulesWindow(stdscr, start_y, start_x)
    ctrl_win.draw_controls()

    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
