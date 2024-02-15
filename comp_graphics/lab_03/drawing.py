from algs import *
import enum
import math


class AlgName(enum.Enum):
    cda = (0, 'ЦДА')
    brFloat = (1, 'Брезенхем действ.')
    brInt = (2, 'Брезенхем цел.')
    brSmooth = (3, 'Брезенхем с устр. ступ.')
    vu = (4, 'Ву')
    lib = (5, 'Библиотечный')

    def __init__(self, id_, title):
        self.id_ = id_
        self.title = title


def draw_single_section(img, x1, y1, x2, y2, color, alg):
    x1, y1, x2, y2 = rnd(x1), rnd(y1), rnd(x2), rnd(y2)

    if alg == AlgName.cda.title:
        DrawCDA(img, x1, y1, x2, y2, color)
        
    elif alg == AlgName.brFloat.title:
        DrawBresenhamFloat(img, x1, y1, x2, y2, color)
        
    elif alg == AlgName.brInt.title:
        DrawBresenhamInt(img, x1, y1, x2, y2, color)
    
    elif alg == AlgName.brSmooth.title:
        DrawBresenhamSmooth(img, x1, y1, x2, y2, color, 5)

    elif alg == AlgName.vu.title:
        DrawVu(img, x1, y1, x2, y2, color)
        
    elif alg == AlgName.lib.title:
        DrawLib(img, x1, y1, x2, y2, color)


def draw_sections_series(img, xc, yc, length, angle, color, alg):
    a = 0

    while a < math.pi * 2:
        x = xc + length * math.cos(a)
        y = yc - length * math.sin(a)

        draw_single_section(img, xc, yc, x, y, color, alg)
        a += angle
