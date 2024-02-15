#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    on_drawButton_clicked();
    ui->backButton->setEnabled(false);

    ui->menubar->addAction("Справка", this, SLOT(info_menu()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::info_menu()
{
    QMessageBox infoDialog;

    infoDialog.setText("Перенос: \ndx, dy - смещение по OX и OY соответственно. \n\n"
                        "Масштабирование: \nXц, Yц - координаты центра масштабирования; \n"
                        "kx, ky - коэффициенты масштабирования по OX и OY. \n\n"
                        "Поворот: \nXц, Yц - координаты центра поворота; \nугол - угол поворота в градусах");
    infoDialog.setWindowTitle("Справка");

    infoDialog.exec();
}

void MainWindow::on_drawButton_clicked()
{
    Graph *g = CreateCatGraph(ui->display->width() / 2);
    if (!g)
        return;

    ui->display->UpdateGraph(*g);
    ui->display->DrawGraph();
    ui->backButton->setEnabled(true);
}

void MainWindow::on_moveButton_clicked()
{
    Graph *g = GraphCopy(ui->display->GetGraph());
    if (!g)
        return;

    double dx = ui->moveDxInput->text().toDouble(),
            dy = ui->moveDyInput->text().toDouble();

    GraphMove(*g, dx, dy);
    ui->display->UpdateGraph(*g);
    ui->display->DrawGraph();
    ui->backButton->setEnabled(true);
}

void MainWindow::on_rescaleButton_clicked()
{
    Graph *g = GraphCopy(ui->display->GetGraph());
    if (!g)
        return;

    Point p = {ui->rescaleXInput->text().toDouble(),
                ui->rescaleYInput->text().toDouble()};
    double kx = ui->rescaleKxInput->text().toDouble(),
            ky = ui->rescaleKyInput->text().toDouble();

    GraphRescale(*g, p, kx, ky);
    ui->display->UpdateGraph(*g);
    ui->display->DrawGraph();
    ui->backButton->setEnabled(true);
}

void MainWindow::on_rotateButton_clicked()
{
    Graph *g = GraphCopy(ui->display->GetGraph());
    if (!g)
        return;

    Point p = {ui->rotateXInput->text().toDouble(),
                ui->rotateYInput->text().toDouble()};
    double angle = ui->rotateAngleInput->text().toDouble()
                    / 180 * M_PI;

    GraphRotate(*g, p, angle);
    ui->display->UpdateGraph(*g);
    ui->display->DrawGraph();
    ui->backButton->setEnabled(true);
}

void MainWindow::on_backButton_clicked()
{
    ui->display->Undo();
    ui->display->DrawGraph();
    ui->backButton->setEnabled(false);
}
