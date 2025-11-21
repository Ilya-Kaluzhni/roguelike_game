from enemy import *

from src.core.movement.directions import *
from random import choice


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
