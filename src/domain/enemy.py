from presentation.static import DetectionRange


class Enemy:
    def __init__(self, type_, health, dexterity, strength, hostility, view=None, x=0, y=0):
        self.type = type_
        self.health = health
        self.dexterity = dexterity
        self.strength = strength
        self.hostility = hostility
        self.view = view or {}
        self.x = x
        self.y = y
        self.chase_character = False
        self.in_fight = False

    @staticmethod
    def change_cords(cord_x, cord_y, direction):
        dx, dy = direction.value
        cord_x += dx
        cord_y += dy
        return cord_x, cord_y

    def move_pattern(self):
        pass

    @staticmethod
    def get_distance(cell_cords, enemy_cords):
        return abs(cell_cords[0] - enemy_cords[0]) + abs(cell_cords[1] - enemy_cords[1])

    def must_chase_character(self, character_cords):
        self.check_character_near(character_cords)
        with open('d.log', 'a') as log:
            log.write(f'{self.chase_character}\n')
        return self.chase_character

    def check_character_near(self, character_cords):
        distance_x = self.x - character_cords[0]
        distance_y = self.y - character_cords[1]
        distance = abs(distance_x) + abs(distance_y)
        with open('d.log', 'a') as log:
            log.write(f'Монстер расстояние{distance, self.hostility.value}\n')
        if distance <= self.hostility.value:
            self.chase_character = True
        elif not self.chase_character:
            self.chase_character = False

    def get_cords(self):
        return self.x, self.y

    def down_health(self, damage):
        self.health -= damage

    def set_cords(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def presentation_data(self):
        return {
            'type': self.view['letter'],
            'color': self.view['color'],
            'x': self.x,
            'y': self.y
        }
