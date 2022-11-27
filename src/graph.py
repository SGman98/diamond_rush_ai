from typing import Dict, List, Tuple

from utils import UP, DOWN, LEFT, RIGHT, a_star

MEMO: Dict[str, str] = {}


class Cell:
    def __init__(self, x: int, y: int, rows: int, cols: int):
        self.x = x
        self.y = y

        # For A* search
        self.closed = False
        self.total_rows = rows
        self.total_cols = cols

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

    def update_state(self, player: "Player"):
        cell = self.get_cell(player.pos)
        if cell is None:
            return
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
        diamonds: int = -1,
        depth: int = 0,
        max_path_length: int = 1000,
        logging: bool = True,
        optimal: bool = False,
        interest_points: List[Tuple[int, int]] = [],
        rocks: Dict[Tuple[int, int], Tuple[int, int]] = {},
        rock_interest_points: List[Tuple[int, int]] = [],
        rock_movement_memo: Dict[str, str] = {},
        doors: List[Tuple[int, int]] = [],
    ):
        self.board = Board(board, depth == 0)
        self.player = Player(
            start,
            has_key,
            self.board.get_total_diamonds() if diamonds == -1 else diamonds,
        )
        self.end = end
        self.depth = depth
        self.max_path_length = max_path_length
        self.movement = ""
        self.logging = logging
        self.optimal = optimal

        if (
            interest_points == []
            or rocks == {}
            or rock_interest_points == []
            or doors == []
        ):
            result = self.get_all_interest_points()
            if interest_points == []:
                interest_points = result[0]
            if rocks == {}:
                rocks = result[1]
            if rock_interest_points == []:
                rock_interest_points = result[2]
            if doors == []:
                doors = result[3]

        self.interest_points = interest_points
        self.rocks = rocks
        self.rock_interest_points = rock_interest_points
        self.doors = doors

        self.rock_movement_memo = rock_movement_memo

    def __repr__(self):
        return str(self.board) + str(self.player)

    def print(self, message: str = "", type: str = "default"):
        if not self.logging:
            return

        colors = {
            "info": "\033[94m",
            "error": "\033[91m",
            "success": "\033[92m",
            "warning": "\033[93m",
            "default": "\033[0m",
        }

        print("> " * self.depth + colors[type] + message + "\033[0m")

    def move(self, path: str):
        self.movement = path

        for direction in self.movement:
            self.player.move(direction)
            self.board.update_state(self.player)

        cell = self.board.get_cell(self.player.pos)
        if cell is None:
            return

        if cell.isrock:
            if self.movement[-1] == UP:
                target = (cell.x - 1, cell.y)
            elif self.movement[-1] == DOWN:
                target = (cell.x + 1, cell.y)
            elif self.movement[-1] == LEFT:
                target = (cell.x, cell.y - 1)
            elif self.movement[-1] == RIGHT:
                target = (cell.x, cell.y + 1)
            else:
                target = (-1, -1)

            target_cell = self.board.get_cell(target)
            if target_cell is None:
                return

            if not (
                (target_cell.x, target_cell.y) in self.rock_interest_points
                or target_cell.ispath
                or target_cell.islava
            ):
                print(f"Target {target} is not in rock interest points")
                return

            cell.isrock = False
            if not cell.isspike:
                cell.make_path()
            # else:
            #     print("Rock is on spike")
            original_pos = self.rocks.pop((cell.x, cell.y))

            rock_movement = str(
                (
                    (cell.x, cell.y),
                    self.movement[-1],
                    original_pos,
                )
            )

            if rock_movement in self.rock_movement_memo:
                self.print("Rock movement is in memo", "error")
                return False

            if target_cell.ishole:
                self.print(f"Filled hole at {target_cell}", "info")
                target_cell.make_path()
                target_cell.ishole = False
                self.rock_interest_points.remove((target_cell.x, target_cell.y))
                self.rock_movement_memo[rock_movement] = "FILL"
            elif target_cell.islava:
                self.print(f"Rock fell into lava at {target_cell}", "info")
                self.rock_movement_memo[rock_movement] = "FALL"
                pass
            elif target_cell.isbutton:
                self.print(f"Rock pressed button at {target_cell}", "info")
                target_cell.make_wall()
            elif target_cell.ispath:
                self.print(f"Rock moved to {target_cell}", "info")
                target_cell.make_rock()
                self.rocks[(target_cell.x, target_cell.y)] = original_pos
                self.rock_movement_memo[rock_movement] = "MOVE"
            else:
                self.print(f"Rock ??? at {target_cell}")

            cell.update_neighbors(self.board.grid)
            target_cell.update_neighbors(self.board.grid)

            return target_cell

    def get_all_interest_points(self):
        interest_points: List[Tuple[int, int]] = []
        rocks: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        rock_interest_points: List[Tuple[int, int]] = []
        doors: List[Tuple[int, int]] = []

        for i, row in enumerate(self.board.grid):
            for j, cell in enumerate(row):
                if cell.isdiamond or cell.iskey or cell.isexit or cell.isgate:
                    interest_points.append((i, j))
                if cell.isrock:
                    rocks[(i, j)] = (i, j)
                if cell.ishole:
                    rock_interest_points.append((i, j))
                if cell.isdoor:
                    doors.append((i, j))

        return interest_points, rocks, rock_interest_points, doors

    def get_interest_points(self):
        interest_points: List[str] = []

        for x, y in self.interest_points:
            path = self.board.get_path(self.player, (x, y))
            cell = self.board.get_cell((x, y))

            if path is None or path == "" or cell is None:
                continue

            is_exit = self.player.diamonds == 0 and cell.isexit
            is_key = not self.player.has_key and cell.iskey
            is_gate = self.player.has_key and cell.isgate
            is_diamond = cell.isdiamond

            if is_exit or is_key or is_gate or is_diamond:
                interest_points.append(path)

        for x, y in self.rocks.keys():
            rock = self.board.get_cell((x, y))
            if rock is None:
                continue

            for neighbor in rock.neighbors:
                post_move = ""
                if rock.x + 1 == neighbor.x:
                    opposite_pos = (rock.x - 1, rock.y)
                    post_move = UP
                elif rock.x - 1 == neighbor.x:
                    opposite_pos = (rock.x + 1, rock.y)
                    post_move = DOWN
                elif rock.y + 1 == neighbor.y:
                    opposite_pos = (rock.x, rock.y - 1)
                    post_move = LEFT
                elif rock.y - 1 == neighbor.y:
                    opposite_pos = (rock.x, rock.y + 1)
                    post_move = RIGHT
                else:
                    opposite_pos = (-1, -1)

                opposite_cell = self.board.get_cell(opposite_pos)
                if opposite_cell is not None and (
                    opposite_cell.ispath or opposite_cell.ishole or opposite_cell.islava
                ):
                    path = self.board.get_path(self.player, (neighbor.x, neighbor.y))
                    if path is None:
                        continue
                    path += post_move
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

    def solve(self, path=""):
        res = None
        if path != "":
            res = self.move(path)
            if res == False:
                return False
            self.print(f"Moved to {self.player.pos} with path {self.movement}")
        else:
            self.print(f"Starting at {self.player.pos}")

        if self.player.pos == self.end:
            return True

        self.interest_points = list(
            filter(lambda x: x != self.player.pos, self.interest_points)
        )

        memo_key = str(self)

        if memo_key in MEMO:
            movement = MEMO[memo_key]

            if movement == "":
                self.print("Player failed to reach the end (memo)", "error")
                return False

            self.print(f"Reach end with path {movement} (memo)", "success")
            self.movement += movement
            return True

        result = ""

        doors = [None] if res is None or not res.isbutton else self.doors

        for door in doors:
            if door is not None:
                d = self.board.get_cell(door)
                self.print(f"Opening door at {door}", "info")
                d.make_open_door()

            interest_points = self.get_interest_points()

            self.print(f"Interest points: {interest_points}", "success")
            self.print(f"Rocks: {self.rocks}", "success")

            for path in interest_points:

                new_node = Node(
                    self.board.copy(),
                    self.player.pos,
                    self.end,
                    self.player.has_key,
                    self.player.diamonds,
                    self.depth + 1,
                    self.max_path_length - len(path),
                    self.logging,
                    self.optimal,
                    self.interest_points.copy(),
                    self.rocks.copy(),
                    self.rock_interest_points.copy(),
                    self.rock_movement_memo.copy(),
                    self.doors.copy(),
                )

                if new_node.solve(path):
                    if len(result) == 0 or len(new_node.movement) < len(result):
                        result = new_node.movement
                        self.max_path_length = min(self.max_path_length, len(result))
                        new_node.print(f"Exit found with path {result}", "success")
                        if not self.optimal:
                            break
                    else:
                        new_node.print(
                            f"Exit found with path {result} (not optimal)", "warning"
                        )

            if door is not None:
                d = self.board.get_cell(door)
                self.print(f"Closing door at {door}", "info")
                d.make_closed_door()

        MEMO[memo_key] = result

        if result != "":
            self.movement += result
            return True

        self.print("Player failed to reach the end", "error")
        return False
