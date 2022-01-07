import unittest
from utilities import *
from QuantLib import *
from math import sin, sqrt, cos
import numpy as np


def isTheSame(a, b):
    eps = 500 * QL_EPSILON

    if abs(b) < QL_EPSILON:
        return abs(a) < eps
    else:
        return abs((a - b) / b) < eps


def vandermondeCoefficients(
        order, x, gridPoints):
    q = gridPoints - x
    n = len(gridPoints)

    m = Matrix(n, n, 1.0)
    for i in range(n):
        fact = Factorial.get(i)
        for j in range(n):
            m[i][j] = pow(q[j], i) / fact

    b = Array(n, 0.0)
    b[order] = 1.0
    return inverse(m) * b


class NumericalDifferentiationTest(unittest.TestCase):

    def testTabulatedCentralScheme(self):
        TEST_MESSAGE("Testing numerical differentiation "
                     "using the central scheme...")
        f = lambda x: x

        central = NumericalDifferentiation.Central

        # see http:#en.wikipedia.org/wiki/Finite_difference_coefficient
        nd = NumericalDifferentiation(f, 1, 1.0, 3, central)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [-0.5, 0.0, 0.5])

        nd = NumericalDifferentiation(f, 1, 0.5, 3, central)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [-1.0, 0.0, 1.0])

        nd = NumericalDifferentiation(f, 1, 0.25, 7, central)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [-4 / 60.0, 12 / 20.0, -12 / 4.0, 0.0, 12 / 4.0, -12 / 20.0, 4 / 60.0])

        nd = NumericalDifferentiation(f, 4, pow(0.5, 0.25), 9, central)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [14 / 240.0, -4 / 5.0, 338 / 60.0, -244 / 15.0, 182 / 8.0, -244 / 15.0, 338 / 60.0, -4 / 5.0, 14 / 240.0])

        nd = NumericalDifferentiation(f, 1, 0.5, 7, central)
        self.checkTwoArraysAreTheSame(
            nd.offsets(),
            [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5])

    def testTabulatedBackwardScheme(self):
        TEST_MESSAGE("Testing numerical differentiation "
                     "using the backward scheme...")
        f = lambda x: x

        backward = NumericalDifferentiation.Backward

        # see http:#en.wikipedia.org/wiki/Finite_difference_coefficient
        nd = NumericalDifferentiation(f, 1, 1.0, 2, backward)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [1.0, -1.0])

        nd = NumericalDifferentiation(f, 2, 2.0, 4, backward)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [2 / 4.0, -5 / 4.0, 4 / 4.0, -1.0 / 4.0])

        nd = NumericalDifferentiation(f, 4, 1.0, 6, backward)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [3.0, -14.0, 26.0, -24.0, 11.0, -2.0])

        nd = NumericalDifferentiation(f, 2, 0.5, 4, backward)
        self.checkTwoArraysAreTheSame(
            nd.offsets(),
            [0.0, -0.5, -1.0, -1.5])

    def testTabulatedForwardScheme(self):
        TEST_MESSAGE("Testing numerical differentiation "
                     "using the Forward scheme...")
        f = lambda x: x

        forward = NumericalDifferentiation.Forward

        # see http:#en.wikipedia.org/wiki/Finite_difference_coefficient
        nd = NumericalDifferentiation(f, 1, 1.0, 2, forward)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [-1.0, 1.0])

        nd = NumericalDifferentiation(f, 1, 0.5, 3, forward)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [-6 / 2.0, 4.0, -2 / 2.0])

        nd = NumericalDifferentiation(f, 1, 0.5, 7, forward)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [-98 / 20.0, 12.0, -30 / 2.0, 40 / 3.0, -30 / 4.0, 12 / 5.0, -2 / 6.0])

        nd = NumericalDifferentiation(f, 2, 0.5, 4, forward)
        self.checkTwoArraysAreTheSame(
            nd.offsets(),
            [0.0, 0.5, 1.0, 1.5])

    def testIrregularSchemeFirstOrder(self):
        TEST_MESSAGE("Testing numerical differentiation "
                     "of first order using an irregular scheme...")
        f = lambda x: x

        h1 = 5e-7
        h2 = 3e-6

        alpha = -h2 / (h1 * (h1 + h2))
        gamma = h1 / (h2 * (h1 + h2))
        beta = -alpha - gamma

        offsets = Array(3)
        offsets[0] = -h1
        offsets[1] = 0.0
        offsets[2] = h2

        nd = NumericalDifferentiation(f, 1, offsets)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [alpha, beta, gamma])

    def testIrregularSchemeSecondOrder(self):
        TEST_MESSAGE("Testing numerical differentiation "
                     "of second order using an irregular scheme...")
        f = lambda x: x

        h1 = 2e-7
        h2 = 8e-8

        alpha = 2 / (h1 * (h1 + h2))
        gamma = 2 / (h2 * (h1 + h2))
        beta = -alpha - gamma

        offsets = Array(3)
        offsets[0] = -h1
        offsets[1] = 0.0
        offsets[2] = h2

        nd = NumericalDifferentiation(f, 2, offsets)
        self.checkTwoArraysAreTheSame(
            nd.weights(),
            [alpha, beta, gamma])

    def testDerivativesOfSineFunction(self):
        TEST_MESSAGE("Testing numerical differentiation"
                     " of sin function...")

        f = sin

        df_central = NumericalDifferentiation(
            f, 1, sqrt(QL_EPSILON), 3,
            NumericalDifferentiation.Central)

        df_backward = NumericalDifferentiation(
            f, 1, sqrt(QL_EPSILON), 3,
            NumericalDifferentiation.Backward)

        df_forward = NumericalDifferentiation(
            f, 1, sqrt(QL_EPSILON), 3,
            NumericalDifferentiation.Forward)

        for x in np.arange(0.0, 5.0, 0.1):
            calculatedCentral = df_central(x)
            calculatedBackward = df_backward(x)
            calculatedForward = df_forward(x)
            expected = cos(x)

            self.singleValueTest("central first", calculatedCentral, expected, 1e-8)
            self.singleValueTest("backward first", calculatedBackward, expected, 1e-6)
            self.singleValueTest("forward first", calculatedForward, expected, 1e-6)

        df4_central = NumericalDifferentiation(
            f, 4, 1e-2, 7,
            NumericalDifferentiation.Central)
        df4_backward = NumericalDifferentiation(
            f, 4, 1e-2, 7,
            NumericalDifferentiation.Backward)
        df4_forward = NumericalDifferentiation(
            f, 4, 1e-2, 7,
            NumericalDifferentiation.Forward)

        for x in np.arange(0.0, 5.0, 0.1):
            calculatedCentral = df4_central(x)
            calculatedBackward = df4_backward(x)
            calculatedForward = df4_forward(x)
            expected = sin(x)

            self.singleValueTest("central 4th", calculatedCentral, expected, 1e-4)
            self.singleValueTest("backward 4th", calculatedBackward, expected, 1e-4)
            self.singleValueTest("forward 4th", calculatedForward, expected, 1e-4)

        offsets = Array(5)
        offsets[0] = -0.01
        offsets[1] = -0.02
        offsets[2] = 0.03
        offsets[3] = 0.014
        offsets[4] = 0.041
        df3_irregular = NumericalDifferentiation(f, 3, offsets)

        self.checkTwoArraysAreTheSame(df3_irregular.offsets(), offsets)

        for x in np.arange(0.0, 5.0, 0.1):
            calculatedIrregular = df3_irregular(x)
            expected = -cos(x)

            self.singleValueTest("irregular 3th", calculatedIrregular, expected, 5e-5)

    def testCoefficientBasedOnVandermonde(self):
        TEST_MESSAGE("Testing coefficients from numerical differentiation"
                     " by comparison with results from"
                     " Vandermonde matrix inversion...")
        f = lambda x: x

        for order in range(5):
            for nGridPoints in range(order + 1, order + 3):

                gridPoints = Array(nGridPoints)
                for i in range(nGridPoints):
                    p = i
                    gridPoints[i] = sin(p) + cos(p)  # strange points

                x = 0.3902842  # strange points
                weightsVandermonde = vandermondeCoefficients(order, x, gridPoints)
                nd = NumericalDifferentiation(f, order, gridPoints - x)

                self.checkTwoArraysAreTheSame(gridPoints, nd.offsets() + x)
                self.checkTwoArraysAreTheSame(weightsVandermonde, nd.weights())

    def checkTwoArraysAreTheSame(self,
                                 calculated,
                                 expected):
        isSame = True
        for i in range(min(len(calculated), len(expected))):
            isSame = isSame and isTheSame(calculated[i], expected[i])
        correct = (len(calculated) == len(expected)) and isSame
        self.assertFalse(not correct)

    def singleValueTest(self,
                        comment,
                        calculated,
                        expected,
                        tol):
        self.assertFalse(abs(calculated - expected) > tol)
