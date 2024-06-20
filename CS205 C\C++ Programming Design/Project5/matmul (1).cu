#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <sys/time.h>
#include <cblas.h>

//nvcc -o matmul matmul.cu -lcublas -lcuda -lopenblas

#define TIME_START gettimeofday(&t_start, NULL);
#define TIME_END(name)    gettimeofday(&t_end, NULL); \
                    elapsedTime = (t_end.tv_sec - t_start.tv_sec) * 1000.0;   \
                    elapsedTime += (t_end.tv_usec - t_start.tv_usec) / 1000.0;  \
                    printf(#name " Time = %f ms.\n", elapsedTime);

typedef struct 
{
    size_t rows;
    size_t cols;
    float * data; // CPU memory
    float * data_device; // GPU memory
} Matrix;

Matrix * createMatrix(size_t r, size_t c)
{
    size_t len = r * c;
    if(len == 0)
    {
        fprintf(stderr, "Invalid size. The input should be > 0.\n");
        return NULL;
    }
    Matrix * p  = (Matrix *) malloc(sizeof(Matrix));
    if (p == NULL)
    {
        fprintf(stderr, "Allocate host memory failed.\n");
        goto ERR_TAG;
    }
    p->rows = r;
    p->cols = c;
    p->data = (float*)malloc(sizeof(float) * len);
    if(p->data == NULL)
    {
        fprintf(stderr, "Allocate host memory failed.\n");
        goto ERR_TAG;
    }
    if (cudaMalloc(&p->data_device, sizeof(float) * len) != cudaSuccess)
    {
        fprintf(stderr, "Allocate device memory failed.\n");
        goto ERR_TAG;
    }
    return p;
ERR_TAG:
    if(p && p->data) free(p->data);
    if(p) free(p);
    return NULL;
}

void freeMatrix(Matrix ** pp)
{
    if(pp == NULL) return;
    Matrix * p = *pp;
    if(p != NULL)
    {
        if(p->data) free(p->data);
        if(p->data_device) cudaFree(p->data_device);
    }
    *pp = NULL;
}

// A simple function to set all elements to the same value
bool setMatrix(Matrix * pMat, float val)
{
    if(pMat == NULL)
    {
        fprintf(stderr, "NULL pointer.\n");
        return false;
    }
    size_t len = pMat->rows * pMat->cols;
    for(size_t i = 0; i < len; i++)
        pMat->data[i] = val;

    return true;
}

void matmulCPU(const Matrix * A, const Matrix * B, Matrix * C)
{
    const float alpha = 1.0f;
    const float beta = 0.0f;
    
    cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                A->rows, B->cols, A->cols,
                alpha, A->data, A->cols,
                B->data, B->cols,
                beta, C->data, C->cols);
}

// void copyToGPU(Matrix * A, Matrix * B)
// {
//     cudaMemcpy(A->data_device, A->data, A->rows * A->cols * sizeof(float), cudaMemcpyHostToDevice);
//     cudaMemcpy(B->data_device, B->data, B->rows * B->cols * sizeof(float), cudaMemcpyHostToDevice);
// }

// void copyFromGPU(Matrix * C)
// {
//     cudaMemcpy(C->data, C->data_device, C->rows * C->cols * sizeof(float), cudaMemcpyDeviceToHost);
// }

// void matmulGPU(const Matrix * A, const Matrix * B, Matrix * C, cublasHandle_t handle)
// {
//     const float alpha = 1.0f;
//     const float beta = 0.0f;

//     // Perform matrix multiplication: C = alpha * A * B + beta * C
//     cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
//                 A->rows, B->cols, A->cols,
//                 &alpha,
//                 A->data_device, A->rows,
//                 B->data_device, B->rows,
//                 &beta,
//                 C->data_device, C->rows);
// }

void matmulGPU(const Matrix * A, const Matrix * B, Matrix * C)
{
    struct timeval t_start, t_end;
    double elapsedTime = 0;

    TIME_START
    cublasHandle_t handle;
    cublasCreate(&handle);
    TIME_END(createhandle)

    const float alpha = 1.0f;
    const float beta = 0.0f;

    // Copy data to GPU
    TIME_START
    cudaMemcpyAsync(A->data_device, A->data, A->rows * A->cols * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpyAsync(B->data_device, B->data, B->rows * B->cols * sizeof(float), cudaMemcpyHostToDevice);
    TIME_END(CopytoGPU)
    // Start measuring time after data is copied

    // Perform matrix multiplication: C = alpha * A * B + beta * C
    TIME_START
    cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
                A->rows, B->cols, A->cols,
                &alpha,
                A->data_device, A->rows,
                B->data_device, B->rows,
                &beta,
                C->data_device, C->rows);
    TIME_END(RealMultiplication)

    TIME_START
    cudaDeviceSynchronize(); // Ensure the kernel has completed
    TIME_END(Synchronize)
    //TIME_END(matmulGPU)

    // Copy result back to CPU
    TIME_START
    cudaMemcpyAsync(C->data, C->data_device, C->rows * C->cols * sizeof(float), cudaMemcpyDeviceToHost);
    TIME_END(CopyfromGPU)

    TIME_START
    cublasDestroy(handle);
    TIME_END(Destroyhandle)
}

int main()
{
    struct timeval t_start, t_end;
    double elapsedTime = 0;

    int dev_count = 0;
    int dev_id = 0;
    cudaGetDeviceCount(&dev_count);
    cudaSetDevice(0);
    cudaGetDevice(&dev_id);
    printf("You have %d cuda devices.\n", dev_count);
    printf("You are using device %d.\n", dev_id);

    size_t size = 4096;
    Matrix * A = createMatrix(size, size);
    Matrix * B = createMatrix(size, size);
    Matrix * C = createMatrix(size, size);

    setMatrix(A, 1.0f);
    setMatrix(B, 2.0f);

    // Measure CPU matrix multiplication time
    TIME_START
    matmulCPU(A, B, C);
    TIME_END(matmulCPU)
    printf("  Result (CPU) = [%.1f, ..., %.1f]\n", C->data[0], C->data[C->rows * C->cols - 1]);

    // Copy data to GPU
    TIME_START
    //copyToGPU(A, B);
    //TIME_END(copyToGPU)

    //TIME_START
    //cublasHandle_t handle;
    //cublasCreate(&handle);
    //TIME_END(createhandle)

    // Measure GPU matrix multiplication time
   // TIME_START
    matmulGPU(A, B, C);
    //cudaDeviceSynchronize(); // Ensure the kernel has completed
    //TIME_END(matmulGPU)

    // Copy result back to CPU
    //TIME_START
    //copyFromGPU(C);
    TIME_END(matmulGPU)
    printf("  Result (GPU) = [%.1f, ..., %.1f]\n", C->data[0], C->data[C->rows * C->cols - 1]);

    //TIME_START
    //cublasDestroy(handle);
    //TIME_END(destroy)

    freeMatrix(&A);
    freeMatrix(&B);
    freeMatrix(&C);
    return 0;
}
