import unittest

from QuantLib import *

from utilities import *


class VarianceOptionTest(unittest.TestCase):

    def testIntegralHeston(self):
        TEST_MESSAGE(
            "Testing variance option with integral Heston engine...")

        dc = Actual360()
        today = Settings.instance().evaluationDate

        s0 = QuoteHandle(SimpleQuote(1.0))
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle()
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))

        v0 = 2.0
        kappa = 2.0
        theta = 0.01
        sigma = 0.1
        rho = -0.5

        process = HestonProcess(rTS, qTS, s0, v0, kappa, theta, sigma, rho)
        engine = IntegralHestonVarianceOptionEngine(process)

        strike = 0.05
        nominal = 1.0
        T = 1.5
        exDate = today + int(360 * T)

        payoff = PlainVanillaPayoff(Option.Call, strike)

        varianceOption1 = VarianceOption(payoff, nominal, today, exDate)
        varianceOption1.setPricingEngine(engine)

        calculated = varianceOption1.NPV()
        expected = 0.9104619
        error = abs(calculated - expected)
        self.assertFalse(error > 1.0e-7)

        v0 = 1.5
        kappa = 2.0
        theta = 0.01
        sigma = 0.1
        rho = -0.5

        process = HestonProcess(
            rTS, qTS, s0, v0, kappa, theta, sigma, rho)
        engine = IntegralHestonVarianceOptionEngine(process)

        strike = 0.7
        nominal = 1.0
        T = 1.0
        exDate = today + int(360 * T)

        payoff = PlainVanillaPayoff(Option.Put, strike)

        varianceOption2 = VarianceOption(payoff, nominal, today, exDate)
        varianceOption2.setPricingEngine(engine)

        calculated = varianceOption2.NPV()
        expected = 0.0466796
        error = abs(calculated - expected)
        self.assertFalse(error > 1.0e-7)
