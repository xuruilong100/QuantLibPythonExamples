import unittest

from QuantLib import *

from utilities import *


class InstrumentTest(unittest.TestCase):

    def testObservable(self):
        TEST_MESSAGE(
            "Testing observability of instruments...")

        me1 = SimpleQuote(0.0)
        h = RelinkableQuoteHandle(me1)
        s = Stock(h)

        f = Flag()
        f.registerWith(s)

        s.NPV()
        me1.setValue(3.14)
        self.assertFalse(not f.isUp())

        s.NPV()
        f.lower()
        me2 = SimpleQuote(0.0)
        h.linkTo(me2)
        self.assertFalse(not f.isUp())

        f.lower()
        s.freeze()
        s.NPV()
        me2.setValue(2.71)
        self.assertFalse(f.isUp())

        s.NPV()
        s.unfreeze()
        self.assertFalse(not f.isUp())

    def testCompositeWhenShiftingDates(self):
        TEST_MESSAGE(
            "Testing reaction of composite instrument to date changes...")

        backup = SavedSettings()

        today = knownGoodDefault
        dc = Actual360()

        payoff = PlainVanillaPayoff(Option.Call, 100.0)
        exercise = EuropeanExercise(today + 30)

        option = EuropeanOption(payoff, exercise)

        spot = SimpleQuote(100.0)
        qTS = flatRate(0.0, dc)
        rTS = flatRate(0.01, dc)
        volTS = flatVol(0.1, dc)

        process = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        engine = AnalyticEuropeanEngine(process)

        option.setPricingEngine(engine)

        composite = CompositeInstrument()
        composite.add(option)

        Settings.instance().evaluationDate = today + 45

        self.assertFalse(not composite.isExpired())
        self.assertFalse(composite.NPV() != 0.0)

        Settings.instance().evaluationDate = today

        self.assertFalse(composite.isExpired())
        self.assertFalse(composite.NPV() == 0.0)
