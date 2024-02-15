from main import full_combinations, parse_full_combinations
import time
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

class ACO_TSP:  # класс алгоритма муравьиной колонии для решения задачи коммивояжёра
    def __init__(self, func, n_dim, size_pop=10, max_iter=20, distance_matrix=None, alpha=1, beta=2, rho=0.1):
        self.func = func
        self.n_dim = n_dim  # количество городов
        self.size_pop = size_pop  # количество муравьёв
        self.max_iter = max_iter  # количество итераций
        self.alpha = alpha  # коэффициент важности феромонов в выборе пути
        self.beta = beta  # коэффициент значимости расстояния
        self.rho = rho  # скорость испарения феромонов

        self.prob_matrix_distance = 1 / (distance_matrix + 1e-10 * np.eye(n_dim, n_dim))

        # Матрица феромонов, обновляющаяся каждую итерацию
        self.Tau = np.ones((n_dim, n_dim))
        # Путь каждого муравья в определённом поколении
        self.Table = np.zeros((size_pop, n_dim)).astype(int)
        self.y = None  # Общее расстояние пути муравья в определённом поколении
        self.generation_best_X, self.generation_best_Y = [], [] # фиксирование лучших поколений
        self.x_best_history, self.y_best_history = self.generation_best_X, self.generation_best_Y
        self.best_x, self.best_y = None, None

    def run(self, max_iter=None):
        self.max_iter = max_iter or self.max_iter
        for i in range(self.max_iter):
            # вероятность перехода без нормализации
            prob_matrix = (self.Tau ** self.alpha) * (self.prob_matrix_distance) ** self.beta
            for j in range(self.size_pop):  # для каждого муравья
                # точка начала пути (она может быть случайной, это не имеет значения)
                self.Table[j, 0] = 0
                for k in range(self.n_dim - 1):  # каждая вершина, которую проходят муравьи
                    # точка, которая была пройдена и не может быть пройдена повторно
                    taboo_set = set(self.Table[j, :k + 1])
                    # список разрешённых вершин, из которых будет происходить выбор
                    allow_list = list(set(range(self.n_dim)) - taboo_set)
                    prob = prob_matrix[self.Table[j, k], allow_list]
                    prob = prob / prob.sum() # нормализация вероятности
                    next_point = np.random.choice(allow_list, size=1, p=prob)[0]
                    self.Table[j, k + 1] = next_point

            # рассчёт расстояния
            y = np.array([self.func(i, distance_matrix, self.n_dim) for i in self.Table])
            # фиксация лучшего решения
            index_best = y.argmin()
            x_best, y_best = self.Table[index_best, :].copy(), y[index_best].copy()
            self.generation_best_X.append(x_best)
            self.generation_best_Y.append(y_best)

            # подсчёт феромона, который будет добавлен к ребру
            delta_tau = np.zeros((self.n_dim, self.n_dim))
            for j in range(self.size_pop):  # для каждого муравья
                for k in range(self.n_dim - 1):  # для каждой вершины
                    # муравьи перебираются из вершины n1 в вершину n2
                    n1, n2 = self.Table[j, k], self.Table[j, k + 1]
                    delta_tau[n1, n2] += 1 / y[j]  # нанесение феромона
                # муравьи ползут от последней вершины обратно к первой
                n1, n2 = self.Table[j, self.n_dim - 1], self.Table[j, 0]
                delta_tau[n1, n2] += 1 / y[j]  # нанесение феромона

            self.Tau = (1 - self.rho) * self.Tau + delta_tau

        best_generation = np.array(self.generation_best_Y).argmin()
        self.best_x = self.generation_best_X[best_generation]
        self.best_y = self.generation_best_Y[best_generation]

        return self.best_x, self.best_y

    fit = run

def cal_total_distance(routine, distance_matrix, num_points):
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])

if __name__ == "__main__":
    full_timers = []
    
    num_points = 5 # количество вершин
    points_coordinate = np.random.rand(num_points, 2)
    distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    timer_full = 0
    timer_full2 = 0
    iter = 10
    for i in range(iter):
        start_time = time.time()
        aca = ACO_TSP(func=cal_total_distance, n_dim=num_points,
                  size_pop=40,  # количество муравьёв
                  max_iter=10, distance_matrix=distance_matrix)
        best_x, best_y = aca.run()
        
        timer_full += time.time() - start_time
        
        start_time = time.time()
        full_combinations(distance_matrix, num_points)
        timer_full2 += time.time() - start_time
    
    full_timers.append([timer_full/iter, timer_full2/iter])
    
    
    num_points = 6 # количество вершин
    points_coordinate = np.random.rand(num_points, 2)
    distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    timer_full = 0
    timer_full2 = 0
    for i in range(iter):
        start_time = time.time()
        aca = ACO_TSP(func=cal_total_distance, n_dim=num_points,
                  size_pop=40,  # количество муравьёв
                  max_iter=10, distance_matrix=distance_matrix)
        best_x, best_y = aca.run()
        
        timer_full += time.time() - start_time
        
        start_time = time.time()
        full_combinations(distance_matrix, num_points)
        timer_full2 += time.time() - start_time
    
    full_timers.append([timer_full/iter, timer_full2/iter])
    
    num_points = 7 # количество вершин
    points_coordinate = np.random.rand(num_points, 2)
    distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    timer_full = 0
    timer_full2 = 0
    for i in range(iter):
        start_time = time.time()
        aca = ACO_TSP(func=cal_total_distance, n_dim=num_points,
                  size_pop=40,  # количество муравьёв
                  max_iter=10, distance_matrix=distance_matrix)
        best_x, best_y = aca.run()
        
        timer_full += time.time() - start_time
        
        start_time = time.time()
        full_combinations(distance_matrix, num_points)
        timer_full2 += time.time() - start_time
    
    full_timers.append([timer_full/iter, timer_full2/iter])
    
    num_points = 8 # количество вершин
    points_coordinate = np.random.rand(num_points, 2)
    distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    timer_full = 0
    timer_full2 = 0
    for i in range(iter):
        start_time = time.time()
        aca = ACO_TSP(func=cal_total_distance, n_dim=num_points,
                  size_pop=40,  # количество муравьёв
                  max_iter=10, distance_matrix=distance_matrix)
        best_x, best_y = aca.run()
        
        timer_full += time.time() - start_time
        
        start_time = time.time()
        full_combinations(distance_matrix, num_points)
        timer_full2 += time.time() - start_time
    
    full_timers.append([timer_full/iter, timer_full2/iter])
    
    num_points = 9 # количество вершин
    points_coordinate = np.random.rand(num_points, 2)
    distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    timer_full = 0
    timer_full2 = 0
    for i in range(iter):
        start_time = time.time()
        aca = ACO_TSP(func=cal_total_distance, n_dim=num_points,
                  size_pop=40,  # количество муравьёв
                  max_iter=10, distance_matrix=distance_matrix)
        best_x, best_y = aca.run()
        
        timer_full += time.time() - start_time
        
        start_time = time.time()
        full_combinations(distance_matrix, num_points)
        timer_full2 += time.time() - start_time
    
    full_timers.append([timer_full/iter, timer_full2/iter])
    
    points = [5, 6, 7, 8, 9]
    
    ants =  [i[0] for i in full_timers]
    print(ants)
    
    comb =  [i[1] for i in full_timers]
    print(comb)
    fig = plt.figure(figsize = (10, 7))
    plot = fig.add_subplot()
    plot.plot(points,ants, marker='o', label = " Муравьиный алгоритм")
    plot.plot(points, comb, '--', marker='o',label = "Полный перебор")
    
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики муравьиного алгоритма")
    plt.ylabel("Затраченное время (секунды)")
    plt.xlabel("Количество вершин")

    
    
    plt.show()

    print(full_timers) # вычисление времени выполнения