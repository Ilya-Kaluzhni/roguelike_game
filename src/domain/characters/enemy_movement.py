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
        for _ in range(self.max_tries):
            if enemy.type == 'ghost':
                new_cord_x, new_cord_y = enemy.move_pattern(self.level.width, self.level.height)
            else:
                new_cord_x, new_cord_y = enemy.move_pattern()
            if self.level.is_walkable(new_cord_y, new_cord_x):
                enemy.set_cords(new_cord_x, new_cord_y)
                self.level.tiles[old_cord_y][old_cord_x] = '.'  # в зависимости от типа точки
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

        for dx, dy in steps:
            new_x = nearest[0] + dx
            new_y = nearest[1] + dy

            if self.level.is_walkable(new_x, new_y):
                dist = self.get_distance(nearest, target_pos)
                if dist < min_dist:
                    min_dist = dist
                    nearest = (new_x, new_y)
        if min_dist <= 1:
            enemy.in_fight = True
            if min_dist == 1:
                enemy.set_cords(nearest[0], nearest[1])
                self.level.tiles[nearest[1]][nearest[0]] = '.'  # в зависимости от типа точки
                self.level.tiles[nearest[1]][nearest[0]] = enemy.view['letter']

    @staticmethod
    def get_distance(cell_cords, enemy_cords):
        return abs(cell_cords[0] - enemy_cords[0]) + abs(cell_cords[1] - enemy_cords[1])
