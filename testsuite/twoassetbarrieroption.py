import unittest
from utilities import *
from QuantLib import *


class OptionData(object):
    def __init__(self,
                 barrierType,
                 typeOpt,
                 barrier,
                 strike,
                 s1,
                 q1,
                 v1,
                 s2,
                 q2,
                 v2,
                 correlation,
                 r,
                 result):
        self.barrierType = barrierType
        self.typeOpt = typeOpt
        self.barrier = barrier
        self.strike = strike
        self.s1 = s1  # spot
        self.q1 = q1  # dividend
        self.v1 = v1  # volatility
        self.s2 = s2
        self.q2 = q2
        self.v2 = v2
        self.correlation = correlation
        self.r = r  # risk-free rate
        self.result = result  # result


class TwoAssetBarrierOptionTest(unittest.TestCase):
    def testHaugValues(self):
        TEST_MESSAGE("Testing two-asset barrier options against Haug's values...")

        values = [
            # The data below are from
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998
            OptionData(Barrier.DownOut, Option.Call, 95, 90, 100.0, 0.0, 0.2, 100.0, 0.0, 0.2, 0.5, 0.08, 6.6592),
            OptionData(Barrier.UpOut, Option.Call, 105, 90, 100.0, 0.0, 0.2, 100.0, 0.0, 0.2, -0.5, 0.08, 4.6670),
            OptionData(Barrier.DownOut, Option.Put, 95, 90, 100.0, 0.0, 0.2, 100.0, 0.0, 0.2, -0.5, 0.08, 0.6184),
            OptionData(Barrier.UpOut, Option.Put, 105, 100, 100.0, 0.0, 0.2, 100.0, 0.0, 0.2, 0.0, 0.08, 0.8246)
        ]

        dc = Actual360()
        calendar = TARGET()
        today = Date.todaysDate()
        maturity = today + 180
        exercise = EuropeanExercise(maturity)

        r = SimpleQuote(0.0)
        rTS = flatRate(today, r, dc)

        s1 = SimpleQuote(0.0)
        q1 = SimpleQuote(0.0)
        qTS1 = flatRate(today, q1, dc)
        vol1 = SimpleQuote(0.1)
        volTS1 = flatVol(today, vol1, dc)

        process1 = BlackScholesMertonProcess(
            QuoteHandle(s1),
            YieldTermStructureHandle(qTS1),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS1))

        s2 = SimpleQuote(0.0)
        q2 = SimpleQuote(0.0)
        qTS2 = flatRate(today, q2, dc)
        vol2 = SimpleQuote(0.1)
        volTS2 = flatVol(today, vol2, dc)

        process2 = BlackScholesMertonProcess(
            QuoteHandle(s2),
            YieldTermStructureHandle(qTS2),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS2))

        rho = SimpleQuote(0.0)

        engine = AnalyticTwoAssetBarrierEngine(process1, process2, QuoteHandle(rho))

        for value in values:
            s1.setValue(value.s1)
            q1.setValue(value.q1)
            vol1.setValue(value.v1)

            s2.setValue(value.s2)
            q2.setValue(value.q2)
            vol2.setValue(value.v2)

            rho.setValue(value.correlation)

            r.setValue(value.r)

            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)

            barrierOption = TwoAssetBarrierOption(value.barrierType, value.barrier, payoff, exercise)
            barrierOption.setPricingEngine(engine)

            calculated = barrierOption.NPV()
            expected = value.result
            error = abs(calculated - expected)
            tolerance = 4.0e-3
            self.assertFalse(error > tolerance)
