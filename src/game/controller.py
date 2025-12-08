# from src7.domain.game.core import GameController
from core import GameController
from static import Keys

class Controller:
    def __init__(self):
        self.back = GameController()

    def get_input_give_update(self, input_key):
        keys_int = {key.value: key for key in Keys}
        if input_key in Keys.W_UP.value:
            input_key = Keys.W_UP
        elif input_key in Keys.S_DOWN.value:
            input_key = Keys.S_DOWN
        elif input_key in Keys.A_LEFT.value:
            input_key = Keys.A_LEFT
        elif input_key in Keys.D_RIGHT.value:
            input_key = Keys.D_RIGHT
        # elif Keys.INDEX_0.value <= input_key <= Keys.INDEX_9.value:
        #     input_key = keys_int[input_key]
        return self.back.handle_input(input_key)

    def _auto_save(self):
        """Автосохранение после прохождения уровня"""
        game_state = self.get_game_state()
        # Создаём временную карту для получения состояния explored
        from map import GameMap
        temp_map = GameMap()
        temp_map.add_rooms(self.level[0])
        temp_map.add_corridors(self.level[1])
        temp_map.explored = [row[:] for row in self.game_map.tiles]  # копируем для сохранения
        # Передаём рюкзак, персонажа и карту для полного сохранения
        self.save_manager.save_game(game_state, self.backpack, self.character, temp_map)
        print(f'Игра сохранена (уровень {self.n_level})')

    def load_from_save(self, save_data: dict) -> bool:
        """Загружает состояние игры из сохранённых данных"""
        try:
            self.n_level = save_data.get('level', 1)
            
            # Восстанавливаем характеристики персонажа
            player_data = save_data.get('player', {})
            self.character.health = player_data.get('health', 40)
            self.character.max_health = player_data.get('max_health', 40)
            self.character.strength = player_data.get('strength', 15)
            self.character.dexterity = player_data.get('dexterity', 6)
            self.character.regen_limit = player_data.get('regen_limit', 40)
            
            # Восстанавливаем золото в рюкзаке
            self.backpack.treasure = player_data.get('gold', 0)
            
            # Восстанавливаем предметы рюкзака
            backpack_data = save_data.get('backpack', {})
            if backpack_data:
                # ...existing backpack restore code...
                pass
            
            # Восстанавливаем врагов и предметы
            self.enemies = []
            self.items = []
            
            # Генерируем уровень заново, но с восстановленным n_level
            self.load_level()
            
            return True
        except Exception as e:
            print(f'Ошибка при загрузке сохранения: {e}')
            return False
