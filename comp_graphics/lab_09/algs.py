from math import sin, cos, sqrt, ceil, pi


def rnd(x):
    return int(x + 0.5)


def getZCrossProduct(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def CheckConvex(p):
    side = 0

    for i in range(len(p) - 1):
        for j in range(len(p)):
            s = checkLocation(p[i], p[i + 1], p[j])
            
            if side * s < 0:
                raise Exception()
            elif s != 0:
                side = s

    return side
    
    '''
    prev = 0
    
    for i in range(len(p) - 2):
        x1 = p[i + 1][0] - p[i][0]
        y1 = p[i + 1][1] - p[i][1]
        x2 = p[i + 2][0] - p[i + 1][0]
        y2 = p[i + 2][1] - p[i + 1][1]

        z = x1 * y2 - y1 * x2

        if prev * z < 0:
            raise Exception()
        else:
            prev = z

    if prev == 0:
        raise Exception()

    return -prev'''

    
def checkLocation(p1, p2, p3):
    return (p3[0] - p1[0]) * (p2[1] - p1[1]) - \
            (p2[0] - p1[0]) * (p3[1] - p1[1]) 


def getIntersection(p1, p2, s1, s2):
    t = ((p2[1] - p1[1]) * (s1[0] - p1[0]) - (p2[0] - p1[0]) * (s1[1] - p1[1])) \
            / ((p2[0] - p1[0]) * (s2[1] - s1[1]) - (p2[1] - p1[1]) * (s2[0] - s1[0]))
    
    x = s1[0] + (s2[0] - s1[0]) * t
    y = s1[1] + (s2[1] - s1[1]) * t

    return x, y


def Crop(polygon, cutter):
    direction = CheckConvex(cutter)
    if direction < 0:
        for i in range(len(cutter) // 2):
            cutter[i], cutter[len(cutter) - i - 1] = cutter[len(cutter) - i - 1], cutter[i] 

    points = [[polygon[i][0], polygon[i][1]] for i in range(len(polygon))]

    for i in range(len(cutter) - 1):
        pnew = []

        for j in range(len(points) - 1):
            p1 = checkLocation(cutter[i], cutter[i + 1], points[j])
            p2 = checkLocation(cutter[i], cutter[i + 1], points[j + 1])

            if p1 < 0 and p2 < 0: # полностью невидим
                continue
            elif p1 >= 0 and p2 >= 0: # полностью видим
                pnew.append(points[j])
            else:
                x, y = getIntersection(points[j], points[j + 1], 
                                        cutter[i], cutter[i + 1])

                if p1 >= 0:
                    pnew.append(points[j])

                pnew.append([rnd(x), rnd(y)])

        if len(pnew) == 0:
            return []

        points = [i for i in pnew]
        points.append(points[0])

    return points
