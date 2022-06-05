import random
import time

from java.util.concurrent import Executors, TimeUnit
from java.lang import Runnable, InterruptedException, Long


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


def roundMatrix(matrix, columns, rows, ndigits):
    for i in range(columns):
        for j in range(rows):
            matrix[i][j] = round(matrix[i][j], ndigits)


def saveMatrix(matrix, path, name):
    file = open(path+name+'.txt', 'w')
    file.writelines('\t'.join(str(j) for j in i) + '\n' for i in matrix)


def saveTime(time, path, name):
    file = open(path+name+'.txt', 'w')
    file.write('Time: '+str(time))
    file.close()


def CheckMatricesEqualities(matrix_A, matrix_B):
    for i in range(len(matrix_A)):
        for j in range(len(matrix_A[i])):
            if(matrix_A[i][j] != matrix_B[i][j]):
                print(i, j)
                print(matrix_A[i][j],  matrix_B[i][j])
                return False
    return True


# Parallel part


class StripedAlgo:
    def __init__(self, A_matrix, B_matrix, A_Columns, A_Rows, B_Columns, B_Rows, n_threads):
        self.n_threads = n_threads
        self.workers = []
        self.result = createMatrixWithZeros(A_Columns, B_Rows)
        self.prepareWorkers(A_matrix, B_matrix, self.result,
                            A_Columns, A_Rows, B_Columns, B_Rows)

    def get_result(self):
        return self.result

    def prepareWorkers(self, A_matrix, B_matrix, C_matrix, A_Columns, A_Rows, B_Columns, B_Rows):
        max_i = 0
        max_j = 0
        i = 0
        j = 0
        while (max_i != A_Columns or max_j != B_Rows):
            self.workers.append(StripeWorker(
                i, j, A_matrix, B_matrix, C_matrix, A_Columns, A_Rows, B_Columns, B_Rows))
                
            if max_i != A_Columns:
                max_i = max_i + 1
            if max_j != B_Rows:
                max_j = max_j + 1
            i = (i + 1) % A_Columns
            j = (j + 1) % B_Rows

    def nextIter(self):
        executor = Executors.newFixedThreadPool(self.n_threads)
        for worker in self.workers:
            executor.execute(worker)
        executor.shutdown()
        try:
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS)
        except InterruptedException as e:
            print(e)


class StripeWorker(Runnable):
    def __init__(self,   row, column, A_matrix, B_matrix, C_matrix, A_Columns, A_Rows, B_Columns, B_Rows):
        self.row = row
        self.column = column
        self.A_matrix = A_matrix
        self.B_matrix = B_matrix
        self.C_matrix = C_matrix
        self.A_Columns = A_Columns
        self.A_Rows = A_Rows
        self.B_Columns = B_Columns
        self.B_Rows = B_Rows

    def multiplyRowAndColumn(self, row, column, A_Rows):
        result = 0
        for i in range(A_Rows):
            result += self.A_matrix[row][i] * self.B_matrix[i][column]
        return result

    def run(self):
        self.C_matrix[self.row][self.column] = self.multiplyRowAndColumn(
            row=self.row, column=self.column, A_Rows=self.A_Rows)
        self.column = (self.column + 1) % self.B_Rows


def runIterations(B_Rows, stripeAlgo):
    for i in range(B_Rows):
        stripeAlgo.nextIter()
    return stripeAlgo.get_result()


def readMatrixFromFile(path, name):
    file = open(path+name+'.txt', 'r')
    return [[float(x) for x in line.split()] for line in file]


def createMatrixWithZeros(columns, rows):
    matrix = [[0 for i in range(rows)] for j in range(columns)]
    return matrix

# A_Columns, A_Rows, B_Columns, B_Rows = (500, 500, 500, 500)
# A_Columns, A_Rows, B_Columns, B_Rows = (400, 300, 300, 150)
A_Columns, A_Rows, B_Columns, B_Rows = (750, 600, 600, 850)
n_threads = 2
matrix_A = readMatrixFromFile(
    './Matrices/', 'matrix_a_'+str(A_Columns)+'x'+str(A_Rows))
matrix_B = readMatrixFromFile(
    './Matrices/', 'matrix_b_'+str(B_Columns)+'x'+str(B_Rows))
matrix_C = readMatrixFromFile(
    './Matrices/', 'matrix_c_'+str(A_Columns)+'x'+str(B_Rows))
print('Timer started')
multiply_time = time.time()
algo = StripedAlgo(matrix_A, matrix_B, A_Columns,
                   A_Rows, B_Columns, B_Rows, n_threads)
matrix_D = runIterations(B_Rows, algo)
multiply_time = round(time.time() - multiply_time, 4)
print('Time: ', multiply_time)
roundMatrix(matrix_D, A_Columns, B_Rows, 2)
roundMatrix(matrix_C, A_Columns, B_Rows, 2)
if not CheckMatricesEqualities(matrix_C, matrix_D):
    print('Matrices not equal!')
    quit()
saveMatrix(matrix_D, './Matrices/', 'matrix_d_'+str(A_Columns)+'x'+str(B_Rows))
