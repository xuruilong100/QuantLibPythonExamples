import unittest
from utilities import *
from QuantLib import *
from math import log, sin
from numpy import exp


class FunctionsTest(unittest.TestCase):
    def testFactorial(self):
        TEST_MESSAGE("Testing factorial numbers...")

        expected = 1.0
        calculated = Factorial.get(0)
        self.assertFalse(calculated != expected)

        for i in range(1, 171):
            expected *= i
            calculated = Factorial.get(i)
            self.assertFalse(abs(calculated - expected) / expected > 1.0e-9)

    def testGammaFunction(self):
        TEST_MESSAGE("Testing Gamma function...")

        expected = 0.0
        calculated = GammaFunction().logValue(1)
        self.assertFalse(abs(calculated) > 1.0e-15)

        for i in range(2, 9000):
            expected += log(i)
            calculated = GammaFunction().logValue(float(i + 1))
            self.assertFalse(abs(calculated - expected) / expected > 1.0e-9)

    def testGammaValues(self):
        TEST_MESSAGE("Testing Gamma values...")

        # reference results are calculated with R
        tasks = [
            [0.0001, 9999.422883231624, 1e3],
            [1.2, 0.9181687423997607, 1e3],
            [7.3, 1271.4236336639089586, 1e3],
            [-1.1, 9.7148063829028946, 1e3],
            [-4.001, -41.6040228304425312, 1e3],
            [-4.999, -8.347576090315059, 1e3],
            [-19.000001, 8.220610833201313e-12, 1e8],
            [-19.5, 5.811045977502255e-18, 1e3],
            [-21.000001, 1.957288098276488e-14, 1e8],
            [-21.5, 1.318444918321553e-20, 1e6]]

        for task in tasks:
            x = task[0]
            expected = task[1]
            calculated = GammaFunction().value(x)
            tol = task[2] * QL_EPSILON * abs(expected)

            self.assertFalse(abs(calculated - expected) > tol)

    def testModifiedBesselFunctions(self):
        TEST_MESSAGE("Testing modified Bessel function of first and second kind...")

        # reference values are computed with R and the additional package Bessel
        # http://cran.r-project.org/web/packages/Bessel

        r = [
            [-1.3, 2.0, 1.2079888436539505, 0.1608243636110430],
            [1.3, 2.0, 1.2908192151358788, 0.1608243636110430],
            [0.001, 2.0, 2.2794705965773794, 0.1138938963603362],
            [1.2, 0.5, 0.1768918783499572, 2.1086579232338192],
            [2.3, 0.1, 0.00037954958988425198, 572.096866928290183],
            [-2.3, 1.1, 1.07222017902746969, 1.88152553684107371],
            [-10.0001, 1.1, 13857.7715614282552, 69288858.9474423379]]

        for i in r:
            nu = i[0]
            x = i[1]
            expected_i = i[2]
            expected_k = i[3]
            tol_i = 5e4 * QL_EPSILON * abs(expected_i)
            tol_k = 5e4 * QL_EPSILON * abs(expected_k)

            calculated_i = modifiedBesselFunction_i(nu, x)
            calculated_k = modifiedBesselFunction_k(nu, x)

            self.assertFalse(abs(expected_i - calculated_i) > tol_i)
            self.assertFalse(abs(expected_k - calculated_k) > tol_k)

        c = [
            [-1.3, 2.0, 0.0, 1.2079888436539505, 0.0, 0.1608243636110430, 0.0],
            [1.2, 1.5, 0.3, 0.7891550871263575, 0.2721408731632123, 0.275126507673411, -0.1316314405663727],
            [1.2, -1.5, 0.0, -0.6650597524355781, -0.4831941938091643, -0.251112360556051, -2.400130904230102],
            [-11.2, 1.5, 0.3, 12780719.20252659, 16401053.26770633, -34155172.65672453, -43830147.36759921],
            [1.2, -1.5, 2.0, -0.3869803778520574, 0.9756701796853728, -3.111629716783005, 0.6307859871879062],
            [1.2, 0.0, 9.9999, -0.03507838078252647, 0.1079601550451466, -0.05979939995451453, 0.3929814473878203],
            [1.2, 0.0, 10.1, -0.02782046891519293, 0.08562259917678558, -0.02035685034691133, 0.3949834389686676],
            [1.2, 0.0, 12.1, 0.07092110620741207, -0.2182727210128104, 0.3368505862966958, -0.1299038064313366],
            [1.2, 0.0, 14.1, -0.03014378676768797, 0.09277303628303372, -0.237531022649052, -0.2351923034581644],
            [1.2, 0.0, 16.1, -0.03823210284792657, 0.1176663135266562, -0.1091239402448228, 0.2930535651966139],
            [1.2, 0.0, 18.1, 0.05626742394733754, -0.173173324361983, 0.2941636588154642, -0.02023355577954348],
            [1.2, 0.0, 180.1, -0.001230682086826484, 0.003787649998122361, 0.02284509628723454, 0.09055419580980778],
            [1.2, 0.0, 21.0, -0.04746415965014021, 0.1460796627610969, -0.2693825171336859, -0.04830804448126782],
            [1.2, 10.0, 0.0, 2609.784936867044, 0, 1.904394919838336e-05, 0],
            [1.2, 14.0, 0.0, 122690.4873454286, 0, 2.902060692576643e-07, 0],
            [1.2, 20.0, 10.0, -37452017.91168936, -13917587.22151363, -3.821534367487143e-10, 4.083211255351664e-10],
            [1.2, 9.0, 9.0, -621.7335051293694, 618.1455736670332, -4.480795479964915e-05, -3.489034389148745e-08]]

        for i in c:
            nu = i[0]
            z = complex(i[1], i[2])
            expected_i = complex(i[3], i[4])
            expected_k = complex(i[5], i[6])

            tol_i = 5e4 * QL_EPSILON * abs(expected_i)
            tol_k = 1e6 * QL_EPSILON * abs(expected_k)

            calculated_i = modifiedBesselFunction_i(nu, z)
            calculated_k = modifiedBesselFunction_k(nu, z)

            self.assertFalse(abs(expected_i - calculated_i) > tol_i)
            self.assertFalse(
                abs(expected_k) > 1e-4  # do not check small values
                and abs(expected_k - calculated_k) > tol_k)

    def testWeightedModifiedBesselFunctions(self):
        TEST_MESSAGE("Testing weighted modified Bessel functions...")
        nu = -5.0
        while nu <= 5.0:
            x = 0.1
            while x <= 15.0:
                calculated_i = modifiedBesselFunction_i_exponentiallyWeighted(nu, x)
                expected_i = modifiedBesselFunction_i(nu, x) * exp(-x)
                calculated_k = modifiedBesselFunction_k_exponentiallyWeighted(nu, x)
                expected_k = M_PI_2 * (
                        modifiedBesselFunction_i(-nu, x) -
                        modifiedBesselFunction_i(nu, x)) * exp(-x) / sin(M_PI * nu)

                tol_i = 1e3 * QL_EPSILON * abs(expected_i) * max(exp(x), 1.0)
                tol_k = max(
                    QL_EPSILON,
                    1e3 * QL_EPSILON * abs(expected_k) * max(exp(x), 1.0))

                self.assertFalse(abs(expected_i - calculated_i) > tol_i)
                self.assertFalse(abs(expected_k - calculated_k) > tol_k)
                x += 0.5
            nu += 0.5

        nu = -5.1
        while nu <= 5.0:
            x = -5.0
            while x <= 5.0:
                y = -5.0
                while y <= 5.0:
                    z = complex(x, y)
                    calculated_i = modifiedBesselFunction_i_exponentiallyWeighted(nu, z)
                    expected_i = modifiedBesselFunction_i(nu, z) * exp(-z)
                    calculated_k = modifiedBesselFunction_k_exponentiallyWeighted(nu, z)
                    expected_k = M_PI_2 * (
                            modifiedBesselFunction_i(-nu, z) * exp(-z) -
                            modifiedBesselFunction_i(nu, z) * exp(-z)) / sin(M_PI * nu)
                    tol_i = 1e5 * QL_EPSILON * abs(calculated_i)
                    tol_k = 1e5 * QL_EPSILON * abs(calculated_k)
                    self.assertFalse(abs(calculated_i - expected_i) > tol_i)
                    self.assertFalse(abs(calculated_k - expected_k) > tol_k)
                    y += 0.5
                x += 0.5
            nu += 0.5
