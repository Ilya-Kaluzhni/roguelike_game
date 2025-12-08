from domain.enemy import Enemy
from presentation.static import Directions,DetectionRange
from random import choice


class Snake(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='snake',
            health=100,
            dexterity=100,
            strength=30,
            hostility=DetectionRange.HIGH,
            view={'letter': 'S', 'color': 'white'},
            x=cord_x,
            y=cord_y
        )
        self.direction = choice(Directions.diagonal_directions())

    def move_pattern(self):
        direction = choice(Directions.diagonal_directions())
        new_cords = super().change_cords(self.x, self.y, direction)
        self.direction = direction
        while direction != self.direction:
            new_cords = super().change_cords(self.x, self.y, direction)
            self.direction = direction
        return new_cords
