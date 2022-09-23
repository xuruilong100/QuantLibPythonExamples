import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.settlementDays = 2
        self.calendar = TARGET()
        self.dayCount = Actual365Fixed()
        self.businessConvention = ModifiedFollowing
        self.euriborHandle = RelinkableYieldTermStructureHandle()
        self.euribor = Euribor6M(self.euriborHandle)
        self.euribor.addFixing(Date(8, February, 2021), 0.0085)
        self.euribor.addFixing(Date(9, February, 2021), 0.0085)
        self.euribor.addFixing(Date(10, February, 2021), 0.0085)

        self.today = self.calendar.adjust(Date(15, March, 2021))
        Settings.instance().evaluationDate = self.today
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)

        self.euriborHandle.linkTo(flatRate(self.settlement, 0.007, self.dayCount))

    def createIborLeg(self, start, end, spread, fixingDays=2):
        sch = MakeSchedule()
        sch.fromDate(start)
        sch.to(end)
        sch.withTenor(self.euribor.tenor())
        sch.withCalendar(self.euribor.fixingCalendar())
        sch.withConvention(self.euribor.businessDayConvention())
        sch.backwards()
        sch = sch.makeSchedule()
        leg = IborLeg(sch, self.euribor)
        leg.withNotionals(1.0)
        leg.withSpreads(spread)
        leg.withExCouponPeriod(
            Period(2, Days), self.calendar, self.businessConvention)
        leg.withPaymentLag(1)
        leg.withFixingDays(fixingDays)

        return leg

    def createSubPeriodsCoupon(self,
                               start,
                               end,
                               rateSpread=0.0,
                               couponSpread=0.0,
                               averaging=RateAveraging.Compound,
                               fixingDays=2):
        paymentCalendar = self.euribor.fixingCalendar()
        paymentBdc = self.euribor.businessDayConvention()
        paymentDate = paymentCalendar.advance(end, Period(1, Days), paymentBdc)
        exCouponDate = paymentCalendar.advance(
            paymentDate, -Period(2, Days), paymentBdc)
        cpn = SubPeriodsCoupon(
            paymentDate, 1.0, start, end, fixingDays,
            self.euribor, 1.0, couponSpread,
            rateSpread, Date(), Date(), DayCounter(), exCouponDate)
        useCompoundedRate = (averaging == RateAveraging.Compound)
        if useCompoundedRate:
            cpn.setPricer(
                CompoundingRatePricer())
        else:
            cpn.setPricer(
                AveragingRatePricer())
        return cpn

    def createSubPeriodsLeg(self,
                            start,
                            end,
                            cpnFrequency,
                            rateSpread=0.0,
                            couponSpread=0.0,
                            averaging=RateAveraging.Compound,
                            fixingDays=2):
        sch = MakeSchedule()
        sch.fromDate(start)
        sch.to(end)
        sch.withTenor(cpnFrequency)
        sch.withCalendar(self.euribor.fixingCalendar())
        sch.withConvention(self.euribor.businessDayConvention())
        sch.backwards()
        sch = sch.makeSchedule()
        leg = SubPeriodsLeg(sch, self.euribor)
        leg.withNotionals(1.0)
        leg.withExCouponPeriod(Period(2, Days), self.calendar, self.businessConvention)
        leg.withPaymentLag(1)
        leg.withFixingDays(fixingDays)
        leg.withRateSpreads(rateSpread)
        leg.withCouponSpreads(couponSpread)
        leg.withAveragingMethod(averaging)

        return leg


def sumIborLegPayments(leg):
    payments = 0.0

    for cf in leg:
        payments += cf.amount()
    return payments


def compoundedIborLegPayment(leg):
    compound = 1.0

    for cf in leg:
        cpn = as_ibor_coupon(cf)
        yearFraction = cpn.accrualPeriod()
        fixing = cpn.indexFixing()
        compound *= (1.0 + yearFraction * (fixing + cpn.spread()))
    return (compound - 1.0)


def averagedIborLegPayment(leg):
    acc = 0.0

    for cf in leg:
        cpn = as_ibor_coupon(cf)
        yearFraction = cpn.accrualPeriod()
        fixing = cpn.indexFixing()
        acc += yearFraction * (fixing + cpn.spread())
    return acc


class SubPeriodsCouponTest(unittest.TestCase):

    def testRegularSinglePeriodForwardStartingCoupon(self):
        TEST_MESSAGE(
            "Testing regular single period forward starting coupon...")

        start = Date(15, April, 2021)
        end = Date(15, October, 2021)

        spread = 0.001

        self._testSinglePeriodCouponReplication(
            start, end, spread, RateAveraging.Compound, 2)
        self._testSinglePeriodCouponReplication(
            start, end, spread, RateAveraging.Simple, 4)

    def testRegularSinglePeriodCouponAfterFixing(self):
        TEST_MESSAGE(
            "Testing regular single period coupon after fixing...")

        start = Date(12, February, 2021)
        end = Date(12, August, 2021)

        spread = 0.001

        self._testSinglePeriodCouponReplication(
            start, end, spread, RateAveraging.Compound, 3)
        self._testSinglePeriodCouponReplication(
            start, end, spread, RateAveraging.Simple, 4)

    def testIrregularSinglePeriodCouponAfterFixing(self):
        TEST_MESSAGE(
            "Testing irregular single period coupon after fixing...")

        start = Date(12, February, 2021)
        end = Date(12, June, 2021)

        spread = 0.001

        self._testSinglePeriodCouponReplication(
            start, end, spread, RateAveraging.Compound, 3)
        self._testSinglePeriodCouponReplication(
            start, end, spread, RateAveraging.Simple, 2)

    def testRegularCompoundedForwardStartingCouponWithMultipleSubPeriods(self):
        TEST_MESSAGE(
            "Testing regular forward starting coupon with multiple compounded sub-periods...")

        start = Date(15, April, 2021)
        end = Date(15, April, 2022)

        spread = 0.001
        self._testMultipleCompoundedSubPeriodsCouponReplication(start, end, spread)

    def testRegularAveragedForwardStartingCouponWithMultipleSubPeriods(self):
        TEST_MESSAGE(
            "Testing regular forward starting coupon with multiple averaged sub-periods...")

        start = Date(15, April, 2021)
        end = Date(15, April, 2022)

        spread = 0.001
        self._testMultipleAveragedSubPeriodsCouponReplication(start, end, spread)

    def testExCouponCashFlow(self):
        TEST_MESSAGE(
            "Testing ex-coupon cash flow...")

        vars = CommonVars()

        start = Date(12, February, 2021)
        end = Date(17, March, 2021)
        cfs = Leg(1)
        cfs[0] = vars.createSubPeriodsCoupon(start, end)

        npv = CashFlows.npv(
            cfs, vars.euriborHandle.currentLink(), false, vars.settlement, vars.settlement)

        tolerance = 1.0e-14

        self.assertFalse(abs(npv) > tolerance)

    def testSubPeriodsLegCashFlows(self):
        TEST_MESSAGE(
            "Testing sub-periods leg replication...")

        self._testSubPeriodsLegReplication(RateAveraging.Compound)
        self._testSubPeriodsLegReplication(RateAveraging.Simple)

    def testSubPeriodsLegConsistencyChecks(self):
        TEST_MESSAGE(
            "Testing sub-periods leg consistency checks...")

        vars = CommonVars()

        start = Date(18, March, 2021)
        end = Date(18, March, 2031)

        subPeriodLeg = vars.createSubPeriodsLeg(start, end, Period(1, Years))

        self.assertRaises(
            Exception, lambda l: l.makeLeg(),
            vars.createSubPeriodsLeg(start, end, Period(1, Years)).withNotionals(DoubleVector()))
        self.assertRaises(
            Exception, lambda l: l.makeLeg(),
            vars.createSubPeriodsLeg(start, end, Period(1, Years)).withNotionals(DoubleVector(11, 1.0)))
        self.assertRaises(
            Exception, lambda l: l.makeLeg(),
            vars.createSubPeriodsLeg(start, end, Period(1, Years)).withFixingDays(NaturalVector(11, 2)))
        self.assertRaises(
            Exception, lambda l: l.makeLeg(),
            vars.createSubPeriodsLeg(start, end, Period(1, Years)).withGearings(0.0))
        self.assertRaises(
            Exception, lambda l: l.makeLeg(),
            vars.createSubPeriodsLeg(start, end, Period(1, Years)).withGearings(DoubleVector(11, 1.0)))
        self.assertRaises(
            Exception, lambda l: l.makeLeg(),
            vars.createSubPeriodsLeg(start, end, Period(1, Years)).withCouponSpreads(DoubleVector(11, 0.0)))
        self.assertRaises(
            Exception, lambda l: l.makeLeg(),
            vars.createSubPeriodsLeg(start, end, Period(1, Years)).withRateSpreads(DoubleVector(11, 0.0)))

    def _testSinglePeriodCouponReplication(self,
                                           start,
                                           end,
                                           rateSpread,
                                           averaging,
                                           fixingDays):
        vars = CommonVars()

        iborLeg = vars.createIborLeg(start, end, rateSpread, fixingDays)
        iborLeg = iborLeg.makeLeg()
        couponSpread = 0.0
        subPeriodCpn = vars.createSubPeriodsCoupon(
            start, end, rateSpread, couponSpread, averaging, fixingDays)

        tolerance = 1.0e-14

        actualPayment = subPeriodCpn.amount()
        expectedPayment = sumIborLegPayments(iborLeg)

        self.assertFalse(abs(actualPayment - expectedPayment) > tolerance)

    def _testMultipleCompoundedSubPeriodsCouponReplication(self,
                                                           start,
                                                           end,
                                                           rateSpread):
        vars = CommonVars()

        iborLeg = vars.createIborLeg(start, end, rateSpread)
        iborLeg = iborLeg.makeLeg()
        couponSpread = 0.0
        subPeriodCpn = vars.createSubPeriodsCoupon(
            start, end, rateSpread, couponSpread, RateAveraging.Compound)

        tolerance = 1.0e-14

        actualPayment = subPeriodCpn.amount()
        expectedPayment = compoundedIborLegPayment(iborLeg)

        self.assertFalse(abs(actualPayment - expectedPayment) > tolerance)

    def _testMultipleAveragedSubPeriodsCouponReplication(self,
                                                         start,
                                                         end,
                                                         rateSpread):
        vars = CommonVars()

        iborLeg = vars.createIborLeg(start, end, rateSpread)
        iborLeg = iborLeg.makeLeg()
        couponSpread = 0.0
        subPeriodCpn = vars.createSubPeriodsCoupon(
            start, end, rateSpread, couponSpread, RateAveraging.Simple)

        tolerance = 1.0e-14

        actualPayment = subPeriodCpn.amount()
        expectedPayment = averagedIborLegPayment(iborLeg)

        self.assertFalse(abs(actualPayment - expectedPayment) > tolerance)

    def _testSubPeriodsLegReplication(self,
                                      averaging):
        vars = CommonVars()

        start = Date(18, March, 2021)
        end = Date(18, March, 2022)

        rateSpread = 0.001
        couponSpread = 0.002

        subPeriodCpn = vars.createSubPeriodsCoupon(
            start, end, rateSpread, couponSpread, averaging)

        subPeriodLeg = vars.createSubPeriodsLeg(
            start, end, Period(1, Years), rateSpread, couponSpread, averaging)
        subPeriodLeg = subPeriodLeg.makeLeg()

        tolerance = 1.0e-14

        actualPayment = 0.0

        for s in subPeriodLeg:
            actualPayment += s.amount()
        expectedPayment = subPeriodCpn.amount()

        self.assertFalse(abs(actualPayment - expectedPayment) > tolerance)
