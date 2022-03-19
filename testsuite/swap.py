import unittest
from utilities import *
from QuantLib import *
from math import log


class CommonVars(object):

    # utilities
    def __init__(self):
        self.type = Swap.Payer
        self.settlementDays = 2
        self.nominal = 100.0
        self.fixedConvention = Unadjusted
        self.floatingConvention = ModifiedFollowing
        self.fixedFrequency = Annual
        self.floatingFrequency = Semiannual
        self.fixedDayCount = Thirty360(Thirty360.BondBasis)
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.index = Euribor(Period(self.floatingFrequency), self.termStructure)
        self.calendar = self.index.fixingCalendar()
        self.today = self.calendar.adjust(Settings.instance().evaluationDate)
        self.settlement = self.calendar.advance(
            self.today, self.settlementDays, Days)
        self.termStructure.linkTo(
            flatRate(self.settlement, 0.05, Actual365Fixed()))
        self.backup = SavedSettings()

    def makeSwap(self,
                 length,
                 fixedRate,
                 floatingSpread,
                 rule=DateGeneration.Forward):
        maturity = self.calendar.advance(
            self.settlement, length, Years,
            self.floatingConvention)
        fixedSchedule = Schedule(
            self.settlement, maturity,
            Period(self.fixedFrequency),
            self.calendar, self.fixedConvention,
            self.fixedConvention, rule, false)
        floatSchedule = Schedule(
            self.settlement, maturity,
            Period(self.floatingFrequency),
            self.calendar, self.floatingConvention,
            self.floatingConvention, rule, false)
        swap = VanillaSwap(
            self.type, self.nominal,
            fixedSchedule, fixedRate, self.fixedDayCount,
            floatSchedule, self.index, floatingSpread,
            self.index.dayCounter())
        swap.setPricingEngine(
            DiscountingSwapEngine(self.termStructure))
        return swap


class SwapTest(unittest.TestCase):

    def testFairRate(self):
        TEST_MESSAGE("Testing vanilla-swap calculation of fair fixed rate...")

        vars = CommonVars()

        lengths = [1, 2, 5, 10, 20]
        spreads = [-0.001, -0.01, 0.0, 0.01, 0.001]

        for length in lengths:
            for spread in spreads:
                swap = vars.makeSwap(length, 0.0, spread)
                swap = vars.makeSwap(length, swap.fairRate(), spread)
                self.assertFalse(abs(swap.NPV()) > 1.0e-10)

    def testFairSpread(self):
        TEST_MESSAGE("Testing vanilla-swap calculation of "
                     "fair floating spread...")

        vars = CommonVars()

        lengths = [1, 2, 5, 10, 20]
        rates = [0.04, 0.05, 0.06, 0.07]

        for length in lengths:
            for j in rates:
                swap = vars.makeSwap(length, j, 0.0)
                swap = vars.makeSwap(length, j, swap.fairSpread())
                self.assertFalse(abs(swap.NPV()) > 1.0e-10)

    def testRateDependency(self):
        TEST_MESSAGE("Testing vanilla-swap dependency on fixed rate...")

        vars = CommonVars()

        lengths = [1, 2, 5, 10, 20]
        spreads = [-0.001, -0.01, 0.0, 0.01, 0.001]
        rates = [0.03, 0.04, 0.05, 0.06, 0.07]

        for length in lengths:
            for spread in spreads:
                # store the results for different rates...
                swap_values = DoubleVector()
                for rate in rates:
                    swap = vars.makeSwap(length, rate, spread)
                    swap_values.append(swap.NPV())

                # and check that they go the right way
                # it = adjacent_find(swap_values.begin(), swap_values.end(), less<Real>())
                # self.assertFalse (it != swap_values.end())
                it = 1
                while swap_values[it - 1] >= swap_values[it]:
                    it += 1
                    if it >= len(swap_values) - 1:
                        break
                self.assertFalse(it != len(swap_values) - 1)

    def testSpreadDependency(self):
        TEST_MESSAGE("Testing vanilla-swap dependency on floating spread...")

        vars = CommonVars()

        lengths = [1, 2, 5, 10, 20]
        rates = [0.04, 0.05, 0.06, 0.07]
        spreads = [
            -0.01, -0.002, -0.001, 0.0, 0.001, 0.002, 0.01]

        for length in lengths:
            for j in rates:
                # store the results for different spreads...
                swap_values = DoubleVector()
                for spread in spreads:
                    swap = vars.makeSwap(length, j, spread)
                    swap_values.append(swap.NPV())

                # and check that they go the right way
                # it = adjacent_find(swap_values.begin(), swap_values.end(), greater<Real>())
                # self.assertFalse (it != swap_values.end())
                it = 1
                while swap_values[it - 1] <= swap_values[it]:
                    it += 1
                    if it >= len(swap_values) - 1:
                        break
                self.assertFalse(it != len(swap_values) - 1)

    def testInArrears(self):
        TEST_MESSAGE("Testing in-arrears swap calculation...")

        vars = CommonVars()

        # See Hull, 4th ed., page 550
        # Note: the calculation in the book is wrong (work out the
        # adjustment and you'll get 0.05 + 0.000115 T1)

        maturity = vars.today + Period(5, Years)
        calendar = NullCalendar()
        schedule = Schedule(
            vars.today, maturity, Period(Annual), calendar,
            Following, Following,
            DateGeneration.Forward, false)
        dayCounter = SimpleDayCounter()
        nominals = DoubleVector(1, 100000000.0)
        index = IborIndex(
            "dummy", Period(1, Years), 0,
            EURCurrency(), calendar,
            Following, false, dayCounter,
            vars.termStructure)
        oneYear = 0.05
        r = log(1.0 + oneYear)
        vars.termStructure.linkTo(flatRate(vars.today, r, dayCounter))

        coupons = DoubleVector(1, oneYear)
        fixedLeg = FixedRateLeg(schedule)
        fixedLeg.withNotionals(nominals)
        fixedLeg.withCouponRates(coupons, dayCounter)
        fixedLeg = fixedLeg.makeLeg()

        gearings = DoubleVector()
        spreads = DoubleVector()
        fixingDays = 0

        capletVolatility = 0.22
        vol = OptionletVolatilityStructureHandle(
            ConstantOptionletVolatility(
                vars.today, NullCalendar(), Following,
                capletVolatility, dayCounter))
        pricer = BlackIborCouponPricer(vol)

        floatingLeg = IborLeg(schedule, index)
        floatingLeg.withNotionals(nominals)
        floatingLeg.withPaymentDayCounter(dayCounter)
        floatingLeg.withFixingDays(fixingDays)
        floatingLeg.withGearings(gearings)
        floatingLeg.withSpreads(spreads)
        floatingLeg.inArrears()
        floatingLeg = floatingLeg.makeLeg()
        setCouponPricer(floatingLeg, pricer)

        swap = Swap(floatingLeg, fixedLeg)
        swap.setPricingEngine(
            DiscountingSwapEngine(vars.termStructure))

        storedValue = -144813.0
        tolerance = 1.0

        self.assertFalse(abs(swap.NPV() - storedValue) > tolerance)

    def testCachedValue(self):
        TEST_MESSAGE("Testing vanilla-swap calculation against cached value...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        vars.today = Date(17, June, 2002)
        Settings.instance().evaluationDate = vars.today
        vars.settlement = vars.calendar.advance(
            vars.today, vars.settlementDays, Days)
        vars.termStructure.linkTo(
            flatRate(vars.settlement, 0.05, Actual365Fixed()))

        swap = vars.makeSwap(10, 0.06, 0.001)

        self.assertFalse(swap.numberOfLegs() != 2)

        cachedNPV = -5.872863313209 if usingAtParCoupons else -5.872342992212

        self.assertFalse(abs(swap.NPV() - cachedNPV) > 1.0e-11)

    def testThirdWednesdayAdjustment(self):
        TEST_MESSAGE("Testing third-Wednesday adjustment...")

        today = Date(16, September, 2015)
        Settings.instance().evaluationDate = today

        vars = CommonVars()

        swap = vars.makeSwap(
            1, 0.0, -0.001, DateGeneration.ThirdWednesdayInclusive)

        self.assertFalse(
            swap.floatingSchedule().startDate() != Date(16, September, 2015))

        self.assertFalse(
            swap.floatingSchedule().endDate() != Date(21, September, 2016))
