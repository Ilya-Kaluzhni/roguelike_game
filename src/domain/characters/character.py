from static import Directions


class Character:

    def __init__(self, cord_x, cord_y, backpack):
        self.max_health = 1
        self.health = 20
        self.dexterity = 1
        self.strength = 1
        self.x = cord_x
        self.y = cord_y
        self.backpack = backpack
        self.current_weapon = None
        self.in_fight = False
        self.asleep = False

    def make_step(self, direction: Directions):
        dx, dy = direction.value
        self.x += dx
        self.y += dy

    def set_cords(self, cord_x, cord_y):
        self.x, self.y = cord_x, cord_y

    def get_cords(self):
        return self.x, self.y

    def put_item(self, item):
        return self.backpack.add_item(item)

    def get_items_by_type(self, item_type):
        return self.backpack.get_list_of_item(item_type)

    def select_weapon(self, index):
        weapons = self.backpack.get_items('weapon')
        if not weapons:
            return 'У вас нет оружия'
        if index < 0 or index >= len(weapons):
            return f'Выберите оружие из: {", ".join([f'{idx} {w.name}' for idx, w in enumerate(weapons)])}'
        self.current_weapon = weapons[index]
        return f'Вы выбрали оружие: {self.current_weapon.name}'

    def use_item(self, index, effect_processor):
        items_list = self.backpack.current_item_list
        if not items_list:
            return "У вас нет ничего"

        if index >= len(index):
            return f"Выберите индекс из 0 по {len(items_list) - 1}"

        item = items_list.pop(index)
        result = effect_processor.apply_item(self, item)
        return result

    def presentation_data(self):
        return {
            'health': self.health,
            'max_health': self.max_health,
            'strength': self.strength,
            'x': self.x,
            'y': self.y
        }


class Backpack:
    max_capacity_weapon = 10
    max_capacity = 9

    def __init__(self):
        self.items = {
            'food': [],
            'elixir': [],
            'scroll': [],
            'weapon': []
        }
        self.treasure = 0
        self.current_item_list = []

    # Добавляет в определенный список атрибутов предмет
    def add_item(self, item):
        if item.type == 'treasure':
            self.treasure += item.value
            return f"Вы получили {item.value} сокровищ"
        if self.items[item.type] == 'weapon' and len(self.items[item.type]) >= self.max_capacity:
            return f"Уберите оружие чтобы взять новое"
        if len(self.items[item.type]) >= self.max_capacity:
            return f"Отделение {item.type} в рюкзаке заполнено"
        self.items[item.type].append(item)
        return f"{item.type} добавлен добавлен в рюкзак"

    # Возвращает список предметов для использования
    def get_items(self, item_type):
        self.current_item_list = self.items.get(item_type, [])
        return self.current_item_list


class EffectProcessor:
    @staticmethod
    def apply_item(self, character, item):
        increased = []
        if hasattr(item, 'health') and item.health != 0:
            character.health += item.health
            increased.append('здоровье')
        if hasattr(item, 'dexterity') and item.dexterity != 0:
            character.dexterity += item.dexterity
            increased.append('ловкость')
        if hasattr(item, 'strength') and item.strength != 0:
            character.strength += item.strength
            increased.append('сила')
        if increased:
            return f"Использован {item.name}. Повышено: {', '.join(increased)}."
        else:
            return f"Использован {item.name}. Изменений нет."
