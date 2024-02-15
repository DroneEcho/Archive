#ifndef POINT_H
#define POINT_H

#include <math.h>
#include <limits>

class point
{
public:
    point();
    point(double x, double y, double z);

    double get_x() const;
    void set_x(double x);

    double get_y() const;
    void set_y(double y);

    double get_z() const;
    void set_z(double z);

    void move(const point &move);
    void scale(const point &center, const point &scale);
    void rotate(const point &center, const point &rotate);
    point operator +(const point& vec) const
    {
            return point(this->x + vec.x, this->y + vec.y, this->z + vec.z);
    }
    point operator-() const
    {
            return point(-x, -y, -z);
    }
    point operator-(const point& v) const
    {
        return point(this->x - v.x, this->y - v.y, this->z - v.z);
    };
    point operator *(const double& val) const{
            return point(this->x * val, this->y * val, this->z * val);
        }
    point normalize() const
    {
            double length = len();
            if (fabs(length) < std::numeric_limits<double>::epsilon())
                length = (double)1;
            return point{x/length, y/length, z/length};
    }
    double len() const
    {
            return std::sqrt(x * x + y * y + z * z);
    }
    static double dot(const point&a, const point& b)
    {
            return a.x * b.x + a.y * b.y + a.z * b.z;
    }
    static point cross(const point& a, const point& b)
    {
            return point(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
    }

private:
    double x;
    double y;
    double z;

    void rotate_xy(double angle);
    void rotate_xz(double angle);
    void rotate_yz(double angle);
};

class point4: public point
{
public:

    point4();
    point4(double x, double y, double z, double f);
    point4(const point& v, double w_ = 1.0f): point(v.get_x(), v.get_y(), v.get_z()), f(w_){}

    double get_x() const;
    void set_x(double x);

    double get_y() const;
    void set_y(double y);

    double get_z() const;
    void set_z(double z);

    double get_f() const;
    void set_f(double f);

    void move(const point4 &move);
    void scale(const point4 &center, const point4 &scale);
    void rotate(const point4 &center, const point4 &rotate);
    point4 operator-() const
    {
            return point4(-x, -y, -z, -f);
    }
    point4 operator-(const point4& v) const
    {
        return point4(this->x - v.x, this->y - v.y, this->z - v.z, this->f - v.f);
    };
    double len() const
    {
            return std::sqrt(x * x + y * y + z * z);
    }
    static double dot(const point4&a, const point4& b)
    {
            return a.x * b.x + a.y * b.y + a.z * b.z;
    }
    static point cross(const point4& a, const point4& b)
    {
            return point(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
    }
    point4 operator *(const double& val){
            return point4(this->x * val, this->y * val, this->z * val, this->f * val);
        }

private:
    double x;
    double y;
    double z;
    double f;

    void rotate_xy(double angle);
    void rotate_xz(double angle);
    void rotate_yz(double angle);
};

#include "matrix.h"
#endif // POINT_H
