# from check.roguelike_game.src7.game.mimic import Mimic
from static import Keys
# from core.movement.directions import Directions
# from session import GameSession
from map_generate import MapGenerator
from character import Character
from backpack import Backpack
from ghost import Ghost
from zombie import Zombie
from mimic import Mimic
from vampire import Vampire
from ogre import Ogre
from snake import Snake
from enemy_movement import MoveEnemy
from random import randint, choice
from fight import Fight
from items import Item
from datalayer import GameSaveManager, StatisticsManager
import time
from typing import Dict


class GameController:
    """
    Класс, который управляет игрой, принимает ввод игрока и обновляет состояние игры.
    """

    def __init__(self):
        self.game_map = MapGenerator()
        self.backpack = Backpack()
        self.character = Character(0, 0, self.backpack)
        self.message = ''
        self.move_enemy = None
        self.enemies = []
        self.items = []
        self.battles = []
        self.level = None
        self.n_level = 1
        self.level_changed = False
        
        # Инициализируем слой данных
        self.save_manager = GameSaveManager()
        self.stats_manager = StatisticsManager()
        self.start_time = time.time()
        self.enemies_defeated = 0
        
        self.load_level()

    def start(self):
        self.load_level()

    def load_level(self):
        """Генерирует новый уровень и размещает игрока."""
        # ---- теперь всё правильно ----
        self.level = self.game_map.generate_level()
        self.move_enemy = MoveEnemy(self.game_map)

        self.character.set_cords(*self.game_map.set_player_cords())
        self.enemies = self.spawn_enemies()

        self.spawn_items()
        self.battles = [None] * len(self.enemies)
        self.level_changed = False

    def spawn_items(self):
        num_items = 9
        while num_items:
            cell = choice(self.level[2])
            if self.game_map.can_set_smth(*cell):
                item = choice([
                    Item("food", "яблоко", health=5,letter='f'),
                    Item("potion", "зелье лечения", health=15,letter='e'),
                    Item("weapon", "кинжал", strength=1,letter='w'),
                    Item("treasure", "монеты", value=20,letter='t'),
                ])
                item.set_cords(*cell)

                self.game_map.tiles[cell[1]][cell[0]] = item.letter
                self.items.append(item)
                num_items -= 1

    def spawn_enemies(self):
        """Создаёт врагов в случайных комнатах."""
        if self.n_level == 1:
            enemy_types = [Ogre, Ghost]
        elif 2 <= self.n_level < 4:
            enemy_types = [Mimic, Zombie, Ogre]
        elif 4 <= self.n_level <= 6:
            enemy_types = [Zombie, Ogre, Vampire]
        else:
            enemy_types = [Mimic, Zombie, Vampire, Ogre, Snake]

            # Увеличиваем количество врагов с каждым уровнем
        num_enemies = 3 + self.n_level - 1  # Пример увеличения врагов с уровнем (не больше 20 врагов)
        # num_enemies = 1
        enemies = []
        while num_enemies:
            cell = choice(self.level[2])
            if self.game_map.can_set_smth(*cell):
                enemy_class = choice(enemy_types)

                enemy = enemy_class(*cell)
                self.game_map.tiles[cell[1]][cell[0]] = enemy.view['letter']
                enemies.append(enemy)
                num_enemies -= 1
        return enemies

    def check_monster_alive(self, current_enemy):
        for i, enemy in enumerate(self.enemies):
            if enemy.health <= 0 and current_enemy == enemy:
                cor_x,cor_y = enemy.get_cords()
                self.game_map.tiles[cor_y][cor_x] = '.'
                self.enemies.pop(i)
                self.battles.pop(i)
                self.enemies_defeated += 1  # увеличиваем счетчик
                return False
        return True

    def handle_input(self, player_input):

        self.message = ''

        old_x, old_y = self.character.get_cords()
        new_x, new_y = old_x, old_y

        if player_input == Keys.W_UP:
            new_y -= 1
        elif player_input == Keys.S_DOWN:
            new_y += 1
        elif player_input == Keys.A_LEFT:
            new_x -= 1
        elif player_input == Keys.D_RIGHT:
            new_x += 1
        elif player_input in Keys.H_USE_WEAPON.value:
            self.backpack.get_items('weapon')
        elif player_input in Keys.J_USE_FOOD.value:
            self.backpack.get_items('food')
        elif player_input in Keys.K_USE_ELIXIR.value:
            self.backpack.get_items('potion')
        elif player_input in Keys.E_USE_SCROLL.value:
            self.backpack.get_items('scroll')
        elif player_input == Keys.Q_CLOSE:
            self.backpack.current_item_list = []
        # Обработка номеров 0-9 для использования предметов
        elif isinstance(player_input, int) and 48 <= player_input <= 57:
            index = player_input - 48
            msg = self.backpack.use_item(index, self.character)
            if msg:
                self.message += msg
            return self.get_game_state()
        elif isinstance(player_input, str) and player_input.isdigit():
            index = int(player_input)
            msg = self.backpack.use_item(index, self.character)
            if msg:
                self.message += msg
            return self.get_game_state()

        max_y = len(self.game_map.tiles) - 1
        max_x = len(self.game_map.tiles[0]) - 1

        if not (0 <= new_x <= max_x and 0 <= new_y <= max_y):
            return self.get_game_state()

        target_tile = self.game_map.tiles[new_y][new_x]

        # Если игрок наступил на тайл перехода '>' — переходим на следующий уровень
        if target_tile == '>':
            self.n_level += 1
            if self.n_level > 21:
                self.message = 'Поздравляю! Вы прошли игру.'
                self._save_attempt(game_won=True)
                return self.get_game_over_state()
            else:
                # генерируем следующий уровень (сохранённый рюкзак и характеристики персонажа остаются)
                self.load_level()
                self.level_changed = True
                self.message = f'Вы перешли на уровень {self.n_level}'
                # сохраняем прогресс после каждого уровня
                self._auto_save()
                return self.get_game_state()

        if target_tile in ('.', ',', '@'):  # '.' — пол, ',' — коридор
            self.game_map.tiles[old_y][old_x] = '.'
            self.character.set_cords(new_x, new_y)
            self.game_map.tiles[new_y][new_x] = '@'

        for i, item in enumerate(self.items):
            if item.get_cords() == (new_x, new_y):
                self.message = self.backpack.add_item(self.items.pop(i))
                self.game_map.tiles[old_y][old_x] = '.'
                self.character.set_cords(new_x, new_y)
                self.game_map.tiles[new_y][new_x] = '@'
                break

        # --------------------------
        # 6. Двигаем врагов
        # --------------------------
        for idx, enemy in enumerate(self.enemies):
            self.move_enemy.move(enemy, self.character.get_cords())

            # Если враг вступил в бой
            if enemy.in_fight:
                if self.battles[idx] is None:
                    self.battles[idx] = Fight(self.character, enemy)

        # --------------------------
        # 7. Обрабатываем бои
        # --------------------------
        #
        for battle in self.battles:
            if battle is None:
                continue
            self.message += battle.player_action((new_x, new_y))
            if self.check_monster_alive(battle.monster):
                self.message += battle.attack()
            else:
                self.character.update_level()


        with open('d.log', 'w') as log:
            log.write(f'{player_input}\n')


        return self.get_game_state()

    def _auto_save(self):
        """Автосохранение после прохождения уровня"""
        game_state = self.get_game_state()
        # Передаём рюкзак и персонажа для полного сохранения
        self.save_manager.save_game(game_state, self.backpack, self.character)
        print(f'Игра сохранена (уровень {self.n_level})')

    def get_game_state(self):
        """
        Возвращает текущее состояние игры: карту, координаты игрока, врагов и здоровье.
        """
        with open('d.log', 'a') as log:
            log.write(f'Итог {[e.get_cords() for e in self.enemies]}:\n')
        player_data = self.character.presentation_data()
        player_data['level'] = self.n_level

        state = {
            "rooms": self.level[0],
            'corridors': self.level[1],
            "player": player_data,
            "enemies": [e.presentation_data() for e in self.enemies],
            "items": [i.presentation_data() for i in self.items],
            'weapon': self.backpack.get_weapons(),
            'food': self.backpack.get_food(),
            'elixir': self.backpack.get_potions(),
            'scroll': self.backpack.get_scrolls(),
            "message": self.message,
            "level": self.n_level,
            "level_changed": self.level_changed
        }
        return state

    def load_from_save(self, save_data: Dict) -> bool:
        """Загружает состояние игры из сохранённых данных"""
        try:
            self.n_level = save_data.get('level', 1)
            
            # Восстанавливаем характеристики персонажа
            player_data = save_data.get('player', {})
            self.character.health = player_data.get('health', 40)
            self.character.max_health = player_data.get('max_health', 40)
            self.character.strength = player_data.get('strength', 15)
            self.character.dexterity = player_data.get('dexterity', 6)
            self.character.regen_limit = player_data.get('regen_limit', 40)
            
            # Восстанавливаем золото в рюкзаке
            self.backpack.treasure = player_data.get('gold', 0)
            
            # Восстанавливаем предметы рюкзака
            backpack_data = save_data.get('backpack', {})
            if backpack_data:
                # Очищаем рюкзак
                self.backpack.items = {
                    "food": [],
                    "potion": [],
                    "scroll": [],
                    "weapon": []
                }
                
                # Восстанавливаем оружие
                for weapon_data in backpack_data.get('weapon', []):
                    weapon = Item(
                        item_type=weapon_data.get('item_type', 'weapon'),
                        subtype=weapon_data.get('subtype', 'оружие'),
                        letter=weapon_data.get('letter', 'w'),
                        health=weapon_data.get('health', 0),
                        max_health=weapon_data.get('max_health', 0),
                        dexterity=weapon_data.get('dexterity', 0),
                        strength=weapon_data.get('strength', 0),
                        value=weapon_data.get('value', 0)
                    )
                    self.backpack.items['weapon'].append(weapon)
                
                # Восстанавливаем еду
                for food_data in backpack_data.get('food', []):
                    food = Item(
                        item_type=food_data.get('item_type', 'food'),
                        subtype=food_data.get('subtype', 'еда'),
                        letter=food_data.get('letter', 'f'),
                        health=food_data.get('health', 0),
                        max_health=food_data.get('max_health', 0),
                        dexterity=food_data.get('dexterity', 0),
                        strength=food_data.get('strength', 0),
                        value=food_data.get('value', 0)
                    )
                    self.backpack.items['food'].append(food)
                
                # Восстанавливаем зелья
                for potion_data in backpack_data.get('potion', []):
                    potion = Item(
                        item_type=potion_data.get('item_type', 'potion'),
                        subtype=potion_data.get('subtype', 'зелье'),
                        letter=potion_data.get('letter', 'e'),
                        health=potion_data.get('health', 0),
                        max_health=potion_data.get('max_health', 0),
                        dexterity=potion_data.get('dexterity', 0),
                        strength=potion_data.get('strength', 0),
                        value=potion_data.get('value', 0)
                    )
                    self.backpack.items['potion'].append(potion)
                
                # Восстанавливаем свитки
                for scroll_data in backpack_data.get('scroll', []):
                    scroll = Item(
                        item_type=scroll_data.get('item_type', 'scroll'),
                        subtype=scroll_data.get('subtype', 'свиток'),
                        letter=scroll_data.get('letter', 't'),
                        health=scroll_data.get('health', 0),
                        max_health=scroll_data.get('max_health', 0),
                        dexterity=scroll_data.get('dexterity', 0),
                        strength=scroll_data.get('strength', 0),
                        value=scroll_data.get('value', 0)
                    )
                    self.backpack.items['scroll'].append(scroll)
            
            # Восстанавливаем врагов и предметы
            self.enemies = []
            self.items = []
            
            # Генерируем уровень заново, но с восстановленным n_level
            self.load_level()
            
            return True
        except Exception as e:
            print(f'Ошибка при загрузке сохранения: {e}')
            return False

    def _save_attempt(self, game_won: bool = False):
        """Сохраняет статистику попытки"""
        play_time = int(time.time() - self.start_time)
        attempt_data = {
            'level_reached': self.n_level,
            'max_health': self.character.max_health,
            'health': self.character.health,
            'strength': self.character.strength,
            'dexterity': self.character.dexterity,
            'gold': self.backpack.treasure,
            'enemies_defeated': self.enemies_defeated,
            'game_won': game_won,
            'play_time': play_time
        }
        self.stats_manager.add_attempt(attempt_data)

    def get_game_over_state(self):
        """
        Возвращает сообщение о завершении игры.
        """
        return {
            "game_over": True,
            "level": self.n_level,
            "gold": self.backpack.treasure,
            "enemies_defeated": self.enemies_defeated
        }


