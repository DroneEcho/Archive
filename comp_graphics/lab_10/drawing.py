from PyQt5.QtGui import *
from math import sin, cos, sqrt, ceil, pi
import numpy as np


def floating_horizon(painter, func, xlims, zlims, angles, display):
    xmin, xmax, xstep = xlims
    zmin, zmax, zstep = zlims
    xarr = np.arange(xmin, xmax, xstep)
    zarr = np.arange(zmax, zmin, -zstep)

    top = [0] * len(xarr)
    bottom = [0] * len(xarr)

    for i in range(len(xarr)):
        top[i] = 0
        bottom[i] = 1000

    nfirst = False

    for z in zarr:        
        # Левое боковое ребро
        y = func(xarr[0], z)
        x, y = rotate_dot(xarr[0], y, z, angles, display)
        if nfirst:
            painter.drawLine(left[0], left[1], x, y)
        left = [x, y]
        
        # Правое боковое ребро
        y = func(xarr[-1], z)
        x, y = rotate_dot(xarr[-1], y, z, angles, display)
        if nfirst:
            painter.drawLine(right[0], right[1], x, y)
        right = [x, y]
        nfirst = True

        visprev = True

        for i in range(len(xarr)):
            y = func(xarr[i], z)
            x, y = rotate_dot(xarr[i], y, z, angles, display)

            if y > top[i] or y < bottom[i]:
                vis = True
            else:
                vis = False
            
            if i > 0:
                if vis and visprev:
                    painter.drawLine(xprev, yprev, x, y)
                elif vis and not visprev:
                    if y > top[i]:
                        xi, yi = intersection(xprev, yprev, x, y, top[i - 1], top[i])
                    else:
                        xi, yi = intersection(xprev, yprev, x, y, top[i - 1], bottom[i])

                    painter.drawLine(xi, yi, x, y)
                elif not vis and visprev:
                    if yprev > top[i]:
                        xi, yi = intersection(xprev, yprev, x, y, top[i - 1], top[i])
                    else:
                        xi, yi = intersection(xprev, yprev, x, y, top[i - 1], bottom[i])

                    painter.drawLine(xi, yi, xprev, yprev)

            top[i] = max(top[i], y)
            bottom[i] = min(bottom[i], y)

            xprev = x
            yprev = y
            visprev = vis


def intersection(x1, y1, x2, y2, arr1, arr2):
    dx = x2 - x1
    dyc = y2 - y1
    dyp = arr2 - arr1
    
    if dx == 0:
        xi = x2
        yi = arr2
        
        return xi, yi
    
    if y1 == arr1 and y2 == arr2:
        return x1, y1
    
    m = dyc / dx
    xi = x1 - round(dx * (y1 - arr1) / (dyc - dyp))
    yi = round((xi - x1) * m + y1)
    
    return xi, yi


def rotate_dot(x, y, z, angles, display):
    x, y = rotate_x(x, y, z, angles[0])
    x, y = rotate_y(x, y, z, angles[1])
    x, y = rotate_z(x, y, z, angles[2])
    
    return (rnd(display[0] + x * display[2]), 
            rnd(display[1] + y * display[2]))


def rotate_x(x, y, z, angle):
    y = cos(angle) * y - sin(angle) * z
    
    return x, y


def rotate_y(x, y, z, angle):
    x = cos(angle) * x - sin(angle) * z
    
    return x, y


def rotate_z(x, y, z, angle):
    temp = x
    с = cos(angle)
    s = sin(angle)
    
    x = с * x - s * y
    y = с * y + s * temp
    
    return x, y


def rnd(x):
    return int(x + 0.5)

