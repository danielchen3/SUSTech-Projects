#include <iostream>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <stdexcept>
#include <memory>

template <typename T>
class Matrix
{
public:
    // Constructor with ROI parameters
    Matrix(size_t rows, size_t cols, size_t startRow, size_t startCol, size_t roiRows, size_t roiCols)
        : rows(rows), cols(cols), startRow(startRow), startCol(startCol), roiRows(roiRows), roiCols(roiCols)
    {
        data = std::shared_ptr<T[]>(new T[rows * cols]);
    }

    // Constructor with shared pointer to data
    Matrix(size_t rows, size_t cols, std::shared_ptr<T[]> data, size_t startRow, size_t startCol, size_t roiRows, size_t roiCols)
        : rows(rows), cols(cols), startRow(startRow), startCol(startCol), roiRows(roiRows), roiCols(roiCols), data(data)
    {
    }

    // Destructor to free memory
    ~Matrix() = default;

    // Copy constructor
    Matrix(const Matrix &other) : rows(other.rows), cols(other.cols), startRow(other.startRow), startCol(other.startCol),
                                  roiRows(other.roiRows), roiCols(other.roiCols), data(other.data)
    {
    }

    // Assignment operator
    Matrix &operator=(const Matrix &other)
    {
        if (this != &other)
        {
            rows = other.rows;
            cols = other.cols;
            data = other.data; // 自动增加计数
        }
        return *this;
    }

    // Equality operator
    bool operator==(const Matrix &other) const
    {
        if (rows != other.rows || cols != other.cols)
            return false;
        for (size_t i = 0; i < rows * cols; ++i)
        {
            if (data[i] != other.data[i])
                return false;
        }
        return true;
    }

    // Addition operator
    Matrix operator+(const Matrix &other) const
    {
        if (rows != other.rows || cols != other.cols)
            throw std::invalid_argument("Matrices in different dimension for addition");
        Matrix result(rows, cols, startRow, startCol, roiRows, roiCols);
        for (size_t i = 0; i < rows * cols; ++i)
        {
            result.data[i] = data[i] + other.data[i];
        }
        return result;
    }

    // Subtraction operator
    Matrix operator-(const Matrix &other) const
    {
        if (rows != other.rows || cols != other.cols)
            throw std::invalid_argument("Matrices in different dimension for subtraction");
        Matrix result(rows, cols, startRow, startCol, roiRows, roiCols);
        for (size_t i = 0; i < rows * cols; ++i)
        {
            result.data[i] = data[i] - other.data[i];
        }
        return result;
    }

    // Multiplication operator
    Matrix operator*(const Matrix &other) const
    {
        if (cols != other.rows)
            throw std::invalid_argument("Invalid Multiplication!");
        Matrix result(rows, other.cols, startRow, startCol, roiRows, roiCols);
        for (size_t i = 0; i < rows; ++i)
        {
            for (size_t j = 0; j < other.cols; ++j)
            {
                T sum = 0;
                for (size_t k = 0; k < cols; ++k)
                {
                    sum += (*this)(i, k) * other(k, j);
                }
                result(i, j) = sum;
            }
        }
        return result;
    }

    // Element access
    T &operator()(size_t i, size_t j)
    {
        if (i >= startRow && i < startRow + roiRows && j >= startCol && j < startCol + roiCols)
        {
            return data[(i - startRow) * cols + (j - startCol)];
        }
        else
        {
            throw std::out_of_range("Index out of range");
        }
    }

    // Const element access
    const T &operator()(size_t i, size_t j) const
    {
        if (i >= startRow && i < startRow + roiRows && j >= startCol && j < startCol + roiCols)
        {
            return data[(i - startRow) * cols + (j - startCol)];
        }
        else
        {
            throw std::out_of_range("Index out of range");
        }
    }

public:
    size_t rows;
    size_t cols;
    std::shared_ptr<T[]> data;

    size_t startRow;
    size_t startCol;
    size_t roiRows;
    size_t roiCols;
};

// generate a random matrix
template <typename T>
Matrix<T> generateRandomMatrix(size_t rows, size_t cols)
{
    Matrix<T> mat(rows, cols, 0, 0, rows, cols);
    if constexpr (std::is_floating_point<T>::value)
    {
        // For floating-point types, generate random numbers between 0 and 1
        for (size_t i = 0; i < rows; ++i)
        {
            for (size_t j = 0; j < cols; ++j)
            {
                mat(i, j) = static_cast<T>(rand()) / static_cast<T>(RAND_MAX); // Random float between 0 and 1
            }
        }
    }
    else
    {
        // For integer types
        for (size_t i = 0; i < rows; ++i)
        {
            for (size_t j = 0; j < cols; ++j)
            {
                mat(i, j) = static_cast<T>(rand() % 100); // Random integer between 0 and RAND_MAX
            }
        }
    }
    return mat;
}

// Function to print a matrix
template <typename T>
void printMatrix(const Matrix<T> &mat)
{
    for (size_t i = mat.startRow; i < mat.roiRows; ++i)
    {
        for (size_t j = mat.startCol; j < mat.roiCols; ++j)
        {
            std::cout << std::setw(4) << mat(i, j) << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

int main()
{

    srand(static_cast<unsigned int>(time(nullptr)));

    // Test with integer data type
    printf("Please input size: ");
    int n;
    std::cin >> n;
    std::shared_ptr<int[]> data(new int[n * n]);
    Matrix<int> A_int(n, n, data, 0, 0, n, n);
    auto B_int = A_int;
    auto C_int = A_int;

    // Generate random integer matrices
    A_int = generateRandomMatrix<int>(n, n);
    B_int = generateRandomMatrix<int>(n, n);
    C_int = generateRandomMatrix<int>(n, n);

    printf("Test for different types:\n");
    std::shared_ptr<short[]> A_short_data(new short[n * n]);
    Matrix<short> A_short(n, n, A_short_data, 0, 0, n, n);
    A_short = generateRandomMatrix<short>(n, n);
    auto B_short = A_short;
    std::cout << "Matrix B_short:" << std::endl;
    printMatrix(B_short);
    std::cout << "sum_short:" << std::endl;
    printMatrix(A_short + B_short);

    std::shared_ptr<float[]> A_float_data(new float[10 * 10]);
    Matrix<float> A_float(n, n, A_float_data, 0, 0, n, n);
    A_float = generateRandomMatrix<float>(n, n);
    auto B_float = A_float;
    std::cout << "Matrix B_float:" << std::endl;
    printMatrix(B_float);
    std::cout << "sum_float:" << std::endl;
    printMatrix(A_float + B_float);

    std::shared_ptr<double[]> A_double_data(new double[n * n]);
    Matrix<double> A_double(n, n, A_double_data, 0, 0, n, n);
    A_double = generateRandomMatrix<double>(n, n);
    auto B_double = A_double;
    std::cout << "Matrix B_double:" << std::endl;
    printMatrix(B_double);
    std::cout << "sum_double:" << std::endl;
    printMatrix(A_double + B_double);

    // Print matrices
    std::cout << "Matrix A (int):" << std::endl;
    printMatrix(A_int);
    std::cout << "Matrix B (int):" << std::endl;
    printMatrix(B_int);
    std::cout << "Matrix C (int):" << std::endl;
    printMatrix(C_int);

    // Test assignment operator
    std::cout << "Testing assignment operator (=)..." << std::endl;
    A_int = B_int;
    std::cout << "Matrix A after assignment:" << std::endl;
    printMatrix(A_int);

    // Test equality operator
    std::cout << "Testing equality operator (==)..." << std::endl;
    std::cout << "A_int == B_int: " << std::boolalpha << (A_int == B_int) << std::endl;

    // Test addition operator
    std::cout << "Testing addition operator (+)..." << std::endl;
    auto result_add_int = A_int + B_int;
    std::cout << "Result of addition:" << std::endl;
    printMatrix(result_add_int);

    // Test subtraction operator
    std::cout << "Testing subtraction operator (-)..." << std::endl;
    auto result_sub_int = A_int - C_int;
    std::cout << "Result of subtraction:" << std::endl;
    printMatrix(result_sub_int);

    // Test multiplication operator
    std::cout << "Testing multiplication operator (*)..." << std::endl;
    auto result_mul_int = A_int * C_int;
    std::cout << "Result of multiplication:" << std::endl;
    printMatrix(result_mul_int);

    std::cout << "Testing assignment with different ROI..." << std::endl;
    Matrix<int> D_int(3, 3, data, 0, 0, 2, 2); // Create a matrix with different ROI
    D_int = C_int;                             // Assign A_int to D_int
    std::cout << "Matrix D after assignment with different ROI:" << std::endl;
    printMatrix(D_int);

    return 0;
}
