import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.Scanner;

public class Matrix_test {

    public static int[] testcases = {10, 100, 200, 500, 1000, 2000, 3000, 5000};

    public static void main(String[] args) throws IOException {
        Scanner scanner = new Scanner(System.in);


        for (int i = 0; i < testcases.length; i++) {


            float[][] matrix1 = new float[testcases[i]][testcases[i]];

            enterMatrixElements(matrix1);


            float[][] matrix2 = new float[testcases[i]][testcases[i]];
            enterMatrixElements(matrix2);

            float[][] result = new float[testcases[i]][testcases[i]];

            long starttime = System.nanoTime();
            multiplyMatrices(matrix1, matrix2, result, testcases[i]);
            long endtime = System.nanoTime();


            long elapsedTime = endtime - starttime;
            double elapsedTimeInSeconds = (double) elapsedTime / 1_000_000_000.0;
            System.out.println("Time taken for matrix multiplication: " + elapsedTimeInSeconds + " seconds.");


//            System.out.println("The result of matrix multiplication is:");

//            long starttime2 = System.nanoTime();
//            printMatrix(result);
//            long endtime2 = System.nanoTime();
//            long elapsedTime2 = endtime2 - starttime2;
//            double elapsedTime2InSeconds = (double) elapsedTime2 / 1_000_000_000.0;
//            System.out.println("Time taken for matrix printing: " + elapsedTime2InSeconds + " seconds.");

            writeTimeToTxt(elapsedTimeInSeconds, testcases[i]);
        }

    }

    public static void enterMatrixElements(float[][] matrix) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[0].length; j++) {
                Random random = new Random();
                float randomNumber = random.nextFloat();
                randomNumber = randomNumber * 10;
                matrix[i][j] = randomNumber;
            }
        }
    }

    public static void multiplyMatrices(float[][] matrix1, float[][] matrix2, float[][] result, int n) {
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                for (int j = 0; j < n; j++) {
                    result[i][j] += matrix1[i][k] * matrix2[k][j];
                }
            }
        }
    }

    public static void printMatrix(float[][] matrix) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[0].length; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
    }

    //文件写入
    public static void writeTimeToTxt(double timeInSeconds, int n) throws IOException {
        if (n == 10) {
            FileWriter writer = new FileWriter("matrix_multiplication_time.txt", false);
            //BufferedWriter bw = new BufferedWriter(writer);
            writer.write("Time taken for matrix multiplication: " + timeInSeconds + " seconds.(sizeof " + n + ")\n");
            writer.close();
            System.out.println("Matrix multiplication time written to matrix_multiplication_time.txt successfully.");
        } else {
            FileWriter writer = new FileWriter("matrix_multiplication_time.txt", true);
            //BufferedWriter bw = new BufferedWriter(writer);
            writer.write("Time taken for matrix multiplication: " + timeInSeconds + " seconds.(sizeof " + n + ")\n");
            writer.close();
            System.out.println("Matrix multiplication time written to matrix_multiplication_time.txt successfully.");
        }
    }
}
