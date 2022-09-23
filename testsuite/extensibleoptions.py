import unittest

from QuantLib import *

from utilities import *


class ExtensibleOptionsTest(unittest.TestCase):

    def testAnalyticHolderExtensibleOptionEngine(self):
        TEST_MESSAGE(
            "Testing analytic engine for holder-extensible option...")

        typeOpt = Option.Call
        strike1 = 100.0
        strike2 = 105.0
        dc = Actual360()
        today = Settings.instance().evaluationDate
        exDate1 = today + 180
        exDate2 = today + 270
        premium = 1.0

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.0)
        rRate = SimpleQuote(0.08)
        vol = SimpleQuote(0.25)

        payoff = PlainVanillaPayoff(typeOpt, strike1)
        exercise = EuropeanExercise(exDate1)

        option = HolderExtensibleOption(
            typeOpt, premium,
            exDate2, strike2,
            payoff, exercise)

        underlying = QuoteHandle(spot)
        dividendTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        riskFreeTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        blackVolTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        process = BlackScholesMertonProcess(
            underlying,
            dividendTS,
            riskFreeTS,
            blackVolTS)

        option.setPricingEngine(AnalyticHolderExtensibleOptionEngine(process))

        calculated = option.NPV()
        expected = 9.4233
        error = abs(calculated - expected)
        tolerance = 1e-4
        self.assertFalse(error > tolerance)

    def testAnalyticWriterExtensibleOptionEngine(self):
        TEST_MESSAGE(
            "Testing analytic engine for writer-extensible option...")

        typeOpt = Option.Call
        strike1 = 90.0
        strike2 = 82.0
        dc = Actual360()
        today = Settings.instance().evaluationDate
        exDate1 = today + 180
        exDate2 = today + 270

        spot = SimpleQuote(80.0)
        qRate = SimpleQuote(0.0)
        dividendTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.10)
        riskFreeTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.30)
        blackVolTS = flatVol(today, vol, dc)

        process = GeneralizedBlackScholesProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(dividendTS),
            YieldTermStructureHandle(riskFreeTS),
            BlackVolTermStructureHandle(blackVolTS))

        engine = AnalyticWriterExtensibleOptionEngine(process)

        payoff1 = PlainVanillaPayoff(typeOpt, strike1)
        exercise1 = EuropeanExercise(exDate1)
        payoff2 = PlainVanillaPayoff(typeOpt, strike2)
        exercise2 = EuropeanExercise(exDate2)

        option = WriterExtensibleOption(payoff1, exercise1, payoff2, exercise2)

        option.setPricingEngine(engine)

        calculated = option.NPV()
        expected = 6.8238
        error = abs(calculated - expected)
        tolerance = 1e-4
        self.assertFalse(error > tolerance)
