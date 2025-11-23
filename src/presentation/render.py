
import curses

class RenderingActors:
    def __init__(self, stdscr, game_map, player_coords, monsters, items):
        self.stdscr = stdscr
        self.game_map = game_map  # экземпляр класса GameMap
        self.player_x, self.player_y = player_coords
        self.monsters = monsters  # список монстров, каждый с атрибутами x, y, char, color
        self.items = items  # список предметов, каждый с атрибутами x, y, char, color

        # Инициализация цветовых пар для curses
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Игрок
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Стены, пол
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)      # Монстры
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Предметы

    def draw_map(self):
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                char = self.game_map.get_tile_display(x, y, self.player_x, self.player_y)
                if char == '#':
                    color = curses.color_pair(2)
                elif char == '.':
                    color = curses.color_pair(2)
                elif char == '+':
                    color = curses.color_pair(2)
                elif char == ',':
                    color = curses.color_pair(2) | curses.A_DIM  # туман
                else:
                    color = curses.color_pair(0)
                self.stdscr.addch(y, x, char, color)

    def draw_actors(self):
        for item in self.items:
            if self.game_map.visible[item.y][item.x]:
                self.stdscr.addch(item.y, item.x, item.char, curses.color_pair(4))

        for monster in self.monsters:
            if self.game_map.visible[monster.y][monster.x]:
                self.stdscr.addch(monster.y, monster.x, monster.char, curses.color_pair(3))

        self.stdscr.addch(self.player_y, self.player_x, '@', curses.color_pair(1) | curses.A_BOLD)

    def render(self):
        self.stdscr.clear()
        self.draw_map()
        self.draw_actors()
        self.stdscr.refresh()

    def update(self, player_coords, monsters, items):
        self.player_x, self.player_y = player_coords
        self.monsters = monsters
        self.items = items
        self.game_map.update_visibility(self.player_x, self.player_y)
        self.render()
