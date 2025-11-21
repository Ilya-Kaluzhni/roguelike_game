from enemy import *
from src.core.movement.directions import *
from random import choice


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
