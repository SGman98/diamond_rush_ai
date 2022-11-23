from typing import Dict, List, Tuple

from utils import UP, DOWN, LEFT, RIGHT, a_star

LOGGING = True


MEMO: Dict[str, str] = {}
MEMO2: Dict[str, bool] = {}


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

    def get_rocks_movement(self):
        rocks = []
        for neighbor in self.neighbors:
            if neighbor.isrock:
                if neighbor.x < self.x:
                    rocks.append(UP)
                elif neighbor.x > self.x:
                    rocks.append(DOWN)
                elif neighbor.y < self.y:
                    rocks.append(LEFT)
                elif neighbor.y > self.y:
                    rocks.append(RIGHT)
        return rocks

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


class Board:
    def __init__(self, board: list, new=False):

        self.grid: List[List[Cell]] = self.create(board) if new else board

        self.width = len(board[0])
        self.height = len(board)

    def __repr__(self):
        return ".".join([cell.to_string() for row in self.grid for cell in row])

    def get_cell(self, pos: Tuple[int, int]):
        if pos[0] < 0 or pos[0] >= self.height or pos[1] < 0 or pos[1] >= self.width:
            return None
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
        board_copy = [[cell.copy() for cell in row] for row in self.grid]

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

        return a_star(grid, start_cell, end_cell)

    def update_state(self, player: "Player", post_move: str):
        cell = self.get_cell(player.pos)
        if cell.iskey and not player.has_key:
            player.has_key = True
            cell.iskey = False
        if cell.isdiamond:
            player.diamonds -= 1
            cell.isdiamond = False
        if cell.isspike:
            cell.make_wall()
            return
        if cell.isgate and player.has_key:
            cell.make_path()
            cell.isgate = False
            player.has_key = False
            return

        MOVEMENT = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}
        if cell.isrock:
            target = self.get_cell(
                (
                    player.pos[0] + MOVEMENT[post_move][0],
                    player.pos[1] + MOVEMENT[post_move][1],
                )
            )
            cell.isrock = False
            cell.make_path()

            if target.islava:
                pass
            elif target.ishole:
                # fill hole
                target.make_path()
                target.ishole = False
            elif target.ispath:
                # move rock
                target.make_rock()
            else:
                print("WTF!! This should not happen")


class Player:
    def __init__(self, pos: Tuple[int, int], has_key: bool, diamonds: int):
        self.pos = pos
        self.has_key = has_key
        self.diamonds = diamonds

    def __repr__(self):
        return str(self.pos) + str(self.has_key)

    def move(self, movement: str):
        MOVEMENTS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}

        self.pos = (
            self.pos[0] + MOVEMENTS[movement][0],
            self.pos[1] + MOVEMENTS[movement][1],
        )


class Node:
    def __init__(
        self,
        board: List[List[Cell]],
        start: Tuple[int, int],
        end: Tuple[int, int],
        has_key: bool = False,
        depth: int = 0,
        max_path_length: int = 200,
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
        print("> " * self.depth + message)

    def move(self, path: str):
        self.movement = "".join(path)

        for direction in self.movement:
            self.player.move(direction)
            self.board.update_state(self.player, path[1])

    def get_interest_points(self):
        interest_points: List[Tuple[str, str]] = []

        for i, row in enumerate(self.board.grid):
            for j, cell in enumerate(row):
                path = self.board.get_path(self.player, (i, j))

                if path == None:
                    continue

                is_exit = self.player.diamonds == 0 and cell.isexit
                is_key = not self.player.has_key and cell.iskey
                is_gate = self.player.has_key and cell.isgate
                is_diamond = cell.isdiamond

                if is_exit or is_key or is_gate or is_diamond:
                    interest_points.append((path, ""))

                MOVEMENT = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}

                for direction in MOVEMENT:
                    neighbor = self.board.get_cell(
                        (i + MOVEMENT[direction][0], j + MOVEMENT[direction][1])
                    )
                    otherside = self.board.get_cell(
                        (
                            i + MOVEMENT[direction][0] * 2,
                            j + MOVEMENT[direction][1] * 2,
                        )
                    )

                    if (
                        neighbor != None
                        and otherside != None
                        and neighbor.isrock
                        and (otherside.ispath or otherside.ishole or otherside.islava)
                    ):
                        interest_points.append((path, direction))

        interest_points.sort(key=lambda x: len("".join(x)))

        interest_points_final: List[Tuple[str, str]] = []
        for path in interest_points:
            for path2 in interest_points:
                if "".join(path) == "".join(path2):
                    continue

                if "".join(path).startswith("".join(path2)):
                    break
            else:
                interest_points_final.append(path)

        def shorter_than_max(x):
            result = len("".join(x)) <= self.max_path_length
            if not result:
                print("\033[33m" + f"Path {x} is too long" + "\033[0m")
            return result

        return list(filter(shorter_than_max, interest_points_final))

    def solve(self):
        global LOGGING

        if self.player.pos == self.end:
            self.print("\033[32mReached end\033[0m")

            return True

        memo_key = str(self)

        if memo_key in MEMO:
            movement = MEMO[memo_key]

            if movement == "":
                self.print("\033[34mPlayer failed to reach the end (memo)\033[0m")
                return False

            self.print(f"\033[34mReach end with path {movement} (memo)\033[0m")
            self.movement += movement
            return True

        if str(self.board) in MEMO2:
            self.print("\033[35mBoard already exists\033[0m")
            return False

        MEMO2[str(self.board)] = True

        result = ""

        interest_points = self.get_interest_points()

        for path in interest_points:

            complete_path = "".join(path)

            new_node = Node(
                self.board.copy(),
                self.player.pos,
                self.end,
                self.player.has_key,
                self.depth + 1,
                self.max_path_length - len(complete_path),
            )

            new_node.move(path)
            for row in new_node.board.grid:
                for cell in row:
                    cell.update_neighbors(new_node.board.grid)

            new_node.print(f"Moved to {new_node.player.pos} with path {complete_path}")

            if new_node.solve():
                if len(result) == 0 or len(new_node.movement) < len(result):
                    result = new_node.movement
                    self.max_path_length = min(self.max_path_length, len(result))
                    self.print(f"\033[92mNew best path: {result}\033[0m")
                    break  # comment this line to find the optimal path
                else:
                    self.print(f"Same or worse path: {new_node.movement}")

        MEMO[memo_key] = result

        if result != "":
            self.movement += result
            if self.depth == 0:
                print(f"Final path: {self.movement}")
            return True

        if self.depth == 0:
            print(f"\033[91mPlayer failed to reach the end\033[0m")
        else:
            self.print(f"\033[91mPlayer failed to reach the end\033[0m")
        return False
