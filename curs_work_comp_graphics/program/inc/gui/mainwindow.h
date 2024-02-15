#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsScene>

#include <QKeyEvent>
#include <QStringListModel>
#include <QColorDialog>
#include <QFileDialog>

#include <stdlib.h>
#include <memory>

#include "facade.h"
#include "base_drawer.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

const float intensityLight = 1.f;

struct UI_data{
    UI_data(bool isLight_ = false, const point& position_ = {0.f, 0.f, 0.f});
    uint32_t amount = 0;

    float shift_x = 0, shift_y = 0, shift_z = 0;
    float rot_x = 0, rot_y = 0, rot_z = 0;
    float scale_x = 1.f, scale_y = 1.f, scale_z = 1.f;

    bool texture_flag = false, color_flag = true;

    point color = {0.5, 0.5, 0.5};

    float specular = 0.f, reflective = 0.f, refractive = 0.f;
    float intensity = intensityLight;
    QImage img;

    bool isLight = false;
};

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    /*
    void on_NewFile_clicked();

    void on_SaveFile_clicked();

    void on_addLight_clicked();
    void on_changeColourLight_clicked();

    void on_delete_object_button_clicked();

    void on_add_texture_button_clicked();
    void on_color_push_back_button_clicked();



    void on_ViewColour_clicked();
    void on_Render_clicked();
    */
    void on_addModel_clicked();

    void on_loadModelBtn_clicked();
    void on_addCameraBtn_clicked();
    void on_cameraCB_currentIndexChanged(int index);
    void on_deleteCameraBtn_clicked();

    void on_upBtn_clicked();

    void on_rightUpBtn_clicked();
    void on_rigntDownBtn_clicked();
    void on_leftDownBtn_clicked();
    void on_leftUpBtn_clicked();

    void on_rigthBtn_clicked();
    void on_downBtn_clicked();
    void on_leftBtn_clicked();

    void on_rotateBtn_clicked();
    void on_moveBtn_clicked();

    /*
    void on_loadModelBtn_clicked();
    void on_deleteModelBtn_clicked();
    */
private:
    void setup_scene();
    void render_scene();
    void checkCamExist();
    void scan_move_model_params(double &dx, double &dy, double &dz) const;
    void scan_scale_model_params(double &kx, double &ky, double &kz) const;
    void scan_rotate_model_params(double &ox, double &oy, double &oz) const;
    void scan_move_camera_params(double &dx, double &dy, double &dz) const;
    void scan_rotate_camera_params(double &ox, double &oy, double &oz) const;

    Ui::MainWindow *ui;

    std::map<QString, uint32_t> text_uid;
    std::map<QString, UI_data> obj_data;

    facade _facade;
    QStringListModel *model;

    size_t cams_count = 0;
    uint32_t models_index = 0;
    std::shared_ptr<QGraphicsScene> _scene;
    std::shared_ptr<base_drawer> _drawer;
};
#endif // MAINWINDOW_H
