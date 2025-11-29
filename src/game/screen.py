# /Users/ilya/roguelike_game/src7/presentation/screen.py
import curses
from curses import wrapper

from controller import Controller
# from controller import Controller
from start_menu import StartScreen
from rules import RulesWindow
from map import GameMap
from render import RenderingActors
from interface import InterfaceBackpack
from player_stats import PlayerStats
from static import Keys
from message import MessageWindow
from enum import Enum

import locale
locale.setlocale(locale.LC_ALL, '')

#from domain.game.loop import GameLoop
#from domain.game.session import GameSession
from map_generate import MapGenerator
# from ./domain.map_generate.map_generate import MapGenerator
#from domain.movement.directions import Directions


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
    with open('a.log', 'a') as f:
        f.write('Начало\n')

    curses.curs_set(0)
    start_screen = StartScreen(stdscr)
    next_step = start_screen.screen()

    if next_step == MenuId.EXIT.value:
        return

    # создаём окна интерфейса
    win_message, win_rules, win_game, win_backpack, win_stats = create_data_windows(stdscr)

    # --- Генерация карты через контроллер ---
    controller = Controller()
    data = controller.get_input_give_update('start')

    with open('d.log', 'a') as f:
        f.write(str(data))

    # создаём карту
    game_map = GameMap()
    game_map.add_rooms(data['rooms'])
    game_map.add_corridors(data['corridors'])
    game_map.place_items()                    # ← размещаем предметы

    # игровые данные
    player_pos   = data['player']['cords']
    player_stats = data['player']
    monsters     = data['enemies']
    message      = data['message']

    # ВАЖНО! Передаём предметы из карты:
    items = game_map.get_render_items()                    # ← теперь предметы ВСЕГДА корректные
    with open('items.log', 'a') as f:
        f.write(str(items) + "\n")
    # передаем всё в renderer
    win_game.setup_game_objects(game_map, player_pos, monsters, items)

    # справочники для инвентаря
    weapons = ["Короткий меч", "Длинный меч", "Боевой топор", "Кинжал", "Лук", "Боевой молот"]
    foods   = ["Хлеб", "Яблоко", "Мясо", "Сыр", "Ягоды", "Рыба"]
    elixirs = ["Эликсир исцеления", "Мана эликсир", "Сила зверя", "Стойкость к огню", "Зелье ночного зрения"]
    scrolls = ["Свиток огненного шара", "Свиток телепортации", "Свиток невидимости", "Свиток защиты", "Свиток обнаружения ловушек"]

    if next_step == MenuId.NEW_GAME.value:

        win_rules.draw_controls()
        win_backpack.show_panel()
        win_stats.draw_stats(player_stats)

        # первый рендер
        win_game.update(player_pos, monsters, items)
        curses.doupdate()

        while True:
            key = stdscr.getch()
            if key == -1:
                continue

            win_message.clear()

            data = controller.get_input_give_update(key)
            player_pos   = data['player']['cords']
            player_stats = data['player']
            monsters     = data['enemies']
            message      = data['message']

            # ВСЕГДА обновляем предметы динамически
            items = game_map.get_render_items()
            win_game.update(player_pos, monsters, items)

            if key == 0x1B:      # Esc
                break

            if message:
                win_message.draw_line(message)

            # управление
            if key in Keys.Q_CLOSE.value:
                win_backpack.show_panel()
                win_rules.clear()

            elif key in Keys.W_UP.value:
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)

            elif key in Keys.A_LEFT.value:
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)

            elif key in Keys.S_DOWN.value:
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)

            elif key in Keys.D_RIGHT.value:
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)

            # инвентарь
            elif key in Keys.H_USE_WEAPON.value:
                win_backpack.show_current_items('weapon', weapons)
                win_rules.clear()

            elif key in Keys.J_USE_FOOD.value:
                win_backpack.show_current_items('food', foods)
                win_rules.clear()

            elif key in Keys.K_USE_ELIXIR.value:
                win_backpack.show_current_items('elixir', elixirs)
                win_rules.clear()

            elif key in Keys.E_USE_SCROLL.value:
                win_backpack.show_current_items('scroll', scrolls)
                win_rules.clear()

            win_stats.draw_stats(player_stats)
            curses.doupdate()

    elif next_step == MenuId.OLD_GAME.value:
        pass


wrapper(main)
