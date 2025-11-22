# src/core/game/session.py

from src.domain.characters.character import Character
from src.domain.map_generate.map_generate import MapGenerator
from ..characters.character import Character
from ..characters.enemy_movement import MoveEnemy
import random


class GameSession:
    """
    Главный игровой контроллер.
    Управляет:
    - генерацией уровня
    - позицией игрока
    - врагами
    """

    def __init__(self, map_width=80, map_height=25, seed=None):
        self.character = Character()

        self.map_width = map_width
        self.map_height = map_height
        self.seed = seed

        self.level = None  # объект Level из map_generate
        self.move_enemy = None
        self.enemies = []  # пока пусто — заполним позже

    # ----------------------------------------------------------
    #  СОЗДАНИЕ УРОВНЯ
    # ----------------------------------------------------------
    def start_new_game(self):
        self.load_level()

    def load_level(self):
        """Генерирует новый уровень и размещает игрока."""
        generator = MapGenerator(width=self.map_width, height=self.map_height, seed=self.seed)

        # ---- теперь всё правильно ----
        self.level = generator.generate_level()
        self.move_enemy = MoveEnemy(self.level)

        # Берём центр стартовой комнаты
        start_x, start_y = self.level.start_room.center()
        self.character.set_cords(start_x, start_y)

        # Опционально — создание врагов
        self.enemies = self.spawn_enemies()

    # ----------------------------------------------------------
    #  ВРАГИ
    # ----------------------------------------------------------
    def spawn_enemies(self):
        """Создаёт врагов в случайных комнатах."""
        enemies = []

        # пример: по одному врагу в комнату, кроме стартовой
        from src.core.entities.snake import Snake

        for room in self.level.rooms:
            if room is self.level.start_room:
                continue

            # выбираем случайную точку в комнате
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            enemies.append(Snake(x, y))

        return enemies

    # ----------------------------------------------------------
    #  СОСТОЯНИЕ ИГРЫ
    # ----------------------------------------------------------
    def is_player_alive(self):
        return self.character.current_health > 0

    # ----------------------------------------------------------
    #  ОСНОВНОЙ ЦИКЛ
    # (UI/отрисовку делает другой разработчик)
    # ----------------------------------------------------------
    def update(self, player_input):
        """
        Обновляет состояние игры.
        UI вызывает этот метод каждый кадр.
        """

        # 1) Обработать ход игрока
        self.process_player_action(player_input)

        # 2) Обновить врагов
        for enemy in self.enemies:
            self.move_enemy(enemy, self.character.get_cords())
            enemy.move(self.character.get_cords(), neighbors_cells=None)
            # neighbors_cells — реализуете позже

        # 3) Проверить смерть игрока
        if not self.is_player_alive():
            return "GAME_OVER"

        return "RUNNING"

    def process_player_action(self, player_input):
        """
        Логика движения игрока.
        UI передаёт направление.
        """
        dx = dy = 0
        if player_input == "UP":
            dy = -1
        elif player_input == "DOWN":
            dy = +1
        elif player_input == "LEFT":
            dx = -1
        elif player_input == "RIGHT":
            dx = +1

        if dx or dy:
            x, y = self.character.get_coords()
            new_x = x + dx
            new_y = y + dy

            # проверяем walkable
            if self.level.is_walkable(new_x, new_y):
                self.character.set_coords(new_x, new_y)
