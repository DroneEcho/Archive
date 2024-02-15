import matplotlib.pyplot as plt
import time
from algs import *
from algs_test import *
from math import pi, sin, cos
from PyQt5.QtGui import QImage, QColor

def measure_time():
    m = [0, 0, 0, 0, 0]
    n = 100

    l = 250
    step = pi / 180

    img = QImage(l * 2, l * 2, QImage.Format_ARGB32)
    color = QColor(0, 0, 0)

    a = 0
    for j in range(360):
        x = rnd(l + l * cos(a))
        y = rnd(l - l * sin(a))

        for i in range(n):
            t = time.time_ns()
            TestCDA(l, l, x, y)
            m[0] += time.time_ns() - t

            t = time.time_ns()
            TestBresenhamFloat(l, l, x, y)
            m[1] += time.time_ns() - t

            t = time.time_ns()
            TestBresenhamInt(l, l, x, y)
            m[2] += time.time_ns() - t

            t = time.time_ns()
            TestBresenhamSmooth(l, l, x, y, 6)
            m[3] += time.time_ns() - t

            t = time.time_ns()
            TestVu(l, l, x, y)
            m[4] += time.time_ns() - t

        a += step

    for i in range(len(m)):
        m[i] /= 10 ** 6

    plt.bar(['ЦДА', 'Б/з действ.', 'Б/з цел.', 'Б/з с устр. ступ.', 'Ву'], m, label="Время в мс за {:d} построений".format(n * 360))
    plt.legend()
    plt.title('Исследование временных характеристик')
    plt.show()


def measure_steps(l):
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []

    step = 5 * pi / 180
    angles = [i * 5 for i in range(360 // 5)]

    img = QImage(l * 2, l * 2, QImage.Format_ARGB32)
    color = QColor(0, 0, 0)

    a = 0
    for i in range(len(angles)):
        x = rnd(l + l * cos(a))
        y = rnd(l - l * sin(a))

        y1.append(DrawCDA(img, l, l, x, y, color))

        y2.append(DrawBresenhamFloat(img, l, l, x, y, color))

        y3.append(DrawBresenhamInt(img, l, l, x, y, color))

        y4.append(DrawBresenhamSmooth(img, l, l, x, y, color, 2))

        y5.append(DrawVu(img, l, l, x, y, color))

        a += step

    plt.plot(angles, y1, '-', label='ЦДА')
    plt.plot(angles, y2, '-', label='Б/з действ.')
    plt.plot(angles, y3, '-', label='Б/з цел.')
    plt.plot(angles, y4, '-', label='Б/з с устр. ступ.')
    plt.plot(angles, y5, '-', label='Ву')
    plt.legend()
    plt.xlabel('Угол наклона в градусах (шаг = 5)')
    plt.ylabel('Максимальная длина ступени')
    plt.title('Исследование ступенчатости')

    plt.show()

# measure_time()
# measure_steps(10)

