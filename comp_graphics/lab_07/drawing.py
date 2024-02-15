from PyQt5.QtGui import *
from math import sin, cos, sqrt, ceil, pi
import time


def rnd(x):
    return int(x + 0.5)


def GetPointCode(p, cutter):
    code = 0
    
    if p[0] < cutter[0]:
        code += 1
    if p[0] > cutter[1]:
        code += 2
    if p[1] < cutter[2]:
        code += 4
    if p[1] > cutter[3]:
        code += 8

    return code


def Crop(segments, rect):
    cutter = [rect[0][0], rect[1][0], rect[0][1], rect[1][1]]
    if cutter[0] > cutter[1]:
        cutter[0], cutter[1] = cutter[1], cutter[0]
    if cutter[2] > cutter[3]:
        cutter[2], cutter[3] = cutter[3], cutter[2]

    res = []    

    for constSeg in segments:
        seg = [[constSeg[0][0], constSeg[0][1]],
                [constSeg[1][0], constSeg[1][1]]]
        
        vertical = True
        if seg[0][0] != seg[1][0]:
            vertical = False
            m = (seg[0][1] - seg[1][1]) / (seg[0][0] - seg[1][0])
            
        p1 = GetPointCode(seg[0], cutter)
        p2 = GetPointCode(seg[1], cutter)

        f1 = p1 & p2 # отрезок вне окна
        f2 = not (p1 | p2) # отрезок полностью видим
        
        while not f1 and not f2:
            if p1 == 0:
                seg[0], seg[1] = seg[1], seg[0]
                p1, p2 = p2, p1

            if p1 & 1:
                seg[0][1] += rnd(m * (cutter[0] - seg[0][0]))
                seg[0][0] = cutter[0]
            if p1 & 2:
                seg[0][1] += rnd(m * (cutter[1] - seg[0][0]))
                seg[0][0] = cutter[1]
            if p1 & 4:
                seg[0][0] += rnd((cutter[2] - seg[0][1]) / m)
                seg[0][1] = cutter[2]
            if p1 & 8:
                seg[0][0] += rnd((cutter[3] - seg[0][1]) / m)
                seg[0][1] = cutter[3]

            p1 = GetPointCode(seg[0], cutter)
            p2 = GetPointCode(seg[1], cutter)
            f1 = p1 & p2 # отрезок вне окна
            f2 = not (p1 | p2) # отрезок полностью видим

        if f2:
            res.append(seg)

    return res
