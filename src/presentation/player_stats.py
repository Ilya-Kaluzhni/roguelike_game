import curses


class PlayerStats:
    def __init__(self, stdscr, start_y, start_x):
        self.height = 5
        self.width = 80
        self.start_y = start_y
        self.start_x = start_x
        self.window = stdscr.subwin(self.height, self.width, self.start_y, self.start_x)

    def draw_stats(self, player_stats):
        self.window.clear()

        line = (
            f"Уровень: {player_stats['level']}    "
            f"Здоровье (Макс Здоровье): {player_stats['current_health']} ({player_stats['max_health']})    "
            f"Сила: {player_stats['strength']}    "
            f"Золото: {player_stats['gold']}"
        )

        self.window.addstr(1, 1, line)
        self.window.refresh()

