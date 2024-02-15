from algs import *

def main():
    do_start = True

    while(do_start):
        command = input("\n\nМеню: \n"
                        "\t 0. Выход\n"
                        "\t 1. Расстояние Дамерау-Левенштейна матрица\n"
                        "\t 2. Расстояние Дамерау-Левенштейна рекурсивно (кеш)\n"
                        "\t 3. Расстояние Дамерау-Левенштейна рекурсивно\n"
                        "\t 4. Расстояние Левенштейна матрица\n"
                        "\t 5. Все алгоритмы вместе\n"
                        "\t 6. Замер времени\n"
                        "\t Выбор: ")
        if (command == "1"):
            words_algoritm(damerau_levenshtein_matrix)
        elif (command == "2"):
            words_algoritm(damerau_levenshtein_recursive_cash)
        elif (command == "3"):
            words_algoritm(damerau_levenshtein_recursive)
        elif (command == "4"):
            words_algoritm(levenshtein_matrix)
        elif (command == "5"):
            y = []
            str1 = input("Введите первую строку 1: ")
            str2 = input("Введите первую строку 2: ")

            res = damerau_levenshtein_matrix(str1, str2)
            print("\nРасстрояние Дамерау-Левенштейна, полученное с использованием матрицы: ", res)
            res = damerau_levenshtein_recursive_cash(str1, str2)
            print("\nРасстрояние Дамерау-Левенштейна, полученное с использованием рекурсии и кэша: ", res)
            res = damerau_levenshtein_recursive(str1, str2)
            print("\nРасстрояние Дамерау-Левенштейна, полученное с использованием рекурсии: ", res)
            res = levenshtein_matrix(str1, str2)
            print("\nРасстрояние Левенштейна, полученное с использованием матрицы: ", res)
        elif (command == "6"):
            count = 100
            for i in range(1, 5, 1):
                print("длина Строки: ", i)
                print("   Дамлев                : ", "{0:.15f}".format(time_analysis(damerau_levenshtein_matrix, count, i)))
                print("   ДамЛев рекурсия + кэш : ", "{0:.15f}".format(time_analysis(damerau_levenshtein_recursive_cash, count, i)))
                print("   ДамЛев рекурсия       : ", "{0:.15f}".format(time_analysis(damerau_levenshtein_recursive, count, i)))
                print("   Лев                   : ", "{0:.15f}".format(time_analysis(levenshtein_matrix, count, i)))
        else:
            do_start = False

if __name__ == "__main__":
    main()