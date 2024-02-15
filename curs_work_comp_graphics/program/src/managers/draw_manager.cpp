#include <math.h>
#include "draw_manager.h"
#include "model.h"
#include "camera.h"
#include "composite.h"
#include <QtDebug>
#include <shaders.h>
std::shared_ptr<draw_manager> draw_manager_creator::get_manager()
{
    if (_manager == nullptr)
        create_manager();

    return _manager;
}

void draw_manager_creator::create_manager()
{
    static std::shared_ptr<draw_manager> _manager(new draw_manager());
    this->_manager = _manager;
}

void draw_manager::set_cam(const std::shared_ptr<camera> &_camera)
{
    cur_cam = _camera;
}

void draw_manager::set_drawer(const std::shared_ptr<base_drawer> &_drawer)
{
    this->_drawer = _drawer;
}

void draw_manager::visit(const camera &_camera)
{
}

void draw_manager::visit(const composite &_composite)
{
}

void draw_manager::visit(const scene &_scene)
{
}

void draw_manager::visit(const model &_model)
{
    auto _points = _model.get_units()->get_points();
    qInfo() << cur_cam->get_pos().get_x() << cur_cam->get_pos().get_y() << cur_cam->get_pos().get_z() << "cam pos\n";
    for (point &_point : _points)
    {
        proect_point(_point);
        qInfo()<< _point.get_x() << _point.get_y() << _point.get_z()  << " proection\n";
    }
    auto _edges = _model.get_units()->get_edges();
    for (auto _edge : _edges)
        _drawer->draw_line(_points[_edge.get_first()], _points[_edge.get_second()]);
}

void draw_manager::visit(const model_poligonal &model)
{
    /*
    auto _points = _model.get_units()->get_points();
    qInfo() << cur_cam->get_pos().get_x() << cur_cam->get_pos().get_y() << cur_cam->get_pos().get_z() << "cam pos\n";
    for (point &_point : _points)
    {
        proect_point(_point);
        qInfo()<< _point.get_x() << _point.get_y() << _point.get_z()  << " proection\n";
    }
    auto _edges = _model.get_units()->get_edges();
    for (auto _edge : _edges)
        _drawer->draw_line(_points[_edge.get_first()], _points[_edge.get_second()]);
    */

    auto camera = cur_cam;
    auto projectMatrix = camera->projectionMatrix;
    auto viewMatrix = camera->viewMatrix();

    auto rotation_matrix = model.rotation_matrix;
    auto objToWorld = model.objToWorld();
    for (auto& face: model.faces)
        {

            auto a = vertex_shader->shade(face.a, rotation_matrix, objToWorld, camera);
            auto b = vertex_shader->shade(face.b, rotation_matrix, objToWorld, camera);
            auto c = vertex_shader->shade(face.c, rotation_matrix, objToWorld, camera);

            if (backfaceCulling(a, b, c))
                continue;

            a = geom_shader->shade(a, projectMatrix, viewMatrix);
            b = geom_shader->shade(b, projectMatrix, viewMatrix);
            c = geom_shader->shade(c, projectMatrix, viewMatrix);


            rasterBarTriangle(a, b, c);
        }

}

void draw_manager::proect_point(point &_point)
{
    point move(-cur_cam->get_pos().get_x(), -cur_cam->get_pos().get_y(), 0);

    _point.move(move);

    point center(0, 0, 0);
    point rotate(-cur_cam->get_xangle(), -cur_cam->get_yangle(), -cur_cam->get_zangle());
    _point.rotate(center, rotate);

//    double eps = 1e-10;
//    double dist = cur_cam->get_pos().get_z() + _point.get_z();
//
//    if (fabs(dist) < eps)
//        dist = eps;
//
//    double dist_coef = cur_cam->get_pos().get_z() / dist;
//    _point.set_x(_point.get_x() * dist_coef);
//    _point.set_y(_point.get_y() * dist_coef);
}
