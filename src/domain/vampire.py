from domain.enemy import Enemy
from presentation.static import Directions,DetectionRange
from random import choice


class Vampire(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='vampire',
            health=150,
            dexterity=75,
            strength=75,
            hostility=DetectionRange.HIGH,
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
