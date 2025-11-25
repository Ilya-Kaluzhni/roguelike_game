from enemy import Enemy


class Mimic(Enemy):
    def __init__(self, cord_x, cord_y):
        super().__init__(
            type_='mimic',
            health=150,  # высокое здоровье
            dexterity=75,  # высокая ловкость
            strength=25,  # низкая сила
            hostility='LOW',  # низкая враждебность
            view={'letter': 'm', 'color': 'white'},
            x=cord_x,
            y=cord_y
        )
