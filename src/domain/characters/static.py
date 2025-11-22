from enum import Enum


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
    LOW = 2,
    AVERAGE = 4,
    HIGH = 6