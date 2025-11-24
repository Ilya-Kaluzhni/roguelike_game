from curses import wrapper, curs_set
from start_menu import StartScreen
from rules import RulesWindow
from map import GameMap
from render import RenderingActors
from interface import InterfaceBackpack
from enum import Enum
import curses


class MenuId(Enum):
    NEW_GAME = 1
    OLD_GAME = 2
    EXIT = 3

def create_windows(stdscr):
    screen_height, screen_width = stdscr.getmaxyx()
    spacing = 5

    width1 = 21
    width2 = 82
    width3 = 40

    height1 = 10
    height2 = 27
    height3 = 10

    total_width = width1 + spacing + width2 + spacing + width3
    start_x = max((screen_width - total_width) // 2, 0)

    start_y1 = max((screen_height - height1) // 2, 0)
    start_y2 = max((screen_height - height2) // 2, 0)
    start_y3 = max((screen_height - height3) // 2, 0)

def main(stdscr):
    start_screen = StartScreen(stdscr)
    next_step = start_screen.screen()
    # stdscr.clear()
    next_step =1

    if next_step == MenuId.EXIT.value:
        return
    # curs_set(0)
    # Левая панель
    screen_height,screen_width = stdscr.getmaxyx()
    width1, width2, width3 = 21, 82, 20
    spacing = 5
    total_width = width1 + spacing + width2 + spacing + width3
    total_height = 27
    start_y = 10
    start_x = max((screen_width - total_width) // 2, 0)
    win_rules = RulesWindow(stdscr, start_y, start_x)


    # Игровая панель
    game_map = GameMap(1,2)

    rooms = [
        {'x': 5, 'y': 3, 'width': 8, 'height': 6},
        {'x': 20, 'y': 3, 'width': 10, 'height': 6},
        {'x': 35, 'y': 3, 'width': 9, 'height': 6},

        {'x': 5, 'y': 12, 'width': 7, 'height': 7},
        {'x': 20, 'y': 12, 'width': 11, 'height': 7},
        {'x': 35, 'y': 12, 'width': 9, 'height': 7},
        #
        # {'x': 5, 'y': 22, 'width': 8, 'height': 6},
        # {'x': 20, 'y': 22, 'width': 10, 'height': 6},
        # {'x': 35, 'y': 22, 'width': 9, 'height': 6},
    ]

    corridors = [
        # горизонтальные коридоры между комнатами в каждом ряду
        {'x': 13, 'y': 6, 'width': 7, 'height': 2},
        {'x': 30, 'y': 6, 'width': 5, 'height': 2},

        {'x': 12, 'y': 15, 'width': 8, 'height': 2},
        {'x': 31, 'y': 15, 'width': 5, 'height': 2},
        #
        # {'x': 13, 'y': 25, 'width': 7, 'height': 2},
        # {'x': 30, 'y': 25, 'width': 5, 'height': 2},
        #
        # # вертикальные коридоры между рядами
        {'x': 9, 'y': 9, 'width': 3, 'height': 3},
        {'x': 24, 'y': 9, 'width': 3, 'height': 3},
        {'x': 40, 'y': 9, 'width': 3, 'height': 3},
    ]

    game_map.add_rooms(rooms)
    game_map.add_corridors(corridors)

    player_pos = (8, 4)
    monsters = []
    items = []
    start_y2 = max((screen_height - 27) // 2, 0)
    win_game = RenderingActors(stdscr, game_map, player_pos, monsters, items, start_y,start_x)
    # win2 = stdscr.subwin(27, 82, start_y, start_x + width1 + spacing)
    # win2.border()
    # win2.refresh()

    backpack_y = start_y
    backpack_x = start_x + width1 + spacing + width2 + spacing
    backpack_height = 15
    backpack_width = 20
    win_backpack = InterfaceBackpack(stdscr, height=backpack_height, width=backpack_width, begin_y=backpack_y,
                                 begin_x=backpack_x)




    if next_step == MenuId.NEW_GAME.value:

        win_rules.draw_controls()
        win_game.update(player_pos)
        win_backpack.show_panel()
        # stdscr.refresh()
        # win_game.update(player_pos)
        width, height = 80, 40
        win_rules.draw_controls()
        win_game.update(player_pos)
        win_backpack.show_panel()
        stdscr.refresh()
        while True:

            key = stdscr.getch()

            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                player_pos = (player_pos[0], max(0, player_pos[1] - 1))
                win_game.update(player_pos)
            elif key == curses.KEY_DOWN:
                player_pos = (player_pos[0], min(height - 1, player_pos[1] + 1))
                win_game.update(player_pos)
            elif key == curses.KEY_LEFT:
                player_pos = (max(0, player_pos[0] - 1), player_pos[1])
                win_game.update(player_pos)
            elif key == curses.KEY_RIGHT:
                player_pos = (min(width - 1, player_pos[0] + 1), player_pos[1])
                win_game.update(player_pos)
    elif next_step == MenuId.OLD_GAME.value:
        pass
    # win1.noutrefresh()
    # win2.noutrefresh()
    # curses.doupdate()




wrapper(main)
