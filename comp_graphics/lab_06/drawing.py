from PyQt5.QtGui import *
from math import sin, cos, sqrt, ceil, pi
import time


def FillFigure(img, x0, y0, color, delay=False, timerStop=None):
    baseColor = img.pixel(x0, y0)
    if baseColor == color:
        return
    
    stack = [(x0, y0)]

    while len(stack) > 0:
        x, y = stack.pop()
        img.setPixel(x, y, color)

        # Правый интервал
        xi = x + 1
        while img.pixel(xi, y) == baseColor:
            img.setPixel(xi, y, color)
            xi += 1
        wr = xi

        # Левый интервал
        xi = x - 1
        while img.pixel(xi, y) == baseColor:
            img.setPixel(xi, y, color)
            xi -= 1
        wl = xi

        # Верхняя строка
        xi = wl + 1
        f = True
        while xi < wr:
            if f:
                if img.pixel(xi, y - 1) == baseColor:
                    stack.append((xi, y - 1))
                    f = False
            else:
                if img.pixel(xi, y - 1) != baseColor:
                    f = True
            xi += 1

        # Нижняя строка
        xi = wl + 1
        f = True
        while xi < wr:
            if f:
                if img.pixel(xi, y + 1) == baseColor:
                    stack.append((xi, y + 1))
                    f = False
            else:
                if img.pixel(xi, y + 1) != baseColor:
                    f = True
            xi += 1

        if delay:
            time.sleep(0.002)

    if delay:
        timerStop()    
