
import matplotlib.pyplot as plt


y_time_random = [0.0259, 0.2155, 0.4105, 0.6530, 0.8424, 1.1948, 1.4040, 1.6308, 1.7480, 1.9709]

y_time_sorted = [0.0299, 0.2315, 0.4491, 0.6905, 1.0893, 1.6078, 2.1618, 2.2028, 2.2261, 2.6202]

if __name__ == "__main__":
    len_arr = []
    for i in range(100, 1001, 100):
        len_arr.append(i)
        
    fig = plt.figure(figsize = (10, 7))
    plot = fig.add_subplot()
    plot.plot(len_arr, y_time_random, label = "Параллельный конвейер")
    plot.plot(len_arr, y_time_sorted,'-.', label = "Последовательный конвейер")
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритмов конвейера со случайными данными")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Количество запросов")

    plt.show()