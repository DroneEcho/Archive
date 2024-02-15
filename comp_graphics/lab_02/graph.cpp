#include "graph.h"

int AddEllipse(Graph *g, double x, double y, double w, double h, size_t p_num)
{
    if (p_num % 2 || w < EPS || h < EPS)
        return -1;

    if (g->p_len + p_num > g->p_alloc
            || g->l_len + p_num > g->l_alloc)
        return -1;

    double a2 = 1 / (w / 2) / (w / 2),
            b2 = 1 / (h / 2) / (h / 2);

    double angle = 0, step = M_PI * 2 / p_num;
    double k;
    Point p1, p2;

    for (size_t i = 0; i < p_num / 2; i++)
    {
        k = tan(angle);

        p1.x = sqrt(1 / (a2 + k * k * b2));
        p1.y = p1.x * k;

        p2.x = - p1.x;
        p2.y = - p1.y;

        p1.x += x + w / 2;
        p1.y += y + h / 2;
        p2.x += x + w / 2;
        p2.y += y + h / 2;

        if (k >= 0)
        {
            g->points[g->p_len + i] = p1;
            g->points[g->p_len + i + p_num / 2] = p2;
        }
        else
        {
            g->points[g->p_len + i] = p2;
            g->points[g->p_len + i + p_num / 2] = p1;
        }

        angle += step;
    }

    for (size_t i = 0; i < p_num; i++)
        g->links[g->l_len + i] = {g->p_len + i, g->p_len + (i + 1) % p_num};

    g->p_len += p_num;
    g->l_len += p_num;

    return 0;
}

Graph* CreateCatGraph(double x)
{
    Graph *g = (Graph*) malloc(sizeof(Graph));

    if (!g)
        return nullptr;

    size_t head = 100, body = 100, eye = 50, ear = 3, mst = 7;

    g->p_len = 0;
    g->p_alloc = head + body + eye * 2 + ear * 2 + mst;
    g->points = (Point*) malloc(sizeof(Point) * g->p_alloc);
    if (!g->points)
    {
        free(g);
        return nullptr;
    }

    g->l_len = 0;
    g->l_alloc = head + body + eye * 2 + ear * 2 - 2 + mst - 1;
    g->links = (Link*) malloc(sizeof(Link) * g->l_alloc);
    if (!g->links)
    {
        free(g->points);
        free(g);
        return nullptr;
    }

    AddEllipse(g, x - 50, 120, 100, 240, body);
    AddEllipse(g, x - 50, 360, 100, 100, head);
    AddEllipse(g, x - 50 + 20, 400, 20, 20, eye);
    AddEllipse(g, x - 50 + 60, 400, 20, 20, eye);

    // Отрезки ушей
    for (size_t i = 0; i < 2; i++)
        g->links[g->l_len++] = {g->p_len + i, g->p_len + i + 1};
    for (size_t i = 3; i < 5; i++)
        g->links[g->l_len++] = {g->p_len + i, g->p_len + i + 1};

    // Точки ушей
    g->points[g->p_len++] = {x - 50 + 20, 450};
    g->points[g->p_len++] = {x - 50 + 30, 480};
    g->points[g->p_len++] = {x - 50 + 40, 459};

    g->points[g->p_len++] = {x - 50 + 80, 450};
    g->points[g->p_len++] = {x - 50 + 70, 480};
    g->points[g->p_len++] = {x - 50 + 60, 459};

    // Отрезки усов
    for (size_t i = 1; i < 7; i++)
        g->links[g->l_len++] = {g->p_len, g->p_len + i};

    // Точки усов
    g->points[g->p_len++] = {x - 50 + 50, 390};

    g->points[g->p_len++] = {x - 50 + 20, 400};
    g->points[g->p_len++] = {x - 50 + 80, 400};
    g->points[g->p_len++] = {x - 50 + 20, 380};
    g->points[g->p_len++] = {x - 50 + 80, 380};
    g->points[g->p_len++] = {x - 50 + 10, 390};
    g->points[g->p_len++] = {x - 50 + 90, 390};

    return g;
}

Graph* GraphCopy(Graph &g)
{
    Graph *c = (Graph*) malloc(sizeof(Graph));
    size_t i;

    if (!c)
        return nullptr;

    c->p_len = g.p_len;
    c->p_alloc = g.p_alloc;
    c->points = (Point*) malloc(sizeof(Point) * c->p_alloc);
    if (!c->points)
    {
        free(c);
        return nullptr;
    }
    for (i = 0; i < c->p_len; i++)
        c->points[i] = g.points[i];

    c->l_len = g.l_len;
    c->l_alloc = g.l_alloc;
    c->links = (Link*) malloc(sizeof(Link) * c->l_alloc);
    if (!c->links)
    {
        free(c->points);
        free(c);
        return nullptr;
    }
    for (i = 0; i < c->l_len; i++)
        c->links[i] = g.links[i];

    return c;
}

void GraphMove(Graph &g, double dx, double dy)
{
    for (size_t i = 0; i < g.p_len; i++)
    {
        g.points[i].x += dx;
        g.points[i].y += dy;
    }
}

void GraphRescale(Graph &g, Point &center, double kx, double ky)
{
    for (size_t i = 0; i < g.p_len; i++)
    {
        g.points[i].x = kx * g.points[i].x + center.x * (1 - kx);
        g.points[i].y = ky * g.points[i].y + center.y * (1 - ky);
    }
}

void GraphRotate(Graph &g, Point &center, double angle)
{
    double x, y;

    for (size_t i = 0; i < g.p_len; i++)
    {
        x = g.points[i].x - center.x;
        y = g.points[i].y - center.y;

        g.points[i].x = center.x + x * cos(angle) + y * sin(angle);
        g.points[i].y = center.y - x * sin(angle) + y * cos(angle);
    }
}

