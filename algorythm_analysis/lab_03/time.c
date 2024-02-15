#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

// Функция Шейкер-сортировки
void ShakerSort(int *to_sort, int c)
{
    int left = 0, right = c - 1;
    int flag = 1, t;
    while ((left < right) && flag > 0) {
        flag = 0;
        for (int i = left; i < right; i++) {
            if (to_sort[i] > to_sort[i + 1])
            {
                t = to_sort[i];
                to_sort[i] = to_sort[i + 1];
                to_sort[i + 1] = t;
                flag = 1;
        }
        }
        right--;
        for (int i = right; i > left; i--) {
            if (to_sort[i - 1] > to_sort[i])
            {
                int t = to_sort[i];
                to_sort[i] = to_sort[i - 1];
                to_sort[i - 1] = t;
                flag = 1;
            }
        }
        left++;
    }
}

//сортировка методом Шелла
void ShellSort(int *to_sort, int c)
{
    int i, j, step;
    int tmp;
    for (step = c / 2; step > 0; step /= 2)
        for (i = step; i < c; i++) {
            tmp = to_sort[i];
            for (j = i; j >= step; j -= step)
            {
                if (tmp < to_sort[j - step])
                    to_sort[j] = to_sort[j - step];
                else
                    break;
            }
            to_sort[j] = tmp;
        }
}

//плавная сортировка
void SmoothSort(int *arr, int c) {
    int gap = 1;
    // Вычисляем начальный зазор
    while (gap < c) {
        gap = gap * 3 + 1;
    }
     
    while (gap > 1) {
        // Уменьшаем зазор по формуле Роберта Седжвика
        gap = (gap - 1) / 3;
         
        for (int i = gap; i < c; i++) {
            int temp = arr[i];
            int j;
             
            for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                arr[j] = arr[j - gap];
            }
             
            arr[j] = temp;
        }
    }
}

int main(void)
{
    //милисек
    clock_t time;
    setbuf(stdout, NULL);
    srand(1);

    int *a, *b, *c, *mas_buf;
    size_t m;

    double t1_shaker = 0;
    double t1_shell = 0;
    double t1_smooth = 0;

    for (int j = 500; j < 5001; j = j+500)
    {
        t1_shaker = 0;
        t1_shell = 0;
        t1_smooth = 0;
        //printf("cycle 1\n");
        m = j;
        
        a = (int*) malloc(m * sizeof(int));
        b = (int*) malloc(m * sizeof(int));
        c = (int*) malloc(m * sizeof(int));
        mas_buf = (int*) malloc(m * sizeof(int));
        int buf;
        for(int i = 0; i < m; i++)
        {
            buf = rand () % 100;
            /*
            a[i] = buf;
            b[i] = buf;
            c[i] = buf;
            */
            mas_buf[i] = buf;
        }
        ShakerSort(mas_buf, m);

        int k;
        for (int i = 0; i < m/2; i++)
        {
            if (i == 0)
                k = 1;
            else
                k = 0;
            buf = mas_buf[i];
            mas_buf[i] = mas_buf[m - (i+k)];
            mas_buf[m - (i+k)] = buf;
        }

        if (j == 500)
        {
            for (int i = 0; i < m; i++)
        {
            printf("%d ", mas_buf[i]);
        }
        }
        for (int i = 0; i < 100; i++)
        { 
            for(int k = 0; k < m; k++)
            {
            a[k] = mas_buf[k];
            b[k] = mas_buf[k];
            c[k] = mas_buf[k];
            }
            
            time=clock();
            ShakerSort(a, m);
            time = clock() - time;
            t1_shaker += time;

            time=clock();
            ShellSort(b, m);
            time = clock() - time;
            t1_shell += time;

            time=clock();
            SmoothSort(c, m);
            time = clock() - time;
            t1_smooth += time;

            
            //input_matrix(*a, m, n);
            //input_matrix(*b, m, n);
        }
    

        printf("%d: shaker:%f shell:%f smooth: %f\n",j, t1_shaker/100/CLOCKS_PER_SEC, t1_shell/100/CLOCKS_PER_SEC, t1_smooth/100/CLOCKS_PER_SEC);

        free(a);
        free(b);
        free(c);
        free(mas_buf);
    }
}