from enemy import *
from src.core.movement.directions import *
from random import randint


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
