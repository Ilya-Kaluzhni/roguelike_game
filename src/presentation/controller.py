from ..domain.game.loop import GameLoop

class Controller:
    def __init__(self):
        self.back = GameLoop()

    def get_input_give_update(self, input_key):
