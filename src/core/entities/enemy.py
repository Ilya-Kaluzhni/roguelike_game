# тип,
# здоровье,
# ловкость,
# сила,
# враждебность;
from src.core.constants.detection import DETECTION_RANGE


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
        if self.check_character_near(character_cords):
            self.shortest_path(character_cords, neighbors_cells)
        else:
            self.move_pattern()

    def move_pattern(self):
        pass

    @staticmethod
    def get_distance(cell_cords, enemy_cords):
        return abs(cell_cords['x'] - enemy_cords['x']) + abs(cell_cords['y'] - enemy_cords['y'])

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
        self.cords = nearest
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
