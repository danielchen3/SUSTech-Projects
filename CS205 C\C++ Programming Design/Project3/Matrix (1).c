#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>
#include <time.h>
#include <omp.h>
#include "cblas.h"
#pragma GCC optimize(3)

#ifdef WITH_AVX2
#include <immintrin.h>
#endif

#ifdef WITH_AVX2
#include <omp.h>
#endif

// gcc -o Matrix Matrix.c -DWITH_AVX2 -mavx2 -lopenblas -lpthread

struct Matrix
{
    size_t rows;
    size_t cols;
    float *data;
};

// allocate memory for a matrix
struct Matrix *allocate_Matrix(size_t rows, size_t cols)
{
    struct Matrix *mat = (struct Matrix *)malloc(sizeof(struct Matrix));
    if (mat == NULL)
    {
        printf("内存分配失败\n");
        return NULL;
    }
    mat->rows = rows;
    mat->cols = cols;
    mat->data = (float *)malloc((long long)rows * (long long)cols * sizeof(float));
    if (mat->data == NULL)
    {
        printf("数据内存分配失败\n");
        free(mat);
        return NULL;
    }
    return mat;
}

// Deallocate memory for a matrix
void deallocateMatrix(struct Matrix *mat)
{
    free(mat->data);
    free(mat);
}

// Generate random matrix values
void generateRandomMatrix(struct Matrix *mat)
{
    for (size_t i = 0; i < mat->rows * mat->cols; ++i)
    {
        mat->data[i] = 1; //(float)rand() / RAND_MAX;
    }
}

void matmul_block(const struct Matrix *A, const struct Matrix *B, const struct Matrix *result)
{
    if (A == NULL || B == NULL || result == NULL)
    {
        printf("输入矩阵不能为空\n");
        return;
    }
    if (A->cols != B->rows)
    {
        printf("矩阵尺寸不兼容\n");
        return;
    }
    if (A->rows != result->rows || B->cols != result->cols)
    {
        printf("结果矩阵尺寸不正确\n");
        return;
    }
    size_t i, j, k;
    int block_size = 64;
#pragma omp parallel for collapse(4) num_threads(4)
    for (i = 0; i < A->rows; i += block_size)
    {
        for (k = 0; k < A->cols; k += block_size)
        {
            for (j = 0; j < B->cols; j += block_size)
            {
                for (size_t ii = i; ii < i + block_size && ii < A->rows; ++ii)
                {
                    for (size_t jj = j; jj < j + block_size && jj < B->cols; ++jj)
                    {
                        __m256 sum_vec = _mm256_setzero_ps();
                        for (size_t kk = k; kk < k + block_size && kk < A->cols; kk += 8)
                        {
                            __m256 a_vec = _mm256_loadu_ps(&A->data[ii * A->cols + kk]);
                            // 加载 B 矩阵的 8 个元素到 SSE 寄存器
                            __m256 b_vec = _mm256_loadu_ps(&B->data[kk * B->cols + jj]);
                            // 使用 SIMD 指令进行乘法运算
                            __m256 mul_vec = _mm256_mul_ps(a_vec, b_vec);
                            // 将乘法结果累加到 sum_vec 中
                            sum_vec = _mm256_add_ps(sum_vec, mul_vec);
                            // C->data[ii * C->cols + jj] += A->data[ii * A->cols + kk] * B->data[kk * B->cols + jj];
                        }
                        result->data[ii * result->cols + jj] += sum_vec[0] + sum_vec[1] + sum_vec[2] + sum_vec[3] + sum_vec[4] + sum_vec[5] + sum_vec[6] + sum_vec[7];
                    }
                }
            }
        }
    }
}

// Function to perform matrix multiplication
void matmul_plain(const struct Matrix *A, const struct Matrix *B, const struct Matrix *result)
{
    if (A == NULL || B == NULL || result == NULL)
    {
        printf("输入矩阵不能为空\n");
        return;
    }
    if (A->cols != B->rows)
    {
        printf("矩阵尺寸不兼容\n");
        return;
    }
    if (A->rows != result->rows || B->cols != result->cols)
    {
        printf("结果矩阵尺寸不正确\n");
        return;
    }
    size_t i, j, k;
    for (i = 0; i < A->rows; ++i)
    {
        for (k = 0; k < A->cols; ++k)
        {
            for (j = 0; j < B->cols; ++j)
            {
                result->data[i * result->cols + j] += A->data[i * A->cols + k] * B->data[k * B->cols + j];
            }
        }
    }
}

void matmul_improved(const struct Matrix *A, const struct Matrix *B, const struct Matrix *result)
{
    if (A == NULL || B == NULL || result == NULL)
    {
        printf("输入矩阵不能为空\n");
        return;
    }
    if (A->cols != B->rows)
    {
        printf("矩阵尺寸不兼容\n");
        return;
    }
    if (A->rows != result->rows || B->cols != result->cols)
    {
        printf("结果矩阵尺寸不正确\n");
        return;
    }

    size_t i, j, k;

    for (i = 0; i < A->rows; ++i)
    {
        for (j = 0; j < B->cols; ++j)
        {
            __m256 sum_vec = _mm256_setzero_ps(); // 使用 SSE 寄存器进行累加
            for (k = 0; k < A->cols / 8; ++k)
            {
                __m256 a_vec = _mm256_loadu_ps(&A->data[i * A->cols + k]);
                // 加载 B 矩阵的 4 个元素到 SSE 寄存器
                __m256 b_vec = _mm256_loadu_ps(&B->data[k * B->cols + j]);
                // 使用 SIMD 指令进行乘法运算
                __m256 mul_vec = _mm256_mul_ps(a_vec, b_vec);
                // 将乘法结果累加到 sum_vec 中
                sum_vec = _mm256_add_ps(sum_vec, mul_vec);
            }
            // 将累加结果存储到 result 矩阵中
            // float sum[4];
            // _mm_storeu_ps(sum, sum_vec);
            result->data[i * result->cols + j] += sum_vec[0] + sum_vec[1] + sum_vec[2] + sum_vec[3] + sum_vec[4] + sum_vec[5] + sum_vec[6] + sum_vec[7];
        }
    }

    // size_t i, j, k;

    // for (i = 0; i < A->rows; ++i)
    // {
    //     for (j = 0; j < B->cols; ++j)
    //     {
    //         __m128 sum_vec = _mm_setzero_ps(); // 使用 SSE 寄存器进行累加
    //         for (k = 0; k < A->cols / 4; ++k)
    //         {
    //             __m128 a_vec = _mm_loadu_ps(&A->data[i * A->cols + k]);
    //             // 加载 B 矩阵的 4 个元素到 SSE 寄存器
    //             __m128 b_vec = _mm_loadu_ps(&B->data[k * B->cols + j]);
    //             // 使用 SIMD 指令进行乘法运算
    //             __m128 mul_vec = _mm_mul_ps(a_vec, b_vec);
    //             // 将乘法结果累加到 sum_vec 中
    //             sum_vec = _mm_add_ps(sum_vec, mul_vec);
    //         }
    //         // 将累加结果存储到 result 矩阵中
    //         // float sum[4];
    //         // _mm_storeu_ps(sum, sum_vec);
    //         result->data[i * result->cols + j] = sum_vec[0] + sum_vec[1] + sum_vec[2] + sum_vec[3];
    //     }
    // }
}

void matmul_improved_OMP(const struct Matrix *A, const struct Matrix *B, const struct Matrix *result)
{
    // 检查输入矩阵和结果矩阵是否为空
    if (A == NULL || B == NULL || result == NULL)
    {
        printf("输入矩阵不能为空\n");
        return;
    }
    // 检查输入矩阵的尺寸是否合法
    if (A->cols != B->rows)
    {
        printf("矩阵尺寸不兼容\n");
        return;
    }
    // 检查结果矩阵的尺寸是否正确
    if (A->rows != result->rows || B->cols != result->cols)
    {
        printf("结果矩阵尺寸不正确\n");
        return;
    }

    // #pragma omp parallel for private(i, j, k)
    // #pragma omp for schedule(static) private(j, k)
#pragma omp parallel for num_threads(4)
    //  外层并行化
    for (size_t i = 0; i < A->rows; ++i)
    {
        for (size_t j = 0; j < B->cols; ++j)
        {
            __m256 sum_vec = _mm256_setzero_ps(); // 使用 AVX 寄存器进行累加
            for (size_t k = 0; k < A->cols / 8; ++k)
            { // 一次处理 8 个元素
                // 加载 A 矩阵的 8 个元素到 AVX 寄存器
                __m256 a_vec = _mm256_loadu_ps(&A->data[i * A->cols + k]);
                // 加载 B 矩阵的 8 个元素到 AVX 寄存器
                __m256 b_vec = _mm256_loadu_ps(&B->data[k * B->cols + j]);
                // 使用 SIMD 指令进行乘法运算
                __m256 mul_vec = _mm256_mul_ps(a_vec, b_vec);
                // 将乘法结果累加到 sum_vec 中
                sum_vec = _mm256_add_ps(sum_vec, mul_vec);
            }
            // 将累加结果存储到 result 矩阵中
            float sum[8];
            _mm256_storeu_ps(sum, sum_vec);

            result->data[i * result->cols + j] += sum[0] + sum[1] + sum[2] + sum[3] + sum[4] + sum[5] + sum[6] + sum[7];
        }
    }
}
int main()
{
    srand((unsigned)time(NULL)); // Seed random number generator with current time

    size_t testcases[] = {16, 128, 1000, 2000, 8000, 12800, 19200, 25600};

    // const size_t size = 2000; // Change the size according to your needs
    for (int testcase = 0; testcase < 8; testcase++)
    {
        struct Matrix *A = allocate_Matrix(testcases[testcase], testcases[testcase]);
        struct Matrix *B = allocate_Matrix(testcases[testcase], testcases[testcase]);
        struct Matrix *result = allocate_Matrix(testcases[testcase], testcases[testcase]);
        struct Matrix *result_improved = allocate_Matrix(testcases[testcase], testcases[testcase]);
        struct Matrix *result_improved_OMP = allocate_Matrix(testcases[testcase], testcases[testcase]);
        struct Matrix *result_block = allocate_Matrix(testcases[testcase], testcases[testcase]);
        generateRandomMatrix(A);
        generateRandomMatrix(B);

        // Measure execution time
        clock_t start = clock();
        matmul_plain(A, B, result);
        clock_t end = clock();
        double elapsed_secs = (double)(end - start) / CLOCKS_PER_SEC;

        start = clock();
        matmul_improved(A, B, result_improved);
        end = clock();
        double elapsed_secs_improved = (double)(end - start) / CLOCKS_PER_SEC;

        start = clock();
        matmul_improved_OMP(A, B, result_improved_OMP);
        end = clock();
        double elapsed_secs_improved_SIMD_OMP = (double)(end - start) / CLOCKS_PER_SEC;

        start = clock();
        cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                    testcases[testcase], testcases[testcase], testcases[testcase], 1.0, A->data, testcases[testcase], B->data, testcases[testcase], 0.0, result->data, testcases[testcase]);
        end = clock();
        double elapsed_secs_openblas = (double)(end - start) / CLOCKS_PER_SEC;

        start = clock();
        // #pragma omp parallel for num_threads(4)
        matmul_block(A, B, result_block);
        end = clock();
        double elapsed_secs_block = (double)(end - start) / CLOCKS_PER_SEC;

        printf("Matrix multiplication completed in %f seconds.\n", elapsed_secs);
        printf("Matrix multiplication improved by SIMD completed in %f seconds.\n", elapsed_secs_improved);
        printf("Matrix multiplication improved by OMP + SIMD completed in %f seconds.\n", elapsed_secs_improved_SIMD_OMP);
        printf("Matrix multiplication by openblas completed in %f seconds.\n", elapsed_secs_openblas);
        printf("Matrix multiplication by block completed in %f seconds.\n", elapsed_secs_block);
        FILE *outputFile = fopen("Time Test.txt", "a");

        fprintf(outputFile, "Time used by SIMD(size = %ld): ", testcases[testcase]);
        fprintf(outputFile, "%fs\n", elapsed_secs_improved);

        fprintf(outputFile, "Time used by SIMD + OMP(size = %ld): ", testcases[testcase]);
        fprintf(outputFile, "%fs\n", elapsed_secs_improved_SIMD_OMP);

        fprintf(outputFile, "Time used by openblas(size = %ld): ", testcases[testcase]);
        fprintf(outputFile, "%fs\n", elapsed_secs_openblas);

        fprintf(outputFile, "Time used by block(size = %ld): ", testcases[testcase]);
        fprintf(outputFile, "%fs\n", elapsed_secs_block);

        // printf("Plain: \n");
        // for (int i = 0; i < result->rows; i++)
        // {
        //     for (int j = 0; j < result->cols; j++)
        //     {
        //         printf("%f ", result->data[i * result->cols + j]);
        //     }
        //     printf("\n");
        // }

        // printf("SIMD: \n");

        // for (int i = 0; i < result_improved->rows; i++)
        // {
        //     for (int j = 0; j < result_improved->cols; j++)
        //     {
        //         printf("%f ", result_improved->data[i * result_improved->cols + j]);
        //     }
        //     printf("\n");
        // }

        // printf("OMP: \n");

        // for (int i = 0; i < result_improved_OMP->rows; i++)
        // {
        //     for (int j = 0; j < result_improved_OMP->cols; j++)
        //     {
        //         printf("%f ", result_improved_OMP->data[i * result_improved_OMP->cols + j]);
        //     }
        //     printf("\n");
        // }

        // for (int i = 0; i < result_block->rows; i++)
        // {
        //     for (int j = 0; j < result_block->cols; j++)
        //     {
        //         printf("%f ", result_block->data[i * result_block->cols + j]);
        //     }
        //     printf("\n");
        // }

        fclose(outputFile);
        printf("Output written to Time Test.txt.\n");
        // Deallocate memory
        deallocateMatrix(result_improved);
        deallocateMatrix(result_improved_OMP);
        deallocateMatrix(result);
        deallocateMatrix(result_block);
        deallocateMatrix(A);
        deallocateMatrix(B);
    }

    return 0;
}
