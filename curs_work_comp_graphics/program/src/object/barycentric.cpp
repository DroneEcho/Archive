#include "barycentric.h"
#include "point.h"

float interPolateCord(float val1, float val2, float val3, const point& bary){
    return bary.get_x() * val1 + bary.get_y() * val2 + bary.get_z() * val3;
}

point baryCentricInterpolation(const point& a, const point& b, const point& c, const point& bary)
{
    float_t x = interPolateCord(a.get_x(), b.get_x(), c.get_x(), bary);
    float_t y = interPolateCord(a.get_y(), b.get_y(), c.get_y(), bary);
    float_t z = interPolateCord(a.get_z(), b.get_z(), c.get_z(), bary);
    return {x, y, z};
}

float calcBar(point a, point b, point p){
    return (a.get_y() - b.get_y()) * p.get_x() + (b.get_x() - a.get_x()) * p.get_y() + a.get_x() * b.get_y() - b.get_x() * a.get_y();
}

point toBarycentric(point a, point b, point c, point p){


    float numA = calcBar(c, b, p);
    float numB = calcBar(a, c, p);
    float numC = calcBar(a, b, p);

    float denumA = calcBar(c, b, a);
    float denumB = calcBar(a, c, b);
    float denumC = calcBar(a, b, c);

    auto f = numA / denumA;
    auto s = numB / denumB;
    auto t = numC / denumC;

    return {f, s, t};
}
