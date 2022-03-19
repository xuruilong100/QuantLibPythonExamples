import unittest
from utilities import *
from QuantLib import *


class CashFlowsTest(unittest.TestCase):

    def testSettings(self):
        TEST_MESSAGE("Testing cash-flow settings...")

        backup = SavedSettings()

        today = Date.todaysDate()
        Settings.instance().evaluationDate = today

        # cash flows at T+0, T+1, T+2
        leg = []
        # leg.reserve(3)
        for i in range(3):
            leg.append(SimpleCashFlow(1.0, today + Period(i, Days)))

        def CHECK_INCLUSION(n, days, expected):
            self.assertFalse(
                (not leg[n].hasOccurred(today + Period(days, Days))) != expected)

        # define CHECK_INCLUSION(n, days, expected) \
        # if ((!leg[n].hasOccurred(today+days)) != expected) { \
        #     BOOST_ERROR("cashflow at T+" << n << " " \
        #                 << (expected ? "not" in "") << "included" \
        #                 << " at T+" << days) \
        # }

        # case 1: don't include reference-date payments, no override at
        #         today's date

        Settings.instance().includeReferenceDateEvents = false
        Settings.instance().includeTodaysCashFlows = None

        CHECK_INCLUSION(0, 0, false)
        CHECK_INCLUSION(0, 1, false)

        CHECK_INCLUSION(1, 0, true)
        CHECK_INCLUSION(1, 1, false)
        CHECK_INCLUSION(1, 2, false)

        CHECK_INCLUSION(2, 1, true)
        CHECK_INCLUSION(2, 2, false)
        CHECK_INCLUSION(2, 3, false)

        # case 2: same, but with explicit setting at today's date

        Settings.instance().includeReferenceDateEvents = false
        Settings.instance().includeTodaysCashFlows = false

        CHECK_INCLUSION(0, 0, false)
        CHECK_INCLUSION(0, 1, false)

        CHECK_INCLUSION(1, 0, true)
        CHECK_INCLUSION(1, 1, false)
        CHECK_INCLUSION(1, 2, false)

        CHECK_INCLUSION(2, 1, true)
        CHECK_INCLUSION(2, 2, false)
        CHECK_INCLUSION(2, 3, false)

        # case 3: do include reference-date payments, no override at
        #         today's date

        Settings.instance().includeReferenceDateEvents = true
        Settings.instance().includeTodaysCashFlows = None

        CHECK_INCLUSION(0, 0, true)
        CHECK_INCLUSION(0, 1, false)

        CHECK_INCLUSION(1, 0, true)
        CHECK_INCLUSION(1, 1, true)
        CHECK_INCLUSION(1, 2, false)

        CHECK_INCLUSION(2, 1, true)
        CHECK_INCLUSION(2, 2, true)
        CHECK_INCLUSION(2, 3, false)

        # case 4: do include reference-date payments, explicit (and same)
        #         setting at today's date

        Settings.instance().includeReferenceDateEvents = true
        Settings.instance().includeTodaysCashFlows = true

        CHECK_INCLUSION(0, 0, true)
        CHECK_INCLUSION(0, 1, false)

        CHECK_INCLUSION(1, 0, true)
        CHECK_INCLUSION(1, 1, true)
        CHECK_INCLUSION(1, 2, false)

        CHECK_INCLUSION(2, 1, true)
        CHECK_INCLUSION(2, 2, true)
        CHECK_INCLUSION(2, 3, false)

        # case 5: do include reference-date payments, override at
        #         today's date

        Settings.instance().includeReferenceDateEvents = true
        Settings.instance().includeTodaysCashFlows = false

        CHECK_INCLUSION(0, 0, false)
        CHECK_INCLUSION(0, 1, false)

        CHECK_INCLUSION(1, 0, true)
        CHECK_INCLUSION(1, 1, true)
        CHECK_INCLUSION(1, 2, false)

        CHECK_INCLUSION(2, 1, true)
        CHECK_INCLUSION(2, 2, true)
        CHECK_INCLUSION(2, 3, false)

        # no discount to make calculations easier
        no_discount = InterestRate(0.0, Actual365Fixed(), Continuous, Annual)

        def CHECK_NPV(includeRef, expected):
            NPV = CashFlows.npv(leg, no_discount, includeRef, today)
            self.assertFalse(abs(NPV - expected) > 1e-6)

        # define CHECK_NPV(includeRef, expected)                             \
        # do {                                                            \
        #     NPV = CashFlows.npv(leg, no_discount, includeRef, today) \
        #     if (abs(NPV - expected) > 1e-6) {                         \
        #         BOOST_ERROR("NPV mismatch:\n"                               \
        #                     << "    calculated: " << NPV << "\n"            \
        #                     << "    expected: " << expected)               \
        #     }                                                               \
        # } while (false)

        # no override
        Settings.instance().includeTodaysCashFlows = None

        CHECK_NPV(false, 2.0)
        CHECK_NPV(true, 3.0)

        # override
        Settings.instance().includeTodaysCashFlows = false

        CHECK_NPV(false, 2.0)
        CHECK_NPV(true, 2.0)

    def testAccessViolation(self):
        TEST_MESSAGE("Testing dynamic cast of coupon in Black pricer...")

        backup = SavedSettings()

        todaysDate = Date(7, April, 2010)
        settlementDate = Date(9, April, 2010)
        Settings.instance().evaluationDate = todaysDate
        calendar = TARGET()

        rhTermStructure = YieldTermStructureHandle(
            flatRate(settlementDate, 0.04875825, Actual365Fixed()))

        volatility = 0.10
        vol = OptionletVolatilityStructureHandle(
            ConstantOptionletVolatility(
                2,
                calendar,
                ModifiedFollowing,
                volatility,
                Actual365Fixed()))

        index3m = USDLibor(
            Period(3, Months), rhTermStructure)

        payDate = Date(20, December, 2013)
        startDate = Date(20, September, 2013)
        endDate = Date(20, December, 2013)
        spread = 0.0115
        pricer = BlackIborCouponPricer(vol)
        coupon = FloatingRateCoupon(
            payDate, 100, startDate, endDate, 2,
            index3m, 1.0, spread / 100)
        coupon.setPricer(pricer)

        try:
            # this caused an access violation in version 1.0
            coupon.amount()

        except Exception as e:
            print(e)
            # ok proper exception thrown

    def testDefaultSettlementDate(self):
        TEST_MESSAGE("Testing default evaluation date in cashflows methods...")
        today = Settings.instance().evaluationDate
        schedule = MakeSchedule()
        schedule.fromDate(
            today - Period(2, Months)).to(today + Period(4, Months))
        schedule.withFrequency(Semiannual)
        schedule.withCalendar(TARGET())
        schedule.withConvention(Unadjusted)
        schedule.backwards()
        schedule = schedule.makeSchedule()

        leg = FixedRateLeg(schedule)
        leg.withNotionals(100.0)
        leg.withCouponRates(0.03, Actual360())
        leg.withPaymentCalendar(TARGET())
        leg.withPaymentAdjustment(Following)
        leg = leg.makeLeg()

        accruedPeriod = CashFlows.accruedPeriod(leg, false)
        self.assertFalse(accruedPeriod == 0.0)

        accruedDays = CashFlows.accruedDays(leg, false)
        self.assertFalse(accruedDays == 0)

        accruedAmount = CashFlows.accruedAmount(leg, false)
        self.assertFalse(accruedAmount == 0.0)

    def testExCouponDates(self):
        TEST_MESSAGE("Testing ex-coupon date calculation...")

        today = Date.todaysDate()
        schedule = MakeSchedule()
        schedule.fromDate(today)
        schedule.to(today + Period(5, Years))
        schedule.withFrequency(Monthly)
        schedule.withCalendar(TARGET())
        schedule.withConvention(Following)
        schedule = schedule.makeSchedule()

        # no ex-coupon dates
        l1 = FixedRateLeg(schedule)
        l1.withNotionals(100.0)
        l1.withCouponRates(0.03, Actual360())
        l1 = l1.makeLeg()
        for i in l1:
            c = as_coupon(i)
            self.assertFalse(c.exCouponDate() != Date())

        # same for floating legs
        index = Euribor3M()
        l2 = IborLeg(schedule, index)
        l2.withNotionals(100.0)
        l2 = l2.makeLeg()
        for i in l2:
            c = as_coupon(i)
            self.assertFalse(c.exCouponDate() != Date())

        # calendar days
        l5 = FixedRateLeg(schedule)
        l5.withNotionals(100.0)
        l5.withCouponRates(0.03, Actual360())
        l5.withExCouponPeriod(
            Period(2, Days), NullCalendar(), Unadjusted, false)
        l5 = l5.makeLeg()

        for i in l5:
            c = as_coupon(i)
            expected = c.accrualEndDate() - 2
            self.assertFalse(c.exCouponDate() != expected)

        l6 = IborLeg(schedule, index)
        l6.withNotionals(100.0)
        l6.withExCouponPeriod(
            Period(2, Days), NullCalendar(), Unadjusted, false)
        l6 = l6.makeLeg()
        for i in l6:
            c = as_coupon(i)
            expected = c.accrualEndDate() - 2
            self.assertFalse(c.exCouponDate() != expected)

        # business days
        l7 = FixedRateLeg(schedule)
        l7.withNotionals(100.0)
        l7.withCouponRates(0.03, Actual360())
        l7.withExCouponPeriod(
            Period(2, Days), TARGET(), Preceding, false)
        l7 = l7.makeLeg()
        for i in l7:
            c = as_coupon(i)
            expected = TARGET().advance(c.accrualEndDate(), -2, Days)
            self.assertFalse(c.exCouponDate() != expected)

        l8 = IborLeg(schedule, index)
        l8.withNotionals(100.0)
        l8.withExCouponPeriod(
            Period(2, Days), TARGET(), Preceding, false)
        l8 = l8.makeLeg()
        for i in l8:
            c = as_coupon(i)
            expected = TARGET().advance(c.accrualEndDate(), -2, Days)
            self.assertFalse(c.exCouponDate() != expected)

    def testNullFixingDays(self):
        TEST_MESSAGE("Testing ibor leg construction with null fixing days...")
        today = Settings.instance().evaluationDate
        schedule = MakeSchedule()
        schedule.fromDate(
            today - Period(2, Months)).to(today + Period(4, Months))
        schedule.withFrequency(Semiannual)
        schedule.withCalendar(TARGET())
        schedule.withConvention(Following)
        schedule.backwards()
        schedule = schedule.makeSchedule()

        index = USDLibor(Period(6, Months))
        leg = IborLeg(schedule, index)
        leg.withNotionals(100.0)
        # this can happen with default values, and caused an
        # exception when the null was not managed properly
        leg.withFixingDays(NullNatural())

    def testIrregularFirstCouponReferenceDatesAtEndOfMonth(self):
        TEST_MESSAGE("Testing irregular first coupon reference dates with end of month enabled...")
        schedule = MakeSchedule()
        schedule.fromDate(
            Date(17, January, 2017)).to(Date(28, February, 2018))
        schedule.withFrequency(Semiannual)
        schedule.withConvention(Unadjusted)
        schedule.endOfMonth()
        schedule.backwards()
        schedule = schedule.makeSchedule()

        leg = FixedRateLeg(schedule)
        leg.withNotionals(100.0)
        leg.withCouponRates(0.01, Actual360())
        leg = leg.makeLeg()

        firstCoupon = as_coupon(leg[0])

        self.assertFalse(
            firstCoupon.referencePeriodStart() != Date(31, August, 2016))

    def testIrregularLastCouponReferenceDatesAtEndOfMonth(self):
        TEST_MESSAGE("Testing irregular last coupon reference dates with end of month enabled...")
        schedule = MakeSchedule()
        schedule.fromDate(Date(17, January, 2017)).to(Date(15, September, 2018))
        schedule.withNextToLastDate(Date(28, February, 2018))
        schedule.withFrequency(Semiannual)
        schedule.withConvention(Unadjusted)
        schedule.endOfMonth()
        schedule.backwards()
        schedule = schedule.makeSchedule()

        leg = FixedRateLeg(schedule)
        leg.withNotionals(100.0)
        leg.withCouponRates(0.01, Actual360())
        leg = leg.makeLeg()

        lastCoupon = as_coupon(leg[-1])

        self.assertFalse(lastCoupon.referencePeriodEnd() != Date(31, August, 2018))

    def testPartialScheduleLegConstruction(self):
        TEST_MESSAGE("Testing leg construction with partial schedule...")
        # schedule with irregular first and last period
        schedule = MakeSchedule()
        schedule.fromDate(Date(15, September, 2017))
        schedule.to(Date(30, September, 2020))
        schedule.withNextToLastDate(Date(25, September, 2020))
        schedule.withFrequency(Semiannual)
        schedule.backwards()
        schedule = schedule.makeSchedule()
        # same schedule, date based, with metadata
        schedule2 = Schedule(
            schedule.dates(), NullCalendar(), Unadjusted, Unadjusted,
            Period(6, Months), None, schedule.endOfMonth(),
            schedule.isRegular())
        # same schedule, date based, without metadata
        schedule3 = Schedule(schedule.dates())

        # fixed rate legs based on the three schedule
        leg = FixedRateLeg(schedule)
        leg.withNotionals(100.0)
        leg.withCouponRates(
            0.01, ActualActual(ActualActual.ISMA))
        leg2 = FixedRateLeg(schedule2)
        leg2.withNotionals(100.0)
        leg2.withCouponRates(
            0.01, ActualActual(ActualActual.ISMA))
        leg3 = FixedRateLeg(schedule3)
        leg3.withNotionals(100.0)
        leg3.withCouponRates(
            0.01, ActualActual(ActualActual.ISMA))

        leg = leg.makeLeg()
        leg2 = leg2.makeLeg()
        leg3 = leg3.makeLeg()

        # check reference period of first and last coupon in all variants
        # for the first two we expect a 6M reference period, for the
        # third it can not be constructed, so should be equal to the
        # respective schedule period
        firstCpn = as_fixed_rate_coupon(leg[0])
        lastCpn = as_fixed_rate_coupon(leg[-1])
        # self.assertTrue(firstCpn != nullptr)
        # self.assertTrue(lastCpn != nullptr)
        self.assertEqual(firstCpn.referencePeriodStart(), Date(25, Mar, 2017))
        self.assertEqual(firstCpn.referencePeriodEnd(), Date(25, Sep, 2017))
        self.assertEqual(lastCpn.referencePeriodStart(), Date(25, Sep, 2020))
        self.assertEqual(lastCpn.referencePeriodEnd(), Date(25, Mar, 2021))

        firstCpn2 = as_fixed_rate_coupon(leg2[0])
        lastCpn2 = as_fixed_rate_coupon(leg2[-1])
        # self.assertTrue(firstCpn2 != nullptr)
        # self.assertTrue(lastCpn2 != nullptr)
        self.assertEqual(firstCpn2.referencePeriodStart(), Date(25, Mar, 2017))
        self.assertEqual(firstCpn2.referencePeriodEnd(), Date(25, Sep, 2017))
        self.assertEqual(lastCpn2.referencePeriodStart(), Date(25, Sep, 2020))
        self.assertEqual(lastCpn2.referencePeriodEnd(), Date(25, Mar, 2021))

        firstCpn3 = as_fixed_rate_coupon(leg3[0])
        lastCpn3 = as_fixed_rate_coupon(leg3[-1])
        # self.assertTrue(firstCpn3 != nullptr)
        # self.assertTrue(lastCpn3 != nullptr)
        self.assertEqual(firstCpn3.referencePeriodStart(), Date(15, Sep, 2017))
        self.assertEqual(firstCpn3.referencePeriodEnd(), Date(25, Sep, 2017))
        self.assertEqual(lastCpn3.referencePeriodStart(), Date(25, Sep, 2020))
        self.assertEqual(lastCpn3.referencePeriodEnd(), Date(30, Sep, 2020))

        # same check as above for a floating leg
        iborIndex = USDLibor(Period(3, Months))
        legf = IborLeg(schedule, iborIndex)
        legf.withNotionals(100.0)
        legf.withPaymentDayCounter(ActualActual(ActualActual.ISMA))
        legf2 = IborLeg(schedule2, iborIndex)
        legf2.withNotionals(100.0)
        legf2.withPaymentDayCounter(ActualActual(ActualActual.ISMA))
        legf3 = IborLeg(schedule3, iborIndex)
        legf3.withNotionals(100.0)
        legf3.withPaymentDayCounter(ActualActual(ActualActual.ISMA))

        legf = legf.makeLeg()
        legf2 = legf2.makeLeg()
        legf3 = legf3.makeLeg()

        firstCpnF = as_floating_rate_coupon(legf[0])
        lastCpnF = as_floating_rate_coupon(legf[-1])
        # self.assertTrue(firstCpnF != nullptr)
        # self.assertTrue(lastCpnF != nullptr)
        self.assertEqual(firstCpnF.referencePeriodStart(), Date(25, Mar, 2017))
        self.assertEqual(firstCpnF.referencePeriodEnd(), Date(25, Sep, 2017))
        self.assertEqual(lastCpnF.referencePeriodStart(), Date(25, Sep, 2020))
        self.assertEqual(lastCpnF.referencePeriodEnd(), Date(25, Mar, 2021))

        firstCpnF2 = as_floating_rate_coupon(legf2[0])
        lastCpnF2 = as_floating_rate_coupon(legf2[-1])
        # self.assertTrue(firstCpnF2 != nullptr)
        # self.assertTrue(lastCpnF2 != nullptr)
        self.assertEqual(firstCpnF2.referencePeriodStart(), Date(25, Mar, 2017))
        self.assertEqual(firstCpnF2.referencePeriodEnd(), Date(25, Sep, 2017))
        self.assertEqual(lastCpnF2.referencePeriodStart(), Date(25, Sep, 2020))
        self.assertEqual(lastCpnF2.referencePeriodEnd(), Date(25, Mar, 2021))

        firstCpnF3 = as_floating_rate_coupon(legf3[0])
        lastCpnF3 = as_floating_rate_coupon(legf3[-1])
        # self.assertTrue(firstCpnF3 != nullptr)
        # self.assertTrue(lastCpnF3 != nullptr)
        self.assertEqual(firstCpnF3.referencePeriodStart(), Date(15, Sep, 2017))
        self.assertEqual(firstCpnF3.referencePeriodEnd(), Date(25, Sep, 2017))
        self.assertEqual(lastCpnF3.referencePeriodStart(), Date(25, Sep, 2020))
        self.assertEqual(lastCpnF3.referencePeriodEnd(), Date(30, Sep, 2020))

    def testFixedIborCouponWithoutForecastCurve(self):
        TEST_MESSAGE("Testing past ibor coupon without forecast curve...")

        # IndexHistoryCleaner cleaner

        today = Settings.instance().evaluationDate

        index = USDLibor(Period(6, Months))
        calendar = index.fixingCalendar()

        fixingDate = calendar.advance(today, -2, Months)
        pastFixing = 0.01
        index.addFixing(fixingDate, pastFixing)

        startDate = index.valueDate(fixingDate)
        endDate = index.maturityDate(fixingDate)

        coupon = IborCoupon(
            endDate, 100.0, startDate, endDate, index.fixingDays(), index)
        coupon.setPricer(BlackIborCouponPricer())

        # BOOST_CHECK_NO_THROW(coupon.amount())
        try:
            coupon.amount()
        except Exception as e:
            no_throw = false
            self.assertTrue(no_throw)

        # the main check is the one above, but let's check for consistency too:
        amount = coupon.amount()
        expected = pastFixing * coupon.nominal() * coupon.accrualPeriod()
        self.assertFalse(abs(amount - expected) > 1e-8)
