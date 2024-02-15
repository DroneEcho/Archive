#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMessageBox>
#include <math.h>
#include "graph.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void info_menu();

    void on_drawButton_clicked();

    void on_moveButton_clicked();

    void on_rescaleButton_clicked();

    void on_rotateButton_clicked();

    void on_backButton_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
