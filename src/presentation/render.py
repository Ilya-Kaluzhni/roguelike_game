# # # рендер локации, сущностей
import curses
import curses




class RenderingActors:
    def __init__(self, stdscr, game_map, player_coords, monsters=None, items=None, start_y=0, start_x=0):
        # self.stdscr = stdscr
        self.window = curses.newwin(30, 82, start_y, start_x + 5 + 21)  # высота, ширина, y, x позиции окна

        self.game_map = game_map
        self.player_x, self.player_y = player_coords
        self.monsters = monsters or []
        self.items = items or []

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Игрок
        curses.init_pair(2, curses.COLOR_WHITE, -1)  # Стены, пол
        curses.init_pair(3, curses.COLOR_RED, -1)  # Монстры
        curses.init_pair(4, curses.COLOR_YELLOW, -1)  # Предметы

    def draw_map(self):
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                ch = self.game_map.get_tile_display(x, y, self.player_x, self.player_y)
                if ch in ('#', '.', '+'):
                    color = curses.color_pair(0)
                    try:
                        self.window.addch(y, x, ch, color)
                    except curses.error:
                        pass
                # elif ch == ',':
                #     color = curses.color_pair(2) | curses.A_DIM
                # else:
                #     color = curses.color_pair(0)
                # try:
                #     self.window.addch(y, x, ch, color)
                # except curses.error:
                #     self.window.addch(y, x, '#', color)
                # except    TypeError:
                #     self.window.addch(y, x, '/', color)

    def draw_actors(self):
        for item in self.items:
            if self.game_map.visible[item.y][item.x]:
                self.window.addch(item.y, item.x, item.char, curses.color_pair(4))
        for monster in self.monsters:
            if self.game_map.visible[monster.y][monster.x]:
                self.window.addch(monster.y, monster.x, monster.char, curses.color_pair(3))
        self.window.addch(self.player_y, self.player_x, '@', curses.color_pair(1) | curses.A_BOLD)

    def render(self):
        self.window.clear()
        self.window.border()
        self.draw_map()
        self.draw_actors()
        self.window.refresh()

    def update(self, player_coords, monsters=None, items=None):
        self.player_x, self.player_y = player_coords
        self.monsters = monsters or []
        self.items = items or []
        self.game_map.update_visibility(self.player_x, self.player_y)
        self.render()


# def main(stdscr):
#     curses.curs_set(0)  # Скрыть курсор
#     width, height = 80, 40
#
#     game_map = GameMap()
#
#     # Пример комнат и коридоров
#     rooms = [
#         {'x': 5, 'y': 3, 'width': 8, 'height': 6},
#         {'x': 20, 'y': 3, 'width': 10, 'height': 6},
#         {'x': 35, 'y': 3, 'width': 9, 'height': 6},
#
#         {'x': 5, 'y': 12, 'width': 7, 'height': 7},
#         {'x': 20, 'y': 12, 'width': 11, 'height': 7},
#         {'x': 35, 'y': 12, 'width': 9, 'height': 7},
#
#         {'x': 5, 'y': 22, 'width': 8, 'height': 6},
#         {'x': 20, 'y': 22, 'width': 10, 'height': 6},
#         {'x': 35, 'y': 22, 'width': 9, 'height': 6},
#     ]
#
#     corridors = [
#         # горизонтальные коридоры между комнатами в каждом ряду
#         {'x': 13, 'y': 6, 'width': 7, 'height': 2},
#         {'x': 30, 'y': 6, 'width': 5, 'height': 2},
#
#         {'x': 12, 'y': 15, 'width': 8, 'height': 2},
#         {'x': 31, 'y': 15, 'width': 5, 'height': 2},
#
#         {'x': 13, 'y': 25, 'width': 7, 'height': 2},
#         {'x': 30, 'y': 25, 'width': 5, 'height': 2},
#
#         # вертикальные коридоры между рядами
#         {'x': 9, 'y': 9, 'width': 3, 'height': 6},
#         {'x': 24, 'y': 9, 'width': 3, 'height': 6},
#         {'x': 40, 'y': 9, 'width': 3, 'height': 6},
#     ]
#
#     game_map.add_rooms(rooms)
#     game_map.add_corridors(corridors)
#
#     player_pos = (12, 8)
#     monsters = []  # Можно добавить объекты с атрибутами x, y, char
#     items = []  # Аналогично
#
#     renderer = RenderingActors(stdscr, game_map, player_pos, monsters, items)
#
#     while True:
#         renderer.update(player_pos)
#         key = stdscr.getch()
#
#         if key == ord('q'):
#             break
#         elif key == curses.KEY_UP:
#             player_pos = (player_pos[0], max(0, player_pos[1] - 1))
#         elif key == curses.KEY_DOWN:
#             player_pos = (player_pos[0], min(height - 1, player_pos[1] + 1))
#         elif key == curses.KEY_LEFT:
#             player_pos = (max(0, player_pos[0] - 1), player_pos[1])
#         elif key == curses.KEY_RIGHT:
#             player_pos = (min(width - 1, player_pos[0] + 1), player_pos[1])
#
#
# if __name__ == "__main__":
#     curses.wrapper(main)
