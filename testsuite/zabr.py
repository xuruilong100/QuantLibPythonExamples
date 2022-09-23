import unittest

from QuantLib import *

from utilities import *


class ZabrTest(unittest.TestCase):

    def testConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of ZABR...")
        tol = 1E-4

        alpha = 0.08
        beta = 0.70
        nu = 0.20
        rho = -0.30
        tau = 5.0
        forward = 0.03

        sabr = SabrSmileSection(tau, forward, [alpha, beta, nu, rho])

        zabr0 = ZabrShortMaturityLognormalSmileSection(
            tau, forward, [alpha, beta, nu, rho, 1.0])

        zabr1 = ZabrShortMaturityNormalSmileSection(
            tau, forward, [alpha, beta, nu, rho, 1.0])

        zabr2 = ZabrLocalVolatilitySmileSection(
            tau, forward, [alpha, beta, nu, rho, 1.0])

        zabr3 = ZabrFullFdSmileSection(
            tau, forward, [alpha, beta, nu, rho, 1.0], DoubleVector(), 2)

        k = 0.0001
        while k <= 0.70:
            c0 = sabr.optionPrice(k)
            z0 = zabr0.optionPrice(k)
            z1 = zabr1.optionPrice(k)
            z2 = zabr2.optionPrice(k)
            z3 = zabr3.optionPrice(k)
            self.assertFalse(abs(z0 - c0) > tol)
            self.assertFalse(abs(z1 - c0) > tol)
            self.assertFalse(abs(z2 - c0) > tol)
            self.assertFalse(abs(z3 - c0) > tol)
            k += 0.0001
