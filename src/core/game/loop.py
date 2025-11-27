# /Users/ilya/roguelike_game/src/domain/game/loop.py

from core.game.session import GameSession
from core.movement.directions import Directions
from core.combat.fight import Fight


class GameLoop:
    """
    Абстрактный цикл игры.
    UI вызывает методы этого класса и получает события.
    """

    def __init__(self):
        self.session = GameSession()
        self.fight = Fight()

    def start(self):
        """Начать игру (создаёт сессию)."""
        self.session = GameSession()

    # ------------------------------------------------------
    # Основной шаг цикла (выполняется каждый тик)
    # ------------------------------------------------------

    def tick(self):
        """
        Выполняет обновление состояния мира:
        - враги двигаются
        - проверяются столкновения
        Возвращает список событий.
        """
        events = []

        # 1. Движение врагов
        self.session.update_enemies()

        # 2. Проверить столкновение игрока с врагом
        enemy = self.session.check_collisions()
        if enemy:
            result = self.fight.start(self.session.character, enemy)
            events.append({"type": "fight", "result": result})

            # если игрок умер
            if not self.session.character_alive():
                events.append({"type": "game_over"})
                return events

        return events

    # ------------------------------------------------------
    # Действия игрока
    # ------------------------------------------------------

    def move_player(self, direction):
        """
        UI вызывает move_player(direction)
        direction — элемент enum Directions
        """
        dx, dy = direction.value
        self.session.move_character(dx, dy)

        # после перемещения — снова тик
        return self.tick()

    def next_level(self):
        """
        Вызывается, если игрок вошёл в выходную дверь.
        """
        self.session.go_to_next_level()
        return [{"type": "new_level", "level": self.session.current_level_index}]

    # ------------------------------------------------------
    # UI может в любой момент спросить состояние мира:
    # ------------------------------------------------------

    def get_world_state(self):
        """
        UI спрашивает карту + координаты.
        """
        return {
            "map": self.session.level.map.grid,
            "player": self.session.character.get_coords(),
            "enemies": [(e.cords["x"], e.cords["y"]) for e in self.session.level.enemies],
            "hp": self.session.character.current_health,
        }
