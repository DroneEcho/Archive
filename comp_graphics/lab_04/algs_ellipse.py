from PyQt5.QtGui import *
from math import sin, cos, sqrt, ceil, pi


def rnd(x):
    return int(x + 0.5)


def SetPixel(img, x, y, color):
    if 0 <= x and x < img.width() and 0 <= y and y < img.height():
        img.setPixel(x, y, color.rgb())


def Draw4EllipsePoints(img, xc, yc, x, y, color):
    x = rnd(x)
    y = rnd(y)

    SetPixel(img, xc + x, yc + y, color)
    SetPixel(img, xc - x, yc + y, color)
    SetPixel(img, xc + x, yc - y, color)
    SetPixel(img, xc - x, yc - y, color)


def DrawBresenhamEllipse(img, xc, yc, a, b, color, draw = True):
    x = 0
    y = b
    a_2 = a * a
    b_2 = b * b
    delta = b_2 - a_2 * (2 * b + 1)
    
    if draw:
        Draw4EllipsePoints(img, xc, yc, x, y, color)

    while y > 0:
        if delta <= 0:
            d1 = delta + delta + a_2 * (2 * y - 1)
            x += 1
            delta += b_2 * (2 * x + 1)

            if d1 >= 0:
                y -= 1
                delta += a_2 * (1 - 2 * y)

        else:
            d2 = delta + delta + b_2 * (-2 * x - 1)
            y -= 1
            delta += a_2 * (-2 * y + 1)

            if d2 < 0:
                x += 1
                delta += b_2 * (2 * x + 1)
    
        if draw:
            Draw4EllipsePoints(img, xc, yc, x, y, color)
        

def DrawMidPointEllipse(img, xc, yc, a, b, color, draw = True):
    sqr_a, sqr_b = a * a, b * b
    limit = round(a / sqrt(1 + sqr_b / sqr_a))
    x, y = 0, b
    f = sqr_b - round(sqr_a * (b - 1/4))
    
    if draw:
        Draw4EllipsePoints(img, xc, yc, x, y, color)

    while x < limit:
        if f > 0:
            y -= 1
            f -= 2 * sqr_a * y

        x += 1
        f += sqr_b * (2 * x + 1)
        
        if draw:
            Draw4EllipsePoints(img, xc, yc, x, y, color)

    limit = round(b / sqrt(1 + sqr_a / sqr_b))
    y, x = 0, a
    f = sqr_a - round(sqr_b * (a - 1/4))

    if draw:
        Draw4EllipsePoints(img, xc, yc, x, y, color)

    while y < limit:
        if f > 0:
            x -= 1
            f -= 2 * sqr_b * x

        y += 1
        f += sqr_a * (2 * y + 1)
        
        if draw:
            Draw4EllipsePoints(img, xc, yc, x, y, color)


def DrawCanonEllipse(img, xc, yc, a, b, color, draw = True):
    x = 0
    y = b

    x_end = a / sqrt(1 + b * b / a / a)

    while x <= x_end:
        y = rnd(sqrt(1 - x * x / a / a) * b)   
        if draw:
            Draw4EllipsePoints(img, xc, yc, x, y, color)
        x += 1
    
    while y >= 0:
        y -= 1
        x = rnd(sqrt(1 - y * y / b / b) * a)
        if draw:
            Draw4EllipsePoints(img, xc, yc, x, y, color)


def DrawParamEllipse(img, xc, yc, a, b, color, draw = True):
    t = 0
    dt = 1 / max(a, b)
    t_end = pi / 2

    while t <= t_end + dt:
        x = rnd(a * cos(t))
        y = rnd(b * sin(t))
        
        if draw:
            Draw4EllipsePoints(img, xc, yc, x, y, color)
        
        t += dt


def DrawLibEllipse(img, xc, yc, a, b, color):
    painter = QPainter(img)
    painter.setPen(color)
    painter.drawEllipse(xc - a, yc - b, a + a, b + b)
