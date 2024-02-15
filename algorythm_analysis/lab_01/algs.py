from funcs import *

"""
    Матричный метод поиска Левенштейна
"""
def levenshtein_matrix(str1, str2, output = False):
    n = len(str1)
    m = len(str2)
    
    if n == 0 or m == 0:
        if n != 0:
            return n
        if m != 0:
            return m
        return 0
    
    matrix = create_matrix(n + 1, m + 1)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            change = 0 
            if (str1[i - 1] != str2[j - 1]):
                change += 1
                
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + change)
            
    if output:        
        print_matrix(str1, str2, matrix)
    return(matrix[-1][-1])

"""
    Нерекурсивный метод поиска Дамерау-Левенштейна
"""
def damerau_levenshtein_matrix(str1, str2, output = False):
    n = len(str1)
    m = len(str2)
    
    if n == 0 or m == 0:
        if n != 0:
            return n
        if m != 0:
            return m
        return 0
    
    matrix = create_matrix(n + 1, m + 1)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            change = 0 
            if (str1[i - 1] != str2[j - 1]):
                change += 1
                
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + change)
            #Дамерау - 
            if (i > 1 and j > 1) and str1[i-1] == str2[j-2] and str1[i-2] == str2[j-1]:
                matrix[i][j] = min(matrix[i][j], matrix[i-2][j-2] + 1)
    if output:        
        print_matrix(str1, str2, matrix)
    return(matrix[-1][-1])

"""
    рекурсивный метод поиска Дамерау-Левенштейна
"""
def damerau_levenshtein_recursive(str1, str2, out_put = False):
    n = len(str1)
    m = len(str2)

    if n == 0 or m == 0:
        if n != 0:
            return n
        if m != 0:
            return m
        return 0

    change = 0
    if str1[-1] != str2[-1]:
        change += 1

    min_ret = min(damerau_levenshtein_recursive(str1[:n - 1], str2) + 1,
                      damerau_levenshtein_recursive(str1, str2[:m - 1]) + 1,
                      damerau_levenshtein_recursive(str1[:n - 1], str2[:m - 1]) + change)
    if n > 1 and m > 1 and str1[-1] == str2[-2] and str1[-2] == str2[-1]:
        min_ret = min(min_ret,
                      damerau_levenshtein_recursive(str1[:n - 2], str2[:m - 2]) + 1)

    return min_ret

"""
    рекурсивный с кешированием метод поиска Дамерау-Левенштейна
"""
def recursive(str1, str2, n, m, matrix):
        if (matrix[n][m] != -1):
            return matrix[n][m]

        if (n == 0):
            matrix[n][m] = m
            return matrix[n][m]

        if (n > 0 and m == 0):
            matrix[n][m] = n
            return matrix[n][m]

        delete = recursive(str1, str2, n - 1, m, matrix) + 1
        add = recursive(str1, str2, n, m - 1, matrix) + 1

        change = 0

        if (str1[n - 1] != str2[m - 1]):
            change = 1

        change = recursive(str1, str2, n - 1, m - 1, matrix) + change
        
        matrix[n][m] = min(add, delete, change)
        if n > 1 and m > 1 and str1[n - 1] == str2[m - 2] and str1[n - 2] == str2[m - 1]:
            swap = recursive(str1, str2, n - 2, m - 2, matrix) + 1
            matrix[n][m] = min(matrix[n][m], swap)
        return matrix[n][m]

def damerau_levenshtein_recursive_cash(str1, str2, output = False):
    n = len(str1)
    m = len(str2)
    
    if n == 0 or m == 0:
        if n != 0:
            return n
        if m != 0:
            return m
        return 0

    matrix =  create_matrix(n + 1, m + 1)

    for i in range(n + 1):
        for j in range(m + 1):
            matrix[i][j] = -1

    recursive(str1, str2, n, m, matrix)

    if output:
        print("Расстояние, вычисленное с помощью матрицы Дамерау - Левенштейна (рекурсивно кеш)")
        print_matrix(str1, str2, matrix)
        print("Расстояние равно ", matrix[n][m])

    return matrix[n][m]

