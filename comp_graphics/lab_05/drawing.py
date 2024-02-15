from PyQt5.QtGui import *
from math import sin, cos, sqrt, ceil, pi
import time


def rnd(x):
    return int(x + 0.5)


def DrawCrossingPoints(img, x1, y1, x2, y2, color):
    if y1 == y2:
        return

    if y1 > y2:
        x1, y1, x2, y2 = x2, y2, x1, y1

    dx = (x2 - x1) / (y2 - y1)
    x, y = x1, y1
    
    for i in range(y2 - y1):
        if img.pixel(x, y) == color:
            img.setPixel(x + 1, y, color)
        else:
            img.setPixel(x, y, color)

        x += dx
        y += 1


def SetPixel(img, x, y, color):
    if 0 <= x and x < img.width() and 0 <= y and y < img.height():
        img.setPixel(x, y, color.rgb())


def FillFigure(img, edges, color, backColor, delay=False, redraw=None):
    crossingColor = QColor.fromRgb((backColor.red() + color.red()) / 2, 0, 0).rgb()
    color = color.rgb()
    backColor = backColor.rgb()

    y_min, y_max = img.height(), 0
    x_min, x_max = 0, img.width()
    for edge in edges:
        DrawCrossingPoints(img, edge[0][0], edge[0][1], edge[1][0], edge[1][1], crossingColor)
        if edge[0][1] + 1 > y_max:
            y_max = edge[0][1] + 1
        if edge[0][1] < y_min:
            y_min = edge[0][1]
        if edge[0][0] + 1 > x_max:
            x_max = edge[0][0] + 1
        if edge[0][0] < x_min:
            x_min = edge[0][0]

    for y in range(y_min, y_max):
        inside = False 
        for x in range(x_min, x_max):
            if img.pixel(x, y) == crossingColor:
                inside = not inside
                
            if inside:
                img.setPixel(x, y, color)
            else:
                img.setPixel(x, y, backColor)
        if delay:
            redraw()
            time.sleep(0.003)
