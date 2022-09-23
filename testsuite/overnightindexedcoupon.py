import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):
    def __init__(self):
        self.today = Date(23, November, 2021)
        self.notional = 10000.0
        self.backup = SavedSettings()
        Settings.instance().evaluationDate = self.today
        self.forecastCurve = RelinkableYieldTermStructureHandle()
        self.sofr = Sofr(self.forecastCurve)

        pastDates = [
            Date(18, October, 2021), Date(19, October, 2021), Date(20, October, 2021),
            Date(21, October, 2021), Date(22, October, 2021), Date(25, October, 2021),
            Date(26, October, 2021), Date(27, October, 2021), Date(28, October, 2021),
            Date(29, October, 2021), Date(1, November, 2021), Date(2, November, 2021),
            Date(3, November, 2021), Date(4, November, 2021), Date(5, November, 2021),
            Date(8, November, 2021), Date(9, November, 2021), Date(10, November, 2021),
            Date(12, November, 2021), Date(15, November, 2021), Date(16, November, 2021),
            Date(17, November, 2021), Date(18, November, 2021), Date(19, November, 2021),
            Date(22, November, 2021)]
        pastRates = [0.0008, 0.0009, 0.0008, 0.0010, 0.0012, 0.0011, 0.0013,
                     0.0012, 0.0012, 0.0008, 0.0009, 0.0010, 0.0011, 0.0014,
                     0.0013, 0.0011, 0.0009, 0.0008, 0.0007, 0.0008, 0.0008,
                     0.0007, 0.0009, 0.0010, 0.0009]

        self.sofr.addFixings(pastDates, pastRates)

    def makeCoupon(self,
                   startDate,
                   endDate):
        return OvernightIndexedCoupon(
            endDate, self.notional, startDate, endDate, self.sofr)


class OvernightIndexedCouponTest(unittest.TestCase):

    def testPastCouponRate(self):
        TEST_MESSAGE(
            "Testing rate for past overnight-indexed coupon...")

        vars = CommonVars()

        pastCoupon = vars.makeCoupon(
            Date(18, October, 2021), Date(18, November, 2021))

        expectedRate = 0.000987136104
        expectedAmount = vars.notional * expectedRate * 31.0 / 360
        self.assertFalse(abs(pastCoupon.rate() - expectedRate) > 1e-12)
        self.assertFalse(abs(pastCoupon.amount() - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()

    def testCurrentCouponRate(self):
        TEST_MESSAGE(
            "Testing rate for current overnight-indexed coupon...")

        vars = CommonVars()

        vars.forecastCurve.linkTo(flatRate(0.0010, Actual360()))

        currentCoupon = vars.makeCoupon(Date(10, November, 2021), Date(10, December, 2021))

        expectedRate = 0.000926701551
        expectedAmount = vars.notional * expectedRate * 30.0 / 360
        self.assertFalse(abs(currentCoupon.rate() - expectedRate) > 1e-12)
        self.assertFalse(abs(currentCoupon.amount() - expectedAmount) > 1e-8)

        vars.sofr.addFixing(Date(23, November, 2021), 0.0007)

        expectedRate = 0.000916700760
        expectedAmount = vars.notional * expectedRate * 30.0 / 360
        self.assertFalse(abs(currentCoupon.rate() - expectedRate) > 1e-12)
        self.assertFalse(abs(currentCoupon.amount() - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()

    def testFutureCouponRate(self):
        TEST_MESSAGE(
            "Testing rate for future overnight-indexed coupon...")

        vars = CommonVars()

        vars.forecastCurve.linkTo(flatRate(0.0010, Actual360()))

        futureCoupon = vars.makeCoupon(Date(10, December, 2021), Date(10, January, 2022))

        expectedRate = 0.001000043057
        expectedAmount = vars.notional * expectedRate * 31.0 / 360
        self.assertFalse(abs(futureCoupon.rate() - expectedRate) > 1e-12)
        self.assertFalse(abs(futureCoupon.amount() - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()

    def testRateWhenTodayIsHoliday(self):
        TEST_MESSAGE(
            "Testing rate for overnight-indexed coupon when today is a holiday...")

        vars = CommonVars()

        Settings.instance().evaluationDate = Date(20, November, 2021)

        vars.forecastCurve.linkTo(flatRate(0.0010, Actual360()))

        coupon = vars.makeCoupon(Date(10, November, 2021), Date(10, December, 2021))

        expectedRate = 0.000930035180
        expectedAmount = vars.notional * expectedRate * 30.0 / 360
        self.assertFalse(abs(coupon.rate() - expectedRate) > 1e-12)
        self.assertFalse(abs(coupon.amount() - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()

    def testAccruedAmountInThePast(self):
        TEST_MESSAGE(
            "Testing accrued amount in the past for overnight-indexed coupon...")

        vars = CommonVars()

        coupon = vars.makeCoupon(Date(18, October, 2021), Date(18, January, 2022))

        expectedAmount = vars.notional * 0.000987136104 * 31.0 / 360
        self.assertFalse(
            abs(coupon.accruedAmount(Date(18, November, 2021)) - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()

    def testAccruedAmountSpanningToday(self):
        TEST_MESSAGE(
            "Testing accrued amount spanning today for current overnight-indexed coupon...")

        vars = CommonVars()

        vars.forecastCurve.linkTo(flatRate(0.0010, Actual360()))

        coupon = vars.makeCoupon(Date(10, November, 2021), Date(10, January, 2022))

        expectedAmount = vars.notional * 0.000926701551 * 30.0 / 360
        self.assertFalse(
            abs(coupon.accruedAmount(Date(10, December, 2021)) - expectedAmount) > 1e-8)

        vars.sofr.addFixing(Date(23, November, 2021), 0.0007)

        expectedAmount = vars.notional * 0.000916700760 * 30.0 / 360
        self.assertFalse(
            abs(coupon.accruedAmount(Date(10, December, 2021)) - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()

    def testAccruedAmountInTheFuture(self):
        TEST_MESSAGE(
            "Testing accrued amount in the future for overnight-indexed coupon...")

        vars = CommonVars()

        vars.forecastCurve.linkTo(flatRate(0.0010, Actual360()))

        coupon = vars.makeCoupon(Date(10, December, 2021), Date(10, March, 2022))

        accrualDate = Date(10, January, 2022)
        expectedRate = 0.001000043057
        expectedAmount = vars.notional * expectedRate * 31.0 / 360
        self.assertFalse(
            abs(coupon.accruedAmount(accrualDate) - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()

    def testAccruedAmountOnPastHoliday(self):
        TEST_MESSAGE(
            "Testing accrued amount on a past holiday for overnight-indexed coupon...")

        vars = CommonVars()

        coupon = vars.makeCoupon(Date(18, October, 2021), Date(18, January, 2022))

        accrualDate = Date(13, November, 2021)
        expectedAmount = vars.notional * 0.000074724810
        self.assertFalse(
            abs(coupon.accruedAmount(accrualDate) - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()

    def testAccruedAmountOnFutureHoliday(self):
        TEST_MESSAGE(
            "Testing accrued amount on a future holiday for overnight-indexed coupon...")

        vars = CommonVars()

        vars.forecastCurve.linkTo(flatRate(0.0010, Actual360()))

        coupon = vars.makeCoupon(Date(10, December, 2021), Date(10, March, 2022))

        accrualDate = Date(15, January, 2022)
        expectedAmount = vars.notional * 0.000100005012
        self.assertFalse(
            abs(coupon.accruedAmount(accrualDate) - expectedAmount) > 1e-8)

        IndexManager.instance().clearHistories()
