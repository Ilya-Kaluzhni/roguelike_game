from enemy import Enemy
from static import Directions
from random import choice


class Snake(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='snake',
            health=100,  # здоровье
            dexterity=100,  # очень высокая ловкость
            strength=30,  # сила
            hostility='HIGH',  # высокая враждебность
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
