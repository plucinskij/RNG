import numpy as np
from matplotlib import pyplot as plt
import cv2
import numpy as np
from scipy.stats import entropy


def color(x, y, frame):
    return (frame[y, x, 1] << 16) + (frame[y, x, 2] << 8) + (frame[y, x, 0])


def color_i(xc, yc, frame):
    colori = ((color(xc - 1, yc - 1, frame) + color(xc - 1, yc, frame) + color(xc - 1, yc + 1, frame)) / 9) + \
             ((color(xc, yc - 1, frame) + color(xc, yc, frame) + color(xc, yc + 1, frame)) / 9) + \
             ((color(xc + 1, yc - 1, frame) + color(xc + 1, yc, frame) + color(xc + 1, yc + 1, frame)) / 9)

    return colori


def initial(frame):
    xc = 170
    yc = 100

    height, width, channels = frame.shape

    colori = int(color_i(xc, yc, frame))
    x = (colori % (width / 2)) + (width / 4)
    y = (colori % (height / 2)) + (height / 4)

    return x, y, width, height


def get_rgb(x, y, image):
    x = int(x)  # float -> int
    y = int(y)
    b = (image[x, y, 0])
    r = (image[x, y, 1])
    g = (image[x, y, 2])
    return r, g, b


def make_rgb_arrays(x, y, length):
    array_r = []
    array_g = []
    array_b = []
    while length > 1:
        retval, image = cap.read()
        r, g, b = get_rgb(x, y, image)

        array_r.append(r)
        array_g.append(g)
        array_b.append(b)

        length -= 1

    return array_r, array_g, array_b


def generate_histograms(array_r, array_g, array_b, length):
    plt.hist(array_r, bins=210, color="red")
    plt.suptitle("Histogram R")
    plt.show()
    plt.hist(array_g, bins=210, color="green")
    plt.suptitle("Histogram G")
    plt.show()
    plt.hist(array_b, bins=210, color="blue")
    plt.suptitle("Histogram B")
    plt.show()

    # array_r, array_g, array_b są tablicami
    # elementy tych tablic mają typ numpy.uint8

    return 0


def ent(array_inp, len):
    array = []
    for i in range(0, 256):
        array.append(array_inp.count(i) / len)
    print("Tablica prawdopodobieństw =", array)
    print("Entropia =", entropy(array))
    return array


if __name__ == '__main__':
    video = "odmien.mp4"
    cap = cv2.VideoCapture(video)

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Paramerty nagrania:")
    print("liczba klatek:", length)
    print("szerokosc:", vid_width)
    print("dlugosc:", vid_height)

    retval, image = cap.read()
    x, y, width, height = initial(image)
    array_r, array_g, array_b = make_rgb_arrays(x, y, length)
    print("\n")
    print("RED:")
    print("Tablica wartości =", array_r)
    ent(array_r, length)

    print("\n")
    print("GREEN:")
    print("Tablica wartości =", array_g)
    ent(array_g, length)

    print("\n")
    print("BLUE:")
    print("Tablica wartości =", array_b)
    ent(array_b, length)

    generate_histograms(array_r, array_g, array_b, length)
