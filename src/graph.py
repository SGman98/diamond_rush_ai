from queue import PriorityQueue
from typing import Dict, List, Tuple

LOGGING = True

MEMO: Dict[str, str] = {}


class Cell:
    def __init__(self, x: int, y: int, rows: int, cols: int):
        self.x = x
        self.y = y

        self.closed = False

        # collectable items
        self.isdiamond = False
        self.iskey = False

        # doors and gates
        self.isdoor = False
        self.isgate = False

        # interactive cells
        self.isbutton = False
        self.isspike = False
        self.isrock = False

        # other
        self.ishole = False
        self.islava = False

        self.ispath = False  # whether the cell is a path or wall

        self.isexit = False

        self.total_rows = rows
        self.total_cols = cols

        self.neighbors: List[Cell] = []

    def get_pos(self):
        return self.x, self.y

    def make_closed(self):
        self.closed = True

    def make_open(self):
        self.closed = False

    def make_wall(self):
        self.ispath = False

    def make_path(self):
        self.ispath = True

    def make_diamond(self):
        self.make_path()
        self.isdiamond = True

    def make_closed_door(self):
        self.make_wall()
        self.isdoor = True

    def make_open_door(self):
        self.make_path()
        self.isdoor = True

    def make_hole(self):
        self.make_wall()
        self.ishole = True

    def make_filled_hole(self):
        self.make_path()
        self.ishole = False

    def make_key(self):
        self.make_path()
        self.iskey = True

    def make_lava(self):
        self.make_wall()
        self.islava = True

    def make_closed_gate(self):
        self.make_wall()
        self.isgate = True

    def make_open_gate(self):
        self.make_path()
        self.isgate = True

    def make_button(self):
        self.make_path()
        self.isbutton = True

    def make_spike(self):
        self.make_path()
        self.isspike = True

    def make_closed_spike(self):
        self.make_wall()
        self.isspike = True

    def make_rock(self):
        self.make_wall()
        self.isrock = True

    def make_exit(self):
        self.make_wall()
        self.isexit = True

    def make_state(self, value):
        transform = {
            "W": self.make_wall,
            "P": self.make_path,
            "D": self.make_diamond,
            "C": self.make_closed_door,
            "O": self.make_open_door,
            "H": self.make_hole,
            "K": self.make_key,
            "L": self.make_lava,
            "G": self.make_closed_gate,
            "B": self.make_button,
            "S": self.make_spike,
            "R": self.make_rock,
            "E": self.make_exit,
            "#": self.make_path,
        }

        if value in transform:
            transform[value]()
        else:
            print(f"Using default state for {value}")
            self.make_path()

    def is_blocked(self):
        return not self.ispath

    def update_neighbors(self, grid: List[List["Cell"]]):
        self.neighbors = []

        if self.x < self.total_rows - 1:
            if not grid[self.x + 1][self.y].is_blocked():
                self.neighbors.append(grid[self.x + 1][self.y])

        if self.x > 0:
            if not grid[self.x - 1][self.y].is_blocked():
                self.neighbors.append(grid[self.x - 1][self.y])

        if self.y < self.total_cols - 1:
            if not grid[self.x][self.y + 1].is_blocked():
                self.neighbors.append(grid[self.x][self.y + 1])

        if self.y > 0:
            if not grid[self.x][self.y - 1].is_blocked():
                self.neighbors.append(grid[self.x][self.y - 1])

    def to_string(self):
        str = ""
        str += "1" if self.ispath else "0"
        str += "1" if self.isdiamond else "0"
        str += "1" if self.iskey else "0"
        str += "1" if self.isdoor else "0"
        str += "1" if self.isgate else "0"
        str += "1" if self.isbutton else "0"
        str += "1" if self.isspike else "0"
        str += "1" if self.isrock else "0"
        str += "1" if self.ishole else "0"
        str += "1" if self.islava else "0"
        str += "1" if self.isexit else "0"

        return str

    def copy(self):
        cell = Cell(self.x, self.y, self.total_rows, self.total_cols)
        cell.closed = self.closed
        cell.isdiamond = self.isdiamond
        cell.iskey = self.iskey
        cell.isdoor = self.isdoor
        cell.isgate = self.isgate
        cell.isbutton = self.isbutton
        cell.isspike = self.isspike
        cell.isrock = self.isrock
        cell.ishole = self.ishole
        cell.islava = self.islava
        cell.ispath = self.ispath
        cell.isexit = self.isexit
        return cell

    def __lt__(self, _):
        return False

    # printable representation of the object
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


def path_to_movement(path: List[Cell]):
    movement = ""
    if len(path) == 0:
        return movement
    for i in range(len(path) - 1):
        x1, y1 = path[i].get_pos()
        x2, y2 = path[i + 1].get_pos()

        if x1 < x2:
            movement += "s"
        elif x1 > x2:
            movement += "w"
        elif y1 < y2:
            movement += "d"
        elif y1 > y2:
            movement += "a"

    return movement


class Board:
    def __init__(self, board: list, new=False):

        self.grid: List[List[Cell]] = self.create(board) if new else board

        self.width = len(board[0])
        self.height = len(board)

    def __repr__(self):
        return ".".join([cell.to_string() for row in self.grid for cell in row])

    def get_cell(self, pos: Tuple[int, int]):
        return self.grid[pos[0]][pos[1]]

    def get_total_diamonds(self):
        return sum([cell.isdiamond for row in self.grid for cell in row])

    def create(self, board: list):
        grid: List[List[Cell]] = []

        for i, row in enumerate(board):
            grid.append([])

            for j, cell in enumerate(row):
                state = cell
                cell = Cell(i, j, len(board), len(row))

                cell.make_state(state)

                grid[i].append(cell)

        for row in grid:
            for cell in row:
                cell.update_neighbors(grid)

        return grid

    def copy(self):
        board_copy: List[List[Cell]] = []

        for i, row in enumerate(self.grid):
            board_copy.append([])

            for j, cell in enumerate(row):
                board_copy[i].append(cell.copy())

        for row in board_copy:
            for cell in row:
                cell.update_neighbors(board_copy)

        return board_copy

    def get_path(self, player: "Player", end: Tuple[int, int]):
        grid = self.copy()
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell.isgate and player.has_key and end == (i, j):
                    cell.make_path()
                if cell.isexit and player.diamonds == 0 and end == (i, j):
                    cell.make_path()

        for row in grid:
            for cell in row:
                cell.update_neighbors(grid)

        start_cell = grid[player.pos[0]][player.pos[1]]
        end_cell = grid[end[0]][end[1]]

        path = self.a_star(grid, start_cell, end_cell)

        return path_to_movement(path)

    def update_state(self, player):
        cell = self.get_cell(player.pos)
        if cell.iskey and not player.has_key:
            player.has_key = True
            cell.iskey = False
            return
        if cell.isdiamond:
            player.diamonds -= 1
            cell.isdiamond = False
            return
        if cell.isspike:
            cell.make_wall()
            return
        if cell.isgate and player.has_key:
            cell.make_path()
            cell.isgate = False
            player.has_key = False
            return

    def a_star(self, grid: List[List[Cell]], start: Cell, end: Cell):
        # Manhattan distance
        def h(p1: Tuple[int, int], p2: Tuple[int, int]):
            x1, y1 = p1
            x2, y2 = p2

            return abs(x1 - x2) + abs(y1 - y2)

        count = 0

        open_set: PriorityQueue = PriorityQueue()
        open_set.put((0, count, start))

        came_from: Dict[Cell, Cell] = {}

        g_score = {cell: float("inf") for row in grid for cell in row}
        g_score[start] = 0

        f_score = {cell: float("inf") for row in grid for cell in row}
        f_score[start] = h(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            current: Cell = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                path: List[Cell] = []

                while current in came_from:
                    path.append(current)
                    current = came_from[current]

                path.append(start)

                return path[::-1]

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(
                        neighbor.get_pos(), end.get_pos()
                    )

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            if current != start:
                current.make_closed()

        return []


class Player:
    def __init__(self, pos: Tuple[int, int], has_key: bool, diamonds: int):
        self.pos = pos
        self.has_key = has_key
        self.diamonds = diamonds

    def __repr__(self):
        return str(self.pos) + str(self.has_key)

    def move(self, movement: str):
        if movement == "w":
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif movement == "a":
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif movement == "s":
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif movement == "d":
            self.pos = (self.pos[0], self.pos[1] + 1)


class Node:
    def __init__(
        self,
        board: List[List[Cell]],
        start: Tuple[int, int],
        end: Tuple[int, int],
        has_key: bool = False,
        depth: int = 0,
        max_path_length: int = 1000,
    ):
        self.board = Board(board, depth == 0)
        self.player = Player(start, has_key, self.board.get_total_diamonds())
        self.end = end
        self.depth = depth
        self.max_path_length = max_path_length
        self.movement = ""

    def __repr__(self):
        return str(self.board) + str(self.player)

    def print(self, message: str = ""):
        global LOGGING
        if not LOGGING:
            return
        print(">\t" * self.depth + message)

    def move(self, path: str):
        self.movement = path

        for direction in self.movement:
            self.player.move(direction)
            self.board.update_state(self.player)

    def get_interest_points(self):
        interest_points: List[str] = []

        for i, row in enumerate(self.board.grid):
            for j, cell in enumerate(row):
                path = self.board.get_path(self.player, (i, j))

                if path == "":
                    continue

                is_exit = self.player.diamonds == 0 and cell.isexit
                is_key = not self.player.has_key and cell.iskey
                is_gate = self.player.has_key and cell.isgate
                is_diamond = cell.isdiamond

                if is_exit or is_key or is_gate or is_diamond:
                    interest_points.append(path)

        interest_points.sort(key=lambda x: len(x))

        interest_points_final: List[str] = []
        for path in interest_points:
            for path2 in interest_points:
                if path == path2:
                    continue

                if path.startswith(path2):
                    break
            else:
                interest_points_final.append(path)

        def shorter_than_max(x):
            return len(x) <= self.max_path_length

        return list(filter(shorter_than_max, interest_points_final))

    def solve(self):
        global LOGGING

        if self.player.pos == self.end:
            self.print("Reached end")
            return True

        memo_key = str(self)

        if memo_key in MEMO:
            movement = MEMO[memo_key]

            if movement == "":
                self.print("Player failed to reach the end (memo)")
                return False

            self.print(f"Reach end with path {movement} (memo)")
            self.movement += movement
            return True

        result = ""

        interest_points = self.get_interest_points()

        for path in interest_points:

            new_node = Node(
                self.board.copy(),
                self.player.pos,
                self.end,
                self.player.has_key,
                self.depth + 1,
                self.max_path_length - len(path),
            )

            new_node.move(path)
            new_node.print(f"Moved to {new_node.player.pos} with path {path}")

            if new_node.solve():
                if len(result) == 0 or len(new_node.movement) < len(result):
                    result = new_node.movement
                    self.max_path_length = min(self.max_path_length, len(result))
                    self.print(f"New best path: {result}")
                    break  # comment this line to find the optimal path
                else:
                    self.print(f"Same or worse path: {new_node.movement}")

        MEMO[memo_key] = result

        if result != "":
            self.movement += result
            if self.depth == 0:
                print(f"Final path: {self.movement}")
            return True

        self.print("Player failed to reach the end")
        return False
