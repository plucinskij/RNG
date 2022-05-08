
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
    x = int(x)
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


def generate_histograms(array_r, array_g, array_b,):
    plt.hist(array_r, bins=256, color="red")
    plt.suptitle("Histogram R")
    plt.show()
    plt.hist(array_g, bins=256, color="green")
    plt.suptitle("Histogram G")
    plt.show()
    plt.hist(array_b, bins=256, color="blue")
    plt.suptitle("Histogram B")
    plt.show()


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
    for i in range(40, length - 40):
        # mask1 = binary_repr(7)
        # mask2 = binary_repr(6)
        # mask3 = binary_repr(5)
        # mask4 = binary_repr(4)
        # mask5 = binary_repr(3)
        # mask6 = binary_repr(2)
        # mask7 = binary_repr(1)
        # mask8 = binary_repr(0)

        # randombit.append(int(binary_repr(1) & ((binary_repr(array_r[i])*binary_repr(mask1)) ^ (binary_repr(array_g[i])*binary_repr(mask1)) ^ (binary_repr(array_b[i])*binary_repr(mask1)) ^
        #                      (binary_repr(array_r[i - 1])*binary_repr(mask1)) ^ (binary_repr(array_g[i - 1])*binary_repr(mask1)) ^ (binary_repr(array_b[i - 1])*binary_repr(mask1)) ^
        #                      (binary_repr(array_r[i + 1])*binary_repr(mask1)) ^ (binary_repr(array_g[i + 1])*binary_repr(mask1)) ^ (binary_repr(array_b[i + 1])*binary_repr(mask1)))))
        #
        randombit.append((array_r[i] ^ array_g[i] ^ array_b[i] ^
                          array_r[i - 21] ^ array_g[i - 31] ^ array_b[i - 2] ^
                          array_r[i + 12] ^ array_g[i + 24] ^ array_b[i + 34]))

    return randombit


def myentropy(array_inp, len):
    array = []
    entr = 0
    for i in range(0, 255):
        array.append(array_inp.count(i) / len)
    print("Tablica prawdopodobieństw =", array)
    for i in range(0, 255):
        entr += array[i] * np.log2(array[i])

    entr = entr * (-1)
    print("Entropia =", entr)


if __name__ == '__main__':
    video = "warszawa3.mp4"
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

    generate_histograms(array_r, array_g, array_b)

    print("\n")
    print("PO POSTPROCESINGU:")
    random_array = random(array_r, array_g, array_b, length)
    print("Tablica wartości =", random_array)
    myentropy(random_array, length)
    plt.hist(random_array, bins=254, color="orange")
    plt.suptitle("Random")
    plt.show()
