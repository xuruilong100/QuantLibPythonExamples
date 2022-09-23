import unittest

from QuantLib import *

from utilities import *


class Case(object):
    def __init__(self,
                 F1,
                 F2,
                 X,
                 r,
                 sigma1,
                 sigma2,
                 rho,
                 length,
                 value,
                 theta):
        self.F1 = F1
        self.F2 = F2
        self.X = X
        self.r = r
        self.sigma1 = sigma1
        self.sigma2 = sigma2
        self.rho = rho
        self.length = length
        self.value = value
        self.theta = theta


class SpreadOptionTest(unittest.TestCase):

    def testKirkEngine(self):
        TEST_MESSAGE(
            "Testing Kirk approximation for spread options...")

        cases = [
            Case(28.0, 20.0, 7.0, 0.05, 0.29, 0.36, 0.42, 90, 2.1670, -3.0431),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.20, -0.5, 36, 4.7530, -25.5905),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.20, 0.0, 36, 3.7970, -20.8841),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.20, 0.5, 36, 2.5537, -14.7260),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.20, -0.5, 180, 10.7517, -10.0847),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.20, 0.0, 180, 8.7020, -8.2619),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.20, 0.5, 180, 6.0257, -5.8661),
            Case(122.0, 120.0, 3.0, 0.10, 0.25, 0.20, -0.5, 36, 5.4275, -28.9013),
            Case(122.0, 120.0, 3.0, 0.10, 0.25, 0.20, 0.0, 36, 4.3712, -23.7133),
            Case(122.0, 120.0, 3.0, 0.10, 0.25, 0.20, 0.5, 36, 3.0086, -16.9864),
            Case(122.0, 120.0, 3.0, 0.10, 0.25, 0.20, -0.5, 180, 12.1941, -11.3603),
            Case(122.0, 120.0, 3.0, 0.10, 0.25, 0.20, 0.0, 180, 9.9340, -9.3589),
            Case(122.0, 120.0, 3.0, 0.10, 0.25, 0.20, 0.5, 180, 7.0067, -6.7463),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.25, -0.5, 36, 5.4061, -28.7963),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.25, 0.0, 36, 4.3451, -23.5848),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.25, 0.5, 36, 2.9723, -16.8060),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.25, -0.5, 180, 12.1483, -11.3200),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.25, 0.0, 180, 9.8780, -9.3091),
            Case(122.0, 120.0, 3.0, 0.10, 0.20, 0.25, 0.5, 180, 6.9284, -6.6761)]

        for i in cases:
            dc = Actual360()
            today = knownGoodDefault
            exerciseDate = today + i.length

            F1 = SimpleQuote(i.F1)
            F2 = SimpleQuote(i.F2)

            riskFreeRate = i.r
            forwardRate = flatRate(today, riskFreeRate, dc)

            rho = SimpleQuote(i.rho)

            vol1 = i.sigma1
            vol2 = i.sigma2
            volTS1 = flatVol(today, vol1, dc)
            volTS2 = flatVol(today, vol2, dc)

            stochProcess1 = BlackProcess(
                QuoteHandle(F1),
                YieldTermStructureHandle(forwardRate),
                BlackVolTermStructureHandle(volTS1))

            stochProcess2 = BlackProcess(
                QuoteHandle(F2),
                YieldTermStructureHandle(forwardRate),
                BlackVolTermStructureHandle(volTS2))

            engine = KirkSpreadOptionEngine(
                stochProcess1, stochProcess2, QuoteHandle(rho))

            typeOpt = Option.Call
            strike = i.X
            payoff = PlainVanillaPayoff(typeOpt, strike)
            exercise = EuropeanExercise(exerciseDate)

            option = SpreadOption(payoff, exercise)
            option.setPricingEngine(engine)

            value = option.NPV()
            theta = option.theta()
            tolerance = 1e-4

            self.assertFalse(abs(value - i.value) > tolerance)
            self.assertFalse(abs(theta - i.theta) > tolerance)
