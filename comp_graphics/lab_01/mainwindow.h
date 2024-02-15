#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "infodialog.h"
#include "geometry.h"
#include "graphics.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Triangle triangle_read();
    int points_read(Point **points, size_t *n);

private:
    Ui::MainWindow *ui;

private slots:
    void on_calcButton_clicked();
    void info_menu();
};

#endif // MAINWINDOW_H
