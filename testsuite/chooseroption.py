import unittest

from QuantLib import *

from utilities import *


class ChooserOptionTest(unittest.TestCase):

    def testAnalyticSimpleChooserEngine(self):
        TEST_MESSAGE(
            "Testing analytic simple chooser option...")

        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(50.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.08)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.25)
        volTS = flatVol(today, vol, dc)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))

        engine = AnalyticSimpleChooserEngine(stochProcess)

        strike = 50.0

        exerciseDate = today + 180
        exercise = EuropeanExercise(exerciseDate)

        choosingDate = today + 90
        option = SimpleChooserOption(
            choosingDate, strike, exercise)
        option.setPricingEngine(engine)

        calculated = option.NPV()
        expected = 6.1071
        tolerance = 3e-5
        self.assertFalse(abs(calculated - expected) > tolerance)

    @unittest.skip("testAnalyticComplexChooserEngine: crash")
    def testAnalyticComplexChooserEngine(self):
        TEST_MESSAGE(
            "Testing analytic complex chooser option...")

        dc = Actual360()
        today = knownGoodDefault
        Settings.instance().evaluationDate = today

        spot = SimpleQuote(50.0)
        qRate = SimpleQuote(0.05)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.10)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.35)
        volTS = flatVol(today, vol, dc)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))

        engine = AnalyticComplexChooserEngine(stochProcess)

        callStrike = 55.0
        putStrike = 48.0

        choosingDate = today + Period(90, Days)
        callExerciseDate = choosingDate + Period(180, Days)
        putExerciseDate = choosingDate + Period(210, Days)
        callExercise = EuropeanExercise(callExerciseDate)
        putExercise = EuropeanExercise(putExerciseDate)

        option = ComplexChooserOption(
            choosingDate, callStrike, putStrike,
            callExercise, putExercise)
        option.setPricingEngine(engine)

        calculated = option.NPV()
        expected = 6.0508
        error = abs(calculated - expected)
        tolerance = 1e-4
        self.assertFalse(error > tolerance)
