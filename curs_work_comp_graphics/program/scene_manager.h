﻿#ifndef SCENE_MANAGER_FIRST_H
#define SCENE_MANAGER_FIRST_H
#include <vector>
#include <numeric>
#include <QImage>
#include <QGraphicsScene>
#include "model.h"
#include "camera.h"
#include "light.h"
#include "color_shader.h"
#include "vertex_shader.h"
#include "raythread.h"
#include <QtDebug>
#include <QMutex>
#include <QStringListModel>

const float intensityLight = 1.f;

struct UI_data{
    UI_data(bool isLight_ = false, const Vec3f& position_ = {0.f, 0.f, 0.f});
    uint32_t amount = 0;

    float shift_x = 0, shift_y = 0, shift_z = 0;
    float rot_x = 0, rot_y = 0, rot_z = 0;
    float scale_x = 1.f, scale_y = 1.f, scale_z = 1.f;

    bool texture_flag = false, color_flag = true;

    Vec3f color = {0.5, 0.5, 0.5};

    float specular = 0.f, reflective = 0.f, refractive = 0.f;
    float intensity = intensityLight;
    QImage img;

    bool isLight = false;
};

enum trans_type{shift_x, shift_y, shift_z,
                rot_x, rot_y, rot_z,
                scale_x, scale_y, scale_z,
                up_y, down_y
               };

using ThreadVector = std::vector<RayThread*>;

const Vec3f pointLightPosition = {0.f, 0.f, -5.f}, directionLightPosition = {0.f, 0.f, -5.f};

class SceneManager{

public:

    SceneManager() = default;

    SceneManager(int width_, int height_, QColor background_color_, QGraphicsScene* scene_): width{width_}, height{height_},
        background_color(background_color_), scene{scene_}{

        img = QImage(width, height, QImage::Format_RGB32);
        depthBuffer.resize(width);
        for (auto &vec : depthBuffer)
            vec.resize(height, std::numeric_limits<float>::max());
        img.fill(background_color);

        //camers.push_back(Camera(width, height));
    }

    void init();

    void shift(trans_type t, float val);

    void rotate(trans_type t, float angle);

    void scale(trans_type t, float factor);

    void addCamera();

    void setCamera(int index);

    void deleteCamera(int index);

    void removeAll();

    void moveCamera(trans_type t, float dist);

    void shift_Camera(float x, float y, float z);

    void rotateCamera(float x, float y, float z);

    void uploadModel(std::string name, uint32_t& uid);

    void uploadLight(std::string name, uint32_t& uid, Vec3f &color);

    void removeModel();

    void setCurrentModel(uint32_t uid);

    void setColor(const Vec3f& color);

    void setLightColor(const Vec3f& color);

    void setAmbientLightColor(const Vec3f &color);

    void setFlagTexture(bool flag, const Vec3f& color);

    void setTexture(const QImage& img);

    void setCoefRefract(float val);

    void setSpecular(float val);

    void setReflective(float val);

    void setRefraction(float refract);

    void setIntensity(float intens);

    void setAmbIntensity(float intensity);

    ThreadVector* trace();

    void showTracedResult();

    void safescene(QString Filename, QStringListModel &model, std::map<QString, uint32_t> &text_uid, std::map<QString, UI_data> &name_data);

    void readfile(QString filepath);
    void render();

    int get_camCount()
    {
        return camera_count;
    };

    int get_curCam()
    {
        return curr_camera;
    };
    void ChangeBackground(QColor newColour)
    {
        background_color = newColour;
        render();
    };
private:
    void render_all();

    void rasterize(Model& model);

    void show();

    void rasterBarTriangle(Vertex p1_, Vertex p2_, Vertex p3_);

    bool testAndSet(const Vec3f& p);

    bool backfaceCulling(const Vertex& a, const Vertex& b, const Vertex& c);

    bool clip(const Vertex& p);

private:
    std::vector<Camera> camers;
    int curr_camera = 0;
    int camera_count = 0;
    int count_light = 0;
    std::vector<Model*> models;
    int width, height;
    std::vector<std::vector<float>> depthBuffer;
    QImage img;
    QColor background_color;
    QGraphicsScene *scene;

    std::shared_ptr<PixelShaderInterface> pixel_shader;
    std::shared_ptr<VertexShaderInterface> vertex_shader;
    std::shared_ptr<GeometryShaderInterface> geom_shader;

    uint32_t models_index = 1;
    int current_model = 0;
    float vw = 1.f, vh = 1.f;
    float d = 1.f;
    float k_n = 1.f;

    ThreadVector threads;

};
#endif // SCENE_MANAGER_H
