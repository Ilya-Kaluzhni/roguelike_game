# # # рендер локации, сущностей
import curses
import curses
import math


class RenderingActors:
    def __init__(self, stdscr, start_y=0, start_x=0):
        # self.player = None
        self.height = 25
        self.width = 80
        self.window = stdscr.subwin(self.height, self.width, start_y, start_x)
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Игрок
        curses.init_pair(2, curses.COLOR_WHITE, -1)  # Стены, пол

        curses.init_pair(30, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(31, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(32, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(33, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(34, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(35, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        for i in range(5):
            intensity = 500 - i * 100
            curses.init_color(50 + i, intensity, intensity, intensity)
            curses.init_pair(50 + i, 50 + i, -1)

        # Игровые данные устанавливаются позднее
        self.game_map = None
        self.player_x = 0
        self.player_y = 0
        self.monsters = []
        self.monsters_data = {
            'Z': 32,
            'G': 30,
            'O': 35,
            'V': 31,
            'S': 30,
            'm': 30
        }

        self.items = []
        self.items_data = {
            'w': [31, 'w'],  # оружие
            'f': [32, '♣'],  # еда
            'e': [33, curses.ACS_PLMINUS],  # эликсир
            's': [34, curses.ACS_DIAMOND],  # сокровище
            't': [35, '*'],  # свиток
        }

        self.player_angle = 0
        self.tride = False

        self.tride_actors = {
            'Z': [
                "//////",
                "    / ",
                "   /  ",
                "  /   ",
                "//////"
            ],
            'O': [
                " //// ",
                "/    /",
                "/    /",
                "/    /",
                " //// "
            ],
            'V': [
                "\\    /",
                "\\    /",
                " \\  / ",
                "  \\/  ",
                "   |  "
            ],
            'G': [
                " //// ",
                "/     ",
                "/  ///",
                "/    /",
                " //// "
            ],
            'S': [
                " //// ",
                "/     ",
                " //// ",
                "     /",
                " //// "
            ],
            'm': [
                "/    /",
                "/    /",
                "/ \\/ /",
                "/  |  /",
                "/    /"
            ],
            'i': [
                ' * ',
                '***',
                '***',
                ' * '
            ]

        }

    def create_mini_window(self, stdscr, height, width, start_y, start_x):
        self.mini_window = stdscr.subwin(height, width, start_y, start_x)

    def setup_game_objects(self, game_map, player_coords, monsters=None, items=None):
        self.game_map = game_map
        self.player_x, self.player_y = player_coords
        self.monsters = monsters or []
        self.items = items or []

    def draw_map(self):
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                ch = self.game_map.get_tile_display(x, y)
                if ch in ('#', '.', '+', ','):
                    color = curses.color_pair(0)
                    if ch == ',':
                        ch = '.'
                        color = curses.color_pair(2) | curses.A_DIM
                    try:
                        self.window.addch(y, x, ch, color)
                    except curses.error:
                        pass

    def draw_actors(self):
        self.draw_items()
        self.draw_monsters()
        self.window.addch(self.player_y, self.player_x, '@', curses.color_pair(1) | curses.A_BOLD)

    def draw_items(self):
        for item in self.items:
            if self.game_map.visible[item['y']][item['x']]:
                self.draw_item(self.window, item, item['x'], item['y'])

    def draw_item(self, win, item, x, y):
        ch = self.items_data[item['type']][1]
        color_n = self.items_data[item['type']][0]
        win.addch(y, x, ch, curses.color_pair(color_n))

    def draw_monsters(self):
        for monster in self.monsters:
            if self.game_map.visible[monster['y']][monster['x']]:
                self.draw_monster(self.window, monster, monster['x'], monster['y'])

    def draw_monster(self, win, monster, x, y):
        ch = monster['type']
        if ch in ['f', 'e', 's', 'w']:
            color_n = self.items_data[ch][0]
            ch = self.items_data[ch][1]

            win.addch(y, x, ch, curses.color_pair(color_n))
        else:
            color_n = self.monsters_data[monster['type']]
            win.addch(y, x, monster['type'], curses.color_pair(color_n))

    def render(self):
        self.window.clear()
        self.window.border()
        self.draw_map()
        self.draw_actors()
        self.window.noutrefresh()

    def set_direction(self, direction):
        if direction == 'up':
            self.player_angle = 3 * math.pi / 2
        elif direction == 'down':
            self.player_angle = math.pi / 2
        elif direction == 'left':
            self.player_angle = math.pi
        elif direction == 'right':
            self.player_angle = 0

    def cast_ray(self, col):
        fov = math.pi / 3
        ray_angle = self.player_angle - fov / 2 + (col / self.width) * fov
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # DDA - исправлены границы и проверки
        map_x, map_y = self.player_x, self.player_y

        # Расстояние шаг
        delta_dist_x = abs(1 / cos_a) if abs(cos_a) > 0 else 0
        delta_dist_y = abs(1 / sin_a) if abs(sin_a) > 0 else 0

        step_x = 1 if cos_a > 0 else -1
        step_y = 1 if sin_a > 0 else -1

        if cos_a > 0:
            side_dist_x = (map_x + 1.0 - self.player_x) * delta_dist_x
        else:
            side_dist_x = (self.player_x - map_x - 1) * delta_dist_x

        if sin_a > 0:
            side_dist_y = (map_y + 1.0 - self.player_y) * delta_dist_y
        else:
            side_dist_y = (self.player_y - map_y - 1) * delta_dist_y

        find_wall = False
        side = 0

        map_width = self.width
        map_height = self.height

        while not find_wall:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if (map_x < 0 or map_x >= map_width or
                    map_y < 0 or map_y >= map_height or
                    self.game_map.tiles[map_y][map_x] == '#' or self.game_map.tiles[map_y][map_x] == ' '):
                find_wall = True

        if side == 0:
            wall_dist = abs((map_x - self.player_x + (1 - step_x) / 2) / (cos_a + 0.0001))
        else:
            wall_dist = abs((map_y - self.player_y + (1 - step_y) / 2) / (sin_a + 0.0001))

        proj_height = int(self.height / (wall_dist + 0.0001))
        return min(proj_height, self.height), side, wall_dist, self.game_map.tiles[map_y][map_x]

    def get_visible_entities(self, entities, max_dist):
        """Возвращает список видимых объектов из entities с расстоянием и углом"""
        fov = math.pi / 3
        visible = []
        for entity in entities:
            dx = entity['x'] - self.player_x
            dy = entity['y'] - self.player_y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > max_dist:
                continue

            angle = math.atan2(dy, dx)
            delta_angle = abs(angle - self.player_angle)
            delta_angle = min(delta_angle, 2 * math.pi - delta_angle)

            if delta_angle > fov / 2:
                continue

            visible.append((dist, entity, delta_angle, angle))

        visible.sort(reverse=True, key=lambda x: x[0])
        return visible

    def draw_entity_sprite(self, sprite, dist, delta_angle, angle, color_pair, scale_factor=6):
        """Рисует один спрайт entity с учётом расстояния и угла"""
        sprite_height = len(sprite)
        sprite_width = len(sprite[0])
        scale = max(0.1, scale_factor / dist)
        height = int(sprite_height * scale)
        width = int(sprite_width * scale)

        center_x = self.width // 2
        center_y = self.height // 2

        side = 1 if angle - self.player_angle >= 0 else -1
        screen_x = int(center_x + (delta_angle / (math.pi / 3 / 2)) * (self.width / 2) * side)
        screen_y = center_y - height // 2

        for i in range(height):
            row = screen_y + i
            if 0 <= row < self.height:
                for j in range(width):
                    col = screen_x - width // 2 + j
                    if 0 <= col < self.width:
                        orig_i = min(int(i / scale), sprite_height - 1)
                        orig_line = sprite[orig_i]
                        orig_j = min(int(j / scale), len(orig_line) - 1)
                        ch = sprite[orig_i][orig_j]
                        if ch != ' ':
                            self.window.addch(row, col, '*', color_pair)

    def render_monster_tride(self):
        visible_monsters = self.get_visible_entities(self.monsters, max_dist=6)
        for dist, monster, delta_angle, angle in visible_monsters:
            monster_type = monster['type']
            sprite = self.tride_actors.get(monster_type, self.tride_actors.get('m'))
            color = curses.color_pair(self.monsters_data.get(monster_type, 0))
            self.draw_entity_sprite(sprite, dist, delta_angle, angle, color, scale_factor=6)

    def render_items_tride(self):
        visible_items = self.get_visible_entities(self.items, max_dist=8)
        for dist, item, delta_angle, angle in visible_items:
            sprite = self.tride_actors.get('i')
            color = curses.color_pair(self.items_data.get(item['type'], [5])[0])
            if dist > 6:
                color |= curses.A_DIM
            self.draw_entity_sprite(sprite, dist, delta_angle, angle, color, scale_factor=8)

    def render_d(self):
        self.window.clear()

        sky_start = 0
        sky_end = self.height // 2
        for row in range(sky_start, sky_end):
            self.window.addstr(row, 0, " " * self.width, curses.color_pair(1) | curses.A_BOLD)

        # Пол (нижняя половина экрана)
        floor_start = self.height // 2
        floor_end = self.height - 1
        for row in range(floor_start, floor_end):
            distance = abs(row - self.player_x)
            color = curses.color_pair(54) | curses.A_BOLD
            if distance > 16:
                color = curses.color_pair(50) | curses.A_BOLD
            elif distance > 11:
                color = curses.color_pair(51) | curses.A_BOLD
            elif distance > 7:
                color = curses.color_pair(52) | curses.A_DIM
            elif distance > 3:
                color = curses.color_pair(53) | curses.A_DIM

            self.window.addstr(row, 0, "." * self.width, color)
        with open('3d.log', 'w') as file:
            file.write('Start')
        for col in range(self.width):
            height, side, distance, char_wall = self.cast_ray(col)
            char = curses.ACS_BLOCK
            color = curses.color_pair(0) | curses.A_BOLD
            if char_wall == ' ':
                char = '|'
            if distance > 16:
                color = curses.color_pair(53) | curses.A_DIM
            elif distance > 11:
                color = curses.color_pair(52) | curses.A_DIM
            elif distance > 7:
                color = curses.color_pair(51) | curses.A_BOLD
            elif distance > 3:
                color = curses.color_pair(50) | curses.A_BOLD

            wall_top = max(0, (self.height - height) // 2)
            wall_bottom = min(self.height - 1, (self.height + height) // 2)

            for row in range(wall_top, wall_bottom):
                self.window.addch(row, col, char, color)
        self.render_items_tride()
        self.render_monster_tride()

        self.window.noutrefresh()

    def draw_mini_window(self):
        self.mini_window.clear()
        self.mini_window.border()
        distance = 5
        mini_size = distance * 2
        items = [(item['x'], item['y']) for item in self.items]
        monsters = [(monster['x'], monster['y']) for monster in self.monsters]
        cells = []
        self.mini_window.clear()
        self.mini_window.border()

        for mini_y in range(mini_size):
            for mini_x in range(mini_size):
                map_x = self.player_x - distance + mini_x
                map_y = self.player_y - distance + mini_y

                if (0 <= map_x < self.game_map.width and
                        0 <= map_y < self.game_map.height):
                    cells.append((map_x, map_y))
                    ch = self.game_map.tiles[map_y][map_x]

                    if map_x == self.player_x and map_y == self.player_y:
                        ch = '@'
                        self.mini_window.addch(mini_y + 1, mini_x + 1, ch,
                                               curses.color_pair(1))
                    else:
                        self.mini_window.addch(mini_y + 1, mini_x + 1, ch)
                        try:
                            idx = monsters.index((map_x, map_y))
                            m = self.monsters[idx]
                            self.draw_monster(self.mini_window, m, mini_x + 1, mini_y + 1)
                        except ValueError:
                            pass
                        try:
                            idx = items.index((map_x, map_y))
                            item = self.items[idx]
                            self.draw_item(self.mini_window, item, mini_x + 1, mini_y + 1)
                        except ValueError:
                            pass
        self.mini_window.noutrefresh()

    def go_tride(self):
        self.tride = not self.tride

    def update(self, player_coords, monsters=None, items=None):
        self.player_x, self.player_y = player_coords
        self.monsters = monsters
        self.items = items

        self.game_map.update_visibility(self.player_x, self.player_y)

        if not self.tride:
            self.render()
            self.mini_window.clear()
            self.mini_window.noutrefresh()
        else:
            self.draw_mini_window()
            self.render_d()
