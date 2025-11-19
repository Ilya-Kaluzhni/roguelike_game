from random import choice, randint, random

DIRECTIONS = [
    'FORWARD',
    'LEFT',
    'RIGHT',
    'BACK',
    'DIAGONALLY_UP_LEFT',
    'DIAGONALLY_UP_RIGHT',
    'DIAGONALLY_DOWN_LEFT',
    'DIAGONALLY_DOWN_RIGHT',
    'STOP'
]

MAX_TRIES = 16

DETECTION_RANGE = {
    'LOW': 2,
    'AVERAGE': 4,
    'HIGH': 6,
}


# тип,
# здоровье,
# ловкость,
# сила,
# враждебность;
class Enemy:
    def __init__(self, type_, health, dexterity, strength, hostility, direction=None, moving_pattern=None, view=None,
                 x=0,
                 y=0):
        self.type = type_
        self.current_health = health
        self.dexterity = dexterity
        self.strength = strength
        self.direction = direction
        self.hostility = hostility
        self.moving_pattern = moving_pattern
        self.view = view or {}
        self.cords = {'x': x, 'y': y}
        self.chase_character = False

    @staticmethod
    def change_cords(current_cords, direction):
        x, y = current_cords['x'], current_cords['y']

        if direction == 'UP':
            y -= 1
        elif direction == 'DOWN':
            y += 1
        elif direction == 'LEFT':
            x -= 1
        elif direction == 'RIGHT':
            x += 1
        elif direction == 'DIAGONALLY_UP_LEFT':
            x -= 1
            y -= 1
        elif direction == 'DIAGONALLY_UP_RIGHT':
            x += 1
            y -= 1
        elif direction == 'DIAGONALLY_DOWN_LEFT':
            x -= 1
            y += 1
        elif direction == 'DIAGONALLY_DOWN_RIGHT':
            x += 1
            y += 1
        return x, y

    def move(self, character_cords, neighbors_cells):
        if self.chase_character or self.check_character_near(character_cords):
            self.shortest_path(character_cords, neighbors_cells)
        else:
            self.move_pattern()

    def move_pattern(self):
        pass

    @staticmethod
    def get_distance(cell_cords, enemy_cords):
        return abs(cell_cords[0] - enemy_cords['x']) + abs(cell_cords[1] - enemy_cords['y'])

    # neighbors - список соседних с монстром клеток, скорее всего через класс комнаты подается
    def shortest_path(self, character_cords, neighbors):
        # min_distance = abs(self.cords['x'] - character_cords['x']) + abs(self.cords['y'] - character_cords['y'])
        # directions = [(-1, -1), (-1, 0), (-1, 1),
        #               (0, -1), (0, 1),
        #               (1, -1), (1, 0), (1, 1)]

        nearest = self.cords
        min_dist = float('inf')
        for cell in neighbors:
            dist = self.get_distance(cell, character_cords)
            if dist < min_dist:
                min_dist = dist
                nearest = cell
        self.cords['x'], self.cords['y'] = nearest[0], nearest[1]
        return nearest

    def check_character_near(self, character_cords):
        distance_x = self.cords['x'] - character_cords['x']
        distance_y = self.cords['y'] - character_cords['y']
        distance = abs(distance_x) + abs(distance_y)
        if distance <= DETECTION_RANGE[self.hostility]:
            self.chase_character = True
        else:
            self.chase_character = False

    def get_cords(self):
        return self.cords['x'], self.cords['y']


class Zombie(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='zombie',
            health=150,  # высокое здоровье
            dexterity=25,  # низкая ловкость
            strength=125,  # средняя сила
            hostility='AVERAGE',  # средняя враждебность
            moving_pattern=None,
            view={'letter': 'Z', 'color': 'green'},
            x=cord_x,
            y=cord_y
        )

    # Мб добавить доп ограничение попыток движения.
    # Выбирает рандомно направление движения из 4 возможных направлений
    def move_pattern(self):
        for _ in range(MAX_TRIES):
            direction = choice(['UP', 'LEFT', 'RIGHT', 'DOWN'])
            new_cords = super().change_cords(self.cords, direction)
            # if Если не выходит за границу и ячейка свободна:
            self.cords['x'], self.cords['y'] = new_cords
            with open('d.log', 'a') as f:
                f.write(str(new_cords))
            break


class Vampire(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='vampire',
            health=150,  # высокая здоровье
            dexterity=75,  # высокая ловкость
            strength=75,  # средняя сила
            hostility='HIGH',  # высокая враждебность
            moving_pattern=None,
            view={'letter': 'V', 'color': 'red'},
            x=cord_x,
            y=cord_y
        )
        self.vampire_first_attack = True  # Первый удар по вампиру — промах

    # Выбирает рандомно направление движения из всех возможных направлений
    def move_pattern(self):
        for _ in range(MAX_TRIES):
            direction = choice(DIRECTIONS)
            new_cords = super().change_cords(self.cords, direction)
            # if Если не выходит за границу и ячейка свободна:
            self.cords['x'], self.cords['y'] = new_cords
            break


class Ghost(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='ghost',
            health=25,  # низкое здоровье
            dexterity=75,  # высокая ловкость
            strength=25,  # низкая сила
            hostility='LOW',  # низкая враждебность
            moving_pattern='teleport_and_invisible',
            view={'letter': 'G', 'color': 'white'},
            x=cord_x,
            y=cord_y
        )

    # Телепортация и невидимость пока игрок не в бою
    # Продумать, нужен ли путь перехода
    def move_pattern(self):
        room_cords = 10  # Координаты комнаты, необходимо изменить
        for _ in range(MAX_TRIES):
            direction_x = randint(0, room_cords)  # Рандомное число из ширины комнаты
            direction_y = randint(0, room_cords)  # Рандомное число из высоты комнаты
            # if Если не выходит за границу и ячейка свободна:
            self.cords['x'], self.cords['x'] = direction_x, direction_y
            break


class Ogre(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='ogre',
            health=150,  # очень высокое здоровье
            dexterity=25,  # низкая ловкость
            strength=150,  # очень высокая сила
            hostility='AVERAGE',  # средняя враждебность
            moving_pattern='move_two_tiles',
            view={'letter': 'O', 'color': 'yellow'},
            x=cord_x,
            y=cord_y
        )
        self.cooldown_after_attack = False

    # Перемещается на 2 шага
    def move_pattern(self):
        for _ in range(MAX_TRIES):
            direction = choice(['UP', 'LEFT', 'RIGHT', 'DOWN'])
            first_step = {'x': (super().change_cords(self.cords, direction))[0],
                          'y': (super().change_cords(self.cords, direction))[1]}
            # if Если не выходит за границу и ячейка свободна еще раз проверить следующую:
            new_cords = super().change_cords(first_step, direction)
            # if Если не выходит за границу и ячейка свободна
            self.cords['x'], self.cords['y'] = new_cords
            break


class Snake(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='snake',
            health=100,  # здоровье
            dexterity=100,  # очень высокая ловкость
            strength=30,  # сила
            hostility='HIGH',  # высокая враждебность
            moving_pattern='diagonal_move',
            view={'letter': 'S', 'color': 'white'},
            x=cord_x,
            y=cord_y
        )
        # self.last_cords = self.cords
        self.direction = DIRECTIONS[4]

    def move_pattern(self):
        for _ in range(MAX_TRIES):
            direction = choice(DIRECTIONS[4:])
            with open('d.log', 'a') as f:
                f.write(str(direction) + '\n')
            if direction != self.direction:
                new_cords = super().change_cords(self.cords, direction)
                # if Если не выходит за границу и ячейка свободна
                self.direction = direction
                self.cords['x'], self.cords['y'] = new_cords
                with open('d.log', 'a') as f:
                    f.write(str(new_cords) + '\n')
                break
        # if Если не выходит за границу и ячейка свободна
        new_cords = super().change_cords(self.cords, self.direction)
        self.cords['x'], self.cords['y'] = new_cords


class Fight:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.turn_player = True
        self.hit_chance = 70
        self.dexterity_factor = 0.3
        self.standard_dexterity = 50
        self.standard_strength = 50
        self.strength_factor = 0.3
        self.strength_addition = 65
        self.initial_damage = 30
        self.sleep_chance = 15
        self.max_hp_part = 10
        self.loot_dexterity_factor = 0.2
        self.loot_hp_factor = 0.5
        self.loot_strength_factor = 0.5
        # self.maximum_fights = 8
        self.player_first_attack = True

    # 1 этап 'Расчет удара' вычисляет вероятность успешного попадания удара
    def check_hit(self):
        chance = self.hit_chance
        if self.turn_player:
            chance += (self.player.dexterity - self.monster.dexterity - self.standard_dexterity) * self.dexterity_factor
        else:
            chance += (self.monster.dexterity - self.player.dexterity - self.standard_dexterity) * self.dexterity_factor
        if random() < chance or self.monster.type == 'ogre':
            return True
        return False

    # 2 этап 'Расчет урона' высчитывает урон, который наносится при атаке
    def calculate_damage(self):
        damage = self.initial_damage
        if self.turn_player:
            if not (self.monster.type == 'vampire' and self.player_first_attack) and not (
                    self.monster.type == 'snake' and self.player.asleep):
                if self.player.current_weapon.strength:
                    damage += self.player.current_weapon.strength * (
                            self.player.strength + self.strength_addition) / 100
                else:
                    damage += (self.player.strength - self.standard_strength) * self.strength_factor
            elif self.monster.type == 'vampire' and self.player_first_attack:
                self.player_first_attack = False
            else:
                self.player.asleep = False
        else:
            damage = self.monster_damage_formula()
        return damage

    # формулы расчёта урона для разных монстров
    def monster_damage_formula(self):
        if self.monster.type == 'vampire':
            return self.player.max_health / self.max_hp_part
        elif self.monster.type == 'ogre':
            if not self.monster.cooldown_after_attack:
                self.monster.cooldown_after_attack = True
                return (self.monster.strength - self.standard_strength) * self.strength_factor
            else:
                self.monster.cooldown_after_attack = False
                return 0
        else:
            if self.monster.type == 'snake' and randint(0, 99) < self.sleep_chance:
                self.player.asleep = True
            return self.initial_damage + (self.monster.strength - self.standard_strength) * self.strength_factor

    # 3 этап 'Применение урона'
    def attack(self):
        if self.turn_player:
            if self.check_hit():
                self.monster.health -= self.calculate_damage()
            if self.monster.health <= 0:
                self.player.backpack.treasures += self.calculate_loot()
        else:
            if self.check_hit():
                self.player.health -= self.calculate_damage()

    def calculate_loot(self):
        return (self.monster.dexterity * self.loot_dexterity_factor +
                self.monster.health * self.loot_hp_factor +
                self.monster.strength * self.loot_strength_factor +
                randint(0, 19))


