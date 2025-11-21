from random import randint, random


class Fight:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.turn_player = True
        self.hit_chance = 70
        self.dexterity_factor = 0.3
        self.standard_dexterity = 50
        self.standard_strength = 50
        self.strength_factor = 0.3
        self.strength_addition = 65
        self.initial_damage = 30
        self.sleep_chance = 15
        self.max_hp_part = 10
        self.loot_dexterity_factor = 0.2
        self.loot_hp_factor = 0.5
        self.loot_strength_factor = 0.5
        self.maximum_fights = 8
        self.player_first_attack = True

    # 1 этап 'Расчет удара' вычисляет вероятность успешного попадания удара
    def check_hit(self):
        chance = self.hit_chance
        if self.turn_player:
            chance += (self.player.dexterity - self.monster.dexterity - self.standard_dexterity) * self.dexterity_factor
        else:
            chance += (self.monster.dexterity - self.player.dexterity - self.standard_dexterity) * self.dexterity_factor
        if random() < chance or self.monster.type == 'ogre':
            return True
        return False

    # 2 этап 'Расчет урона' высчитывает урон, который наносится при атаке
    def calculate_damage(self):
        damage = self.initial_damage
        if self.turn_player:
            if not (self.monster.type == 'vampire' and self.player_first_attack) and not (
                    self.monster.type == 'snake' and self.player.asleep):
                if self.player.current_weapon.strength:
                    damage += self.player.current_weapon.strength * (
                            self.player.strength + self.strength_addition) / 100
                else:
                    damage += (self.player.strength - self.standard_strength) * self.strength_factor
            elif self.monster.type == 'vampire' and self.player_first_attack:
                self.player_first_attack = False
            else:
                self.player.asleep = False
        else:
            damage = self.monster_damage_formula()
        return damage

    # формулы расчёта урона для разных монстров
    def monster_damage_formula(self):
        if self.monster.type == 'vampire':
            return self.player.regen_limit / self.max_hp_part  # Что такое regen_limit
        elif self.monster.type == 'ogre':
            if not self.monster.cooldown_after_attack:
                self.monster.cooldown_after_attack = True
                return (self.monster.strength - self.standard_strength) * self.strength_factor
            else:
                self.monster.cooldown_after_attack = False
                return 0
        else:
            if self.monster.type == 'snake' and randint(0, 99) < self.sleep_chance:
                self.player.asleep = True
            return self.initial_damage + (self.monster.strength - self.standard_strength) * self.strength_factor

    # 3 этап 'Применение урона'
    def attack(self):
        if self.turn_player:
            if self.check_hit():
                self.monster.health -= self.calculate_damage()
            if self.monster.health <= 0:
                self.player.backpack.treasures += self.calculate_loot()
        else:
            if self.check_hit():
                self.player.health -= self.calculate_damage()

    def calculate_loot(self):
        return (self.monster.dexterity * self.loot_dexterity_factor +
                self.monster.health * self.loot_hp_factor +
                self.monster.strength * self.loot_strength_factor +
                randint(0, 19))
