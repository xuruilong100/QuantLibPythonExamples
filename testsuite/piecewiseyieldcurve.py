import unittest
from utilities import *
from QuantLib import *
from copy import deepcopy


class Datum(object):
    def __init__(self,
                 n,
                 units,
                 rate):
        self.n = n
        self.units = units
        self.rate = rate


class BondDatum(object):
    def __init__(self,
                 n,
                 units,
                 length,
                 frequency,
                 coupon,
                 price):
        self.n = n
        self.units = units
        self.length = length
        self.frequency = frequency
        self.coupon = coupon
        self.price = price


depositData = [
    Datum(1, Weeks, 4.559),
    Datum(1, Months, 4.581),
    Datum(2, Months, 4.573),
    Datum(3, Months, 4.557),
    Datum(6, Months, 4.496),
    Datum(9, Months, 4.490)]

fraData = [
    Datum(1, Months, 4.581),
    Datum(2, Months, 4.573),
    Datum(3, Months, 4.557),
    Datum(6, Months, 4.496),
    Datum(9, Months, 4.490)]

immFutData = [
    Datum(1, Months, 4.581),
    Datum(2, Months, 4.573),
    Datum(3, Months, 4.557)]

asxFutData = [
    Datum(1, Months, 4.581),
    Datum(2, Months, 4.573),
    Datum(3, Months, 4.557)]

swapData = [
    Datum(1, Years, 4.54),
    Datum(2, Years, 4.63),
    Datum(3, Years, 4.75),
    Datum(4, Years, 4.86),
    Datum(5, Years, 4.99),
    Datum(6, Years, 5.11),
    Datum(7, Years, 5.23),
    Datum(8, Years, 5.33),
    Datum(9, Years, 5.41),
    Datum(10, Years, 5.47),
    Datum(12, Years, 5.60),
    Datum(15, Years, 5.75),
    Datum(20, Years, 5.89),
    Datum(25, Years, 5.95),
    Datum(30, Years, 5.96)]

bondData = [
    BondDatum(6, Months, 5, Semiannual, 4.75, 101.320),
    BondDatum(1, Years, 3, Semiannual, 2.75, 100.590),
    BondDatum(2, Years, 5, Semiannual, 5.00, 105.650),
    BondDatum(5, Years, 11, Semiannual, 5.50, 113.610),
    BondDatum(10, Years, 11, Semiannual, 3.75, 104.070)]

bmaData = [
    Datum(1, Years, 67.56),
    Datum(2, Years, 68.00),
    Datum(3, Years, 68.25),
    Datum(4, Years, 68.50),
    Datum(5, Years, 68.81),
    Datum(7, Years, 69.50),
    Datum(10, Years, 70.44),
    Datum(15, Years, 71.69),
    Datum(20, Years, 72.69),
    Datum(30, Years, 73.81)]


class CommonVars(object):

    # setup
    def __init__(self):
        # data
        self.backup = SavedSettings()
        self.calendar = TARGET()
        self.settlementDays = 2
        # self.today = self.calendar.adjust(Date.todaysDate())
        self.today = self.calendar.adjust(Date(16, Sep, 2015))
        Settings.instance().evaluationDate = self.today
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)
        self.fixedLegConvention = Unadjusted
        self.fixedLegFrequency = Annual
        self.fixedLegDayCounter = Thirty360(Thirty360.BondBasis)
        self.bondSettlementDays = 3
        self.bondDayCounter = ActualActual(ActualActual.ISDA)
        self.bondConvention = Following
        self.bondRedemption = 100.0
        self.bmaFrequency = Quarterly
        self.bmaConvention = Following
        self.bmaDayCounter = ActualActual(ActualActual.ISDA)
        self.termStructure = None
        self.deposits = len(depositData)
        self.fras = len(fraData)
        self.immFuts = len(immFutData)
        self.asxFuts = len(asxFutData)
        self.swaps = len(swapData)
        self.bonds = len(bondData)
        self.bmas = len(bmaData)

        # market elements
        self.rates = []
        self.fraRates = []
        self.immFutPrices = []
        self.asxFutPrices = []
        self.prices = []
        self.fractions = []
        for i in range(self.deposits):
            self.rates.append(
                SimpleQuote(depositData[i].rate / 100))

        for i in range(self.swaps):
            self.rates.append(
                SimpleQuote(swapData[i].rate / 100))

        for i in range(self.fras):
            self.fraRates.append(
                SimpleQuote(fraData[i].rate / 100))

        for i in range(self.bonds):
            self.prices.append(
                SimpleQuote(bondData[i].price))

        for i in range(self.immFuts):
            self.immFutPrices.append(
                SimpleQuote(100.0 - immFutData[i].rate))

        for i in range(self.asxFuts):
            self.asxFutPrices.append(
                SimpleQuote(100.0 - asxFutData[i].rate))

        for i in range(self.bmas):
            self.fractions.append(
                SimpleQuote(bmaData[i].rate / 100))

        # rate helpers
        self.instruments = RateHelperVector(self.deposits + self.swaps)
        self.fraHelpers = RateHelperVector(self.fras)
        self.immFutHelpers = RateHelperVector(self.immFuts)
        self.asxFutHelpers = RateHelperVector()
        self.bondHelpers = RateHelperVector(self.bonds)
        self.schedules = []
        self.bmaHelpers = RateHelperVector(self.bmas)

        euribor6m = Euribor6M()
        for i in range(self.deposits):
            r = QuoteHandle(self.rates[i])
            self.instruments[i] = DepositRateHelper(
                r,
                Euribor(
                    Period(depositData[i].n, depositData[i].units)))

        for i in range(self.swaps):
            r = QuoteHandle(self.rates[i + self.deposits])
            self.instruments[i + self.deposits] = SwapRateHelper(
                r, Period(swapData[i].n, swapData[i].units),
                self.calendar,
                self.fixedLegFrequency, self.fixedLegConvention,
                self.fixedLegDayCounter, euribor6m)

        # ifdef QL_USE_INDEXED_COUPON
        # useIndexedFra = false
        # else
        useIndexedFra = true
        # endif

        euribor3m = Euribor3M()
        for i in range(self.fras):
            r = QuoteHandle(self.fraRates[i])
            self.fraHelpers[i] = FraRateHelper(
                r, fraData[i].n,
                fraData[i].n + 3,
                euribor3m.fixingDays(),
                euribor3m.fixingCalendar(),
                euribor3m.businessDayConvention(),
                euribor3m.endOfMonth(),
                euribor3m.dayCounter(),
                Pillar.LastRelevantDate,
                Date(),
                useIndexedFra)

        immDate = Date()
        for i in range(self.immFuts):
            r = QuoteHandle(self.immFutPrices[i])
            immDate = IMM.nextDate(immDate, false)
            # if the fixing is before the evaluation date, we
            # just jump forward by one future maturity
            if euribor3m.fixingDate(immDate) < Settings.instance().evaluationDate:
                immDate = IMM.nextDate(immDate, false)
            self.immFutHelpers[i] = FuturesRateHelper(
                r, immDate, euribor3m, QuoteHandle(),
                Futures.IMM)

        asxDate = Date()
        for i in range(self.asxFuts):
            r = QuoteHandle(self.asxFutPrices[i])
            asxDate = ASX.nextDate(asxDate, false)
            # if the fixing is before the evaluation date, we
            # just jump forward by one future maturity
            if euribor3m.fixingDate(asxDate) < Settings.instance().evaluationDate:
                asxDate = ASX.nextDate(asxDate, false)
            if euribor3m.fixingCalendar().isBusinessDay(asxDate):
                self.asxFutHelpers.append(
                    FuturesRateHelper(
                        r, asxDate, euribor3m,
                        QuoteHandle(), Futures.ASX))

        for i in range(self.bonds):
            p = QuoteHandle(self.prices[i])
            maturity = self.calendar.advance(self.today, bondData[i].n, bondData[i].units)
            issue = self.calendar.advance(maturity, -bondData[i].length, Years)
            coupons = DoubleVector(1, bondData[i].coupon / 100.0)
            self.schedules.append(Schedule(
                issue, maturity,
                Period(bondData[i].frequency),
                self.calendar,
                self.bondConvention, self.bondConvention,
                DateGeneration.Backward, false))
            self.bondHelpers[i] = FixedRateBondHelper(
                p,
                self.bondSettlementDays,
                self.bondRedemption, self.schedules[i],
                coupons, self.bondDayCounter,
                self.bondConvention,
                self.bondRedemption, issue)


# helper classes for testGlobalBootstrap() below:

# functor returning the additional error terms for the cost function
class additionalErrors(object):
    def __init__(self,
                 additionalHelpers):
        self.additionalHelpers = additionalHelpers

    def __call__(self):
        errors = Array(5)
        a = self.additionalHelpers[0].impliedQuote()
        b = self.additionalHelpers[6].impliedQuote()
        for k in range(5):
            errors[k] = (5.0 - k) / 6.0 * a + (1.0 + k) / 6.0 * b - \
                        self.additionalHelpers[1 + k].impliedQuote()

        return errors


# functor returning additional dates used in the bootstrap
class additionalDates(object):
    def __init__(self):
        pass

    def __call__(self):
        settl = TARGET().advance(
            Settings.instance().evaluationDate, Period(2, Days))
        dates = DateVector()
        for i in range(5):
            dates.append(TARGET().advance(settl, Period(1 + i, Months)))
        return dates


class PiecewiseYieldCurveTest(unittest.TestCase):

    @unittest.skip('unstable')
    def testLogCubicDiscountConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of piecewise-log-cubic discount curve...")

        vars = CommonVars()

        # self.testCurveConsistency<Discount, LogCubic, IterativeBootstrap>(vars, MonotonicLogCubic())
        self._testCurveConsistency(
            PiecewiseLogCubicDiscount, PiecewiseLogCubicDiscount, vars, MonotonicLogCubic())
        # self.testBMACurveConsistency<Discount, LogCubic, IterativeBootstrap>(vars, MonotonicLogCubic())
        self._testBMACurveConsistency(
            PiecewiseLogCubicDiscount, vars, MonotonicLogCubic())

        IndexManager.instance().clearHistories()

    def testLogLinearDiscountConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of piecewise-log-linear discount curve...")

        vars = CommonVars()

        # self.testCurveConsistency<Discount, LogLinear, IterativeBootstrap>(vars)
        self._testCurveConsistency(
            PiecewiseLogLinearDiscount, PiecewiseLogLinearDiscount, vars, LogLinear())
        # self.testBMACurveConsistency<Discount, LogLinear, IterativeBootstrap>(vars)
        self._testBMACurveConsistency(
            PiecewiseLogLinearDiscount, vars, LogLinear())

        IndexManager.instance().clearHistories()

    def testLinearDiscountConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of piecewise-linear discount curve...")

        vars = CommonVars()

        # self._testCurveConsistency < Discount, Linear, IterativeBootstrap > (vars)
        self._testCurveConsistency(
            PiecewiseLinearDiscount, PiecewiseLinearDiscount, vars, Linear())
        # self._testBMACurveConsistency < Discount, Linear, IterativeBootstrap > (vars)
        self._testBMACurveConsistency(
            PiecewiseLinearDiscount, vars, Linear())

        IndexManager.instance().clearHistories()

    def testLinearZeroConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of piecewise-linear zero-yield curve...")

        vars = CommonVars()

        # self._testCurveConsistency < ZeroYield, Linear, IterativeBootstrap > (vars)
        self._testCurveConsistency(
            PiecewiseLinearZeroYield, PiecewiseLinearZeroYield, vars, Linear())
        # self._testBMACurveConsistency < ZeroYield, Linear, IterativeBootstrap > (vars)
        self._testBMACurveConsistency(
            PiecewiseLinearZeroYield, vars, Linear())

        IndexManager.instance().clearHistories()

    def testSplineZeroConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of piecewise-cubic zero-yield curve...")

        vars = CommonVars()

        # self._testCurveConsistency < ZeroYield, Cubic, IterativeBootstrap > (
        #     vars,
        #     Cubic(CubicInterpolation.Spline, true,
        #         CubicInterpolation.SecondDerivative, 0.0,
        #         CubicInterpolation.SecondDerivative, 0.0))
        self._testCurveConsistency(
            PiecewiseCubicZeroYield,
            PiecewiseCubicZeroYield,
            vars,
            Cubic(CubicInterpolation.Spline, true,
                  CubicInterpolation.SecondDerivative, 0.0,
                  CubicInterpolation.SecondDerivative, 0.0))
        # self._testBMACurveConsistency < ZeroYield, Cubic, IterativeBootstrap > (
        #     vars,
        #     Cubic(CubicInterpolation.Spline, true,
        #         CubicInterpolation.SecondDerivative, 0.0,
        #         CubicInterpolation.SecondDerivative, 0.0))
        self._testBMACurveConsistency(
            PiecewiseCubicZeroYield,
            vars,
            Cubic(CubicInterpolation.Spline, true,
                  CubicInterpolation.SecondDerivative, 0.0,
                  CubicInterpolation.SecondDerivative, 0.0))

        IndexManager.instance().clearHistories()

    def testLinearForwardConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of piecewise-linear forward-rate curve...")

        vars = CommonVars()

        # self._testCurveConsistency < ForwardRate, Linear, IterativeBootstrap > (vars)
        self._testCurveConsistency(
            PiecewiseLinearForward, PiecewiseLinearForward, vars, Linear())
        # self._testBMACurveConsistency < ForwardRate, Linear, IterativeBootstrap > (vars)
        self._testBMACurveConsistency(
            PiecewiseLinearForward, vars, Linear())

        IndexManager.instance().clearHistories()

    def testFlatForwardConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of piecewise-flat forward-rate curve...")

        vars = CommonVars()

        # self._testCurveConsistency < ForwardRate, BackwardFlat, IterativeBootstrap > (vars)
        self._testCurveConsistency(
            PiecewiseBackwardFlatForward, PiecewiseBackwardFlatForward, vars, BackwardFlat())
        # self._testBMACurveConsistency < ForwardRate, BackwardFlat, IterativeBootstrap > (vars)
        self._testBMACurveConsistency(
            PiecewiseBackwardFlatForward, vars, BackwardFlat())

        IndexManager.instance().clearHistories()

    @unittest.skip('unstable')
    def testSplineForwardConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of piecewise-cubic forward-rate curve...")

        vars = CommonVars()

        # self._testCurveConsistency < ForwardRate, Cubic, IterativeBootstrap > (
        #     vars,
        #     Cubic(CubicInterpolation.Spline, true,
        #         CubicInterpolation.SecondDerivative, 0.0,
        #         CubicInterpolation.SecondDerivative, 0.0))
        self._testCurveConsistency(
            PiecewiseCubicForward,
            PiecewiseCubicForward,
            vars,
            Cubic(CubicInterpolation.Spline, true,
                  CubicInterpolation.SecondDerivative, 0.0,
                  CubicInterpolation.SecondDerivative, 0.0))
        # self._testBMACurveConsistency < ForwardRate, Cubic, IterativeBootstrap > (
        #     vars,
        #     Cubic(CubicInterpolation.Spline, true,
        #         CubicInterpolation.SecondDerivative, 0.0,
        #         CubicInterpolation.SecondDerivative, 0.0))
        self._testBMACurveConsistency(
            PiecewiseCubicForward,
            vars,
            Cubic(CubicInterpolation.Spline, true,
                  CubicInterpolation.SecondDerivative, 0.0,
                  CubicInterpolation.SecondDerivative, 0.0))

        IndexManager.instance().clearHistories()

    def testConvexMonotoneForwardConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of convex monotone forward-rate curve...")

        vars = CommonVars()

        # self._testCurveConsistency < ForwardRate, ConvexMonotone, IterativeBootstrap > (vars)
        self._testCurveConsistency(
            PiecewiseConvexMonotoneForward, PiecewiseConvexMonotoneForward, vars, ConvexMonotone())
        # self._testBMACurveConsistency < ForwardRate, ConvexMonotone, IterativeBootstrap > (vars)
        self._testBMACurveConsistency(
            PiecewiseConvexMonotoneForward, vars, ConvexMonotone())

        IndexManager.instance().clearHistories()

    def testLocalBootstrapConsistency(self):
        TEST_MESSAGE(
            "Testing consistency of local-bootstrap algorithm...")

        vars = CommonVars()

        # self._testCurveConsistency < ForwardRate, ConvexMonotone, LocalBootstrap > (vars, ConvexMonotone(), 1.0e-6)
        self._testCurveConsistency(
            PiecewiseConvexMonotoneForward, PiecewiseConvexMonotoneForward, vars, ConvexMonotone(), 1.0e-6)
        # self._testBMACurveConsistency < ForwardRate, ConvexMonotone, LocalBootstrap > (vars, ConvexMonotone(), 1.0e-7)
        self._testBMACurveConsistency(
            PiecewiseConvexMonotoneForward, vars, ConvexMonotone(), 1.0e-7)

        IndexManager.instance().clearHistories()

    def testObservability(self):
        TEST_MESSAGE("Testing observability of piecewise yield curve...")

        vars = CommonVars()

        # vars.termStructure = PiecewiseYieldCurve<Discount, LogLinear>(
        vars.termStructure = PiecewiseLogLinearDiscount(
            vars.settlementDays,
            vars.calendar,
            vars.instruments,
            Actual360(),
            LogLinear())
        f = Flag()
        f.registerWith(vars.termStructure)

        for i in range(vars.deposits + vars.swaps):
            testTime = Actual360().yearFraction(
                vars.settlement, vars.instruments[i].pillarDate())
            discount = vars.termStructure.discount(testTime)
            f.lower()
            vars.rates[i].setValue(vars.rates[i].value() * 1.01)
            self.assertFalse(not f.isUp())
            self.assertFalse(
                vars.termStructure.discount(testTime, true) == discount)

            vars.rates[i].setValue(vars.rates[i].value() / 1.01)

        vars.termStructure.maxDate()
        f.lower()
        Settings.instance().evaluationDate = vars.calendar.advance(vars.today, 15, Days)
        self.assertFalse(not f.isUp())

        f.lower()
        Settings.instance().evaluationDate = vars.today
        self.assertFalse(f.isUp())

        IndexManager.instance().clearHistories()

    def testLiborFixing(self):
        TEST_MESSAGE(
            "Testing use of today's LIBOR fixings in swap curve...")

        vars = CommonVars()

        swapHelpers = RateHelperVector(vars.swaps)
        euribor6m = Euribor6M()

        for i in range(vars.swaps):
            r = QuoteHandle(vars.rates[i + vars.deposits])
            swapHelpers[i] = SwapRateHelper(
                r, Period(swapData[i].n, swapData[i].units),
                vars.calendar,
                vars.fixedLegFrequency, vars.fixedLegConvention,
                vars.fixedLegDayCounter, euribor6m)

        # vars.termStructure = PiecewiseYieldCurve<Discount, LogLinear>(
        vars.termStructure = PiecewiseLogLinearDiscount(
            vars.settlement,
            swapHelpers,
            Actual360(),
            LogLinear())

        curveHandle = YieldTermStructureHandle(vars.termStructure)

        index = Euribor6M(curveHandle)
        for i in range(vars.swaps):
            tenor = Period(swapData[i].n, swapData[i].units)

            swap = MakeVanillaSwap(tenor, index, 0.0)
            swap.withEffectiveDate(vars.settlement)
            swap.withFixedLegDayCount(vars.fixedLegDayCounter)
            swap.withFixedLegTenor(Period(vars.fixedLegFrequency))
            swap.withFixedLegConvention(vars.fixedLegConvention)
            swap.withFixedLegTerminationDateConvention(vars.fixedLegConvention)
            swap = swap.makeVanillaSwap()

            expectedRate = swapData[i].rate / 100
            estimatedRate = swap.fairRate()
            tolerance = 1.0e-9
            self.assertFalse(abs(expectedRate - estimatedRate) > tolerance)

        f = Flag()
        f.registerWith(vars.termStructure)
        f.lower()

        index.addFixing(vars.today, 0.0425)

        self.assertFalse(not f.isUp())

        for i in range(vars.swaps):
            tenor = Period(swapData[i].n, swapData[i].units)

            swap = MakeVanillaSwap(tenor, index, 0.0)
            swap.withEffectiveDate(vars.settlement)
            swap.withFixedLegDayCount(vars.fixedLegDayCounter)
            swap.withFixedLegTenor(Period(vars.fixedLegFrequency))
            swap.withFixedLegConvention(vars.fixedLegConvention)
            swap.withFixedLegTerminationDateConvention(vars.fixedLegConvention)
            swap = swap.makeVanillaSwap()

            expectedRate = swapData[i].rate / 100
            estimatedRate = swap.fairRate()
            tolerance = 1.0e-9
            self.assertFalse(abs(expectedRate - estimatedRate) > tolerance)

        IndexManager.instance().clearHistories()

    def testJpyLibor(self):
        TEST_MESSAGE(
            "Testing bootstrap over JPY LIBOR swaps...")

        vars = CommonVars()

        vars.today = Date(4, October, 2007)
        Settings.instance().evaluationDate = vars.today

        vars.calendar = Japan()
        vars.settlement = vars.calendar.advance(
            vars.today, vars.settlementDays, Days)

        # market elements
        vars.rates = []
        for i in range(vars.swaps):
            vars.rates.append(SimpleQuote(
                swapData[i].rate / 100))

        # rate helpers
        vars.instruments = RateHelperVector(vars.swaps)

        index = JPYLibor(Period(6, Months))
        for i in range(vars.swaps):
            r = QuoteHandle(vars.rates[i])
            vars.instruments[i] = SwapRateHelper(
                r, Period(swapData[i].n, swapData[i].units),
                vars.calendar,
                vars.fixedLegFrequency, vars.fixedLegConvention,
                vars.fixedLegDayCounter, index)

        # vars.termStructure = PiecewiseYieldCurve<Discount, LogLinear>(
        vars.termStructure = PiecewiseLogLinearDiscount(
            vars.settlement, vars.instruments,
            Actual360(), LogLinear())

        curveHandle = RelinkableYieldTermStructureHandle()
        curveHandle.linkTo(vars.termStructure)

        # check swaps
        jpylibor6m = JPYLibor(Period(6, Months), curveHandle)
        for i in range(vars.swaps):
            tenor = Period(swapData[i].n, swapData[i].units)

            swap = MakeVanillaSwap(tenor, jpylibor6m, 0.0)
            swap.withEffectiveDate(vars.settlement)
            swap.withFixedLegDayCount(vars.fixedLegDayCounter)
            swap.withFixedLegTenor(Period(vars.fixedLegFrequency))
            swap.withFixedLegConvention(vars.fixedLegConvention)
            swap.withFixedLegTerminationDateConvention(vars.fixedLegConvention)
            swap.withFixedLegCalendar(vars.calendar)
            swap.withFloatingLegCalendar(vars.calendar)
            swap = swap.makeVanillaSwap()

            expectedRate = swapData[i].rate / 100
            estimatedRate = swap.fairRate()
            error = abs(expectedRate - estimatedRate)
            tolerance = 1.0e-9

            self.assertFalse(error > tolerance)

        IndexManager.instance().clearHistories()

    @unittest.skip("can not deep copy a SwigPyObject")
    def testDiscountCopy(self):
        TEST_MESSAGE("Testing copying of discount curve...")

        vars = CommonVars()
        # self._testCurveCopy<Discount, LogLinear>(vars)
        self._testCurveCopy(
            PiecewiseLogLinearDiscount, vars, LogLinear())

        IndexManager.instance().clearHistories()

    @unittest.skip("can not deep copy a SwigPyObject")
    def testForwardCopy(self):
        TEST_MESSAGE("Testing copying of forward-rate curve...")

        vars = CommonVars()
        # testCurveCopy<ForwardRate, BackwardFlat>(vars)
        self._testCurveCopy(
            PiecewiseBackwardFlatForward, vars, BackwardFlat())

        IndexManager.instance().clearHistories()

    @unittest.skip("can not deep copy a SwigPyObject")
    def testZeroCopy(self):
        TEST_MESSAGE("Testing copying of zero-rate curve...")

        vars = CommonVars()
        # testCurveCopy<ZeroYield, Linear>(vars)
        self._testCurveCopy(
            PiecewiseLinearZeroYield, vars, Linear())

        IndexManager.instance().clearHistories()

    def testSwapRateHelperLastRelevantDate(self):
        TEST_MESSAGE("Testing SwapRateHelper last relevant date...")

        backup = SavedSettings()
        Settings.instance().evaluationDate = Date(22, Dec, 2016)
        today = Settings.instance().evaluationDate

        flat3m = YieldTermStructureHandle(
            FlatForward(
                today, QuoteHandle(SimpleQuote(0.02)), Actual365Fixed()))
        usdLibor3m = USDLibor(Period(3, Months), flat3m)

        # note that the calendar should be US+UK here actually, but technically it should also work with
        # the US calendar only
        helper = SwapRateHelper(
            0.02, Period(50, Years),
            UnitedStates(UnitedStates.GovernmentBond),
            Semiannual, ModifiedFollowing,
            Thirty360(Thirty360.BondBasis), usdLibor3m)

        # curve=PiecewiseYieldCurve<Discount, LogLinear> (today, RateHelperVector(1, helper), Actual365Fixed())
        curve = PiecewiseLogLinearDiscount(
            today, RateHelperVector(1, helper), Actual365Fixed(), LogLinear())
        # BOOST_CHECK_NO_THROW(curve.discount(1.0))
        try:
            curve.discount(1.0)
        except Exception as e:
            NO_THROW = False
            self.assertTrue(NO_THROW)

    def testSwapRateHelperSpotDate(self):
        TEST_MESSAGE("Testing SwapRateHelper spot date...")

        backup = SavedSettings()

        usdLibor3m = USDLibor(Period(3, Months))

        helper = SwapRateHelper(
            0.02, Period(5, Years),
            UnitedStates(UnitedStates.GovernmentBond),
            Semiannual, ModifiedFollowing,
            Thirty360(Thirty360.BondBasis), usdLibor3m)

        Settings.instance().evaluationDate = Date(11, October, 2019)

        # Advancing 2 days on the US calendar would yield October 16th (because October 14th
        # is Columbus day), but the LIBOR spot is calculated advancing on the UK calendar,
        # resulting in October 15th which is also a business day for the US calendar.
        expected = Date(15, October, 2019)
        calculated = helper.swap().startDate()
        self.assertFalse(calculated != expected)

        # Settings.instance().evaluationDate = Date(1, July, 2020)

        # TODO: July 3rd is holiday in the US, but not for LIBOR purposes.  This should probably
        # be considered when building the schedule.
        # expected = Date(3, July, 2020)
        # calculated = helper.swap().startDate()
        # if (calculated != expected)
        #     BOOST_ERROR("expected spot date: " << expected << "\n"
        #                 "calculated:         " << calculated)

    # This regression test didn't work with indexed coupons anyway.
    @unittest.skipUnless(
        IborCouponSettings.instance().usingAtParCoupons(),
        "This regression test didn't work with indexed coupons anyway.")
    def testBadPreviousCurve(self):
        TEST_MESSAGE("Testing bootstrap starting from bad guess...")

        backup = SavedSettings()

        data = [
            Datum(1, Weeks, -0.003488),
            Datum(2, Weeks, -0.0033),
            Datum(6, Months, -0.00339),
            Datum(2, Years, -0.00336),
            Datum(8, Years, 0.00302),
            Datum(50, Years, 0.01185)]

        helpers = RateHelperVector()
        euribor1m = Euribor1M()
        for i in data:
            helpers.append(SwapRateHelper(
                i.rate, Period(i.n, i.units), TARGET(), Monthly, Unadjusted,
                Thirty360(Thirty360.BondBasis), euribor1m))

        today = Date(12, October, 2017)
        test_date = Date(16, December, 2016)

        Settings.instance().evaluationDate = today

        # curve =PiecewiseYieldCurve<ForwardRate, BackwardFlat> (
        curve = PiecewiseBackwardFlatForward(
            test_date, helpers, Actual360(), BackwardFlat())

        # force bootstrap on today's date, so we have a previous curve...
        curve.discount(1.0)

        # ...then move to a date where the previous curve is a bad guess.
        Settings.instance().evaluationDate = test_date

        h = RelinkableYieldTermStructureHandle()
        h.linkTo(curve)

        index = Euribor1M(h)
        for i in data:
            tenor = Period(i.n, i.units)

            swap = MakeVanillaSwap(tenor, index, 0.0)
            swap.withFixedLegDayCount(Thirty360(Thirty360.BondBasis))
            swap.withFixedLegTenor(Period(1, Months))
            swap.withFixedLegConvention(Unadjusted)
            swap = swap.makeVanillaSwap()
            swap.setPricingEngine(DiscountingSwapEngine(h))

            expectedRate = i.rate
            estimatedRate = swap.fairRate()
            error = abs(expectedRate - estimatedRate)
            tolerance = 1.0e-9
            self.assertFalse(error > tolerance)

    def testConstructionWithExplicitBootstrap(self):
        TEST_MESSAGE("Testing that construction with an explicit bootstrap succeeds...")

        vars = CommonVars()

        # With an explicit IterativeBootstrap object
        # typedef PiecewiseYieldCurve<ForwardRate, Linear, IterativeBootstrap> PwLinearForward
        PwLinearForward = PiecewiseLinearForward
        yts = PwLinearForward(
            vars.settlement, vars.instruments, Actual360(), Linear(),
            IterativeBootstrap())

        # Check anything to show that the construction succeeded
        # BOOST_CHECK_NO_THROW(yts.discount(1.0, true))
        try:
            yts.discount(1.0, true)
        except Exception as e:
            NO_THROW = False
            self.assertTrue(NO_THROW)

        # With an explicit LocalBootstrap object
        # typedef PiecewiseYieldCurve<ForwardRate, ConvexMonotone, LocalBootstrap> PwCmForward
        PwCmForward = LocalPiecewiseConvexMonotoneForward
        yts = PwCmForward(
            vars.settlement, vars.instruments, Actual360(),
            ConvexMonotone(), LocalBootstrap())

        # BOOST_CHECK_NO_THROW(yts.discount(1.0, true))
        try:
            yts.discount(1.0, true)
        except Exception as e:
            NO_THROW = False
            self.assertTrue(NO_THROW)

        IndexManager.instance().clearHistories()

    def testLargeRates(self):
        TEST_MESSAGE("Testing bootstrap with large input rates...")

        backup = SavedSettings()

        data = [
            Datum(1, Weeks, 2.418633),
            Datum(2, Weeks, 1.361540),
            Datum(3, Weeks, 1.195362),
            Datum(1, Months, 0.829009)]

        helpers = RateHelperVector()
        for i in data:
            helpers.append(DepositRateHelper(
                i.rate, Period(i.n, i.units), 0,
                WeekendsOnly(), Following, false, Actual360()))

        today = Date(12, October, 2017)

        Settings.instance().evaluationDate = today

        accuracy = NullReal()  # use the default
        minValue = NullReal()  # use the default
        maxValue = 3.0  # override

        # typedef PiecewiseYieldCurve<ForwardRate, BackwardFlat> PiecewiseCurve
        PiecewiseCurve = PiecewiseBackwardFlatForward
        curve = PiecewiseCurve(
            today, helpers, Actual360(), BackwardFlat(),
            IterativeBootstrap(accuracy, minValue, maxValue))

        # force bootstrap and check it worked
        curve.discount(0.01)
        # BOOST_CHECK_NO_THROW(curve.discount(0.01))
        try:
            curve.discount(0.01)
        except Exception as e:
            NO_THROW = False
            self.assertTrue(NO_THROW)

    @unittest.skip("skip testGlobalBootstrap")
    def testGlobalBootstrap(self):
        TEST_MESSAGE("Testing global bootstrap...")

        backup = SavedSettings()

        today = Date(26, Sep, 2019)
        Settings.instance().evaluationDate = today

        # market rates
        refMktRate = [
            -0.373, -0.388, -0.402, -0.418, -0.431, -0.441, -0.45,
            -0.457, -0.463, -0.469, -0.461, -0.463, -0.479, -0.4511,
            -0.45418, -0.439, -0.4124, -0.37703, -0.3335, -0.28168, -0.22725,
            -0.1745, -0.12425, -0.07746, 0.0385, 0.1435, 0.17525, 0.17275,
            0.1515, 0.1225, 0.095, 0.0644]

        # expected outputs
        refDate = [
            Date(31, Mar, 2020), Date(30, Apr, 2020), Date(29, May, 2020), Date(30, Jun, 2020),
            Date(31, Jul, 2020), Date(31, Aug, 2020), Date(30, Sep, 2020), Date(30, Oct, 2020),
            Date(30, Nov, 2020), Date(31, Dec, 2020), Date(29, Jan, 2021), Date(26, Feb, 2021),
            Date(31, Mar, 2021), Date(30, Sep, 2021), Date(30, Sep, 2022), Date(29, Sep, 2023),
            Date(30, Sep, 2024), Date(30, Sep, 2025), Date(30, Sep, 2026), Date(30, Sep, 2027),
            Date(29, Sep, 2028), Date(28, Sep, 2029), Date(30, Sep, 2030), Date(30, Sep, 2031),
            Date(29, Sep, 2034), Date(30, Sep, 2039), Date(30, Sep, 2044), Date(30, Sep, 2049),
            Date(30, Sep, 2054), Date(30, Sep, 2059), Date(30, Sep, 2064), Date(30, Sep, 2069)]

        refZeroRate = [
            -0.00373354, -0.00381005, -0.00387689, -0.00394124, -0.00407706, -0.00413633, -0.00411935,
            -0.00416370, -0.00420557, -0.00424431, -0.00427824, -0.00430977, -0.00434401, -0.00445243,
            -0.00448506, -0.00433690, -0.00407401, -0.00372752, -0.00330050, -0.00279139, -0.00225477,
            -0.00173422, -0.00123688, -0.00077237, 0.00038554, 0.00144248, 0.00175995, 0.00172873,
            0.00150782, 0.00121145, 0.000933912, 0.000628946]

        # build ql helpers
        helpers = RateHelperVector()
        index = Euribor(Period(6, Months))

        helpers.append(
            DepositRateHelper(
                refMktRate[0] / 100.0, Period(6, Months), 2,
                TARGET(), ModifiedFollowing, true, Actual360()))

        for i in range(12):
            helpers.append(
                FraRateHelper(refMktRate[1 + i] / 100.0, Period(i + 1, Months), index))

        swapTenors = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 25, 30, 35, 40, 45, 50]
        for i in range(19):
            helpers.append(
                SwapRateHelper(
                    refMktRate[13 + i] / 100.0, Period(swapTenors[i], Years),
                    TARGET(), Annual, ModifiedFollowing,
                    Thirty360(Thirty360.BondBasis), index))

        # global bootstrap constraints
        # vector<ext.shared_ptr<BootstrapHelper<YieldTermStructure> > > additionalHelpers
        additionalHelpers = []

        # set up the additional rate helpers we need in the cost function
        for i in range(7):
            additionalHelpers.append(
                FraRateHelper(-0.004, Period(12 + i, Months), index))

        # build curve with additional dates and constraints using a global bootstrapper
        # typedef PiecewiseYieldCurve<SimpleZeroYield, Linear, GlobalBootstrap> Curve
        Curve = GlobalPiecewiseLinearSimpleZeroYield
        a = additionalHelpers[0].impliedQuote()
        b = additionalHelpers[6].impliedQuote()
        curve = Curve(
            2, TARGET(), helpers, Actual365Fixed(),
            QuoteHandleVector(), DateVector(),
            Linear(),
            GlobalBootstrap(
                additionalHelpers, additionalDates()(),
                additionalErrors(additionalHelpers)(), 1.0e-12))
        curve.enableExtrapolation()

        # check expected pillar dates
        for i in range(len(refDate)):
            self.assertEqual(refDate[i], helpers[i].pillarDate())

        # check expected zero rates
        for i in range(len(refZeroRate)):
            # 0.01 basis points tolerance
            self.assertLess(
                abs(refZeroRate[i] - curve.zeroRate(refDate[i], Actual360(), Continuous).rate()),
                1E-6)

    def testIterativeBootstrapRetries(self):
        # This test attempts to build an ARS collateralised in USD curve as of 25 Sep 2019. Using the default
        # IterativeBootstrap with no retries, the yield curve building fails. Allowing retries, it expands the min and max
        # bounds and passes.

        TEST_MESSAGE("Testing iterative bootstrap with retries...")

        backup = SavedSettings()

        asof = Date(25, Sep, 2019)
        Settings.instance().evaluationDate = asof
        tsDayCounter = Actual365Fixed()

        # USD discount curve built out of FedFunds OIS swaps.
        usdCurveDates = [
            Date(25, Sep, 2019),
            Date(26, Sep, 2019),
            Date(8, Oct, 2019),
            Date(16, Oct, 2019),
            Date(22, Oct, 2019),
            Date(30, Oct, 2019),
            Date(2, Dec, 2019),
            Date(31, Dec, 2019),
            Date(29, Jan, 2020),
            Date(2, Mar, 2020),
            Date(31, Mar, 2020),
            Date(29, Apr, 2020),
            Date(29, May, 2020),
            Date(1, Jul, 2020),
            Date(29, Jul, 2020),
            Date(31, Aug, 2020),
            Date(30, Sep, 2020)]

        usdCurveDfs = [
            1.000000000,
            0.999940837,
            0.999309357,
            0.998894646,
            0.998574816,
            0.998162528,
            0.996552511,
            0.995197584,
            0.993915264,
            0.992530008,
            0.991329696,
            0.990179606,
            0.989005698,
            0.987751691,
            0.986703371,
            0.985495036,
            0.984413446]

        usdYts = YieldTermStructureHandle(
            # InterpolatedDiscountCurve<LogLinear> (
            DiscountCurve(
                usdCurveDates, usdCurveDfs, tsDayCounter))

        # USD/ARS forward points
        arsSpot = QuoteHandle(SimpleQuote(56.881))
        arsFwdPoints = [
            (Period(1, Months), 8.5157),
            (Period(2, Months), 12.7180),
            (Period(3, Months), 17.8310),
            (Period(6, Months), 30.3680),
            (Period(9, Months), 45.5520),
            (Period(1, Years), 60.7370)]

        # Create the FX swap rate helpers for the ARS in USD curve.
        instruments = []
        for it in arsFwdPoints:
            arsFwd = QuoteHandle(SimpleQuote(it[1]))
            instruments.append(
                FxSwapRateHelper(
                    arsFwd, arsSpot, it[0], 2,
                    UnitedStates(UnitedStates.GovernmentBond),
                    Following, false, true, usdYts))

        # Create the ARS in USD curve with the default IterativeBootstrap.
        # typedef PiecewiseYieldCurve<Discount, LogLinear, IterativeBootstrap> LLDFCurve
        LLDFCurve = PiecewiseLogLinearDiscount
        arsYts = LLDFCurve(asof, instruments, tsDayCounter, LogLinear())

        # USD/ARS spot date. The date on which we check the ARS discount curve.
        spotDate = Date(27, Sep, 2019)

        # Check that the ARS in USD curve throws by requesting a discount factor.
        # using piecewise_yield_curve_test.ExpErrorPred
        # BOOST_CHECK_EXCEPTION(arsYts.discount(spotDate), Error,
        #     ExpErrorPred("1st iteration: failed at 1st alive instrument"))
        # BOOST_CHECK_EXCEPTION(arsYts.discount(spotDate), Error)
        self.assertRaises(RuntimeError, arsYts.discount, spotDate)

        # Create the ARS in USD curve with an IterativeBootstrap allowing for 4 retries.
        ib = IterativeBootstrap(NullReal(), NullReal(), NullReal(), 5)
        arsYts = LLDFCurve(asof, instruments, tsDayCounter, LogLinear(), ib)

        # Check that the ARS in USD curve builds and populate the spot ARS discount factor.
        spotDfArs = 1.0
        # BOOST_REQUIRE_NO_THROW(spotDfArs = arsYts.discount(spotDate))
        try:
            spotDfArs = arsYts.discount(spotDate)
        except Exception as e:
            NO_THROW = False
            self.assertTrue(NO_THROW)

        # Additional dates and discount factors used in the final check i.e. that calculated 1Y FX forward equals input.
        oneYearFwdDate = Date(28, Sep, 2020)
        spotDfUsd = usdYts.discount(spotDate)
        oneYearDfUsd = usdYts.discount(oneYearFwdDate)

        # Given that the ARS in USD curve builds, check that the 1Y USD/ARS forward rate is as expected.
        oneYearDfArs = arsYts.discount(oneYearFwdDate)
        calcFwd = (spotDfArs * arsSpot.value() / oneYearDfArs) / (spotDfUsd / oneYearDfUsd)
        # expFwd = arsSpot.value() + arsFwdPoints.at(Period(1 , Years))
        expFwd = arsSpot.value() + arsFwdPoints[-1][1]
        self.assertLess(calcFwd - expFwd, 1e-10)

    def _testCurveConsistency(self,
                              PYCtib,
                              PYCti,
                              vars,
                              interpolator,
                              tolerance=1.0e-9):

        # vars.termStructure = PiecewiseYieldCurve<T, I, B>(vars.settlement, vars.instruments, Actual360(), interpolator)
        vars.termStructure = PYCtib(
            vars.settlement, vars.instruments, Actual360(), interpolator)

        curveHandle = RelinkableYieldTermStructureHandle()
        curveHandle.linkTo(vars.termStructure)

        # check deposits
        for i in range(vars.deposits):
            index = Euribor(
                Period(depositData[i].n, depositData[i].units), curveHandle)
            expectedRate = depositData[i].rate / 100
            estimatedRate = index.fixing(vars.today)

            self.assertFalse(abs(expectedRate - estimatedRate) > tolerance)

        # check swaps
        euribor6m = Euribor6M(curveHandle)
        for i in range(vars.swaps):
            tenor = Period(swapData[i].n, swapData[i].units)

            swap = MakeVanillaSwap(tenor, euribor6m, 0.0)
            swap.withEffectiveDate(vars.settlement)
            swap.withFixedLegDayCount(vars.fixedLegDayCounter)
            swap.withFixedLegTenor(Period(vars.fixedLegFrequency))
            swap.withFixedLegConvention(vars.fixedLegConvention)
            swap.withFixedLegTerminationDateConvention(vars.fixedLegConvention)
            swap = swap.makeVanillaSwap()

            expectedRate = swapData[i].rate / 100
            estimatedRate = swap.fairRate()
            error = abs(expectedRate - estimatedRate)
            self.assertFalse(error > tolerance)

        # check bonds
        # vars.termStructure = PiecewiseYieldCurve<T, I, B>(vars.settlement, vars.bondHelpers, Actual360(), interpolator)
        vars.termStructure = PYCtib(
            vars.settlement, vars.bondHelpers, Actual360(), interpolator)
        curveHandle.linkTo(vars.termStructure)

        for i in range(vars.bonds):
            maturity = vars.calendar.advance(
                vars.today,
                bondData[i].n,
                bondData[i].units)
            issue = vars.calendar.advance(
                maturity, -bondData[i].length, Years)
            coupons = DoubleVector(1, bondData[i].coupon / 100.0)

            bond = FixedRateBond(
                vars.bondSettlementDays, 100.0,
                vars.schedules[i], coupons,
                vars.bondDayCounter, vars.bondConvention,
                vars.bondRedemption, issue)

            bondEngine = DiscountingBondEngine(curveHandle)
            bond.setPricingEngine(bondEngine)

            expectedPrice = bondData[i].price
            estimatedPrice = bond.cleanPrice()
            error = abs(expectedPrice - estimatedPrice)
            self.assertFalse(error > tolerance)

        # check FRA
        # vars.termStructure = PiecewiseYieldCurve<T, I>(
        # vars.settlement, vars.fraHelpers, Actual360(), interpolator)
        vars.termStructure = PYCti(
            vars.settlement, vars.fraHelpers, Actual360(), interpolator)
        curveHandle.linkTo(vars.termStructure)

        # ifdef QL_USE_INDEXED_COUPON
        # useIndexedFra = false
        # else
        useIndexedFra = true
        # endif

        euribor3m = Euribor3M(curveHandle)
        for i in range(vars.fras):
            start = vars.calendar.advance(
                vars.settlement,
                fraData[i].n,
                fraData[i].units,
                euribor3m.businessDayConvention(),
                euribor3m.endOfMonth())
            self.assertTrue(fraData[i].units == Months)
            end = vars.calendar.advance(
                vars.settlement, 3 + fraData[i].n, Months,
                euribor3m.businessDayConvention(),
                euribor3m.endOfMonth())

            fra = ForwardRateAgreement(
                start, end, Position.Long,
                fraData[i].rate / 100, 100.0,
                euribor3m, curveHandle,
                useIndexedFra)

            expectedRate = fraData[i].rate / 100
            estimatedRate = fra.forwardRate().rate()
            self.assertFalse(abs(expectedRate - estimatedRate) > tolerance)

        # check immFuts
        # vars.termStructure = PiecewiseYieldCurve<T, I>(vars.settlement, vars.immFutHelpers, Actual360(), interpolator)
        vars.termStructure = PYCti(
            vars.settlement, vars.immFutHelpers, Actual360(), interpolator)
        curveHandle.linkTo(vars.termStructure)

        immStart = Date()
        for i in range(vars.immFuts):
            immStart = IMM.nextDate(immStart, false)
            # if the fixing is before the evaluation date, we
            # just jump forward by one future maturity
            if euribor3m.fixingDate(immStart) < Settings.instance().evaluationDate:
                immStart = IMM.nextDate(immStart, false)
            end = vars.calendar.advance(
                immStart, 3, Months,
                euribor3m.businessDayConvention(),
                euribor3m.endOfMonth())

            immFut = ForwardRateAgreement(
                immStart, end, Position.Long,
                immFutData[i].rate / 100, 100.0,
                euribor3m, curveHandle)
            expectedRate = immFutData[i].rate / 100
            estimatedRate = immFut.forwardRate().rate()
            self.assertFalse(abs(expectedRate - estimatedRate) > tolerance)

        # check asxFuts
        # vars.termStructure = PiecewiseYieldCurve<T, I>(vars.settlement, vars.asxFutHelpers, Actual360(), interpolator)
        vars.termStructure = PYCti(
            vars.settlement, vars.asxFutHelpers, Actual360(), interpolator)
        curveHandle.linkTo(vars.termStructure)

        asxStart = Date()
        for i in range(vars.asxFuts):
            asxStart = ASX.nextDate(asxStart, false)
            # if the fixing is before the evaluation date, we
            # just jump forward by one future maturity
            if euribor3m.fixingDate(asxStart) < Settings.instance().evaluationDate:
                asxStart = ASX.nextDate(asxStart, false)
            if euribor3m.fixingCalendar().isHoliday(asxStart):
                continue
            end = vars.calendar.advance(
                asxStart, 3, Months,
                euribor3m.businessDayConvention(),
                euribor3m.endOfMonth())

            asxFut = ForwardRateAgreement(
                asxStart, end, Position.Long,
                asxFutData[i].rate / 100, 100.0,
                euribor3m, curveHandle)
            expectedRate = asxFutData[i].rate / 100
            estimatedRate = asxFut.forwardRate().rate()
            self.assertFalse(abs(expectedRate - estimatedRate) > tolerance)

            # end checks

    # template <class T, class I, template<class C> class B>
    def _testBMACurveConsistency(self,
                                 PYCtib,
                                 vars,
                                 interpolator,
                                 tolerance=1.0e-9):

        # re-adjust settlement
        vars.calendar = JointCalendar(
            BMAIndex().fixingCalendar(),
            USDLibor(Period(3, Months)).fixingCalendar(),
            JoinHolidays)
        vars.today = vars.calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = vars.today
        vars.settlement = vars.calendar.advance(
            vars.today, vars.settlementDays, Days)

        riskFreeCurve = YieldTermStructureHandle(
            FlatForward(vars.settlement, 0.04, Actual360()))

        bmaIndex = BMAIndex()
        liborIndex = USDLibor(Period(3, Months), riskFreeCurve)
        for i in range(vars.bmas):
            f = QuoteHandle(vars.fractions[i])
            vars.bmaHelpers[i] = BMASwapRateHelper(
                f, Period(bmaData[i].n, bmaData[i].units),
                vars.settlementDays,
                vars.calendar,
                Period(vars.bmaFrequency),
                vars.bmaConvention,
                vars.bmaDayCounter,
                bmaIndex,
                liborIndex)

        w = vars.today.weekday()
        lastWednesday = vars.today - (w - 4) if w >= 4 else vars.today + (4 - w - 7)
        lastFixing = bmaIndex.fixingCalendar().adjust(lastWednesday)
        bmaIndex.addFixing(lastFixing, 0.03)

        # vars.termStructure = PiecewiseYieldCurve<T, I, B>(vars.today, vars.bmaHelpers, Actual360(), interpolator)
        vars.termStructure = PYCtib(
            vars.today, vars.bmaHelpers, Actual360(), interpolator)

        curveHandle = RelinkableYieldTermStructureHandle()
        curveHandle.linkTo(vars.termStructure)

        # check BMA swaps
        bma = BMAIndex(curveHandle)
        libor3m = USDLibor(Period(3, Months), riskFreeCurve)
        for i in range(vars.bmas):
            tenor = Period(bmaData[i].n, bmaData[i].units)

            bmaSchedule = MakeSchedule()
            bmaSchedule.fromDate(vars.settlement)
            bmaSchedule.to(vars.settlement + tenor)
            bmaSchedule.withFrequency(vars.bmaFrequency)
            bmaSchedule.withCalendar(bma.fixingCalendar())
            bmaSchedule.withConvention(vars.bmaConvention)
            bmaSchedule.backwards()
            bmaSchedule = bmaSchedule.makeSchedule()
            liborSchedule = MakeSchedule()
            liborSchedule.fromDate(vars.settlement)
            liborSchedule.to(vars.settlement + tenor)
            liborSchedule.withTenor(libor3m.tenor())
            liborSchedule.withCalendar(libor3m.fixingCalendar())
            liborSchedule.withConvention(libor3m.businessDayConvention())
            liborSchedule.endOfMonth(libor3m.endOfMonth())
            liborSchedule.backwards()
            liborSchedule = liborSchedule.makeSchedule()

            swap = BMASwap(
                Swap.Payer, 100.0,
                liborSchedule, 0.75, 0.0,
                libor3m, libor3m.dayCounter(),
                bmaSchedule, bma, vars.bmaDayCounter)
            swap.setPricingEngine(
                DiscountingSwapEngine(libor3m.forwardingTermStructure()))

            expectedFraction = bmaData[i].rate / 100
            estimatedFraction = swap.fairLiborFraction()
            error = abs(expectedFraction - estimatedFraction)
            self.assertFalse(error > tolerance)

    def _testCurveCopy(self,
                       PYC,
                       vars,
                       interpolator):

        curve = PYC(
            vars.settlement, vars.instruments,
            Actual360(), interpolator)
        # necessary to trigger bootstrap
        curve.recalculate()

        # typedef typename T::template curve<I>::type base_curve
        # base_curve copiedCurve = curve
        copiedCurve = deepcopy(curve)

        # the two curves should be the same.
        t = 2.718
        r1 = curve.zeroRate(t, Continuous)
        r2 = copiedCurve.zeroRate(t, Continuous)
        self.assertFalse(not close(r1.rate(), r2.rate()))

        # for rate in vars.rates:
        #     rate.setValue(rate.value() + 0.001)
        for i in range(len(vars.rates)):
            vars.rates[i].setValue(vars.rates[i].value() + 0.001)

        # now the original curve should have changed the copied
        # curve should not.
        r3 = curve.zeroRate(t, Continuous)
        r4 = copiedCurve.zeroRate(t, Continuous)
        self.assertFalse(close(r1.rate(), r3.rate()))
        b = close(r2.rate(), r4.rate())
        self.assertFalse(not close(r2.rate(), r4.rate()))
