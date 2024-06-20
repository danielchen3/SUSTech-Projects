#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// 双重指针的运算函数
void multiplyMatrices(float **matrix1, float **matrix2, float **result, int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < n; k++)
        {
            for (int j = 0; j < n; j++)
            {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
}

// 单指针存储下的运算
void matrixMultiplication(int *mat1, int *mat2, int *result, int n)
{
    int i, j, k;
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            *(result + i * n + j) = 0;
            for (k = 0; k < n; k++)
            {
                *(result + i * n + k) += *(mat1 + i * n + j) * *(mat2 + j * n + k);
            }
        }
    }
}

int main()
{
    // int m1Rows, m1Cols, m2Rows, m2Cols;
    int testcases[] = {15000, 10000, 5000, 3000, 2000, 1000, 500, 200, 100, 10};

    // printf("Enter the number of rows and columns for the first matrix: ");
    // scanf("%d %d", &m1Rows, &m1Cols);

    // printf("Enter the number of rows and columns for the second matrix: ");
    // scanf("%d %d", &m2Rows, &m2Cols);

    // if (m1Cols != m2Rows)
    // {
    //     printf("Cannot multiply matrices. Number of columns in the first matrix must be equal to the number of rows in the second matrix.");
    //     return 0;
    // }

    for (int testcase = 0; testcase < 10; testcase++)
    {

        // 双指针存储分配内存空间
        float **matrix1 = (float **)malloc(testcases[testcase] * sizeof(float *));
        float **matrix2 = (float **)malloc(testcases[testcase] * sizeof(float *));
        float **result = (float **)malloc(testcases[testcase] * sizeof(float *));
        for (int i = 0; i < testcases[testcase]; i++)
        {
            matrix1[i] = (float *)malloc(testcases[testcase] * sizeof(float));
            result[i] = (float *)malloc(testcases[testcase] * sizeof(float));
        }
        for (int i = 0; i < testcases[testcase]; i++)
        {
            matrix2[i] = (float *)malloc(testcases[testcase] * sizeof(float));
        }

        // int *matrix1 = (int *)malloc(testcases[testcase] * testcases[testcase] * sizeof(int));
        // int *matrix2 = (int *)malloc(testcases[testcase] * testcases[testcase] * sizeof(int));
        // int *result = (int *)malloc(testcases[testcase] * testcases[testcase] * sizeof(int));
        float upper = 10;

        // 分配初始值
        // for (int i = 0; i < testcases[testcase]; i++)
        // {
        //     for (int j = 0; j < testcases[testcase]; j++)
        //     {
        //         float num = (float)1.0 * rand() / RAND_MAX * upper;
        //         *(matrix1 + i * testcases[testcase] + j) = num;
        //     }
        // }

        // for (int i = 0; i < testcases[testcase]; i++)
        // {
        //     for (int j = 0; j < testcases[testcase]; j++)
        //     {
        //         float num = (float)1.0 * rand() / RAND_MAX * upper;
        //         *(matrix2 + i * testcases[testcase] + j) = num;
        //     }
        // }

        // for (int i = 0; i < testcases[testcase]; i++)
        // {
        //     for (int j = 0; j < testcases[testcase]; j++)
        //     {
        //         *(result + i * testcases[testcase] + j) = 0.0f;
        //     }
        // }

        // 分配初始值

        for (int i = 0; i < testcases[testcase]; i++)
        {
            for (int j = 0; j < testcases[testcase]; j++)
            {
                float randnumber1 = 1.0 * rand() / RAND_MAX * upper;
                matrix1[i][j] = randnumber1;
            }
        }

        for (int i = 0; i < testcases[testcase]; i++)
        {
            for (int j = 0; j < testcases[testcase]; j++)
            {
                float randnumber2 = 1.0 * rand() / RAND_MAX * upper;
                matrix2[i][j] = randnumber2;
            }
        }

        for (int i = 0; i < testcases[testcase]; i++)
        {
            for (int j = 0; j < testcases[testcase]; j++)
            {
                result[i][j] = 0.0f;
            }
        }

        // 计算矩阵乘法的运行时间
        clock_t start = clock();
        multiplyMatrices(matrix1, matrix2, result, testcases[testcase]);
        // matrixMultiplication(matrix1, matrix2, result, testcases[testcase]);
        clock_t end = clock();
        double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

        FILE *fp;
        fp = fopen("output.txt", "a");
        if (fp == NULL)
        {
            printf("无法打开");
            return 1;
        }

        fprintf(fp, "Sizeof %d ", testcases[testcase]);
        fprintf(fp, "Time taken(seconds): ");
        fprintf(fp, "%.10f\n", time_spent);

        // 输出结果
        // fprintf(fp, "Result of matrix multiplication:\n");
        // for (int i = 0; i < testcases[testcase]; i++)
        // {
        //     for (int j = 0; j < testcases[testcase]; j++)
        //     {
        //         fprintf(fp, "%.2f ", result[i][j]);
        //     }
        //     fprintf(fp, "\n");
        // }

        // 双指针存储内存释放
        for (int i = 0; i < testcases[testcase]; i++)
        {
            free(matrix1[i]);
            free(result[i]);
        }
        for (int i = 0; i < testcases[testcase]; i++)
        {
            free(matrix2[i]);
        }

        // 单指针存储内存释放
        // free(matrix1);
        // free(matrix2);
        // free(result);
    }

    return 0;
}
