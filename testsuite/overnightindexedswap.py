import unittest
from utilities import *
from QuantLib import *
from math import exp


class Datum(object):
    def __init__(self, settlementDays,
                 n,
                 unit,
                 rate, ):
        self.settlementDays = settlementDays
        self.n = n
        self.unit = unit
        self.rate = rate


depositData = [
    Datum(0, 1, Days, 1.10),
    Datum(1, 1, Days, 1.10),
    Datum(2, 1, Weeks, 1.40),
    Datum(2, 2, Weeks, 1.50),
    Datum(2, 1, Months, 1.70),
    Datum(2, 2, Months, 1.90),
    Datum(2, 3, Months, 2.05),
    Datum(2, 4, Months, 2.08),
    Datum(2, 5, Months, 2.11),
    Datum(2, 6, Months, 2.13)]

eoniaSwapData = [
    Datum(2, 1, Weeks, 1.245),
    Datum(2, 2, Weeks, 1.269),
    Datum(2, 3, Weeks, 1.277),
    Datum(2, 1, Months, 1.281),
    Datum(2, 2, Months, 1.18),
    Datum(2, 3, Months, 1.143),
    Datum(2, 4, Months, 1.125),
    Datum(2, 5, Months, 1.116),
    Datum(2, 6, Months, 1.111),
    Datum(2, 7, Months, 1.109),
    Datum(2, 8, Months, 1.111),
    Datum(2, 9, Months, 1.117),
    Datum(2, 10, Months, 1.129),
    Datum(2, 11, Months, 1.141),
    Datum(2, 12, Months, 1.153),
    Datum(2, 15, Months, 1.218),
    Datum(2, 18, Months, 1.308),
    Datum(2, 21, Months, 1.407),
    Datum(2, 2, Years, 1.510),
    Datum(2, 3, Years, 1.916),
    Datum(2, 4, Years, 2.254),
    Datum(2, 5, Years, 2.523),
    Datum(2, 6, Years, 2.746),
    Datum(2, 7, Years, 2.934),
    Datum(2, 8, Years, 3.092),
    Datum(2, 9, Years, 3.231),
    Datum(2, 10, Years, 3.380),
    Datum(2, 11, Years, 3.457),
    Datum(2, 12, Years, 3.544),
    Datum(2, 15, Years, 3.702),
    Datum(2, 20, Years, 3.703),
    Datum(2, 25, Years, 3.541),
    Datum(2, 30, Years, 3.369)]


class CommonVars(object):

    def __init__(self):
        self.type = Swap.Payer
        self.settlementDays = 2
        self.nominal = 100.0
        self.fixedEoniaConvention = ModifiedFollowing
        self.floatingEoniaConvention = ModifiedFollowing
        self.fixedEoniaPeriod = Period(1, Years)
        self.floatingEoniaPeriod = Period(1, Years)
        self.fixedEoniaDayCount = Actual360()
        self.eoniaTermStructure = RelinkableYieldTermStructureHandle()
        self.eoniaIndex = Eonia(self.eoniaTermStructure)
        self.fixedSwapConvention = ModifiedFollowing
        self.fixedSwapFrequency = Annual
        self.fixedSwapDayCount = Thirty360(Thirty360.BondBasis)
        self.swapTermStructure = RelinkableYieldTermStructureHandle()
        self.swapIndex = Euribor3M(self.swapTermStructure)
        self.calendar = self.eoniaIndex.fixingCalendar()
        self.today = Date(5, February, 2009)
        # today = calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = self.today
        self.settlement = self.calendar.advance(
            self.today, Period(self.settlementDays, Days), Following)
        self.eoniaTermStructure.linkTo(
            flatRate(self.today, 0.05, Actual365Fixed()))
        self.backup = SavedSettings()

    # utilities
    def makeSwap(self,
                 length,
                 fixedRate,
                 spread,
                 telescopicValueDates,
                 effectiveDate=NullDate(),
                 paymentLag=0,
                 averagingMethod=RateAveraging.Compound):
        ois = MakeOIS(length, self.eoniaIndex, fixedRate, Period(0, Days))
        ois.withEffectiveDate(
            self.settlement if effectiveDate == NullDate() else effectiveDate)
        ois.withOvernightLegSpread(spread)
        ois.withNominal(self.nominal)
        ois.withPaymentLag(paymentLag)
        ois.withDiscountingTermStructure(self.eoniaTermStructure)
        ois.withTelescopicValueDates(telescopicValueDates)
        ois.withAveragingMethod(averagingMethod)
        ois = ois.makeOIS()
        return ois


class OvernightIndexedSwapTest(unittest.TestCase):

    def testFairRate(self):
        TEST_MESSAGE("Testing Eonia-swap calculation of fair fixed rate...")

        vars = CommonVars()

        lengths = [
            Period(1, Years), Period(2, Years), Period(5, Years),
            Period(10, Years), Period(20, Years)]
        spreads = [-0.001, -0.01, 0.0, 0.01, 0.001]

        for length in lengths:
            for spread in spreads:
                swap = vars.makeSwap(length, 0.0, spread, false)
                swap2 = vars.makeSwap(length, 0.0, spread, true)
                self.assertFalse(abs(swap.fairRate() - swap2.fairRate()) > 1.0e-10)
                swap = vars.makeSwap(length, swap.fairRate(), spread, false)
                self.assertFalse(abs(swap.NPV()) > 1.0e-10)
                swap = vars.makeSwap(length, swap.fairRate(), spread, true)
                self.assertFalse(abs(swap.NPV()) > 1.0e-10)

    def testFairSpread(self):
        TEST_MESSAGE("Testing Eonia-swap calculation of fair floating spread...")

        vars = CommonVars()

        lengths = [
            Period(1, Years), Period(2, Years), Period(5, Years),
            Period(10, Years), Period(20, Years)]
        rates = [0.04, 0.05, 0.06, 0.07]

        for length in lengths:
            for j in rates:
                swap = vars.makeSwap(length, j, 0.0, false)
                swap2 = vars.makeSwap(length, j, 0.0, true)
                fairSpread = swap.fairSpread()
                fairSpread2 = swap2.fairSpread()
                self.assertFalse(abs(fairSpread - fairSpread2) > 1.0e-10)
                swap = vars.makeSwap(length, j, fairSpread, false)
                self.assertFalse(abs(swap.NPV()) > 1.0e-10)
                swap = vars.makeSwap(length, j, fairSpread, true)
                self.assertFalse(abs(swap.NPV()) > 1.0e-10)

    def testCachedValue(self):
        TEST_MESSAGE("Testing Eonia-swap calculation against cached value...")

        vars = CommonVars()

        Settings.instance().evaluationDate = vars.today
        vars.settlement = vars.calendar.advance(
            vars.today, vars.settlementDays, Days)
        flat = 0.05
        vars.eoniaTermStructure.linkTo(
            flatRate(vars.settlement, flat, Actual360()))
        fixedRate = exp(flat) - 1
        swap = vars.makeSwap(Period(1, Years), fixedRate, 0.0, false)
        swap2 = vars.makeSwap(Period(1, Years), fixedRate, 0.0, true)
        cachedNPV = 0.001730450147
        tolerance = 1.0e-11
        self.assertFalse(abs(swap.NPV() - cachedNPV) > tolerance)
        self.assertFalse(abs(swap2.NPV() - cachedNPV) > tolerance)

    def testBootstrap(self):
        TEST_MESSAGE("Testing Eonia-swap curve building with daily compounded ON rates...")
        self._testBootstrap(false, RateAveraging.Compound)

    def testBootstrapWithArithmeticAverage(self):
        TEST_MESSAGE("Testing Eonia-swap curve building with arithmetic average ON rates...")
        self._testBootstrap(false, RateAveraging.Simple)

    def testBootstrapWithTelescopicDates(self):
        TEST_MESSAGE("Testing Eonia-swap curve building with telescopic value dates and DCON rates...")
        self._testBootstrap(true, RateAveraging.Compound)

    def testBootstrapWithTelescopicDatesAndArithmeticAverage(self):
        TEST_MESSAGE(
            "Testing Eonia-swap curve building with telescopic value dates and AAON rates...")
        # Given that we are using an approximation that omits
        # the required convexity correction, a lower tolerance
        # is needed.
        self._testBootstrap(true, RateAveraging.Simple, 1.0e-5)

    def testSeasonedSwaps(self):
        TEST_MESSAGE("Testing seasoned Eonia-swap calculation...")

        vars = CommonVars()

        lengths = [
            Period(1, Years), Period(2, Years), Period(5, Years),
            Period(10, Years), Period(20, Years)]
        spreads = [-0.001, -0.01, 0.0, 0.01, 0.001]

        effectiveDate = Date(2, February, 2009)

        vars.eoniaIndex.addFixing(Date(2, February, 2009), 0.0010)  # fake fixing values
        vars.eoniaIndex.addFixing(Date(3, February, 2009), 0.0011)
        vars.eoniaIndex.addFixing(Date(4, February, 2009), 0.0012)
        vars.eoniaIndex.addFixing(Date(5, February, 2009), 0.0013)

        for length in lengths:
            for spread in spreads:
                swap = vars.makeSwap(length, 0.0, spread, false, effectiveDate)
                swap2 = vars.makeSwap(length, 0.0, spread, true, effectiveDate)
                self.assertFalse(abs(swap.NPV() - swap2.NPV()) > 1.0e-10)

    def testBootstrapRegression(self):
        TEST_MESSAGE("Testing 1.16 regression with OIS bootstrap...")

        backup = SavedSettings()

        data = [
            Datum(0, 1, Days, 0.0066),
            Datum(2, 1, Weeks, 0.006445),
            Datum(2, 2, Weeks, 0.006455),
            Datum(2, 3, Weeks, 0.00645),
            Datum(2, 1, Months, 0.00675),
            Datum(2, 2, Months, 0.007),
            Datum(2, 3, Months, 0.00724),
            Datum(2, 4, Months, 0.007533),
            Datum(2, 5, Months, 0.00785),
            Datum(2, 6, Months, 0.00814),
            Datum(2, 9, Months, 0.00889),
            Datum(2, 1, Years, 0.00967),
            Datum(2, 2, Years, 0.01221),
            Datum(2, 3, Years, 0.01413),
            Datum(2, 4, Years, 0.01555),
            Datum(2, 5, Years, 0.01672),
            Datum(2, 10, Years, 0.02005),
            Datum(2, 12, Years, 0.0208),
            Datum(2, 15, Years, 0.02152),
            Datum(2, 20, Years, 0.02215),
            Datum(2, 25, Years, 0.02233),
            Datum(2, 30, Years, 0.02234),
            Datum(2, 40, Years, 0.02233)]

        Settings.instance().evaluationDate = Date(21, February, 2017)

        helpers = RateHelperVector()
        index = FedFunds()

        helpers.append(
            DepositRateHelper(
                data[0].rate,
                Period(data[0].n, data[0].unit),
                index.fixingDays(),
                index.fixingCalendar(),
                index.businessDayConvention(),
                index.endOfMonth(),
                index.dayCounter()))

        for i in range(1, len(data)):
            helpers.append(
                OISRateHelper(
                    data[i].settlementDays,
                    Period(data[i].n, data[i].unit),
                    QuoteHandle(SimpleQuote(data[i].rate)),
                    index,
                    YieldTermStructureHandle(),
                    false, 2,
                    Following, Annual, Calendar(), Period(0, Days), 0.0,
                    # this bootstrap fails with the default LastRelevantDate choice
                    Pillar.MaturityDate))

        # curve = PiecewiseYieldCurve<Discount, LogCubic>(
        #     0, UnitedStates(UnitedStates.GovernmentBond),
        #     helpers, Actual365Fixed(), MonotonicLogCubic())
        curve = PiecewiseLogCubicDiscount(
            0, UnitedStates(UnitedStates.GovernmentBond),
            helpers, Actual365Fixed(), MonotonicLogCubic())

        # BOOST_CHECK_NO_THROW(curve.discount(1.0))
        try:
            curve.discount(1.0)
        except Exception as e:
            NO_THROW = false
            self.assertTrue(NO_THROW)

    def _testBootstrap(self,
                       telescopicValueDates,
                       averagingMethod,
                       tolerance=1.0e-8):

        vars = CommonVars()

        paymentLag = 2

        eoniaHelpers = RateHelperVector()

        euribor3m = Euribor3M()
        eonia = Eonia()

        for i in depositData:
            rate = 0.01 * i.rate
            simple = SimpleQuote(rate)
            quote = simple
            term = Period(i.n, i.unit)
            helper = DepositRateHelper(
                QuoteHandle(quote), term, i.settlementDays,
                euribor3m.fixingCalendar(),
                euribor3m.businessDayConvention(),
                euribor3m.endOfMonth(), euribor3m.dayCounter())

            if term <= Period(2, Days):
                eoniaHelpers.push_back(helper)

        for i in eoniaSwapData:
            rate = 0.01 * i.rate
            simple = SimpleQuote(rate)
            quote = simple
            term = Period(i.n, i.unit)
            helper = OISRateHelper(
                i.settlementDays,
                term,
                QuoteHandle(quote),
                eonia,
                YieldTermStructureHandle(),
                telescopicValueDates,
                paymentLag,
                Following,
                Annual,
                Calendar(),
                Period(0, Days),
                0.0,
                Pillar.LastRelevantDate,
                Date(),
                averagingMethod)
            eoniaHelpers.push_back(helper)

        eoniaTS = PiecewiseLogLinearDiscount(
            vars.today, eoniaHelpers, Actual365Fixed(), LogLinear())

        vars.eoniaTermStructure.linkTo(eoniaTS)

        # test curve consistency
        for i in eoniaSwapData:
            expected = i.rate / 100
            term = Period(i.n, i.unit)
            # test telescopic value dates (in bootstrap) against non telescopic value dates (swap here)
            swap = vars.makeSwap(
                term, 0.0, 0.0, false, NullDate(), paymentLag, averagingMethod)
            calculated = swap.fairRate()
            error = abs(expected - calculated)

            self.assertFalse(error > tolerance)
