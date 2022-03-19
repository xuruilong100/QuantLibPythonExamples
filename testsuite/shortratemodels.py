import unittest
from utilities import *
from QuantLib import *


class CalibrationData(object):
    def __init__(self,
                 start,
                 length,
                 volatility):
        self.start = start
        self.length = length
        self.volatility = volatility


class ShortRateModelTest(unittest.TestCase):

    def testFuturesConvexityBias(self):
        TEST_MESSAGE("Testing Hull-White futures convexity bias...")

        # G. Kirikos, D. Novak, "Convexity Conundrums", Risk Magazine, March 1997
        futureQuote = 94.0
        a = 0.03
        sigma = 0.015
        t = 5.0
        T = 5.25

        expectedForward = 0.0573037
        tolerance = 0.0000001

        futureImpliedRate = (100.0 - futureQuote) / 100.0
        calculatedForward = futureImpliedRate - \
                            HullWhite.convexityBias(futureQuote, t, T, sigma, a)

        error = abs(calculatedForward - expectedForward)

        self.assertFalse(error > tolerance)

    def testCachedHullWhite(self):
        TEST_MESSAGE(
            "Testing Hull-White calibration against cached values using swaptions with start delay...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        backup = SavedSettings()
        # cleaner = IndexHistoryCleaner()

        today = Date(15, February, 2002)
        settlement = Date(19, February, 2002)
        Settings.instance().evaluationDate = today
        termStructure = YieldTermStructureHandle(
            flatRate(settlement, 0.04875825, Actual365Fixed()))
        model = HullWhite(termStructure)
        data = [
            CalibrationData(1, 5, 0.1148),
            CalibrationData(2, 4, 0.1108),
            CalibrationData(3, 3, 0.1070),
            CalibrationData(4, 2, 0.1021),
            CalibrationData(5, 1, 0.1000)]
        index = Euribor6M(termStructure)

        engine = JamshidianSwaptionEngine(model)

        swaptions = CalibrationHelperVector()
        for i in data:
            vol = SimpleQuote(i.volatility)
            helper = SwaptionHelper(
                Period(i.start, Years), Period(i.length, Years),
                QuoteHandle(vol), index, Period(1, Years),
                Thirty360(Thirty360.BondBasis), Actual360(), termStructure)
            helper.setPricingEngine(engine)
            swaptions.append(helper)

        # Set up the optimization problem
        # simplexLambda = 0.1
        # Simplex optimizationMethod(simplexLambda)
        optimizationMethod = LevenbergMarquardt(1.0e-8, 1.0e-8, 1.0e-8)
        endCriteria = EndCriteria(10000, 100, 1e-6, 1e-8, 1e-8)

        # Optimize
        model.calibrate(swaptions, optimizationMethod, endCriteria)
        ecType = model.endCriteria()

        # Check and print out results
        # cachedA, cachedSigma
        if not usingAtParCoupons:
            cachedA = 0.0463679
            cachedSigma = 0.00579831
        else:
            cachedA = 0.0464041
            cachedSigma = 0.00579912

        tolerance = 1.0e-5
        xMinCalculated = model.params()
        yMinCalculated = model.value(xMinCalculated, swaptions)
        xMinExpected = Array(2)
        xMinExpected[0] = cachedA
        xMinExpected[1] = cachedSigma
        yMinExpected = model.value(xMinExpected, swaptions)
        self.assertFalse(
            abs(xMinCalculated[0] - cachedA) > tolerance or
            abs(xMinCalculated[1] - cachedSigma) > tolerance)

        IndexManager.instance().clearHistories()

    def testCachedHullWhiteFixedReversion(self):
        TEST_MESSAGE("Testing Hull-White calibration with fixed reversion against cached values...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        backup = SavedSettings()
        # cleaner = IndexHistoryCleaner()

        today = Date(15, February, 2002)
        settlement = Date(19, February, 2002)
        Settings.instance().evaluationDate = today
        termStructure = YieldTermStructureHandle(
            flatRate(
                settlement, 0.04875825, Actual365Fixed()))
        model = HullWhite(termStructure, 0.05, 0.01)
        data = [
            CalibrationData(1, 5, 0.1148),
            CalibrationData(2, 4, 0.1108),
            CalibrationData(3, 3, 0.1070),
            CalibrationData(4, 2, 0.1021),
            CalibrationData(5, 1, 0.1000)]
        index = Euribor6M(termStructure)

        engine = JamshidianSwaptionEngine(model)

        swaptions = CalibrationHelperVector()
        for i in data:
            vol = SimpleQuote(i.volatility)
            helper = SwaptionHelper(
                Period(i.start, Years), Period(i.length, Years), QuoteHandle(vol),
                index, Period(1, Years), Thirty360(Thirty360.BondBasis),
                Actual360(), termStructure)
            helper.setPricingEngine(engine)
            swaptions.append(helper)

        # Set up the optimization problem
        # simplexLambda = 0.1
        # Simplex optimizationMethod(simplexLambda)
        optimizationMethod = LevenbergMarquardt(1.0e-18, 1.0e-18, 1.0e-18)
        endCriteria = EndCriteria(1000, 500, 1E-8, 1E-8, 1E-8)

        # Optimize
        model.calibrate(
            swaptions, optimizationMethod, endCriteria,
            Constraint(), DoubleVector(),
            HullWhite.FixedReversion())
        ecType = model.endCriteria()

        # Check and print out results
        # cachedA, cachedSigma
        if not usingAtParCoupons:
            cachedA = 0.05
            cachedSigma = 0.00585835
        else:
            cachedA = 0.05
            cachedSigma = 0.00585858

        tolerance = 1.0e-5
        xMinCalculated = model.params()
        yMinCalculated = model.value(xMinCalculated, swaptions)
        xMinExpected = Array(2)
        xMinExpected[0] = cachedA
        xMinExpected[1] = cachedSigma
        yMinExpected = model.value(xMinExpected, swaptions)
        self.assertFalse(
            abs(xMinCalculated[0] - cachedA) > tolerance or
            abs(xMinCalculated[1] - cachedSigma) > tolerance)
        IndexManager.instance().clearHistories()

    def testCachedHullWhite2(self):
        TEST_MESSAGE("Testing Hull-White calibration against cached "
                     "values using swaptions without start delay...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        backup = SavedSettings()
        # cleaner = IndexHistoryCleaner()

        today = Date(15, February, 2002)
        settlement = Date(19, February, 2002)
        Settings.instance().evaluationDate = today
        termStructure = YieldTermStructureHandle(
            flatRate(
                settlement, 0.04875825, Actual365Fixed()))
        model = HullWhite(termStructure)
        data = [
            CalibrationData(1, 5, 0.1148),
            CalibrationData(2, 4, 0.1108),
            CalibrationData(3, 3, 0.1070),
            CalibrationData(4, 2, 0.1021),
            CalibrationData(5, 1, 0.1000)]
        index = Euribor6M(termStructure)
        index0 = IborIndex(
            index.familyName(), index.tenor(), 0,
            index.currency(), index.fixingCalendar(),
            index.businessDayConvention(), index.endOfMonth(),
            index.dayCounter(), termStructure)  # Euribor 6m with zero fixing days

        engine = JamshidianSwaptionEngine(model)

        swaptions = CalibrationHelperVector()
        for i in data:
            vol = SimpleQuote(i.volatility)
            helper = SwaptionHelper(
                Period(i.start, Years), Period(i.length, Years), QuoteHandle(vol),
                index0, Period(1, Years), Thirty360(Thirty360.BondBasis),
                Actual360(), termStructure)
            helper.setPricingEngine(engine)
            swaptions.append(helper)

        # Set up the optimization problem
        # simplexLambda = 0.1
        # Simplex optimizationMethod(simplexLambda)
        optimizationMethod = LevenbergMarquardt(1.0e-8, 1.0e-8, 1.0e-8)
        endCriteria = EndCriteria(10000, 100, 1e-6, 1e-8, 1e-8)

        # Optimize
        model.calibrate(swaptions, optimizationMethod, endCriteria)
        ecType = model.endCriteria()

        # Check and print out results
        # The cached values were produced with an older version of the
        # JamshidianEngine not accounting for the delay between option
        # expiry and underlying start
        # cachedA, cachedSigma
        if not usingAtParCoupons:
            cachedA = 0.0481608
            cachedSigma = 0.00582493
        else:
            cachedA = 0.0482063
            cachedSigma = 0.00582687

        tolerance = 5.0e-6
        xMinCalculated = model.params()
        yMinCalculated = model.value(xMinCalculated, swaptions)
        xMinExpected = Array(2)
        xMinExpected[0] = cachedA
        xMinExpected[1] = cachedSigma
        yMinExpected = model.value(xMinExpected, swaptions)
        self.assertFalse(
            abs(xMinCalculated[0] - cachedA) > tolerance or
            abs(xMinCalculated[1] - cachedSigma) > tolerance)
        IndexManager.instance().clearHistories()

    def testSwaps(self):
        TEST_MESSAGE("Testing Hull-White swap pricing against known values...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        backup = SavedSettings()
        # cleaner = IndexHistoryCleaner()

        today = Settings.instance().evaluationDate
        calendar = TARGET()
        today = calendar.adjust(today)
        Settings.instance().evaluationDate = today

        settlement = calendar.advance(today, 2, Days)

        dates = [
            settlement,
            calendar.advance(settlement, 1, Weeks),
            calendar.advance(settlement, 1, Months),
            calendar.advance(settlement, 3, Months),
            calendar.advance(settlement, 6, Months),
            calendar.advance(settlement, 9, Months),
            calendar.advance(settlement, 1, Years),
            calendar.advance(settlement, 2, Years),
            calendar.advance(settlement, 3, Years),
            calendar.advance(settlement, 5, Years),
            calendar.advance(settlement, 10, Years),
            calendar.advance(settlement, 15, Years)]
        discounts = [
            1.0,
            0.999258,
            0.996704,
            0.990809,
            0.981798,
            0.972570,
            0.963430,
            0.929532,
            0.889267,
            0.803693,
            0.596903,
            0.433022]

        termStructure = YieldTermStructureHandle(
            DiscountCurve(dates, discounts, Actual365Fixed()))

        model = HullWhite(termStructure)

        start = [-3, 0, 3]
        length = [2, 5, 10]
        rates = [0.02, 0.04, 0.06]
        euribor = Euribor6M(termStructure)

        engine = TreeVanillaSwapEngine(model, 120)

        tolerance = 1.0e-8 if usingAtParCoupons else 4.0e-3

        for i in range(len(start)):

            startDate = calendar.advance(settlement, start[i], Months)
            if startDate < today:
                fixingDate = calendar.advance(startDate, -2, Days)
                pastFixings = RealTimeSeries()
                pastFixings[fixingDate] = 0.03
                IndexManager.instance().setHistory(
                    euribor.name(), pastFixings)

            for j in range(len(length)):

                maturity = calendar.advance(startDate, length[i], Years)
                fixedSchedule = Schedule(
                    startDate, maturity, Period(Annual),
                    calendar, Unadjusted, Unadjusted,
                    DateGeneration.Forward, false)
                floatSchedule = Schedule(
                    startDate, maturity, Period(Semiannual),
                    calendar, Following, Following,
                    DateGeneration.Forward, false)
                for rate in rates:
                    swap = VanillaSwap(
                        Swap.Payer, 1000000.0, fixedSchedule, rate,
                        Thirty360(Thirty360.BondBasis),
                        floatSchedule, euribor, 0.0, Actual360())
                    swap.setPricingEngine(
                        DiscountingSwapEngine(termStructure))
                    expected = swap.NPV()
                    swap.setPricingEngine(engine)
                    calculated = swap.NPV()

                    error = abs((expected - calculated) / expected)
                    self.assertFalse(error > tolerance)
        IndexManager.instance().clearHistories()

    def testExtendedCoxIngersollRossDiscountFactor(self):
        TEST_MESSAGE("Testing zero-bond pricing for extended CIR model...")

        backup = SavedSettings()
        today = Settings.instance().evaluationDate

        rate = 0.1
        rTS = YieldTermStructureHandle(
            flatRate(today, rate, Actual365Fixed()))

        now = 1.5
        maturity = 2.5

        cirModel = ExtendedCoxIngersollRoss(rTS, rate, 1.0, 1e-4, rate)

        expected = rTS.discount(maturity) / rTS.discount(now)
        calculated = cirModel.discountBond(now, maturity, rate)

        tol = 1e-6
        diff = abs(expected - calculated)

        self.assertFalse(diff > tol)
