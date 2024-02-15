import math


def func(n):
    
    m = list([0] * (n + 1))
    ans = []
    if n < 3:
        return ans
    n2 = int(math.sqrt(n))
    m[2], m[3] = True, True
    for i in range( 1, n2 + 1):
        x2 = i * i
        for j in range(1, n2 + 1):
            y2 = j * j
            lim = 4*x2 + y2

            if (lim <= n) and (lim % 12 == 1 or lim % 12 == 5):
                m[lim] = not m[lim]

            lim = 3*x2 + y2
            if (lim <= n) and (lim % 12 == 7):
                m[lim] = not m[lim]
            
            lim = 3*x2 - y2
            if (i > j) and (lim <= n) and (lim % 12 == 11):
                m[lim] = not m[lim]
    
    for i in range(5, n2):
        if (m[i]):
            x2 = i * i
            for i in range(x2, n, x2):
                m[j] = False
    
    for x in range(n):
        if x > 1 and m[x] == True: 
            ans.append(x)
   
    return ans



name = input().strip()
Upper = 0
flag = False
if name.isalpha():
    for i in (name):
        if i.isupper():
            Upper += 1
            flag = True
            if Upper > 1:
                flag = False
                break

print(flag)