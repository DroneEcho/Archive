#include "scene_manager.h"
#include "bary.h"
#include "texture.h"
#include "geometry_shader.h"
#include <iostream>
#include <QDebug>
#include <chrono>
#include <QFileDialog>
#include <fstream>

#define NDCX_TO_RASTER(ndc_x, width) (((ndc_x + 1.0f) * (width >> 1)))
#define NDCY_TO_RASTER(ndc_y, height) (((1.0f - ndc_y) * (height >> 1)))

void denormolize(int width, int height, Vertex& vert)
{
    vert.pos.x = vert.pos.x * vert.invW;
    vert.pos.y = vert.pos.y * vert.invW;
    vert.pos.z = vert.pos.z * vert.invW;
    vert.pos.x = NDCX_TO_RASTER(vert.pos.x, width);
    vert.pos.y = NDCY_TO_RASTER(vert.pos.y, height);
}


void SceneManager::init()
{
    models.push_back(new Light(Light::light_type::ambient));
    pixel_shader = std::make_shared<ColorShader>();
    vertex_shader = std::make_shared<VertexShader>();
    geom_shader = std::make_shared<GeometryShader>();
    render_all();
}

void SceneManager::render()
{
    this->render_all();
}

void SceneManager::render_all()
{

    img.fill(background_color);

    for (auto& vec: depthBuffer)
        std::fill(vec.begin(), vec.end(), std::numeric_limits<float>::max());

    for (auto& model: models)
    {
        // Если свет - то ничего не делаем
        if (!model->isObject())
        {
            Light* l = dynamic_cast<Light*>(model);
            if (l->t == Light::light_type::ambient)
                continue;
        }
        // Для текстуры или цвета делаем разный шейдер
        if (model->has_texture)
            pixel_shader = std::make_shared<TextureShader>(model->texture);
        else
            pixel_shader = std::make_shared<ColorShader>();
        rasterize(*model);
    }

    show();
}

bool SceneManager::backfaceCulling(const Vertex &a, const Vertex &b, const Vertex &c)
{
    auto cam = camers[curr_camera];

    auto face_normal = Vec3f::cross(b.pos - a.pos, c.pos - a.pos);

    auto res1 = Vec3f::dot(face_normal, a.pos - cam.position);
    auto res2 = Vec3f::dot(face_normal, b.pos - cam.position);
    auto res3 = Vec3f::dot(face_normal, c.pos - cam.position);

    if ((res1 > 0) && (res2 > 0) && (res3 > 0))
        return true;
    return false;
}

bool SceneManager::clip(const Vertex& v){
    const float w = 1 / v.invW;
    return (v.pos.x > -w || fabs(v.pos.x + w) < eps) &&
           (v.pos.x < w || fabs(v.pos.x - w) < eps) &&
           (v.pos.y > -w || fabs(v.pos.y + w) < eps) &&
           (v.pos.y < w || fabs(v.pos.y - w) < eps) &&
           (v.pos.z > 0.f || fabs(v.pos.z) < eps) &&
           (v.pos.z < w || fabs(v.pos.z - w) < eps);
}

void SceneManager::safescene(QString Filename, QStringListModel &model, std::map<QString, uint32_t> &text_uid, std::map<QString, UI_data> &name_data)
{
    auto filepath = "C:\\Users\\Maria\\Desktop\\JUSTDOIT\\curs\\save\\1.dat";
    std::ofstream fout;
    fout.open(filepath, std::ofstream::binary);
    //if (!fout.is_open())
    //    qDebug() << "open file err" << endl;
    //    return;
    qDebug() << "!1";
    for (auto& model: models)
    {
        if (model->isObject())
        {
            fout.write((char*)&model->rotation_matrix, sizeof(Mat4x4f));
            fout.write((char*)&model->scale_matrix, sizeof(Mat4x4f));
            fout.write(reinterpret_cast<char*>(&model->texture), sizeof(QImage));
            fout.write((char*)&model->has_texture, sizeof(bool));
            fout.write((char*)&model->specular, sizeof(float));
            fout.write((char*)&model->reflective, sizeof(float));
            fout.write((char*)&model->refractive, sizeof(float));
            fout.write((char*)&model->transparency, sizeof(float));
            fout.write((char*)&model->n, sizeof(int));
            fout.write((char*)&model->color, sizeof(Vec3f));
            fout.write((char*)&model->box, sizeof(BoundingBox));

            float tmp = model->return_angle_x_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            tmp = model->return_angle_y_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            tmp = model->return_angle_z_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            tmp = model->return_shift_x_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            tmp = model->return_shift_y_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            tmp = model->return_shift_z_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            tmp = model->return_scale_x_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            tmp = model->return_scale_y_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            tmp = model->return_scale_z_for_copy();
            fout.write((char*)&(tmp), sizeof(float));

            uint32_t tmp2 = model->return_uid_for_copy();
            fout.write((char*)&(tmp2), sizeof(float));

            size_t size = model->index_buffer.size();
            size_t size2;
            fout.write((char*)&size, sizeof(size_t));

            for (size_t i = 0; i < size; i++) {
                fout.write((char*)&model->index_buffer[i], sizeof(uint32_t));
                //qDebug() << model->index_buffer[i] << endl;
            }
            size = model->vertex_buffer.size();
            fout.write(reinterpret_cast<char*>(&size), sizeof(size_t));
            for (size_t i = 0; i < size; i++) {
                // Write the size of the string.
                /*
                Vec3f pos, normal, color;
                float u, v;
                float invW = 1.f;
                */
                fout.write((char*)&model->vertex_buffer[i].pos, sizeof(Vec3f));
                fout.write((char*)&model->vertex_buffer[i].normal, sizeof(Vec3f));
                fout.write((char*)&model->vertex_buffer[i].color, sizeof(Vec3f));
                fout.write((char*)&model->vertex_buffer[i].u, sizeof(float));
                fout.write((char*)&model->vertex_buffer[i].v, sizeof(float));
                fout.write((char*)&model->vertex_buffer[i].invW, sizeof(float));
                //fout.write((char*)&model->vertex_buffer[i], sizeof size2);
                //qDebug() << "pos: "<<model->vertex_buffer[i].pos.x << model->vertex_buffer[i].pos.y << \
                //            model->vertex_buffer[i].pos.z << "normal:" << model->vertex_buffer[i].normal.x <<\
                //            model->vertex_buffer[i].normal.y << model->vertex_buffer[i].normal.z << endl;
            }
            size = model->faces.size();
            fout.write(reinterpret_cast<char*>(&size), sizeof(size_t));
            for (size_t i = 0; i < size; i++) {
                // Write the size of the string.
                /*
                Vertex a, b, c;
                Vec3f normal;
                */
                fout.write((char*)&model->faces[i].a.pos, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].a.normal, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].a.color, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].a.u, sizeof(float));
                fout.write((char*)&model->faces[i].a.v, sizeof(float));
                fout.write((char*)&model->faces[i].a.invW, sizeof(float));

                fout.write((char*)&model->faces[i].b.pos, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].b.normal, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].b.color, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].b.u, sizeof(float));
                fout.write((char*)&model->faces[i].b.v, sizeof(float));
                fout.write((char*)&model->faces[i].b.invW, sizeof(float));

                fout.write((char*)&model->faces[i].c.pos, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].c.normal, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].c.color, sizeof(Vec3f));
                fout.write((char*)&model->faces[i].c.u, sizeof(float));
                fout.write((char*)&model->faces[i].c.v, sizeof(float));
                fout.write((char*)&model->faces[i].c.invW, sizeof(float));

                fout.write((char*)&model->faces[i].normal, sizeof(Vec3f));
                //size2 = sizeof(model->faces[i]);
                //fout.write(reinterpret_cast<char*>(&size), sizeof(size_t));

                //fout.write((char*)&model->faces[i], sizeof size2);
                //qDebug() << sizeof size2 << "- size2(3)";
            }
        }
    }
    //for (auto& m: model)
    //{
    fout.close();
}

void SceneManager::readfile(QString fileName)
{
    auto filepath = fileName.toStdString();
    std::ifstream fout;
    fout.open(filepath, std::ifstream::binary);
    //if (!fout.is_open())
    //    qDebug("open file err");
    //    return;
    Model temp;
    std::vector<uint32_t> index_buffer;
    uint32_t v1_tmp;
    std::vector<Vertex> vertex_buffer;
    Vertex v2_tmp;
    std::vector<Face> faces;
    Face v3_tmp;
    size_t vsize = 0;

    while(fout.read((char*)&temp.rotation_matrix, sizeof(Mat4x4f)))
    {
        //qDebug() << "reading===" << endl;
        fout.read((char*)&temp.scale_matrix, sizeof(Mat4x4f));
        fout.read(reinterpret_cast<char*>(&temp.texture), sizeof(QImage));
        fout.read((char*)&temp.has_texture, sizeof(bool));
        fout.read((char*)&temp.specular, sizeof(float));
        fout.read((char*)&temp.reflective, sizeof(float));
        fout.read((char*)&temp.refractive, sizeof(float));
        fout.read((char*)&temp.transparency, sizeof(float));
        fout.read((char*)&temp.n, sizeof(int));
        fout.read((char*)&temp.color, sizeof(Vec3f));
        fout.read((char*)&temp.box, sizeof(BoundingBox));

        float tmp;
        fout.read((char*)&(tmp), sizeof(float));
        temp.set_angle_x_for_copy(tmp);

        fout.read((char*)&(tmp), sizeof(float));
        temp.set_angle_y_for_copy(tmp);

        fout.read((char*)&(tmp), sizeof(float));
        temp.set_angle_z_for_copy(tmp);

        fout.read((char*)&(tmp), sizeof(float));
        temp.set_shift_x_for_copy(tmp);

        fout.read((char*)&(tmp), sizeof(float));
        temp.set_shift_y_for_copy(tmp);

        fout.read((char*)&(tmp), sizeof(float));
        temp.set_shift_z_for_copy(tmp);

        fout.read((char*)&(tmp), sizeof(float));
        temp.set_scale_x_for_copy(tmp);

        fout.read((char*)&(tmp), sizeof(float));
        temp.set_scale_y_for_copy(tmp);

        fout.read((char*)&(tmp), sizeof(float));
        temp.set_scale_z_for_copy(tmp);


        uint32_t tmp2;
        fout.read((char*)&(tmp2), sizeof(float));
        temp.set_uid_for_copy(tmp2);

        //qDebug() << sizeof(Model) << endl;
        fout.read((char*)&vsize, sizeof(size_t));
        for (size_t i = 0; i < vsize; i++) {
            fout.read((char*)&v1_tmp, sizeof(uint32_t));
            index_buffer.push_back(v1_tmp);
            //qDebug() << v1_tmp << endl;
        }
        fout.read((char*)&vsize, sizeof(size_t));
        for (size_t i = 0; i < vsize; i++) {
            //size_t size = 0;
            //fout.read(reinterpret_cast<char*>(&size), sizeof(size_t));
            fout.read((char*)&v2_tmp.pos, sizeof(Vec3f));
            fout.read((char*)&v2_tmp.normal, sizeof(Vec3f));
            fout.read((char*)&v2_tmp.color, sizeof(Vec3f));
            fout.read((char*)&v2_tmp.u, sizeof(float));
            fout.read((char*)&v2_tmp.v, sizeof(float));
            fout.read((char*)&v2_tmp.invW, sizeof(float));
            //fout.read((char*)&v2_tmp, sizeof size);
            qDebug() << "pos: "<<v2_tmp.pos.x << v2_tmp.pos.y << \
                        v2_tmp.pos.z << "normal:" << v2_tmp.normal.x <<\
                        v2_tmp.normal.y << v2_tmp.normal.z << endl;
            vertex_buffer.push_back(v2_tmp);
        }
        fout.read(reinterpret_cast<char*>(&vsize), sizeof(size_t));
        for (size_t i = 0; i < vsize; i++) {
            //size_t size = 0;
            //fout.read(reinterpret_cast<char*>(&size), sizeof(size_t));

            //fout.read((char*)&v3_tmp, sizeof size);
            //qDebug() << sizeof size << "- size2(3)";
            fout.read((char*)&v3_tmp.a.pos, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.a.normal, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.a.color, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.a.u, sizeof(float));
            fout.read((char*)&v3_tmp.a.v, sizeof(float));
            fout.read((char*)&v3_tmp.a.invW, sizeof(float));

            fout.read((char*)&v3_tmp.b.pos, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.b.normal, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.b.color, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.b.u, sizeof(float));
            fout.read((char*)&v3_tmp.b.v, sizeof(float));
            fout.read((char*)&v3_tmp.b.invW, sizeof(float));

            fout.read((char*)&v3_tmp.c.pos, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.c.normal, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.c.color, sizeof(Vec3f));
            fout.read((char*)&v3_tmp.c.u, sizeof(float));
            fout.read((char*)&v3_tmp.c.v, sizeof(float));
            fout.read((char*)&v3_tmp.c.invW, sizeof(float));

            fout.read((char*)&v3_tmp.normal, sizeof(Vec3f));

            faces.push_back(v3_tmp);
        }
        models.push_back(new Model(temp, index_buffer, vertex_buffer, faces));
        int n = models.size() - 1;
        index_buffer.clear();
        vertex_buffer.clear();
        faces.clear();
    }
    fout.close();
    render_all();
}
void SceneManager::rasterize(Model& model)
{
    auto camera = camers[curr_camera];
    auto projectMatrix = camera.projectionMatrix;
    auto viewMatrix = camera.viewMatrix();

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

#define Min(val1, val2) std::min(val1, val2)
#define Max(val1, val2) std::max(val1, val2)
void SceneManager::rasterBarTriangle(Vertex p1_, Vertex p2_, Vertex p3_)
{
    if (!clip(p1_) && !clip(p2_) && !clip(p3_))
    {
        return;
    }

    denormolize(width, height, p1_);
    denormolize(width, height, p2_);
    denormolize(width, height, p3_);

    auto p1 = p1_.pos;
    auto p2 = p2_.pos;
    auto p3 = p3_.pos;

    float sx = std::floor(Min(Min(p1.x, p2.x), p3.x));
    float ex = std::ceil(Max(Max(p1.x, p2.x), p3.x));

    float sy = std::floor(Min(Min(p1.y, p2.y), p3.y));
    float ey = std::ceil(Max(Max(p1.y, p2.y), p3.y));

    for (int y = static_cast<int>(sy); y < static_cast<int>(ey); y++)
    {
        for (int x = static_cast<int>(sx); x < static_cast<int>(ex); x++)
        {
            Vec3f bary = toBarycentric(p1, p2, p3, Vec3f(static_cast<float>(x), static_cast<float>(y)));
            if ( (bary.x > 0.0f || fabs(bary.x) < eps) && (bary.x < 1.0f || fabs(bary.x - 1.0f) < eps) &&
                 (bary.y > 0.0f || fabs(bary.y) < eps) && (bary.y < 1.0f || fabs(bary.y - 1.0f) < eps) &&
                 (bary.z > 0.0f || fabs(bary.z) < eps) && (bary.z < 1.0f || fabs(bary.z - 1.0f) < eps))
            {
                auto interpolated = baryCentricInterpolation(p1, p2, p3, bary);
                interpolated.x = x;
                interpolated.y = y;
                if (testAndSet(interpolated))
                {
                    // Рисуем
                    auto pixel_color = pixel_shader->shade(p1_, p2_, p3_, bary) * 255.f;
                    img.setPixelColor(x, y, qRgb(pixel_color.x, pixel_color.y, pixel_color.z));
                }
            }
        }
    }

}

bool SceneManager::testAndSet(const Vec3f& p)
{
    int x = std::round(p.x), y = std::round(p.y);
    if (x >= width || y >= height || x < 0 || y < 0)
        return false;
    if (p.z < depthBuffer[x][y] || fabs(p.z - depthBuffer[x][y]) < eps)
    {
        depthBuffer[x][y] = p.z;
        return true;
    }
    return false;
}


void SceneManager::showTracedResult()
{
    for (auto& th: threads)
    {
        th->wait();
        delete th;
    }
    threads.clear();
    this->show();
}

void SceneManager::show()
{
    scene->clear();
    scene->addPixmap(QPixmap::fromImage(img));
}

float check_shift(float curr, float target)
{
    return curr > target ? -1.f : 1.f;
}

void SceneManager::shift(trans_type t, float val)
{
    switch (t)
    {
        case shift_x:
            models[current_model]->shiftX(val);
            break;
        case shift_y:
            models[current_model]->shiftY(val);
            break;
        case shift_z:
            models[current_model]->shiftZ(val);
            break;
        default:
            return;
    }

    render_all();
}

void SceneManager::rotate(trans_type t, float angle){
    switch (t)
    {
        case rot_x:
            models[current_model]->rotateX(angle);
            break;
        case rot_y:
            models[current_model]->rotateY(angle);
            break;
        case rot_z:
            models[current_model]->rotateZ(angle);
            break;
        default:
            return;
    }

    render_all();
}

void SceneManager::scale(trans_type t, float factor)
{
    switch (t)
    {
        case scale_x:
            models[current_model]->scaleX(factor);
            break;
        case scale_y:
            models[current_model]->scaleY(factor);
            break;
        case scale_z:
            models[current_model]->scaleZ(factor);
            break;
        default:
            return;
    }

    render_all();
}

void SceneManager::addCamera()
{
    camera_count++;
    camers.push_back(Camera(width, height));
    curr_camera = camera_count - 1;
    render_all();
}

void SceneManager::setCamera(int index)
{
    curr_camera = index;
    render_all();
}
void SceneManager::deleteCamera(int index)
{
    camera_count--;
    camers.erase(camers.begin() + index);
    render_all();
}

void SceneManager::moveCamera(trans_type t, float dist)
{
    auto& cam = camers[curr_camera];
    std::function<void ()> change_func;
    switch (t)
    {
    case shift_x:
        change_func = [&]()
        {
            cam.shiftX(dist);
        };
        break;
    case shift_y:
        change_func = [&]()
        {
            cam.shiftY(dist);
        };
        break;
    case shift_z:
        change_func = [&]()
        {
            cam.shiftZ(dist);
        };
        break;
    case rot_x:
        change_func = [&]()
        {
            cam.rotateX(dist);
        };
        break;
    case rot_y:
        change_func = [&]()
        {
            cam.rotateY(dist);
        };
        break;
    case rot_z:
        change_func = [&]()
        {
            cam.rotateZ(dist);
        };
        break;
    case up_y:
        change_func = [&]()
        {
            cam.shiftY(dist);
        };
        break;
    case down_y:
        change_func = [&]()
        {
            cam.shiftY(dist);
        };
        break;
    default:
        return;
    }

    change_func();
    render_all();
}

void SceneManager::uploadModel(std::string name, uint32_t& uid)
{

    const std::map<std::string, std::string> files =
    {
        //C:\Users\Maria\Desktop\JUSTDOIT\curs\models
        {"Куб", "C:\\Users\\Maria\\Desktop\\JUSTDOIT\\curs\\models\\cube_new.obj"},
        {"Сфера", "C:\\Users\\Maria\\Desktop\\JUSTDOIT\\curs\\models\\sphere_new.obj"},
        {"Цилиндр", "C:\\Users\\Maria\\Desktop\\JUSTDOIT\\curs\\models\\cylinder1.obj"},
        {"Параллелепипед", "C:\\Users\\Maria\\Desktop\\JUSTDOIT\\curs\\models\\parallepiped.obj"},
        {"Конус", "C:\\Users\\Maria\\Desktop\\JUSTDOIT\\curs\\models\\conus1.obj"}
    };


    const std::map<std::string, int> n_power =
    {
        {"Куб", 12},
        {"Сфера", 20},
        {"Цилиндр", 512},
        {"Параллелепипед", 12},
        {"Конус", 512}
    };

    if (!files.count(name))

        return;

    uid = models_index++;
    models.push_back(new Model(files.at(name), uid, n_power.at(name)));

    render_all();
}

void SceneManager::uploadLight(std::string name, uint32_t &uid, Vec3f &color)
{
    if (this->count_light == 1)
    {
        return;
    }
    else
    {
        this->count_light = 1;
    }
    const std::map<std::string, std::string> files =
    {
        {"Точечный источник", "C:\\Users\\Maria\\Desktop\\JUSTDOIT\\curs\\models\\icosphere.obj"},
    };

    if (!files.count(name))
        return;

    uid = models_index++;
    if (name == "Точечный источник")
    {
        models.push_back(new Light(Light::light_type::point, color, pointLightPosition,
                                   1, {0.2f, 0.2f, 0.2f}, files.at(name), uid, {0.2f, 0.2f, 0.2f}));
    }

    render_all();
}

void SceneManager::removeAll()
{
    models.erase(models.begin(), models.end());
    render_all();
}

void SceneManager::removeModel()
{
    if (!models[current_model]->isObject())
        count_light = 0;
    models.erase(models.begin() + current_model);
    render_all();
}

void SceneManager::setCurrentModel(uint32_t uid)
{
    auto it = models.begin();
    int i = 0;
    for (; it <  models.end(); it++, i++)
        if ((*it)->getUid() == uid)
            break;
    current_model = i;
}

void SceneManager::setColor(const Vec3f &color)
{
    models[current_model]->setColor(color);
    render_all();
}

void SceneManager::setLightColor(const Vec3f &color)
{
    for (auto& model: models)
    {
        if (!model->isObject())
        {
            Light* l = dynamic_cast<Light*>(model);
            if (l->t != Light::light_type::ambient)
                l->setLightColor(color);
        }
    }
    render_all();
}

void SceneManager::setAmbientLightColor(const Vec3f &color)
{
    for (auto& model: models)
    {
        if (!model->isObject())
        {
            Light* l = dynamic_cast<Light*>(model);
            if (l->t == Light::light_type::ambient)
                l->setLightColor(color);
        }
    }
    render_all();
}

void SceneManager::setTexture(const QImage &img)
{
    models[current_model]->has_texture = true;
    models[current_model]->setColor(Vec3f{1.f, 1.f, 1.f});
    models[current_model]->texture = img;
    render_all();
}

void SceneManager::setFlagTexture(bool flag, const Vec3f& color)
{
    models[current_model]->has_texture = flag;
    models[current_model]->setColor(color);
    render_all();
}

void SceneManager::setSpecular(float val)
{
    models[current_model]->specular = val;
    render_all();
}

void SceneManager::setReflective(float val)
{
    models[current_model]->reflective = val;
    render_all();
}

void SceneManager::setRefraction(float refract)
{
    models[current_model]->refractive = refract;
    render_all();
}

void SceneManager::setIntensity(float intens){
    Light* l = dynamic_cast<Light*>(models[current_model]);
    l->color_intensity.x = intens;
    l->color_intensity.y = intens;
    l->color_intensity.z = intens;
    render_all();
}

void SceneManager::setAmbIntensity(float intensity){
    for (auto& model: models)
    {
        if (model->isObject())
            continue;
        Light* l = dynamic_cast<Light*>(model);
        if (l->t == Light::light_type::ambient)
        {
            l->color_intensity.x = intensity;
            l->color_intensity.y = intensity;
            l->color_intensity.z = intensity;
        }
    }
}

void SceneManager::setCoefRefract(float val)
{
    this->k_n = val;
}
