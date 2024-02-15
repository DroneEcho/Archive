#ifndef VERTEX_H
#define VERTEX_H

#include "point.h"

class Vertex{
public:
    Vertex(point pos_, point normal_, float u_, float v_, point color_ = {0.5, 0.5, 0.5}):
        pos{pos_}, normal{normal_}, color{color_}, u{u_}, v{v_}{}
public:
    point pos, normal, color;
    float u, v;
    float invW = 1.f;
};

#endif // VERTEX_H
