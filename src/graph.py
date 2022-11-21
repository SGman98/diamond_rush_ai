from queue import PriorityQueue

LOGGING = True

MEMO = {}


class Spot:
    def __init__(self, x, y, rows, cols):
        self.x = x
        self.y = y

        self.closed = False

        # collectable items
        self.isdiamond = False
        self.iskey = False

        # doors and gates
        self.isdoor = False
        self.isgate = False

        # interactive spots
        self.isbutton = False
        self.isspike = False
        self.isrock = False

        # other
        self.ishole = False
        self.islava = False

        self.ispath = False  # whether the spot is a path or wall

        self.isexit = False

        self.total_rows = rows
        self.total_cols = cols

        self.neighbors = []

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

    def make_exit(self):
        self.isexit = True

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
            'W': self.make_wall,
            'P': self.make_path,
            'D': self.make_diamond,
            'C': self.make_closed_door,
            'O': self.make_open_door,
            'H': self.make_hole,
            'K': self.make_key,
            'L': self.make_lava,
            'G': self.make_closed_gate,
            'B': self.make_button,
            'S': self.make_spike,
            'R': self.make_rock,

            'E': self.make_exit,
            '#': self.make_path,
        }

        if (value in transform):
            transform[value]()
        else:
            print(f'Using default state for {value}')
            self.make_path()

    def is_blocked(self):
        return not self.ispath

    def update_neighbors(self, grid):
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
        str = ''
        str += '1' if self.ispath else '0'
        str += '1' if self.isdiamond else '0'
        str += '1' if self.iskey else '0'
        str += '1' if self.isdoor else '0'
        str += '1' if self.isgate else '0'
        str += '1' if self.isbutton else '0'
        str += '1' if self.isspike else '0'
        str += '1' if self.isrock else '0'
        str += '1' if self.ishole else '0'
        str += '1' if self.islava else '0'
        str += '1' if self.isexit else '0'

        return str

    def copy(self):
        spot = Spot(self.x, self.y, self.total_rows, self.total_cols)
        spot.closed = self.closed
        spot.isdiamond = self.isdiamond
        spot.iskey = self.iskey
        spot.isdoor = self.isdoor
        spot.isgate = self.isgate
        spot.isbutton = self.isbutton
        spot.isspike = self.isspike
        spot.isrock = self.isrock
        spot.ishole = self.ishole
        spot.islava = self.islava
        spot.ispath = self.ispath
        spot.isexit = self.isexit
        return spot

    def __lt__(self, _):
        return False

    # printable representation of the object
    def __repr__(self):
        return f'Spot({self.x}, {self.y})'


def astar(grid, start, end):

    # Manhattan distance
    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        return abs(x1 - x2) + abs(y1 - y2)

    count = 0

    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}

    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = []

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
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if current != start:
            current.make_closed()

    return None


def path_to_movement(path):
    movement = []
    if path is None:
        # print('No path found in path_to_movement')
        return movement
    for i in range(len(path) - 1):
        x1, y1 = path[i].get_pos()
        x2, y2 = path[i + 1].get_pos()

        if x1 < x2:
            movement.append('s')
        elif x1 > x2:
            movement.append('w')
        elif y1 < y2:
            movement.append('d')
        elif y1 > y2:
            movement.append('a')

    return movement


class Player:
    def __init__(
        self,
        board,
        start,
        end,
        has_key=False,
        depth=0,
        max_path_length=1000
    ):
        if depth != 0:
            self.board = board
        else:
            self.board = self.create_board(board)
        self.pos = start
        self.end = end
        self.depth = depth
        self.max_path_length = max_path_length
        self.has_key = has_key
        self.diamonds = self.get_total_diamonds()
        self.movement = ''

    def get_total_diamonds(self):
        total_diamonds = 0

        for row in self.board:
            for spot in row:
                if spot.isdiamond:
                    total_diamonds += 1

        return total_diamonds

    def get_interest_points(self):
        interest_points = []

        for i, row in enumerate(self.board):
            for j, spot in enumerate(row):
                path = self.get_path((i, j))

                if path == '':
                    continue

                is_exit = self.diamonds == 0 and spot.isexit
                is_key = not self.has_key and spot.iskey
                is_gate = self.has_key and spot.isgate
                is_diamond = spot.isdiamond

                if is_exit or is_key or is_gate or is_diamond:
                    interest_points.append(path)

        interest_points.sort(key=lambda x: len(x))

        interest_points_final = []
        for path in interest_points:
            for path2 in interest_points:
                if path == path2:
                    continue

                if path.startswith(path2):
                    break
            else:
                interest_points_final.append(path)

        def shorter_than_max(x): return len(x) <= self.max_path_length

        return list(filter(shorter_than_max, interest_points_final))

    def get_path(self, end):
        grid = self.get_board_copy()
        for i, row in enumerate(grid):
            for j, spot in enumerate(row):
                if spot.isgate and self.has_key and end == (i, j):
                    spot.make_path()
                if spot.isexit and self.diamonds == 0 and end == (i, j):
                    spot.make_path()

        for row in grid:
            for spot in row:
                spot.update_neighbors(grid)

        # get path
        start = grid[self.pos[0]][self.pos[1]]
        end = grid[end[0]][end[1]]

        path = astar(grid, start, end)

        # transform path to movement W, A, S, D
        movement = path_to_movement(path)

        return ''.join(movement)

    def create_board(self, board):
        grid = []

        for i, row in enumerate(board):
            grid.append([])

            for j, spot in enumerate(row):
                state = spot
                spot = Spot(i, j, len(board), len(row))

                spot.make_state(state)

                grid[i].append(spot)

        for row in grid:
            for spot in row:
                spot.update_neighbors(grid)

        return grid

    def get_board_copy(self):
        board_copy = []

        for i, row in enumerate(self.board):
            board_copy.append([])

            for j, spot in enumerate(row):
                board_copy[i].append(spot.copy())

        for row in board_copy:
            for spot in row:
                spot.update_neighbors(board_copy)

        return board_copy

    def move(self, path):
        self.movement = path

        def move_player(direction):
            if direction == 'w':
                self.pos = (self.pos[0] - 1, self.pos[1])
            elif direction == 's':
                self.pos = (self.pos[0] + 1, self.pos[1])
            elif direction == 'a':
                self.pos = (self.pos[0], self.pos[1] - 1)
            elif direction == 'd':
                self.pos = (self.pos[0], self.pos[1] + 1)

        for direction in self.movement:
            move_player(direction)
            self.update_state()

    def update_state(self):
        spot = self.board[self.pos[0]][self.pos[1]]
        if spot.iskey and not self.has_key:
            self.has_key = True
            spot.iskey = False
            return
        if spot.isdiamond:
            self.diamonds -= 1
            spot.isdiamond = False
            return
        if spot.isspike:
            spot.make_wall()
            return
        if spot.isgate and self.has_key:
            spot.make_path()
            spot.isgate = False
            self.has_key = False
            return
        if spot.isgate:
            print("wtf")

    def print(self, message=''):
        global LOGGING
        if not LOGGING:
            return
        print(">\t"*self.depth + message)

    def board_to_string(self):
        return '.'.join([spot.to_string() for row in self.board for spot in row])

    def solve(self):
        global LOGGING

        if self.pos == self.end:
            self.print("Reached end")
            return True

        memo_key = str(self)

        if memo_key in MEMO:
            movement = MEMO[memo_key]

            if movement == '':
                self.print("Player failed to reach the end (memo)")
                return False

            self.print(f"Reach end with path {movement} (memo)")
            self.movement += movement
            return True

        result = ''

        interest_points = self.get_interest_points()

        for path in interest_points:

            new_player = Player(
                self.get_board_copy(),
                self.pos,
                self.end,
                self.has_key,
                self.depth+1,
                self.max_path_length - len(path)
            )

            new_player.move(path)
            new_player.print(f"Moved to {new_player.pos} with path {path}")

            if new_player.solve():
                if len(result) == 0 or len(new_player.movement) < len(result):
                    result = new_player.movement
                    self.max_path_length = min(
                        self.max_path_length, len(result))
                    self.print(f"New best path: {result}")
                    break  # comment this line to find the optimal path
                else:
                    self.print(f"Same or worse path: {new_player.movement}")

        MEMO[memo_key] = result

        if result != '':
            self.movement += result
            if self.depth == 0:
                print(f"Final path: {self.movement}")
            return True

        self.print("Player failed to reach the end")
        return False

    def __repr__(self):
        return self.board_to_string() + str(self.pos) + str(self.has_key)
