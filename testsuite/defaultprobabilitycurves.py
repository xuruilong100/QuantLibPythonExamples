import unittest
from math import exp

from QuantLib import *

from utilities import *


class ExpErrorPred(object):

    def __init__(self, msg):
        self.expMsg = msg

    def __call__(self, ex):
        errMsg = str(ex)
        if not (self.expMsg in errMsg):
            return false

        else:
            return true


class DefaultProbabilityCurveTest(unittest.TestCase):

    def testDefaultProbability(self):
        TEST_MESSAGE(
            "Testing default-probability structure...")

        hazardRate = 0.0100
        hazardRateQuote = QuoteHandle(SimpleQuote(hazardRate))
        dayCounter = Actual360()
        calendar = TARGET()
        n = 20

        tolerance = 1.0e-10
        today = Settings.instance().evaluationDate
        startDate = today
        endDate = startDate

        flatHazardRate = FlatHazardRate(
            startDate, hazardRateQuote, dayCounter)

        for i in range(n):
            startDate = endDate
            endDate = calendar.advance(endDate, 1, Years)

            pStart = flatHazardRate.defaultProbability(startDate)
            pEnd = flatHazardRate.defaultProbability(endDate)

            pBetweenComputed = flatHazardRate.defaultProbability(
                startDate, endDate)

            pBetween = pEnd - pStart

            self.assertFalse(abs(pBetween - pBetweenComputed) > tolerance)

            t2 = dayCounter.yearFraction(today, endDate)
            timeProbability = flatHazardRate.defaultProbability(t2)
            dateProbability = flatHazardRate.defaultProbability(endDate)

            self.assertFalse(abs(timeProbability - dateProbability) > tolerance)

            t1 = dayCounter.yearFraction(today, startDate)
            timeProbability = flatHazardRate.defaultProbability(t1, t2)
            dateProbability = flatHazardRate.defaultProbability(startDate, endDate)

            self.assertFalse(abs(timeProbability - dateProbability) > tolerance)

    def testFlatHazardRate(self):
        TEST_MESSAGE(
            "Testing flat hazard rate...")

        hazardRate = 0.0100
        hazardRateQuote = QuoteHandle(
            SimpleQuote(hazardRate))
        dayCounter = Actual360()
        calendar = TARGET()
        n = 20

        tolerance = 1.0e-10
        today = Settings.instance().evaluationDate
        startDate = today
        endDate = startDate

        flatHazardRate = FlatHazardRate(
            today, hazardRateQuote, dayCounter)

        for i in range(n):
            endDate = calendar.advance(endDate, 1, Years)
            t = dayCounter.yearFraction(startDate, endDate)
            probability = 1.0 - exp(-hazardRate * t)
            computedProbability = flatHazardRate.defaultProbability(t)

            self.assertFalse(abs(probability - computedProbability) > tolerance)

    def testFlatHazardConsistency(self):
        TEST_MESSAGE(
            "Testing piecewise-flat hazard-rate consistency...")

        self._testBootstrapFromSpread(PiecewiseBackwardFlatHazard, BackwardFlat())
        self._testBootstrapFromUpfront(PiecewiseBackwardFlatHazard, BackwardFlat())

    def testFlatDensityConsistency(self):
        TEST_MESSAGE(
            "Testing piecewise-flat default-density consistency...")

        self._testBootstrapFromSpread(PiecewiseBackwardFlatDefault, BackwardFlat())
        self._testBootstrapFromUpfront(PiecewiseBackwardFlatDefault, BackwardFlat())

    def testLinearDensityConsistency(self):
        TEST_MESSAGE(
            "Testing piecewise-linear default-density consistency...")

        self._testBootstrapFromSpread(PiecewiseLinearDefault, Linear())
        self._testBootstrapFromUpfront(PiecewiseLinearDefault, Linear())

    def testLogLinearSurvivalConsistency(self):
        TEST_MESSAGE(
            "Testing log-linear survival-probability consistency...")

        self._testBootstrapFromSpread(PiecewiseLogLinearSurvival, LogLinear())
        self._testBootstrapFromUpfront(PiecewiseLogLinearSurvival, LogLinear())

    def testSingleInstrumentBootstrap(self):
        TEST_MESSAGE(
            "Testing single-instrument curve bootstrap...")

        calendar = TARGET()

        today = Settings.instance().evaluationDate

        settlementDays = 0

        quote = 0.005
        tenor = Period(2, Years)

        frequency = Quarterly
        convention = Following
        rule = DateGeneration.TwentiethIMM
        dayCounter = Thirty360(Thirty360.BondBasis)
        recoveryRate = 0.4

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(
            FlatForward(today, 0.06, Actual360()))

        helpers = DefaultProbabilityHelperVector(1)

        helpers[0] = SpreadCdsHelper(
            quote, tenor,
            settlementDays, calendar,
            frequency, convention, rule,
            dayCounter, recoveryRate,
            discountCurve)

        defaultCurve = PiecewiseBackwardFlatHazard(
            today, helpers, dayCounter, BackwardFlat())
        defaultCurve.recalculate()

    def testUpfrontBootstrap(self):
        TEST_MESSAGE(
            "Testing bootstrap on upfront quotes...")

        backup = SavedSettings()

        Settings.instance().setIncludeTodaysCashFlows(False)

        self._testBootstrapFromUpfront(PiecewiseBackwardFlatHazard, BackwardFlat())

        flag = Settings.instance().includeTodaysCashFlows
        self.assertFalse(flag != false)

    def testIterativeBootstrapRetries(self):
        TEST_MESSAGE(
            "Testing iterative bootstrap with retries...")

        backup = SavedSettings()

        asof = Date(1, Apr, 2020)
        Settings.instance().evaluationDate = asof
        tsDayCounter = Actual365Fixed()

        usdCurveDates = [
            Date(1, Apr, 2020),
            Date(2, Apr, 2020),
            Date(14, Apr, 2020),
            Date(21, Apr, 2020),
            Date(28, Apr, 2020),
            Date(6, May, 2020),
            Date(5, Jun, 2020),
            Date(7, Jul, 2020),
            Date(5, Aug, 2020),
            Date(8, Sep, 2020),
            Date(7, Oct, 2020),
            Date(5, Nov, 2020),
            Date(7, Dec, 2020),
            Date(6, Jan, 2021),
            Date(5, Feb, 2021),
            Date(5, Mar, 2021),
            Date(7, Apr, 2021),
            Date(4, Apr, 2022),
            Date(3, Apr, 2023),
            Date(3, Apr, 2024),
            Date(3, Apr, 2025),
            Date(5, Apr, 2027),
            Date(3, Apr, 2030),
            Date(3, Apr, 2035),
            Date(3, Apr, 2040),
            Date(4, Apr, 2050)]

        usdCurveDfs = [
            1.000000000,
            0.999955835,
            0.999931070,
            0.999914629,
            0.999902799,
            0.999887990,
            0.999825782,
            0.999764392,
            0.999709076,
            0.999647785,
            0.999594638,
            0.999536198,
            0.999483093,
            0.999419291,
            0.999379417,
            0.999324981,
            0.999262356,
            0.999575101,
            0.996135441,
            0.995228348,
            0.989366687,
            0.979271200,
            0.961150726,
            0.926265361,
            0.891640651,
            0.839314063]

        usdYts = YieldTermStructureHandle(

            DiscountCurve(
                usdCurveDates, usdCurveDfs, tsDayCounter))

        cdsSpreads = [
            (Period(6, Months), 2.957980250),
            (Period(1, Years), 3.076933100),
            (Period(2, Years), 2.944524520),
            (Period(3, Years), 2.844498960),
            (Period(4, Years), 2.769234420),
            (Period(5, Years), 2.713474100)]
        recoveryRate = 0.035

        settlementDays = 1
        calendar = WeekendsOnly()
        frequency = Quarterly
        paymentConvention = Following
        rule = DateGeneration.CDS2015
        dayCounter = Actual360()
        lastPeriodDayCounter = Actual360(true)

        instruments = []
        for it in cdsSpreads:
            instruments.append(
                SpreadCdsHelper(
                    it[1], it[0], settlementDays, calendar,
                    frequency, paymentConvention, rule, dayCounter,
                    recoveryRate, usdYts, true, true, Date(),
                    lastPeriodDayCounter))

        SPCurve = PiecewiseLogLinearSurvival
        dpts = SPCurve(asof, instruments, tsDayCounter, LogLinear())

        testDate = Date(21, Dec, 2020)

        self.assertRaises(RuntimeError, dpts.survivalProbability, testDate)

        ib = IterativeBootstrap(NullReal(), NullReal(), NullReal(), 5, 1.0, 10.0)
        dpts = SPCurve(asof, instruments, tsDayCounter, LogLinear(), ib)

        self.assertRaises(RuntimeError, dpts.survivalProbability, testDate)

        ibNoThrow = IterativeBootstrap(NullReal(), NullReal(), NullReal(), 5, 1.0, 10.0, true, 2)
        dpts = SPCurve(asof, instruments, tsDayCounter, LogLinear(), ibNoThrow)

        try:
            dpts.survivalProbability(testDate)
        except Exception as e:
            NO_THROW = false
            self.assertTrue(NO_THROW)

    def _testBootstrapFromSpread(self,
                                 PDC,
                                 I):

        calendar = TARGET()

        today = Settings.instance().evaluationDate

        settlementDays = 1

        quote = [0.005, 0.006, 0.007, 0.009]
        n = [1, 2, 3, 5]

        frequency = Quarterly
        convention = Following
        rule = DateGeneration.TwentiethIMM
        dayCounter = Thirty360(Thirty360.BondBasis)
        recoveryRate = 0.4

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo((
            FlatForward(today, 0.06, Actual360())))

        helpers = DefaultProbabilityHelperVector()

        for i in range(len(n)):
            helpers.append(
                SpreadCdsHelper(
                    quote[i], Period(n[i], Years),
                    settlementDays, calendar,
                    frequency, convention, rule,
                    dayCounter, recoveryRate,
                    discountCurve))

        piecewiseCurve = RelinkableDefaultProbabilityTermStructureHandle()
        piecewiseCurve.linkTo(
            PDC(today, helpers, Thirty360(Thirty360.BondBasis), I))

        notional = 1.0
        tolerance = 1.0e-6

        backup = SavedSettings()
        Settings.instance().includeTodaysCashFlows = true

        for i in range(len(n)):
            protectionStart = today + settlementDays
            startDate = calendar.adjust(protectionStart, convention)
            endDate = today + Period(n[i], Years)

            schedule = Schedule(
                startDate, endDate, Period(frequency), calendar,
                convention, Unadjusted, rule, false)

            cds = CreditDefaultSwap(
                Protection.Buyer, notional, quote[i],
                schedule, convention, dayCounter,
                true, true, protectionStart)
            cds.setPricingEngine(
                MidPointCdsEngine(
                    piecewiseCurve, recoveryRate,
                    discountCurve))

            inputRate = quote[i]
            computedRate = cds.fairSpread()
            self.assertFalse(abs(inputRate - computedRate) > tolerance)

    def _testBootstrapFromUpfront(self,
                                  PDC,
                                  I):

        calendar = TARGET()

        today = Settings.instance().evaluationDate

        settlementDays = 1

        quote = [0.01, 0.02, 0.04, 0.06]
        n = [2, 3, 5, 7]

        fixedRate = 0.05
        frequency = Quarterly
        convention = ModifiedFollowing
        rule = DateGeneration.CDS
        dayCounter = Actual360()
        recoveryRate = 0.4
        upfrontSettlementDays = 3

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(
            FlatForward(today, 0.06, Actual360()))

        helpers = DefaultProbabilityHelperVector()

        for i in range(len(n)):
            helpers.append(
                UpfrontCdsHelper(
                    quote[i], fixedRate,
                    Period(n[i], Years),
                    settlementDays, calendar,
                    frequency, convention, rule,
                    dayCounter, recoveryRate,
                    discountCurve,
                    upfrontSettlementDays,
                    true, true, Date(), Actual360(true)))

        piecewiseCurve = RelinkableDefaultProbabilityTermStructureHandle()
        piecewiseCurve.linkTo(
            PDC(today, helpers, Thirty360(Thirty360.BondBasis), I))

        notional = 1.0
        tolerance = 1.0e-6

        backup = SavedSettings()

        Settings.instance().includeTodaysCashFlows = true

        for i in range(len(n)):
            protectionStart = today + settlementDays
            startDate = protectionStart
            endDate = cdsMaturity(today, Period(n[i], Years), rule)
            upfrontDate = calendar.advance(
                today, upfrontSettlementDays,
                Days, convention)

            schedule = Schedule(
                startDate, endDate, Period(frequency), calendar,
                convention, Unadjusted, rule, false)

            cds = CreditDefaultSwap(
                Protection.Buyer, notional,
                quote[i], fixedRate,
                schedule, convention, dayCounter,
                true, true, protectionStart,
                upfrontDate, Actual360(true),
                true, today)
            cds.setPricingEngine(
                MidPointCdsEngine(
                    piecewiseCurve, recoveryRate,
                    discountCurve, true))

            inputUpfront = quote[i]
            computedUpfront = cds.fairUpfront()
            self.assertFalse(abs(inputUpfront - computedUpfront) > tolerance)
