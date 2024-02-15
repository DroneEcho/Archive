#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
int multMatrix(int **matrix1, int **matrix2, int **matrix_res, size_t n1, size_t m1, size_t m2);
int Vinograd(int **matrix1, int **matrix2, int **matrix_res, size_t n1, size_t m1, size_t m2);
int Vinograd_Opt(int **matrix1, int **matrix2, int **matrix_res, size_t n1, size_t m1, size_t m2);
int **alloc_matrix(size_t m, size_t n);
int create_matrix(int ***a, size_t *m, size_t *n);
void free_matrix(int ***m);
int input_matrix(int **a, size_t m, size_t n);
void output_matrix(int **a, size_t m, size_t n);

int multMatrix(int **matrix1, int **matrix2, int **matrix_res, size_t n1, size_t m1, size_t m2){
	for (size_t i = 0; i < n1; i++) {
		for (size_t j = 0; j < m2; j++) {
			matrix_res[i][j] = 0;
			for (size_t k = 0; k < m1; k++) {
				matrix_res[i][j] += matrix1[i][k] * matrix2[k][j];
			}
		}
	}
	return 0;
}

int Vinograd(int **matrix1, int **matrix2, int **matrix_res, const size_t n1, size_t m1, size_t m2)
{
    //printf("\n%d\n", n1);
    //int row[n1];
    int *rowCnt = (int*)malloc(n1 * sizeof(int));
    /*
    if (rowCnt == NULL)
        return -1;
    */
    int *colCnt = (int*)malloc(m2 * sizeof(int));;
    /*
    if (&colCnt == NULL)
        free(rowCnt);
        return -1;
    */
    for (size_t i = 0; i < n1; i++)
    {
        rowCnt[i] = 0;
        for (size_t j = 0; j < m1 / 2; j++)
            rowCnt[i] = rowCnt[i] + matrix1[i][j * 2] * matrix1[i][(j*2) + 1];
        //printf("%d ", rowCnt[i]);
    }
    //printf("\n");
    for (size_t i = 0; i < m2; i++)
    {
        colCnt[i] = 0;
        for (size_t j = 0; j < m1 / 2; j++)
            colCnt[i] = colCnt[i] + matrix2[j * 2][i] * matrix2[j*2 + 1][i];
    }

    for (size_t i = 0; i < n1; i++) {
        for (size_t j = 0; j < m2; j++) {
            matrix_res[i][j] = -rowCnt[i] - colCnt[j];
            for (size_t k = 0; k < m1 / 2; k++) {
                matrix_res[i][j] += (matrix1[i][2*k] + matrix2[2*k+1][j]) * \
                (matrix1[i][2*k+1] + matrix2[2*k][j]);
            }
        }
    }
    if (m1 % 2 == 1)
    {
        for (size_t i = 0; i < n1; i++)
            for (size_t j = 0; j < m2; j++)
                matrix_res[i][j] = matrix_res[i][j] + matrix1[i][m1 - 1] * matrix2[m1 - 1][j];
    }

    free(rowCnt);
    free(colCnt);
    return 0;
}

int Vinograd_Opt(int **matrix1, int **matrix2, int **matrix_res, size_t n1, size_t m1, size_t m2)
{
    //printf("\n%d\n", n1);
    //int row[n1];
    int *rowCnt = (int*)malloc(n1 * sizeof(int));
    /*
    if (rowCnt == NULL)
        return -1;
    */
    int *colCnt = (int*)malloc(m2 * sizeof(int));;
    /*
    if (&colCnt == NULL)
        free(rowCnt);
        return -1;
    */
    for (size_t i = 0; i < n1; i++)
    {
        rowCnt[i] = 0;
        for (int j = 0; j < m1 / 2; j++){
            //printf("%d %d\n", j* 2, j<<1);
            rowCnt[i] += matrix1[i][j << 1] * matrix1[i][(j<<1) + 1];
        //printf("%d ", rowCnt[i]);
        }
    }
    //printf("\n");
    for (size_t i = 0; i < m2; i++)
    {
        colCnt[i] = 0;
        for (int j = 0; j < m1 / 2; j++){
            //printf("j2: %d %d\n", j* 2, j<<1);
            colCnt[i] += matrix2[j * 2][i] * matrix2[(j<<1) + 1][i];
        }
    }

    for (size_t i = 0; i < n1; i++) {
        for (size_t j = 0; j < m2; j++) {
            matrix_res[i][j] = -rowCnt[i] - colCnt[j];
            for (int k = 0; k < m1 / 2; k++) {
                //printf("k: %d %d\n", k* 2, k<<1);
                matrix_res[i][j] += (matrix1[i][k<<1] + matrix2[(k<<1)+1][j]) * \
                (matrix1[i][2*k+1] + matrix2[2*k][j]);
            }
        }
    }
    if (m1 % 2 == 1)
    {
        for (size_t i = 0; i < n1; i++)
            for (size_t j = 0; j < m2; j++)
                matrix_res[i][j] += matrix1[i][m1 - 1] * matrix2[m1 - 1][j];
    }

    free(rowCnt);
    free(colCnt);
    return 0;
}

int **alloc_matrix(size_t m, size_t n)
{
    size_t i;
    int **a = malloc(m * sizeof(int*) + m * n * sizeof(int));
    
    if (a == NULL)
        return NULL;
    
    for (i = 0; i < m; i++)
    {
        a[i] = (int*)((int8_t*) a + m * sizeof(int*) + n * i * sizeof(int));
    }
    
    return a;
}
int create_matrix(int ***a, size_t *m, size_t *n)
{    
    // Ввод размеров матрицы
    if (scanf("%zu %zu", m, n) != 2 || *m == 0 || *n == 0)
        return -1;
    
    // Проверка на отрицательные размерыы
    size_t max_size_t = (size_t) -1;
    if (*m > max_size_t / 2 || *n > max_size_t / 2)
        return -1;
    
    // Выделение памяти под матрицу
    *a = alloc_matrix(*m, *n);
    if (*a == NULL)
        return -2;
    
    // Ввод матрицы
    if (input_matrix(*a, *m, *n) != 0)
    {
        free_matrix(a);
        return -2;
    }
    
    return 0;
}
void free_matrix(int ***m)
{
    free(*m);
    *m = NULL;
}
int input_matrix(int **a, size_t m, size_t n)
{
    int i, j;
    
    for (i = 0; i < m; i++)
    {
        for (j = 0; j < n; j++)
        {
            if (scanf("%ld", &a[i][j]) != 1)
                return -1;
        }
    }
    
    return 0;
}
void output_matrix(int **a, size_t m, size_t n)
{
    size_t i, j;
    
    for (i = 0; i < m; i++)
    {
        for (j = 0; j < n; j++)
        {
            printf("%ld ", a[i][j]);
        }
        printf("\n");
    }
}


int main(void)
{
    setbuf(stdout, NULL);
    
    int rc;
    int **a, **b, **res;
    size_t m, n, p, q;
    unsigned int r, y;
    printf("Создание матрицы А\n");
    // Создание и ввод матрицы A
    rc = create_matrix(&a, &m, &n);
    if (rc)
        return rc;
    printf("Создание матрицы B\n");
    // Создание и ввод матрицы B
    printf("ПЕРВОЕ ЧИСЛО ДОЛЖНО БЫТЬ %zu!!\n\n", n);
    rc = create_matrix(&b, &p, &q);
    if (rc)
    {
        free_matrix(&a);
        printf("\nERR create\n");
        return rc;
    }
    if (n != p)
    {
        printf("неверные размеры для умножения!");
        free_matrix(&a);
        free_matrix(&b);
        return -2;
    }
    res = alloc_matrix(m, q);
    if (res == NULL)
    {
        printf("\nERR create\n");
        free_matrix(&a);
        free_matrix(&b);
        return -2;
    }
    // Перемножение матриц A и B
    multMatrix(a, b, res, m, n, q);
    
    // Вывод
    printf("\n\nВывод простого умножения: \n");
    output_matrix(res, m, q);
    
    //Виноград
    rc = Vinograd(a, b, res, m, n, q);

    if (rc != 0)
    {
        free_matrix(&a);
        free_matrix(&b);
        free_matrix(&res);
        printf("\nERR count1\n");
        return rc;
    }
    // Вывод
    printf("\n\nВывод Виноград умножения: \n");
    output_matrix(res, m, q);

    //Виноград опт
    rc = Vinograd_Opt(a, b, res, m, n, q);

    if (rc != 0)
    {
        free_matrix(&a);
        free_matrix(&b);
        free_matrix(&res);
        printf("\nERR count2\n");
        return rc;
    }
    // Вывод
    printf("\n\nВывод опт Виноград умножения: \n");
    output_matrix(res, m, q);

    // Освобождение памяти
    free_matrix(&a);
    free_matrix(&b);
    free_matrix(&res);
 
    return 0;
}