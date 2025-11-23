import curses

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[' ' for _ in range(width)] for _ in range(height)]
        self.visible = [[False for _ in range(width)] for _ in range(height)]
        self.explored = [[False for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.corridors = []

    #
    def add_rooms(self, rooms):
        for room_data in rooms:
            x, y, w, h = room_data['x'], room_data['y'], room_data['width'], room_data['height']
            room_cells = []
            for row in range(y, y + h):
                for col in range(x, x + w):
                    if 0 <= row < self.height and 0 <= col < self.width:
                        room_cells.append((col, row))
                        if row == y or row == y + h - 1 or col == x or col == x + w - 1:
                            self.tiles[row][col] = '#'
                        else:
                            self.tiles[row][col] = '.'
            self.rooms.append({'x': x, 'y': y, 'width': w, 'height': h, 'cells': room_cells})

    def add_corridors(self, corridors):
        for seg in corridors:
            if isinstance(seg, dict):
                x, y, w, h = seg['x'], seg['y'], seg['width'], seg['height']
            else:
                x, y, w, h = seg
            for row in range(y, y + h):
                for col in range(x, x + w):
                    if 0 <= row < self.height and 0 <= col < self.width:
                        self.tiles[row][col] = '+'
            for row in range(y - 1, y + h + 1):
                for col in range(x - 1, x + w + 1):
                    if 0 <= row < self.height and 0 <= col < self.width:
                        # Пропускаем, если здесь уже коридор или комната
                        if self.tiles[row][col] in ('+', '.', '#'):
                            continue
                        self.tiles[row][col] = '*'


    def reset_visibility(self):
        for y in range(self.height):
            for x in range(self.width):
                if not self.tiles[y][x] == '+':
                    self.visible[y][x] = False

    @staticmethod
    def bresenham_line(x0, y0, x1, y1):
        points = []
        # разности координат
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # направления
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        # смещение
        d = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            d2 = 2 * d
            if d2 > -dy:
                d -= dy
                x0 += sx
            if d2 < dx:
                d += dx
                y0 += sy
        return points

    def ray_casting_visibility(self, source_x, source_y, room_cells, max_distance):
        visible_cells = set()
        for cell in room_cells:
            x1, y1 = cell
            line_points = self.bresenham_line(source_x, source_y, x1, y1)
            if len(line_points) < max_distance:
                blocked = False
                for px, py in line_points:
                    # Добавить край коридора
                    if not (0 <= py < self.height and 0 <= px < self.width):
                        blocked = True
                        break
                    if self.tiles[py][px] == '#':
                        # blocked = True
                        break
                    if self.tiles[py][px] == '*':
                        blocked = True
                        break
                    visible_cells.add((px, py))
                if not blocked:
                    visible_cells.update(line_points)
        return visible_cells

    def update_visibility(self, player_x, player_y, max_vision_distance=10):
        self.reset_visibility()

        # Коридоры в радиусе видимости
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] == '+':
                    dist = (x - player_x) ** 2 + (y - player_y) ** 2
                    if dist <= max_vision_distance ** 2:
                        self.visible[y][x] = True

        # Найти соседние комнаты рядом с игроком (расстояние <= 1)
        visible_rooms = []
        for room in self.rooms:
            for cx, cy in room['cells']:
                if abs(cx - player_x) <= 1 and abs(cy - player_y) <= 1:
                    visible_rooms.append(room)
                    break

        # Ray Casting на каждую соседнюю комнату
        for room in visible_rooms:
            visible_cells = self.ray_casting_visibility(player_x, player_y, room['cells'], max_vision_distance)
            for vx, vy in visible_cells:
                if 0 <= vy < self.height and 0 <= vx < self.width:
                    self.visible[vy][vx] = True
                    # self.explored[vy][vx] = True

        for y in range(self.height):
            for x in range(self.width):
                if self.visible[y][x]:
                    self.explored[y][x] = True

    def get_tile_display(self, x, y, player_x, player_y):
        if self.visible[y][x]:
            if self.tiles[y][x] == '#':
                return '#'
            for room in self.rooms:
                if (x, y) in room['cells'] and room['x'] <= player_x < room['x'] + room['width'] and room[
                    'y'] <= player_y < room['y'] + room['height']:
                    return self.tiles[y][x]
            if self.tiles[y][x] == '.':
                return ' '
            return self.tiles[y][x]
        elif self.explored[y][x]:
            if self.tiles[y][x] == '.':
                return ','
            return self.tiles[y][x]
        else:
            return ' '


class RenderingActors:
    def __init__(self, stdscr, game_map, player_coords, monsters=None, items=None):
        self.stdscr = stdscr
        self.game_map = game_map
        self.player_x, self.player_y = player_coords
        self.monsters = monsters or []
        self.items = items or []

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Игрок
        curses.init_pair(2, curses.COLOR_WHITE, -1)  # Стены, пол
        curses.init_pair(3, curses.COLOR_RED, -1)    # Монстры
        curses.init_pair(4, curses.COLOR_YELLOW, -1) # Предметы

    def draw_map(self):
        screen_height, screen_width = self.stdscr.getmaxyx()
        start_y = max(0, (screen_height - 40) // 2)
        start_x = max(0, (screen_width - 80) // 2)
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                ch = self.game_map.get_tile_display(x, y, self.player_x, self.player_y)
                if ch in ('#', '.', '+'):
                    color = curses.color_pair(0)
                elif ch == ',':
                    color = curses.color_pair(2) | curses.A_DIM
                else:
                    color = curses.color_pair(0)
                try:
                    self.stdscr.addch(y + start_y , x + start_x, ch, color)
                except curses.error:
                    self.stdscr.addch(y, x, '#', color)
                # self.stdscr.addch(y, x, ch, color)

    def draw_actors(self):
        screen_height, screen_width = self.stdscr.getmaxyx()
        start_y = max(0, (screen_height - 40) // 2)
        start_x = max(0, (screen_width - 80) // 2)
        for item in self.items:
            if self.game_map.visible[item.y][item.x]:
                self.stdscr.addch(item.y, item.x, item.char, curses.color_pair(4))
        for monster in self.monsters:
            if self.game_map.visible[monster.y][monster.x]:
                self.stdscr.addch(monster.y, monster.x, monster.char, curses.color_pair(3))
        self.stdscr.addch(self.player_y + start_y, self.player_x + start_x, '@', curses.color_pair(1) | curses.A_BOLD)

    def render(self):
        self.stdscr.clear()
        self.draw_map()
        self.draw_actors()
        self.stdscr.refresh()

    def update(self, player_coords, monsters=None, items=None):
        self.player_x, self.player_y = player_coords
        self.monsters = monsters or []
        self.items = items or []
        self.game_map.update_visibility(self.player_x, self.player_y)
        self.render()

def main(stdscr):
    curses.curs_set(0)  # Скрыть курсор
    width, height = 80, 40

    game_map = GameMap(width, height)

    rooms = [
        {'x': 5, 'y': 3, 'width': 8, 'height': 6},
        {'x': 20, 'y': 3, 'width': 10, 'height': 6},
        {'x': 35, 'y': 3, 'width': 9, 'height': 6},

        {'x': 5, 'y': 12, 'width': 7, 'height': 7},
        {'x': 20, 'y': 12, 'width': 11, 'height': 7},
        {'x': 35, 'y': 12, 'width': 9, 'height': 7},

        {'x': 5, 'y': 22, 'width': 8, 'height': 6},
        {'x': 20, 'y': 22, 'width': 10, 'height': 6},
        {'x': 35, 'y': 22, 'width': 9, 'height': 6},
    ]

    corridors = [
        {'x': 13, 'y': 6, 'width': 7, 'height': 2},
        {'x': 30, 'y': 6, 'width': 5, 'height': 2},

        {'x': 12, 'y': 15, 'width': 8, 'height': 2},
        {'x': 31, 'y': 15, 'width': 5, 'height': 2},

        {'x': 13, 'y': 25, 'width': 7, 'height': 2},
        {'x': 30, 'y': 25, 'width': 5, 'height': 2},

        {'x': 9, 'y': 9, 'width': 3, 'height': 6},
        {'x': 24, 'y': 9, 'width': 3, 'height': 6},
        {'x': 40, 'y': 9, 'width': 3, 'height': 6},
    ]

    game_map.add_rooms(rooms)
    game_map.add_corridors(corridors)

    player_pos = (12, 8)
    monsters = []
    items = []

    renderer = RenderingActors(stdscr, game_map, player_pos, monsters, items)

    while True:
        renderer.update(player_pos)
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            player_pos = (player_pos[0], max(0, player_pos[1] - 1))
        elif key == curses.KEY_DOWN:
            player_pos = (player_pos[0], min(height - 1, player_pos[1] + 1))
        elif key == curses.KEY_LEFT:
            player_pos = (max(0, player_pos[0] - 1), player_pos[1])
        elif key == curses.KEY_RIGHT:
            player_pos = (min(width - 1, player_pos[0] + 1), player_pos[1])

if __name__ == "__main__":
    curses.wrapper(main)
