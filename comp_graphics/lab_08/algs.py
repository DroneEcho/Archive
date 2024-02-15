from PyQt5.QtGui import *
from math import sin, cos, sqrt, ceil, pi
import time


def rnd(x):
    return int(x + 0.5)


def getNormal(seg):
    return [seg[1][1] - seg[0][1], 
            seg[0][0] - seg[1][0]]


def getVector(seg):
    return [seg[1][0] - seg[0][0],
            seg[1][1] - seg[0][1]]


def getProduct(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def CheckConvex(polygon):
    prev = 0
    
    for i in range(len(polygon) - 1):
        x1 = polygon[i][1][0] - polygon[i][0][0]
        y1 = polygon[i][1][1] - polygon[i][0][1]
        x2 = polygon[i + 1][1][0] - polygon[i + 1][0][0]
        y2 = polygon[i + 1][1][1] - polygon[i + 1][0][1]

        z = x1 * y2 - y1 * x2

        if prev * z < 0:
            raise Exception()
        else:
            prev = z

    if prev == 0:
        raise Exception()

    return -prev


def Crop(segs, cutter):
    direction = CheckConvex(cutter)
    if direction < 0:
        for c in cutter:
            c[0], c[1] = c[1], c[0]

    newsegs = []
    normals = [getNormal(c) for c in cutter]

    for seg in segs:
        visible = True
        t0, t1 = 0, 1

        for i in range(len(cutter)):
            n = normals[i]
            q = getVector([cutter[i][0], seg[0]])
            p = getVector(seg)

            pi = getProduct(n, p)
            qi = getProduct(n, q)
                
            if pi == 0:
                if qi < 0:
                    visible = False
                    break

            else:
                t = - qi / pi

                if pi > 0:
                    if t > 1:
                        visible = False
                        break
                    t0 = max(t0, t)

                else:
                    if t < 0:
                        visible = False
                        break
                    t1 = min(t1, t)

        if visible and t1 > t0:
            x1 = rnd(seg[0][0] + (seg[1][0] - seg[0][0]) * t0)
            y1 = rnd(seg[0][1] + (seg[1][1] - seg[0][1]) * t0)
            x2 = rnd(seg[0][0] + (seg[1][0] - seg[0][0]) * t1)
            y2 = rnd(seg[0][1] + (seg[1][1] - seg[0][1]) * t1)
            newsegs.append( [[x1, y1], [x2, y2]] )

    return newsegs
