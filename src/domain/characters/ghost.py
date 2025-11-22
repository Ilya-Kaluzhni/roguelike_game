from enemy import Enemy
from random import randint

class Ghost(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='ghost',
            health=25,  # низкое здоровье
            dexterity=75,  # высокая ловкость
            strength=25,  # низкая сила
            hostility='LOW',  # низкая враждебность
            view={'letter': 'G', 'color': 'white'},
            x=cord_x,
            y=cord_y
        )

    def move_pattern(self,room_cords_x = 0, room_cords_y =0):
            direction_x = randint(0, room_cords_x)
            direction_y = randint(0, room_cords_y)
            return direction_x, direction_y
