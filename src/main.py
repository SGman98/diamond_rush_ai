from image_processing import crop_black_borders, crop_img, get_image, show_image


def main():
    print("Please select an image for the game board...")
    board = get_image()
    board = crop_black_borders(board)
    board = crop_img(board, 10, 15, top=2, bottom=1, left=1, right=1)

    show_image(board)

    tileset = get_image("tileset.png")

    show_image(tileset)


if __name__ == "__main__":
    main()
