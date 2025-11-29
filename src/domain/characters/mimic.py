from enemy import Enemy
from static import DetectionRange
from random import choice

class Mimic(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='mimic',
            health=150,  # высокое здоровье
            dexterity=75,  # высокая ловкость
            strength=25,  # низкая сила
            hostility=DetectionRange.LOW,  # низкая враждебность
            view={'letter': 'm', 'color': 'white'},
            x=cord_x,
            y=cord_y
        )
        self.view['letter'] = choice(['f','e','s','w'])

    def move_pattern(self):
        return self.x, self.y

    def presentation_data(self):
        letter = self.view['letter']
        if self.in_fight:
            letter = 'm'
        return {
            'type': letter,
            'color': self.view['color'],
            'x': self.x,
            'y': self.y
        }
