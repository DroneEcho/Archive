#include "primitive.h"

#define SIGN(x) (((x) < 0) ? -1 : 1)

Primitive::~Primitive(){}

BoundingBox::~BoundingBox(){}

bool BoundingBox::intersect(const Ray &r) const
{

    float txmin, txmax, tymin, tymax, tzmin, tzmax;

    txmin = (bounds[r.sign[0]].get_x() - r.origin.get_x()) * r.invdirection.get_x();
    txmax = (bounds[1-r.sign[0]].get_x() - r.origin.get_x()) * r.invdirection.get_x();

    tymin = (bounds[r.sign[1]].get_y() - r.origin.get_y()) * r.invdirection.get_y();
    tymax = (bounds[1-r.sign[1]].get_y() - r.origin.get_y()) * r.invdirection.get_y();

    tzmin = (bounds[r.sign[2]].get_z() - r.origin.get_z()) * r.invdirection.get_z();
    tzmax = (bounds[1-r.sign[2]].get_z() - r.origin.get_z()) * r.invdirection.get_z();

    if ((txmin > tymax) || (tymin > txmax))
        return false;
    if (tymin > txmin)
        txmin = tymin;
    if (tymax < txmax)
        txmax = tymax;

    if ((txmin > tzmax) || (tzmin > txmax))
        return false;
    if (tzmin > txmin)
        txmin = tzmin;
    if (tzmax < txmax)
        txmax = tzmax;

    return (SIGN(txmin) == SIGN(txmax));
}
