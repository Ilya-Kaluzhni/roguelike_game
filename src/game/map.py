class GameMap:
    def __init__(self):
        self.width = 80
        self.height = 25
        self.max_vision_distance = 6
        self.tiles = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.visible = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.explored = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []
        self.corridors = []
        # ДОБАВЛЕНО
        self.items_on_map = {}  # координата → Item

    def take_item_at(self, x, y):
        """
        Возвращает предмет с клетки (если есть) и удаляет его с карты.
        """
        if (x, y) in self.items_on_map:
            item = self.items_on_map[(x, y)]
            del self.items_on_map[(x, y)]
            return item

        return None

    #
    def add_rooms(self, rooms):
        for room_id, room_data in enumerate(rooms):
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
            self.rooms.append({'x': x, 'y': y, 'width': w, 'height': h, 'cells': room_cells, 'id': room_id})

    def add_corridors(self, corridors):
        for seg in corridors:
            if isinstance(seg, dict):
                x, y, w, h = seg['x'], seg['y'], seg['width'], seg['height']
            else:
                x, y, w, h = seg
            connected_rooms = set()
            for row in range(y, y + h):
                for col in range(x, x + w):
                    if 0 <= row < self.height and 0 <= col < self.width:
                        neighbors = [
                            (row - 1, col),
                            (row + 1, col),
                            (row, col - 1),
                            (row, col + 1),
                        ]
                        for ny, nx in neighbors:
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                if self.tiles[ny][nx] == '#':
                                    room_id = self.find_room_id(nx, ny)
                                    if room_id:
                                        connected_rooms.add(room_id)
                                    self.tiles[ny][nx] = '.'
                        self.tiles[row][col] = '+'
            self.corridors.append({'x': x, 'y': y, 'width': w, 'height': h, 'connected_rooms': connected_rooms})


    def find_room_id(self, x, y):
        for room in self.rooms:
            if room['x'] <= x < room['x'] + room['width'] and room['y'] <= y < room['y'] + room['height']:
                return room['id']
        return None

    # Ищет путь от a к b
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
        max_dist_sq = max_distance ** 2
        for x1, y1 in room_cells:
            dist_sq = (x1 - source_x) ** 2 + (y1 - source_y) ** 2
            if dist_sq <= max_dist_sq:
                line_points = self.bresenham_line(source_x, source_y, x1, y1)
                blocked = False
                for px, py in line_points:
                    if not (0 <= py < self.height and 0 <= px < self.width):
                        blocked = True
                        break
                    if self.tiles[py][px] == '#':
                        break
                    if self.tiles[py][px] == ' ':
                        blocked = True
                        break
                    visible_cells.add((px, py))
                if not blocked:
                    visible_cells.update(line_points)
        return visible_cells

    def reset_visibility(self):
        for y in range(self.height):
            for x in range(self.width):
                self.visible[y][x] = False

    def find_corridor_id(self, x, y):
        for i, corridor in enumerate(self.corridors):
            if corridor['x'] <= x < corridor['x'] + corridor['width'] and corridor['y'] <= y < corridor['y'] + corridor[
                'height']:
                return i
        return None

    def update_visibility(self, player_x, player_y):
        self.reset_visibility()
        # Текущая комната, делаем видимой, помещаем в исследованные
        player_room_id = self.find_room_id(player_x, player_y)
        if player_room_id is not None:
            for x, y in self.rooms[player_room_id]['cells']:
                self.visible[y][x] = True
                self.explored[y][x] = True
        else:
            corridor_id = self.find_corridor_id(player_x, player_y)

            # Для коридора делаем видимыми клетки самого коридора
            corridor = self.corridors[corridor_id]
            for y in range(corridor['y'], corridor['y'] + corridor['height']):
                for x in range(corridor['x'], corridor['x'] + corridor['width']):
                    self.visible[y][x] = True
                    self.explored[y][x] = True

            # И делаем ray casting для соседних комнат этого коридора
            for room_id in corridor['connected_rooms']:
                room = self.rooms[room_id]
                visible_cells = self.ray_casting_visibility(player_x, player_y, room['cells'], self.max_vision_distance)
                for vx, vy in visible_cells:
                    if 0 <= vy < self.height and 0 <= vx < self.width:
                        self.visible[vy][vx] = True
                        # self.explored[vy][vx] = True

        for room_id, room in enumerate(self.rooms):
            if room_id != player_room_id:
                explored = any(self.explored[y][x] for (x, y) in room['cells'])
                if explored:
                    for x, y in room['cells']:
                        if self.tiles[y][x] == '#':
                            self.visible[y][x] = True

    def get_tile_display(self, x, y):
        if self.visible[y][x]:
            if not self.explored[y][x] and self.tiles[y][x] == '.':
                return ','
            return self.tiles[y][x]
        elif self.explored[y][x] and self.tiles[y][x] in ('#', '+'):
            return self.tiles[y][x]
        return None
        # Если клетка невидима — всё как раньше
        # if not self.visible[y][x]:
        #     if self.explored[y][x] and self.tiles[y][x] in ('#', '+'):
        #         return self.tiles[y][x]
        #     return None

        # ЕСЛИ ВИДИМО — проверяем предмет
        # if (x, y) in self.items_on_map:
        #     item = self.items_on_map[(x, y)]
        #     if item.item_type == "treasure":
        #         return '$'
        #     return '!'

        # иначе возвращаем обычную плитку
        # if not self.explored[y][x] and self.tiles[y][x] == '.':
        #     return ','
        # return self.tiles[y][x]

    def remove_item(self, x, y):
        if (x, y) in self.items_on_map:
            del self.items_on_map[(x, y)]
