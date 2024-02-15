#ifndef CAMERA_H
#define CAMERA_H

#include "object.h"
#include "point.h"

class camera : public invisible_object
{
public:
    camera() = default;
    explicit camera(const point &pos, float width, float height) : pos(pos), x_angle(0), y_angle(0), z_angle(0)
    {
        aspect_ratio = width / height;
        projectionMatrix = Mat4x4f::ProjectionFOV(45, aspect_ratio, 0.1f, 1000.f);
    }
    /*
    Mat4x4f viewMatrix() const
    {
        return Mat4x4f::LookAtLH(position, position + direction, up);
    }
    */

    point get_pos() const;
    void set_pos(const point &_point);

    double get_xangle() const;
    void set_xangle(double angle);

    double get_yangle() const;
    void set_yangle(double angle);

    double get_zangle() const;
    void set_zangle(double angle);

    void accept(const std::shared_ptr<visitor> &_visitor) const override;
    void transform(const point &move, const point &scale, const point &rotate) override;

    float aspect_ratio;
    Mat4x4f projectionMatrix;
private:
    point pos;
    double x_angle;
    double y_angle;
    double z_angle;

    void move(const point &move);
    void rotate(const point &rotate);
};

#endif // CAMERA_H
