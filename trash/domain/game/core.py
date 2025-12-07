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
        # selmf.move_enemy = MoveEnemy(self.level)
        # rooms_ui, corridors_ui, rooms_cells, corridors_cells = generator.generate_level()
        # Берём центр стартовой комнаты
        # start_x, start_y = self.level.start_room.center()
        self.character.set_cords(10, 5)
        # self.level.take(player_cords)
        # Опционально — создание врагов
        self.enemies = self.spawn_enemies()
        self.battles = [None] * len(self.enemies)
        with open('d.log', 'a') as f:
            f.write(str([e.presentation_data() for e in self.enemies]) + '\n')

    def spawn_enemies(self):
        """Создаёт врагов в случайных комнатах."""
        if self.n_level == 1:
            enemy_types = [Mimic, Ghost]
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
            if self.game_map.get_room_inner_size(*cell):
                with open('d.log', 'a') as f:
                    f.write(str(cell) + '\n')
                enemy_class = choice(enemy_types)

                enemy = enemy_class(*cell)
                self.game_map.tiles[cell[1]][cell[0]] = enemy.view['letter']
                enemies.append(enemy)
                num_enemies -= 1
                with open('d.log', 'a') as log:
                    log.write(f'Вот он враг{enemy.get_cords()}:\n')
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
        cord_x, cord_y = self.character.get_cords()
        if player_input in Keys:
            cord_x, cord_y = self.character.get_cords()
            self.game_map.tiles[cord_y][cord_x] = '.'
            if player_input == Keys.W_UP:
                cord_y -= 1
            elif player_input == Keys.S_DOWN:
                cord_y += 1
            elif player_input == Keys.A_LEFT:
                cord_x -= 1
            elif player_input == Keys.D_RIGHT:
                cord_x += 1
            if self.game_map.tiles[cord_y][cord_x] == '.' or self.game_map.tiles[cord_y][cord_x] == ',':
                self.character.set_cords(cord_x, cord_y)
            if (cord_x, cord_y) in self.level[2] and self.character.get_cords() in self.level[3]:
                self.character.set_cords(cord_x, cord_y)
            new_cord_x, new_cord_y = self.character.get_cords()
            self.game_map.tiles[new_cord_y][new_cord_x] = '@'
        for idx, enemy in enumerate(self.enemies):
            self.move_enemy.move(enemy, self.character.get_cords())
            if enemy.in_fight:
                if self.battles[idx] is None:
                    self.battles[idx] = Fight(self.character, enemy)
                    # self.battles[idx].attack()
        message = ''
        if any(self.battles):
            for battle in self.battles:
                if battle:
                    if battle.monster.get_cords() == (cord_x, cord_y):
                        battle.set_turn_player()
                        self.message = battle.attack()
                    if self.check_monster_alive(battle.monster):
                        with open('f.log', 'a') as log:
                            log.write(f'Сообщение: {message}\n')
                        message = battle.attack()

                        with open('f.log', 'a') as log:
                            log.write(f'Сообщение: {message}\n')
                    else:
                        self.character.update_level()
        with open('f.log', 'a') as log:
            log.write(f'{self.battles} Сообщение: {message}\n')
        with open('map.txt', 'w') as f:
            for tile in self.game_map.tiles:
                f.write(str(tile) + '\n')
        return self.get_game_state()

    def get_game_state(self):
        """
        Возвращает текущее состояние игры: карту, координаты игрока, врагов и здоровье.
        """
        with open('d.log', 'a') as log:
            log.write(f'Итог {[e.get_cords() for e in self.enemies]}:\n')
        state = {
            "rooms": self.level[0],
            'corridors': self.level[1],
            "player": self.character.presentation_data(),
            "enemies": [e.presentation_data() for e in self.enemies],
            "message": self.message
            # "hp": self.game_session.character.current_health,
        }
        return state

    def get_game_over_state(self):
        """
        Возвращает сообщение о завершении игры.
        """
        return {"game_over": True}
