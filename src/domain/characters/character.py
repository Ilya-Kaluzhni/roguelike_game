from static import Directions


class Character:

    def __init__(self, cord_x, cord_y, backpack):
        self.max_health = 20
        self.health = 20
        self.dexterity = 1
        self.strength = 1

        self.x = cord_x
        self.y = cord_y

        self.backpack = backpack
        self.current_weapon = None

        self.in_fight = False
        self.asleep = False

    # ----------------------------------
    # MOVEMENT
    # ----------------------------------

    def make_step(self, direction: Directions):
        dx, dy = direction.value
        self.x += dx
        self.y += dy

    def set_cords(self, cord_x, cord_y):
        self.x, self.y = cord_x, cord_y

    def get_cords(self):
        return self.x, self.y

    # ----------------------------------
    # ITEMS
    # ----------------------------------

    def put_item(self, item):
        return self.backpack.add_item(item)

    def get_items_by_type(self, item_type):
        return self.backpack.get_items(item_type)

    def select_weapon(self, index):
        weapons = self.backpack.get_items('weapon')
        if not weapons:
            return "У вас нет оружия"

        if index < 0 or index >= len(weapons):
            return f'Выберите оружие от 0 до {len(weapons)-1}'

        self.current_weapon = weapons[index]
        return f'Вы выбрали оружие: {self.current_weapon.subtype if hasattr(self.current_weapon, "subtype") else self.current_weapon}'

    def use_item(self, index):
        """
        Использует предмет через встроенный механизм item.apply_to_character().
        """

        items_list = self.backpack.current_item_list
        if not items_list:
            return "У вас нет предметов этого типа"

        if index < 0 or index >= len(items_list):
            return f"Выберите индекс от 0 до {len(items_list) - 1}"

        item = items_list.pop(index)  # удалить из рюкзака

        result = item.apply_to_character(self)
        return f"Использован {item.subtype}. {result}"

    # ----------------------------------
    # UI data
    # ----------------------------------

    def presentation_data(self):
        return {
            'health': self.health,
            'max_health': self.max_health,
            'strength': self.strength,
            'dexterity': self.dexterity,
            'x': self.x,
            'y': self.y
        }
