#ifndef GRAPHICSVIEWZOOMED_H
#define GRAPHICSVIEWZOOMED_H

#include <graphicsview.h>

namespace Ui {
class GraphicsViewZoomed;
}

class GraphicsViewZoomed : public GraphicsView
{
    Q_OBJECT

public:
    explicit GraphicsViewZoomed(QWidget *parent = nullptr);
    ~GraphicsViewZoomed();

private:
    Ui::GraphicsViewZoomed *ui;

public slots:
    void mousePressEvent(QMouseEvent * e);

};

#endif // GRAPHICSVIEWZOOMED_H
