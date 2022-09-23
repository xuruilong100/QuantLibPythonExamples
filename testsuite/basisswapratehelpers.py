import unittest

from QuantLib import *

from utilities import *


class BasisSwapQuote(object):
    def __init__(self,
                 n,
                 units,
                 basis):
        self.n = n
        self.units = units
        self.basis = basis


class BasisSwapRateHelpersTest(unittest.TestCase):

    def testIborIborBaseCurveBootstrap(self):
        TEST_MESSAGE(
            "Testing IBOR-IBOR basis-swap rate helpers (base curve bootstrap)...")

        self._testIborIborBootstrap(true)

    def testIborIborOtherCurveBootstrap(self):
        TEST_MESSAGE(
            "Testing IBOR-IBOR basis-swap rate helpers (other curve bootstrap)...")

        self._testIborIborBootstrap(false)

    def testOvernightIborBootstrap(self):
        TEST_MESSAGE(
            "Testing overnight-IBOR basis-swap rate helpers...")

        self._testOvernightIborBootstrap(false)

    def testOvernightIborBootstrapWithDiscountCurve(self):
        TEST_MESSAGE(
            "Testing overnight-IBOR basis-swap rate helpers with external discount curve...")

        self._testOvernightIborBootstrap(true)

    def _testIborIborBootstrap(self,
                               bootstrapBaseCurve):
        quotes = [
            BasisSwapQuote(1, Years, 0.0010), BasisSwapQuote(2, Years, 0.0012), BasisSwapQuote(3, Years, 0.0015),
            BasisSwapQuote(5, Years, 0.0015), BasisSwapQuote(8, Years, 0.0018), BasisSwapQuote(10, Years, 0.0020),
            BasisSwapQuote(15, Years, 0.0021), BasisSwapQuote(20, Years, 0.0021), ]

        settlementDays = 2
        calendar = UnitedStates(UnitedStates.GovernmentBond)
        convention = Following
        endOfMonth = false

        knownForecastCurve = YieldTermStructureHandle(flatRate(0.01, Actual365Fixed()))
        discountCurve = YieldTermStructureHandle(flatRate(0.005, Actual365Fixed()))

        if bootstrapBaseCurve:
            baseIndex = USDLibor(Period(3, Months))
            otherIndex = USDLibor(Period(6, Months), knownForecastCurve)
        else:
            baseIndex = USDLibor(Period(3, Months), knownForecastCurve)
            otherIndex = USDLibor(Period(6, Months))

        helpers = RateHelperVector()
        for q in quotes:
            h = IborIborBasisSwapRateHelper(
                QuoteHandle(SimpleQuote(q.basis)),
                Period(q.n, q.units),
                settlementDays, calendar, convention,
                endOfMonth, baseIndex, otherIndex,
                discountCurve, bootstrapBaseCurve)
            helpers.push_back(h)

        bootstrappedCurve = PiecewiseLinearZeroYield(
            0, calendar, helpers, Actual365Fixed(), Linear())

        today = knownGoodDefault
        Settings.instance().evaluationDate = today
        spot = calendar.advance(today, settlementDays, Days)

        if bootstrapBaseCurve:
            baseIndex = USDLibor(
                Period(3, Months), YieldTermStructureHandle(bootstrappedCurve))
            otherIndex = USDLibor(
                Period(6, Months), knownForecastCurve)
        else:
            baseIndex = USDLibor(
                Period(3, Months), knownForecastCurve)
            otherIndex = USDLibor(
                Period(6, Months), YieldTermStructureHandle(bootstrappedCurve))

        for q in quotes:
            maturity = calendar.advance(
                spot, q.n, q.units, convention)

            s1 = MakeSchedule()
            s1.fromDate(spot)
            s1.to(maturity)
            s1.withTenor(baseIndex.tenor())
            s1.withCalendar(calendar)
            s1.withConvention(convention)
            s1.withRule(DateGeneration.Forward)
            s1 = s1.makeSchedule()
            leg1 = IborLeg(s1, baseIndex)
            leg1.withSpreads(q.basis)
            leg1.withNotionals(100.0)
            leg1 = leg1.makeLeg()

            s2 = MakeSchedule()
            s2.fromDate(spot)
            s2.to(maturity)
            s2.withTenor(otherIndex.tenor())
            s2.withCalendar(calendar)
            s2.withConvention(convention)
            s2.withRule(DateGeneration.Forward)
            s2 = s2.makeSchedule()
            leg2 = IborLeg(s2, otherIndex)
            leg2.withNotionals(100.0)
            leg2 = leg2.makeLeg()

            swap = Swap(leg1, leg2)
            swap.setPricingEngine(DiscountingSwapEngine(discountCurve))

            NPV = swap.NPV()
            tolerance = 1e-8
            self.assertFalse(abs(NPV) > tolerance)

    def _testOvernightIborBootstrap(self,
                                    externalDiscountCurve):
        quotes = [
            BasisSwapQuote(1, Years, 0.0010), BasisSwapQuote(2, Years, 0.0012), BasisSwapQuote(3, Years, 0.0015),
            BasisSwapQuote(5, Years, 0.0015), BasisSwapQuote(8, Years, 0.0018), BasisSwapQuote(10, Years, 0.0020),
            BasisSwapQuote(15, Years, 0.0021), BasisSwapQuote(20, Years, 0.0021), ]

        settlementDays = 2
        calendar = UnitedStates(UnitedStates.GovernmentBond)
        convention = Following
        endOfMonth = false

        knownForecastCurve = YieldTermStructureHandle(flatRate(0.01, Actual365Fixed()))

        discountCurve = RelinkableYieldTermStructureHandle()
        if externalDiscountCurve:
            discountCurve.linkTo(flatRate(0.005, Actual365Fixed()))

        baseIndex = Sofr(knownForecastCurve)
        otherIndex = USDLibor(Period(6, Months))

        helpers = RateHelperVector()
        for q in quotes:
            h = OvernightIborBasisSwapRateHelper(
                QuoteHandle(SimpleQuote(q.basis)),
                Period(q.n, q.units),
                settlementDays, calendar, convention,
                endOfMonth, baseIndex, otherIndex,
                discountCurve)
            helpers.push_back(h)

        bootstrappedCurve = PiecewiseLinearZeroYield(
            0, calendar, helpers, Actual365Fixed(), Linear())

        today = knownGoodDefault
        Settings.instance().evaluationDate = today
        spot = calendar.advance(today, settlementDays, Days)

        otherIndex = USDLibor(
            Period(6, Months), YieldTermStructureHandle(bootstrappedCurve))

        for q in quotes:

            maturity = calendar.advance(spot, q.n, q.units, convention)

            s = MakeSchedule()
            s.fromDate(spot)
            s.to(maturity)
            s.withTenor(otherIndex.tenor())
            s.withCalendar(calendar)
            s.withConvention(convention)
            s.withRule(DateGeneration.Forward)
            s = s.makeSchedule()

            leg1 = OvernightLeg(s, baseIndex)
            leg1.withSpreads(q.basis)
            leg1.withNotionals(100.0)
            leg1 = leg1.makeLeg()
            leg2 = IborLeg(s, otherIndex)
            leg2.withNotionals(100.0)
            leg2 = leg2.makeLeg()

            swap = Swap(leg1, leg2)
            if externalDiscountCurve:
                swap.setPricingEngine(DiscountingSwapEngine(discountCurve))
            else:
                swap.setPricingEngine(DiscountingSwapEngine(
                    YieldTermStructureHandle(bootstrappedCurve)))

            NPV = swap.NPV()
            tolerance = 1e-8
            self.assertFalse(abs(NPV) > tolerance)
