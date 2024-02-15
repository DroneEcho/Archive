#include "graphdialog.h"
#include "ui_graphdialog.h"

GraphDialog::GraphDialog(QWidget *parent, GraphData data) :
    QDialog(parent),
    ui(new Ui::GraphDialog)
{
    ui->setupUi(this);

    ui->graphicsView->update_graph_data(data);
    ui->graphicsView->redraw();
}

GraphDialog::~GraphDialog()
{
    delete ui;
}
