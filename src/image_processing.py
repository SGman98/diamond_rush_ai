import os

from cv2 import cv2 as cv
import numpy as np

import image_processing as img_proc


def get_image(name):
    name = os.path.join(os.path.dirname(__file__), "..", "images", name)
    return cv.imread(name)


def show_image(image):
    cv.imshow('image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def crop_img(image, cols, rows, top=0, bottom=0, left=0, right=0):
    height, width = image.shape[:2]
    tile_width = width / cols
    tile_height = height / rows
    # remove top and bottom
    image = image[int(top * tile_height):int((rows - bottom) * tile_height), :]
    # remove left and right
    image = image[:, int(left * tile_width):int((cols - right) * tile_width)]

    return image


def get_tiles(image, cols, rows):
    height, width = image.shape[:2]
    tile_width = width / cols
    tile_height = height / rows
    tiles = []
    for i in range(rows):
        for j in range(cols):
            tile = image[int(i * tile_height):int((i + 1) * tile_height),
                         int(j * tile_width):int((j + 1) * tile_width)]
            tile = cv.resize(tile, (64, 64))
            tiles.append(tile)
    return tiles


def compare_tiles(tile1, tile2):
    # Convert to grayscale
    tile1 = cv.cvtColor(tile1, cv.COLOR_BGR2GRAY)
    tile2 = cv.cvtColor(tile2, cv.COLOR_BGR2GRAY)

    # Compare
    result = cv.matchTemplate(tile1, tile2, cv.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv.minMaxLoc(result)

    return max_val


def compare_all_tiles(tiles_a, tiles_b, error_margin=0.9, default_value=-1):
    results = []
    for i, tile_a in enumerate(tiles_a):
        max_val, max_index = 0, 0
        if i < 8:
            tile_a = crop_img(tile_a, 1, 2, top=1)

        for j, tile_b in enumerate(tiles_b):
            if i < 8:
                tile_b = crop_img(tile_b, 1, 2, top=1)

            val = compare_tiles(tile_a, tile_b)

            if val > max_val and val != 1:
                max_val = val
                max_index = j
        if max_val < error_margin:
            max_index = default_value

        results.append(max_index)
    return np.array(results)


def board_to_processable_array(board):
    # if board is 0..=6     => 'W' (wall)
    # if board is 7..=15    => 'P' (path)
    # if board is 16        => 'D' (diamond)
    # if board is 17 or 18  => 'E' (exit)
    # if board is 19        => 'C' (closed door)
    # if board is 20        => 'O' (open door)
    # if board is 21        => 'H' (hole)
    # if board is 22        => 'P' (path) (filled hole)
    # if board is 23 or 24  => 'K' (key)
    # if board is 25..=33   => 'L' (lava)
    # if board is 34        => 'G' (gate) (key door)
    # if board is 35..=54   => 'W' (wall)
    # if board is 55 or 56  => 'B' (button)
    # if board is 57        => 'W' (wall) (activated spikes)
    # if board is 58        => 'S' (spikes) (deactivated spikes)
    # if board is 59        => 'R' (rock)
    # if board is 60        => '#' (player) (start)

    result = []
    for row in board:
        new_row = []
        for tile in row:
            if tile in range(0, 7):
                new_row.append('W')
            elif tile in range(7, 16):
                new_row.append('P')
            elif tile == 16:
                new_row.append('D')
            elif tile in range(17, 19):
                new_row.append('E')
            elif tile == 19:
                new_row.append('C')
            elif tile == 20:
                new_row.append('O')
            elif tile == 21:
                new_row.append('H')
            elif tile == 22:
                new_row.append('P')
            elif tile in range(23, 25):
                new_row.append('K')
            elif tile in range(25, 34):
                new_row.append('L')
            elif tile == 34:
                new_row.append('G')
            elif tile in range(35, 55):
                new_row.append('W')
            elif tile == 55:  # Set to 'P' because is failling
                new_row.append('P')
            elif tile in range(55, 57):
                new_row.append('B')
            elif tile == 57:
                new_row.append('W')
            elif tile == 58:
                new_row.append('S')
            elif tile == 59:
                new_row.append('R')
            elif tile == 60:
                new_row.append('#')
            elif tile == 61:
                new_row.append('E')

        result.append(new_row)
    return np.array(result)


def recreate_board(types, cols, rows):
    tileset = img_proc.get_image("tileset.png")
    tiles = img_proc.get_tiles(tileset, 8, 8)[:-2]

    tile_width, tile_height = tiles[0].shape[:2]
    result = np.zeros((rows * tile_height, cols * tile_width, 3), np.uint8)

    types = types.flatten()

    resolve = {
        'W': 0,
        'P': 7,
        'D': 16,
        'E': 17,
        'C': 19,
        'O': 20,
        'H': 21,
        'K': 23,
        'L': 25,
        'G': 34,
        'B': 56,
        'S': 58,
        'R': 59,
        '#': 60
    }

    # replace tiles
    for i, type in enumerate(types):
        index = resolve.get(type, 0)
        x = i % cols
        y = i // cols
        result[y * tile_height:(y + 1) * tile_height,
               x * tile_width:(x + 1) * tile_width] = tiles[index]

    return result


def process_board(board):
    board = img_proc.crop_img(board, 10, 15, top=2, bottom=1, left=1, right=1)

    tileset = img_proc.get_image("tileset.png")

    board_tiles = img_proc.get_tiles(board, 8, 12)
    tileset_tiles = img_proc.get_tiles(tileset, 8, 8)[:-2]

    result = img_proc.compare_all_tiles(board_tiles, tileset_tiles, 0.5, 13)

    result = board_to_processable_array(result.reshape(12, 8))

    return result
