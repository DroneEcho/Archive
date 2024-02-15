#ifndef GRAPHICS_H
#define GRAPHICS_H

#include <qpainter.h>
#include "geometry.h"

// Отрисовка результата
QPixmap* draw_result(bool result, Point *points, size_t n, Triangle trl,
                    Circle crl, Point tangency, Point trl_tgc_point, int w, int h);

// Отрисовка точки
void draw_point(QPainter *paint, Screen scr, Point p, QString name, QColor color);

// Отрисовка отрезкаы
void draw_section(QPainter *paint, Screen scr, Point p1, Point p2,
                              QColor color, int width);

#endif // GRAPHICS_H
