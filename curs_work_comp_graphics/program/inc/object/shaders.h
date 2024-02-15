#ifndef SHADERS_H
#define SHADERS_H

#include <vertex.h>
#include <camera.h>
#include <point.h>
template <typename T, typename U, typename V>
inline T Clamp(T val, U low, V high)
{
    if (val < low)
        return low;
    if (val > high)
        return high;
    return val;
}

inline float GammaCorrect(float value)
{
    if (value <= 0.0031308f)
    {
        return 12.92f * value;
    }
    return 1.055f * std::pow(value, (1.f / 2.4f)) - 0.055f;
}


class PixelShaderInterface{
public:
    virtual point shade(const Vertex& a, const Vertex& b, const Vertex&c, const point& bary) = 0;
    virtual ~PixelShaderInterface(){}
};

class VertexShaderInterface{
public:
    virtual Vertex shade(const Vertex &a,
                         const Mat4x4f& rotation,
                         const Mat4x4f& objToWorld,
                         const camera& cam) = 0;
    virtual ~VertexShaderInterface(){}

};

class GeometryShaderInterface{
public:
    virtual Vertex shade(const Vertex &a,
                         const Mat4x4f& projectMatrix, const Mat4x4f& camView) = 0;
    virtual ~GeometryShaderInterface(){}
};

class VertexShader: public VertexShaderInterface{
public:
    VertexShader(const point& dir_ = {0.f, 0.f, 1.f},
                 const point& diff_ = {0.8f, 0.8f, 0.8f},
                 const point& ambient_ = {0.3f, 0.3f, 0.3f}):
        dir{dir_}, light_color{diff_}, ambient{ambient_}{}
    Vertex shade(const Vertex &a,
                 const Mat4x4f& rotationMatrix,
                 const Mat4x4f& objToWorld,
                 const camera& cam) override;
    ~VertexShader() override{}

    void set_light_color(const point &color)
    {
        this->light_color = color;
    }
private:
    point dir;
    point light_color;
    point ambient;
    float intensity = 1.f;
};

#endif // SHADERS_H
