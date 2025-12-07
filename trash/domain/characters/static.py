from enum import Enum

class Keys(Enum):
    W_UP = (87, 119)  # W и w
    A_LEFT = (65, 97)  # A и a
    S_DOWN = (83, 115)  # S и s
    D_RIGHT = (68, 100)  # D и d

    H_USE_WEAPON = (72, 104)  # H и h
    J_USE_FOOD = (74, 106)  # J и j
    K_USE_ELIXIR = (75, 107)  # K и k
    E_USE_SCROLL = (69, 101) # E и e

    Q_CLOSE = (81, 113)



class Directions(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DIAGONALLY_UP_LEFT = (-1, -1)
    DIAGONALLY_UP_RIGHT = (1, -1)
    DIAGONALLY_DOWN_LEFT = (-1, 1)
    DIAGONALLY_DOWN_RIGHT = (1, 1)

    @classmethod
    def simple_directions(cls):
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]

    @classmethod
    def diagonal_directions(cls):
        return [
            cls.DIAGONALLY_UP_LEFT,
            cls.DIAGONALLY_UP_RIGHT,
            cls.DIAGONALLY_DOWN_LEFT,
            cls.DIAGONALLY_DOWN_RIGHT
        ]

class DetectionRange(Enum):
    LOW = 2
    AVERAGE = 4
    HIGH = 6