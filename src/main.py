import browser
import image_processing as img_proc


def main():
    browser.connect()
    input("Press enter to remove help...")
    browser.remove_help()
    input("Press enter to get board...")
    board = browser.get_board()

    board = img_proc.crop_img(board, 10, 15, top=2, bottom=1, left=1, right=1)

    tileset = img_proc.get_image("tileset.png")

    board_tiles = img_proc.get_tiles(board, 8, 12)
    tileset_tiles = img_proc.get_tiles(tileset, 8, 8)[:-3]

    result = img_proc.compare_all_tiles(board_tiles, tileset_tiles, 0.6, 13)

    new_board = img_proc.recreate_board(result, tileset_tiles, 8, 12)

    img_proc.show_image(new_board)

    input("Press enter to start solving...")

    solutions = {
        1: "dddddsssaaaaassdsdddds",
        2: "aaaaasawwwwwwwwwdwdsddssddsaassaas",
        3: "dssssssassdddddddaaawwwwddwdssawaaawwssssssdswwwwwwawwdwddwdassdw",
        4: "ddddssaaaaassddddddassaaaaasdwdsssdswwawddwdsss",
        # ...
    }

    browser.move(solutions[1])

    input("Press enter to exit...")
    browser.close()


if __name__ == "__main__":
    main()
