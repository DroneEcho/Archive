from time import perf_counter
import threading
from multiprocessing import Process, Pipe
import os
import random
import string
import matplotlib.pyplot as plt

def bad_char_heuristic(pattern):
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    return bad_char
# Ввод
#     pattern - искомая подстрока
# Вывод
#     содержит информацию о суффиксах и их связях
def good_suffix_heuristic(pattern):
    good_suffix = [-1] * (len(pattern) + 1)
    border = [0] * (len(pattern) + 1)
    i = len(pattern)
    j = len(pattern) + 1
    border[i] = j
    while i > 0:
        while j <= len(pattern) and pattern[i - 1] != pattern[j - 1]:
            if good_suffix[j] == 0:
                good_suffix[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j
    j = border[0]
    for i in range(len(pattern) + 1):
        if good_suffix[i] == -1:
            good_suffix[i] = j
        if i == j:
            j = border[j]
    return good_suffix
# Ввод
#     text - строка, в которой будет искаться подстрока
#     pattern - искомая подстрока
# Вывод
#     массив индексов, в которых находится подстрока
def bouer_moor(text, pattern):
    bad_char = bad_char_heuristic(pattern)
    good_suffix = good_suffix_heuristic(pattern)
    i = 0
    indexes = []
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            indexes.append(i)
            i += good_suffix[0]
        else:
            x = j - bad_char.get(text[i + j], -1)
            y = good_suffix[j + 1]
            i += max(x, y)
    return indexes


def bouer_moor_thread(thread_results_pipe, text, pattern, good_suffix, bad_char, start, end):
    indexes = []
    pattern_len = len(pattern)
    i = start
    text_len = len(text) if end + pattern_len > len(text) else end + pattern_len
    
    #print(i, " to ", text_len, "\n")
    while i <= text_len - pattern_len:
        j = pattern_len - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            indexes.append(i)
            i += good_suffix[0]
        else:
            x = j - bad_char.get(text[i + j], -1)
            y = good_suffix[j + 1]
            if (max(x, y) > text_len - pattern_len and max(x, y) < text_len):
                i = text_len - pattern_len
            else:
                i += max(x, y)
    #print("ended", indexes)
    #thread_results_pipe.send(indexes)
    



def bouer_moor_parallel(text, pattern, thread_num):
    thread_results_pipe,thread_results_pipe_recieve = Pipe()
    thread_results = []
    bad_char = bad_char_heuristic(pattern)
    good_suffix = good_suffix_heuristic(pattern)
    text_len = len(text)
    
    text_slice = int(text_len / thread_num)
    
    k = 0
        
    threads = []
    for i in range(thread_num):
        k_end = k + text_slice
        if (i == thread_num - 1):
            k_end = text_len
        threads.append(threading.Thread(target=bouer_moor_thread, args=(thread_results_pipe, text, pattern, \
                                                               good_suffix, bad_char, k, k_end,)))
        k += text_slice
    
    time_start = perf_counter()
    for thread in threads:
        thread.start()
    
    for thread in threads:
        #thread_results.append(thread_results_pipe_recieve.recv())
        thread.join()
    time_finish = perf_counter() - time_start
    return time_finish
    
if __name__ =="__main__":
    
    txts = ["1.txt","2.txt","3.txt","4.txt","5.txt", "6.txt", "7.txt"]
    mbs = [1, 2, 3, 4, 5, 6, 7]
    bouer = []
    bouer_2 = []
    bouer_4 = []
    bouer_8 = []
    bouer_16 = []
    for txt in txts:
        f = open(txt, "r+")
        try:
            source = f.read()
        finally:
            f.close()
        print(txt + "\n") 
        time_finish_b = 0
        time_finish_b2 = 0
        time_finish_b4 = 0
        time_finish_b8 = 0
        time_finish_b16 = 0
        for i in range(10):
                        
            time_finish_b2 += bouer_moor_parallel(source, "ada", 16)
    
            time_finish_b4 += bouer_moor_parallel(source, "ada", 32)
           
            time_finish_b8 += bouer_moor_parallel(source, "ada", 64)

            
        bouer.append(time_finish_b / 10)
        bouer_2.append(time_finish_b2 / 10)
        bouer_4.append(time_finish_b4 / 10)
        bouer_8.append(time_finish_b8 / 10)
        bouer_16.append(time_finish_b16 / 10)
    
    fig = plt.figure(figsize = (10, 7))
    plot = fig.add_subplot()
    plot.plot(mbs, bouer_2, marker='o', label = " Алг. Бойера--Мура (16 потоков)")
    plot.plot(mbs, bouer_4, '--', marker='o',label = "Алг. Бойера--Мура (32 потока)")
    plot.plot(mbs, bouer_8, ':', marker='o',label = "Алг. Бойера--Мура (64 потока)")
    
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритма Бойера--Мура")
    plt.ylabel("Затраченное время (секунды)")
    plt.xlabel("Размер файла (мб)")

    
    
    plt.show()

        