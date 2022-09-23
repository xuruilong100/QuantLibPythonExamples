import unittest

from QuantLib import *

from utilities import *


class NoArbSabrTest(unittest.TestCase):

    def testAbsorptionMatrix(self):
        TEST_MESSAGE(
            "Testing no-arbitrage Sabr absorption matrix...")

        self.checkD0(1, 0.01, 0.75, 0.1, 0.25, 60342)
        self.checkD0(0.8, 0.01, 0.75, 0.1, 0.25, 12148)
        self.checkD0(0.05, 0.01, 0.75, 0.1, 0.25, 0)
        self.checkD0(1, 0.01, 0.75, 0.1, 10.0, 1890509)
        self.checkD0(0.8, 0.01, 0.75, 0.1, 10.0, 1740233)
        self.checkD0(0.05, 0.01, 0.75, 0.1, 10.0, 0)
        self.checkD0(1, 0.01, 0.75, 0.1, 30.0, 2174176)
        self.checkD0(0.8, 0.01, 0.75, 0.1, 30.0, 2090672)
        self.checkD0(0.05, 0.01, 0.75, 0.1, 30.0, 31)
        self.checkD0(0.35, 0.10, -0.75, 0.1, 0.25, 0)
        self.checkD0(0.35, 0.10, -0.75, 0.1, 14.75, 1087841)
        self.checkD0(0.35, 0.10, -0.75, 0.1, 30.0, 1406569)
        self.checkD0(0.24, 0.90, 0.50, 0.8, 1.25, 27)
        self.checkD0(0.24, 0.90, 0.50, 0.8, 25.75, 167541)
        self.checkD0(0.05, 0.90, -0.75, 0.8, 2.0, 17)
        self.checkD0(0.05, 0.90, -0.75, 0.8, 30.0, 42100)

    def testConsistencyWithHagan(self):
        TEST_MESSAGE(
            "Testing consistency of noarb-sabr with Hagan et al (2002)")

        tau = 1.0
        beta = 0.5
        alpha = 0.026
        rho = -0.1
        nu = 0.4
        f = 0.0488

        sabr = SabrSmileSection(tau, f, [alpha, beta, nu, rho])
        noarbsabr = NoArbSabrSmileSection(tau, f, [alpha, beta, nu, rho])

        absProb = noarbsabr.model().absorptionProbability()
        self.assertFalse(absProb > 1E-10 or absProb < 0.0)

        strike = 0.0001
        while strike < 0.15:
            sabrPrice = sabr.optionPrice(strike)
            noarbsabrPrice = noarbsabr.optionPrice(strike)
            self.assertFalse(abs(sabrPrice - noarbsabrPrice) > 1e-5)

            sabrDigital = sabr.digitalOptionPrice(strike)
            noarbsabrDigital = noarbsabr.digitalOptionPrice(strike)
            self.assertFalse(abs(sabrDigital - noarbsabrDigital) > 1e-3)

            sabrDensity = sabr.density(strike)
            noarbsabrDensity = noarbsabr.density(strike)
            self.assertFalse(abs(sabrDensity - noarbsabrDensity) > 1e-0)
            strike += 0.0001

    def checkD0(self, sigmaI, beta, rho, nu,
                tau, absorptions):
        forward = 0.03
        alpha = sigmaI / pow(forward, beta - 1.0)

        d = D0Interpolator(forward, tau, alpha, beta, nu, rho)

        self.assertFalse(
            abs(d() * 2500000.0 - absorptions) > 0.1)
