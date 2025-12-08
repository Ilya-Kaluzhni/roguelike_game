# /Users/ilya/roguelike_game/src7/presentation/screen.py
import curses
from curses import wrapper
from datetime import datetime

from domain.controller import Controller
from domain.character import Character
from domain.backpack import Backpack
from presentation.start_menu import StartScreen
from presentation.rules import RulesWindow
from domain.map import GameMap
from presentation.render import RenderingActors
from presentation.interface import InterfaceBackpack
from domain.player_stats import PlayerStats
from presentation.static import Keys
from presentation.message import MessageWindow
from enum import Enum
from datalayer.datalayer import GameSaveManager, LeaderboardManager, StatisticsManager

import locale
locale.setlocale(locale.LC_ALL, '')

from domain.map_generate import MapGenerator



class MenuId(Enum):
    NEW_GAME = 1
    CONTINUE_GAME = 2
    LEADERBOARD = 3
    EXIT = 4


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
    win_game.create_mini_window(stdscr, win_rules.height - 3, win_rules.width, start_y + win_rules.height, start_x)

    start_x_shift += win_game.width
    win_backpack = InterfaceBackpack(stdscr, start_y, start_x_shift)

    start_y += win_game.height
    start_x_shift -= win_game.width
    win_stats = PlayerStats(stdscr, start_y, start_x_shift)

    return win_message, win_rules, win_game, win_backpack, win_stats

def show_leaderboard(stdscr, stats_manager):
    """Показывает таблицу лидеров"""
    leaderboard_manager = LeaderboardManager(stats_manager)
    
    curses.curs_set(1)
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== ТАБЛИЦА ЛИДЕРОВ ===\n\n", curses.A_BOLD)
        
        leaderboard = leaderboard_manager.get_leaderboard_by_level(limit=10)
        stdscr.addstr(f"{'Ранг':<5} {'Уровень':<10} {'Золото':<10} {'Дата':<20}\n")
        stdscr.addstr('-' * 50 + '\n')
        
        for rank, attempt in enumerate(leaderboard, 1):
            date = datetime.fromisoformat(attempt['timestamp']).strftime('%Y-%m-%d %H:%M')
            line = f'{rank:<5} {attempt["level_reached"]:<10} {attempt["gold"]:<10} {date:<20}\n'
            stdscr.addstr(line)
        
        stdscr.addstr('\nНажмите ESC для выхода\n')
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == 0x1B:  # Esc
            break
    curses.curs_set(0)

def main(stdscr):
    curses.curs_set(0)
    save_manager = GameSaveManager()
    stats_manager = StatisticsManager()
    
    start_screen = StartScreen(stdscr)
    
    # Используем существующий метод screen()
    menu_result = start_screen.screen()
    
    if menu_result == 3:  # EXIT
        return
    elif menu_result == 1:  # NEW_GAME
        menu_result = MenuId.NEW_GAME.value
    elif menu_result == 2:  # OLD_GAME — проверяем наличие сохранения
        if save_manager.has_save():
            menu_result = MenuId.CONTINUE_GAME.value
        else:
            menu_result = MenuId.NEW_GAME.value
    
    if menu_result == MenuId.EXIT.value:
        return
    
    win_message, win_rules, win_game, win_backpack, win_stats = create_data_windows(stdscr)

    controller = Controller()
    
    # Если продолжаем игру — загружаем сохранённое состояние
    if menu_result == MenuId.CONTINUE_GAME.value and save_manager.has_save():
        save_data = save_manager.load_game()
        if save_data:
            # Загружаем состояние в контроллер
            controller.back.load_from_save(save_data)
            # Получаем актуальное состояние после загрузки
            data = controller.get_input_give_update(0)
        else:
            # Если ошибка загрузки — начинаем заново
            data = controller.get_input_give_update(0)
    else:
        # Новая игра
        data = controller.get_input_give_update(0)

    # создаём карту
    game_map = GameMap()
    game_map.add_rooms(data['rooms'])
    game_map.add_corridors(data['corridors'])

    # игровые данные
    player_pos   = data['player']['cords']
    player_stats = data['player']
    monsters     = data['enemies']
    message      = data['message']
    items = data['items']

    win_game.setup_game_objects(game_map, player_pos, monsters, items)

    current_level = data.get('level', 1)

    if menu_result in [MenuId.NEW_GAME.value, MenuId.CONTINUE_GAME.value]:
        # Инициализируем UI для обоих случаев (новая игра и загрузка)
        win_rules.draw_controls()
        win_backpack.show_panel()
        win_stats.draw_stats(player_stats)
        win_game.update(player_pos, monsters, items)
        curses.doupdate()

        while True:
            key = stdscr.getch()
            if key == -1:
                continue

            win_message.clear()

            data = controller.get_input_give_update(key)
            
            # Проверяем game_over перед обращением к данным
            if data.get('game_over'):
                # Показываем экран завершения игры
                stdscr.clear()
                stdscr.addstr(0, 0, "=== КОНЕЦ ИГРЫ ===\n\n", curses.A_BOLD)
                stdscr.addstr(2, 0, f"Уровень достигнут: {data.get('level', 1)}\n")
                stdscr.addstr(3, 0, f"Золото: {data.get('gold', 0)}\n")
                stdscr.addstr(4, 0, f"Врагов повержено: {data.get('enemies_defeated', 0)}\n")
                stdscr.addstr(6, 0, "Нажмите ESC для выхода в главное меню\n")
                stdscr.refresh()
                
                key = stdscr.getch()
                if key == 0x1B:  # Esc
                    break
                continue
            
            player_pos   = data['player']['cords']
            player_stats = data['player']
            monsters     = data['enemies']
            items = data['items']
            message      = data['message']

            # если уровень сменился — пересобираем GameMap и перенастраиваем win_game
            if data.get('level_changed'):
                game_map = GameMap()
                game_map.add_rooms(data['rooms'])
                game_map.add_corridors(data['corridors'])
                game_map.update_visibility(player_pos[0], player_pos[1])
                win_game.setup_game_objects(game_map, player_pos, monsters, items)
                current_level = data.get('level', current_level)
                win_rules.draw_controls()
                win_backpack.show_panel()
            else:
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
                win_game.set_direction('up')
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)
            elif key in Keys.A_LEFT.value:
                win_game.set_direction('left')
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)
            elif key in Keys.S_DOWN.value:
                win_game.set_direction('down')
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)
            elif key in Keys.D_RIGHT.value:
                win_game.set_direction('right')
                win_game.update(player_pos, monsters, items)
                win_rules.press_btn(key)

            # инвентарь
            elif key in Keys.H_USE_WEAPON.value:
                win_backpack.show_current_items('weapon', data['weapon'])
                win_rules.clear()
            elif key in Keys.J_USE_FOOD.value:
                win_backpack.show_current_items('food', data['food'])
                win_rules.clear()
            elif key in Keys.K_USE_ELIXIR.value:
                win_backpack.show_current_items('elixir', data['elixir'])
                win_rules.clear()
            elif key in Keys.E_USE_SCROLL.value:
                win_backpack.show_current_items('scroll', data['scroll'])
                win_rules.clear()
            elif key in Keys.P_GO_3D.value:
                win_game.go_tride()
                win_game.update(player_pos, monsters, items)

            if ord('0') <= key <= ord('9'):
                win_backpack.show_panel()
            
            win_stats.draw_stats(player_stats)
            curses.doupdate()


wrapper(main)
