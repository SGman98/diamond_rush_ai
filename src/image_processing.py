import cv2 as cv
import numpy as np
import os

import browser
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
        for j, tile_b in enumerate(tiles_b):
            val = compare_tiles(tile_a, tile_b)
            if val > max_val:
                max_val = val
                max_index = j
        if max_val < error_margin:
            max_index = default_value
        print(f"Tile {i} is {max_index} with {max_val}")
        results.append(max_index)
    return np.array(results)


def recreate_board(indexes, tiles, cols, rows):
    tile_width, tile_height = tiles[0].shape[:2]
    result = np.zeros((rows * tile_height, cols * tile_width, 3), np.uint8)

    for i, index in enumerate(indexes):
        if index == -1:
            continue
        x = i % cols
        y = i // cols
        result[y * tile_height:(y + 1) * tile_height,
               x * tile_width:(x + 1) * tile_width] = tiles[index]

    return result


def process_board():

    board = browser.get_board()

    board = img_proc.crop_img(board, 10, 15, top=2, bottom=1, left=1, right=1)

    tileset = img_proc.get_image("tileset.png")

    board_tiles = img_proc.get_tiles(board, 8, 12)
    tileset_tiles = img_proc.get_tiles(tileset, 8, 8)[:-3]

    result = img_proc.compare_all_tiles(board_tiles, tileset_tiles, 0.6, 13)

    new_board = img_proc.recreate_board(result, tileset_tiles, 8, 12)

    img_proc.show_image(new_board)

    input("Press enter to start solving...")
