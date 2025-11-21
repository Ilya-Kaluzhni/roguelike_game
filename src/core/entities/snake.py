from enemy import *
from src.core.movement.directions import *
from random import choice


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
