# src/core/entities/character.py

class Character:
    """
    Игровой персонаж.
    Хранит характеристики и координаты.
    """

    def __init__(self):
        # Базовые атрибуты — позже вы сможете расширить их системой прокачки
        self.max_health = 10
        self.current_health = 10

        self.dexterity = 1  # ловкость — шанс уклонения / крит
        self.strength = 1  # сила атаки
        self.treasure_points = 0

        self.current_weapon = None
        self.backpack = []  # пока простой список, можно заменить на класс Backpack

        # Позиция игрока в мире
        self.x = 0
        self.y = 0

    # ------------------------------------------------------
    #   ПОЗИЦИЯ ПЕРСОНАЖА
    # ------------------------------------------------------

    def set_coords(self, x, y):
        """Задать позицию персонажа."""
        self.x = x
        self.y = y

    def get_coords(self):
        """Получить позицию персонажа."""
        return self.x, self.y

    # ------------------------------------------------------
    #   АТАКИ И БОЙ
    #   (можно оставить пустым — боем управляет Fight)
    # ------------------------------------------------------

    def take_damage(self, amount):
        """Уменьшить здоровье игрока."""
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def heal(self, amount):
        """Восстановить здоровье."""
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    # ------------------------------------------------------
    #   УСИЛЕНИЕ ПЕРСОНАЖА
    # ------------------------------------------------------

    def increase_stats_after_kill(self, enemy):
        """
        Прокачка после победы над врагом.
        Enemy должен иметь difficulty / value.
        """
        self.treasure_points += enemy.value if hasattr(enemy, "value") else 1
