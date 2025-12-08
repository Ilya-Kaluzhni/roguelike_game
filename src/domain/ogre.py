from domain.enemy import Enemy
from presentation.static import Directions,DetectionRange
from random import choice


class Ogre(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='ogre',
            health=150,
            dexterity=25,
            strength=150,
            hostility=DetectionRange.AVERAGE,
            view={'letter': 'O', 'color': 'yellow'},
            x=cord_x,
            y=cord_y
        )
        self.cooldown_after_attack = False


    def move_pattern(self):
        direction = choice(Directions.simple_directions())
        first_step_x, first_step_y = super().change_cords(self.x, self.y, direction)
        new_cords = super().change_cords(first_step_x, first_step_y, direction)
        return new_cords