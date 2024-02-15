from PyQt5.QtGui import *
from math import sin, cos, sqrt, ceil, pi


def rnd(x):
    return int(x + 0.5)


def SetPixel(img, x, y, color):
    if 0 <= x and x < img.width() and 0 <= y and y < img.height():
        img.setPixel(x, y, color.rgb())


def Draw8CirclePoints(img, xc, yc, x, y, color):
    x = rnd(x)
    y = rnd(y)

    SetPixel(img, xc + x, yc + y, color)
    SetPixel(img, xc + y, yc + x, color)
    
    SetPixel(img, xc - x, yc + y, color)
    SetPixel(img, xc - y, yc + x, color)
    
    SetPixel(img, xc + x, yc - y, color)
    SetPixel(img, xc + y, yc - x, color)
    
    SetPixel(img, xc - x, yc - y, color)
    SetPixel(img, xc - y, yc - x, color)


def DrawBresenham(img, xc, yc, r, color, draw = True):
    x = 0
    y = r
    d = 2 - r - r
    
    if draw:
        Draw8CirclePoints(img, xc, yc, x, y, color)

    while x < y:
        if d <= 0:
            d1 = d + d + y + y - 1
            x += 1
            if d1 >= 0:
                y -= 1
                d += x + x - y - y + 2 # 2 * (x - y + 1)
            else:
                d += x + x + 1

        else:
            d2 = d + d - x - x - 1 # 2 * (d - x) - 1
            y -= 1
            if d2 < 0:
                x += 1
                d += x + x - y - y + 2 # 2 * (x - y + 1)
            else:
                d -= y + y - 1
                
        if draw:
            Draw8CirclePoints(img, xc, yc, x, y, color)
        

def DrawMidPoint(img, xc, yc, r, color, draw = True):
    x = r
    y = 0
    p = 1 - r
    q = -2 * r + 5

    while x >= y:
        if draw:
            Draw8CirclePoints(img, xc, yc, x, y, color)

        if p < 0:
            p += y + y + 3
            q += 2
        else:
            p += q
            q += 4
            x -= 1

        y += 1


def DrawCanon(img, xc, yc, r, color, draw = True):
    r2 = r * r
    x = 0
    y = r

    while x <= y:
        y = rnd(sqrt(r2 - x * x))
        
        if draw:
            Draw8CirclePoints(img, xc, yc, x, y, color)
        
        x += 1


def DrawParam(img, xc, yc, r, color, draw = True):
    t = 0
    dt = 1 / r
    t_end = pi / 4

    while t <= t_end + dt:
        x = rnd(r * cos(t))
        y = rnd(r * sin(t))
        
        if draw:
            Draw8CirclePoints(img, xc, yc, x, y, color)
        
        t += dt


def DrawLib(img, xc, yc, r, color):
    painter = QPainter(img)
    painter.setPen(color)
    painter.drawEllipse(xc - r, yc - r, r + r, r + r)
