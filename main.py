import numpy as np
from matplotlib import pyplot as plt
import cv2
import numpy as np
from numpy import binary_repr
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
    plt.hist(array_r, bins=256, color="red")
    plt.suptitle("Histogram R")
    plt.show()
    plt.hist(array_g, bins=256, color="green")
    plt.suptitle("Histogram G")
    plt.show()
    plt.hist(array_b, bins=256, color="blue")
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


def random(array_r, array_g, array_b, length):
    randombit = []

    # (1 & (r ^ g ^ b ^ r1 ^ g1 ^ b1 ^ r2 ^ g2 ^ b2))
    for i in range(1, length - 2):
        mask1 = binary_repr(7)
        mask2 = binary_repr(6)
        mask3 = binary_repr(5)
        mask4 = binary_repr(4)
        mask5 = binary_repr(3)
        mask6 = binary_repr(2)
        mask7 = binary_repr(1)
        mask8 = binary_repr(0)

        randombit.append(int(binary_repr(1) & ((binary_repr(array_r[i])*binary_repr(mask1)) ^ (binary_repr(array_g[i])*binary_repr(mask1)) ^ (binary_repr(array_b[i])*binary_repr(mask1)) ^
                              (binary_repr(array_r[i - 1])*binary_repr(mask1)) ^ (binary_repr(array_g[i - 1])*binary_repr(mask1)) ^ (binary_repr(array_b[i - 1])*binary_repr(mask1)) ^
                              (binary_repr(array_r[i + 1])*binary_repr(mask1)) ^ (binary_repr(array_g[i + 1])*binary_repr(mask1)) ^ (binary_repr(array_b[i + 1])*binary_repr(mask1)))))

    return randombit


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

    # print(entropy([1/2, 1/2], base=2))
    # generate_histograms(array_r, array_g, array_b, length)

    # print("\n")
    # print("ENTROPIA:")
    random_array = random(array_r, array_g, array_b, length)
    print(random_array)
    # print(len(random_array))
    # print(entropy(random_array))
