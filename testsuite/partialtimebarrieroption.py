import unittest

from QuantLib import *

from utilities import *


class TestCase(object):
    def __init__(self,
                 underlying,
                 strike,
                 days,
                 result):
        self.underlying = underlying
        self.strike = strike
        self.days = days
        self.result = result


class PartialTimeBarrierOptionTest(unittest.TestCase):

    def testAnalyticEngine(self):
        TEST_MESSAGE(
            "Testing analytic engine for partial-time barrier option...")

        today = Settings.instance().evaluationDate

        typeOpt = Option.Call
        dc = Actual360()
        maturity = today + 360
        exercise = EuropeanExercise(maturity)
        barrier = 100.0
        rebate = 0.0

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        rRate = SimpleQuote(0.1)
        vol = SimpleQuote(0.25)

        underlying = QuoteHandle(spot)
        dividendTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        riskFreeTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        blackVolTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        process = BlackScholesMertonProcess(
            underlying,
            dividendTS,
            riskFreeTS,
            blackVolTS)
        engine = AnalyticPartialTimeBarrierOptionEngine(process)

        cases = [
            TestCase(95.0, 90.0, 1, 0.0393),
            TestCase(95.0, 110.0, 1, 0.0000),
            TestCase(105.0, 90.0, 1, 9.8751),
            TestCase(105.0, 110.0, 1, 6.2303),
            TestCase(95.0, 90.0, 90, 6.2747),
            TestCase(95.0, 110.0, 90, 3.7352),
            TestCase(105.0, 90.0, 90, 15.6324),
            TestCase(105.0, 110.0, 90, 9.6812),
            TestCase(95.0, 90.0, 180, 10.3345),
            TestCase(95.0, 110.0, 180, 5.8712),
            TestCase(105.0, 90.0, 180, 19.2896),
            TestCase(105.0, 110.0, 180, 11.6055),
            TestCase(95.0, 90.0, 270, 13.4342),
            TestCase(95.0, 110.0, 270, 7.1270),
            TestCase(105.0, 90.0, 270, 22.0753),
            TestCase(105.0, 110.0, 270, 12.7342),
            TestCase(95.0, 90.0, 359, 16.8576),
            TestCase(95.0, 110.0, 359, 7.5763),
            TestCase(105.0, 90.0, 359, 25.1488),
            TestCase(105.0, 110.0, 359, 13.1376)]

        for i in cases:
            coverEventDate = today + i.days
            payoff = PlainVanillaPayoff(typeOpt, i.strike)
            option = PartialTimeBarrierOption(
                PartialBarrier.DownOut,
                PartialBarrier.EndB1,
                barrier, rebate,
                coverEventDate,
                payoff, exercise)
            option.setPricingEngine(engine)

            spot.setValue(i.underlying)
            calculated = option.NPV()
            expected = i.result
            error = abs(calculated - expected)
            tolerance = 1e-4
            self.assertFalse(error > tolerance)
