#ifndef GEOMETRY_H
#define GEOMETRY_H

#include <stdlib.h>
#include <math.h>
#include <algorithm>

#define EPS 1e-8

typedef struct
{
    double x, y;
} Point;

typedef struct
{
    Point p1, p2, p3;
} Triangle;

typedef struct
{
    double a, b, c;
} Line;

typedef struct
{
    Point center;
    double radius;
} Circle;

typedef struct
{
    int width, height;
    int margin_left, margin_right, margin_top, margin_bottom;
    double x_min, x_max;
    double y_min, y_max;
} Screen;

typedef struct
{
    bool result;
    Triangle trl;
    Point *points;
    size_t n;
    Circle crl;
    Point tangency;
    Point trl_tgc_point;
    Point trl_center;
} GraphData;

// Получение окружности проходящей через 3 точки
Circle get_circumscribed(Point p1, Point p2, Point p3);

// Получение серединного перпендикуляра
Line get_middle_perpendicular(Point p1, Point p2);

// Получение точки пересечения
Point get_lines_intersection(Line l1, Line l2);

// Получение прямой проходящей через две точки
Line get_line(Point p1, Point p2);

// Поиск точки касания прямой и окружности
bool get_tangency(Line l, Circle crl, Point *tangency, Point *trl_tgc_point);

// Проверка, образуют ли три точки треугольник
bool check_triangle(Point p1, Point p2, Point p3);

// Вычисление длины отрезка
double get_section_len(Point p1, Point p2);

// Получение центральной точки отрезка
Point get_section_center(Point p1, Point p2);

// Получение центральной точки треугольника
Point get_triangle_center(Triangle trl);

// Вычисление площади треугольника
double get_triangle_area(Point p1, Point p2, Point p3);

// Решение поставленной геометрической задачи
bool get_sought_circle(Triangle trl, Point *points, size_t n, Circle *crl, Point *tangency, Point *trl_tgc_point,
                       Point *triangle_center, size_t *p1, size_t *p2, size_t *p3, double *s);

// Преобразование координаты x
int x_convert(double x, Screen screen);

// Преобразование координаты y
int y_convert(double x, Screen screen);

// Преобразование ширины
int w_convert(double w, Screen scr);

// Преобразование высоты
int h_convert(double h, Screen scr);

// Создание экрана
Screen get_screen(int w, int h, bool result, Point *points, size_t n, Triangle trl, Circle crl);

#endif // GEOMETRY_H
