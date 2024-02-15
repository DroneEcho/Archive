import matplotlib.pyplot as plt
import time
from algs import *
from algs_ellipse import *
from math import pi, sin, cos
from PyQt5.QtGui import QImage, QColor
from scipy.optimize import curve_fit
import numpy as np


def curve(x, a, b):
    return a * x + b


def approx(x, y):
    xdata = np.asarray(x)
    ydata = np.asarray(y)

    xfine = np.linspace(xdata.min(), xdata.max(), 100)
    popt, pcov = curve_fit(curve, xdata, ydata)

    return xfine, curve(xfine, *popt)


def measure_time():
    n = 2000

    r1 = 10
    r2 = 310
    step = 25
    qty = (r2 - r1) // step
    
    m = [[0] * qty, [0] * qty, [0] * qty, [0] * qty]

    xc = r2
    yc = r2
    img = QImage(r2 * 2, r2 * 2, QImage.Format_ARGB32)
    color = QColor(0, 0, 0)

    index = 0
    for r in range(r1, r2, step):
        for i in range(n):
            t = time.time_ns()
            DrawCanon(img, xc, yc, r, color, draw=False)
            m[0][index] += (time.time_ns() - t) / 1000000

            t = time.time_ns()
            DrawParam(img, xc, yc, r, color, draw=False)
            m[1][index] += (time.time_ns() - t) / 1000000

            t = time.time_ns()
            DrawBresenham(img, xc, yc, r, color, draw=False)
            m[2][index] += (time.time_ns() - t) / 1000000

            t = time.time_ns()
            DrawMidPoint(img, xc, yc, r, color, draw=False)
            m[3][index] += (time.time_ns() - t) / 1000000

        index += 1

    x = list(range(r1, r2, step))

    plt.plot(x, m[0], 'r.')
    x1, y1 = approx(x, m[0])
    plt.plot(x1, y1, 'r-', label='Каноническое ур. (Время в мс за {:d} построений)'.format(n))
    
    plt.plot(x, m[1], 'g.')
    x1, y1 = approx(x, m[1])
    plt.plot(x1, y1, 'g-', label='Парам ур.')

    plt.plot(x, m[2], 'b.')
    x1, y1 = approx(x, m[2])
    plt.plot(x1, y1, 'b-', label='Алг. Брезенхема')

    plt.plot(x, m[3], 'c.')
    x1, y1 = approx(x, m[3])
    plt.plot(x1, y1, 'c-', label='Алг. средней точки')

    plt.xlabel('Радиус')
    plt.ylabel('Время в мс за {:d} построений'.format(n))

    plt.legend()
    plt.title('Исследование временных характеристик')
    plt.show()


def measure_time_ellipse():
    n = 1000

    a1 = 10
    a2 = 310
    step = 25
    

    xc = a1
    yc = a1 // 2
    img = QImage(a1 * 2, a1, QImage.Format_ARGB32)
    color = QColor(0, 0, 0)

    x = list(range(a1, a2, step))
    qty = len(x)
    a = a1
    b = a // 2
    
    m = [[0] * qty, [0] * qty, [0] * qty, [0] * qty]

    for index in range(qty):
        for i in range(n):
            t = time.time_ns()
            DrawCanonEllipse(img, xc, yc, a, b, color, draw=False)
            m[0][index] += (time.time_ns() - t) / 1000000

            t = time.time_ns()
            DrawParamEllipse(img, xc, yc, a, b, color, draw=False)
            m[1][index] += (time.time_ns() - t) / 1000000

            t = time.time_ns()
            DrawBresenhamEllipse(img, xc, yc, a, b, color, draw=False)
            m[2][index] += (time.time_ns() - t) / 1000000

            t = time.time_ns()
            DrawMidPointEllipse(img, xc, yc, a, b, color, draw=False)
            m[3][index] += (time.time_ns() - t) / 1000000

        index += 1
        a += step
        b = a // 2

    plt.plot(x, m[0], 'r.', alpha=1)
    x1, y1 = approx(x, m[0])
    plt.plot(x1, y1, 'r-', label='Каноническое ур.')
    
    plt.plot(x, m[1], 'g.', alpha=1)
    x1, y1 = approx(x, m[1])
    plt.plot(x1, y1, 'g-', label='Парам ур.')

    plt.plot(x, m[2], 'b.', alpha=1)
    x1, y1 = approx(x, m[2])
    plt.plot(x1, y1, 'b-', label='Алг. Брезенхема')

    plt.plot(x, m[3], 'c.', alpha=1)
    x1, y1 = approx(x, m[3])
    plt.plot(x1, y1, 'c-', label='Алг. средней точки')

    plt.xlabel('Полуось')
    plt.ylabel('Время в мс за {:d} построений'.format(n))

    plt.legend()
    plt.title('Исследование временных характеристик')
    plt.show()
