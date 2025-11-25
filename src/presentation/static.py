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