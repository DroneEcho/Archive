#ifndef BARYCENTRIC_H
#define BARYCENTRIC_H

#include "point.h"

float interPolateCord(float val1, float val2, float val3, const point& bary);

point baryCentricInterpolation(const point& a, const point& b, const point& c, const point& bary);

float calcBar(point a, point b, point p);

point toBarycentric(point a, point b, point c, point p);


#endif // BARYCENTRIC_H
