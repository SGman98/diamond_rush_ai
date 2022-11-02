from queue import PriorityQueue

import numpy as np

LOGGING = True

MEMO = {}


class Spot:
    def __init__(self, x, y, rows, cols):
        self.x = x
        self.y = y

        self.closed = False

        self.state = ''
        self.isdiamond = False

        self.total_rows = rows
        self.total_cols = cols

        self.neighbors = []

    def get_pos(self):
        return self.x, self.y

    def is_closed(self):
        return self.closed

    def is_open(self):
        return not self.closed

    def make_closed(self):
        self.closed = True

    def make_open(self):
        self.closed = False

    def make_wall(self):
        self.state = 'W'

    def make_path(self):
        self.state = 'P'

    def make_diamond(self):
        self.state = 'P'
        self.isdiamond = True

    def make_exit(self):
        self.state = 'E'

    def make_closed_door(self):
        self.state = 'W'
        self.isdoor = True

    def make_open_door(self):
        self.state = 'P'
        self.isdoor = True

    def make_hole(self):
        self.state = 'W'
        self.ishole = True

    def make_filled_hole(self):
        self.state = 'P'
        self.ishole = False

    def make_key(self):
        self.state = 'P'
        self.iskey = True

    def make_lava(self):
        self.state = 'W'
        self.islava = True

    def make_closed_gate(self):
        self.state = 'W'
        self.isgate = True

    def make_open_gate(self):
        self.state = 'P'
        self.isgate = True

    def make_button(self):
        self.state = 'P'
        self.isbutton = True

    def make_spike(self):
        self.state = 'P'
        self.isspike = True

    def make_closed_spike(self):
        self.state = 'W'
        self.isspike = True

    def make_rock(self):
        self.state = 'W'
        self.isrock = True

    def make_start(self):
        self.state = 'S'

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

            'E': lambda: None,
            '#': lambda: None,
        }

        if (value in transform):
            transform[value]()
        else:
            print(f'Using default state for {value}')
            self.make_path()

    def is_blocked(self):
        return self.state == 'W'

    def is_path(self):
        return self.state == 'P'

    def is_start(self):
        return self.state == 'S'

    def is_exit(self):
        return self.state == 'E'

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

    def __lt__(self, other):
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
    def __init__(self, board, start, end, depth=0):
        self.board = board
        self.pos = start
        self.end = end
        self.depth = depth
        self.has_key = False
        self.diamonds = self.get_total_diamonds()
        self.movement = []
        self.logging = False

    def get_total_diamonds(self):
        total_diamonds = 0

        for row in self.board:
            for spot in row:
                if spot == 'D':
                    total_diamonds += 1

        return total_diamonds

    def get_interest_points(self):
        interest_points = []

        for i, row in enumerate(self.board):
            for j, spot in enumerate(row):
                if self.get_path((i, j)) == []:
                    continue

                if self.diamonds == 0 and spot == 'E':
                    interest_points.append((i, j))
                elif not self.has_key and spot == 'K':
                    interest_points.append((i, j))
                elif spot == 'D':
                    interest_points.append((i, j))

        return interest_points

    def get_path(self, end):
        grid = []

        for i, row in enumerate(self.board):
            grid.append([])

            for j, spot in enumerate(row):
                spot = Spot(i, j, len(self.board), len(row))

                spot.make_state(self.board[i][j])

                grid[i].append(spot)

        for row in grid:
            for spot in row:
                spot.update_neighbors(grid)

        # get path
        start = grid[self.pos[0]][self.pos[1]]
        path = astar(grid, start, grid[end[0]][end[1]])

        # transform path to movement W, A, S, D
        movement = path_to_movement(path)

        return movement

    def move(self, end):
        self.movement = self.get_path(end)

        for direction in self.movement:
            if direction == 'w':
                self.pos = (self.pos[0] - 1, self.pos[1])
            elif direction == 's':
                self.pos = (self.pos[0] + 1, self.pos[1])
            elif direction == 'a':
                self.pos = (self.pos[0], self.pos[1] - 1)
            elif direction == 'd':
                self.pos = (self.pos[0], self.pos[1] + 1)

            self.update_state()

    def update_state(self):
        if self.board[self.pos[0]][self.pos[1]] == 'K' and not self.has_key:
            self.has_key = True
            self.board[self.pos[0]][self.pos[1]] = 'P'
            return
        if self.board[self.pos[0]][self.pos[1]] == 'D':
            self.diamonds -= 1
            self.board[self.pos[0]][self.pos[1]] = 'P'
            return
        if self.board[self.pos[0]][self.pos[1]] == 'S':
            self.board[self.pos[0]][self.pos[1]] = 'W'
            return

    def print(self, message):
        global LOGGING
        if not LOGGING:
            return
        print(">\t"*self.depth + message)

    def board_to_string(self):
        return '\n'.join([''.join(row) for row in self.board])

    def solve(self):
        global LOGGING
        if self.pos[0] == 10 and self.depth == 1:
            LOGGING = True
        self.print(f"New Player from position {self.pos[0]}, {self.pos[1]}")
        interest_points = self.get_interest_points()

        if self.board_to_string() in MEMO:
            if MEMO[self.board_to_string()][0]:
                movement = MEMO[self.board_to_string()][1]
                self.print(f"Found movement {movement} in memo")
                self.movement = movement
                return
            else:
                self.print(f"Found no movement in memo")
                return False

        result_ = False

        for point in interest_points:
            board_copy = self.board.copy()
            new_player = Player(board_copy, self.pos, self.end, self.depth+1)

            new_player.move(point)
            self.print(f"Get {point} movement {''.join(new_player.movement)}")

            if new_player.pos == self.pos:
                self.print('No path found')
                result_ = False
                break

            if new_player.pos == new_player.end:
                self.print("Player reached the end")
                self.movement += new_player.movement

                result_ = True
                break

            if new_player.solve():
                self.movement += new_player.movement
                if (self.depth == 0):
                    self.print(f"Result: {''.join(self.movement)}")
                result_ = True
                break

        if not result_:
            self.print(f"Player failed to reach the end")

        MEMO[self.board_to_string()] = (result_, self.movement)
        return result_
