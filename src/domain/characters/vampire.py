from enemy import Enemy
from static import Directions
from random import choice


class Vampire(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='vampire',
            health=150,  # высокая здоровье
            dexterity=75,  # высокая ловкость
            strength=75,  # средняя сила
            hostility='HIGH',  # высокая враждебность
            view={'letter': 'V', 'color': 'red'},
            x=cord_x,
            y=cord_y
        )
        self.vampire_first_attack = True  # Первый удар по вампиру — промах

    # Выбирает рандомно направление движения из всех возможных направлений
    def move_pattern(self):
        direction = choice(list(Directions))
        new_cords = super().change_cords(self.x, self.y, direction)
        return new_cords
