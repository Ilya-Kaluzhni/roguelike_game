# # # рендер локации, сущностей
import curses
import curses


class RenderingActors:
    def __init__(self, stdscr, game_map, player_coords, monsters=None, items=None, start_y=0, start_x=0):
        self.window = stdscr.subwin(30, 82, start_y, start_x + 5 + 21)

        self.game_map = game_map
        self.player_x, self.player_y = player_coords
        self.monsters = monsters or []
        self.monsters_data = {
            'Z': 32,
            'G': 30,
            'O': 35,
            'V': 31,
            'S': 30
        }

        self.items = items
        self.items_data = {
            'w': [31, curses.ACS_UARROW],
            'f': [32, '♣'],
            'e': [33, curses.ACS_PLMINUS],
            's': [34, curses.ACS_DIAMOND],
            't': [35, '*']
        }
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Игрок
        curses.init_pair(2, curses.COLOR_WHITE, -1)  # Стены, пол

        curses.init_pair(30, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(31, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(32, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(33, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(34, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(35, curses.COLOR_YELLOW, curses.COLOR_BLACK)




    def draw_map(self):
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                ch = self.game_map.get_tile_display(x, y)
                if ch in ('#', '.', '+', ','):
                    color = curses.color_pair(0)
                    if ch ==',':
                        ch = '.'
                        color = curses.color_pair(2) | curses.A_DIM
                    try:
                        self.window.addch(y, x, ch, color)
                    except curses.error:
                        pass


    def draw_actors(self):
        self.draw_items()
        self.draw_monsters()
        self.window.addch(self.player_y, self.player_x, '@', curses.color_pair(1) | curses.A_BOLD)

    def draw_items(self):
        for item in self.items:
            if self.game_map.visible[item['y']][item['x']]:
                ch = self.items_data[item['type']][1]
                color_n = self.items_data[item['type']][0]
                self.window.addch(item['y'], item['x'], ch, curses.color_pair(color_n))

    def draw_monsters(self):
        for monster in self.monsters:
            if self.game_map.visible[monster['y']][monster['x']]:
                color_n = self.monsters_data[monster['type']]
                self.window.addch(monster['y'], monster['x'], monster['type'], curses.color_pair(color_n))

    def render(self):
        self.window.clear()
        self.window.border()
        self.draw_map()
        self.draw_actors()
        self.window.refresh()

    def update(self, player_coords, monsters=None, items=None):
        self.player_x, self.player_y = player_coords
        self.monsters = monsters or []
        self.items = items
        self.game_map.update_visibility(self.player_x, self.player_y)
        self.render()
