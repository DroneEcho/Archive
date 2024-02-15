from algs import *
from algs_ellipse import *
import enum
import math


class AlgName(enum.Enum):
    canon = (0, 'Каноническое ур.')
    param = (1, 'Параметрическое ур.')
    brs = (2, 'Брезенхем')
    mid = (3, 'Алг. средней точки')
    lib = (5, 'Библиотечный')

    def __init__(self, id_, title):
        self.id_ = id_
        self.title = title


def draw_single_circle(img, xc, yc, r, color, alg):
    if alg == AlgName.canon.title:
        DrawCanon(img, xc, yc, r, color)

    elif alg == AlgName.param.title:
        DrawParam(img, xc, yc, r, color)

    elif alg == AlgName.brs.title:
        DrawBresenham(img, xc, yc, r, color)

    elif alg == AlgName.mid.title:
        DrawMidPoint(img, xc, yc, r, color)
        
    elif alg == AlgName.lib.title:
        DrawLib(img, xc, yc, r, color)


def draw_spector(img, xc, yc, r1, r2, step, color, alg):
    for r in range(r1, r2, step):
        draw_single_circle(img, xc, yc, r, color, alg)

def draw_single_ellipse(img, xc, yc, a, b, color, alg):
    if alg == AlgName.canon.title:
        DrawCanonEllipse(img, xc, yc, a, b, color)

    elif alg == AlgName.param.title:
        DrawParamEllipse(img, xc, yc, a, b, color)

    elif alg == AlgName.brs.title:
        DrawBresenhamEllipse(img, xc, yc, a, b, color)

    elif alg == AlgName.mid.title:
        DrawMidPointEllipse(img, xc, yc, a, b, color)
        
    elif alg == AlgName.lib.title:
        DrawLibEllipse(img, xc, yc, a, b, color)


def draw_spector_ellipse(img, xc, yc, a1, b1, a2, b2, qty, color, alg):
    da = (a2 - a1) / (qty - 1)
    db = (b2 - b1) / (qty - 1)

    for i in range(qty):
        draw_single_ellipse(img, xc, yc, a1, b1, color, alg)

        a1 = int(a1 + da)
        b1 = int(b1 + db)
