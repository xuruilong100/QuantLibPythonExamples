import unittest
from utilities import *
from QuantLib import *
from math import sqrt, isnan


def inner_product(x, y, v):
    ip = v
    for i in range(len(x)):
        ip += x[i] * y[i]
    return ip


def normArray(v):
    return sqrt(DotProduct(v, v))


def normMatrix(m):
    sum = 0.0
    for i in range(m.rows()):
        for j in range(m.columns()):
            sum += m[i][j] * m[i][j]
    return sqrt(sum)


N = 3


class MatricesTest(unittest.TestCase):
    def testEigenvectors(self):
        TEST_MESSAGE("Testing eigenvalues and eigenvectors calculation...")
        M1 = Matrix(N, N)
        M2 = Matrix(N, N)
        I = Matrix(N, N)

        M1[0][0] = 1.0
        M1[0][1] = 0.9
        M1[0][2] = 0.7
        M1[1][0] = 0.9
        M1[1][1] = 1.0
        M1[1][2] = 0.4
        M1[2][0] = 0.7
        M1[2][1] = 0.4
        M1[2][2] = 1.0

        M2[0][0] = 1.0
        M2[0][1] = 0.9
        M2[0][2] = 0.7
        M2[1][0] = 0.9
        M2[1][1] = 1.0
        M2[1][2] = 0.3
        M2[2][0] = 0.7
        M2[2][1] = 0.3
        M2[2][2] = 1.0

        I[0][0] = 1.0
        I[0][1] = 0.0
        I[0][2] = 0.0
        I[1][0] = 0.0
        I[1][1] = 1.0
        I[1][2] = 0.0
        I[2][0] = 0.0
        I[2][1] = 0.0
        I[2][2] = 1.0

        testMatrices = [M1, M2]

        for M in testMatrices:

            dec = SymmetricSchurDecomposition(M)
            eigenValues = dec.eigenvalues()
            eigenVectors = dec.eigenvectors()
            minHolder = QL_MAX_REAL

            for i in range(N):
                v = Array(N)
                for j in range(N):
                    v[j] = eigenVectors[j][i]
                # check definition
                a = M * v
                b = eigenValues[i] * v
                self.assertFalse(normArray(a - b) > 1.0e-15)
                # check decreasing ordering
                self.assertFalse(eigenValues[i] >= minHolder)
                minHolder = eigenValues[i]

            # check normalization
            m = eigenVectors * transpose(eigenVectors)
            n = normMatrix(m - I)
            self.assertFalse(normMatrix(m - I) > 1.0e-15)

    def testSqrt(self):
        TEST_MESSAGE("Testing matricial square root...")
        M1 = Matrix(N, N)

        M1[0][0] = 1.0
        M1[0][1] = 0.9
        M1[0][2] = 0.7
        M1[1][0] = 0.9
        M1[1][1] = 1.0
        M1[1][2] = 0.4
        M1[2][0] = 0.7
        M1[2][1] = 0.4
        M1[2][2] = 1.0

        m = pseudoSqrt(M1, SalvagingAlgorithm.NoAlgorithm)
        temp = m * transpose(m)
        error = normMatrix(temp - M1)
        tolerance = 1.0e-12
        self.assertFalse(error > tolerance)

    def testHighamSqrt(self):
        TEST_MESSAGE("Testing Higham matricial square root...")
        M5 = Matrix(4, 4)
        M6 = Matrix(4, 4)

        # from Higham - nearest correlation matrix
        M5[0][0] = 2
        M5[0][1] = -1
        M5[0][2] = 0.0
        M5[0][3] = 0.0
        M5[1][0] = M5[0][1]
        M5[1][1] = 2
        M5[1][2] = -1
        M5[1][3] = 0.0
        M5[2][0] = M5[0][2]
        M5[2][1] = M5[1][2]
        M5[2][2] = 2
        M5[2][3] = -1
        M5[3][0] = M5[0][3]
        M5[3][1] = M5[1][3]
        M5[3][2] = M5[2][3]
        M5[3][3] = 2

        # from Higham - nearest correlation matrix to M5
        M6[0][0] = 1
        M6[0][1] = -0.8084124981
        M6[0][2] = 0.1915875019
        M6[0][3] = 0.106775049
        M6[1][0] = M6[0][1]
        M6[1][1] = 1
        M6[1][2] = -0.6562326948
        M6[1][3] = M6[0][2]
        M6[2][0] = M6[0][2]
        M6[2][1] = M6[1][2]
        M6[2][2] = 1
        M6[2][3] = M6[0][1]
        M6[3][0] = M6[0][3]
        M6[3][1] = M6[1][3]
        M6[3][2] = M6[2][3]
        M6[3][3] = 1

        tempSqrt = pseudoSqrt(M5, SalvagingAlgorithm.Higham)
        ansSqrt = pseudoSqrt(M6, SalvagingAlgorithm.NoAlgorithm)
        error = normMatrix(ansSqrt - tempSqrt)
        tolerance = 1.0e-4
        self.assertFalse(error > tolerance)

    def testSVD(self):
        TEST_MESSAGE("Testing singular value decomposition...")

        M1 = Matrix(N, N)
        M2 = Matrix(N, N)
        M3 = Matrix(3, 4)
        M4 = Matrix(4, 3)
        I = Matrix(N, N)

        M1[0][0] = 1.0
        M1[0][1] = 0.9
        M1[0][2] = 0.7
        M1[1][0] = 0.9
        M1[1][1] = 1.0
        M1[1][2] = 0.4
        M1[2][0] = 0.7
        M1[2][1] = 0.4
        M1[2][2] = 1.0

        M2[0][0] = 1.0
        M2[0][1] = 0.9
        M2[0][2] = 0.7
        M2[1][0] = 0.9
        M2[1][1] = 1.0
        M2[1][2] = 0.3
        M2[2][0] = 0.7
        M2[2][1] = 0.3
        M2[2][2] = 1.0

        M3[0][0] = 1
        M3[0][1] = 2
        M3[0][2] = 3
        M3[0][3] = 4
        M3[1][0] = 2
        M3[1][1] = 0
        M3[1][2] = 2
        M3[1][3] = 1
        M3[2][0] = 0
        M3[2][1] = 1
        M3[2][2] = 0
        M3[2][3] = 0

        M4[0][0] = 1
        M4[0][1] = 2
        M4[0][2] = 400
        M4[1][0] = 2
        M4[1][1] = 0
        M4[1][2] = 1
        M4[2][0] = 30
        M4[2][1] = 2
        M4[2][2] = 0
        M4[3][0] = 2
        M4[3][1] = 0
        M4[3][2] = 1.05

        I[0][0] = 1.0
        I[0][1] = 0.0
        I[0][2] = 0.0
        I[1][0] = 0.0
        I[1][1] = 1.0
        I[1][2] = 0.0
        I[2][0] = 0.0
        I[2][1] = 0.0
        I[2][2] = 1.0

        tol = 1.0e-12
        testMatrices = [M1, M2, M3, M4]

        for A in testMatrices:
            # m >= n required (rows >= columns)
            svd = SVD(A)
            # U is m x n
            U = svd.U()
            # s is n long
            s = svd.singularValues()
            # S is n x n
            S = svd.S()
            # V is n x n
            V = svd.V()

            for i in range(S.rows()):
                self.assertFalse(S[i][i] != s[i])

            # tests
            U_Utranspose = transpose(U) * U
            self.assertFalse(normMatrix(U_Utranspose - I) > tol)

            V_Vtranspose = transpose(V) * V
            self.assertFalse(normMatrix(V_Vtranspose - I) > tol)

            A_reconstructed = U * S * transpose(V)
            self.assertFalse(normMatrix(A_reconstructed - A) > tol)

    def testQRDecomposition(self):
        TEST_MESSAGE("Testing QR decomposition...")

        M1 = Matrix(N, N)
        M2 = Matrix(N, N)
        I = Matrix(N, N)
        M3 = Matrix(3, 4)
        M4 = Matrix(4, 3)
        M5 = Matrix(4, 4)

        M1[0][0] = 1.0
        M1[0][1] = 0.9
        M1[0][2] = 0.7
        M1[1][0] = 0.9
        M1[1][1] = 1.0
        M1[1][2] = 0.4
        M1[2][0] = 0.7
        M1[2][1] = 0.4
        M1[2][2] = 1.0

        M2[0][0] = 1.0
        M2[0][1] = 0.9
        M2[0][2] = 0.7
        M2[1][0] = 0.9
        M2[1][1] = 1.0
        M2[1][2] = 0.3
        M2[2][0] = 0.7
        M2[2][1] = 0.3
        M2[2][2] = 1.0

        I[0][0] = 1.0
        I[0][1] = 0.0
        I[0][2] = 0.0
        I[1][0] = 0.0
        I[1][1] = 1.0
        I[1][2] = 0.0
        I[2][0] = 0.0
        I[2][1] = 0.0
        I[2][2] = 1.0

        # setup

        M3[0][0] = 1
        M3[0][1] = 2
        M3[0][2] = 3
        M3[0][3] = 4
        M3[1][0] = 2
        M3[1][1] = 0
        M3[1][2] = 2
        M3[1][3] = 1
        M3[2][0] = 0
        M3[2][1] = 1
        M3[2][2] = 0
        M3[2][3] = 0

        M4[0][0] = 1
        M4[0][1] = 2
        M4[0][2] = 400
        M4[1][0] = 2
        M4[1][1] = 0
        M4[1][2] = 1
        M4[2][0] = 30
        M4[2][1] = 2
        M4[2][2] = 0
        M4[3][0] = 2
        M4[3][1] = 0
        M4[3][2] = 1.05

        # from Higham - nearest correlation matrix
        M5[0][0] = 2
        M5[0][1] = -1
        M5[0][2] = 0.0
        M5[0][3] = 0.0
        M5[1][0] = M5[0][1]
        M5[1][1] = 2
        M5[1][2] = -1
        M5[1][3] = 0.0
        M5[2][0] = M5[0][2]
        M5[2][1] = M5[1][2]
        M5[2][2] = 2
        M5[2][3] = -1
        M5[3][0] = M5[0][3]
        M5[3][1] = M5[1][3]
        M5[3][2] = M5[2][3]
        M5[3][3] = 2

        tol = 1.0e-12
        testMatrices = [
            M1, M2, I,
            M3, transpose(M3), M4, transpose(M4), M5]

        for A in testMatrices:
            Q = Matrix()
            R = Matrix()
            pivot = true
            ipvt = qrDecomposition(A, Q, R, pivot)

            P = Matrix(A.columns(), A.columns(), 0.0)

            # reverse column pivoting
            for i in range(P.columns()):
                P[ipvt[i]][i] = 1.0

            self.assertFalse(normMatrix(Q * R - A * P) > tol)

            pivot = false
            qrDecomposition(A, Q, R, pivot)

            self.assertFalse(normMatrix(Q * R - A) > tol)

    def testQRSolve(self):
        TEST_MESSAGE("Testing QR solve...")

        M1 = Matrix(N, N)
        M2 = Matrix(N, N)
        I = Matrix(N, N)
        M3 = Matrix(3, 4)
        M4 = Matrix(4, 3)
        M5 = Matrix(4, 4)
        M6 = Matrix(4, 4)
        M7 = M1

        M1[0][0] = 1.0
        M1[0][1] = 0.9
        M1[0][2] = 0.7
        M1[1][0] = 0.9
        M1[1][1] = 1.0
        M1[1][2] = 0.4
        M1[2][0] = 0.7
        M1[2][1] = 0.4
        M1[2][2] = 1.0

        M2[0][0] = 1.0
        M2[0][1] = 0.9
        M2[0][2] = 0.7
        M2[1][0] = 0.9
        M2[1][1] = 1.0
        M2[1][2] = 0.3
        M2[2][0] = 0.7
        M2[2][1] = 0.3
        M2[2][2] = 1.0

        I[0][0] = 1.0
        I[0][1] = 0.0
        I[0][2] = 0.0
        I[1][0] = 0.0
        I[1][1] = 1.0
        I[1][2] = 0.0
        I[2][0] = 0.0
        I[2][1] = 0.0
        I[2][2] = 1.0

        # setup

        M3[0][0] = 1
        M3[0][1] = 2
        M3[0][2] = 3
        M3[0][3] = 4
        M3[1][0] = 2
        M3[1][1] = 0
        M3[1][2] = 2
        M3[1][3] = 1
        M3[2][0] = 0
        M3[2][1] = 1
        M3[2][2] = 0
        M3[2][3] = 0

        M4[0][0] = 1
        M4[0][1] = 2
        M4[0][2] = 400
        M4[1][0] = 2
        M4[1][1] = 0
        M4[1][2] = 1
        M4[2][0] = 30
        M4[2][1] = 2
        M4[2][2] = 0
        M4[3][0] = 2
        M4[3][1] = 0
        M4[3][2] = 1.05

        # from Higham - nearest correlation matrix
        M5[0][0] = 2
        M5[0][1] = -1
        M5[0][2] = 0.0
        M5[0][3] = 0.0
        M5[1][0] = M5[0][1]
        M5[1][1] = 2
        M5[1][2] = -1
        M5[1][3] = 0.0
        M5[2][0] = M5[0][2]
        M5[2][1] = M5[1][2]
        M5[2][2] = 2
        M5[2][3] = -1
        M5[3][0] = M5[0][3]
        M5[3][1] = M5[1][3]
        M5[3][2] = M5[2][3]
        M5[3][3] = 2

        # from Higham - nearest correlation matrix to M5
        M6[0][0] = 1
        M6[0][1] = -0.8084124981
        M6[0][2] = 0.1915875019
        M6[0][3] = 0.106775049
        M6[1][0] = M6[0][1]
        M6[1][1] = 1
        M6[1][2] = -0.6562326948
        M6[1][3] = M6[0][2]
        M6[2][0] = M6[0][2]
        M6[2][1] = M6[1][2]
        M6[2][2] = 1
        M6[2][3] = M6[0][1]
        M6[3][0] = M6[0][3]
        M6[3][1] = M6[1][3]
        M6[3][2] = M6[2][3]
        M6[3][3] = 1

        M7[0][1] = 0.3
        M7[0][2] = 0.2
        M7[2][1] = 1.2

        tol = 1.0e-12
        rng = MersenneTwisterUniformRng(1234)
        bigM = Matrix(50, 100, 0.0)
        for i in range(min(bigM.rows(), bigM.columns())):
            bigM[i][i] = i + 1.0

        randM = Matrix(50, 200)
        for i in range(randM.rows()):
            for j in range(randM.columns()):
                randM[i][j] = rng.next().value()

        testMatrices = [
            M1, M2, M3, transpose(M3),
            M4, transpose(M4), M5, I, M7,
            bigM, transpose(bigM),
            randM, transpose(randM)]

        for A in testMatrices:
            b = Array(A.rows())

            for k in range(10):
                for i in range(len(b)):
                    b[i] = rng.next().value()

                x = qrSolve(A, b, true, Array())

                if A.columns() >= A.rows():
                    self.assertFalse(normArray(A * x - b) > tol)
                else:
                    # use the SVD to calculate the reference values
                    n = A.columns()
                    xr = Array(n, 0.0)

                    svd = SVD(A)
                    V = svd.V()
                    U = svd.U()
                    w = svd.singularValues()
                    threshold = n * QL_EPSILON

                    for i in range(n):
                        if w[i] > threshold:
                            u = Array(U.rows())
                            for ii in range(U.rows()):
                                u[ii] = U[ii][i]
                            u = inner_product(u, b, 0.0) / w[i]

                            for j in range(n):
                                xr[j] += u * V[j][i]

                    self.assertFalse(normArray(xr - x) > tol)

    def testInverse(self):
        TEST_MESSAGE("Testing LU inverse calculation...")

        M1 = Matrix(N, N)
        M2 = Matrix(N, N)
        I = Matrix(N, N)
        M5 = Matrix(4, 4)

        M1[0][0] = 1.0
        M1[0][1] = 0.9
        M1[0][2] = 0.7
        M1[1][0] = 0.9
        M1[1][1] = 1.0
        M1[1][2] = 0.4
        M1[2][0] = 0.7
        M1[2][1] = 0.4
        M1[2][2] = 1.0

        M2[0][0] = 1.0
        M2[0][1] = 0.9
        M2[0][2] = 0.7
        M2[1][0] = 0.9
        M2[1][1] = 1.0
        M2[1][2] = 0.3
        M2[2][0] = 0.7
        M2[2][1] = 0.3
        M2[2][2] = 1.0

        I[0][0] = 1.0
        I[0][1] = 0.0
        I[0][2] = 0.0
        I[1][0] = 0.0
        I[1][1] = 1.0
        I[1][2] = 0.0
        I[2][0] = 0.0
        I[2][1] = 0.0
        I[2][2] = 1.0

        # from Higham - nearest correlation matrix
        M5[0][0] = 2
        M5[0][1] = -1
        M5[0][2] = 0.0
        M5[0][3] = 0.0
        M5[1][0] = M5[0][1]
        M5[1][1] = 2
        M5[1][2] = -1
        M5[1][3] = 0.0
        M5[2][0] = M5[0][2]
        M5[2][1] = M5[1][2]
        M5[2][2] = 2
        M5[2][3] = -1
        M5[3][0] = M5[0][3]
        M5[3][1] = M5[1][3]
        M5[3][2] = M5[2][3]
        M5[3][3] = 2

        tol = 1.0e-12
        testMatrices = [M1, M2, I, M5]

        for A in testMatrices:
            invA = inverse(A)

            I1 = invA * A
            I2 = A * invA

            identity = Matrix(A.rows(), A.rows(), 0.0)
            for i in range(A.rows()):
                identity[i][i] = 1.0

            self.assertFalse(normMatrix(I1 - identity) > tol)
            self.assertFalse(normMatrix(I2 - identity) > tol)

    def testDeterminant(self):
        TEST_MESSAGE("Testing LU determinant calculation...")

        M1 = Matrix(N, N)
        M2 = Matrix(N, N)
        I = Matrix(N, N)
        M5 = Matrix(4, 4)
        M6 = Matrix(4, 4)

        M1[0][0] = 1.0
        M1[0][1] = 0.9
        M1[0][2] = 0.7
        M1[1][0] = 0.9
        M1[1][1] = 1.0
        M1[1][2] = 0.4
        M1[2][0] = 0.7
        M1[2][1] = 0.4
        M1[2][2] = 1.0

        M2[0][0] = 1.0
        M2[0][1] = 0.9
        M2[0][2] = 0.7
        M2[1][0] = 0.9
        M2[1][1] = 1.0
        M2[1][2] = 0.3
        M2[2][0] = 0.7
        M2[2][1] = 0.3
        M2[2][2] = 1.0

        I[0][0] = 1.0
        I[0][1] = 0.0
        I[0][2] = 0.0
        I[1][0] = 0.0
        I[1][1] = 1.0
        I[1][2] = 0.0
        I[2][0] = 0.0
        I[2][1] = 0.0
        I[2][2] = 1.0

        # from Higham - nearest correlation matrix
        M5[0][0] = 2
        M5[0][1] = -1
        M5[0][2] = 0.0
        M5[0][3] = 0.0
        M5[1][0] = M5[0][1]
        M5[1][1] = 2
        M5[1][2] = -1
        M5[1][3] = 0.0
        M5[2][0] = M5[0][2]
        M5[2][1] = M5[1][2]
        M5[2][2] = 2
        M5[2][3] = -1
        M5[3][0] = M5[0][3]
        M5[3][1] = M5[1][3]
        M5[3][2] = M5[2][3]
        M5[3][3] = 2

        # from Higham - nearest correlation matrix to M5
        M6[0][0] = 1
        M6[0][1] = -0.8084124981
        M6[0][2] = 0.1915875019
        M6[0][3] = 0.106775049
        M6[1][0] = M6[0][1]
        M6[1][1] = 1
        M6[1][2] = -0.6562326948
        M6[1][3] = M6[0][2]
        M6[2][0] = M6[0][2]
        M6[2][1] = M6[1][2]
        M6[2][2] = 1
        M6[2][3] = M6[0][1]
        M6[3][0] = M6[0][3]
        M6[3][1] = M6[1][3]
        M6[3][2] = M6[2][3]
        M6[3][3] = 1

        tol = 1e-10

        testMatrices = [M1, M2, M5, M6, I]
        # expected results calculated with octave
        expected = [0.044, -0.012, 5.0, 5.7621e-11, 1.0]

        for j in range(len(testMatrices)):
            calculated = determinant(testMatrices[j])
            self.assertFalse(abs(expected[j] - calculated) > tol)

        rng = MersenneTwisterUniformRng(1234)
        for j in range(100):
            m = Matrix(3, 3)
            for r in range(m.rows()):
                for c in range(m.columns()):
                    m[r][c] = rng.next().value()

            if (j % 3) == 0:
                # every third matrix is a singular matrix
                row = int(3 * rng.next().value())
                # fill(m.row_begin(row), m.row_end(row), 0.0)
                for i in range(m.columns()):
                    m[row][i] = 0.0

            a = m[0][0]
            b = m[0][1]
            c = m[0][2]
            d = m[1][0]
            e = m[1][1]
            f = m[1][2]
            g = m[2][0]
            h = m[2][1]
            i = m[2][2]

            expected = a * e * i + b * f * g + c * d * h - (g * e * c + h * f * a + i * d * b)
            calculated = determinant(m)

            self.assertFalse(abs(expected - calculated) > tol)

    def testOrthogonalProjection(self):
        TEST_MESSAGE("Testing orthogonal projections...")

        dimension = 1000
        numberVectors = 50
        multiplier = 100
        tolerance = 1e-6
        seed = 1

        errorAcceptable = 1E-11

        test = Matrix(numberVectors, dimension)

        rng = MersenneTwisterUniformRng(seed)

        for i in range(numberVectors):
            for j in range(dimension):
                test[i][j] = rng.next().value()

        projector = OrthogonalProjections(
            test,
            multiplier,
            tolerance)

        numberFailures = 0
        failuresTwo = 0
        validVec = projector.validVectors()

        for i in range(numberVectors):
            # check output vector i is orthogonal to all other vectors

            if validVec[i]:
                for j in range(numberVectors):
                    if validVec[j] and i != j:
                        dotProduct = 0.0
                        for k in range(dimension):
                            dotProduct += test[j][k] * projector.GetVector(i)[k]

                        if abs(dotProduct) > errorAcceptable:
                            numberFailures += 1

                innerProductWithOriginal = 0.0
                normSq = 0.0

                for j in range(dimension):
                    innerProductWithOriginal += projector.GetVector(i)[j] * test[i][j]
                    normSq += test[i][j] * test[i][j]

                if abs(innerProductWithOriginal - normSq) > errorAcceptable:
                    failuresTwo += 1

        self.assertFalse(numberFailures > 0 or failuresTwo > 0)

    def testCholeskyDecomposition(self):
        TEST_MESSAGE("Testing Cholesky Decomposition...")

        # This test case fails prior to release 1.8

        # The eigenvalues of this matrix are
        # 0.0438523 0.0187376 0.000245617 0.000127656 8.35899e-05 6.14215e-05
        # 1.94241e-05 1.14417e-06 9.79481e-18 1.31141e-18 5.81155e-19

        tmp = [
            [6.4e-05, 5.28e-05, 2.28e-05, 0.00032, 0.00036, 6.4e-05, 6.3968010664e-06, 7.2e-05, 7.19460269899e-06, 1.2e-05, 1.19970004999e-06],
            [5.28e-05, 0.000121, 1.045e-05, 0.00044, 0.000165, 2.2e-05, 2.19890036657e-06, 1.65e-05, 1.64876311852e-06, 1.1e-05, 1.09972504583e-06],
            [2.28e-05, 1.045e-05, 9.025e-05, 0, 0.0001425, 9.5e-06, 9.49525158294e-07, 2.85e-05, 2.84786356835e-06, 4.75e-06, 4.74881269789e-07],
            [0.00032, 0.00044, 0, 0.04, 0.009, 0.0008, 7.996001333e-05, 0.0006, 5.99550224916e-05, 0.0001, 9.99750041661e-06],
            [0.00036, 0.000165, 0.0001425, 0.009, 0.0225, 0.0003, 2.99850049987e-05, 0.001125, 0.000112415667172, 0.000225, 2.24943759374e-05],
            [6.4e-05, 2.2e-05, 9.5e-06, 0.0008, 0.0003, 0.0001, 9.99500166625e-06, 7.5e-05, 7.49437781145e-06, 2e-05, 1.99950008332e-06],
            [6.3968010664e-06, 2.19890036657e-06, 9.49525158294e-07, 7.996001333e-05, 2.99850049987e-05, 9.99500166625e-06, 9.99000583083e-07, 7.49625124969e-06, 7.49063187129e-07, 1.99900033325e-06, 1.99850066645e-07],
            [7.2e-05, 1.65e-05, 2.85e-05, 0.0006, 0.001125, 7.5e-05, 7.49625124969e-06, 0.000225, 2.24831334343e-05, 1.5e-05, 1.49962506249e-06],
            [7.19460269899e-06, 1.64876311852e-06, 2.84786356835e-06, 5.99550224916e-05, 0.000112415667172, 7.49437781145e-06, 7.49063187129e-07, 2.24831334343e-05, 2.24662795123e-06, 1.49887556229e-06, 1.49850090584e-07],
            [1.2e-05, 1.1e-05, 4.75e-06, 0.0001, 0.000225, 2e-05, 1.99900033325e-06, 1.5e-05, 1.49887556229e-06, 2.5e-05, 2.49937510415e-06],
            [1.19970004999e-06, 1.09972504583e-06, 4.74881269789e-07, 9.99750041661e-06, 2.24943759374e-05, 1.99950008332e-06, 1.99850066645e-07, 1.49962506249e-06, 1.49850090584e-07, 2.49937510415e-06, 2.49875036451e-07]]

        m = Matrix(11, 11)
        for i in range(11):
            for j in range(11):
                m[i][j] = tmp[i][j]

        c = CholeskyDecomposition(m, true)
        m2 = c * transpose(c)

        tol = 1.0E-12
        for i in range(11):
            for j in range(11):
                self.assertFalse(isnan(m2[i][j]))
                # this does not detect nan values
                self.assertFalse(abs(m[i][j] - m2[i][j]) > tol)

    def testMoorePenroseInverse(self):
        TEST_MESSAGE("Testing Moore-Penrose inverse...")

        # this is taken from
        # http:#de.mathworks.com/help/matlab/ref/pinv.html
        tmp = [[64, 2, 3, 61, 60, 6], [9, 55, 54, 12, 13, 51],
               [17, 47, 46, 20, 21, 43], [40, 26, 27, 37, 36, 30],
               [32, 34, 35, 29, 28, 38], [41, 23, 22, 44, 45, 19],
               [49, 15, 14, 52, 53, 11], [8, 58, 59, 5, 4, 62]]
        A = Matrix(8, 6)
        for i in range(8):
            for j in range(6):
                A[i][j] = tmp[i][j]

        P = moorePenroseInverse(A)
        b = Array(8, 260.0)
        x = P * b

        cached = [
            1.153846153846152, 1.461538461538463, 1.384615384615384,
            1.384615384615385, 1.461538461538462, 1.153846153846152]
        tol = 500.0 * QL_EPSILON

        for i in range(6):
            self.assertFalse(abs(x[i] - cached[i]) > tol)

        y = A * x
        tol2 = 2000.0 * QL_EPSILON
        for i in range(6):
            self.assertFalse(abs(y[i] - 260.0) > tol2)

    @unittest.skip('skip testIterativeSolvers')
    def testIterativeSolvers(self):
        pass

    @unittest.skip('skip testInitializers')
    def testInitializers(self):
        pass

    @unittest.skip('skip testInitializers')
    def testSparseMatrixMemory(self):
        pass
