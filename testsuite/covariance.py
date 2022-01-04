import unittest
from utilities import *
from QuantLib import *
from math import sqrt


def norm(m):
    sum = 0.0
    for i in range(m.rows()):
        for j in range(m.columns()):
            sum += m[i][j] * m[i][j]
    return sqrt(sum)


class CovarianceTest(unittest.TestCase):
    def testRankReduction(self):
        TEST_MESSAGE("Testing matrix rank reduction salvaging algorithms...")

        n = 3

        badCorr = Matrix(n, n)
        badCorr[0][0] = 1.0
        badCorr[0][1] = 0.9
        badCorr[0][2] = 0.7
        badCorr[1][0] = 0.9
        badCorr[1][1] = 1.0
        badCorr[1][2] = 0.3
        badCorr[2][0] = 0.7
        badCorr[2][1] = 0.3
        badCorr[2][2] = 1.0

        goodCorr = Matrix(n, n)
        goodCorr[0][0] = goodCorr[1][1] = goodCorr[2][2] = 1.00000000000
        goodCorr[0][1] = goodCorr[1][0] = 0.894024408508599
        goodCorr[0][2] = goodCorr[2][0] = 0.696319066114392
        goodCorr[1][2] = goodCorr[2][1] = 0.300969036104592

        b = rankReducedSqrt(badCorr, 3, 1.0, SalvagingAlgorithm.Spectral)
        calcCorr = b * transpose(b)

        for i in range(n):
            for j in range(n):
                expected = goodCorr[i][j]
                calculated = calcCorr[i][j]
                self.assertFalse(abs(calculated - expected) > 1.0e-10)

        badCov = Matrix(n, n)
        badCov[0][0] = 0.04000
        badCov[0][1] = 0.03240
        badCov[0][2] = 0.02240
        badCov[1][0] = 0.03240
        badCov[1][1] = 0.03240
        badCov[1][2] = 0.00864
        badCov[2][0] = 0.02240
        badCov[2][1] = 0.00864
        badCov[2][2] = 0.02560

        b = pseudoSqrt(badCov, SalvagingAlgorithm.Spectral)
        b = rankReducedSqrt(badCov, 3, 1.0, SalvagingAlgorithm.Spectral)
        goodCov = b * transpose(b)

        error = norm(goodCov - badCov)
        self.assertFalse(error > 4.0e-4)

    def testSalvagingMatrix(self):
        TEST_MESSAGE("Testing positive semi-definiteness salvaging "
                     "algorithms...")

        n = 3

        badCorr = Matrix(n, n)
        badCorr[0][0] = 1.0
        badCorr[0][1] = 0.9
        badCorr[0][2] = 0.7
        badCorr[1][0] = 0.9
        badCorr[1][1] = 1.0
        badCorr[1][2] = 0.3
        badCorr[2][0] = 0.7
        badCorr[2][1] = 0.3
        badCorr[2][2] = 1.0

        goodCorr = Matrix(n, n)
        goodCorr[0][0] = goodCorr[1][1] = goodCorr[2][2] = 1.00000000000
        goodCorr[0][1] = goodCorr[1][0] = 0.894024408508599
        goodCorr[0][2] = goodCorr[2][0] = 0.696319066114392
        goodCorr[1][2] = goodCorr[2][1] = 0.300969036104592

        b = pseudoSqrt(badCorr, SalvagingAlgorithm.Spectral)

        calcCorr = b * transpose(b)

        for i in range(n):
            for j in range(n):
                expected = goodCorr[i][j]
                calculated = calcCorr[i][j]
                self.assertFalse(abs(calculated - expected) > 1.0e-10)

        badCov = Matrix(n, n)
        badCov[0][0] = 0.04000
        badCov[0][1] = 0.03240
        badCov[0][2] = 0.02240
        badCov[1][0] = 0.03240
        badCov[1][1] = 0.03240
        badCov[1][2] = 0.00864
        badCov[2][0] = 0.02240
        badCov[2][1] = 0.00864
        badCov[2][2] = 0.02560

        b = pseudoSqrt(badCov, SalvagingAlgorithm.Spectral)
        goodCov = b * transpose(b)

        error = norm(goodCov - badCov)
        self.assertFalse(error > 4.0e-4)

    def testCovariance(self):
        TEST_MESSAGE("Testing covariance and correlation calculations...")

        data = [
            [3.0, 9.0],
            [2.0, 7.0],
            [4.0, 12.0],
            [5.0, 15.0],
            [6.0, 17.0]]
        weights = DoubleVector(len(data), 1.0)

        n = len(data[0])

        expCor = Matrix(n, n)
        expCor[0][0] = 1.0000000000000000
        expCor[0][1] = 0.9970544855015813
        expCor[1][0] = 0.9970544855015813
        expCor[1][1] = 1.0000000000000000

        s = SequenceStatistics(n)
        temp = DoubleVector(n)

        for i in range(len(data)):
            for j in range(n):
                temp[j] = data[i][j]

            s.add(temp, weights[i])

        std = s.standardDeviation()
        calcCov = s.covariance()
        calcCor = s.correlation()

        expCov = Matrix(n, n)
        for i in range(n):
            expCov[i][i] = std[i] * std[i]
            for j in range(i):
                expCov[i][j] = expCov[j][i] = expCor[i][j] * std[i] * std[j]

        for i in range(n):
            for j in range(n):
                expected = expCor[i][j]
                calculated = calcCor[i][j]
                self.assertFalse(abs(calculated - expected) > 1.0e-10)

                expected = expCov[i][j]
                calculated = calcCov[i][j]
                self.assertFalse(abs(calculated - expected) > 1.0e-10)

        calcCov = getCovariance(std, expCor)

        for i in range(n):
            for j in range(n):
                calculated = calcCov[i][j]
                expected = expCov[i][j]
                self.assertFalse(abs(calculated - expected) > 1.0e-10)

        covDecomposition = CovarianceDecomposition(expCov)
        calcCor = covDecomposition.correlationMatrix()
        calcStd = covDecomposition.standardDeviations()

        for i in range(n):
            calculated = calcStd[i]
            expected = std[i]
            self.assertFalse(abs(calculated - expected) > 1.0e-16)
            for j in range(n):
                calculated = calcCor[i][j]
                expected = expCor[i][j]
                self.assertFalse(abs(calculated - expected) > 1.0e-14)
