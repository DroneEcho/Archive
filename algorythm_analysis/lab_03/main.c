#define _CRT_SECURE_NO_WARNINGS // для корректной работы scanf()
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
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
        for (int i = step; i < c; i++) {
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

int main() {

    int a[10], b[10], c[10];
    int buf;
    // Вводим элементы массива
    for (int i = 0; i < 10; i++) {
        printf("a[%d]=", i);
        scanf("%d", &buf);
        a[i] = buf;
        b[i] = buf;
        c[i] = buf;
    }

    ShakerSort(&a, 10);
    ShellSort(&b, 10);
    SmoothSort(&c, 10);
    
    // Выводим отсортированные элементы массива
    printf("\n\n");
    for (int i = 0; i<10; i++)
    printf("%d ", a[i]);

    printf("\n\n");

    for (int i = 0; i<10; i++)
    printf("%d ", b[i]);

    printf("\n\n");

    for (int i = 0; i<10; i++)
    printf("%d ", c[i]);

	return 0;
}