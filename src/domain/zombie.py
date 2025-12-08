from domain.enemy import Enemy
from presentation.static import Directions,DetectionRange
from random import choice


class Zombie(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='zombie',
            health=150,  # высокое здоровье
            dexterity=25,  # низкая ловкость
            strength=125,  # средняя сила
            hostility=DetectionRange.AVERAGE,  # средняя враждебность
            view={'letter': 'Z', 'color': 'green'},
            x=cord_x,
            y=cord_y
        )

    def move_pattern(self):
        direction = choice(Directions.simple_directions())
        new_cords = super().change_cords(self.x, self.y, direction)
        return new_cords
