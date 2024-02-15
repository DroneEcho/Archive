#ifndef GRAPH_H
#define GRAPH_H

#include <stdlib.h>
#include <math.h>

#define EPS 1e-8

typedef struct
{
    double x, y;
} Point;

typedef struct
{
    size_t p1, p2;
} Link;

typedef struct
{
    Point *points;
    size_t p_len;
    size_t p_alloc;

    Link *links;
    size_t l_len;
    size_t l_alloc;
} Graph;

// Добавление эллипса
int AddEllipse(Graph *g, double x, double y, double w, double h, size_t p_num);

// Создание кошки
Graph* CreateCatGraph(double x);

// Копирование графа
Graph* GraphCopy(Graph &g);

// Перенос
void GraphMove(Graph &g, double dx, double dy);

// Масштабирование
void GraphRescale(Graph &g, Point &center, double kx, double ky);

// Поворот
void GraphRotate(Graph &g, Point &center, double angle);

#endif // GRAPH_H
