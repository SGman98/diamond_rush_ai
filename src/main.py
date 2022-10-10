from image_processing import crop_black_borders, get_image, show_image


def main():
    im = get_image()
    im = crop_black_borders(im)

    show_image(im)


if __name__ == "__main__":
    main()
