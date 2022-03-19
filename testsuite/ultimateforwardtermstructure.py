import unittest
from utilities import *
from QuantLib import *
from math import exp


class Datum(object):
    def __init__(self,
                 n,
                 units,
                 rate):
        self.n = n
        self.units = units
        self.rate = rate


class LLFRWeight(object):
    def __init__(self,
                 ttm,
                 weight):
        self.ttm = ttm
        self.weight = weight


class CommonVars(object):

    def __init__(self):
        self.backup = SavedSettings()
        self.settlementDays = 2
        self.businessConvention = Unadjusted
        self.dayCount = SimpleDayCounter()
        self.calendar = NullCalendar()
        self.ccy = EURCurrency()
        self.fixedFrequency = Annual
        self.floatingTenor = Period(6, Months)
        self.ftkCurveHandle = RelinkableYieldTermStructureHandle()

        self.index = IborIndex(
            "FTK_IDX", self.floatingTenor, self.settlementDays, self.ccy, self.calendar,
            self.businessConvention, false, self.dayCount, self.ftkCurveHandle)

        # Data source: https:#fred.stlouisfed.org/
        # Note that these rates are used as a proxy.

        # In order to fully replicate the rates published by the Dutch Central Bank
        # (with the required accuracy) one needs to use Bloomberg CMPL BID Euribor 6m swap
        # rates as stated in the documentation: https:#www.toezicht.dnb.nl 
        swapData = [
            Datum(1, Years, -0.00315), Datum(2, Years, -0.00205), Datum(3, Years, -0.00144),
            Datum(4, Years, -0.00068), Datum(5, Years, 0.00014), Datum(6, Years, 0.00103),
            Datum(7, Years, 0.00194), Datum(8, Years, 0.00288), Datum(9, Years, 0.00381),
            Datum(10, Years, 0.00471), Datum(12, Years, 0.0063), Datum(15, Years, 0.00808),
            Datum(20, Years, 0.00973), Datum(25, Years, 0.01035), Datum(30, Years, 0.01055),
            Datum(40, Years, 0.0103), Datum(50, Years, 0.0103)]

        ufr = InterestRate(0.023, self.dayCount, Compounded, Annual)
        self.ufrRate = SimpleQuote(
            ufr.equivalentRate(Continuous, Annual, 1.0).rate())
        self.fsp = Period(20, Years)
        self.alpha = 0.1

        self.today = self.calendar.adjust(Date(29, March, 2019))
        Settings.instance().evaluationDate = self.today
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)

        nInstruments = len(swapData)
        instruments = RateHelperVector(nInstruments)
        for i in range(nInstruments):
            instruments[i] = SwapRateHelper(
                swapData[i].rate, Period(swapData[i].n, swapData[i].units), self.calendar,
                self.fixedFrequency, self.businessConvention, self.dayCount, self.index)

        self.ftkCurve = PiecewiseLogLinearDiscount(
            self.settlement, instruments, self.dayCount, LogLinear())
        self.ftkCurve.enableExtrapolation()
        self.ftkCurveHandle.linkTo(self.ftkCurve)


def calculateLLFR(ts, fsp):
    dc = ts.dayCounter()
    omega = 8.0 / 15.0
    cutOff = ts.timeFromReference(ts.referenceDate() + fsp)

    llfrWeights = [
        LLFRWeight(25.0, 1.0), LLFRWeight(30.0, 0.5),
        LLFRWeight(40.0, 0.25), LLFRWeight(50.0, 0.125)]
    nWeights = len(llfrWeights)
    llfr = 0.0
    for j in range(nWeights):
        w = llfrWeights[j]
        llfr += w.weight * ts.forwardRate(
            cutOff, w.ttm, Continuous, NoFrequency, true).rate()

    return SimpleQuote(omega * llfr)


def calculateExtrapolatedForward(t, fsp, llfr, ufr, alpha):
    deltaT = t - fsp
    beta = (1.0 - exp(-alpha * deltaT)) / (alpha * deltaT)
    return ufr + (llfr - ufr) * beta


class UltimateForwardTermStructureTest(unittest.TestCase):

    def testDutchCentralBankRates(self):
        TEST_MESSAGE("Testing DNB replication of UFR zero annually compounded rates...")

        vars = CommonVars()

        llfr = calculateLLFR(vars.ftkCurveHandle, vars.fsp)

        ufrTs = UltimateForwardTermStructure(
            vars.ftkCurveHandle, QuoteHandle(llfr),
            QuoteHandle(vars.ufrRate), vars.fsp, vars.alpha)

        # Official annually compounded zero rates published
        # by the Dutch Central Bank: https:#statistiek.dnb.nl/
        expectedZeroes = [
            Datum(10, Years, 0.00477), Datum(20, Years, 0.01004), Datum(30, Years, 0.01223),
            Datum(40, Years, 0.01433), Datum(50, Years, 0.01589), Datum(60, Years, 0.01702),
            Datum(70, Years, 0.01785), Datum(80, Years, 0.01849), Datum(90, Years, 0.01899),
            Datum(100, Years, 0.01939)]

        tolerance = 1.0e-4
        nRates = len(expectedZeroes)

        for i in range(nRates):
            p = Period(expectedZeroes[i].n, expectedZeroes[i].units)
            maturity = vars.settlement + p

            actual = ufrTs.zeroRate(
                maturity, vars.dayCount, Compounded, Annual).rate()
            expected = expectedZeroes[i].rate

            self.assertFalse(abs(actual - expected) > tolerance)

    def testExtrapolatedForward(self):
        TEST_MESSAGE("Testing continuous forward rates in extrapolation region...")

        vars = CommonVars()

        llfr = SimpleQuote(0.0125)

        ufrTs = UltimateForwardTermStructure(
            vars.ftkCurveHandle, QuoteHandle(llfr),
            QuoteHandle(vars.ufrRate), vars.fsp, vars.alpha)
        cutOff = ufrTs.timeFromReference(ufrTs.referenceDate() + vars.fsp)

        tenors = [
            # Period(20, Years),
            Period(30, Years), Period(40, Years), Period(50, Years),
            Period(60, Years), Period(70, Years), Period(80, Years),
            Period(90, Years), Period(100, Years)]

        nTenors = len(tenors)

        for i in range(nTenors):
            maturity = vars.settlement + tenors[i]
            t = ufrTs.timeFromReference(maturity)

            actual = ufrTs.forwardRate(
                cutOff, t, Continuous, NoFrequency, true).rate()
            expected = calculateExtrapolatedForward(
                t, cutOff, llfr.value(),
                vars.ufrRate.value(), vars.alpha)

            tolerance = 1.0e-10
            self.assertFalse(abs(actual - expected) > tolerance)

    def testZeroRateAtFirstSmoothingPoint(self):
        TEST_MESSAGE("Testing zero rate on the first smoothing point...")

        vars = CommonVars()

        llfr = SimpleQuote(0.0125)

        ufrTs = UltimateForwardTermStructure(
            vars.ftkCurveHandle, QuoteHandle(llfr),
            QuoteHandle(vars.ufrRate), vars.fsp, vars.alpha)
        cutOff = ufrTs.timeFromReference(
            ufrTs.referenceDate() + vars.fsp)

        actual = ufrTs.zeroRate(
            cutOff, Continuous, NoFrequency, true).rate()
        expected = vars.ftkCurveHandle.zeroRate(
            cutOff, Continuous, NoFrequency, true).rate()

        tolerance = 1.0e-10
        self.assertFalse(abs(actual - expected) > tolerance)

    def testThatInspectorsEqualToBaseCurve(self):
        TEST_MESSAGE("Testing UFR curve inspectors...")

        vars = CommonVars()

        llfr = SimpleQuote(0.0125)

        ufrTs = UltimateForwardTermStructure(
            vars.ftkCurveHandle, QuoteHandle(llfr),
            QuoteHandle(vars.ufrRate), vars.fsp, vars.alpha)

        self.assertFalse(ufrTs.dayCounter() != vars.ftkCurveHandle.dayCounter())
        self.assertFalse(ufrTs.referenceDate() != vars.ftkCurveHandle.referenceDate())
        self.assertFalse(ufrTs.maxDate() == vars.ftkCurveHandle.maxDate())
        self.assertFalse(ufrTs.maxTime() == vars.ftkCurveHandle.maxTime())

    def testExceptionWhenFspLessOrEqualZero(self):
        TEST_MESSAGE("Testing exception when the first smoothing point is less than or equal to zero...")

        vars = CommonVars()

        llfr = SimpleQuote(0.0125)

        self.assertRaises(
            RuntimeError,
            UltimateForwardTermStructure,
            vars.ftkCurveHandle, QuoteHandle(llfr),
            QuoteHandle(vars.ufrRate), Period(0, Years), vars.alpha)

        self.assertRaises(
            RuntimeError,
            UltimateForwardTermStructure,
            vars.ftkCurveHandle, QuoteHandle(llfr),
            QuoteHandle(vars.ufrRate), -Period(1, Years), vars.alpha)

    def testObservability(self):
        TEST_MESSAGE("Testing observability of the UFR curve...")

        vars = CommonVars()

        llfr = SimpleQuote(0.0125)
        llfr_quote = QuoteHandle(llfr)
        ufr = SimpleQuote(0.02)
        ufr_handle = QuoteHandle(ufr)
        ufrTs = UltimateForwardTermStructure(
            vars.ftkCurveHandle, llfr_quote,
            ufr_handle, vars.fsp, vars.alpha)

        flag = Flag()
        flag.registerWith(ufrTs)
        llfr.setValue(0.012)
        self.assertFalse(not flag.isUp())
        flag.lower()
        ufr.setValue(0.019)
        self.assertFalse(not flag.isUp())
