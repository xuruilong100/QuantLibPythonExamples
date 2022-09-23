import unittest
from math import exp, cosh, sin, cos

from QuantLib import *
from scipy.stats import ncx2

from utilities import *


def inv_exp(x):
    return exp(-x)


def x_inv_exp(x):
    return x * exp(-x)


def x_normaldistribution(x):
    return x * NormalDistribution()(x)


def x_x_normaldistribution(x):
    return x * x * NormalDistribution()(x)


def inv_cosh(x):
    return 1 / cosh(x)


def x_inv_cosh(x):
    return x / cosh(x)


def x_x_nonCentralChiSquared(x):
    return x * x * ncx2(4.0, 1.0).pdf(x)


def x_sin_exp_nonCentralChiSquared(x):
    return x * sin(0.1 * x) * exp(0.3 * x) * ncx2(1.0, 1.0).pdf(x)


class GaussianQuadraturesTest(unittest.TestCase):

    def testJacobi(self):
        TEST_MESSAGE(
            "Testing Gauss-Jacobi integration...")

        self._testSingleJacobi(GaussLegendreIntegration(16))
        self._testSingleJacobi(GaussChebyshevIntegration(130))
        self._testSingleJacobi(GaussChebyshev2ndIntegration(130))
        self._testSingleJacobi(GaussGegenbauerIntegration(50, 0.55))

    def testLaguerre(self):
        TEST_MESSAGE(
            "Testing Gauss-Laguerre integration...")

        self._testSingleLaguerre(GaussLaguerreIntegration(16))
        self._testSingleLaguerre(GaussLaguerreIntegration(150, 0.01))
        self._testSingle(GaussLaguerreIntegration(16, 1.0), "f(x) = x*exp(-x)", x_inv_exp, 1.0)
        self._testSingle(GaussLaguerreIntegration(32, 0.9), "f(x) = x*exp(-x)", x_inv_exp, 1.0)

    def testHermite(self):
        TEST_MESSAGE(
            "Testing Gauss-Hermite integration...")

        self._testSingle(GaussHermiteIntegration(16), "f(x) = Gaussian(x)", NormalDistribution(), 1.0)
        self._testSingle(GaussHermiteIntegration(16, 0.5), "f(x) = x*Gaussian(x)", x_normaldistribution, 0.0)
        self._testSingle(GaussHermiteIntegration(64, 0.9), "f(x) = x*x*Gaussian(x)", x_x_normaldistribution, 1.0)

    def testHyperbolic(self):
        TEST_MESSAGE(
            "Testing Gauss hyperbolic integration...")

        self._testSingle(GaussHyperbolicIntegration(16), "f(x) = 1/cosh(x)", inv_cosh, M_PI)
        self._testSingle(GaussHyperbolicIntegration(16), "f(x) = x/cosh(x)", x_inv_cosh, 0.0)

    def testTabulated(self):
        TEST_MESSAGE(
            "Testing tabulated Gauss-Laguerre integration...")

        self._testSingleTabulated(lambda x: 1.0, "f(x) = 1", 2.0, 1.0e-13)
        self._testSingleTabulated(lambda x: x, "f(x) = x", 0.0, 1.0e-13)
        self._testSingleTabulated(lambda x: x * x, "f(x) = x^2", (2.0 / 3.0), 1.0e-13)
        self._testSingleTabulated(lambda x: x * x * x, "f(x) = x^3", 0.0, 1.0e-13)
        self._testSingleTabulated(lambda x: x * x * x * x, "f(x) = x^4", (2.0 / 5.0), 1.0e-13)

    def testNonCentralChiSquared(self):
        TEST_MESSAGE(
            "Testing Gauss non-central chi-squared integration...")

        self._testSingle(
            GaussianQuadrature(2, GaussNonCentralChiSquaredPolynomial(4.0, 1.0)),
            "f(x) = x^2 * nonCentralChiSquared(4, 1)(x)",
            x_x_nonCentralChiSquared, 37.0)
        self._testSingle(
            GaussianQuadrature(14, GaussNonCentralChiSquaredPolynomial(1.0, 1.0)),
            "f(x) = x * sin(0.1*x)*exp(0.3*x)*nonCentralChiSquared(1, 1)(x)",
            x_sin_exp_nonCentralChiSquared, 17.408092)

    def testNonCentralChiSquaredSumOfNodes(self):
        TEST_MESSAGE(
            "Testing Gauss non-central chi-squared sum of nodes...")

        expected = [
            47.53491786730293,
            70.6103295419633383,
            98.0593406849441607,
            129.853401537905341,
            165.96963582663912,
            206.389183233992043]

        nu = 4.0
        lmd = 1.0
        orthPoly = GaussNonCentralChiSquaredPolynomial(nu, lmd)

        tol = 1e-5

        for n in range(4, 10):
            g = GaussianQuadrature(n, orthPoly)
            x = g.x()

            calculated = 0.0
            for i in x:
                calculated += i

            self.assertFalse(abs(calculated - expected[n - 4]) > tol)

    @unittest.skip("testMomentBasedGaussianPolynomial")
    def testMomentBasedGaussianPolynomial(self):
        TEST_MESSAGE(
            "Testing moment-based Gaussian polynomials...")

    @unittest.skip("testGaussLaguerreCosinePolynomial")
    def testGaussLaguerreCosinePolynomial(self):
        TEST_MESSAGE(
            "Testing Gauss-Laguerre-Cosine quadrature...")

        quadCosine = GaussianQuadrature(16, GaussLaguerreCosineRealPolynomial(0.2))

        self._testSingle(quadCosine, "f(x) = exp(-x)", inv_exp, 1.0)
        self._testSingle(quadCosine, "f(x) = x*exp(-x)", x_inv_exp, 1.0)

        quadSine = GaussianQuadrature(16, GaussLaguerreSineRealPolynomial(0.2))

        self._testSingle(quadSine, "f(x) = exp(-x)", inv_exp, 1.0)
        self._testSingle(quadSine, "f(x) = x*exp(-x)", x_inv_exp, 1.0)

    def _testSingle(self,
                    I,
                    tag,
                    f,
                    expected):
        calculated = I(f)
        self.assertFalse(abs(calculated - expected) > 1.0e-4)

    def _testSingleJacobi(self, I):
        self._testSingle(
            I, "f(x) = 1", lambda x: 1.0, 2.0)
        self._testSingle(I, "f(x) = x", lambda x: x, 0.0)
        self._testSingle(I, "f(x) = x^2", lambda x: x * x, 2 / 3.)
        self._testSingle(I, "f(x) = sin(x)", lambda x: sin(x), 0.0)
        self._testSingle(I, "f(x) = cos(x)", lambda x: cos(x), sin(1.0) - sin(-1.0))
        self._testSingle(
            I, "f(x) = Gaussian(x)",
            NormalDistribution(),
            CumulativeNormalDistribution()(1.0) - CumulativeNormalDistribution()(-1.0))

    def _testSingleLaguerre(self, I):
        self._testSingle(I, "f(x) = exp(-x)", inv_exp, 1.0)
        self._testSingle(I, "f(x) = x*exp(-x)", x_inv_exp, 1.0)
        self._testSingle(I, "f(x) = Gaussian(x)", NormalDistribution(), 0.5)

    def _testSingleTabulated(self,
                             f,
                             tag,
                             expected,
                             tolerance):
        order = [6, 7, 12, 20]
        quad = TabulatedGaussLegendre()
        for i in order:
            quad.order(i)
            realised = quad(f)
            self.assertFalse(abs(realised - expected) > tolerance)
