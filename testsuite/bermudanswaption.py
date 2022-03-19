import unittest
from utilities import *
from QuantLib import *
import numpy as np


class CommonVars(object):
    # setup
    def __init__(self):
        self.startYears = 1
        self.length = 5
        self.type = Swap.Payer
        self.nominal = 1000.0
        self.settlementDays = 2
        self.fixedConvention = Unadjusted
        self.floatingConvention = ModifiedFollowing
        self.fixedFrequency = Annual
        self.floatingFrequency = Semiannual
        self.fixedDayCount = Thirty360(Thirty360.BondBasis)
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.index = Euribor6M(self.termStructure)
        self.calendar = self.index.fixingCalendar()
        self.today = self.calendar.adjust(Date.todaysDate())
        self.settlement = self.calendar.advance(
            self.today, self.settlementDays, Days)
        self.backup = SavedSettings()

    # utilities
    def makeSwap(self, fixedRate):
        start = self.calendar.advance(
            self.settlement, self.startYears, Years)
        maturity = self.calendar.advance(
            start, self.length, Years)
        fixedSchedule = Schedule(
            start, maturity,
            Period(self.fixedFrequency),
            self.calendar,
            self.fixedConvention,
            self.fixedConvention,
            DateGeneration.Forward, false)
        floatSchedule = Schedule(
            start, maturity,
            Period(self.floatingFrequency),
            self.calendar,
            self.floatingConvention,
            self.floatingConvention,
            DateGeneration.Forward, false)
        swap = VanillaSwap(
            self.type, self.nominal,
            fixedSchedule, fixedRate, self.fixedDayCount,
            floatSchedule, self.index, 0.0,
            self.index.dayCounter())
        swap.setPricingEngine(
            DiscountingSwapEngine(self.termStructure))
        return swap


class BermudanSwaptionTest(unittest.TestCase):

    def testCachedValues(self):
        TEST_MESSAGE(
            "Testing Bermudan swaption with HW model against cached values...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        vars.today = Date(15, February, 2002)

        Settings.instance().evaluationDate = vars.today

        vars.settlement = Date(19, February, 2002)
        # flat yield term structure impling 1x5 swap at 5%
        vars.termStructure.linkTo(
            flatRate(vars.settlement, 0.04875825, Actual365Fixed()))

        atmRate = vars.makeSwap(0.0).fairRate()

        itmSwap = vars.makeSwap(0.8 * atmRate)
        atmSwap = vars.makeSwap(atmRate)
        otmSwap = vars.makeSwap(1.2 * atmRate)

        a = 0.048696
        sigma = 0.0058904
        model = HullWhite(vars.termStructure, a, sigma)
        exerciseDates = DateVector()
        leg = atmSwap.fixedLeg()
        for i in leg:
            coupon = as_coupon(i)
            exerciseDates.append(coupon.accrualStartDate())

        exercise = BermudanExercise(exerciseDates)

        treeEngine = TreeSwaptionEngine(model, 50)
        fdmEngine = FdHullWhiteSwaptionEngine(model)

        # itmValue, atmValue, otmValue
        # itmValueFdm, atmValueFdm, otmValueFdm
        if not usingAtParCoupons:
            itmValue = 42.2413
            atmValue = 12.8789
            otmValue = 2.4759
            itmValueFdm = 42.2111
            atmValueFdm = 12.8879
            otmValueFdm = 2.44443
        else:
            itmValue = 42.2470
            atmValue = 12.8826
            otmValue = 2.4769
            itmValueFdm = 42.2091
            atmValueFdm = 12.8864
            otmValueFdm = 2.4437

        tolerance = 1.0e-4

        swaption = Swaption(itmSwap, exercise)
        swaption.setPricingEngine(treeEngine)
        self.assertFalse(abs(swaption.NPV() - itmValue) > tolerance)
        swaption.setPricingEngine(fdmEngine)
        self.assertFalse(abs(swaption.NPV() - itmValueFdm) > tolerance)

        swaption = Swaption(atmSwap, exercise)
        swaption.setPricingEngine(treeEngine)
        self.assertFalse(abs(swaption.NPV() - atmValue) > tolerance)
        swaption.setPricingEngine(fdmEngine)
        self.assertFalse(abs(swaption.NPV() - atmValueFdm) > tolerance)

        swaption = Swaption(otmSwap, exercise)
        swaption.setPricingEngine(treeEngine)
        self.assertFalse(abs(swaption.NPV() - otmValue) > tolerance)
        swaption.setPricingEngine(fdmEngine)
        self.assertFalse(abs(swaption.NPV() - otmValueFdm) > tolerance)

        for i in range(len(exerciseDates)):
            exerciseDates[i] = vars.calendar.adjust(
                exerciseDates[i] - Period(10, Days))
        exercise = BermudanExercise(exerciseDates)

        if not usingAtParCoupons:
            itmValue = 42.1917
            atmValue = 12.7788
            otmValue = 2.4388

        else:
            itmValue = 42.1974
            atmValue = 12.7825
            otmValue = 2.4399

        swaption = Swaption(itmSwap, exercise)
        swaption.setPricingEngine(treeEngine)
        self.assertFalse(abs(swaption.NPV() - itmValue) > tolerance)
        swaption = Swaption(atmSwap, exercise)
        swaption.setPricingEngine(treeEngine)
        self.assertFalse(abs(swaption.NPV() - atmValue) > tolerance)

        swaption = Swaption(otmSwap, exercise)
        swaption.setPricingEngine(treeEngine)
        self.assertFalse(abs(swaption.NPV() - otmValue) > tolerance)

    def testCachedG2Values(self):
        TEST_MESSAGE(
            "Testing Bermudan swaption with G2 model against cached values...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        vars.today = Date(15, September, 2016)
        Settings.instance().evaluationDate = vars.today
        vars.settlement = Date(19, September, 2016)

        # flat yield term structure impling 1x5 swap at 5%
        vars.termStructure.linkTo(
            flatRate(vars.settlement, 0.04875825, Actual365Fixed()))

        atmRate = vars.makeSwap(0.0).fairRate()
        swaptions = []
        for s in np.arange(0.5, 1.51, 0.25):
            swap = vars.makeSwap(s * atmRate)

            exerciseDates = DateVector()
            for i in swap.fixedLeg():
                exerciseDates.append(
                    as_coupon(i).accrualStartDate())

            swaptions.append(
                Swaption(swap, BermudanExercise(exerciseDates)))

        a = 0.1
        sigma = 0.01
        b = 0.2
        eta = 0.013
        rho = -0.5

        g2Model = G2(
            vars.termStructure, a, sigma, b, eta, rho)
        fdmEngine = FdG2SwaptionEngine(g2Model, 50, 75, 75, 0, 1e-3)
        treeEngine = TreeSwaptionEngine(g2Model, 50)

        # expectedFdm[5], expectedTree[5]
        if not usingAtParCoupons:
            tmpExpectedFdm = [103.231, 54.6519, 20.0475, 5.26941, 1.07097]
            tmpExpectedTree = [103.253, 54.6685, 20.1399, 5.40517, 1.10642]

            expectedFdm = tmpExpectedFdm
            expectedTree = tmpExpectedTree

        else:
            tmpExpectedFdm = [103.227, 54.6502, 20.0469, 5.26924, 1.07093]
            tmpExpectedTree = [103.256, 54.6726, 20.1429, 5.4064, 1.10677]

            expectedFdm = tmpExpectedFdm
            expectedTree = tmpExpectedTree

        tol = 0.005
        for i in range(len(swaptions)):
            swaptions[i].setPricingEngine(fdmEngine)
            calculatedFdm = swaptions[i].NPV()

            self.assertFalse(abs(calculatedFdm - expectedFdm[i]) > tol)

            swaptions[i].setPricingEngine(treeEngine)
            calculatedTree = swaptions[i].NPV()

            self.assertFalse(abs(calculatedTree - expectedTree[i]) > tol)
