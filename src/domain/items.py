class Item:
    """
    Универсальный предмет игры.
    """

    def __init__(
            self,
            item_type: str,  # weapon / food / potion / scroll / treasure
            subtype: str,
            letter: str,
            health: int = 0,
            max_health: int = 0,
            dexterity: int = 0,
            strength: int = 0,
            value: int = 0
    ):
        self.item_type = item_type
        self.subtype = subtype

        self.health = health
        self.max_health = max_health
        self.dexterity = dexterity
        self.strength = strength
        self.letter = letter

        self.value = value
        self.x = 0
        self.y = 0

    def __str__(self):
        return self.subtype

    def __repr__(self):
        return self.subtype

    # ----------------------------------------
    # ЛОГИКА ИСПОЛЬЗОВАНИЯ ПРЕДМЕТА
    # ----------------------------------------
    def set_cords(self, x, y):
        self.x = x
        self.y = y

    def get_cords(self):
        return self.x, self.y

    def apply_to_character(self, character):
        """
        Накладывает эффект предмета на персонажа.
        Возвращает строку для UI.
        """

        messages = []

        if self.health:
            character.health = min(character.health + self.health, character.max_health)
            messages.append(f"+{self.health} HP")

        if self.max_health:
            character.max_health += self.max_health
            character.health += self.max_health
            messages.append(f"+{self.max_health} макс. HP")

        if self.dexterity:
            character.dexterity += self.dexterity
            messages.append(f"+{self.dexterity} ловкости")

        if self.strength:
            character.strength += self.strength
            messages.append(f"+{self.strength} силы")

        if not messages:
            return "Этот предмет ничего не сделал."

        return ", ".join(messages)

    def presentation_data(self):
        return {
            'type': self.letter,
            'x': self.x,
            'y': self.y
        }
