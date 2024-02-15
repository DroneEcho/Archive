from math import *

FUNCS = [
    "sin^2(x) + cos^2(z) - y = 0",
    "sqrt(fabs(x * z)) - y = 0",
    "exp(cos(x) * sin(z)) - y = 0",
    "sin(x * z) - y = 0",
    "x^2 + z^2 - y = 0"
]

def f1(x, z):
    return sin(x) ** 2 + cos(z) ** 2


def f2(x, z):
    return sqrt(fabs(x * z))


def f3(x, z):
    return exp(cos(x) * sin(z))


def f4(x, z):
    return sin(x * z)


def f5(x, z):
    return x * x + z * z
