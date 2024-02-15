import string
import random
from time import time, thread_time, process_time

"""
    Функция для печати матрицы
"""
def print_matrix(str1, str2, matrix):
    print("0  0  " + "  ".join([letter for letter in str2]))

    for i in range(len(str1) + 1):
        print(str1[i - 1] if i != 0 else "0", end="")
        for j in range(len(str2) + 1):
            print("  " + str(matrix[i][j]), end="")
        print("")

"""
    Функция для создания матрицы, которая заполнена 0, 
    кроме 0 строки и 0 столбца
"""
def create_matrix(n, m):
    matrix = [[0] * m for i in range(n)]

    # заполняем 0 строку
    for j in range(m):
        matrix[0][j] = j

    # заполняем 0 столбец
    for i in range(n):
        matrix[i][0] = i

    return matrix



def words_algoritm(func):
    str1 = input("Введите строку 1: ")
    str2 = input("Введите строку 2: ")

    res = func(str1, str2, True)
    print("_______________")
    print("Расстояние = ", res)
    print("_______________")


def random_string(str_len):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(str_len))

def time_analysis(func, count = 100, str_len = 8):
    start = time()
    for i in range(count):
        str1 = random_string(str_len)
        str2 = random_string(str_len)
        func(str1, str2, False)
    end = time()
    return (end - start) / count