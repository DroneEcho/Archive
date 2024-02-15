#ifndef PRIMITIVE_H
#define PRIMITIVE_H

#include "point.h"
class Ray
{
    public:

      Ray(const point& origin_, const point& direction_)
        : origin(origin_)
        , direction(direction_.normalize())
      {
          invdirection = {1 / direction.get_x(), 1 / direction.get_y(), 1 / direction.get_z()};
          sign[0] = (invdirection.get_x() < 0);
          sign[1] = (invdirection.get_y() < 0);
          sign[2] = (invdirection.get_z() < 0);
      }
      Ray(const Ray& other)
        : origin(other.origin)
        , direction(other.direction.normalize())
      {}

    public:
      point origin;
      point direction, invdirection;
      int sign[3];
};


class Primitive {
public:
  virtual ~Primitive();

  virtual bool intersect(const Ray& ray) const
  {
    return false;
  }
};


class BoundingBox: public Primitive{
public:
    BoundingBox() = default;
    BoundingBox(const point& min_, const point& max_){
        bounds[0] = min_;
        bounds[1] = max_;
    }
    virtual ~BoundingBox() override;
    virtual bool intersect(const Ray &ray) const override;
private:
    point min;
    point max;
    point bounds[2];
};

#endif // PRIMITIVE_H
