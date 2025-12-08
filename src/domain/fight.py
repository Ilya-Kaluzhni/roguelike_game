from random import randint, random,choice


class Fight:
    def __init__(self, player, monster):
        self.player = player
        self.player.in_fight = True
        self.monster = monster
        self.turn_player = False
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
        if random() * 100 < chance or self.monster.type == 'ogre':
            return True
        return False

    # 2 этап 'Расчет урона' высчитывает урон, который наносится при атаке
    def calculate_damage(self):
        damage = self.initial_damage
        if self.turn_player:
            if not (self.monster.type == 'vampire' and self.player_first_attack) and not (
                    self.monster.type == 'snake' and self.player.asleep):
                if self.player.current_weapon and self.player.current_weapon.strength:
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
            return self.player.regen_limit / self.max_hp_part
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
        with open('f.log', 'a') as log:
            log.write(f'{self.turn_player}\n')
        if self.turn_player:
            if self.check_hit():
                damage = self.calculate_damage()
                self.monster.health -= damage
                message = f'Вы нанесли монстру {damage} урона'
                with open('fight.log', 'a') as log:
                    log.write(f'Зашел\n')
            else:
                message = 'К сожалению, вы промахнулись!'
                with open('fight.log', 'a') as log:
                    log.write(f'Не зашел\n')
            if self.monster.health <= 0:
                self.player.backpack.treasure += int(self.calculate_loot())
                self.player.bit_enemy += 1
                message = 'Вы победили монстра!'
            self.next_turn()
        else:
            if self.check_hit():
                damage = self.calculate_damage()
                self.player.health -= damage
                message = f' Монстер нанес вам {damage} урона!'
                with open('fight.log', 'a') as log:
                    log.write(f'Зашел\n')
            else:
                message = ' Вы увернулись от монстра!'
                with open('fight.log', 'a') as log:
                    log.write(f'Не зашел\n')
        return message

    def set_turn_monster(self):
        self.turn_player = False

    def set_turn_player(self):
        self.turn_player = True

    def calculate_loot(self):
        return (self.monster.dexterity * self.loot_dexterity_factor +
                self.monster.health * self.loot_hp_factor +
                self.monster.strength * self.loot_strength_factor +
                randint(0, 19))

    def next_turn(self):
        self.turn_player = not self.turn_player
        if self.turn_player:
            self.player_first_attack = False

    def player_action(self, new_cords):
        monster_cords = self.monster.get_cords()
        if new_cords == monster_cords:
            self.set_turn_player()
            message = self.attack()
            self.player_first_attack = False
        else:
            self.turn_player = False
            if not self.player_first_attack:
                message = choice(["Вы решили быть пацифистом.", "Вы убегаете от монстра."])
            else:
                message = 'Нападение!'

        return message
