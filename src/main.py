from image_processing import crop_img, get_image, show_image

import browser


def main():
    browser.connect()
    input("Press enter to remove help...")
    browser.remove_help()
    input("Press enter to get board...")
    board = browser.get_board()

    board = crop_img(board, 10, 15, top=2, bottom=1, left=1, right=1)

    show_image(board)

    tileset = get_image("tileset.png")

    show_image(tileset)


if __name__ == "__main__":
    main()
