import unittest
from utilities import *
from QuantLib import *


def add10(x):
    return x + 10


def mul10(x):
    return x * 10


def sub10(x):
    return x - 10


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def sub(x, y):
    return x - y


class QuoteTest(unittest.TestCase):

    def testObservable(self):
        TEST_MESSAGE("Testing observability of quotes...")

        me = SimpleQuote(0.0)
        f = Flag()
        f.registerWith(me)
        me.setValue(3.14)

        self.assertFalse(not f.isUp())

    def testObservableHandle(self):
        TEST_MESSAGE("Testing observability of quote handles...")

        me1 = SimpleQuote(0.0)
        h = RelinkableQuoteHandle(me1)
        f = Flag()
        f.registerWith(h.asObservable())

        me1.setValue(3.14)
        self.assertFalse(not f.isUp())

        f.lower()
        me2 = SimpleQuote(0.0)
        h.linkTo(me2)
        self.assertFalse(not f.isUp())

    def testDerived(self):
        TEST_MESSAGE("Testing derived quotes...")

        funcs = [add10, mul10, sub10]

        me = SimpleQuote(17.0)
        h = QuoteHandle(me)

        for func in funcs:
            derived = DerivedUFQuote(h, func)
            x = derived.value()
            y = func(me.value())
            self.assertFalse(abs(x - y) > 1.0e-10)

    def testComposite(self):
        TEST_MESSAGE("Testing composite quotes...")

        funcs = [add, mul, sub]

        me1 = SimpleQuote(12.0)
        me2 = SimpleQuote(13.0)
        h1 = QuoteHandle(me1)
        h2 = QuoteHandle(me2)

        for func in funcs:
            composite = CompositeBFQuote(h1, h2, func)
            x = composite.value()
            y = func(me1.value(), me2.value())
            self.assertFalse(abs(x - y) > 1.0e-10)

    def testForwardValueQuoteAndImpliedStdevQuote(self):
        TEST_MESSAGE(
            "Testing forward-value and implied-standard-deviation quotes...")
        forwardRate = .05
        dc = ActualActual(ActualActual.ISDA)
        calendar = TARGET()
        forwardQuote = SimpleQuote(forwardRate)
        forwardHandle = QuoteHandle(forwardQuote)
        evaluationDate = Settings.instance().evaluationDate
        yc = FlatForward(
            evaluationDate, forwardHandle, dc)
        ycHandle = YieldTermStructureHandle(yc)
        euriborTenor = Period(1, Years)
        euribor = Euribor(euriborTenor, ycHandle)
        fixingDate = calendar.advance(evaluationDate, euriborTenor)
        forwardValueQuote = ForwardValueQuote(euribor, fixingDate)
        forwardValue = forwardValueQuote.value()
        expectedForwardValue = euribor.fixing(fixingDate, true)
        # we test if the forward value given by the quote is consistent
        # with the one directly given by the index
        self.assertFalse(abs(forwardValue - expectedForwardValue) > 1.0e-15)
        # then we test the observer/observable chain
        f = Flag()
        f.registerWith(forwardValueQuote)
        forwardQuote.setValue(0.04)
        self.assertFalse(not f.isUp())

        # and we retest if the values are still matching
        forwardValue = forwardValueQuote.value()
        expectedForwardValue = euribor.fixing(fixingDate, true)
        self.assertFalse(abs(forwardValue - expectedForwardValue) > 1.0e-15)
        # we test the ImpliedStdevQuote class
        f.unregisterWith(forwardValueQuote)
        f.lower()
        price = 0.02
        strike = 0.04
        guess = .15
        accuracy = 1.0e-6
        optionType = Option.Call
        priceQuote = SimpleQuote(price)
        priceHandle = QuoteHandle(priceQuote)
        impliedStdevQuote = ImpliedStdDevQuote(
            optionType, forwardHandle, priceHandle,
            strike, guess, accuracy)
        impliedStdev = impliedStdevQuote.value()
        expectedImpliedStdev = blackFormulaImpliedStdDev(
            optionType, strike,
            forwardQuote.value(), price,
            1.0, 0.0, guess, 1.0e-6)
        self.assertFalse(abs(impliedStdev - expectedImpliedStdev) > 1.0e-15)
        # then we test the observer/observable chain
        quote = impliedStdevQuote
        f.registerWith(quote)
        forwardQuote.setValue(0.05)
        self.assertFalse(not f.isUp())

        quote.value()
        f.lower()
        quote.value()
        priceQuote.setValue(0.11)
        self.assertFalse(not f.isUp())
