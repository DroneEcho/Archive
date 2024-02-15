#include "model.h"
#include <QtDebug>
#include "OBJ_loader.h"
#include "point.h"
#include "barycentric.h"
const float eps_intersect = std::numeric_limits<float>::epsilon();

model::model()
    :_units(new units)
{
}

model::model(const std::shared_ptr<units> &_units)
    :_units(_units)
{
}

std::shared_ptr<units> model::get_units() const
{
    return _units;
}

void model::accept(const std::shared_ptr<visitor> &_visitor) const
{
    _visitor->visit(*this);
}

void model::transform(const point &move, const point &scale, const point &rotate)
{
    _units->transform(move, scale, rotate);
}

std::shared_ptr<units> model_poligonal::get_units() const
{
    return _units;
}

void model_poligonal::accept(const std::shared_ptr<visitor> &_visitor) const
{
    _visitor->visit(*this);
}


void model_poligonal::transform(const point &move, const point &scale, const point &rotate)
{
    _units->transform(move, scale, rotate);
}


model_poligonal::model_poligonal(const std::string& fileName, uint32_t uid_,  int n_, const point& scale, const point& position){
    if (fileName == "")  return;
    uid = uid_;
    objl::Loader loader;
    bool l = loader.LoadFile(fileName);
    qDebug() <<"mean = " << l;
    color = {0.5, 0.5, 0.5};
    for (size_t i = 0; i < loader.LoadedMeshes.size(); ++i){
        objl::Mesh curMesh = loader.LoadedMeshes[i];
        for (size_t j = 0; j < curMesh.Vertices.size(); j++)
        {
            vertex_buffer.push_back(Vertex{
                                   point{curMesh.Vertices[j].Position.X , curMesh.Vertices[j].Position.Y, curMesh.Vertices[j].Position.Z},
                                   point{curMesh.Vertices[j].Normal.X,  curMesh.Vertices[j].Normal.Y, curMesh.Vertices[j].Normal.Z},
                                   curMesh.Vertices[j].TextureCoordinate.X, curMesh.Vertices[j].TextureCoordinate.Y,
                                   color
                               });
        }

        for (size_t j = 0; j < curMesh.Indices.size(); j++ )
            index_buffer.push_back(curMesh.Indices[j]);
    }

    // create faces
    for (uint i = 0; i < this->index_buffer.size() / 3; i++)
    {

        faces.push_back(
        {this->vertex_buffer[this->index_buffer[3 * i]],
                    this->vertex_buffer[this->index_buffer[3 * i + 1]],
                    this->vertex_buffer[this->index_buffer[3 * i + 2]]});
        auto& f = faces.back();
        f.normal = point::cross(f.b.pos - f.a.pos, f.c.pos - f.a.pos);
    }

    qDebug() << "size = " << faces.size();
    scale_x = scale.get_x();
    scale_y = scale.get_y();
    scale_z = scale.get_z();

    shift_x = position.get_x();
    shift_y = position.get_y();
    shift_z = position.get_z();

    n = n_;

}

Vertex transform_position(const Vertex& v, const Mat4x4f& objToWorld, const Mat4x4f& rotationMatrix){
    point4 res(v.pos);
    res = res * objToWorld;
    Vertex out = v;
    point4 normal(out.normal);
    normal = normal * rotationMatrix;
    out.normal = {normal.get_x(), normal.get_y(), normal.get_z()};
    out.pos = point(res.get_x(), res.get_y(), res.get_z());
    return out;
}

bool model_poligonal::triangleIntersect(const Face& face, const Ray &ray, const Mat4x4f &objToWorld, const Mat4x4f &rotMatrix, InterSectionData &data){
    auto p0 = transform_position(face.a, objToWorld, rotMatrix);
    auto p1 = transform_position(face.b, objToWorld, rotMatrix);
    auto p2 = transform_position(face.c, objToWorld, rotMatrix);

    auto edge1 = p1.pos - p0.pos;
    auto edge2 = p2.pos - p0.pos;

    auto h = point::cross(ray.direction, edge2);
    auto a = point::dot(edge1, h);

    bool intersected = false;

    if (fabs(a) < eps_intersect)
        return intersected;

    auto f = 1.f / a;
    auto s = ray.origin - p0.pos;

    auto u = f * point::dot(s, h);

    if (u < 0.f || u > 1.f)
        return intersected;

    auto q = point::cross(s, edge1);

    auto v = f * point::dot(ray.direction, q);

    if (v < 0.f || u + v > 1.f)
        return intersected;

    double t = f * point::dot(edge2, q);

    if (t > 0){
        auto bary = point{1 - u - v, u, v};
        data.pointer = ray.origin + ray.direction * t;
        data.normal = baryCentricInterpolation(p0.normal, p1.normal, p2.normal, bary).normalize();
        data.t = t;
        intersected = true;
        if (this->has_texture){
            float pixel_u = interPolateCord(p0.u , p1.u, p2.u, bary);
            float pixel_v = interPolateCord(p0.v, p1.v, p2.v, bary);

            int x = std::floor(pixel_u * (texture.width()) - 1);
            int y = std::floor(pixel_v * (texture.height() - 1));

            if (x < 0) x = 0;
            if (y < 0) y = 0;

            auto color = texture.pixelColor(x, y);
            auto red = (float)color.red();
            auto green = (float)color.green();
            auto blue = (float)color.blue();
            data.color = point{red / 255.f,
                    green/ 255.f ,
                    blue /255.f};

        }else{
            data.color = baryCentricInterpolation(p0.color, p1.color, p2.color, bary);
        }
    }
    return intersected;
}

bool model_poligonal::intersect(const Ray &ray, InterSectionData &data){

    if (!this->box.intersect(ray)) return false;

    float model_dist = std::numeric_limits<float>::max();

    bool intersected = false;

    auto objToWorld = this->objToWorld();
    auto rotMatrix = this->rotation_matrix;
    InterSectionData d;
    for (auto& face: faces){
        if (triangleIntersect(face, ray, objToWorld, rotMatrix, d) && d.t < model_dist){
            model_dist = d.t;
            data = d;
            intersected = true;
        }
    }

    return intersected;
}


void model_poligonal::genBox(){
    float inf = std::numeric_limits<float>::infinity();
    //const float eps_box = 1e-5;
    point min = {inf, inf, inf};
    point max = {-inf, -inf, -inf};

    for (auto &v : vertex_buffer){
        point4 tmp(v.pos);
        tmp = tmp * this->objToWorld();
        if (tmp.get_x() < min.get_x())
            min.set_x(tmp.get_x());
        if (tmp.get_y() < min.get_y())
            min.set_y(tmp.get_y());
        if (tmp.get_z() < min.get_z())
            min.set_z(tmp.get_z());

        if (tmp.get_x() > max.get_x())
            max.set_x(tmp.get_x());
        if (tmp.get_y() > max.get_y())
            max.set_y(tmp.get_y());
        if (tmp.get_z() > max.get_z())
            max.set_z(tmp.get_z());
    }

    this->box = BoundingBox(min, max);

}
