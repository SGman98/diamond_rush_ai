from queue import PriorityQueue

import numpy as np


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


# Manhattan distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def astar(grid, start, end):
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
        print('No path found')
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


def get_path(board, start, end):
    # make grid
    grid = []

    for i, row in enumerate(board):
        grid.append([])

        for j, spot in enumerate(row):
            spot = Spot(i, j, len(board), len(row))

            spot.make_state(board[i][j])

            grid[i].append(spot)

    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    # get path
    path = astar(grid, grid[start[0]][start[1]], grid[end[0]][end[1]])

    # transform path to movement W, A, S, D
    movement = path_to_movement(path)

    print(movement)

    return movement
