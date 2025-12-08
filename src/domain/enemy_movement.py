class MoveEnemy:
    max_tries = 16

    def __init__(self, level):
        self.level = level

    def move(self, enemy, character_cords):
        if enemy.must_chase_character(character_cords):
            self.shortest_path(enemy, character_cords)
        else:
            self.move_by_own(enemy)

    def move_by_own(self, enemy):
        old_cord_x, old_cord_y = enemy.get_cords()
        self.level.tiles[old_cord_y][old_cord_x] = '.'
        for i in range(self.max_tries):
            if enemy.type == 'ghost':
                with open('d.log', 'a') as log:
                    log.write(f'Координаты комнаты{(self.level.get_room_size(old_cord_x, old_cord_y))}\n')
                new_cord_x, new_cord_y = enemy.move_pattern(*(self.level.get_room_size(old_cord_x, old_cord_y)))
            else:
                new_cord_x, new_cord_y = enemy.move_pattern()
            if self.level.is_walkable(new_cord_x, new_cord_y):
                enemy.set_cords(new_cord_x, new_cord_y)
                self.level.tiles[old_cord_y][old_cord_x] = '.'
                self.level.tiles[new_cord_y][new_cord_x] = enemy.view['letter']
                break

    def shortest_path(self, enemy, target_pos):
        steps = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]
        nearest = enemy.get_cords()
        min_dist = self.get_distance(nearest, target_pos)
        with open('d.log', 'a') as log:
            log.write(f'Ищем клеточку{nearest}\n')
        if min_dist == 0:
            return
        for dx, dy in steps:
            new_x = nearest[0] + dx
            new_y = nearest[1] + dy

            if self.level.is_walkable(new_x, new_y):
                dist = self.get_distance((new_x, new_y), target_pos)
                if dist < min_dist:
                    min_dist = dist
                    nearest = (new_x, new_y)
                with open('d.log', 'a') as log:
                    log.write(f'{nearest, min_dist,(new_x, new_y), dist}:\n')
        with open('d.log', 'a') as log:
            log.write(f'Итого {nearest, min_dist}:\n')
        if min_dist <= 1:
            enemy.in_fight = True
        if min_dist >= 1:
            old = enemy.get_cords()
            self.level.tiles[old[1]][old[0]] = '.'
            enemy.set_cords(nearest[0], nearest[1])
            self.level.tiles[nearest[1]][nearest[0]] = enemy.view['letter']


    @staticmethod
    def get_distance(cell_cords, enemy_cords):
        return abs(cell_cords[0] - enemy_cords[0]) + abs(cell_cords[1] - enemy_cords[1])
