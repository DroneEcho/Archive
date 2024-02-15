#include "graphicsviewzoomed.h"
#include "ui_graphicsviewzoomed.h"

GraphicsViewZoomed::GraphicsViewZoomed(QWidget *parent) :
    GraphicsView(parent, 970, 970),
    ui(new Ui::GraphicsViewZoomed)
{
    ui->setupUi(this);
}

GraphicsViewZoomed::~GraphicsViewZoomed()
{
    delete ui;
}

void GraphicsViewZoomed::mousePressEvent(QMouseEvent *e)
{
    parentWidget()->close();
}
