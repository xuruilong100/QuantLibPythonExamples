import unittest
from utilities import *
from QuantLib import *


class Globals(object):

    def __init__(self):
        self.calendar = TARGET()
        self.dayCounter = Actual365Fixed()
        self.rollingConvention = ModifiedFollowing

        self.today = Date.todaysDate()
        Settings.instance().evaluationDate = self.today
        self.settlement = self.calendar.advance(self.today, 2, Days)
        self.backup = SavedSettings()
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.model = RelinkableShortRateModelHandle()

    def issueDate(self):
        # ensure that we're in mid-coupon
        return self.calendar.adjust(self.today - Period(100, Days))

    def maturityDate(self):
        # ensure that we're in mid-coupon
        return self.calendar.advance(self.issueDate(), 10, Years)

    def evenYears(self):
        dates = DateVector()
        for i in range(2, 10, 2):  # (i = 2 i < 10 i += 2)
            dates.push_back(self.calendar.advance(self.issueDate(), i, Years))
        return dates

    def oddYears(self):
        dates = DateVector()
        for i in range(1, 10, 2):  # (i = 1 i < 10 i += 2)
            dates.push_back(self.calendar.advance(self.issueDate(), i, Years))
        return dates

    def makeFlatCurve(self, r):
        return FlatForward(self.settlement, r, self.dayCounter)


class CallableBondTest(unittest.TestCase):

    def testConsistency(self):
        TEST_MESSAGE("Testing consistency of callable bonds...")

        vars = Globals()

        vars.termStructure.linkTo(vars.makeFlatCurve(0.032))
        vars.model.linkTo(HullWhite(vars.termStructure))

        schedule = MakeSchedule()
        schedule.fromDate(vars.issueDate())
        schedule.to(vars.maturityDate())
        schedule.withCalendar(vars.calendar)
        schedule.withFrequency(Semiannual)
        schedule.withConvention(vars.rollingConvention)
        schedule.withRule(DateGeneration.Backward)
        schedule = schedule.makeSchedule()

        coupons = DoubleVector(1, 0.05)

        bond = FixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis))
        bond.setPricingEngine(
            DiscountingBondEngine(vars.termStructure))

        callabilities = CallabilitySchedule()
        callabilityDates = vars.evenYears()
        for callabilityDate in callabilityDates:
            callabilities.push_back(Callability(
                BondPrice(110.0, BondPrice.Clean),
                Callability.Call, callabilityDate))

        puttabilities = CallabilitySchedule()
        puttabilityDates = vars.oddYears()
        for puttabilityDate in puttabilityDates:
            puttabilities.push_back(
                Callability(
                    BondPrice(90.0, BondPrice.Clean),
                    Callability.Put, puttabilityDate))

        timeSteps = 240

        engine = TreeCallableFixedRateBondEngine(
            vars.model.currentLink(), timeSteps, vars.termStructure)

        callable = CallableFixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis),
            vars.rollingConvention,
            100.0, vars.issueDate(),
            callabilities)
        callable.setPricingEngine(engine)

        puttable = CallableFixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis),
            vars.rollingConvention,
            100.0, vars.issueDate(),
            puttabilities)
        puttable.setPricingEngine(engine)

        self.assertFalse(bond.cleanPrice() <= callable.cleanPrice())
        self.assertFalse(bond.cleanPrice() >= puttable.cleanPrice())

    def testInterplay(self):
        TEST_MESSAGE("Testing interplay of callability and puttability for callable bonds...")

        vars = Globals()

        vars.termStructure.linkTo(vars.makeFlatCurve(0.03))
        vars.model.linkTo(HullWhite(vars.termStructure))

        timeSteps = 240

        engine = TreeCallableZeroCouponBondEngine(
            vars.model.currentLink(), timeSteps, vars.termStructure)

        # case 1: an earlier out-of-the-money callability must prevent
        #         a later in-the-money puttability

        callabilities = CallabilitySchedule()

        callabilities.push_back(Callability(
            BondPrice(100.0, BondPrice.Clean),
            Callability.Call,
            vars.calendar.advance(vars.issueDate(), 4, Years)))

        callabilities.push_back(Callability(
            BondPrice(1000.0, BondPrice.Clean),
            Callability.Put,
            vars.calendar.advance(vars.issueDate(), 6, Years)))

        bond = CallableZeroCouponBond(
            3, 100.0, vars.calendar,
            vars.maturityDate(), Thirty360(Thirty360.BondBasis),
            vars.rollingConvention, 100.0,
            vars.issueDate(), callabilities)
        bond.setPricingEngine(engine)

        expected = callabilities[0].price().amount() * \
                   vars.termStructure.discount(callabilities[0].date()) / \
                   vars.termStructure.discount(bond.settlementDate())

        self.assertFalse(abs(bond.settlementValue() - expected) > 1.0e-2)

        # case 2: same as case 1, with an added callability later on

        callabilities.push_back(Callability(
            BondPrice(100.0, BondPrice.Clean),
            Callability.Call,
            vars.calendar.advance(vars.issueDate(), 8, Years)))

        bond = CallableZeroCouponBond(
            3, 100.0, vars.calendar,
            vars.maturityDate(), Thirty360(Thirty360.BondBasis),
            vars.rollingConvention, 100.0,
            vars.issueDate(), callabilities)
        bond.setPricingEngine(engine)

        self.assertFalse(abs(bond.settlementValue() - expected) > 1.0e-2)

        # case 3: an earlier in-the-money puttability must prevent
        #         a later in-the-money callability

        callabilities.clear()

        callabilities.push_back(Callability(
            BondPrice(100.0, BondPrice.Clean),
            Callability.Put,
            vars.calendar.advance(vars.issueDate(), 4, Years)))

        callabilities.push_back(Callability(
            BondPrice(10.0, BondPrice.Clean),
            Callability.Call,
            vars.calendar.advance(vars.issueDate(), 6, Years)))

        bond = CallableZeroCouponBond(
            3, 100.0, vars.calendar,
            vars.maturityDate(), Thirty360(Thirty360.BondBasis),
            vars.rollingConvention, 100.0,
            vars.issueDate(), callabilities)
        bond.setPricingEngine(engine)

        expected = callabilities[0].price().amount() * \
                   vars.termStructure.discount(callabilities[0].date()) / \
                   vars.termStructure.discount(bond.settlementDate())

        self.assertFalse(abs(bond.settlementValue() - expected) > 1.0e-2)

        # case 4: same as case 3, with an added puttability later on

        callabilities.push_back(Callability(
            BondPrice(100.0, BondPrice.Clean),
            Callability.Put,
            vars.calendar.advance(vars.issueDate(), 8, Years)))

        bond = CallableZeroCouponBond(
            3, 100.0, vars.calendar,
            vars.maturityDate(), Thirty360(Thirty360.BondBasis),
            vars.rollingConvention, 100.0,
            vars.issueDate(), callabilities)
        bond.setPricingEngine(engine)

        self.assertFalse(abs(bond.settlementValue() - expected) > 1.0e-2)

    def testObservability(self):
        TEST_MESSAGE("Testing observability of callable bonds...")

        vars = Globals()

        observable = SimpleQuote(0.03)
        h = QuoteHandle(observable)
        vars.termStructure.linkTo(vars.makeFlatCurve(h))
        vars.model.linkTo(HullWhite(vars.termStructure))

        schedule = MakeSchedule()
        schedule.fromDate(vars.issueDate())
        schedule.to(vars.maturityDate())
        schedule.withCalendar(vars.calendar)
        schedule.withFrequency(Semiannual)
        schedule.withConvention(vars.rollingConvention)
        schedule.withRule(DateGeneration.Backward)
        schedule = schedule.makeSchedule()

        coupons = DoubleVector(1, 0.05)

        callabilities = CallabilitySchedule()

        callabilityDates = vars.evenYears()
        for callabilityDate in callabilityDates:
            callabilities.push_back(
                Callability(
                    BondPrice(110.0, BondPrice.Clean),
                    Callability.Call, callabilityDate))

        puttabilityDates = vars.oddYears()
        for puttabilityDate in puttabilityDates:
            callabilities.push_back(
                Callability(
                    BondPrice(90.0, BondPrice.Clean),
                    Callability.Put, puttabilityDate))

        bond = CallableZeroCouponBond(
            3, 100.0, vars.calendar,
            vars.maturityDate(),
            Thirty360(Thirty360.BondBasis),
            vars.rollingConvention, 100.0,
            vars.issueDate(), callabilities)

        timeSteps = 240

        engine = TreeCallableFixedRateBondEngine(
            vars.model.currentLink(), timeSteps, vars.termStructure)

        bond.setPricingEngine(engine)

        originalValue = bond.NPV()

        observable.setValue(0.04)

        self.assertFalse(bond.NPV() == originalValue)

    def testDegenerate(self):
        TEST_MESSAGE("Repricing bonds using degenerate callable bonds...")

        vars = Globals()

        vars.termStructure.linkTo(vars.makeFlatCurve(0.034))
        vars.model.linkTo(HullWhite(vars.termStructure))

        schedule = MakeSchedule()
        schedule.fromDate(vars.issueDate())
        schedule.to(vars.maturityDate())
        schedule.withCalendar(vars.calendar)
        schedule.withFrequency(Semiannual)
        schedule.withConvention(vars.rollingConvention)
        schedule.withRule(DateGeneration.Backward)
        schedule = schedule.makeSchedule()

        coupons = DoubleVector(1, 0.05)

        zeroCouponBond = ZeroCouponBond(
            3, vars.calendar, 100.0,
            vars.maturityDate(),
            vars.rollingConvention)
        couponBond = FixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis))

        # no callability
        callabilities = CallabilitySchedule()

        bond1 = CallableZeroCouponBond(
            3, 100.0, vars.calendar,
            vars.maturityDate(), Thirty360(Thirty360.BondBasis),
            vars.rollingConvention, 100.0,
            vars.issueDate(), callabilities)

        bond2 = CallableFixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis),
            vars.rollingConvention,
            100.0, vars.issueDate(),
            callabilities)

        discountingEngine = DiscountingBondEngine(vars.termStructure)

        zeroCouponBond.setPricingEngine(discountingEngine)
        couponBond.setPricingEngine(discountingEngine)

        timeSteps = 240

        treeEngine = TreeCallableFixedRateBondEngine(
            vars.model.currentLink(), timeSteps, vars.termStructure)

        bond1.setPricingEngine(treeEngine)
        bond2.setPricingEngine(treeEngine)

        tolerance = 1.0e-4

        self.assertFalse(abs(bond1.cleanPrice() - zeroCouponBond.cleanPrice()) > tolerance)
        self.assertFalse(abs(bond2.cleanPrice() - couponBond.cleanPrice()) > tolerance)

        # out-of-the-money callability

        callabilityDates = vars.evenYears()
        for callabilityDate in callabilityDates:
            callabilities.push_back(Callability(
                BondPrice(10000.0, BondPrice.Clean),
                Callability.Call, callabilityDate))

        puttabilityDates = vars.oddYears()
        for puttabilityDate in puttabilityDates:
            callabilities.push_back(
                Callability(
                    BondPrice(0.0, BondPrice.Clean),
                    Callability.Put, puttabilityDate))

        bond1 = CallableZeroCouponBond(
            3, 100.0, vars.calendar,
            vars.maturityDate(), Thirty360(Thirty360.BondBasis),
            vars.rollingConvention, 100.0,
            vars.issueDate(), callabilities)

        bond2 = CallableFixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis),
            vars.rollingConvention,
            100.0, vars.issueDate(),
            callabilities)

        bond1.setPricingEngine(treeEngine)
        bond2.setPricingEngine(treeEngine)

        self.assertFalse(abs(bond1.cleanPrice() - zeroCouponBond.cleanPrice()) > tolerance)

        self.assertFalse(abs(bond2.cleanPrice() - couponBond.cleanPrice()) > tolerance)

    def testCached(self):
        TEST_MESSAGE("Testing callable-bond value against cached values...")

        vars = Globals()

        vars.today = Date(3, June, 2004)
        Settings.instance().evaluationDate = vars.today
        vars.settlement = vars.calendar.advance(vars.today, 3, Days)

        vars.termStructure.linkTo(vars.makeFlatCurve(0.032))
        vars.model.linkTo(HullWhite(vars.termStructure))

        schedule = MakeSchedule()
        schedule.fromDate(vars.issueDate())
        schedule.to(vars.maturityDate())
        schedule.withCalendar(vars.calendar)
        schedule.withFrequency(Semiannual)
        schedule.withConvention(vars.rollingConvention)
        schedule.withRule(DateGeneration.Backward)
        schedule = schedule.makeSchedule()

        coupons = DoubleVector(1, 0.05)

        callabilities = CallabilitySchedule()
        puttabilities = CallabilitySchedule()
        all_exercises = CallabilitySchedule()

        callabilityDates = vars.evenYears()
        for callabilityDate in callabilityDates:
            exercise = Callability(
                BondPrice(110.0, BondPrice.Clean),
                Callability.Call, callabilityDate)
            callabilities.push_back(exercise)
            all_exercises.push_back(exercise)

        puttabilityDates = vars.oddYears()
        for puttabilityDate in puttabilityDates:
            exercise = Callability(
                BondPrice(100.0, BondPrice.Clean),
                Callability.Put, puttabilityDate)
            puttabilities.push_back(exercise)
            all_exercises.push_back(exercise)

        timeSteps = 240

        engine = TreeCallableFixedRateBondEngine(
            vars.model.currentLink(), timeSteps, vars.termStructure)

        tolerance = 1.0e-8

        storedPrice1 = 110.60975477
        bond1 = CallableFixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis),
            vars.rollingConvention,
            100.0, vars.issueDate(),
            callabilities)
        bond1.setPricingEngine(engine)

        self.assertFalse(abs(bond1.cleanPrice() - storedPrice1) > tolerance)

        storedPrice2 = 115.16559362
        bond2 = CallableFixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis),
            vars.rollingConvention,
            100.0, vars.issueDate(),
            puttabilities)
        bond2.setPricingEngine(engine)

        self.assertFalse(abs(bond2.cleanPrice() - storedPrice2) > tolerance)

        storedPrice3 = 110.97509625
        bond3 = CallableFixedRateBond(
            3, 100.0, schedule,
            coupons, Thirty360(Thirty360.BondBasis),
            vars.rollingConvention,
            100.0, vars.issueDate(),
            all_exercises)
        bond3.setPricingEngine(engine)

        self.assertFalse(abs(bond3.cleanPrice() - storedPrice3) > tolerance)

    def testSnappingExerciseDate2ClosestCouponDate(self):
        TEST_MESSAGE("Testing snap of callability dates to the closest coupon date...")

        # This is a test case inspired by
        # https:#github.com/lballabio/QuantLib/issues/930#issuecomment-853886024 */

        today = Date(18, May, 2021)
        calendar = UnitedStates(UnitedStates.FederalReserve)

        backup = SavedSettings()
        Settings.instance().evaluationDate = today

        def makeBonds(
                callDate):
            termStructure = RelinkableYieldTermStructureHandle()
            termStructure.linkTo(FlatForward(today, 0.02, Actual365Fixed()))

            settlementDays = 2
            settlementDate = Date(20, May, 2021)
            coupon = 0.05
            faceAmount = 100.00
            redemption = faceAmount
            accrualDCC = Thirty360(Thirty360.USA)
            maturityDate = Date(14, Feb, 2026)
            issueDate = settlementDate - Period(2 * 366, Days)
            schedule = MakeSchedule()
            schedule.fromDate(issueDate)
            schedule.to(maturityDate)
            schedule.withFrequency(Semiannual)
            schedule.withCalendar(calendar)
            schedule.withConvention(Unadjusted)
            schedule.withTerminationDateConvention(Unadjusted)
            schedule.backwards()
            schedule.endOfMonth(false)
            schedule = schedule.makeSchedule()
            coupons = DoubleVector(len(schedule) - 1, coupon)

            callabilitySchedule = CallabilitySchedule()
            callabilitySchedule.push_back(Callability(
                BondPrice(faceAmount, BondPrice.Clean), Callability.Call, callDate))

            newCallableBond = CallableFixedRateBond(
                settlementDays, faceAmount, schedule, coupons, accrualDCC,
                Following, redemption, issueDate, callabilitySchedule)

            model = HullWhite(termStructure, 1e-12, 0.003)
            treeEngine = TreeCallableFixedRateBondEngine(model, 40)
            newCallableBond.setPricingEngine(treeEngine)

            # callableBond.swap(newCallableBond)

            fixedRateBondSchedule = schedule.until(callDate)
            fixedRateBondCoupons = DoubleVector(len(schedule) - 1, coupon)

            newFixedRateBond = FixedRateBond(
                settlementDays, faceAmount, fixedRateBondSchedule,
                fixedRateBondCoupons, accrualDCC,
                Following, redemption, issueDate)
            discountigEngine = DiscountingBondEngine(termStructure)
            newFixedRateBond.setPricingEngine(discountigEngine)

            # fixedRateBond.swap(newFixedRateBond)

            return (newFixedRateBond, newCallableBond)

        initialCallDate = Date(14, Feb, 2022)
        tolerance = 1e-10

        for i in range(-10, 11):  # i = -10 i < 11):
            callDate = initialCallDate + Period(i, Days)
            if calendar.isBusinessDay(callDate):
                fixedRateBond, callableBond = makeBonds(callDate)
                npvFixedRateBond = fixedRateBond.NPV()
                npvCallable = callableBond.NPV()

                self.assertFalse(abs(npvCallable - npvFixedRateBond) > tolerance)
