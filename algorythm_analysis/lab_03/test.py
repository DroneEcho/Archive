
import matplotlib.pyplot as plt


y_time_random = [[0.000480, 0.000020 , 0.000010]
		, [0.001510 , 0.000060 ,0.000090]
		, [0.003550 , 0.000070 , 0.000120] 
		, [0.005940 , 0.000120 , 0.000170]
		, [0.009570 , 0.000220 , 0.000200] 
		, [0.014710 , 0.000230 , 0.000210] 
		, [0.019260 , 0.000300 , 0.000250] 
		, [0.026680 , 0.000330 , 0.000320] 
		, [0.033320 , 0.000470 , 0.000375] 
		, [0.040930 , 0.000470 , 0.000390]]

y_time_sorted = [[0.000020 , 0.000000 , 0.000010]
		, [0.000030 , 0.000050 ,0.000010] 
		, [0.000040 , 0.000070 , 0.000030]
		, [0.000080 , 0.000095 , 0.000060]
		, [0.000110 , 0.000140 , 0.000070]
		, [0.000160 , 0.000160 , 0.000072]
		, [0.000210 , 0.000180 , 0.000076]
		, [0.000290 , 0.000192 , 0.000120]
		, [0.000360 , 0.000220 , 0.000125]
		, [0.000460 , 0.000240 , 0.000150]]

y_time_revrse = [[0.000390 , 0.000020 , 0.000010]
		, [0.001540 , 0.000090 ,0.000030]
		, [0.003280 , 0.000120 , 0.000040]
		, [0.005990 , 0.000120 , 0.000050]
		, [0.009460 , 0.000140 , 0.000050]
		, [0.013000 , 0.000160 , 0.000060]
		, [0.017650 , 0.000200 , 0.000090]
		, [0.023050 , 0.000200 , 0.000150]
		, [0.028870 , 0.000240 , 0.000220]
		, [0.036060 , 0.000250 , 0.000220]]

if __name__ == "__main__":
    y_time_shake = []
    y_time_shell = []
    y_time_smooth = []

    for elem in y_time_random:
        y_time_shake.append(elem[0])
        y_time_shell.append(elem[1])
        y_time_smooth.append(elem[2])
    len_arr = []
    for i in range(500, 5001, 500):
        len_arr.append(i)
        
    fig, (plot) = plt.subplots(1, 2)
    #plot = fig.add_subplot()
    #plot_only = fig.add_subplot()
    plot[1].plot(len_arr, y_time_shell,'-.', label = "Сортировка Шелла", marker='D')
    plot[1].plot(len_arr, y_time_smooth, '--', label = "Плавная сортировка", marker='D')
    plot[0].plot(len_arr, y_time_shake, label = "Сортировка перемешиванием", marker='D')
    plot[0].plot(len_arr, y_time_shell,'-.', label = "Сортировка Шелла", marker='D')
    plot[0].plot(len_arr, y_time_smooth, '--', label = "Плавная сортировка", marker='D')
    fig.suptitle("Временные характеристики алгоритмов сортировки со случайными данными")
    
    for plot in plot.flat:
        plot.legend()
        plot.grid()
        plot.set(ylabel ="Затраченное время (мс)", xlabel ="Размер массива")
        

    plt.show()
    
    y_time_shake = []
    y_time_shell = []
    y_time_smooth = []
    
    for elem in y_time_sorted:
        y_time_shake.append(elem[0])
        y_time_shell.append(elem[1])
        y_time_smooth.append(elem[2])
    
    fig2 = plt.figure(figsize = (10, 7))
    plot2 = fig2.add_subplot()
    plot2.plot(len_arr, y_time_shake, label = "Сортировка перемешиванием", marker='D')
    plot2.plot(len_arr, y_time_shell,'-.', label = "Сортировка Шелла", marker='D')
    plot2.plot(len_arr, y_time_smooth, '--', label = "Плавная сортировка", marker='D')
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритмов сортировки с отсортированными данными")
    plt.ylabel("Затраченное время (мс)")
    plt.xlabel("Размер массива")

    plt.show()
    
    y_time_shake = []
    y_time_shell = []
    y_time_smooth = []
    
    for elem in y_time_revrse:
        y_time_shake.append(elem[0])
        y_time_shell.append(elem[1])
        y_time_smooth.append(elem[2])
    
    fig1, (plot1) = plt.subplots(1, 2)
    
    plot1[1].plot(len_arr, y_time_shell,'-.', label = "Сортировка Шелла", marker='D')
    plot1[1].plot(len_arr, y_time_smooth, '--', label = "Плавная сортировка", marker='D')
    plot1[0].plot(len_arr, y_time_shake, label = "Сортировка перемешиванием", marker='D')
    plot1[0].plot(len_arr, y_time_shell,'-.', label = "Сортировка Шелла", marker='D')
    plot1[0].plot(len_arr, y_time_smooth, '--', label = "Плавная сортировка", marker='D')
    fig1.suptitle("Временные характеристики алгоритмов сортировки с отсортированными в обратном порядке данными")
    
    for plot in plot1.flat:
        plot.legend()
        plot.grid()
        plot.set(ylabel ="Затраченное время (мс)", xlabel ="Размер массива")
    
    plt.show()