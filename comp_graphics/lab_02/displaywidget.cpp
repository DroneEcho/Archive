#include "displaywidget.h"

DisplayWidget::DisplayWidget(QWidget *parent) : QGraphicsView(parent)
{
    QGraphicsScene *myScene= new QGraphicsScene();
    myScene->setSceneRect(0, 0, 560, 560);
    this->setScene(myScene);

    this->Pixmap = new QPixmap(560, 560);

    this->g = {nullptr, 0, 0, nullptr, 0, 0};
    this->prev = {nullptr, 0, 0, nullptr, 0, 0};
    this->UndoFlag = true;
}

DisplayWidget::~DisplayWidget()
{
    delete Pixmap;

    if (prev.p_alloc > 0)
        free(prev.points);
    if (prev.l_alloc > 0)
        free(prev.links);

    if (g.p_alloc > 0)
        free(g.points);
    if (g.l_alloc > 0)
        free(g.links);
}

void DisplayWidget::Undo()
{
    if (UndoFlag)
    {
        if (g.p_alloc > 0)
            free(g.points);
        if (g.l_alloc > 0)
            free(g.links);

        g = prev;
        prev = {nullptr, 0, 0, nullptr, 0, 0};
        UndoFlag = false;
    }
}

void DisplayWidget::UpdateGraph(Graph &newGraph)
{
    if (prev.p_alloc > 0)
        free(prev.points);
    if (prev.l_alloc > 0)
        free(prev.links);

    prev = g;
    g = newGraph;
    UndoFlag = true;
}

Graph& DisplayWidget::GetGraph()
{
    return g;
}

void DisplayWidget::DrawGraph()
{
    size_t i;
    QPainter *paint = new QPainter(Pixmap);
    int w = this->Pixmap->width(), h = this->Pixmap->height();

    // Заливка фона
    paint->fillRect(0, 0, w, h, QColor(255, 255, 255, 255));
    paint->setPen(QColor(0, 0, 0, 50));
    paint->drawRect(0, 0, w - 1, h - 1);
    paint->setPen(QColor(0, 0, 0, 255));

    // Оси
    paint->drawText(5, h - 10, "(0,0)");
    paint->drawText(w - 63, h - 10, QString("(%1, 0)").arg(w));
    paint->drawText(5, 15, QString("(0, %1)").arg(h));
    paint->drawText(w - 78, 15, QString("(%1, %2)").arg(w).arg(h));

    // Отрисовка линий
    for (i = 0; i < g.l_len; i++)
        DrawSection(paint, g.points[g.links[i].p1],
                            g.points[g.links[i].p2]);

    // Отрисовка точек
    //for (i = 0; i < g->p_len; i++)
    //    DrawPoint(paint, g->points[i]);

    delete paint;
    this->scene()->addPixmap(*Pixmap);
}

void DisplayWidget::DrawPoint(QPainter *paint, Point p)
{
    int x = round(p.x), y = round(this->Pixmap->height() - p.y);
    paint->fillRect(x, y, 1, 1, QColor(255, 0, 0, 255));
}

void DisplayWidget::DrawSection(QPainter *paint, Point p1, Point p2)
{
    paint->setPen(QPen(QColor(0, 0, 0, 255), 2));
    int x1 = round(p1.x), y1 = round(this->Pixmap->height() - p1.y),
         x2 = round(p2.x), y2 = round(this->Pixmap->height() - p2.y);

    paint->drawLine(x1, y1, x2, y2);
}
