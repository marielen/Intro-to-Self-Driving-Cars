import math
from math import sqrt
import numbers

def zeroes(height, width):
    """
    Creates a matrix of zeroes.
    """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)

def identity(n):
    """
    Creates a n x n identity matrix.
    """
    I = zeroes(n, n)
    for i in range(n):
        I.g[i][i] = 1.0
    return I

def dot_product(A, B):
    """
    Calculates dot product between two matrices.
    """
    if not len(A) == len(B):
        raise(ValueError, "Number of columns are not equal.")

    sumVector = 0

    for i in range(len(A)):
        sumVector+= A[i]*B[i]

    return sumVector
    
def get_column(matrix, column_number):
    """
    Get the column from a matrix into a list.
    """
    nRows = len(matrix)
    column = []
    
    for i in range(nRows):
        column.append(matrix[i][column_number])
    
    return column

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            determinant = self.g[0][0]
        
        elif self.h == 2:
            diagonal1 = self.g[0][0] * self.g[1][1]
            diagonal2 = self.g[0][1] * self.g[1][0]
            determinant = diagonal1 - diagonal2
        
        return determinant                    
                    

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
            
        sumDiagonal = 0
        for i in range(self.h):
            for j in range(self.w):
                if i==j:
                    sumDiagonal+= self.g[i][j]
        return sumDiagonal

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
    
        inverse = []

        if self.h == 1:
            inverse.append(1/self.g[0][0])
            inverse = [inverse]

        elif self.h == 2:
            a = self.g[0][0]
            b = self.g[0][1]
            c = self.g[1][0]
            d = self.g[1][1]

            if a*d == b*c:
                raise ValueError('The matrix does not have an inverse.')

            else:
                constant = 1/(a*d-b*c)
                inverse.append([constant*d])
                inverse[0].append(constant*(-b))
                inverse.append([constant*(-c)])
                inverse[1].append(constant*a)

        return Matrix(inverse)
        

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = []

        for j in range(self.w):
            row = []
            for i in range(self.h):
                row.append(self.g[i][j])
            matrix_transpose.append(row)

        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w
    
    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")
            
        result =[]

        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self.g[i][j]+other.g[i][j])
            result.append(row)

        return Matrix(result)
                

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        result = []
        
        for i in range(self.h):
            
            row=[]
            
            for j in range(self.w):
                row.append(self.g[i][j]*(-1))
            result.append(row)

        return(Matrix(result))

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        matrixSub = []

        for i in range(self.h):
            row=[]
            for j in range(self.w):
                row.append(self.g[i][j] - other.g[i][j])
            matrixSub.append(row)

        return Matrix(matrixSub)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        product = []

        for i in range(self.h):
            row_result = []
            for j in range(other.w):
                A = self.g[i]
                B = get_column(other.g, j)
                row_result.append(dot_product(A,B))
            product.append(row_result)

        return Matrix(product)

        

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            r = []

            for i in range(self.h):
                r.append([self.g[i][j]*other for j in range(self.w)])
            
            return Matrix(r)
            
            