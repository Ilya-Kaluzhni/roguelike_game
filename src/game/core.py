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
        self.load_level()

    def start(self):
        self.load_level()

    def load_level(self):
        """Генерирует новый уровень и размещает игрока."""
        # generator = MapGenerator()

        # ---- теперь всё правильно ----
        self.level = self.game_map.generate_level()
        self.move_enemy = MoveEnemy(self.game_map)

        self.character.set_cords(*self.game_map.set_player_cords())
        self.enemies = self.spawn_enemies()

        self.spawn_items()
        self.battles = [None] * len(self.enemies)

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
        elif 48 <= int(player_input) <= 57:
            self.message += self.backpack.use_item(player_input - 48,self.character)

        max_y = len(self.game_map.tiles) - 1
        max_x = len(self.game_map.tiles[0]) - 1

        if not (0 <= new_x <= max_x and 0 <= new_y <= max_y):
            # ударились в стену карты — движение игнорируем
            return self.get_game_state()

        # --------------------------
        # 5. Проверяем, можно ли ходить на новую клетку
        # --------------------------
        target_tile = self.game_map.tiles[new_y][new_x]

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

    def get_game_state(self):
        """
        Возвращает текущее состояние игры: карту, координаты игрока, врагов и здоровье.
        """
        with open('d.log', 'a') as log:
            log.write(f'Итог {[e.get_cords() for e in self.enemies]}:\n')
        # with open('items.log', 'a') as log:
        #     for i, itt in enumerate(self.items):
        #         log.write(f'{i}. {itt.get_cords()}: {itt.subtype}\n')
        state = {
            "rooms": self.level[0],
            'corridors': self.level[1],
            "player": self.character.presentation_data(),
            "enemies": [e.presentation_data() for e in self.enemies],
            "items": [i.presentation_data() for i in self.items],
            'weapon': self.backpack.get_weapons(),
            'food': self.backpack.get_food(),
            'elixir': self.backpack.get_potions(),
            'scroll': self.backpack.get_scrolls(),
            "message": self.message
        }
        return state

    def get_game_over_state(self):
        """
        Возвращает сообщение о завершении игры.
        """
        return {"game_over": True}


