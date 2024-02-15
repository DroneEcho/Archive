#ifndef DISPLAYWIDGET_H
#define DISPLAYWIDGET_H

#include <QGraphicsView>
#include "graph.h"

class DisplayWidget : public QGraphicsView
{
    Q_OBJECT

public:
    explicit DisplayWidget(QWidget *parent = nullptr);
    ~DisplayWidget();
    void UpdateGraph(Graph &newGraph);
    Graph& GetGraph();
    void DrawGraph();
    void Undo();

private:
    QPixmap *Pixmap;
    Graph g, prev;
    bool UndoFlag;
    void DrawPoint(QPainter *paint, Point p);
    void DrawSection(QPainter *paint, Point p1, Point p2);

signals:

};

#endif // DISPLAYWIDGET_H
