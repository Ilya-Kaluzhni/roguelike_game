from enemy import Enemy
from random import randint
from static import DetectionRange


class Ghost(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='ghost',
            health=25,  # низкое здоровье
            dexterity=75,  # высокая ловкость
            strength=25,  # низкая сила
            hostility=DetectionRange.LOW,  # низкая враждебность
            view={'letter': 'G', 'color': 'white'},
            x=cord_x,
            y=cord_y
        )

    def move_pattern(self, start_x=0, start_y=0, room_cords_x=0, room_cords_y=0):
        direction_x = randint(start_x, start_x + room_cords_x - 1)
        direction_y = randint(start_y, start_y + room_cords_y - 1)
        with open('d.log', 'a') as log:
            log.write(f'Новые{direction_x, direction_y}\n')
        return direction_x, direction_y
