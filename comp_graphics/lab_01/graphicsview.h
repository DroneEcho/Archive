#ifndef GRAPHICSVIEW_H
#define GRAPHICSVIEW_H

#include <QGraphicsView>
#include <QMouseEvent>
#include "graphdialog.h"
#include "geometry.h"

namespace Ui {
class GraphicsView;
}

class GraphicsView : public QGraphicsView
{
    Q_OBJECT

public:
    explicit GraphicsView(QWidget *parent = nullptr, int width = 460, int height = 460);
    ~GraphicsView();

    void update_graph_data(bool result, Point *points, size_t n, Triangle trl,
                        Circle crl, Point tangency, Point trl_tgc_point, Point trl_center);
    void update_graph_data(GraphData data);
    void redraw();

private:
    void draw_point(QPainter *paint, Screen scr, Point p, QString name, QColor color);
    void draw_section(QPainter *paint, Screen scr, Point p1, Point p2,
                                  QColor color, int width);
    void draw_triangle(QPainter *paint, Screen scr, Triangle trl,
                       QColor color, int width);
    void fill_triangle(QPainter *paint, Screen scr, Triangle trl,
                                  QColor color, int width, int freq);

public:
    int width, height;

private:
    Ui::GraphicsView *ui;
    QPixmap *pix;
    GraphData data;

signals:

public slots:
    void mousePressEvent(QMouseEvent * e);

};

#endif // GRAPHICSVIEW_H
