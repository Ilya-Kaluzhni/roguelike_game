from curses import wrapper, curs_set

# from controller import Controller
from start_menu import StartScreen
from rules import RulesWindow
from map import GameMap
from render import RenderingActors
from interface import InterfaceBackpack
from enum import Enum
import curses
from player_stats import PlayerStats
from static import Keys
from message import MessageWindow


class MenuId(Enum):
    NEW_GAME = 1
    OLD_GAME = 2
    EXIT = 3


def create_data_windows(stdscr):
    screen_height, screen_width = stdscr.getmaxyx()

    width_rules = 21
    width_game = 80
    width_interface = 20

    height_rules = 15
    height_game = 25
    height_interface = 15
    height_stats = 3

    total_width = width_rules + width_game + width_interface
    start_y = (screen_height - max(height_rules, height_game, height_interface, height_stats)) // 2
    start_x = (screen_width - total_width) // 2

    win_rules = RulesWindow(stdscr, start_y, start_x)

    start_x_shift = start_x + win_rules.width
    win_message = MessageWindow(stdscr, start_y - 1, start_x_shift + 1)

    win_game = RenderingActors(stdscr, start_y, start_x_shift)

    start_x_shift += win_game.width

    win_backpack = InterfaceBackpack(stdscr, start_y, start_x_shift)

    start_y += win_game.height

    start_x_shift -= win_game.width

    win_stats = PlayerStats(stdscr, start_y, start_x_shift)

    return win_message, win_rules, win_game, win_backpack, win_stats


def main(stdscr):
    curses.curs_set(0)
    start_screen = StartScreen(stdscr)
    next_step = start_screen.screen()
    # stdscr.clear()
    if next_step == MenuId.EXIT.value:
        return

    rooms = [
        {'x': 5, 'y': 3, 'width': 8, 'height': 6},
        {'x': 20, 'y': 3, 'width': 10, 'height': 6},
        {'x': 35, 'y': 3, 'width': 9, 'height': 6},

        {'x': 5, 'y': 12, 'width': 7, 'height': 7},
        {'x': 20, 'y': 12, 'width': 11, 'height': 7},
        {'x': 35, 'y': 12, 'width': 9, 'height': 7}
    ]
    corridors = [
        # горизонтальные коридоры между комнатами в каждом ряду
        {'x': 13, 'y': 6, 'width': 7, 'height': 2},
        {'x': 30, 'y': 6, 'width': 5, 'height': 2},

        {'x': 12, 'y': 15, 'width': 8, 'height': 2},
        {'x': 31, 'y': 15, 'width': 5, 'height': 2},

        {'x': 9, 'y': 9, 'width': 3, 'height': 3},
        {'x': 24, 'y': 9, 'width': 3, 'height': 3},
        {'x': 40, 'y': 9, 'width': 3, 'height': 3},
    ]
    player_stats = {
        "level": 5,
        "current_health": 35,
        "max_health": 50,
        "strength": 8,
        "gold": 120
    }
    items = [
        {'x': 7, 'y': 5, 'type': 'w'},  # оружие
        {'x': 21, 'y': 6, 'type': 'f'},  # еда
        {'x': 6, 'y': 14, 'type': 'e'},  # эликсир
        {'x': 8, 'y': 15, 'type': 's'},  # свиток
        {'x': 8, 'y': 6, 'type': 't'},  # сокровище
    ]
    monsters = [
        {'x': 10, 'y': 7, 'type': 'G'},
        {'x': 38, 'y': 17, 'type': 'O'},
        {'x': 23, 'y': 15, 'type': 'S'},
        {'x': 27, 'y': 4, 'type': 'V'},
        {'x': 40, 'y': 7, 'type': 'Z'},
    ]
    weapons = [
        "Короткий меч",
        "Длинный меч",
        "Боевой топор",
        "Кинжал",
        "Лук",
        "Боевой молот",
        "Боевой молот",
        "Боевой молот",
        "Боевой молот",
        "Боевой молот"
    ]
    foods = [
        "Хлеб",
        "Яблоко",
        "Мясо",
        "Сыр",
        "Ягоды",
        "Рыба"
    ]
    elixirs = [
        "Эликсир исцеления",
        "Мана эликсир",
        "Сила зверя",
        "Стойкость к огню",
        "Зелье ночного зрения"
    ]
    scrolls = [
        "Свиток огненного шара",
        "Свиток телепортации",
        "Свиток невидимости",
        "Свиток защиты",
        "Свиток обнаружения ловушек"
    ]
    message = 'Сообщение из бэка(при необходимости)'
    win_message, win_rules, win_game, win_backpack, win_stats = create_data_windows(stdscr)

    game_map = GameMap()
    game_map.add_rooms(rooms)
    game_map.add_corridors(corridors)

    player_pos = (8, 4)
    win_game.setup_game_objects(game_map, player_pos, monsters, items)

    if next_step == MenuId.NEW_GAME.value:

        win_rules.draw_controls()
        win_game.update(player_pos, monsters, items)
        win_backpack.show_panel()
        win_stats.draw_stats(player_stats)
        width, height = 80, 40
        curses.doupdate()
        while True:

            key = stdscr.getch()
            win_message.clear()

            if key == 0x1B:
                break
            if message:
                win_message.draw_line(message)

            if key in Keys.Q_CLOSE.value:
                win_backpack.show_panel()
                win_rules.clear()
            elif key in Keys.W_UP.value:
                player_pos = (player_pos[0], max(0, player_pos[1] - 1))
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)
                # controller.get_input_give_update(Keys.W_UP)
            elif key in Keys.A_LEFT.value:
                player_pos = (max(0, player_pos[0] - 1), player_pos[1])
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)
                # controller.get_input_give_update(Keys.A_LEFT)
            elif key in Keys.S_DOWN.value:
                player_pos = (player_pos[0], min(height - 1, player_pos[1] + 1))
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)
                # controller.get_input_give_update(Keys.S_DOWN)
            elif key in Keys.D_RIGHT.value:
                player_pos = (min(width - 1, player_pos[0] + 1), player_pos[1])
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)
            elif key in Keys.H_USE_WEAPON.value:
                win_backpack.show_current_items('weapon', weapons)
                win_rules.clear()
                # controller.get_input_give_update(Keys.H_USE_WEAPON)
            elif key in Keys.J_USE_FOOD.value:
                win_backpack.show_current_items('food', foods)
                win_rules.clear()
                # controller.get_input_give_update(Keys.J_USE_FOOD)
            elif key in Keys.K_USE_ELIXIR.value:
                win_backpack.show_current_items('elixir', elixirs)
                win_rules.clear()
                # controller.get_input_give_update(Keys.K_USE_ELIXIR)
            elif key in Keys.E_USE_SCROLL.value:
                win_backpack.show_current_items('scroll', scrolls)
                win_rules.clear()
                # controller.get_input_give_update(Keys.E_USE_SCROLL)
            curses.doupdate()
            # message = ''

    elif next_step == MenuId.OLD_GAME.value:
        pass


wrapper(main)
