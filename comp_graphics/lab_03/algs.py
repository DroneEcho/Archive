from PyQt5.QtGui import *
from math import ceil


def rnd(x):
    return int(x + 0.5)


def set_pixel(img, x, y, color, intensity):
    if 0 <= x < img.width() and 0 <= y < img.height():
        alpha = rnd(255 * intensity)
        if alpha != 0:
            color.setAlpha(alpha)
            img.setPixel(rnd(x), rnd(y), color.rgba())


def update_max(xflag, x_p, y_p, x, y, max_step):
    if xflag:
        if rnd(y) != y_p:
            max_step = max(max_step, abs(rnd(x) - x_p))
            x_p = rnd(x)
            y_p = rnd(y)
    else:
        if rnd(x) != x_p:
            max_step = max(max_step, abs(rnd(y) - y_p))
            x_p = rnd(x)
            y_p = rnd(y)
    
    return x_p, y_p, max_step


def DrawCDA(img, x1, y1, x2, y2, color):
    if x1 == x2 and y1 == y2:
        set_pixel(img, x1, y1, color, 1)
        return
    
    l = max(abs(x2 - x1), abs(y2 - y1))

    dx = (x2 - x1) / l
    dy = (y2 - y1) / l

    x = x1
    y = y1
    
    set_pixel(img, x, y, color, 1)

    max_step = 0
    step_flag = abs(x2 - x1) > abs(y2 - y1)
    x_p = x1
    y_p = y1

    for i in range(l):
        x += dx
        y += dy
        set_pixel(img, x, y, color, 1)

        x_p, y_p, max_step = update_max(step_flag, x_p, y_p, x, y, max_step)

    return max_step  

def DrawBresenhamFloat(img, x1, y1, x2, y2, color):
    if x1 == x2 and y1 == y2:
        set_pixel(img, x1, y1, color, 1)
        return

    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1 if dx < 0 else 0
    sy = 1 if dy > 0 else -1 if dy < 0 else 0

    dx = abs(dx)
    dy = abs(dy)
    
    set_pixel(img, x1, y1, color, 1)

    max_step = 0
    x_p = x1
    y_p = y1
    
    if dy > dx:
        m = dx / dy
        f = m - 0.5
        x = x1
        
        for y in range(y1 + sy, y2 + sy, sy):
            if f > 1e-8:
                x += sx
                f -= 1
            f += m
            set_pixel(img, x, y, color, 1)
            
            x_p, y_p, max_step = update_max(False, x_p, y_p, x, y, max_step)
    else:
        m = dy / dx
        f = m - 0.5
        y = y1
        
        for x in range(x1 + sx, x2 + sx, sx):
            if f > 1e-8:
                y += sy
                f -= 1
            f += m
            set_pixel(img, x, y, color, 1)

            x_p, y_p, max_step = update_max(True, x_p, y_p, x, y, max_step)

    return max_step

def DrawBresenhamInt(img, x1, y1, x2, y2, color):
    if x1 == x2 and y1 == y2:
        set_pixel(img, x1, y1, color, 1)
        return

    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1 if dx < 0 else 0
    sy = 1 if dy > 0 else -1 if dy < 0 else 0

    dx = abs(dx)
    dy = abs(dy)
    
    set_pixel(img, x1, y1, color, 1)

    max_step = 0
    x_p = x1
    y_p = y1
    
    if dy > dx:
        f = 2 * dx - dy
        x = x1
        
        for y in range(y1 + sy, y2 + sy, sy):
            if f > 0:
                x += sx
                f -= 2 * dy
            f += 2 * dx
            set_pixel(img, x, y, color, 1)
            
            x_p, y_p, max_step = update_max(False, x_p, y_p, x, y, max_step)        
    else:
        f = 2 * dy - dx
        y = y1
        
        for x in range(x1 + sx, x2 + sx, sx):
            if f > 0:
                y += sy
                f -= 2 * dx
            f += 2 * dy
            set_pixel(img, x, y, color, 1)
            
            x_p, y_p, max_step = update_max(True, x_p, y_p, x, y, max_step)

    return max_step

def DrawBresenhamSmooth(img, x1, y1, x2, y2, color, n):
    if x1 == x2 and y1 == y2:
        set_pixel(img, x1, y1, color, 1)
        return

    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1 if dx < 0 else 0
    sy = 1 if dy > 0 else -1 if dy < 0 else 0

    dx = abs(dx)
    dy = abs(dy)
    
    col = QColor(color.red(), color.green(), color.blue()) 
    set_pixel(img, x1, y1, col, 1)

    max_step = 0
    x_p = x1
    y_p = y1
    
    if dy > dx:
        m = n * dx / dy
        w = n - m
        f = n / 2
        x = x1
        
        for y in range(y1 + sy, y2 + sy, sy):
            if f > w:
                x += sx
                f -= w
            else:
                f += m

            set_pixel(img, x, y, col, ceil(f) / n)
            
            x_p, y_p, max_step = update_max(False, x_p, y_p, x, y, max_step)
    else:
        m = n * dy / dx
        w = n - m
        f = n / 2
        y = y1
        
        for x in range(x1 + sx, x2 + sx, sx):
            if f > w:
                y += sy
                f -= w
            else:
                f += m
                
            set_pixel(img, x, y, col, ceil(f) / n)
            
            x_p, y_p, max_step = update_max(True, x_p, y_p, x, y, max_step)

    return max_step

def DrawVu(img, x1, y1, x2, y2, color):
    if x1 == x2 and y1 == y2:
        img.setPixel(x1, y1, color.rgb())
        return

    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1 if dx < 0 else 0
    sy = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx == 0:
        for y in range(y1, y2, sy):
            set_pixel(img, x1, y, color, 1)
    if dy == 0:
        for x in range(x1, x2, sx):
            set_pixel(img, x, y1, color, 1)

    dx = abs(dx)
    dy = abs(dy)
    
    col = QColor(color.red(), color.green(), color.blue(), 255)
    set_pixel(img, x1, y1, col, 1) 

    max_step = 0
    x_p = x1
    y_p = y1
    
    if dy > dx:
        m = dx / dy
        f = m
        x = x1
        
        for y in range(y1 + sy, y2 + sy, sy):
            if f > 1:
                x += sx
                f -= 1
            
            set_pixel(img, x, y, col, 1 - f)
            set_pixel(img, x + sx, y, col, f)
            
            f += m
            
            x_p, y_p, max_step = update_max(False, x_p, y_p, x, y, max_step)

    else:
        m = dy / dx
        f = m
        y = y1
        
        for x in range(x1 + sx, x2 + sx, sx):
            if f > 1:
                y += sy
                f -= 1
            
            set_pixel(img, x, y, col, 1 - f)
            set_pixel(img, x, y + sy, col, f)
            
            f += m
            
            x_p, y_p, max_step = update_max(True, x_p, y_p, x, y, max_step)

    return max_step

def DrawLib(img, x1, y1, x2, y2, color):
    painter = QPainter(img)
    painter.setPen(color)
    painter.drawLine(x1, y1, x2, y2)
