#include "geometry.h"

Circle get_circumscribed(Point p1, Point p2, Point p3)
{
    Line l1, l2;
    Circle crl = {{0, 0}, 0};

    if (!check_triangle(p1, p2, p3))
        return crl;

    // Серединные перпендикуляры двух сторон треугольника
    l1 = get_middle_perpendicular(p1, p2);
    l2 = get_middle_perpendicular(p1, p3);

    crl.center = get_lines_intersection(l1, l2);
    crl.radius = get_section_len(p1, crl.center);;

    return crl;
}

Point get_lines_intersection(Line l1, Line l2)
{
    Point p;

    if (abs(l1.a * l2.b - l1.b * l2.a) < EPS)
    {
        return {NAN, NAN};
    }

    if (abs(l1.a) < EPS)
    {
        p.y = - l1.c / l1.b;
        p.x = (l2.b / l1.b * l1.c - l2.c) / l2.a;
    }
    else
    {
        p.y = (l2.a / l1.a * l1.c - l2.c) / (l2.b - l2.a / l1.a * l1.b);
        p.x = - (l1.b * p.y + l1.c) / l1.a;
    }

    return p;
}

bool check_triangle(Point p1, Point p2, Point p3)
{
    return abs((p1.x - p2.x) * (p1.y - p3.y) - (p1.x - p3.x) * (p1.y - p2.y)) > EPS;
}

Line get_middle_perpendicular(Point p1, Point p2)
{
    Line l = {0, 0, 0};

    l.a = p2.x - p1.x;
    l.b = p2.y - p1.y;
    l.c = - ((p1.x + p2.x) / 2  * l.a + (p1.y + p2.y) / 2 * l.b);

    return l;
}

Line get_line(Point p1, Point p2)
{
    Line l = {0, 0, 0};

    l.a = p1.y - p2.y;
    l.b = p2.x - p1.x;
    l.c = p1.x * p2.y - p2.x * p1.y;

    return l;
}

bool get_tangency(Line l, Circle crl, Point *tangency)
{
    if (abs(l.a) < EPS)
    {
        if (abs(crl.center.y - crl.radius + l.c / l.b) < EPS)
        {
            tangency->x = crl.center.x;
            tangency->y = crl.center.y - crl.radius;

            return true;
        }
        if (abs(crl.center.y + crl.radius + l.c / l.b) < EPS)
        {
            tangency->x = crl.center.x;
            tangency->y = crl.center.y + crl.radius;

            return true;
        }

        return false;
    }

    l.c += l.a * crl.center.x + l.b * crl.center.y;

    double D = l.b * l.b * l.c * l.c / pow(l.a, 4) -
        (l.b * l.b / l.a / l.a + 1) * (l.c * l.c / l.a / l.a - crl.radius * crl.radius);

    if (abs(D) < EPS)
    {
        tangency->y = - l.b * l.c / (l.a * l.a + l.b * l.b);
        tangency->x = - (l.b / l.a * tangency->y + l.c / l.a);

        tangency->x += crl.center.x;
        tangency->y += crl.center.y;

        return true;
    }

    return false;
}

Point get_section_center(Point p1, Point p2)
{
    return {(p1.x + p2.x) / 2, (p1.y + p2.y) / 2};
}

double get_section_len(Point p1, Point p2)
{
    return sqrt((p1.x - p2.x) * (p1.x - p2.x)
                + (p1.y - p2.y) * (p1.y - p2.y));
}

Point get_triangle_center(Triangle trl)
{
    Point m1, m2;
    Line l1, l2;

    m1 = get_section_center(trl.p1, trl.p2);
    m2 = get_section_center(trl.p1, trl.p3);

    l1 = get_line(trl.p3, m1);
    l2 = get_line(trl.p2, m2);

    return get_lines_intersection(l1, l2);
}

double get_triangle_area(Point p1, Point p2, Point p3)
{
    return abs((p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)) / 2;
}

bool get_sought_circle(Triangle trl, Point *points, size_t n, Circle *crl,
                       Point *tangency, Point *trl_tgc_point,
                       Point *triangle_center, size_t *p1, size_t *p2, size_t *p3, double *s)
{
    size_t i, j, k;
    Point t, ttp;
    Circle c;
    double s1;

    *triangle_center = get_triangle_center(trl);
    *s = -1;

    if (n < 3)
        return false;

    for (i = 0; i < n - 2; i++)
    {
        for (j = i + 1; j < n - 1; j++)
        {
            for (k = j + 1; k < n; k++)
            {
                c = get_circumscribed(points[i], points[j], points[k]);
                if (c.radius < EPS)
                    continue;

                s1 = -1;

                if (get_tangency(get_line(ttp = trl.p1, trl.p2), c, &t))
                    s1 = get_triangle_area(c.center, *triangle_center, t);

                else if (get_tangency(get_line(ttp = trl.p1, trl.p3), c, &t))
                    s1 = get_triangle_area(c.center, *triangle_center, t);

                else if (get_tangency(get_line(ttp = trl.p2, trl.p3), c, &t))
                    s1 = get_triangle_area(c.center, *triangle_center, t);

                if (s1 > *s)
                {
                    *s = s1;
                    *tangency = t;
                    *trl_tgc_point = ttp;
                    *crl = c;

                    *p1 = i;
                    *p2 = j;
                    *p3 = k;
                }
            }
        }
    }

    if (*s < 0)
        return false;

    return true;
}

int x_convert(double x, Screen scr)
{
    scr.width -= scr.margin_left + scr.margin_right;
    int res = (int)round((x - scr.x_min) / (scr.x_max - scr.x_min) * scr.width + scr.margin_left);
    return res;
}

int y_convert(double y, Screen scr)
{
    scr.height -= scr.margin_top + scr.margin_bottom;
    int res =  (int)round(scr.height -
                      (y - scr.y_min) / (scr.y_max - scr.y_min) * scr.height + scr.margin_top);
    return res;
}

int w_convert(double w, Screen scr)
{
    int res = (int)round(w / (scr.x_max - scr.x_min) * (scr.width - scr.margin_left - scr.margin_right));
    return res;
}

int h_convert(double h, Screen scr)
{
    int res = - (int)round(h / (scr.y_max - scr.y_min) * (scr.height - scr.margin_top - scr.margin_bottom));
    return res;
}

Screen get_screen(int w, int h, bool result, Point *points, size_t n, Triangle trl, Circle crl)
{
    Screen scr = {w, h, 10, 70, 20, 10, 0, 0, 0, 0};
    if (result)
    {
        scr.x_min = std::min({crl.center.x - crl.radius, trl.p1.x, trl.p2.x, trl.p3.x});
        scr.x_max = std::max({crl.center.x + crl.radius, trl.p1.x, trl.p2.x, trl.p3.x});
        scr.y_min = std::min({crl.center.y - crl.radius, trl.p1.y, trl.p2.y, trl.p3.y});
        scr.y_max = std::max({crl.center.y + crl.radius, trl.p1.y, trl.p2.y, trl.p3.y});
    }
    else
    {
        scr.x_min = std::min({trl.p1.x, trl.p2.x, trl.p3.x});
        scr.x_max = std::max({trl.p1.x, trl.p2.x, trl.p3.x});
        scr.y_min = std::min({trl.p1.y, trl.p2.y, trl.p3.y});
        scr.y_max = std::max({trl.p1.y, trl.p2.y, trl.p3.y});

        for (size_t i = 0; i < n; i++)
        {
            if (points[i].x < scr.x_min)
                scr.x_min = points[i].x;
            if (points[i].x > scr.x_max)
                scr.x_max = points[i].x;
            if (points[i].y < scr.y_min)
                scr.y_min = points[i].y;
            if (points[i].y > scr.y_max)
                scr.y_max = points[i].y;
        }
    }

    int real_width = scr.width - scr.margin_left - scr.margin_right;
    int real_height = scr.height - scr.margin_top - scr.margin_bottom;

    double diff = (scr.x_max - scr.x_min) / real_width
                - (scr.y_max - scr.y_min) / real_height;

    if (diff > 0)
    {
        scr.y_min -= diff * real_height / 2;
        scr.y_max += diff * real_height / 2;
    }
    else if (diff < 0)
    {
        scr.x_min -= - diff * real_width / 2;
        scr.x_max += - diff * real_width / 2;
    }

    return scr;
}
