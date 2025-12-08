class Backpack:
    """
    Рюкзак персонажа.
    """

    max_capacity = 9           # ограничение для food/potion/scroll
    max_capacity_weapon = 10   # ограничение для оружия

    def __init__(self):
        self.items = {
            "food": [],
            "potion": [],
            "scroll": [],
            "weapon": []
        }
        self.treasure = 0

        # Список выбранного типа предметов — под использование
        self.current_item_list = []
        self.current_type = None

    def add_item(self, item):
        """
        Кладёт предмет в рюкзак.
        """

        # Сокровище — просто увеличить золото
        if item.item_type == "treasure":
            self.treasure += item.value
            return f"Получено {item.value} золота"

        if item.item_type not in self.items:
            return f"Неизвестный тип предмета: {item.item_type}"

        target = self.items[item.item_type]

        # Лимиты
        limit = self.max_capacity_weapon if item.item_type == "weapon" else self.max_capacity

        if len(target) >= limit:
            return f"Раздел '{item.item_type}' заполнен!"

        target.append(item)
        return f"Предмет {item.subtype} добавлен в рюкзак."

    # ----------------------------------------
    # ДОСТУП К ПРЕДМЕТАМ
    # ----------------------------------------

    def get_items(self, item_type):
        self.current_type = item_type
        self.current_item_list = self.items.get(item_type, [])
        with open('items.log', "a") as f:
            f.write(str(self.current_item_list))

        return self.current_item_list

    def use_item(self, index, character):
        items_list = self.current_item_list
        
        if not items_list:
            return ""

        if index < 0 or index >= len(items_list):
            return "Неверный индекс"

        item = items_list[index]
        result = item.apply_to_character(character)
        
        # Удаляем предмет из рюкзака
        if item in self.items.get(self.current_type, []):
            self.items[self.current_type].remove(item)
        
        self.current_item_list = []
        return f"Использован {item.subtype}: {result}"

    # Новые методы для получения предметов по типам
    def get_weapons(self):
        return self.items.get("weapon", [])

    def get_food(self):
        return self.items.get("food", [])

    def get_potions(self):
        return self.items.get("potion", [])

    def get_scrolls(self):
        return self.items.get("scroll", [])

    def remove_item(self, item):
        """Удаляет предмет из рюкзака"""
        for item_type in self.items:
            if item in self.items[item_type]:
                self.items[item_type].remove(item)
                return True
        return False

    def count_items(self):
        """Возвращает общее количество предметов"""
        total = 0
        for item_type in self.items:
            total += len(self.items[item_type])
        return total
