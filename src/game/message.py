class MessageWindow:
    def __init__(self, stdscr, start_y, start_x):
        self.height = 1
        self.width = 100
        self.window = stdscr.subwin(self.height, self.width, start_y, start_x)
        self.start_y = start_y
        self.start_x = start_x

    def draw_line(self, text):
        self.window.erase()
        # Ограничиваем длину текста шириной окна
        display_text = text[:self.width]
        self.window.addstr(0, 0, display_text)
        self.window.noutrefresh()

    def clear(self):
        self.window.erase()
        self.window.noutrefresh()
