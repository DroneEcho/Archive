#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->textResult->setText("Введите координаты треугольника (в соответствующие поля слева) "
                                "и точек (x и y через пробел, каждая точка в отдельной строке) \n");

    ui->menubar->addAction("Справка", this, SLOT(info_menu()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_calcButton_clicked()
{
    Triangle trl;
    Point *points;
    size_t n;

    // Чтение данных
    trl = triangle_read();
    if (points_read(&points, &n))
    {
        ui->textResult->setText("Неверно введено множество точек \n");
        return;
    }
    if (n < 3)
    {
        ui->textResult->setText("Необходимо ввести минимум 3 точки \n");
        free(points);
        return;
    }

    QString res;

    if (!check_triangle(trl.p1, trl.p2, trl.p3))
    {
        res = QString("Введенные точки не образуют треугольник \n");
        ui->textResult->setText(res);

        free(points);
        return;
    }

    // Решение задачи
    Circle crl;
    Point tangency, trl_tgc_point, trl_center;
    size_t p1, p2, p3;
    double s;

    bool result = get_sought_circle(trl, points, n, &crl, &tangency, &trl_tgc_point, &trl_center,
                                    &p1, &p2, &p3, &s);

    // Отрисовка результата
    ui->graphResult->update_graph_data(result, points, n, trl, crl, tangency, trl_tgc_point, trl_center);
    ui->graphResult->redraw();

    // Вывод текстового результата
    res = QString("Треугольник: \n(%1; %2) \n(%3; %4) \n(%5; %6) \n").arg(trl.p1.x).arg(trl.p1.y)
                                                            .arg(trl.p2.x).arg(trl.p2.y)
                                                            .arg(trl.p3.x).arg(trl.p3.y);
    res.append("\nТочки: \n");

    for (size_t i = 0; i < n; i++)
        res.append(QString("%1 - (%2; %3)\n").arg(i + 1).arg(points[i].x).arg(points[i].y));

    if (result)
    {
        res.append(QString("\nИскомая окружность построена на точках %1, %2 и %3 \n").arg(p1 + 1).arg(p2 + 1).arg(p3 + 1));
        res.append(QString("Площадь треугольника - %1 \n").arg(s));
    }
    else
        res.append(QString("\nНе удалось найти искомую окружность\n"));

    ui->textResult->setText(res);
}

void MainWindow::info_menu()
{
    InfoDialog dialog(nullptr);
    dialog.exec();
}

Triangle MainWindow::triangle_read()
{
    Triangle trl = {{0, 0}, {0, 0}, {0, 0}};

    trl.p1.x = ui->triangleX1->text().toDouble();
    trl.p1.y = ui->triangleY1->text().toDouble();

    trl.p2.x = ui->triangleX2->text().toDouble();
    trl.p2.y = ui->triangleY2->text().toDouble();

    trl.p3.x = ui->triangleX3->text().toDouble();
    trl.p3.y = ui->triangleY3->text().toDouble();

    return trl;
}

int MainWindow::points_read(Point **points, size_t *n)
{
    QString str = ui->pointsInput->toPlainText();
    QStringList str_list = str.split('\n');

    *n = str_list.size();
    if (str_list.at(*n - 1).size() == 0)
        *n -= 1;
    if (!n)
        return -1;

    *points = (Point*) malloc(sizeof(Point) * *n);

    size_t i;
    QStringList s;

    for (i = 0; i < *n; i++)
    {
        s = str_list.at(i).split(' ');
        if (s.size() != 2)
        {
            free(*points);
            return -1;
        }
        (*points)[i] = {s.at(0).toDouble(), s.at(1).toDouble()};
    }

    return 0;
}
