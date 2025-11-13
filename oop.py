from random import randint


# Класс, реализующий игру
# Атрибуты
# Гг, текущий уровень
class GameSession:
    def __init__(self):
        self.character = Character()
        self.level = Level(0)

    def check_alive(self):
        # Проверяет жив ли персонаж, если нет, должна сохранять данные для статистики
        pass


# Атрибуты
# Значение текущего левла
# Список комнат
# Количество врагов
# Необходимо продумать сложность врагов и т.п.
# Необходимо продумать соединение коридоров
class Level:
    count_rooms = 9

    def __init__(self, lvl):
        self.level = lvl
        self.rooms = self.create_rooms()
        self.count_enemy = 5

    # Возвращает список комнат со стартовой.
    # Добавить установку перехода на след уровень в одной из комнат
    @classmethod
    def create_rooms(cls):
        rooms = [Room() for _ in range(cls.count_rooms - 1)]
        rooms.insert(0, Room(True))
        return rooms

    # Должна создавать врагов в созданных комнатах и коридорах
    def create_enemy(self):
        pass


# Атрибуты
# Стартовая ли комната
# Размеры
# Если стартовая - рандомно задает позицию перса
class Room:
    def __init__(self, is_start_room=False):
        self.start_room = is_start_room
        self.width = randint(3, 10)
        self.height = randint(3, 10)

        if self.start_room:
            self.character_pos = (randint(0, self.width), randint(0, self.height))

    # Должна задавать положение перехода на след уровень
    def create_exit(self):
        pass


class Corridor:
    pass


# Здоровье эквивалентно уровню перса
class Character:
    max_health = 1

    def __init__(self):
        self.max_health = 1
        self.current_health = 1
        self.dexterity = 1
        self.strength = 1
        self.current_weapon = None
        self.direction = None
        # Увеличивается при победе над врагом, увеличивается относительно сложности врага
        self.treasure_points = 0
        self.backpack = Backpack()

    # Удар перса по врагу, учитывается ловкость
    def attack_enemy(self):
        pass

    # Борьба перса с врагом, где учитывается сила
    def fight_enemy(self):
        pass

    # Добавлять оружие игроку или меняет на новое
    def get_or_change_weapon(self):
        pass


class Backpack:
    def __init__(self):
        self.count_treasure = []
        self.count_food = []
        self.count_elixirs = []
        self.count_scrolls = []
        self.count_weapons = []

    # Добавляет в определенный список атрибутов предмет
    def get_item(self, item):
        pass


# 5 врагов
class Enemy:

    def __init__(self):
        self.type = None
        self.current_health = 0
        self.dexterity = 0
        self.strength = 0
        self.direction = None

        # Логика движения, зависит от типа
        self.moving_pattern = None

        # определяет расстояние, с которого противник начинает преследовать игрока
        self.hostility = 0

    # Преследование персонажа, возвращать новые координаты положения
    def move(self):
        pass


# 5 типов
class Item:
    def __init__(self):
        self.type = None
        self.subtype = 0
        self.health = None
        self.maximum_health = 0
        self.dexterity = 0
        self.strength = 0
        self.value = 0

# Должна получать игрока и врага и реализовывать бой между ними
class Fight:
    pass