import unittest
from utilities import *
from QuantLib import *
from math import exp, sin, cos, sqrt, sinh, log, isnan
import numpy as np


def sign(y1, y2):
    if y1 == y2:
        return 0
    elif y1 < y2:
        return 1
    else:
        return -1


def xRange(start, finish, points):
    x = Array(points)
    dx = (finish - start) / (points - 1)
    for i in range(points - 1):
        x[i] = start + i * dx
    x[points - 1] = finish
    return x


def gaussian(x):
    y = Array(len(x))
    for i in range(len(x)):
        y[i] = exp(-x[i] * x[i])
    return y


def parabolic(x):
    y = Array(len(x))
    for i in range(len(x)):
        y[i] = -x[i] * x[i]
    return y


class errorFunction(object):
    def __init__(self, f):
        self.f_ = f

    def __call__(self, x):
        temp = self.f_(x) - exp(-x * x)
        return temp * temp


def make_error_function(f):
    return errorFunction(f)


def multif(s, t, u, v, w):
    return sqrt(
        s * sinh(log(t)) +
        exp(sin(u) * sin(3 * v)) +
        sinh(log(v * w)))


def epanechnikovKernel(u):
    if abs(u) <= 1:
        return (3.0 / 4.0) * (1 - u * u)
    else:
        return 0.0


class GF(object):
    def __init__(self, exponent, factor):
        self.exponent_ = exponent
        self.factor_ = factor

    def __call__(self, h):
        return M_PI + \
               self.factor_ * pow(h, self.exponent_) + \
               pow(self.factor_ * h, self.exponent_ + 1)


def limCos(h):
    return -cos(h)


class InterpolationTest(unittest.TestCase):
    # # cubic spline tests
    def testSplineOnGenericValues(self):
        TEST_MESSAGE("Testing spline interpolation on generic values...")

        generic_x = [0.0, 1.0, 3.0, 4.0]
        generic_y = [0.0, 0.0, 2.0, 2.0]
        generic_natural_y2 = [0.0, 1.5, -1.5, 0.0]

        i = len(generic_x)
        n = len(generic_x)
        x35 = DoubleVector(3)

        # spline
        f = SafeCubicInterpolation(
            generic_x,
            generic_y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.SecondDerivative,
            generic_natural_y2[0],
            CubicInterpolation.SecondDerivative,
            generic_natural_y2[n - 1])
        f.update()
        self._checkValues("spline", f, generic_x, generic_y)
        # cached second derivative
        for i in range(n):
            interpolated = f.secondDerivative(generic_x[i])
            error = interpolated - generic_natural_y2[i]
            self.assertFalse(abs(error) > 3e-16)
        x35[1] = f(3.5)

        # Clamped spline
        y1a = 0.0
        y1b = 0.0
        f = SafeCubicInterpolation(
            generic_x, generic_y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.FirstDerivative, y1a,
            CubicInterpolation.FirstDerivative, y1b)
        f.update()
        self._checkValues("Clamped spline", f, generic_x, generic_y)
        self._check1stDerivativeValue("Clamped spline", f, generic_x[0], 0.0)
        self._check1stDerivativeValue("Clamped spline", f, generic_x[-1], 0.0)
        x35[0] = f(3.5)

        # Not-a-knot spline
        f = SafeCubicInterpolation(
            generic_x, generic_y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.NotAKnot, NullReal(),
            CubicInterpolation.NotAKnot, NullReal())
        f.update()
        self._checkValues("Not-a-knot spline", f, generic_x, generic_y)
        self._checkNotAKnotCondition("Not-a-knot spline", f)

        x35[2] = f(3.5)

        self.assertFalse(x35[0] > x35[1] or x35[1] > x35[2])

    def testSimmetricEndConditions(self):
        TEST_MESSAGE("Testing symmetry of spline interpolation "
                     "end-conditions...")

        n = 9
        x = xRange(-1.8, 1.8, n)
        y = gaussian(x)

        # Not-a-knot spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.NotAKnot, NullReal(),
            CubicInterpolation.NotAKnot, NullReal())
        f.update()
        self._checkValues("Not-a-knot spline", f, x, y)
        self._checkNotAKnotCondition("Not-a-knot spline", f)
        self._checkSymmetry("Not-a-knot spline", f, x[0])

        # MC not-a-knot spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.NotAKnot, NullReal(),
            CubicInterpolation.NotAKnot, NullReal())
        f.update()
        self._checkValues("MC not-a-knot spline", f, x, y)
        self._checkSymmetry("MC not-a-knot spline", f, x[0])

    def testDerivativeEndConditions(self):
        TEST_MESSAGE("Testing derivative end-conditions "
                     "for spline interpolation...")

        n = 4

        x = xRange(-2.0, 2.0, n)
        y = parabolic(x)

        # Not-a-knot spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.NotAKnot, NullReal(),
            CubicInterpolation.NotAKnot, NullReal())
        f.update()
        self._checkValues("Not-a-knot spline", f, x, y)
        self._check1stDerivativeValue("Not-a-knot spline", f, x[0], 4.0)
        self._check1stDerivativeValue("Not-a-knot spline", f, x[n - 1], -4.0)
        self._check2ndDerivativeValue("Not-a-knot spline", f, x[0], -2.0)
        self._check2ndDerivativeValue("Not-a-knot spline", f, x[n - 1], -2.0)

        # Clamped spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.FirstDerivative, 4.0,
            CubicInterpolation.FirstDerivative, -4.0)
        f.update()
        self._checkValues("Clamped spline", f, x, y)
        self._check1stDerivativeValue("Clamped spline", f, x[0], 4.0)
        self._check1stDerivativeValue("Clamped spline", f, x[n - 1], -4.0)
        self._check2ndDerivativeValue("Clamped spline", f, x[0], -2.0)
        self._check2ndDerivativeValue("Clamped spline", f, x[n - 1], -2.0)

        # SecondDerivative spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.SecondDerivative, -2.0,
            CubicInterpolation.SecondDerivative, -2.0)
        f.update()
        self._checkValues("SecondDerivative spline", f, x, y)
        self._check1stDerivativeValue("SecondDerivative spline", f, x[0], 4.0)
        self._check1stDerivativeValue("SecondDerivative spline", f, x[n - 1], -4.0)
        self._check2ndDerivativeValue("SecondDerivative spline", f, x[0], -2.0)
        self._check2ndDerivativeValue("SecondDerivative spline", f, x[n - 1], -2.0)

        # MC Not-a-knot spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.NotAKnot, NullReal(),
            CubicInterpolation.NotAKnot, NullReal())
        f.update()
        self._checkValues("MC Not-a-knot spline", f, x, y)
        self._check1stDerivativeValue("MC Not-a-knot spline", f, x[0], 4.0)
        self._check1stDerivativeValue("MC Not-a-knot spline", f, x[n - 1], -4.0)
        self._check2ndDerivativeValue("MC Not-a-knot spline", f, x[0], -2.0)
        self._check2ndDerivativeValue("MC Not-a-knot spline", f, x[n - 1], -2.0)

        # MC Clamped spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.FirstDerivative, 4.0,
            CubicInterpolation.FirstDerivative, -4.0)
        f.update()
        self._checkValues("MC Clamped spline", f, x, y)
        self._check1stDerivativeValue("MC Clamped spline", f, x[0], 4.0)
        self._check1stDerivativeValue("MC Clamped spline", f, x[n - 1], -4.0)
        self._check2ndDerivativeValue("MC Clamped spline", f, x[0], -2.0)
        self._check2ndDerivativeValue("MC Clamped spline", f, x[n - 1], -2.0)

        # MC SecondDerivative spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.SecondDerivative, -2.0,
            CubicInterpolation.SecondDerivative, -2.0)
        f.update()
        self._checkValues("MC SecondDerivative spline", f, x, y)
        self._check1stDerivativeValue("MC SecondDerivative spline", f, x[0], 4.0)
        self._check1stDerivativeValue("MC SecondDerivative spline", f, x[n - 1], -4.0)
        self._check2ndDerivativeValue("SecondDerivative spline", f, x[0], -2.0)
        self._check2ndDerivativeValue("MC SecondDerivative spline", f, x[n - 1], -2.0)

    def testNonRestrictiveHymanFilter(self):
        TEST_MESSAGE("Testing non-restrictive Hyman filter...")

        n = 4

        x = xRange(-2.0, 2.0, n)
        y = parabolic(x)
        zero = 0.0
        interpolated = 0.0
        expected = 0.0

        # MC Not-a-knot spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.NotAKnot, NullReal(),
            CubicInterpolation.NotAKnot, NullReal())
        f.update()
        interpolated = f(zero)
        self.assertFalse(abs(interpolated - expected) > 1e-15)

        # MC Clamped spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.FirstDerivative, 4.0,
            CubicInterpolation.FirstDerivative, -4.0)
        f.update()
        interpolated = f(zero)
        self.assertFalse(abs(interpolated - expected) > 1e-15)

        # MC SecondDerivative spline
        f = SafeCubicInterpolation(
            x, y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.SecondDerivative, -2.0,
            CubicInterpolation.SecondDerivative, -2.0)
        f.update()
        interpolated = f(zero)
        self.assertFalse(abs(interpolated - expected) > 1e-15)

    def testSplineOnRPN15AValues(self):
        TEST_MESSAGE("Testing spline interpolation on RPN15A data set...")

        RPN15A_x = [
            7.99, 8.09, 8.19, 8.7, 9.2, 10.0, 12.0, 15.0, 20.0]
        RPN15A_y = [
            0.0, 2.76429e-5, 4.37498e-5, 0.169183,
            0.469428, 0.943740, 0.998636, 0.999919, 0.999994]

        # spline
        f = SafeCubicInterpolation(
            RPN15A_x,
            RPN15A_y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.SecondDerivative, 0.0,
            CubicInterpolation.SecondDerivative, 0.0)
        f.update()
        self._checkValues("spline", f, RPN15A_x, RPN15A_y)
        self._check2ndDerivativeValue("spline", f, RPN15A_x[0], 0.0)
        self._check2ndDerivativeValue("spline", f, RPN15A_x[-1], 0.0)
        # poor performance
        x_bad = 11.0
        interpolated = f(x_bad)
        self.assertFalse(interpolated < 1.0)

        # Clamped spline
        f = SafeCubicInterpolation(
            RPN15A_x, RPN15A_y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.FirstDerivative, 0.0,
            CubicInterpolation.FirstDerivative, 0.0)
        f.update()
        self._checkValues("Clamped spline", f, RPN15A_x, RPN15A_y)
        self._check1stDerivativeValue("Clamped spline", f, RPN15A_x[0], 0.0)
        self._check1stDerivativeValue("Clamped spline", f, RPN15A_x[-1], 0.0)
        # poor performance
        interpolated = f(x_bad)
        self.assertFalse(interpolated < 1.0)

        # Not-a-knot spline
        f = SafeCubicInterpolation(
            RPN15A_x, RPN15A_y,
            CubicInterpolation.Spline, false,
            CubicInterpolation.NotAKnot, NullReal(),
            CubicInterpolation.NotAKnot, NullReal())
        f.update()
        self._checkValues("Not-a-knot spline", f, RPN15A_x, RPN15A_y)
        self._checkNotAKnotCondition("Not-a-knot spline", f)
        # poor performance
        interpolated = f(x_bad)
        self.assertFalse(interpolated < 1.0)

        # MC natural spline values
        f = SafeCubicInterpolation(
            RPN15A_x, RPN15A_y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.SecondDerivative, 0.0,
            CubicInterpolation.SecondDerivative, 0.0)
        f.update()
        self._checkValues("MC natural spline", f, RPN15A_x, RPN15A_y)
        # good performance
        interpolated = f(x_bad)
        self.assertFalse(interpolated > 1.0)

        # MC clamped spline values
        f = SafeCubicInterpolation(
            RPN15A_x, RPN15A_y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.FirstDerivative, 0.0,
            CubicInterpolation.FirstDerivative, 0.0)
        f.update()
        self._checkValues("MC clamped spline", f, RPN15A_x, RPN15A_y)
        self._check1stDerivativeValue("MC clamped spline", f, RPN15A_x[0], 0.0)
        self._check1stDerivativeValue("MC clamped spline", f, RPN15A_x[-1], 0.0)
        # good performance
        interpolated = f(x_bad)
        self.assertFalse(interpolated > 1.0)

        # MC not-a-knot spline values
        f = SafeCubicInterpolation(
            RPN15A_x, RPN15A_y,
            CubicInterpolation.Spline, true,
            CubicInterpolation.NotAKnot, NullReal(),
            CubicInterpolation.NotAKnot, NullReal())
        f.update()
        self._checkValues("MC not-a-knot spline", f, RPN15A_x, RPN15A_y)
        # good performance
        interpolated = f(x_bad)
        self.assertFalse(interpolated > 1.0)

    def testSplineOnGaussianValues(self):
        # See J. M. Hyman, "Accurate monotonicity preserving cubic interpolation"
        # SIAM J. of Scientific and Statistical Computing, v. 4, 1983, pp. 645-654.
        # http:#math.lanl.gov/~mac/papers/numerics/H83.pdf

        TEST_MESSAGE("Testing spline interpolation on a Gaussian data set...")

        interpolated = 0.0
        interpolated2 = 0.0
        n = 5

        x1_bad = -1.7
        x2_bad = 1.7

        start = -1.9
        for j in range(2):  # (start = -1.9, j = 0 j < 2 start += 0.2, j++):
            x = xRange(start, start + 3.6, n)
            y = gaussian(x)

            # Not-a-knot spline
            f = SafeCubicInterpolation(
                x, y,
                CubicInterpolation.Spline, false,
                CubicInterpolation.NotAKnot, NullReal(),
                CubicInterpolation.NotAKnot, NullReal())
            f.update()
            self._checkValues("Not-a-knot spline", f, x, y)
            self._checkNotAKnotCondition("Not-a-knot spline", f)
            # bad performance
            interpolated = f(x1_bad)
            interpolated2 = f(x2_bad)
            self.assertFalse(interpolated > 0.0 and interpolated2 > 0.0)

            # MC not-a-knot spline
            f = SafeCubicInterpolation(
                x, y,
                CubicInterpolation.Spline, true,
                CubicInterpolation.NotAKnot, NullReal(),
                CubicInterpolation.NotAKnot, NullReal())
            f.update()
            self._checkValues("MC not-a-knot spline", f, x, y)
            # good performance
            interpolated = f(x1_bad)
            self.assertFalse(interpolated < 0.0)

            interpolated = f(x2_bad)
            self.assertFalse(interpolated < 0.0)

            start += 0.2

    def testSplineErrorOnGaussianValues(self):
        # See J. M. Hyman, "Accurate monotonicity preserving cubic interpolation"
        # SIAM J. of Scientific and Statistical Computing, v. 4, 1983, pp. 645-654.
        # http:#math.lanl.gov/~mac/papers/numerics/H83.pdf

        TEST_MESSAGE("Testing spline approximation on Gaussian data sets...")

        points = [5, 9, 17, 33]

        # complete spline data from the original 1983 Hyman paper
        tabulatedErrors = [3.5e-2, 2.0e-3, 4.0e-5, 1.8e-6]
        toleranceOnTabErr = [0.1e-2, 0.1e-3, 0.1e-5, 0.1e-6]

        # (complete) MC spline data from the original 1983 Hyman paper
        # NB: with the improved Hyman filter from the Dougherty, Edelman, and
        #     Hyman 1989 paper the n=17 nonmonotonicity is not filtered anymore
        #     so the error agrees with the non MC method.
        tabulatedMCErrors = [1.7e-2, 2.0e-3, 4.0e-5, 1.8e-6]
        toleranceOnTabMCErr = [0.1e-2, 0.1e-3, 0.1e-5, 0.1e-6]

        integral = SimpsonIntegral(1e-12, 10000)

        # still unexplained scale factor needed to obtain the numerical
        # results from the paper
        scaleFactor = 1.9

        for i in range(len(points)):
            n = points[i]
            x = xRange(-1.7, 1.9, n)
            y = gaussian(x)

            # Not-a-knot
            f = SafeCubicInterpolation(
                x, y,
                CubicInterpolation.Spline, false,
                CubicInterpolation.NotAKnot, NullReal(),
                CubicInterpolation.NotAKnot, NullReal())
            f.update()
            result = sqrt(integral(make_error_function(f), -1.7, 1.9))
            result /= scaleFactor
            self.assertFalse(
                abs(result - tabulatedErrors[i]) > toleranceOnTabErr[i])

            # MC not-a-knot
            f = SafeCubicInterpolation(
                x, y,
                CubicInterpolation.Spline, true,
                CubicInterpolation.NotAKnot, NullReal(),
                CubicInterpolation.NotAKnot, NullReal())
            f.update()
            result = sqrt(integral(make_error_function(f), -1.7, 1.9))
            result /= scaleFactor
            self.assertFalse(
                abs(result - tabulatedMCErrors[i]) > toleranceOnTabMCErr[i])

    def testMultiSpline(self):
        pass

    def testAsFunctor(self):
        TEST_MESSAGE("Testing use of interpolations as functors...")

        x = [0.0, 1.0, 2.0, 3.0, 4.0]
        y = [5.0, 4.0, 3.0, 2.0, 1.0]

        f = SafeLinearInterpolation(x, y)
        f.update()

        x2 = [-2.0, -1.0, 0.0, 1.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        N = len(x2)
        y2 = DoubleVector(N)
        tolerance = 1.0e-12

        # case 1: extrapolation not allowed
        try:
            for i in range(len(x2)):
                y2[i] = f(x2[i])
        except Exception as e:
            print(e)

        # case 2: enable extrapolation
        f.enableExtrapolation()
        y2 = DoubleVector(N)
        for i in range(len(x2)):
            y2[i] = f(x2[i])
        for i in range(N):
            expected = 5.0 - x2[i]
            self.assertFalse(abs(y2[i] - expected) > tolerance)

    def testFritschButland(self):
        TEST_MESSAGE("Testing Fritsch-Butland interpolation...")

        x = [0.0, 1.0, 2.0, 3.0, 4.0]
        y = [[1.0, 2.0, 1.0, 1.0, 2.0],
             [1.0, 2.0, 1.0, 1.0, 1.0],
             [2.0, 1.0, 0.0, 2.0, 3.0]]

        for i in range(3):

            f = SafeFritschButlandCubic(x, y[i])
            f.update()

            for j in range(4):
                left_knot = x[j]
                expected_sign = sign(y[i][j], y[i][j + 1])
                for k in range(10):
                    x1 = left_knot + k * 0.1
                    x2 = left_knot + (k + 1) * 0.1
                    y1 = f(x1)
                    y2 = f(x2)
                    self.assertFalse(isnan(y1))
                    self.assertFalse(sign(y1, y2) != expected_sign)

    # other interpolations
    def testBackwardFlat(self):
        TEST_MESSAGE("Testing backward-flat interpolation...")

        x = [0.0, 1.0, 2.0, 3.0, 4.0]
        y = [5.0, 4.0, 3.0, 2.0, 1.0]

        f = SafeBackwardFlatInterpolation(x, y)
        f.update()

        N = len(x)
        tolerance = 1.0e-12

        # at original points
        for i in range(N):
            p = x[i]
            calculated = f(p)
            expected = y[i]
            self.assertFalse(abs(expected - calculated) > tolerance)

        # at middle points
        for i in range(N - 1):
            p = (x[i] + x[i + 1]) / 2
            calculated = f(p)
            expected = y[i + 1]
            self.assertFalse(abs(expected - calculated) > tolerance)

        # outside the original range
        f.enableExtrapolation()

        p = x[0] - 0.5
        calculated = f(p)
        expected = y[0]
        self.assertFalse(abs(expected - calculated) > tolerance)

        p = x[N - 1] + 0.5
        calculated = f(p)
        expected = y[N - 1]
        self.assertFalse(abs(expected - calculated) > tolerance)

        # primitive at original points
        calculated = f.primitive(x[0])
        expected = 0.0
        self.assertFalse(abs(expected - calculated) > tolerance)

        sum = 0.0
        for i in range(1, N):
            sum += (x[i] - x[i - 1]) * y[i]
            calculated = f.primitive(x[i])
            expected = sum
            self.assertFalse(abs(expected - calculated) > tolerance)

        # primitive at middle points
        sum = 0.0
        for i in range(N - 1):
            p = (x[i] + x[i + 1]) / 2
            sum += (x[i + 1] - x[i]) * y[i + 1] / 2
            calculated = f.primitive(p)
            expected = sum
            sum += (x[i + 1] - x[i]) * y[i + 1] / 2
            self.assertFalse(abs(expected - calculated) > tolerance)

    def testForwardFlat(self):
        TEST_MESSAGE("Testing forward-flat interpolation...")

        x = [0.0, 1.0, 2.0, 3.0, 4.0]
        y = [5.0, 4.0, 3.0, 2.0, 1.0]

        f = SafeForwardFlatInterpolation(x, y)
        f.update()

        N = len(x)

        tolerance = 1.0e-12

        # at original points
        for i in range(N):
            p = x[i]
            calculated = f(p)
            expected = y[i]
            self.assertFalse(abs(expected - calculated) > tolerance)

        # at middle points
        for i in range(N - 1):
            p = (x[i] + x[i + 1]) / 2
            calculated = f(p)
            expected = y[i]
            self.assertFalse(abs(expected - calculated) > tolerance)

        # outside the original range
        f.enableExtrapolation()

        p = x[0] - 0.5
        calculated = f(p)
        expected = y[0]
        self.assertFalse(abs(expected - calculated) > tolerance)

        p = x[N - 1] + 0.5
        calculated = f(p)
        expected = y[N - 1]
        self.assertFalse(abs(expected - calculated) > tolerance)

        # primitive at original points
        calculated = f.primitive(x[0])
        expected = 0.0
        self.assertFalse(abs(expected - calculated) > tolerance)

        sum = 0.0
        for i in range(1, N):
            sum += (x[i] - x[i - 1]) * y[i - 1]
            calculated = f.primitive(x[i])
            expected = sum
            self.assertFalse(abs(expected - calculated) > tolerance)

        # primitive at middle points
        sum = 0.0
        for i in range(N - 1):
            p = (x[i] + x[i + 1]) / 2
            sum += (x[i + 1] - x[i]) * y[i] / 2
            calculated = f.primitive(p)
            expected = sum
            sum += (x[i + 1] - x[i]) * y[i] / 2
            self.assertFalse(abs(expected - calculated) > tolerance)

    def testSabrInterpolation(self):
        TEST_MESSAGE("Testing Sabr interpolation...")

        # Test SABR function against input volatilities
        tolerance = 1.0e-12
        strikes = Array(31)
        volatilities = Array(31)
        # input strikes
        strikes[0] = 0.03
        strikes[1] = 0.032
        strikes[2] = 0.034
        strikes[3] = 0.036
        strikes[4] = 0.038
        strikes[5] = 0.04
        strikes[6] = 0.042
        strikes[7] = 0.044
        strikes[8] = 0.046
        strikes[9] = 0.048
        strikes[10] = 0.05
        strikes[11] = 0.052
        strikes[12] = 0.054
        strikes[13] = 0.056
        strikes[14] = 0.058
        strikes[15] = 0.06
        strikes[16] = 0.062
        strikes[17] = 0.064
        strikes[18] = 0.066
        strikes[19] = 0.068
        strikes[20] = 0.07
        strikes[21] = 0.072
        strikes[22] = 0.074
        strikes[23] = 0.076
        strikes[24] = 0.078
        strikes[25] = 0.08
        strikes[26] = 0.082
        strikes[27] = 0.084
        strikes[28] = 0.086
        strikes[29] = 0.088
        strikes[30] = 0.09
        # input volatilities
        volatilities[0] = 1.16725837321531
        volatilities[1] = 1.15226075991385
        volatilities[2] = 1.13829711098834
        volatilities[3] = 1.12524190877505
        volatilities[4] = 1.11299079244474
        volatilities[5] = 1.10145609357162
        volatilities[6] = 1.09056348513411
        volatilities[7] = 1.08024942745106
        volatilities[8] = 1.07045919457758
        volatilities[9] = 1.06114533019077
        volatilities[10] = 1.05226642581503
        volatilities[11] = 1.04378614411707
        volatilities[12] = 1.03567243073732
        volatilities[13] = 1.0278968727451
        volatilities[14] = 1.02043417226345
        volatilities[15] = 1.01326171139321
        volatilities[16] = 1.00635919013311
        volatilities[17] = 0.999708323124949
        volatilities[18] = 0.993292584155381
        volatilities[19] = 0.987096989695393
        volatilities[20] = 0.98110791455717
        volatilities[21] = 0.975312934134512
        volatilities[22] = 0.969700688771689
        volatilities[23] = 0.964260766651027
        volatilities[24] = 0.958983602256592
        volatilities[25] = 0.953860388001395
        volatilities[26] = 0.948882997029509
        volatilities[27] = 0.944043915545469
        volatilities[28] = 0.939336183299237
        volatilities[29] = 0.934753341079515
        volatilities[30] = 0.930289384251337

        expiry = 1.0
        forward = 0.039
        # input SABR coefficients (corresponding to the vols above)
        initialAlpha = 0.3
        initialBeta = 0.6
        initialNu = 0.02
        initialRho = 0.01
        # calculate SABR vols and compare with input vols
        for i in range(len(strikes)):
            calculatedVol = sabrVolatility(
                strikes[i], forward, expiry,
                initialAlpha, initialBeta,
                initialNu, initialRho)
            self.assertFalse(
                abs(volatilities[i] - calculatedVol) > tolerance)

        # Test SABR calibration against input parameters
        # Use default values (but not null, since then parameters
        # will then not be fixed during optimization, see the
        # interpolation constructor, thus rendering the test cases
        # with fixed parameters non-sensical)
        alphaGuess = sqrt(0.2)
        betaGuess = 0.5
        nuGuess = sqrt(0.4)
        rhoGuess = 0.0

        vegaWeighted = [true, false]
        isAlphaFixed = [true, false]
        isBetaFixed = [true, false]
        isNuFixed = [true, false]
        isRhoFixed = [true, false]

        calibrationTolerance = 5.0e-8
        # initialize optimization methods
        methods_ = [
            Simplex(0.01),
            LevenbergMarquardt(1e-8, 1e-8, 1e-8)]
        # Initialize end criteria
        endCriteria = EndCriteria(100000, 100, 1e-8, 1e-8, 1e-8)
        # Test looping over all possibilities
        for method in methods_:
            for i in vegaWeighted:
                for k_a in isAlphaFixed:
                    for k_b in isBetaFixed:
                        for k_n in isNuFixed:
                            for k_r in isRhoFixed:
                                # to meet the tough calibration tolerance we need to lower the default
                                # error threshold for accepting a calibration (to be more specific,
                                # some of the new test cases arising from fixing a subset of the
                                # model's parameters do not calibrate with the desired error using the
                                # initial guess (i.e. optimization runs into a local minimum) - then a
                                # series of random start values for optimization is chosen until our
                                # tight custom error threshold is satisfied.
                                sabrInterpolation = SafeSABRInterpolation(
                                    strikes, volatilities, expiry, forward,
                                    # k_a ? initialAlpha: alphaGuess,
                                    initialAlpha if k_a else alphaGuess,
                                    # k_b ? initialBeta: betaGuess,
                                    initialBeta if k_b else betaGuess,
                                    # k_n ? initialNu: nuGuess,
                                    initialNu if k_n else nuGuess,
                                    # k_r ? initialRho: rhoGuess,
                                    initialRho if k_r else rhoGuess,
                                    k_a, k_b, k_n, k_r, i, endCriteria,
                                    method, 1E-10)
                                sabrInterpolation.update()

                                # Recover SABR calibration parameters
                                failed = false
                                calibratedAlpha = sabrInterpolation.alpha()
                                calibratedBeta = sabrInterpolation.beta()
                                calibratedNu = sabrInterpolation.nu()
                                calibratedRho = sabrInterpolation.rho()

                                # compare results: alpha
                                error = abs(initialAlpha - calibratedAlpha)
                                self.assertFalse(error > calibrationTolerance)
                                # Beta
                                error = abs(initialBeta - calibratedBeta)
                                self.assertFalse(error > calibrationTolerance)
                                # Nu
                                error = abs(initialNu - calibratedNu)
                                self.assertFalse(error > calibrationTolerance)
                                # Rho
                                error = abs(initialRho - calibratedRho)
                                self.assertFalse(error > calibrationTolerance)

                                self.assertFalse(failed)

    def testKernelInterpolation(self):
        TEST_MESSAGE("Testing kernel 1D interpolation...")

        deltaGrid = [0.10, 0.25, 0.50, 0.75, 0.90]

        yd2 = DoubleVector(len(deltaGrid))  # test y-values 2
        yd3 = DoubleVector(len(deltaGrid))  # test y-values 3

        yd = [
            [11.275, 11.125, 11.250, 11.825, 12.625],
            [16.025, 13.450, 11.350, 10.150, 10.075],
            [10.300, 9.6375, 9.2000, 9.1125, 9.4000]]
        lambdaVec = [0.05, 0.50, 0.75, 1.65, 2.55]

        tolerance = 2.0e-5

        # Check that y-values at knots are exactly the feeded y-values,
        # irrespective of kernel parameters
        for i in lambdaVec:
            myKernel = GaussianKernel(0, i)

            for curri in range(len(yd)):
                f = SafeKernelInterpolation(
                    deltaGrid,
                    yd[curri], myKernel)
                f.update()

                for dIt in range(len(deltaGrid)):
                    expectedVal = yd[curri][dIt]
                    calcVal = f(deltaGrid[dIt])

                    self.assertFalse(abs(expectedVal - calcVal) > tolerance)

        testDeltaGrid = [0.121, 0.279, 0.678, 0.790, 0.980]

        # Gaussian Kernel values for testDeltaGrid with a standard
        # deviation of 2.05 (the value is arbitrary.)  Source: parrallel
        # implementation in R, no literature sources found

        ytd = [
            [11.23847, 11.12003, 11.58932, 11.99168, 13.29650],
            [15.55922, 13.11088, 10.41615, 10.05153, 10.50741],
            [10.17473, 9.557842, 9.09339, 9.149687, 9.779971]]

        myKernel = GaussianKernel(0, 2.05)

        for j in range(len(ytd)):
            currY = yd[j]
            currTY = ytd[j]

            # Build interpolation according to original grid + y-values
            f = SafeKernelInterpolation(
                deltaGrid, currY, myKernel)
            f.update()

            # test values at test Grid
            for dIt in range(len(testDeltaGrid)):
                expectedVal = currTY[dIt]
                f.enableExtrapolation()  # allow extrapolation

                calcVal = f(testDeltaGrid[dIt])
                self.assertFalse(abs(expectedVal - calcVal) > tolerance)

    @unittest.skip('crash randomly')
    def testKernelInterpolation2D(self):
        # No test values known from the literature.
        # Testing for consistency of input output data
        # at the nodes

        TEST_MESSAGE("Testing kernel 2D interpolation...")

        mean = 0.0
        var = 0.18
        myKernel = GaussianKernel(mean, var)

        xVec = Array(10)
        xVec[0] = 0.10
        xVec[1] = 0.20
        xVec[2] = 0.30
        xVec[3] = 0.40
        xVec[4] = 0.50
        xVec[5] = 0.60
        xVec[6] = 0.70
        xVec[7] = 0.80
        xVec[8] = 0.90
        xVec[9] = 1.00

        yVec = Array(3)
        yVec[0] = 1.0
        yVec[1] = 2.0
        yVec[2] = 3.5

        M = Matrix(len(xVec), len(yVec))

        M[0][0] = 0.25
        M[1][0] = 0.24
        M[2][0] = 0.23
        M[3][0] = 0.20
        M[4][0] = 0.19
        M[5][0] = 0.20
        M[6][0] = 0.21
        M[7][0] = 0.22
        M[8][0] = 0.26
        M[9][0] = 0.29

        M[0][1] = 0.27
        M[1][1] = 0.26
        M[2][1] = 0.25
        M[3][1] = 0.22
        M[4][1] = 0.21
        M[5][1] = 0.22
        M[6][1] = 0.23
        M[7][1] = 0.24
        M[8][1] = 0.28
        M[9][1] = 0.31

        M[0][2] = 0.21
        M[1][2] = 0.22
        M[2][2] = 0.27
        M[3][2] = 0.29
        M[4][2] = 0.24
        M[5][2] = 0.28
        M[6][2] = 0.25
        M[7][2] = 0.22
        M[8][2] = 0.29
        M[9][2] = 0.30

        kernel2D = SafeKernelInterpolation2D(
            xVec, yVec, M, myKernel)

        tolerance = 1.0e-10

        for i in range(M.rows()):
            for j in range(M.columns()):
                calcVal = kernel2D(xVec[i], yVec[j])
                expectedVal = M[i][j]

                self.assertFalse(
                    abs(expectedVal - calcVal) > tolerance)

        # alternative data set
        xVec1 = Array(4)
        xVec1[0] = 80.0
        xVec1[1] = 90.0
        xVec1[2] = 100.0
        xVec1[3] = 110.0

        yVec1 = Array(8)
        yVec1[0] = 0.5
        yVec1[1] = 0.7
        yVec1[2] = 1.0
        yVec1[3] = 2.0
        yVec1[4] = 3.5
        yVec1[5] = 4.5
        yVec1[6] = 5.5
        yVec1[7] = 6.5

        M1 = Matrix(len(xVec1), len(yVec1))
        M1[0][0] = 10.25
        M1[1][0] = 12.24
        M1[2][0] = 14.23
        M1[3][0] = 17.20
        M1[0][1] = 12.25
        M1[1][1] = 15.24
        M1[2][1] = 16.23
        M1[3][1] = 16.20
        M1[0][2] = 12.25
        M1[1][2] = 13.24
        M1[2][2] = 13.23
        M1[3][2] = 17.20
        M1[0][3] = 13.25
        M1[1][3] = 15.24
        M1[2][3] = 12.23
        M1[3][3] = 19.20
        M1[0][4] = 14.25
        M1[1][4] = 16.24
        M1[2][4] = 13.23
        M1[3][4] = 12.20
        M1[0][5] = 15.25
        M1[1][5] = 17.24
        M1[2][5] = 14.23
        M1[3][5] = 12.20
        M1[0][6] = 16.25
        M1[1][6] = 13.24
        M1[2][6] = 15.23
        M1[3][6] = 10.20
        M1[0][7] = 14.25
        M1[1][7] = 14.24
        M1[2][7] = 16.23
        M1[3][7] = 19.20

        # test with function pointer
        kernel2DEp = SafeKernelInterpolation2D(
            xVec1,
            yVec1, M1,
            epanechnikovKernel)

        for i in range(M1.rows()):
            for j in range(M1.columns()):
                calcVal = kernel2DEp(xVec1[i], yVec1[j])
                expectedVal = M1[i][j]

                self.assertFalse(abs(expectedVal - calcVal) > tolerance)

        # test updating mechanism by changing initial variables
        xVec1[0] = 60.0
        xVec1[1] = 95.0
        xVec1[2] = 105.0
        xVec1[3] = 135.0

        yVec1[0] = 12.5
        yVec1[1] = 13.7
        yVec1[2] = 15.0
        yVec1[3] = 19.0
        yVec1[4] = 26.5
        yVec1[5] = 27.5
        yVec1[6] = 29.2
        yVec1[7] = 36.5

        kernel2DEp = SafeKernelInterpolation2D(
            xVec1,
            yVec1, M1,
            epanechnikovKernel)
        kernel2DEp.update()

        for i in range(M1.rows()):
            for j in range(M1.columns()):
                calcVal = kernel2DEp(xVec1[i], yVec1[j])
                expectedVal = M1[i][j]

                self.assertFalse(abs(expectedVal - calcVal) > tolerance)

    def testBicubicDerivatives(self):
        TEST_MESSAGE("Testing bicubic spline derivatives...")

        x = Array(100)
        y = Array(100)
        for i in range(100):
            x[i] = y[i] = i / 20.0

        f = Matrix(100, 100)
        for i in range(100):
            for j in range(100):
                f[i][j] = y[i] / 10 * sin(x[j]) + cos(y[i])

        tol = 0.005
        spline = SafeBicubicSpline(x, y, f)

        for i in range(5, 95, 10):
            for j in range(5, 95, 10):
                f_x = spline.derivativeX(x[j], y[i])
                f_xx = spline.secondDerivativeX(x[j], y[i])
                f_y = spline.derivativeY(x[j], y[i])
                f_yy = spline.secondDerivativeY(x[j], y[i])
                f_xy = spline.derivativeXY(x[j], y[i])

                self.assertFalse(abs(f_x - y[i] / 10 * cos(x[j])) > tol)
                self.assertFalse(abs(f_xx + y[i] / 10 * sin(x[j])) > tol)
                self.assertFalse(abs(f_y - (sin(x[j]) / 10 - sin(y[i]))) > tol)
                self.assertFalse(abs(f_yy + cos(y[i])) > tol)
                self.assertFalse(abs(f_xy - cos(x[j]) / 10) > tol)

    def testBicubicUpdate(self):
        TEST_MESSAGE("Testing that bicubic splines actually update...")

        N = 6
        x = Array(N)
        y = Array(N)
        for i in range(N):
            x[i] = y[i] = i * 0.2

        f = Matrix(N, N)
        for i in range(N):
            for j in range(N):
                f[i][j] = x[j] * (x[j] + y[i])

        spline = SafeBicubicSpline(x, y, f)

        old_result = spline(x[2] + 0.1, y[4])

        # modify input matrix and update.
        f[4][3] += 1.0
        spline = SafeBicubicSpline(x, y, f)
        spline.update()

        new_result = spline(x[2] + 0.1, y[4])
        self.assertFalse(abs(old_result - new_result) < 0.5)

    def testUnknownRichardsonExtrapolation(self):
        TEST_MESSAGE("Testing Richardson extrapolation with "
                     "unknown order of convergence...")

        stepSize = 0.01

        testCases = [
            (1.0, 1.0), (1.0, -1.0),
            (2.0, 0.25), (2.0, -1.0),
            (3.0, 2.0), (3.0, -0.5),
            (4.0, 1.0), (4.0, 0.5)]

        for testCase in testCases:
            extrap = RichardsonExtrapolation(
                GF(testCase[0], testCase[1]), stepSize)

            calculated = extrap(4.0, 2.0)
            diff = abs(M_PI - calculated)

            tol = pow(stepSize, testCase[0] + 1)

            self.assertFalse(diff > tol)

        highOrder = RichardsonExtrapolation(GF(14.0, 1.0), 0.5)(4.0, 2.0)
        self.assertFalse(abs(highOrder - M_PI) > 1e-12)

        try:
            RichardsonExtrapolation(GF(16.0, 1.0), 0.5)(4.0, 2.0)
            # BOOST_ERROR("Richardson extrapolation with order of"
            # " convergence above 15 should throw exception")
        except Exception as e:
            print(e)

        limCosValue = RichardsonExtrapolation(limCos, 0.01)(4.0, 2.0)
        self.assertFalse(abs(limCosValue + 1.0) > 1e-6)

    def testRichardsonExtrapolation(self):

        def f(h):
            return pow(1.0 + h, 1 / h)

        TEST_MESSAGE("Testing Richardson extrapolation...")

        # example taken from
        # http:#www.ipvs.uni-stuttgart.de/abteilungen/bv/lehre/
        #      lehrveranstaltungen/vorlesungen/WS0910/
        #      NSG_termine/dateien/Richardson.pdf

        stepSize = 0.1
        orderOfConvergence = 1.0
        extrap = RichardsonExtrapolation(
            f, stepSize, orderOfConvergence)

        tol = 0.00002
        expected = 2.71285

        scalingFactor = 2.0
        calculated = extrap(scalingFactor)

        self.assertFalse(abs(expected - calculated) > tol)

        calculated = extrap()
        self.assertFalse(abs(expected - calculated) > tol)

        expected = 2.721376
        scalingFactor2 = 4.0
        calculated = extrap(scalingFactor2, scalingFactor)

        self.assertFalse(abs(expected - calculated) > tol)

    def testNoArbSabrInterpolation(self):
        TEST_MESSAGE("Testing no-arbitrage Sabr interpolation...")

        # Test SABR function against input volatilities
        # #ifndef __FAST_MATH__
        tolerance = 1.0e-12
        # #else
        #     tolerance = 1.0e-8
        # #endif
        strikes = Array(31)
        volatilities = Array(31)
        volatilities2 = Array(31)
        # input strikes
        strikes[0] = 0.03
        strikes[1] = 0.032
        strikes[2] = 0.034
        strikes[3] = 0.036
        strikes[4] = 0.038
        strikes[5] = 0.04
        strikes[6] = 0.042
        strikes[7] = 0.044
        strikes[8] = 0.046
        strikes[9] = 0.048
        strikes[10] = 0.05
        strikes[11] = 0.052
        strikes[12] = 0.054
        strikes[13] = 0.056
        strikes[14] = 0.058
        strikes[15] = 0.06
        strikes[16] = 0.062
        strikes[17] = 0.064
        strikes[18] = 0.066
        strikes[19] = 0.068
        strikes[20] = 0.07
        strikes[21] = 0.072
        strikes[22] = 0.074
        strikes[23] = 0.076
        strikes[24] = 0.078
        strikes[25] = 0.08
        strikes[26] = 0.082
        strikes[27] = 0.084
        strikes[28] = 0.086
        strikes[29] = 0.088
        strikes[30] = 0.09
        # input volatilities for noarb sabr (other than above
        # alpha is 0.2 here due to the restriction sigmaI <= 1.0 !)
        volatilities[0] = 0.773729077752926
        volatilities[1] = 0.763916242454194
        volatilities[2] = 0.754773878663612
        volatilities[3] = 0.746222305031368
        volatilities[4] = 0.738193023523582
        volatilities[5] = 0.730629785825930
        volatilities[6] = 0.723484825471685
        volatilities[7] = 0.716716812668892
        volatilities[8] = 0.710290301049393
        volatilities[9] = 0.704174528906769
        volatilities[10] = 0.698342635400901
        volatilities[11] = 0.692771033345972
        volatilities[12] = 0.687438902593476
        volatilities[13] = 0.682327777297265
        volatilities[14] = 0.677421206991904
        volatilities[15] = 0.672704476238547
        volatilities[16] = 0.668164371832768
        volatilities[17] = 0.663788984329375
        volatilities[18] = 0.659567547226380
        volatilities[19] = 0.655490294349232
        volatilities[20] = 0.651548341349061
        volatilities[21] = 0.647733583657137
        volatilities[22] = 0.644038608699086
        volatilities[23] = 0.640456620061898
        volatilities[24] = 0.636981371712714
        volatilities[25] = 0.633607110719560
        volatilities[26] = 0.630328527192861
        volatilities[27] = 0.627140710386248
        volatilities[28] = 0.624039110072250
        volatilities[29] = 0.621019502453590
        volatilities[30] = 0.618077959983455

        expiry = 1.0
        forward = 0.039
        # input SABR coefficients (corresponding to the vols above)
        initialAlpha = 0.2
        initialBeta = 0.6
        initialNu = 0.02
        initialRho = 0.01
        # calculate SABR vols and compare with input vols
        noarbSabr = NoArbSabrSmileSection(
            expiry, forward,
            [initialAlpha, initialBeta, initialNu, initialRho])
        for i in range(len(strikes)):
            calculatedVol = noarbSabr.volatility(strikes[i])
            self.assertFalse(
                abs(volatilities[i] - calculatedVol) > tolerance)

        # Test SABR calibration against input parameters
        betaGuess = 0.5
        alphaGuess = 0.2 / pow(forward, betaGuess - 1.0)  # new default value for alpha
        nuGuess = sqrt(0.4)
        rhoGuess = 0.0

        vegaWeighted = [true, false]
        isAlphaFixed = [true, false]
        isBetaFixed = [true, false]
        isNuFixed = [true, false]
        isRhoFixed = [true, false]

        calibrationTolerance = 5.0e-6
        # initialize optimization methods
        methods_ = [
            Simplex(0.01),
            LevenbergMarquardt(1e-8, 1e-8, 1e-8)]
        # Initialize end criteria
        endCriteria = EndCriteria(100000, 100, 1e-8, 1e-8, 1e-8)
        # Test looping over all possibilities
        for j in range(1, len(methods_)):  # j = 1 j < methods_.size() + +j):  # skip simplex (gets caught in some cases)
            for i in vegaWeighted:
                for k_a in isAlphaFixed:
                    for k_b in range(1):  # (k_b = 0 k_b < 1 / * len(isBetaFixed) * / ++k_b):  # keep beta fixed (all 4 params free is a problem for this kind of test)
                        for k_n in isNuFixed:
                            for k_r in isRhoFixed:
                                noarbSabrInterpolation = SafeNoArbSabrInterpolation(
                                    strikes, volatilities, expiry, forward,
                                    # k_a ? initialAlpha: alphaGuess,
                                    initialAlpha if k_a else alphaGuess,
                                    # isBetaFixed[k_b] ? initialBeta: betaGuess,
                                    initialBeta if isBetaFixed[k_b] else betaGuess,
                                    # k_n ? initialNu: nuGuess,
                                    initialNu if k_n else nuGuess,
                                    # k_r ? initialRho: rhoGuess,
                                    initialRho if k_r else rhoGuess,
                                    k_a, isBetaFixed[k_b], k_n, k_r,
                                    i, endCriteria, methods_[j], 1E-10)
                                noarbSabrInterpolation.update()

                                # Recover SABR calibration parameters
                                failed = false
                                calibratedAlpha = noarbSabrInterpolation.alpha()
                                calibratedBeta = noarbSabrInterpolation.beta()
                                calibratedNu = noarbSabrInterpolation.nu()
                                calibratedRho = noarbSabrInterpolation.rho()

                                # compare results: alpha
                                error = abs(initialAlpha - calibratedAlpha)
                                self.assertFalse(error > calibrationTolerance)
                                # Beta
                                error = abs(initialBeta - calibratedBeta)
                                self.assertFalse(error > calibrationTolerance)
                                # Nu
                                error = abs(initialNu - calibratedNu)
                                self.assertFalse(error > calibrationTolerance)
                                # Rho
                                error = abs(initialRho - calibratedRho)
                                self.assertFalse(error > calibrationTolerance)

                                self.assertFalse(failed)

    def testSabrSingleCases(self):
        TEST_MESSAGE("Testing Sabr calibration single cases...")

        # case #1
        # this fails with an exception thrown in 1.4, fixed in 1.5

        strikes = [0.01, 0.01125, 0.0125, 0.01375, 0.0150]
        vols = [0.1667, 0.2020, 0.2785, 0.3279, 0.3727]

        tte = 0.3833
        forward = 0.011025

        s0 = SafeSABRInterpolation(
            strikes, vols, tte, forward,
            NullReal(), 0.25, NullReal(), NullReal(),
            false, true, false, false)
        s0.update()

        self.assertFalse(s0.maxError() > 0.01 or s0.rmsError() > 0.01)

    def testFlochKennedySabrIsSmoothAroundATM(self):
        TEST_MESSAGE("Testing that Andersen SABR formula is smooth "
                     "close to the ATM level...")

        f0 = 1.1
        alpha = 0.35
        nu = 1.1
        rho = 0.25
        beta = 0.3
        strike = f0
        t = 2.1

        vol = sabrFlochKennedyVolatility(
            strike, f0, t, alpha, beta, nu, rho)

        expected = 0.3963883944
        tol = 1e-8
        diff = abs(expected - vol)
        self.assertFalse(diff > tol)

        k = 0.996 * strike
        v = sabrFlochKennedyVolatility(
            k, f0, t, alpha, beta, nu, rho)

        for k in np.arange(0.996 * strike, 1.004 * strike, 0.0001 * strike):
            vt = sabrFlochKennedyVolatility(
                k, f0, t, alpha, beta, nu, rho)

            diff = abs(v - vt)

            self.assertFalse(diff > 1e-5)

            v = vt

    def testLeFlochKennedySabrExample(self):
        TEST_MESSAGE("Testing Le Floc'h Kennedy SABR Example...")

        # Example is taken from F. Le Floc'h, G. Kennedy:
        # Explicit SABR Calibration through Simple Expansions.
        # https:#papers.ssrn.com/sol3/papers.cfm?abstract_id=2467231

        f0 = 1.0
        alpha = 0.35
        nu = 1.0
        rho = 0.25
        beta = 0.25
        strikes = [1.0, 1.5, 0.5]
        t = 2.0

        expected = [0.408702473958, 0.428489933046, 0.585701651161]

        for i in range(len(strikes)):
            strike = strikes[i]
            vol = sabrFlochKennedyVolatility(
                strike, f0, t, alpha, beta, nu, rho)

            tol = 1e-8
            diff = abs(expected[i] - vol)

            self.assertFalse(diff > tol)

    def testTransformations(self):
        def lagrangeTestFct(x):
            return abs(x) + 0.5 * x - x * x

        TEST_MESSAGE("Testing Lagrange interpolation...")

        x = [-1.0, -0.5, -0.25, 0.1, 0.4, 0.75, 0.96]
        y = Array(len(x))

        for i in range(len(x)):
            y[i] = lagrangeTestFct(x[i])

        interpl = SafeLagrangeInterpolation(x, y)

        # reference results are taken from R package pracma
        references = [
            -0.5000000000000000, -0.5392414024347419, -0.5591485962711904,
            -0.5629199661387594, -0.5534414777017116, -0.5333043347921566,
            -0.5048221831582063, -0.4700478608272949, -0.4307896950846587,
            -0.3886273460669714, -0.3449271969711449, -0.3008572908782903,
            -0.2574018141928359, -0.2153751266968088, -0.1754353382192734,
            -0.1380974319209344, -0.1037459341938971, -0.0726471311765894,
            -0.0449608318838433, -0.0207516779521373, 0.0000000000000000,
            0.0173877793964286, 0.0315691961126723, 0.0427562482700356,
            0.0512063534145595, 0.0572137590808174, 0.0611014067405497,
            0.0632132491361394, 0.0639070209989264, 0.0635474631523613,
            0.0625000000000000, 0.0611248703983366, 0.0597717119144768,
            0.0587745984686508, 0.0584475313615655, 0.0590803836865967,
            0.0609352981268212, 0.0642435381368876, 0.0692027925097279,
            0.0759749333281079, 0.0846842273010179, 0.0954160004849021,
            0.1082157563897290, 0.1230887474699003, 0.1400000000000001,
            0.1588747923353829, 0.1795995865576031, 0.2020234135046815,
            0.2259597111862140, 0.2511886165833182, 0.2774597108334206,
            0.3044952177998833, 0.3319936560264689, 0.3596339440766487,
            0.3870799592577457, 0.4139855497299214, 0.4400000000000001,
            0.4647739498001331, 0.4879657663513030, 0.5092483700116673,
            0.5283165133097421, 0.5448945133624253, 0.5587444376778583,
            0.5696747433431296, 0.5775493695968156, 0.5822972837863635,
            0.5839224807103117, 0.5825144353453510, 0.5782590089582251,
            0.5714498086024714, 0.5625000000000000, 0.5519545738075141,
            0.5405030652677689, 0.5289927272456703, 0.5184421566492137,
            0.5100553742352614, 0.5052363578001620, 0.5056040287552059,
            0.5130076920869246]

        tol = 50 * QL_EPSILON
        for i in range(79):
            xx = -1.0 + i * 0.025
            calculated = interpl(xx)
            self.assertFalse(
                isnan(calculated) or abs(references[i] - calculated) > tol)

    def testLagrangeInterpolation(self):
        def lagrangeTestFct(x):
            return abs(x) + 0.5 * x - x * x

        TEST_MESSAGE("Testing Lagrange interpolation...")

        x = [-1.0, -0.5, -0.25, 0.1, 0.4, 0.75, 0.96]
        y = Array(len(x))
        # transform(x, y, & lagrangeTestFct)
        for i in range(len(x)):
            y[i] = lagrangeTestFct(x[i])

        interpl = SafeLagrangeInterpolation(x, y)

        # reference results are taken from R package pracma
        references = [
            -0.5000000000000000, -0.5392414024347419, -0.5591485962711904,
            -0.5629199661387594, -0.5534414777017116, -0.5333043347921566,
            -0.5048221831582063, -0.4700478608272949, -0.4307896950846587,
            -0.3886273460669714, -0.3449271969711449, -0.3008572908782903,
            -0.2574018141928359, -0.2153751266968088, -0.1754353382192734,
            -0.1380974319209344, -0.1037459341938971, -0.0726471311765894,
            -0.0449608318838433, -0.0207516779521373, 0.0000000000000000,
            0.0173877793964286, 0.0315691961126723, 0.0427562482700356,
            0.0512063534145595, 0.0572137590808174, 0.0611014067405497,
            0.0632132491361394, 0.0639070209989264, 0.0635474631523613,
            0.0625000000000000, 0.0611248703983366, 0.0597717119144768,
            0.0587745984686508, 0.0584475313615655, 0.0590803836865967,
            0.0609352981268212, 0.0642435381368876, 0.0692027925097279,
            0.0759749333281079, 0.0846842273010179, 0.0954160004849021,
            0.1082157563897290, 0.1230887474699003, 0.1400000000000001,
            0.1588747923353829, 0.1795995865576031, 0.2020234135046815,
            0.2259597111862140, 0.2511886165833182, 0.2774597108334206,
            0.3044952177998833, 0.3319936560264689, 0.3596339440766487,
            0.3870799592577457, 0.4139855497299214, 0.4400000000000001,
            0.4647739498001331, 0.4879657663513030, 0.5092483700116673,
            0.5283165133097421, 0.5448945133624253, 0.5587444376778583,
            0.5696747433431296, 0.5775493695968156, 0.5822972837863635,
            0.5839224807103117, 0.5825144353453510, 0.5782590089582251,
            0.5714498086024714, 0.5625000000000000, 0.5519545738075141,
            0.5405030652677689, 0.5289927272456703, 0.5184421566492137,
            0.5100553742352614, 0.5052363578001620, 0.5056040287552059,
            0.5130076920869246]

        tol = 50 * QL_EPSILON
        for i in range(79):
            xx = -1.0 + i * 0.025
            calculated = interpl(xx)
            self.assertFalse(
                isnan(calculated) or abs(references[i] - calculated) > tol)

    def testLagrangeInterpolationAtSupportPoint(self):
        TEST_MESSAGE(
            "Testing Lagrange interpolation at supporting points...")

        n = 5
        x = Array(n)
        y = Array(n)
        for i in range(n):
            x[i] = i / n
            y[i] = 1.0 / (1.0 - x[i])

        interpl = SafeLagrangeInterpolation(x, y)

        relTol = 5e-12

        for i in range(1, n - 1):
            for z in np.arange(
                    x[i] - 100 * QL_EPSILON,
                    x[i] + 100 * QL_EPSILON,
                    2 * QL_EPSILON):
                expected = 1.0 / (1.0 - x[i])
                calculated = interpl(z)

                self.assertFalse(
                    isnan(calculated) or abs(expected - calculated) > relTol)

    def testLagrangeInterpolationDerivative(self):
        TEST_MESSAGE(
            "Testing Lagrange interpolation derivatives...")

        x = Array(5)
        y = Array(5)
        x[0] = -1.0
        y[0] = 2.0
        x[1] = -0.3
        y[1] = 3.0
        x[2] = 0.1
        y[2] = 6.0
        x[3] = 0.3
        y[3] = 3.0
        x[4] = 0.9
        y[4] = -1.0

        interpl = SafeLagrangeInterpolation(x, y)

        eps = sqrt(QL_EPSILON)
        for i in np.arange(-1.0, 0.9 + 0.01, 0.01):  # i in np.arange(-1.0, 0.9 + 0.01, 0.01):
            calculated = interpl.derivative(i, true)
            expected = \
                (interpl(i + eps, true) - interpl(i - eps, true)) / (2 * eps)
            # fail, when i = 0.1
            if abs(i - 0.1) > 0.01 / 2:
                self.assertFalse(
                    isnan(calculated) or abs(expected - calculated) > 25 * eps)

    def testLagrangeInterpolationOnChebyshevPoints(self):
        TEST_MESSAGE(
            "Testing Lagrange interpolation on Chebyshev points...")

        # Test example taken from
        # J.P. Berrut, L.N. Trefethen, Barycentric Lagrange Interpolation
        # https:#people.maths.ox.ac.uk/trefethen/barycentric.pdf

        n = 50
        x = Array(n + 1)
        y = Array(n + 1)
        for i in range(n + 1):
            # Chebyshev points
            x[i] = cos((2 * i + 1) * M_PI / (2 * n + 2))
            y[i] = exp(x[i]) / cos(x[i])

        interpl = SafeLagrangeInterpolation(x, y)

        tol = 1e-6  # 1e-13
        tolDeriv = 1e-5  # 1e-11

        for x in np.arange(-1.0, 1.0 + 0.03, 0.03):
            calculated = interpl(x, true)
            expected = exp(x) / cos(x)

            diff = abs(expected - calculated)
            self.assertFalse(isnan(calculated) or diff > tol)

            calculatedDeriv = interpl.derivative(x, true)
            expectedDeriv = exp(x) * (cos(x) + sin(x)) / (cos(x) ** 2)

            diffDeriv = abs(expectedDeriv - calculatedDeriv)
            self.assertFalse(isnan(calculated) or diffDeriv > tolDeriv)

    def testBSplines(self):
        TEST_MESSAGE("Testing B-Splines...")

        # reference values have been generate with the R package splines2
        # https:#cran.r-project.org/web/packages/splines2/splines2.pdf

        knots = [-1.0, 0.5, 0.75, 1.2, 3.0, 4.0, 5.0]

        p = 2
        bspline = BSpline(p, len(knots) - p - 2, knots)

        referenceValues = [
            (0, -0.95, 9.5238095238e-04),
            (0, -0.01, 0.37337142857),
            (0, 0.49, 0.84575238095),
            (0, 1.21, 0.0),
            (1, 1.49, 0.562987654321),
            (1, 1.59, 0.490888888889),
            (2, 1.99, 0.62429409171),
            (3, 1.19, 0.0),
            (3, 1.99, 0.12382936508),
            (3, 3.59, 0.765914285714)]

        tol = 1e-10
        for referenceValue in referenceValues:
            idx = referenceValue[0]
            x = referenceValue[1]
            expected = referenceValue[2]

            calculated = bspline(idx, x)

            self.assertFalse(
                isnan(calculated) or abs(calculated - expected) > tol)

    @unittest.skip('fails on ubuntu')
    def testBackwardFlatOnSinglePoint(self):
        TEST_MESSAGE("Testing piecewise constant interpolation on a single point...")
        knots = Array(1, 1.0)
        values = Array(1, 2.5)

        impl = SafeBackwardFlat().interpolate(knots, values)
        # impl = SafeBackwardFlatInterpolation(knots, values)

        x = [-1.0, 1.0, 2.0, 3.0]

        for i in x:
            calculated = impl(i, True)
            expected = values[0]

            self.assertFalse(
                not close_enough(calculated, expected))

            expectedPrimitive = values[0] * (i - knots[0])
            calculatedPrimitive = impl.primitive(i, true)

            self.assertFalse(
                not close_enough(
                    calculatedPrimitive, expectedPrimitive))

    def _checkValues(self,
                     type,
                     cubic,
                     x, y):
        tolerance = 2.0e-15
        for i in range(len(x)):
            interpolated = cubic(x[i])
            self.assertFalse(abs(interpolated - y[i]) > tolerance)

    def _check1stDerivativeValue(self,
                                 type,
                                 cubic,
                                 x,
                                 value):
        tolerance = 1.0e-14
        interpolated = cubic.derivative(x)
        error = abs(interpolated - value)
        self.assertFalse(error > tolerance)

    def _check2ndDerivativeValue(self,
                                 type,
                                 cubic,
                                 x,
                                 value):
        tolerance = 1.0e-13
        interpolated = cubic.secondDerivative(x)
        error = abs(interpolated - value)
        self.assertFalse(error > tolerance)

    def _checkNotAKnotCondition(self,
                                type,
                                cubic):
        tolerance = 1.0e-14
        c = cubic.cCoefficients()
        self.assertFalse(abs(c[0] - c[1]) > tolerance)
        n = len(c)
        self.assertFalse(abs(c[n - 2] - c[n - 1]) > tolerance)

    def _checkSymmetry(self,
                       type,
                       cubic,
                       xMin):
        tolerance = 1.0e-15
        for x in np.arange(xMin, 0.0, 0.1):  # (x = xMin x < 0.0 x += 0.1):
            y1 = cubic(x)
            y2 = cubic(-x)
            self.assertFalse(abs(y1 - y2) > tolerance)
