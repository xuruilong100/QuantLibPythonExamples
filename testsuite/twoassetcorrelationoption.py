import unittest

from QuantLib import *

from utilities import *


class TwoAssetCorrelationOptionTest(unittest.TestCase):

    def testAnalyticEngine(self):
        TEST_MESSAGE(
            "Testing analytic engine for two-asset correlation option...")

        today = Settings.instance().evaluationDate
        dc = Actual360()

        typeOpt = Option.Call
        strike1 = 50.0
        strike2 = 70.0
        exDate = today + 180

        exercise = EuropeanExercise(exDate)

        option = TwoAssetCorrelationOption(typeOpt, strike1, strike2, exercise)

        underlying1 = QuoteHandle(SimpleQuote(52.0))
        underlying2 = QuoteHandle(SimpleQuote(65.0))
        dividendTS1 = YieldTermStructureHandle(flatRate(today, 0.0, dc))
        dividendTS2 = YieldTermStructureHandle(flatRate(today, 0.0, dc))
        riskFreeTS = YieldTermStructureHandle(flatRate(today, 0.1, dc))
        blackVolTS1 = BlackVolTermStructureHandle(flatVol(today, 0.2, dc))
        blackVolTS2 = BlackVolTermStructureHandle(flatVol(today, 0.3, dc))
        correlation = QuoteHandle(SimpleQuote(0.75))

        process1 = BlackScholesMertonProcess(
            underlying1,
            dividendTS1,
            riskFreeTS,
            blackVolTS1)

        process2 = BlackScholesMertonProcess(
            underlying2,
            dividendTS2,
            riskFreeTS,
            blackVolTS2)

        option.setPricingEngine(AnalyticTwoAssetCorrelationEngine(
            process1,
            process2,
            correlation))

        calculated = option.NPV()
        expected = 4.7073
        error = abs(calculated - expected)
        tolerance = 1e-4
        self.assertFalse(error > tolerance)
