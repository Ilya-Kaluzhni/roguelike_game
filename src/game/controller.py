# from src7.domain.game.core import GameController
from core import GameController
from static import Keys

class Controller:
    def __init__(self):
        self.back = GameController()

    def get_input_give_update(self, input_key):
        # with open('d.log', 'a') as f:
        #     f.write('Зашел в контроллер\n')
        if input_key in Keys.W_UP.value:
            input_key = Keys.W_UP
        elif input_key in Keys.S_DOWN.value:
            input_key = Keys.S_DOWN
        elif input_key in Keys.A_LEFT.value:
            input_key = Keys.A_LEFT
        elif input_key in Keys.D_RIGHT.value:
            input_key = Keys.D_RIGHT
        return self.back.handle_input(input_key)
