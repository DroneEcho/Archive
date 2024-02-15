import threading
from multiprocessing import Process, Pipe
import os
import random
import string

# Алгоритм Бойера-Мура поиска подстроки в строке (поиск одной и той же подстроки в файле от 100 Мбайт)

# Ввод
#     pattern - искомая подстрока
# Вывод
#     возвращает словарь: символ из шаблона - индекс последнего вхождения
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
    
    print(i, " to ", text_len, "\n")
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
    print("ended", indexes)
    thread_results_pipe.send(indexes)
    return indexes



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
    print("threads inited")
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread_results.append(thread_results_pipe_recieve.recv())
        thread.join()
    
    return thread_results
 
    
def generate():
    name = input("please input new file name: ")
    size = int(input("please input new file size(mb): "))
    
    print("Choose a statement:\n\
            1 - lowercase \n\
            2 - uppercase\n\
            3 - mixed\n\
            4 - digits\n")
    a = int(input("input: "))
    if a == 1:
        chars = ''.join([random.choice(string.ascii_lowercase) for i in range(size*1048576)]) #1
    elif a == 2:
        chars = ''.join([random.choice(string.ascii_uppercase) for i in range(size*1048576)]) #2
    elif a == 3:
        chars = ''.join([random.choice(string.ascii_letters) for i in range(size*1048576)]) #3
    elif a == 4:
        chars = ''.join([random.choice(string.digits) for i in range(size*1048576)]) #4
    else:
        print("Err: abort")

    with open(name, 'w') as f:
        f.write(chars)
    pass


    
def buer_mour_init():
    name = input("please input a file: ")
    try:
        file_size = os.path.getsize(name)
        #if (file_size < 1048576):
        #    raise Exception()
        f = open(name, "r+")
        try:
            source = f.read()
        finally:
            f.close()
    except FileNotFoundError:
        print("ERR: file not found!")
        return
    except Exception:
        print("ERR: file is less than 100mb!")
        return
    
    search = input("input seraching thread: ")
    
    print("Choose a statement:\n\
            1 - test buer-mour algorythm without treads \n\
            2 - test buer-mour algorythm with treads\n")
    a = int(input("input: "))
    if a == 1:
        indexes = bouer_moor(source, search)
        print("indexes of patterns inside: \n", indexes, "\n")
    elif a == 2:
        thread_num = int(input("Input number of threads(2^n)(1,2,4,8 ...64): "))
        indexes = bouer_moor_parallel(source, search, thread_num)
        print("indexes of patterns inside: \n", indexes, "\n")
    else:
        print("Wrong input!\n\n")
    
if __name__ =="__main__":
    loop = 1
    while(loop):
        print("Choose a statement:\n\
            1 - generate a file \n\
            2 - test buer-mour algorythm\n\
            3 - exit\n")
        a = int(input("input: "))
        if a == 1:
            generate()
        elif a == 2:
            buer_mour_init()
        elif a == 3:
            loop = 0
        else:
            print("Wrong input!\n\n")
    