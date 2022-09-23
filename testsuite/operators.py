import unittest
from math import log

from QuantLib import *

from utilities import *


class OperatorTest(unittest.TestCase):

    def testTridiagonal(self):

        TEST_MESSAGE(
            "Testing tridiagonal operator...")

        n = 8

        T = TridiagonalOperator(n)
        T.setFirstRow(1.0, 2.0)
        T.setMidRows(0.0, 2.0, 0.0)
        T.setLastRow(2.0, 1.0)

        original = Array(n, 1.0)

        intermediate = T.applyTo(original)

        final = Array(intermediate)
        T.solveFor(final, final)
        for i in range(n):
            self.assertFalse(final[i] != original[i])

        final = Array(n, 0.0)
        temp = Array(intermediate)
        T.solveFor(temp, final)
        for i in range(n):
            self.assertFalse(temp[i] != intermediate[i])

        for i in range(n):
            self.assertFalse(final[i] != original[i])

        final = T.solveFor(temp)
        for i in range(n):
            self.assertFalse(temp[i] != intermediate[i])

        for i in range(n):
            self.assertFalse(final[i] != original[i])

        delta = 0.0
        error = 0.0
        tolerance = 1e-9
        final = T.SOR(temp, tolerance)
        for i in range(n):
            delta = final[i] - original[i]
            error += delta * delta
            self.assertFalse(temp[i] != intermediate[i])

        self.assertFalse(error > tolerance)

    def testConsistency(self):

        TEST_MESSAGE(
            "Testing differential operators...")

        average = 0.0
        sigma = 1.0

        normal = NormalDistribution(average, sigma)
        cum = CumulativeNormalDistribution(average, sigma)

        xMin = average - 4 * sigma
        xMax = average + 4 * sigma
        N = 10001

        h = (xMax - xMin) / (N - 1)

        x = Array(N)
        y = Array(N)
        yi = Array(N)
        yd = Array(N)
        temp = Array(N)
        diff = Array(N)

        for i in range(N):
            x[i] = xMin + h * i

        for i in range(len(x)):
            y[i] = normal(x[i])
            yi[i] = cum(x[i])

        for i in range(len(x)):
            yd[i] = normal.derivative(x[i])

        D = DZero(N, h)
        D2 = DPlusDMinus(N, h)

        temp = D.applyTo(yi)

        for i in range(len(y)):
            diff[i] = y[i] - temp[i]
        e = norm(diff, h)
        self.assertFalse(e > 1.0e-6)

        temp = D2.applyTo(yi)

        for i in range(len(yd)):
            diff[i] = yd[i] - temp[i]
        e = norm(diff, h)
        self.assertFalse(e > 1.0e-4)

    def testBSMOperatorConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of BSM operators...")

        grid = Array(10)
        price = 20.0
        factor = 1.1

        for i in range(len(grid)):
            grid[i] = price

            price *= factor

        dx = log(factor)
        r = 0.05
        q = 0.01
        sigma = 0.5

        ref = BSMOperator(len(grid), dx, r, q, sigma)

        dc = Actual360()
        today = knownGoodDefault
        exercise = today + Period(2, Years)
        residualTime = dc.yearFraction(today, exercise)

        spot = SimpleQuote(0.0)
        qTS = flatRate(today, q, dc)
        rTS = flatRate(today, r, dc)
        volTS = flatVol(today, sigma, dc)
        stochProcess = GeneralizedBlackScholesProcess(
            QuoteHandle(spot), YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        op2 = BSMTermOperator(grid, stochProcess, residualTime)

        tolerance = 1.0e-6

        lderror = ref.lowerDiagonal() - op2.lowerDiagonal()
        derror = ref.diagonal() - op2.diagonal()
        uderror = ref.upperDiagonal() - op2.upperDiagonal()

        for i in range(2, len(grid) - 2):
            self.assertFalse(
                abs(lderror[i]) > tolerance or
                abs(derror[i]) > tolerance or
                abs(uderror[i]) > tolerance)
