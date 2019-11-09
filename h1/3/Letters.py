from PIL import Image
import string


def main():
    img = open_image("letters.jpg")

    left, upper, right, lower = (0, 50, 230, 250)
    letters = list(string.ascii_uppercase)

    i = 1
    row = 1

    while (i < 27):

        save_img(img, (left, upper, right, lower), letters[i - 1]+".png")

        if i != 0 and i % 7 == 0:
            if row == 1:
                upper += 315
                lower += 315

            elif row == 2:
                upper += 300
                lower += 300

            elif row == 3:
                upper += 315
                lower += 315

            left, right = 0, 230
            row += 1
        else:
            # Some adjustments
            if letters[i-1] == "L":
                left += 260
                right += 260
                upper -= 20
                lower -= 20
            elif letters[i-1] == "P":
                upper -= 30
                lower -= 30
                left += 230
                right += 230
            elif letters[i-1] == "R":
                upper -= 40
                lower -= 40
                left += 270
                right += 270
            else:
                left += 230
                right += 230

        i += 1


def save_img(img, coords, letter):

    region = img.crop(coords)
    img_path = "./"+letter
    region.save(img_path, "PNG")


def open_image(fp):
    img = Image.open(fp)
    return img


main()
