import numpy as np
import random
import time


def generateMatrix(matrix, n_size, m_size):
    for i in range(n_size):
        for j in range(m_size):
            matrix[i, j] = round(random.uniform(1.0, 10.00), 2)


def userInput(input):
    try:
        val = int(input)
        if(val > 0):
            return val
        print('Should be greater than 0!')
        quit()
    except ValueError:
        print('Should be integer!')
        quit()


def checkMatrixSize(A_Rows, B_Columns):
    if(A_Rows != B_Columns):
        print('Rows of matrix A should be equal to columns of Matrix B!')
        quit()


def getInitData():
    A_Columns = userInput(input('Input number of columns of matrix A: '))
    A_Rows = userInput(input('Input number of rows of matrix A: '))
    B_Columns = userInput(input('Input number of columns of matrix B: '))
    B_Rows = userInput(input('Input number of rows of matrix B: '))
    return A_Columns, A_Rows, B_Columns, B_Rows


def multiplyMatrices(matrix_A, matrix_B, matrix_C, A_Columns, A_Rows,  B_Rows):
    for i in range(A_Columns):
        for j in range(B_Rows):
            for k in range(A_Rows):
                matrix_C[i, j] = matrix_C[i, j] + \
                    matrix_A[i, k] * matrix_B[k, j]


def roundMatrix(matrix, columns, rows, ndigits):
    for i in range(columns):
        for j in range(rows):
            matrix[i, j] = round(matrix[i, j], ndigits)


def saveMatrix(matrix, path, name):
    np.savetxt(path+name+'.txt', matrix)


def saveTime(time, path, name):
    file = open(path+name+'.txt', 'w')
    file.write('Time: ' + str(time))
    file.close()


def main_func_simple(A_Columns, A_Rows, B_Columns, B_Rows):
    matrix_A = np.zeros((A_Columns, A_Rows))
    matrix_B = np.zeros((B_Columns, B_Rows))
    matrix_C = np.zeros((A_Columns, B_Rows))
    generateMatrix(matrix_A, A_Columns, A_Rows)
    generateMatrix(matrix_B, B_Columns, B_Rows)
    print('Timer started')
    multiply_time = time.time()
    multiplyMatrices(matrix_A, matrix_B, matrix_C, A_Columns, A_Rows, B_Rows)
    multiply_time = round(time.time() - multiply_time, 4)
    print('Time: ', multiply_time)
    # roundMatrix(matrix_C, A_Columns, B_Rows, 2)
    saveMatrix(matrix_A, './Matrices/', 'matrix_a_' +
               str(A_Columns)+'x'+str(A_Rows))
    saveMatrix(matrix_B, './Matrices/', 'matrix_b_' +
               str(B_Columns)+'x'+str(B_Rows))
    saveMatrix(matrix_C, './Matrices/', 'matrix_c_' +
               str(A_Columns)+'x'+str(B_Rows))

# sizes = np.array([(500,500,500,500),(750, 600, 600, 850), (1000,1000,1000,1000), (1000, 1500, 1500, 1100), (2000, 2000, 2000, 2000)])
# for i in sizes:
#     A_Columns, A_Rows, B_Columns, B_Rows = i
#     main_func_simple(A_Columns, A_Rows, B_Columns, B_Rows)


A_Columns, A_Rows, B_Columns, B_Rows = getInitData()
checkMatrixSize(A_Rows, B_Columns)
main_func_simple(A_Columns, A_Rows, B_Columns, B_Rows)

