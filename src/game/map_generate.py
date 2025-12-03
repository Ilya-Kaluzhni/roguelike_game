# /domain/map_generate/map_generate.py
import random
from typing import List, Dict, Tuple

class MapGenerator:
    """
    Генератор уровня для UI и GameMap.
    """

    def __init__(self, seed=None):
        self.width = 80
        self.height = 25
        self.tiles = []
        self.rooms_ui = []
        self.corridors_ui = []
        self.start_room = 0
        if seed is not None:
            random.seed(seed)

    def is_walkable(self, x, y):
        return self.tiles[y][x] in (".", ",")

    def get_room_size(self, x, y):
        for room in self.rooms_ui:
            room_x, room_y = room['x'], room['y']
            room_width, room_height = room['width'], room['height']

            if (room_x <= x < room_x + room_width and
                    room_y <= y < room_y + room_height):
                return room_x, room_y, room_width, room_height
        return 0

    def set_player_cords(self,):
        cords = self.rooms_ui[self.start_room]
        cord_x = random.randint(cords['x'] + 1, cords['x'] + cords['width'] - 2)
        cord_y = random.randint(cords['y']+ 1 , cords['y'] + cords['height'] - 2)
        return cord_x, cord_y

    def can_set_smth(self, x, y):
        for i, room in enumerate(self.rooms_ui):
            room_x, room_y = room['x'], room['y']
            room_width, room_height = room['width'], room['height']

            inner_x1 = room_x + 1
            inner_y1 = room_y + 1
            inner_x2 = room_x + room_width - 1
            inner_y2 = room_y + room_height - 1

            if inner_x1 <= x < inner_x2 and inner_y1 <= y < inner_y2:
                if i == self.start_room:
                    return False
                return True

        return False

    def _create_tilemap(self, rooms, corridors):
        tiles = [[" " for _ in range(self.width)] for _ in range(self.height)]

        for room in rooms:
            for x in range(room['x'], room['x'] + room['width']):
                for y in range(room['y'], room['y'] + room['height']):
                    if room['y'] < y < room['y'] + room['height'] -1 and room['x'] < x < room['x'] + room['width'] - 1:
                        tiles[y][x] = "."
                    else:
                        tiles[y][x] = "#"

        for (x, y) in corridors:
            if 0 <= x < self.width and 0 <= y < self.height:
                tiles[y][x] = ","
                neighbors = [
                    (y - 1, x),
                    (y + 1, x),
                    (y, x - 1),
                    (y, x + 1),
                ]
                for ny, nx in neighbors:
                    if 0 <= ny < self.height  and 0 <= nx < self.width:
                        try:
                            if tiles[ny][nx] == '#':
                                tiles[ny][nx] = '.'
                        except IndexError:
                            pass

        return tiles

    def generate_level(self):
        rooms_ui = self._generate_rooms()
        corridors_ui = self._generate_corridors(rooms_ui)
        self.start_room = random.randint(0, 8)
        # --- преобразуем в клетки для GameMap ---
        rooms_cells = []
        for r in rooms_ui:
            for y in range(r['y'], r['y'] + r['height']):
                for x in range(r['x'], r['x'] + r['width']):
                    rooms_cells.append((x, y))

        corridors_cells = []
        for c in corridors_ui:
            for y in range(c['y'], c['y'] + c['height']):
                for x in range(c['x'], c['x'] + c['width']):
                    corridors_cells.append((x, y))

        self.tiles = self._create_tilemap(rooms_ui, corridors_cells)
        with open('map.txt', 'w') as f:
            for tile in self.tiles:
                f.write(str(tile) + '\n')
        self.rooms_ui = rooms_ui
        self.corridors_ui = corridors_ui
        return rooms_ui, corridors_ui, rooms_cells, corridors_cells

    def _generate_rooms(self) -> List[Dict]:
        """Создаем 9 комнат в сетке 3x3"""
        room_coords = [
            (5, 3, 8, 6), (20, 3, 10, 6), (35, 3, 9, 6),
            (5, 12, 7, 7), (20, 12, 11, 7), (35, 12, 9, 7),
            (5, 21, 7, 3), (20, 21, 11, 3), (35, 21, 9, 3),
        ]
        rooms = [{'x': x, 'y': y, 'width': w, 'height': h} for x, y, w, h in room_coords]
        return rooms

    def _generate_corridors(self, rooms: List[Dict]) -> List[Dict]:
        corridors = []

        # горизонтальные коридоры
        for row_start in [0, 3, 6]:
            r1, r2, r3 = rooms[row_start:row_start + 3]
            # между 1 и 2
            corridors.append({
                'x': r1['x'] + r1['width'] - 1,
                'y': r1['y'] + r1['height']//2 - 1,
                'width': r2['x'] - (r1['x'] + r1['width'] - 1),
                'height': 2
            })
            # между 2 и 3
            corridors.append({
                'x': r2['x'] + r2['width'] - 1,
                'y': r2['y'] + r2['height']//2 - 1,
                'width': r3['x'] - (r2['x'] + r2['width'] - 1),
                'height': 2
            })

        # вертикальные коридоры
        for col in [0, 1, 2]:
            r_top, r_mid, r_bot = rooms[col], rooms[col+3], rooms[col+6]
            corridors.append({
                'x': r_top['x'] + r_top['width']//2 - 1,
                'y': r_top['y'] + r_top['height'] - 1,
                'width': 3,
                'height': r_mid['y'] - (r_top['y'] + r_top['height'] - 1)
            })
            corridors.append({
                'x': r_mid['x'] + r_mid['width']//2 - 1,
                'y': r_mid['y'] + r_mid['height'] - 1,
                'width': 3,
                'height': r_bot['y'] - (r_mid['y'] + r_mid['height'] - 1)
            })

        return corridors
