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

    # ----------------------------------------
    # ДОБАВЛЕНИЕ ПРЕДМЕТА
    # ----------------------------------------

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

        target_list = self.items[item.item_type]

        # Лимиты
        limit = (
            self.max_capacity_weapon
            if item.item_type == "weapon"
            else self.max_capacity
        )

        if len(target_list) >= limit:
            return f"Раздел '{item.item_type}' заполнен"

        target_list.append(item)
        return f"{item.subtype} добавлен в рюкзак"

    # ----------------------------------------
    # ДОСТУП К ПРЕДМЕТАМ
    # ----------------------------------------

    def get_items(self, item_type):
        """
        Возвращает список предметов типа.
        И сохраняет его в current_item_list, чтобы можно было использовать.
        """

        self.current_item_list = self.items.get(item_type, [])
        return self.current_item_list
