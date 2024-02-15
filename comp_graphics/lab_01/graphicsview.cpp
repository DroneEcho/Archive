#include "graphicsview.h"
#include "ui_graphicsview.h"

GraphicsView::GraphicsView(QWidget *parent, int width, int height) :
    QGraphicsView(parent),
    ui(new Ui::GraphicsView)
{
    ui->setupUi(this);

    this->width = width;
    this->height = height;

    this->data = {};

    QGraphicsScene *myScene= new QGraphicsScene();
    myScene->setSceneRect(0, 0, width, height);
    this->setScene(myScene);

    this->pix = new QPixmap(width, height);
}

GraphicsView::~GraphicsView()
{
    delete ui;
}

void GraphicsView::mousePressEvent(QMouseEvent *e)
{
    if (data.points)
    {
        GraphDialog dialog(nullptr, data);
        dialog.exec();
    }
}

void GraphicsView::update_graph_data(bool result, Point *points, size_t n, Triangle trl, Circle crl,
                                     Point tangency, Point trl_tgc_point, Point trl_center)
{
    data.result = result;
    free(data.points);
    data.points = points;
    data.n = n;
    data.trl = trl;
    data.crl = crl;
    data.tangency = tangency;
    data.trl_tgc_point = trl_tgc_point;
    data.trl_center = trl_center;
}

void GraphicsView::update_graph_data(GraphData data)
{
    this->data = data;
}

void GraphicsView::redraw()
{
    QPainter *paint = new QPainter(pix);

    Screen scr = get_screen(width, height, data.result, data.points, data.n, data.trl, data.crl);

    // Заливка фона
    paint->fillRect(0, 0, width, height, QColor(255, 255, 255, 255));

    // Настройка шрифта
    QFont font("Calibri", 9);
    //font.setBold(true);
    paint->setFont(font);

    // Отрисовка точек
    for (size_t i = 0; i < data.n; i++)
        draw_point(paint, scr, data.points[i], QString("%1").arg(i + 1), QColor(0, 0, 0, 255));

    // Отрисовка треугольника
    draw_triangle(paint, scr, data.trl, QColor(0, 0, 0, 255), 2);

    draw_point(paint, scr, data.trl.p1, "", QColor(0, 0, 0, 200));
    draw_point(paint, scr, data.trl.p2, "", QColor(0, 0, 0, 200));
    draw_point(paint, scr, data.trl.p3, "", QColor(0, 0, 0, 200));

    if (data.result)
    {
        // Отрисовка окружности
        paint->setPen(QPen(QColor(0, 0, 0, 255), 2));
        if (data.crl.radius > EPS)
            paint->drawEllipse(x_convert(data.crl.center.x - data.crl.radius, scr), y_convert(data.crl.center.y - data.crl.radius, scr),
                            w_convert(data.crl.radius * 2, scr), h_convert(data.crl.radius * 2, scr));

        // Отрисовка точки касания
        draw_point(paint, scr, data.tangency, "", QColor(255, 0, 0, 200));

        // Отрисовка касательной
        draw_section(paint, scr, data.trl_tgc_point, data.tangency, QColor(0, 0, 0, 100), 2);

        // Отрисовка площади
        draw_point(paint, scr, data.trl_center, "", QColor(255, 0, 0, 200));
        draw_point(paint, scr, data.crl.center, "", QColor(255, 0, 0, 200));

        draw_triangle(paint, scr, {data.crl.center, data.tangency, data.trl_center},
                      QColor(255, 0, 0, 150), 2);
        fill_triangle(paint, scr, {data.crl.center, data.tangency, data.trl_center},
                      QColor(255, 0, 0, 150), 1, 10);
    }

    delete paint;
    this->scene()->addPixmap(*pix);
}

void GraphicsView::draw_point(QPainter *paint, Screen scr, Point p, QString name, QColor color)
{
    QString sign = QString("%1 ").arg(name);

    if (abs(floor(p.x) * 100 - floor(p.x * 100)) < EPS)
        sign.append(QString("(%2; ").arg(p.x, 0, 'f', 0));
    else
        sign.append(QString("(%2; ").arg(p.x, 0, 'f', 2));

    if (abs(floor(p.y) * 100 - floor(p.y * 100)) < EPS)
        sign.append(QString("%3)").arg(p.y, 0, 'f', 0));
    else
        sign.append(QString("%3)").arg(p.y, 0, 'f', 2));


    int x = x_convert(p.x, scr), y = y_convert(p.y, scr);

    paint->fillRect(x - 4, y - 4, 9, 9, color);
    paint->setPen(QPen(QColor(0, 0, 0, 255)));
    paint->drawText(x + 5, y - 5, sign);
}

void GraphicsView::draw_section(QPainter *paint, Screen scr, Point p1, Point p2,
                              QColor color, int width)
{
    paint->setPen(QPen(color, width));
    paint->drawLine(x_convert(p1.x, scr), y_convert(p1.y, scr),
                    x_convert(p2.x, scr), y_convert(p2.y, scr));
}

void GraphicsView::draw_triangle(QPainter *paint, Screen scr, Triangle trl,
                              QColor color, int width)
{
    draw_section(paint, scr, trl.p1, trl.p2, color, width);
    draw_section(paint, scr, trl.p1, trl.p3, color, width);
    draw_section(paint, scr, trl.p2, trl.p3, color, width);
}

void GraphicsView::fill_triangle(QPainter *paint, Screen scr, Triangle trl,
                              QColor color, int width, int freq)
{
    paint->setPen(QPen(color, width));

    Line hatch;
    Line l1, l2, l3;
    Point p1, p2, p3;
    bool p1_f, p2_f, p3_f, flag = true, turn = false;

    trl.p1.x = x_convert(trl.p1.x, scr);
    trl.p1.y = y_convert(trl.p1.y, scr);
    trl.p2.x = x_convert(trl.p2.x, scr);
    trl.p2.y = y_convert(trl.p2.y, scr);
    trl.p3.x = x_convert(trl.p3.x, scr);
    trl.p3.y = y_convert(trl.p3.y, scr);

    // Линия штриховки
    hatch = {1, 1, - trl.p1.x - trl.p1.y};

    l1 = get_line(trl.p1, trl.p2);
    l2 = get_line(trl.p1, trl.p3);
    l3 = get_line(trl.p2, trl.p3);

    while (flag)
    {
        p1 = get_lines_intersection(hatch, l1);
        p2 = get_lines_intersection(hatch, l2);
        p3 = get_lines_intersection(hatch, l3);

        p1_f = get_section_len(p1, trl.p1) + get_section_len(p1, trl.p2)
                > get_section_len(trl.p1, trl.p2) + EPS;
        p2_f = get_section_len(p2, trl.p1) + get_section_len(p2, trl.p3)
                > get_section_len(trl.p1, trl.p3) + EPS;
        p3_f = get_section_len(p3, trl.p2) + get_section_len(p3, trl.p3)
                > get_section_len(trl.p2, trl.p3) + EPS;

        if (p1_f + p2_f + p3_f > 1)
        {
            if (turn)
                flag = false;
            else
            {
                turn = true;
                hatch = {1, 1, - trl.p1.x - trl.p1.y};
            }

            continue;
        }

        if (isnan(p1.x) || p1_f)
        {
            paint->drawLine((int)round(p2.x), (int)round(p2.y),
                            (int)round(p3.x), (int)round(p3.y));
        }
        else if (isnan(p2.x) || p2_f)
        {
            paint->drawLine((int)round(p1.x), (int)round(p1.y),
                            (int)round(p3.x), (int)round(p3.y));
        }
        else if (isnan(p3.x) || p3_f)
        {
            paint->drawLine((int)round(p1.x), (int)round(p1.y),
                             (int)round(p2.x), (int)round(p2.y));
        }

        if (turn)
            hatch.c += freq;
        else
            hatch.c -= freq;
    }
}
