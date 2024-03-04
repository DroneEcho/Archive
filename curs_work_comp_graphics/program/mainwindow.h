#ifndef MAINWINDOW_H
#define MAINWINDOW_H
#include <QMainWindow>
#include <QKeyEvent>
#include <QStringListModel>
#include <QColorDialog>
#include <QFileDialog>
#include "scene_manager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    SceneManager manager;
    ~MainWindow();

public slots:

    void checkThread();

private slots:
    void fetch(QModelIndex index);

    void fill_data(const UI_data& data);
    void save_data(UI_data& data);
    void showButtons(bool isLight);
    void hideButtons(bool isLight);
    void changeHidence(bool, bool);
    void lockSignals(bool signal);
    void on_delete_object_button_clicked();

    void on_SaveFile_clicked();


    void on_changeColourLight_clicked();
    void on_color_flag_clicked();
    void on_texture_flag_clicked();

    void on_add_texture_button_clicked();
    void on_add_color_button_clicked();

    void on_render_clicked();
    void on_ViewColour_clicked();

    void on_addLight_clicked();
    void on_addModel_clicked();

    void on_loadModelBtn_clicked();
    void on_newModelBtn_clicked();
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


    void on_rotate_x_spin_valueChanged(double arg1);
    void on_rotate_y_spin_valueChanged(double arg1);
    void on_rotate_z_spin_valueChanged(double arg1);
    void on_offset_x_spin_valueChanged(double arg1);
    void on_offset_y_spin_valueChanged(double arg1);
    void on_offset_z_spin_valueChanged(double arg1);
    void on_scale_z_spin_valueChanged(double arg1);
    void on_scale_x_spin_valueChanged(double arg1);
    void on_scale_y_spin_valueChanged(double arg1);

    void namedata_update(QImage img, int index);
private:
    void disableAll(bool flag);

private:
    Ui::MainWindow *ui;
    QStringListModel *model;
    std::map<QString, uint32_t> text_uid;
    std::map<QString, UI_data> name_data;
    QString prev_selected = "";
    std::shared_ptr<QGraphicsScene> _scene;

    ThreadVector* threads;
    int th_amount = 0;
    QMutex mutex;
    bool isLocked = false;
};

class Filter: public QObject{
    Q_OBJECT
public:
    Filter(std::function<void (trans_type, float)> f_): f{f_}{}
protected:
    bool eventFilter(QObject *obj, QEvent *event) override;
private:
    std::function<void (trans_type, float)> f;
};


#endif // MAINWINDOW_H
