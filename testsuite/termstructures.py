import unittest
from utilities import *
from QuantLib import *


class Datum(object):
    def __init__(self,
                 n,
                 units,
                 rate):
        self.n = n
        self.units = units
        self.rate = rate


class CommonVars(object):
    # common data
    # calendar
    # settlementDays
    # termStructure
    # dummyTermStructure

    # cleanup
    backup = SavedSettings()

    def __init__(self):
        self.calendar = TARGET()
        self.settlementDays = 2
        today = self.calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = today
        settlement = self.calendar.advance(today, self.settlementDays, Days)
        depositData = [
            Datum(1, Months, 4.581),
            Datum(2, Months, 4.573),
            Datum(3, Months, 4.557),
            Datum(6, Months, 4.496),
            Datum(9, Months, 4.490)]
        swapData = [
            Datum(1, Years, 4.54),
            Datum(5, Years, 4.99),
            Datum(10, Years, 5.47),
            Datum(20, Years, 5.89),
            Datum(30, Years, 5.96)]
        deposits = len(depositData)
        swaps = len(swapData)

        instruments = RateHelperVector(deposits + swaps)
        for i in range(deposits):
            instruments[i] = DepositRateHelper(
                depositData[i].rate / 100,
                Period(depositData[i].n, depositData[i].units),
                self.settlementDays, self.calendar,
                ModifiedFollowing, true,
                Actual360())

        index = IborIndex(
            "dummy",
            Period(6, Months),
            self.settlementDays,
            Currency(),
            self.calendar,
            ModifiedFollowing,
            false,
            Actual360())
        for i in range(swaps):
            instruments[i + deposits] = SwapRateHelper(
                swapData[i].rate / 100,
                Period(swapData[i].n, swapData[i].units),
                self.calendar,
                Annual, Unadjusted,
                Thirty360(Thirty360.BondBasis),
                index)

        self.termStructure = PiecewiseLogLinearDiscount(
            settlement,
            instruments, Actual360())
        self.dummyTermStructure = PiecewiseLogLinearDiscount(
            settlement,
            instruments, Actual360())


def sub(x, y):
    return x - y


class TermStructureTest(unittest.TestCase):

    def testReferenceChange(self):
        TEST_MESSAGE("Testing term structure against evaluation date change...")

        vars = CommonVars()

        flatRate = SimpleQuote(NullReal())
        flatRateHandle = QuoteHandle(flatRate)
        vars.termStructure = FlatForward(
            vars.settlementDays, NullCalendar(),
            flatRateHandle, Actual360())
        today = Settings.instance().evaluationDate
        flatRate.setValue(.03)
        days = [10, 30, 60, 120, 360, 720]

        expected = DoubleVector(len(days))
        for i in range(len(days)):
            expected[i] = vars.termStructure.discount(today + days[i])

        Settings.instance().evaluationDate = today + 30
        calculated = DoubleVector(len(days))
        for i in range(len(days)):
            calculated[i] = vars.termStructure.discount(today + 30 + days[i])

        for i in range(len(days)):
            self.assertFalse(not close(expected[i], calculated[i]))

    def testImplied(self):
        TEST_MESSAGE("Testing consistency of implied term structure...")

        vars = CommonVars()

        tolerance = 1.0e-10
        today = Settings.instance().evaluationDate
        newToday = today + 3 * Years
        newSettlement = vars.calendar.advance(
            newToday, vars.settlementDays, Days)
        testDate = newSettlement + Period(5, Years)
        implied = ImpliedTermStructure(
            YieldTermStructureHandle(vars.termStructure),
            newSettlement)
        baseDiscount = vars.termStructure.discount(newSettlement)
        discount = vars.termStructure.discount(testDate)
        impliedDiscount = implied.discount(testDate)
        self.assertFalse(
            abs(discount - baseDiscount * impliedDiscount) > tolerance)

    def testImpliedObs(self):
        TEST_MESSAGE("Testing observability of implied term structure...")

        vars = CommonVars()

        today = Settings.instance().evaluationDate
        newToday = today + 3 * Years
        newSettlement = vars.calendar.advance(
            newToday, vars.settlementDays, Days)
        h = RelinkableYieldTermStructureHandle()
        implied = ImpliedTermStructure(h, newSettlement)
        flag = Flag()
        flag.registerWith(implied)
        h.linkTo(vars.termStructure)
        self.assertFalse(not flag.isUp())

    def testFSpreaded(self):
        TEST_MESSAGE("Testing consistency of forward-spreaded term structure...")

        vars = CommonVars()

        tolerance = 1.0e-10
        me = SimpleQuote(0.01)
        mh = QuoteHandle(me)
        spreaded = ForwardSpreadedTermStructure(
            YieldTermStructureHandle(vars.termStructure), mh)
        testDate = vars.termStructure.referenceDate() + Period(5, Years)
        tsdc = vars.termStructure.dayCounter()
        sprdc = spreaded.dayCounter()
        forward = vars.termStructure.forwardRate(
            testDate, testDate, tsdc, Continuous, NoFrequency)
        spreadedForward = spreaded.forwardRate(
            testDate, testDate, sprdc, Continuous, NoFrequency)
        self.assertFalse(
            abs(forward.rate() - (spreadedForward.rate() - me.value())) > tolerance)

    def testFSpreadedObs(self):
        TEST_MESSAGE("Testing observability of forward-spreaded "
                     "term structure...")

        vars = CommonVars()

        me = SimpleQuote(0.01)
        mh = QuoteHandle(me)
        h = RelinkableYieldTermStructureHandle()  # (vars.dummyTermStructure)
        spreaded = ForwardSpreadedTermStructure(h, mh)
        flag = Flag()
        flag.registerWith(spreaded)
        h.linkTo(vars.termStructure)
        self.assertFalse(not flag.isUp())
        flag.lower()
        me.setValue(0.005)
        self.assertFalse(not flag.isUp())

    def testZSpreaded(self):
        TEST_MESSAGE("Testing consistency of zero-spreaded term structure...")

        vars = CommonVars()

        tolerance = 1.0e-10
        me = SimpleQuote(0.01)
        mh = QuoteHandle(me)
        spreaded = ZeroSpreadedTermStructure(
            YieldTermStructureHandle(vars.termStructure), mh)
        testDate = vars.termStructure.referenceDate() + Period(5, Years)
        rfdc = vars.termStructure.dayCounter()
        zero = vars.termStructure.zeroRate(
            testDate, rfdc,
            Continuous, NoFrequency)
        spreadedZero = spreaded.zeroRate(
            testDate, rfdc,
            Continuous, NoFrequency)
        self.assertFalse(
            abs(zero.rate() - (spreadedZero.rate() - me.value())) > tolerance)

    def testZSpreadedObs(self):
        TEST_MESSAGE("Testing observability of zero-spreaded term structure...")

        vars = CommonVars()

        me = SimpleQuote(0.01)
        mh = QuoteHandle(me)
        h = RelinkableYieldTermStructureHandle(vars.dummyTermStructure)

        spreaded = ZeroSpreadedTermStructure(h, mh)
        flag = Flag()
        flag.registerWith(spreaded)
        h.linkTo(vars.termStructure)
        self.assertFalse(not flag.isUp())
        flag.lower()
        me.setValue(0.005)
        self.assertFalse(not flag.isUp())

    def testCreateWithNullUnderlying(self):
        TEST_MESSAGE(
            "Testing that a zero-spreaded curve can be created with "
            "a null underlying curve...")

        vars = CommonVars()

        spread = QuoteHandle(SimpleQuote(0.01))
        underlying = RelinkableYieldTermStructureHandle()
        # this shouldn't throw
        spreaded = ZeroSpreadedTermStructure(underlying, spread)
        # if we do this, the curve can work.
        underlying.linkTo(vars.termStructure)
        # check that we can use it
        spreaded.referenceDate()

    @unittest.skip('YieldTermStructure: No constructor defined')
    def testLinkToNullUnderlying(self):
        TEST_MESSAGE(
            "Testing that an underlying curve can be relinked to "
            "a null underlying curve...")

        vars = CommonVars()

        spread = QuoteHandle(SimpleQuote(0.01))
        underlying = RelinkableYieldTermStructureHandle(vars.termStructure)
        spreaded = ZeroSpreadedTermStructure(underlying, spread)
        # check that we can use it
        spreaded.referenceDate()
        # if we do this, the curve can't work anymore. But it shouldn't
        # throw as long as we don't try to use it.
        underlying.linkTo(YieldTermStructure())

    def testCompositeZeroYieldStructures(self):
        TEST_MESSAGE(
            "Testing composite zero yield structures...")

        backup = SavedSettings()
        Settings.instance().evaluationDate = Date(10, Nov, 2017)

        # First curve
        dates = [
            Date(10, Nov, 2017), Date(13, Nov, 2017), Date(12, Feb, 2018),
            Date(10, May, 2018), Date(10, Aug, 2018), Date(12, Nov, 2018),
            Date(21, Dec, 2018), Date(15, Jan, 2020), Date(31, Mar, 2021),
            Date(28, Feb, 2023), Date(21, Dec, 2026), Date(31, Jan, 2030),
            Date(28, Feb, 2031), Date(31, Mar, 2036), Date(28, Feb, 2041),
            Date(28, Feb, 2048), Date(31, Dec, 2141)]

        rates = [
            0.0655823213132524, 0.0655823213132524, 0.0699455024156877,
            0.0799107139233497, 0.0813931951022577, 0.0841615820666691,
            0.0501297919004145, 0.0823483583439658, 0.0860720030924466,
            0.0922887604375688, 0.10588902278996, 0.117021968693922,
            0.109824660896137, 0.109231572878364, 0.119218123236241,
            0.128647300167664, 0.0506086995288751]

        termStructure1 = ForwardCurve(dates, rates, Actual365Fixed(), NullCalendar())

        # Second curve
        dates = [
            Date(10, Nov, 2017), Date(13, Nov, 2017), Date(11, Dec, 2017), Date(12, Feb, 2018),
            Date(10, May, 2018), Date(31, Jan, 2022), Date(7, Dec, 2023), Date(31, Jan, 2025),
            Date(31, Mar, 2028), Date(7, Dec, 2033), Date(1, Feb, 2038), Date(2, Apr, 2046),
            Date(2, Jan, 2051), Date(31, Dec, 2141)]

        rates = [
            0.056656806197189, 0.056656806197189, 0.0419541633454473, 0.0286681050019797,
            0.0148840226959593, 0.0246680238374363, 0.0255349067810599, 0.0298907184711927,
            0.0263943927922053, 0.0291924526539802, 0.0270049276163556, 0.028775807327614,
            0.0293567711641792, 0.010518655099659]

        termStructure2 = ForwardCurve(dates, rates, Actual365Fixed(), NullCalendar())

        # typedef Real(*binary_f)(Real, Real)

        compoundCurve = CompositeBFZeroYieldStructure(
            YieldTermStructureHandle(termStructure1),
            YieldTermStructureHandle(termStructure2),
            sub)

        # Expected values
        dates = [
            Date(10, Nov, 2017), Date(15, Dec, 2017), Date(15, Jun, 2018), Date(15, Sep, 2029),
            Date(15, Sep, 2038), Date(15, Mar, 2046), Date(15, Dec, 2141)]

        rates = [
            0.00892551511527986, 0.0278755322562788, 0.0512001768603456, 0.0729941474263546,
            0.0778333309498459, 0.0828451659139004, 0.0503573807521742]

        tolerance = 1.0e-10
        for i in range(len(dates)):
            actual = compoundCurve.zeroRate(
                dates[i], Actual365Fixed(), Continuous).rate()
            expected = rates[i]

            self.assertFalse(abs(actual - expected) > tolerance)
