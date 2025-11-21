import random
from typing import List, Tuple


# ================================================================
# DATA CLASSES
# ================================================================

class Room:
    """
    Прямоугольная комната со стартовыми и конечными координатами.
    """

    def __init__(self, id: int, x1: int, y1: int, x2: int, y2: int):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def center(self) -> Tuple[int, int]:
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def intersects(self, other: "Room") -> bool:
        """Проверяет, пересекается ли эта комната с другой."""
        return not (
                self.x2 < other.x1 or
                self.x1 > other.x2 or
                self.y2 < other.y1 or
                self.y1 > other.y2
        )


class Level:
    """
    Итоговая структура уровня (результат работы MapGenerator).
    """

    def __init__(self, width, height, tiles, rooms, start_room, exit_room):
        self.width = width
        self.height = height
        self.tiles = tiles  # 2D массив с символами карты
        self.rooms = rooms
        self.start_room = start_room
        self.exit_room = exit_room

    def is_walkable(self, x, y):
        return self.tiles[y][x] in (".", ",")


# ================================================================
# MAP GENERATOR
# ================================================================

class MapGenerator:
    """
    Генератор уровня:
    - Делит карту на 3×3 секции
    - В каждой секции генерирует случайную комнату
    - Соединяет комнаты коридорами
    - Проверяет связность
    - Создаёт итоговый 2D tilemap
    """

    def __init__(self, width=80, height=25, seed=None):
        self.width = width
        self.height = height
        self.seed = seed
        self.room_id = 0

        if seed is not None:
            random.seed(seed)

        # размеры секций
        self.sec_w = width // 3
        self.sec_h = height // 3

    # ---------------------------
    # PUBLIC API
    # ---------------------------

    def generate_level(self) -> Level:
        while True:
            rooms = self._generate_rooms()
            corridors = self._connect_rooms(rooms)

            if self._check_connected(rooms, corridors):
                break

        tiles = self._create_tilemap(rooms, corridors)

        start_room = random.choice(rooms)
        exit_room = random.choice([r for r in rooms if r != start_room])

        return Level(
            width=self.width,
            height=self.height,
            tiles=tiles,
            rooms=rooms,
            start_room=start_room,
            exit_room=exit_room,
        )

    # ---------------------------
    # ROOM GENERATION
    # ---------------------------

    def _generate_rooms(self) -> List[Room]:
        rooms = []
        for sy in range(3):
            for sx in range(3):
                room = self._generate_room_in_section(sx, sy)
                rooms.append(room)
        return rooms

    def _generate_room_in_section(self, sx: int, sy: int) -> Room:
        x_start = sx * self.sec_w
        y_start = sy * self.sec_h

        min_w, min_h = 5, 4

        w = random.randint(min_w, self.sec_w - 2)
        h = random.randint(min_h, self.sec_h - 2)

        x1 = x_start + random.randint(1, self.sec_w - w - 1)
        y1 = y_start + random.randint(1, self.sec_h - h - 1)
        x2 = x1 + w
        y2 = y1 + h

        self.room_id += 1
        return Room(self.room_id, x1, y1, x2, y2)

    # ---------------------------
    # CORRIDORS
    # ---------------------------

    def _connect_rooms(self, rooms: List[Room]) -> List[List[Tuple[int, int]]]:
        """Соединяет комнаты коридорами по их центрам."""
        corridors = []

        # сортировка по X для стабильности структуры
        rooms_sorted = sorted(rooms, key=lambda r: r.center()[0])

        for i in range(len(rooms_sorted) - 1):
            r1 = rooms_sorted[i]
            r2 = rooms_sorted[i + 1]
            corridors.append(self._create_corridor(r1.center(), r2.center()))

        return corridors

    def _create_corridor(self, c1, c2) -> List[Tuple[int, int]]:
        """
        Возвращает список координат клеток коридора.
        """
        path = []

        x1, y1 = c1
        x2, y2 = c2

        if random.random() < 0.5:
            path.extend(self._dig_horiz(x1, x2, y1))
            path.extend(self._dig_vert(y1, y2, x2))
        else:
            path.extend(self._dig_vert(y1, y2, x1))
            path.extend(self._dig_horiz(x1, x2, y2))

        return path

    def _dig_horiz(self, x1, x2, y):
        path = []
        if x2 < x1:
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            path.append((x, y))
        return path

    def _dig_vert(self, y1, y2, x):
        path = []
        if y2 < y1:
            y1, y2 = y2, y1
        for y in range(y1, y2 + 1):
            path.append((x, y))
        return path

    def _check_connected(self, rooms, corridors) -> bool:
        """Проверяет связность графа комнат по коридорам."""

        # построение графа
        graph = {room.id: set() for room in rooms}

        # проверка пересечения центров с коридорами
        for cpath in corridors:
            pts = set(cpath)
            for r1 in rooms:
                for r2 in rooms:
                    if r1.id != r2.id:
                        if r1.center() in pts and r2.center() in pts:
                            graph[r1.id].add(r2.id)
                            graph[r2.id].add(r1.id)

        # BFS для проверки связности
        start_id = rooms[0].id
        visited = set([start_id])
        queue = [start_id]

        while queue:
            r = queue.pop()
            for nei in graph[r]:
                if nei not in visited:
                    visited.add(nei)
                    queue.append(nei)

        return len(visited) == len(rooms)

    def _create_tilemap(self, rooms, corridors):
        tiles = [[" " for _ in range(self.width)] for _ in range(self.height)]

        for room in rooms:
            for y in range(room.y1, room.y2 + 1):
                for x in range(room.x1, room.x2 + 1):
                    tiles[y][x] = "."

        for cpath in corridors:
            for (x, y) in cpath:
                if 0 <= x < self.width and 0 <= y < self.height:
                    tiles[y][x] = ","

        return tiles
