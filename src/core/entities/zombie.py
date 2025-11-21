from enemy import *
from src.core.movement.directions import *
from random import choice


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
