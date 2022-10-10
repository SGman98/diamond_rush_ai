from image_processing import crop_black_borders, get_image, show_image


def main():
    im = get_image()
    im = crop_black_borders(im)
    im = crop_img(im, 10, 15, top=2, bottom=1, left=1, right=1)

    show_image(im)


if __name__ == "__main__":
    main()
