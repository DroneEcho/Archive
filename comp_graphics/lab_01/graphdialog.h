#ifndef GRAPHDIALOG_H
#define GRAPHDIALOG_H

#include <QDialog>
#include <QGraphicsView>
#include "geometry.h"

namespace Ui {
class GraphDialog;
}

class GraphDialog : public QDialog
{
    Q_OBJECT

public:
    explicit GraphDialog(QWidget *parent = nullptr, GraphData data = {});
    ~GraphDialog();

private:
    Ui::GraphDialog *ui;
};

#endif // GRAPHDIALOG_H
