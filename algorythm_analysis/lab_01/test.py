import main
import string
import random
from time import process_time 
from algs import *

import matplotlib.pyplot as plt

N = 100
y_time_dlev_rec = []
y_time_dlev_cash = []
y_time_dlev_matrix = []
y_time_lev_matrix = []
len_arr = []


def test(len):
    time_dlev_rec = 0
    time_dlev_cash = 0
    time_dlev_matrix = 0
    time_lev_matrix = 0

    for i in range(N):
        s1 = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=len))
        s2 = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=len))

        start = process_time()
        levenshtein_matrix(s1, s2, False)
        stop = process_time()

        time_lev_matrix += stop - start

        start = process_time()
        damerau_levenshtein_recursive(s1, s2, False)
        stop = process_time()

        time_dlev_rec += stop - start

        start = process_time()
        damerau_levenshtein_recursive_cash(s1, s2, False)
        stop = process_time()

        time_dlev_cash += stop - start

        start = process_time()
        damerau_levenshtein_matrix(s1, s2, False)
        stop = process_time()

        time_dlev_matrix += stop - start

    len_arr.append(len)
    y_time_dlev_rec.append((time_dlev_rec / N) * 1000000)
    y_time_dlev_matrix.append((time_dlev_matrix / N) * 1000000)
    y_time_lev_matrix.append((time_lev_matrix / N) * 1000000)
    y_time_dlev_cash.append((time_dlev_cash / N) * 1000000)


    return (time_lev_matrix / N) * 1000000, (time_dlev_matrix / N) * 1000000, (time_dlev_rec / N) * 1000000, (time_dlev_cash / N) * 1000000


def print_results(count):
    time_lev_matrix, time_dlev_matrix, time_dlev_rec, time_dlev_cash = test(count)
    print("\n--------------------------------------------------------------------------------------")
    print("Время работы функции при n = : ", count)
    print("Матричный способ нахождения расстояния Левенштейна: ", "{0:.6f}".format(time_lev_matrix), "мкс")
    print("Матричный способ нахождения расстояния Д-Левенштейна: ", "{0:.6f}".format(time_dlev_matrix), "мкс")
    print("Нахождение расстояния Д-Левенштейна с использованием рекурсии: ", "{0:.6f}".format(time_dlev_rec), "мкс")
    print("Нахождение расстояния Д-Левенштейна c использования кэша: ", "{0:.6f}".format(time_dlev_cash), "мкс")

    return

if __name__ == "__main__":
    for i in range(9):
       print_results(i)

    fig = plt.figure(figsize = (10, 7))
    plot = fig.add_subplot()
    plot.plot(len_arr, y_time_lev_matrix, label = "Р-Левенштейна(матр)")
    plot.plot(len_arr, y_time_dlev_matrix,'-.', label = "Р-Д-Левенштейна(матр)")
    plot.plot(len_arr, y_time_dlev_rec, '--', label = "Р-Д-Левенштейна(рек)")
    plot.plot(len_arr, y_time_dlev_cash, ':', label = "Р-Д-Левенштейна(кэш)")
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритмов вычисления расстояния")
    plt.ylabel("Затраченное время (мск)")
    plt.xlabel("Длина (симболы")

    
    
    plt.show()
