def rnd(x):
    return int(x + 0.5)


def TestCDA(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        # set_pixel(img, x1, y1, color, 1)
        return
    
    l = max(abs(x2 - x1), abs(y2 - y1))

    dx = (x2 - x1) / l
    dy = (y2 - y1) / l

    x = x1
    y = y1
    
    # set_pixel(img, x, y, color, 1)

    for i in range(l):
        x += dx
        y += dy
        # set_pixel(img, x, y, color, 1)
    

def TestBresenhamFloat(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        # set_pixel(img, x1, y1, color, 1)
        return

    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1 if dx < 0 else 0
    sy = 1 if dy > 0 else -1 if dy < 0 else 0

    dx = abs(dx)
    dy = abs(dy)
    
    # set_pixel(img, x1, y1, color, 1)
    
    if dy > dx:
        m = dx / dy
        f = m - 0.5
        x = x1
        
        for y in range(y1 + sy, y2 + sy, sy):
            if f > 0:
                x += sx
                f -= 1
            f += m
            # set_pixel(img, x, y, color, 1)
    else:
        m = dy / dx
        f = m - 0.5
        y = y1
        
        for x in range(x1 + sx, x2 + sx, sx):
            if f > 0:
                y += sy
                f -= 1
            f += m
            # set_pixel(img, x, y, color, 1)


def TestBresenhamInt(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        # set_pixel(img, x1, y1, color, 1)
        return

    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1 if dx < 0 else 0
    sy = 1 if dy > 0 else -1 if dy < 0 else 0

    dx = abs(dx)
    dy = abs(dy)

    dx2 = 2 * dx
    dy2 = 2 * dy
    
    # set_pixel(img, x1, y1, color, 1)
    
    if dy > dx:
        f = dx2 - dy
        x = x1
        
        for y in range(y1 + sy, y2 + sy, sy):
            if f > 0:
                x += sx
                f -= dy2
            f += sx
            # set_pixel(img, x, y, color, 1)
    else:
        f = dy2 - dx
        y = y1
        
        for x in range(x1 + sx, x2 + sx, sx):
            if f > 0:
                y += sy
                f -= dx2
            f += sy
            # set_pixel(img, x, y, color, 1)


def TestBresenhamSmooth(x1, y1, x2, y2, n):
    if x1 == x2 and y1 == y2:
        # set_pixel(img, x1, y1, color, 1)
        return

    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1 if dx < 0 else 0
    sy = 1 if dy > 0 else -1 if dy < 0 else 0

    dx = abs(dx)
    dy = abs(dy)
    
    # col = QColor(color.red(), color.green(), color.blue()) 
    # set_pixel(img, x1, y1, col, 1)
    
    if dy > dx:
        m = n * dx / dy
        w = n - m
        f = n / 2
        x = x1
        
        for y in range(y1 + sy, y2 + sy, sy):
            if f > w:
                x += sx
                f -= w
            f += m

            # set_pixel(img, x, y, col, f / n)
    else:
        m = n * dy / dx
        w = n - m
        f = n / 2
        y = y1
        
        for x in range(x1 + sx, x2 + sx, sx):
            if f > w:
                y += sy
                f -= w
            f += m
                
            # set_pixel(img, x, y, col, f / n)


def TestVu(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        img.setPixel(x1, y1, color.rgb())
        return

    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1 if dx < 0 else 0
    sy = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx == 0:
        for y in range(y1, y2, sy):
            None # set_pixel(img, x1, y, color, 1)
    if dy == 0:
        for x in range(x1, x2, sx):
            None # set_pixel(img, x, y1, color, 1)

    dx = abs(dx)
    dy = abs(dy)
    
    # col = QColor(color.red(), color.green(), color.blue(), 255)
    # set_pixel(img, x1, y1, col, 1) 
    
    if dy > dx:
        m = dx / dy
        f = m
        x = x1
        
        for y in range(y1 + sy, y2 + sy, sy):
            if f > 1:
                x += sx
                f -= 1
            
            # set_pixel(img, x, y, col, 1 - f)
            # set_pixel(img, x + sx, y, col, f)
            
            f += m

    else:
        m = dy / dx
        f = m
        y = y1
        
        for x in range(x1 + sx, x2 + sx, sx):
            if f > 1:
                y += sy
                f -= 1
            
            # set_pixel(img, x, y, col, 1 - f)
            # set_pixel(img, x, y + sy, col, f)
            
            f += m
