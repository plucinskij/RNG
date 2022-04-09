import numpy as np
from matplotlib import pyplot as plt
from math import log, e
import cv2
from scipy.io import wavfile
import moviepy.editor as mp
from os import path
from pydub import AudioSegment


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

    colori = color_i(xc, yc, frame)
    x = (colori % (width / 2)) + (width / 4)
    y = (colori % (height / 2)) + (height / 4)
    th = 100
    watchdog = 0

    return x, y, th, watchdog, width, height


def extractaudio(video):
    # audio = VideoFileClip(video).audio
    # clip = mp.VideoFileClip(video)
    # audio = clip.audio
    # audio.write_audiofile("audio.mp3")
    # src = "audio.mp3"
    # sound = AudioSegment.from_mp3(src)
    # sound.export("audio.wav", format="wav")
    # samplerate, audiodata = wavfile.read("audio.wav")
    samplerate, audio = wavfile.read("test.wav")

    return audio


def get_rgb(frame, x, y):
    x = int(x)
    y = int(y)
    b = int(frame[x, y, 0])
    r = int(frame[x, y, 1])
    g = int(frame[x, y, 2])
    return r, g, b


def SN(r, g, b, audio):
    k = 500
    runcnt = 0

    for i in range(0, 16):
        sound_byte = []
        for iter in range(5880):
            sound_byte.append(audio[iter])
            if runcnt < 100000:
                runcnt += 1

        SN1 = sound_byte[int(10 + (r * i + (g << 2) + b + runcnt) % (k / 2))]
        SN2 = sound_byte[int(15 + (r * i + (g << 3) + b + runcnt) % (k / 2))]
        SN3 = sound_byte[int(20 + (r * i + (g << 4) + b + runcnt) % (k / 2))]
        SN4 = sound_byte[int(5 + (r * i + (g << 1) + b + runcnt) % (k / 2))]
        SN5 = sound_byte[int(25 + (r * i + (g << 5) + b + runcnt) % (k / 2))]

    return SN1, SN2, SN3, SN4, SN5


def diff():
    r1 = 0
    r2 = 0
    g1 = 0
    g2 = 0
    b1 = 0
    b2 = 0
    return r1, r2, g1, g2, b1, b2


def randombit(r, g, b, SN1, SN2, SN3, SN4, SN5, r1, r2, g1, g2, b1, b2, x, y, width, height):

    random = str(1 & (r ^ g ^ b ^ r1 ^ g1 ^ b1 ^ r2 ^ g2 ^ b2 ^ SN1 ^ SN2 ^ SN3 ^ SN4 ^ SN5))
    x_old = x
    y_old = y



    x = ((((r ^ int(x_old)) << 4) ^ (g ^ int(y_old))) % width)/2
    y = ((((g ^ int(x_old)) << 4) ^ (b ^ int(y_old))) % height)/2
    return random, x, y


def rng(video, cap, frame, x, y, th, audio):
    randomuotstr = ''
    for i in range(0, 8):
        r, g, b = get_rgb(frame, x, y)
        SN1, SN2, SN3, SN4, SN5 = SN(r, g, b, audio)
        r1, r2, g1, g2, b1, b2 = diff()
        random, x, y = (randombit(r, g, b, SN1, SN2, SN3, SN4, SN5, r1, r2, g1, g2, b1, b2, x, y, width, height))
        randint = 0
        randint += int(random[1])
        randint += int(random[3])
        randint += int(random[5])
        randint += int(random[7])
        randint += int(random[9])
        randint += int(random[11])
        randomuotstr += str(randint)
    return randomuotstr, x, y


if __name__ == '__main__':
    video = "test.mp4"
    randomout = []
    cap = cv2.VideoCapture(video)
    res, frame = cap.read()
    x, y, th, watchdog, width, height = initial(frame)
    audio = extractaudio(video)
    for i in range (0,1000):
        rngout, x, y = rng(video, cap, frame, x, y, th, audio)
        randomout.append(rngout)
    plt.hist(randomout)
    plt.show()
    print (randomout)
