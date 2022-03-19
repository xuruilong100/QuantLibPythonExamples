import unittest
from utilities import *
from QuantLib import *


class CommonVars(object):

    def __init__(self):
        self.calendar = TARGET()
        self.today = self.calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = self.today
        self.faceAmount = 1000000.0
        self.backup = SavedSettings()


class BondTest(unittest.TestCase):

    def testYield(self):
        TEST_MESSAGE("Testing consistency of bond price/bondYield calculation...")

        vars = CommonVars()

        tolerance = 1.0e-7
        maxEvaluations = 100

        issueMonths = [-24, -18, -12, -6, 0, 6, 12, 18, 24]
        lengths = [3, 5, 10, 15, 20]
        settlementDays = 3
        coupons = [0.02, 0.05, 0.08]
        frequencies = [Semiannual, Annual]
        bondDayCount = Thirty360(Thirty360.BondBasis)
        accrualConvention = Unadjusted
        paymentConvention = ModifiedFollowing
        redemption = 100.0

        yields = [0.03, 0.04, 0.05, 0.06, 0.07]
        compounding = [Compounded, Continuous]

        for issueMonth in issueMonths:
            for length in lengths:
                for coupon in coupons:
                    for frequencie in frequencies:
                        for n in compounding:

                            dated = vars.calendar.advance(
                                vars.today, issueMonth, Months)
                            issue = dated
                            maturity = vars.calendar.advance(
                                issue, length, Years)

                            sch = Schedule(
                                dated, maturity, Period(frequencie), vars.calendar,
                                accrualConvention, accrualConvention,
                                DateGeneration.Backward, false)

                            bond = FixedRateBond(
                                settlementDays, vars.faceAmount, sch,
                                DoubleVector(1, coupon), bondDayCount,
                                paymentConvention, redemption, issue)

                            for m in yields:

                                price = BondFunctions.cleanPrice(
                                    bond, m, bondDayCount, n, frequencie)

                                calculated = BondFunctions.bondYield(
                                    bond, price, bondDayCount, n, frequencie, Date(), tolerance,
                                    maxEvaluations, 0.05, BondPrice.Clean)

                                if abs(m - calculated) > tolerance:
                                    # the difference might not matter
                                    price2 = BondFunctions.cleanPrice(
                                        bond, calculated, bondDayCount, n, frequencie)
                                    self.assertFalse(abs(price - price2) / price > tolerance)

                                price = BondFunctions.dirtyPrice(
                                    bond, m, bondDayCount, n, frequencie)

                                calculated = BondFunctions.bondYield(
                                    bond, price, bondDayCount, n, frequencie, Date(), tolerance,
                                    maxEvaluations, 0.05, BondPrice.Dirty)

                                if abs(m - calculated) > tolerance:
                                    # the difference might not matter
                                    price2 = BondFunctions.dirtyPrice(
                                        bond, calculated, bondDayCount, n, frequencie)
                                    self.assertFalse(abs(price - price2) / price > tolerance)

    def testAtmRate(self):
        TEST_MESSAGE("Testing consistency of bond price/ATM rate calculation...")

        vars = CommonVars()

        tolerance = 1.0e-7

        issueMonths = [-24, -18, -12, -6, 0, 6, 12, 18, 24]
        lengths = [3, 5, 10, 15, 20]
        settlementDays = 3
        coupons = [0.02, 0.05, 0.08]
        frequencies = [Semiannual, Annual]
        bondDayCount = Thirty360(Thirty360.BondBasis)
        accrualConvention = Unadjusted
        paymentConvention = ModifiedFollowing
        redemption = 100.0
        disc = YieldTermStructureHandle(
            flatRate(vars.today, 0.03, Actual360()))
        bondEngine = DiscountingBondEngine(disc)

        for issueMonth in issueMonths:
            for length in lengths:
                for coupon in coupons:
                    for frequencie in frequencies:
                        dated = vars.calendar.advance(
                            vars.today, issueMonth, Months)
                        issue = dated
                        maturity = vars.calendar.advance(
                            issue, length, Years)

                        sch = Schedule(
                            dated, maturity, Period(frequencie), vars.calendar,
                            accrualConvention, accrualConvention,
                            DateGeneration.Backward, false)

                        bond = FixedRateBond(
                            settlementDays, vars.faceAmount, sch,
                            DoubleVector(1, coupon), bondDayCount,
                            paymentConvention, redemption, issue)

                        bond.setPricingEngine(bondEngine)
                        price = bond.cleanPrice()
                        calculated = BondFunctions.atmRate(
                            bond, disc.currentLink(), bond.settlementDate(), price)

                        self.assertFalse(abs(coupon - calculated) > tolerance)

    def testZspread(self):
        TEST_MESSAGE("Testing consistency of bond price/z-spread calculation...")

        vars = CommonVars()

        tolerance = 1.0e-7
        maxEvaluations = 100

        discountCurve = YieldTermStructureHandle(
            flatRate(vars.today, 0.03, Actual360()))

        issueMonths = [-24, -18, -12, -6, 0, 6, 12, 18, 24]
        lengths = [3, 5, 10, 15, 20]
        settlementDays = 3
        coupons = [0.02, 0.05, 0.08]
        frequencies = [Semiannual, Annual]
        bondDayCount = Thirty360(Thirty360.BondBasis)
        accrualConvention = Unadjusted
        paymentConvention = ModifiedFollowing
        redemption = 100.0

        spreads = [-0.01, -0.005, 0.0, 0.005, 0.01]
        compounding = [Compounded, Continuous]

        for issueMonth in issueMonths:
            for length in lengths:
                for coupon in coupons:
                    for frequencie in frequencies:
                        for n in compounding:

                            dated = vars.calendar.advance(
                                vars.today, issueMonth, Months)
                            issue = dated
                            maturity = vars.calendar.advance(
                                issue, length, Years)

                            sch = Schedule(
                                dated, maturity, Period(frequencie), vars.calendar,
                                accrualConvention, accrualConvention,
                                DateGeneration.Backward, false)

                            bond = FixedRateBond(
                                settlementDays, vars.faceAmount, sch,
                                DoubleVector(1, coupon), bondDayCount,
                                paymentConvention, redemption, issue)

                            for spread in spreads:

                                price = BondFunctions.cleanPrice(
                                    bond, discountCurve.currentLink(), spread,
                                    bondDayCount, n, frequencie)
                                calculated = BondFunctions.zSpread(
                                    bond, price, discountCurve.currentLink(),
                                    bondDayCount, n, frequencie, Date(),
                                    tolerance, maxEvaluations)

                                if abs(spread - calculated) > tolerance:
                                    # the difference might not matter
                                    price2 = BondFunctions.cleanPrice(
                                        bond, discountCurve.currentLink(),
                                        calculated, bondDayCount, n, frequencie)
                                    self.assertFalse(abs(price - price2) / price > tolerance)

    def testTheoretical(self):
        TEST_MESSAGE("Testing theoretical bond price/bondYield calculation...")

        vars = CommonVars()

        tolerance = 1.0e-7
        maxEvaluations = 100

        lengths = [3, 5, 10, 15, 20]
        settlementDays = 3
        coupons = [0.02, 0.05, 0.08]
        frequencies = [Semiannual, Annual]
        bondDayCount = Actual360()
        accrualConvention = Unadjusted
        paymentConvention = ModifiedFollowing
        redemption = 100.0

        yields = [0.03, 0.04, 0.05, 0.06, 0.07]

        for length in lengths:
            for coupon in coupons:
                for frequencie in frequencies:

                    dated = vars.today
                    issue = dated
                    maturity = vars.calendar.advance(issue, length, Years)

                    rate = SimpleQuote(0.0)
                    discountCurve = YieldTermStructureHandle(
                        flatRate(vars.today, rate, bondDayCount))

                    sch = Schedule(
                        dated, maturity, Period(frequencie), vars.calendar, accrualConvention,
                        accrualConvention, DateGeneration.Backward, false)

                    bond = FixedRateBond(
                        settlementDays, vars.faceAmount, sch,
                        DoubleVector(1, coupon), bondDayCount,
                        paymentConvention, redemption, issue)

                    bondEngine = DiscountingBondEngine(discountCurve)
                    bond.setPricingEngine(bondEngine)

                    for m in yields:
                        rate.setValue(m)

                        price = BondFunctions.cleanPrice(
                            bond, m, bondDayCount, Continuous, frequencie)
                        calculatedPrice = bond.cleanPrice()

                        self.assertFalse(abs(price - calculatedPrice) > tolerance)

                        calculatedYield = BondFunctions.bondYield(
                            bond, calculatedPrice, bondDayCount, Continuous, frequencie,
                            bond.settlementDate(), tolerance, maxEvaluations)
                        self.assertFalse(abs(m - calculatedYield) > tolerance)

    def testCached(self):
        TEST_MESSAGE(
            "Testing bond price/bondYield calculation against cached values...")

        vars = CommonVars()

        # with implicit settlement calculation:

        today = Date(22, November, 2004)
        Settings.instance().evaluationDate = today

        bondCalendar = NullCalendar()

        settlementDays = 1

        discountCurve = YieldTermStructureHandle(
            flatRate(today, 0.03, Actual360()))

        # actual market values from the evaluation date

        freq = Semiannual
        # This means that this bond has a short first coupon, as the
        # first coupon payment is april 30th and therefore the notional
        # first coupon is on October 30th 2004. Changing the EOM
        # convention to true will correct this so that the coupon starts
        # on October 31st and the first coupon is complete. This is
        # effectively assumed by the no-schedule daycounter.
        sch1 = Schedule(
            Date(31, October, 2004), Date(31, October, 2006),
            Period(freq), bondCalendar,
            Unadjusted, Unadjusted, DateGeneration.Backward, true)
        bondDayCount1 = ActualActual(ActualActual.ISMA, sch1)
        bondDayCount1NoSchedule = ActualActual(ActualActual.ISMA)

        bond1 = FixedRateBond(
            settlementDays, vars.faceAmount, sch1,
            DoubleVector(1, 0.025),
            bondDayCount1, ModifiedFollowing,
            100.0, Date(1, November, 2004))
        bond1NoSchedule = FixedRateBond(
            settlementDays, vars.faceAmount, sch1,
            DoubleVector(1, 0.025),
            bondDayCount1NoSchedule, ModifiedFollowing,
            100.0, Date(1, November, 2004))

        bondEngine = DiscountingBondEngine(discountCurve)
        bond1.setPricingEngine(bondEngine)
        bond1NoSchedule.setPricingEngine(bondEngine)

        marketPrice1 = 99.203125
        marketYield1 = 0.02925

        sch2 = Schedule(
            Date(15, November, 2004),
            Date(15, November, 2009), Period(freq), bondCalendar,
            Unadjusted, Unadjusted, DateGeneration.Backward, false)
        bondDayCount2 = ActualActual(ActualActual.ISMA, sch2)
        bondDayCount2NoSchedule = ActualActual(ActualActual.ISMA)

        bond2 = FixedRateBond(
            settlementDays, vars.faceAmount, sch2,
            DoubleVector(1, 0.035),
            bondDayCount2, ModifiedFollowing,
            100.0, Date(15, November, 2004))
        bond2NoSchedule = FixedRateBond(
            settlementDays, vars.faceAmount, sch2,
            DoubleVector(1, 0.035),
            bondDayCount2NoSchedule, ModifiedFollowing,
            100.0, Date(15, November, 2004))

        bond2.setPricingEngine(bondEngine)
        bond2NoSchedule.setPricingEngine(bondEngine)

        marketPrice2 = 99.6875
        marketYield2 = 0.03569

        # calculated values

        cachedPrice1a = 99.204505
        cachedPrice2a = 99.687192
        cachedPrice1b = 98.943393
        cachedPrice2b = 101.986794
        cachedYield1a = 0.029257
        cachedYield2a = 0.035689
        cachedYield1b = 0.029045
        cachedYield2b = 0.035375
        cachedYield1c = 0.030423
        cachedYield2c = 0.030432

        # check
        tolerance = 1.0e-6

        self.checkValue(
            BondFunctions.cleanPrice(
                bond1, marketYield1, bondDayCount1, Compounded, freq),
            cachedPrice1a, tolerance,
            "failed to reproduce cached price with schedule for bond 1:")
        self.checkValue(
            BondFunctions.cleanPrice(
                bond1NoSchedule, marketYield1, bondDayCount1NoSchedule, Compounded, freq),
            cachedPrice1a, tolerance,
            "failed to reproduce cached price with no schedule for bond 1:")
        self.checkValue(
            bond1.cleanPrice(),
            cachedPrice1b, tolerance,
            "failed to reproduce cached clean price with schedule for bond 1:")
        self.checkValue(
            bond1NoSchedule.cleanPrice(),
            cachedPrice1b, tolerance,
            "failed to reproduce cached clean price with no schdule for bond 1:")
        self.checkValue(
            BondFunctions.bondYield(
                bond1, marketPrice1, bondDayCount1, Compounded, freq),
            cachedYield1a, tolerance,
            "failed to reproduce cached compounded bondYield with schedule for bond 1:")
        self.checkValue(
            BondFunctions.bondYield(
                bond1NoSchedule, marketPrice1, bondDayCount1NoSchedule, Compounded, freq),
            cachedYield1a, tolerance,
            "failed to reproduce cached compounded bondYield with no schedule for bond 1:")
        self.checkValue(
            BondFunctions.bondYield(
                bond1, marketPrice1, bondDayCount1, Continuous, freq),
            cachedYield1b, tolerance,
            "failed to reproduce cached continuous bondYield with schedule for bond 1:")
        self.checkValue(
            BondFunctions.bondYield(
                bond1NoSchedule, marketPrice1, bondDayCount1NoSchedule, Continuous, freq),
            cachedYield1b, tolerance,
            "failed to reproduce cached continuous bondYield with no schedule for bond 1:")
        self.checkValue(
            BondFunctions.bondYield(
                bond1, bond1.cleanPrice(), bondDayCount1, Continuous, freq, bond1.settlementDate()),
            cachedYield1c, tolerance,
            "failed to reproduce cached continuous bondYield with schedule for bond 1:")
        self.checkValue(
            BondFunctions.bondYield(
                bond1NoSchedule, bond1NoSchedule.cleanPrice(), bondDayCount1NoSchedule, Continuous, freq, bond1.settlementDate()),
            cachedYield1c, tolerance,
            "failed to reproduce cached continuous bondYield with no schedule for bond 1:")

        # Now bond 2
        self.checkValue(
            BondFunctions.cleanPrice(
                bond2, marketYield2, bondDayCount2, Compounded, freq),
            cachedPrice2a, tolerance,
            "failed to reproduce cached price with schedule for bond 2")
        self.checkValue(
            BondFunctions.cleanPrice(
                bond2NoSchedule, marketYield2, bondDayCount2NoSchedule, Compounded, freq),
            cachedPrice2a, tolerance,
            "failed to reproduce cached price with no schedule for bond 2:")
        self.checkValue(
            bond2.cleanPrice(),
            cachedPrice2b, tolerance,
            "failed to reproduce cached clean price with schedule for bond 2:")
        self.checkValue(
            bond2NoSchedule.cleanPrice(),
            cachedPrice2b, tolerance,
            "failed to reproduce cached clean price with no schedule for bond 2:")
        self.checkValue(
            BondFunctions.bondYield(
                bond2, marketPrice2, bondDayCount2, Compounded, freq),
            cachedYield2a, tolerance,
            "failed to reproduce cached compounded bondYield with schedule for bond 2:")
        self.checkValue(
            BondFunctions.bondYield(
                bond2NoSchedule, marketPrice2, bondDayCount2NoSchedule, Compounded, freq),
            cachedYield2a, tolerance,
            "failed to reproduce cached compounded bondYield with no schedule for bond 2:")
        self.checkValue(
            BondFunctions.bondYield(
                bond2, marketPrice2, bondDayCount2, Continuous, freq),
            cachedYield2b, tolerance,
            "failed to reproduce chached continuous bondYield with schedule for bond 2:")
        self.checkValue(
            BondFunctions.bondYield(
                bond2NoSchedule, marketPrice2, bondDayCount2NoSchedule, Continuous, freq),
            cachedYield2b, tolerance,
            "failed to reproduce cached continuous bondYield with schedule for bond 2:")
        self.checkValue(
            BondFunctions.bondYield(
                bond2, bond2.cleanPrice(), bondDayCount2, Continuous, freq, bond2.settlementDate()),
            cachedYield2c, tolerance,
            "failed to reproduce cached continuous bondYield for bond 2 with schedule:")
        self.checkValue(
            BondFunctions.bondYield(
                bond2NoSchedule, bond2NoSchedule.cleanPrice(), bondDayCount2NoSchedule, Continuous, freq, bond2NoSchedule.settlementDate()),
            cachedYield2c, tolerance,
            "failed to reproduce cached continuous bondYield for bond 2 with no schedule:")

        # with explicit settlement date:

        sch3 = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2006), Period(freq),
            UnitedStates(UnitedStates.GovernmentBond),
            Unadjusted, Unadjusted, DateGeneration.Backward, false)
        bondDayCount3 = ActualActual(ActualActual.ISMA, sch3)
        bondDayCount3NoSchedule = ActualActual(ActualActual.ISMA)

        bond3 = FixedRateBond(
            settlementDays, vars.faceAmount, sch3,
            DoubleVector(1, 0.02875),
            bondDayCount3,
            ModifiedFollowing,
            100.0, Date(30, November, 2004))
        bond3NoSchedule = FixedRateBond(
            settlementDays, vars.faceAmount, sch3,
            DoubleVector(1, 0.02875),
            bondDayCount3NoSchedule,
            ModifiedFollowing,
            100.0, Date(30, November, 2004))

        bond3.setPricingEngine(bondEngine)
        bond3NoSchedule.setPricingEngine(bondEngine)

        marketYield3 = 0.02997

        settlementDate = Date(30, November, 2004)
        cachedPrice3 = 99.764759

        self.checkValue(
            BondFunctions.cleanPrice(
                bond3, marketYield3, bondDayCount3, Compounded, freq, settlementDate),
            cachedPrice3,
            tolerance,
            "Failed to reproduce cached price for bond 3 with schedule")
        self.checkValue(
            BondFunctions.cleanPrice(
                bond3NoSchedule, marketYield3, bondDayCount3NoSchedule, Compounded, freq, settlementDate),
            cachedPrice3, tolerance,
            "Failed to reproduce cached price for bond 3 with no schedule")

        # this should give the same result since the issue date is the
        # earliest possible settlement date

        Settings.instance().evaluationDate = Date(22, November, 2004)
        self.checkValue(
            BondFunctions.cleanPrice(
                bond3, marketYield3, bondDayCount3, Compounded, freq),
            cachedPrice3, tolerance,
            "Failed to reproduce the cached price for bond 3 with schedule and the earlierst possible settlment date")
        self.checkValue(
            BondFunctions.cleanPrice(
                bond3NoSchedule, marketYield3, bondDayCount3NoSchedule, Compounded, freq),
            cachedPrice3,
            tolerance,
            "Failed to reproduce the cached price for bond 3 with no schedule and the earlierst possible settlment date")

    def testCachedZero(self):
        TEST_MESSAGE("Testing zero-coupon bond prices against cached values...")

        vars = CommonVars()

        today = Date(22, November, 2004)
        Settings.instance().evaluationDate = today

        settlementDays = 1

        discountCurve = YieldTermStructureHandle(
            flatRate(today, 0.03, Actual360()))

        tolerance = 1.0e-6

        # plain

        bond1 = ZeroCouponBond(
            settlementDays,
            UnitedStates(UnitedStates.GovernmentBond),
            vars.faceAmount,
            Date(30, November, 2008),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))

        bondEngine = DiscountingBondEngine(discountCurve)
        bond1.setPricingEngine(bondEngine)

        cachedPrice1 = 88.551726

        price = bond1.cleanPrice()
        self.assertFalse(abs(price - cachedPrice1) > tolerance)

        bond2 = ZeroCouponBond(
            settlementDays,
            UnitedStates(UnitedStates.GovernmentBond),
            vars.faceAmount,
            Date(30, November, 2007),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))

        bond2.setPricingEngine(bondEngine)

        cachedPrice2 = 91.278949

        price = bond2.cleanPrice()
        self.assertFalse(abs(price - cachedPrice2) > tolerance)

        bond3 = ZeroCouponBond(
            settlementDays,
            UnitedStates(UnitedStates.GovernmentBond),
            vars.faceAmount,
            Date(30, November, 2006),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))

        bond3.setPricingEngine(bondEngine)

        cachedPrice3 = 94.098006

        price = bond3.cleanPrice()
        self.assertFalse(abs(price - cachedPrice3) > tolerance)

    def testCachedFixed(self):
        TEST_MESSAGE("Testing fixed-coupon bond prices against cached values...")

        vars = CommonVars()

        today = Date(22, November, 2004)
        Settings.instance().evaluationDate = today

        settlementDays = 1

        discountCurve = YieldTermStructureHandle(
            flatRate(today, 0.03, Actual360()))

        tolerance = 1.0e-6

        # plain

        sch = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2008), Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            Unadjusted, Unadjusted, DateGeneration.Backward, false)

        bond1 = FixedRateBond(
            settlementDays, vars.faceAmount, sch,
            DoubleVector(1, 0.02875),
            ActualActual(ActualActual.ISMA),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))

        bondEngine = DiscountingBondEngine(discountCurve)
        bond1.setPricingEngine(bondEngine)

        cachedPrice1 = 99.298100

        price = bond1.cleanPrice()
        self.assertFalse(abs(price - cachedPrice1) > tolerance)

        # varying coupons

        couponRates = DoubleVector(4)
        couponRates[0] = 0.02875
        couponRates[1] = 0.03
        couponRates[2] = 0.03125
        couponRates[3] = 0.0325

        bond2 = FixedRateBond(
            settlementDays, vars.faceAmount, sch,
            couponRates,
            ActualActual(ActualActual.ISMA),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))

        bond2.setPricingEngine(bondEngine)

        cachedPrice2 = 100.334149

        price = bond2.cleanPrice()
        self.assertFalse(abs(price - cachedPrice2) > tolerance)

        # stub date

        sch3 = Schedule(
            Date(30, November, 2004),
            Date(30, March, 2009), Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            Unadjusted, Unadjusted, DateGeneration.Backward, false,
            Date(), Date(30, November, 2008))

        bond3 = FixedRateBond(
            settlementDays, vars.faceAmount, sch3,
            couponRates, ActualActual(ActualActual.ISMA),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))

        bond3.setPricingEngine(bondEngine)

        cachedPrice3 = 100.382794

        price = bond3.cleanPrice()
        self.assertFalse(abs(price - cachedPrice3) > tolerance)

    def testCachedFloating(self):
        TEST_MESSAGE("Testing floating-rate bond prices against cached values...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        today = Date(22, November, 2004)
        Settings.instance().evaluationDate = today

        settlementDays = 1

        riskFreeRate = YieldTermStructureHandle(flatRate(today, 0.025, Actual360()))
        discountCurve = YieldTermStructureHandle(flatRate(today, 0.03, Actual360()))

        index = USDLibor(Period(6, Months), riskFreeRate)
        fixingDays = 1

        tolerance = 1.0e-6

        pricer = BlackIborCouponPricer(OptionletVolatilityStructureHandle())

        # plain

        sch = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2008),
            Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)

        bond1 = FloatingRateBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        bondEngine = DiscountingBondEngine(riskFreeRate)
        bond1.setPricingEngine(bondEngine)

        setCouponPricer(bond1.cashflows(), pricer)

        cachedPrice1 = 99.874646 if usingAtParCoupons else 99.874645

        price = bond1.cleanPrice()
        self.assertFalse(abs(price - cachedPrice1) > tolerance)

        # different risk-free and discount curve

        bond2 = FloatingRateBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        bondEngine2 = DiscountingBondEngine(discountCurve)
        bond2.setPricingEngine(bondEngine2)

        setCouponPricer(bond2.cashflows(), pricer)

        cachedPrice2 = 97.955904

        price = bond2.cleanPrice()
        self.assertFalse(abs(price - cachedPrice2) > tolerance)

        # varying spread

        spreads = DoubleVector(4)
        spreads[0] = 0.001
        spreads[1] = 0.0012
        spreads[2] = 0.0014
        spreads[3] = 0.0016

        bond3 = FloatingRateBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            ModifiedFollowing, fixingDays,
            DoubleVector(), spreads,
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        bond3.setPricingEngine(bondEngine2)

        setCouponPricer(bond3.cashflows(), pricer)

        cachedPrice3 = 98.495459 if usingAtParCoupons else 98.495458

        price = bond3.cleanPrice()
        self.assertFalse(abs(price - cachedPrice3) > tolerance)

        sch2 = Schedule(
            Date(26, November, 2003), Date(26, November, 2007), Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond), ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)
        bond4 = FloatingRateBond(
            settlementDays, vars.faceAmount, sch2, index,
            ActualActual(ActualActual.ISMA), ModifiedFollowing, fixingDays,
            DoubleVector(), spreads, DoubleVector(),
            DoubleVector(), false, 100.0, Date(29, October, 2004), Period(6, Days))

        index.addFixing(Date(25, May, 2004), 0.0402)
        bond4.setPricingEngine(bondEngine2)

        setCouponPricer(bond4.cashflows(), pricer)

        cachedPrice4 = 98.892055 if usingAtParCoupons else 98.892346

        price = bond4.cleanPrice()
        self.assertFalse(abs(price - cachedPrice4) > tolerance)

    def testBrazilianCached(self):
        TEST_MESSAGE(
            "Testing Brazilian public bond prices against Andima cached values...")

        vars = CommonVars()

        settlementDays = 1
        faceAmount = 1000.0
        redemption = 100.0
        today = Date(6, June, 2007)
        issueDate = Date(1, January, 2007)

        # The tolerance is high because Andima truncate yields
        tolerance = 1.0e-4

        # Reset evaluation date
        Settings.instance().evaluationDate = today

        # NTN-F maturity dates
        maturityDates = DateVector(6)
        maturityDates[0] = Date(1, January, 2008)
        maturityDates[1] = Date(1, January, 2010)
        maturityDates[2] = Date(1, July, 2010)
        maturityDates[3] = Date(1, January, 2012)
        maturityDates[4] = Date(1, January, 2014)
        maturityDates[5] = Date(1, January, 2017)

        # Andima NTN-F yields
        yields = DoubleVector(6)
        yields[0] = 0.114614
        yields[1] = 0.105726
        yields[2] = 0.105328
        yields[3] = 0.104283
        yields[4] = 0.103218
        yields[5] = 0.102948

        # Andima NTN-F prices
        prices = DoubleVector(6)
        prices[0] = 1034.63031372
        prices[1] = 1030.09919487
        prices[2] = 1029.98307160
        prices[3] = 1028.13585068
        prices[4] = 1028.33383817
        prices[5] = 1026.19716497

        couponRates = InterestRateVector(1)
        couponRates[0] = InterestRate(0.1, Thirty360(Thirty360.BondBasis), Compounded, Annual)

        for bondIndex in range(maturityDates.size()):
            bondYield = InterestRate(
                yields[bondIndex], Business252(Brazil()), Compounded, Annual)

            schedule = Schedule(
                Date(1, January, 2007),
                maturityDates[bondIndex], Period(Semiannual),
                Brazil(Brazil.Settlement),
                Unadjusted, Unadjusted,
                DateGeneration.Backward, false)

            bond = FixedRateBond(
                settlementDays, faceAmount, schedule, couponRates,
                Following, redemption, issueDate)

            cachedPrice = prices[bondIndex]
            price = faceAmount * (
                    BondFunctions.cleanPrice(
                        bond, bondYield.rate(), bondYield.dayCounter(),
                        bondYield.compounding(), bondYield.frequency(), today) +
                    bond.accruedAmount(today)) / 100.0

            self.assertFalse(abs(price - cachedPrice) > tolerance)

    def testFixedBondWithGivenDates(self):
        TEST_MESSAGE("Testing fixed-coupon bond built on schedule with given dates...")

        vars = CommonVars()

        today = Date(22, November, 2004)
        Settings.instance().evaluationDate = today

        settlementDays = 1

        discountCurve = YieldTermStructureHandle(flatRate(today, 0.03, Actual360()))

        tolerance = 1.0e-6

        bondEngine = DiscountingBondEngine(discountCurve)
        # plain

        sch1 = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2008), Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            Unadjusted, Unadjusted, DateGeneration.Backward, false)
        bond1 = FixedRateBond(
            settlementDays, vars.faceAmount, sch1,
            DoubleVector(1, 0.02875),
            ActualActual(ActualActual.ISMA),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))
        bond1.setPricingEngine(bondEngine)

        sch1_copy = Schedule(
            sch1.dates(),
            UnitedStates(UnitedStates.GovernmentBond),
            Unadjusted,
            Unadjusted,
            Period(Semiannual),
            DateGeneration.Backward,
            False,
            # BoolVector(len(sch1) - 1, true)
        )
        bond1_copy = FixedRateBond(
            settlementDays, vars.faceAmount, sch1_copy,
            DoubleVector(1, 0.02875),
            ActualActual(ActualActual.ISMA),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))
        bond1_copy.setPricingEngine(bondEngine)

        expected = bond1.cleanPrice()
        calculated = bond1_copy.cleanPrice()
        self.assertFalse(abs(expected - calculated) > tolerance)

        # varying coupons

        couponRates = DoubleVector(4)
        couponRates[0] = 0.02875
        couponRates[1] = 0.03
        couponRates[2] = 0.03125
        couponRates[3] = 0.0325

        bond2 = FixedRateBond(
            settlementDays, vars.faceAmount, sch1,
            couponRates,
            ActualActual(ActualActual.ISMA),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))
        bond2.setPricingEngine(bondEngine)

        bond2_copy = FixedRateBond(
            settlementDays, vars.faceAmount, sch1_copy,
            couponRates,
            ActualActual(ActualActual.ISMA),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))
        bond2_copy.setPricingEngine(bondEngine)

        expected = bond2.cleanPrice()
        calculated = bond2_copy.cleanPrice()
        self.assertFalse(abs(expected - calculated) > tolerance)

        # stub date

        sch3 = Schedule(
            Date(30, November, 2004),
            Date(30, March, 2009), Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            Unadjusted, Unadjusted, DateGeneration.Backward, false,
            Date(), Date(30, November, 2008))
        bond3 = FixedRateBond(
            settlementDays, vars.faceAmount, sch3,
            couponRates,
            Actual360(),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))
        bond3.setPricingEngine(bondEngine)

        sch3_copy = Schedule(
            sch3.dates(), UnitedStates(UnitedStates.GovernmentBond),
            Unadjusted, Unadjusted, Period(Semiannual),
            DateGeneration.Backward,
            false, BoolVector(len(sch3) - 1, true))
        bond3_copy = FixedRateBond(
            settlementDays, vars.faceAmount, sch3_copy,
            couponRates,
            Actual360(),
            ModifiedFollowing,
            100.0, Date(30, November, 2004))
        bond3_copy.setPricingEngine(bondEngine)

        expected = bond3.cleanPrice()
        calculated = bond3_copy.cleanPrice()
        self.assertFalse(abs(expected - calculated) > tolerance)

    def testRiskyBondWithGivenDates(self):
        TEST_MESSAGE("Testing risky bond engine...")

        vars = CommonVars()

        today = Date(22, November, 2005)
        Settings.instance().evaluationDate = today

        # Structure
        hazardRate = QuoteHandle(SimpleQuote(0.1))
        defaultProbability = DefaultProbabilityTermStructureHandle(
            FlatHazardRate(0, TARGET(), hazardRate, Actual360()))

        # Yield term structure
        riskFree = RelinkableYieldTermStructureHandle()
        riskFree.linkTo(FlatForward(today, 0.02, Actual360()))
        sch1 = Schedule(
            Date(30, November, 2004), Date(30, November, 2008), Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond), Unadjusted, Unadjusted,
            DateGeneration.Backward, false)

        # Create Bond
        settlementDays = 1
        notionals = [0.0167, 0.023, 0.03234, 0.034, 0.038, 0.042, 0.047, 0.053]

        couponRates = DoubleVector(4)
        couponRates[0] = 0.02875
        couponRates[1] = 0.03
        couponRates[2] = 0.03125
        couponRates[3] = 0.0325
        recoveryRate = 0.4

        bond = FixedRateBond(
            settlementDays, vars.faceAmount, sch1, couponRates,
            ActualActual(ActualActual.ISMA), ModifiedFollowing, 100.0,
            Date(20, November, 2004))

        # Create Engine
        bondEngine = RiskyBondEngine(
            defaultProbability, recoveryRate, riskFree)
        bond.setPricingEngine(bondEngine)

        # Calculate and validate NPV and price
        expected = 888458.819055
        calculated = bond.NPV()
        tolerance = 1.0e-6
        self.assertFalse(abs(expected - calculated) > tolerance)

        expected = 87.407883
        calculated = bond.cleanPrice()
        self.assertFalse(abs(expected - calculated) > tolerance)

    def testExCouponGilt(self):
        TEST_MESSAGE(
            "Testing ex-coupon UK Gilt price against market values...")

        # UK Gilts have an exCouponDate 7 business days before the coupon
        # is due (see <http:#www.dmo.gov.uk/index.aspx?page=Gilts/Gilt_Faq>).
        # On the exCouponDate the bond still trades cum-coupon so we use
        # 6 days below and UK calendar

        # Output verified with Bloomberg:

        # ISIN: GB0009997999
        # Issue Date: February 29th, 1996
        # Interest Accrue: February 29th, 1996
        # First Coupon: June 7th, 1996
        # Maturity: June 7th, 2021
        # coupon: 8
        # period: 6M

        # Settlement date: May 29th, 2013
        # Test Price in 103
        # Accrued in 38021.97802
        # NPV in 106.8021978
        # Yield in 7.495180593
        # Yield.NPV in 106.8021978
        # Yield.NPV.Price in 103
        # Mod duration in 5.676044458
        # Convexity in 0.4215314859
        # PV 0.01 in 0.0606214023

        # Settlement date: May 30th, 2013
        # Test Price in 103
        # Accrued in -1758.241758
        # NPV in 102.8241758
        # Yield in 7.496183543
        # Yield.NPV in 102.8241758
        # Yield.NPV.Price in 103
        # Mod duration in 5.892816328
        # Convexity in 0.4375621862
        # PV 0.01 in 0.06059239822

        # Settlement date: May 31st, 2013
        # Test Price in 103
        # Accrued in -1538.461538
        # NPV in 102.8461538
        # Yield in 7.495987492
        # Yield.NPV in 102.8461539
        # Yield.NPV.Price in 103
        # Mod duration in 5.890186028
        # Convexity in 0.4372394381
        # PV 0.01 in 0.06057829784

        class test_case(object):
            def __init__(self,
                         settlementDate,
                         testPrice,
                         accruedAmount,
                         NPV,
                         bondYield,
                         duration,
                         convexity):
                self.settlementDate = settlementDate
                self.testPrice = testPrice
                self.accruedAmount = accruedAmount
                self.NPV = NPV
                self.bondYield = bondYield
                self.duration = duration
                self.convexity = convexity

        calendar = UnitedKingdom()

        settlementDays = 3

        issueDate = Date(29, February, 1996)
        startDate = Date(29, February, 1996)
        firstCouponDate = Date(7, June, 1996)
        maturityDate = Date(7, June, 2021)

        coupon = 0.08

        tenor = Period(6, Months)
        exCouponPeriod = Period(6, Days)

        comp = Compounded
        freq = Semiannual

        schedule = Schedule(
            startDate, maturityDate, tenor,
            NullCalendar(), Unadjusted, Unadjusted,
            DateGeneration.Forward, true, firstCouponDate)
        dc = ActualActual(ActualActual.ISMA, schedule)

        bond = FixedRateBond(
            settlementDays, 100.0,
            schedule,
            DoubleVector(1, coupon),
            dc, Unadjusted, 100.0,
            issueDate, calendar, exCouponPeriod, calendar)

        leg = bond.cashflows()

        cases = [
            test_case(Date(29, May, 2013), 103.0, 3.8021978, 106.8021978, 0.0749518, 5.6760445, 42.1531486),
            test_case(Date(30, May, 2013), 103.0, -0.1758242, 102.8241758, 0.0749618, 5.8928163, 43.7562186),
            test_case(Date(31, May, 2013), 103.0, -0.1538462, 102.8461538, 0.0749599, 5.8901860, 43.7239438)]

        for i in cases:
            accrued = bond.accruedAmount(i.settlementDate)
            self.ASSERT_CLOSE(
                "accrued amount", i.settlementDate, accrued, i.accruedAmount, 1e-6)

            npv = i.testPrice + accrued
            self.ASSERT_CLOSE(
                "NPV", i.settlementDate, npv, i.NPV, 1e-6)

            bondYield = CashFlows.yieldRate(
                leg, npv, dc, comp, freq, false, i.settlementDate)
            self.ASSERT_CLOSE(
                "bondYield", i.settlementDate, bondYield, i.bondYield, 1e-6)

            duration = CashFlows.duration(
                leg, bondYield, dc, comp, freq, Duration.Modified, false, i.settlementDate)
            self.ASSERT_CLOSE(
                "duration", i.settlementDate, duration, i.duration, 1e-6)

            convexity = CashFlows.convexity(
                leg, bondYield, dc, comp, freq, false, i.settlementDate)
            self.ASSERT_CLOSE(
                "convexity", i.settlementDate, convexity, i.convexity, 1e-6)

            calcnpv = CashFlows.npv(
                leg, bondYield, dc, comp, freq, false, i.settlementDate)
            self.ASSERT_CLOSE(
                "NPV from bondYield", i.settlementDate, calcnpv, i.NPV, 1e-6)

            calcprice = calcnpv - accrued
            self.ASSERT_CLOSE(
                "price from bondYield", i.settlementDate, calcprice, i.testPrice, 1e-6)

    def testExCouponAustralianBond(self):
        TEST_MESSAGE(
            "Testing ex-coupon Australian bond price against market values...")

        # Australian Government Bonds have an exCouponDate 7 calendar
        # days before the coupon is due.  On the exCouponDate the bond
        # trades ex-coupon so we use 7 days below and NullCalendar.
        # AGB accrued interest is rounded to 3dp.

        # Output verified with Bloomberg:

        # ISIN: AU300TB01208
        # Issue Date: June 10th, 2004
        # Interest Accrue: February 15th, 2004
        # First Coupon: August 15th, 2004
        # Maturity: February 15th, 2017
        # coupon: 6
        # period: 6M

        # Settlement date: August 7th, 2014
        # Test Price in 103
        # Accrued in 28670
        # NPV in 105.867
        # Yield in 4.723814867
        # Yield.NPV in 105.867
        # Yield.NPV.Price in 103
        # Mod duration in 2.262763296
        # Convexity in 0.0654870275
        # PV 0.01 in 0.02395519619

        # Settlement date: August 8th, 2014
        # Test Price in 103
        # Accrued in -1160
        # NPV in 102.884
        # Yield in 4.72354833
        # Yield.NPV in 102.884
        # Yield.NPV.Price in 103
        # Mod duration in 2.325360055
        # Convexity in 0.06725307785
        # PV 0.01 in 0.02392423439

        # Settlement date: August 11th, 2014
        # Test Price in 103
        # Accrued in -660
        # NPV in 102.934
        # Yield in 4.719277687
        # Yield.NPV in 102.934
        # Yield.NPV.Price in 103
        # Mod duration in 2.317320093
        # Convexity in 0.06684074058
        # PV 0.01 in 0.02385310264

        class test_case(object):
            def __init__(self,
                         settlementDate,
                         testPrice,
                         accruedAmount,
                         NPV,
                         bondYield,
                         duration,
                         convexity):
                self.settlementDate = settlementDate
                self.testPrice = testPrice
                self.accruedAmount = accruedAmount
                self.NPV = NPV
                self.bondYield = bondYield
                self.duration = duration
                self.convexity = convexity

        calendar = Australia()

        settlementDays = 3

        issueDate = Date(10, June, 2004)
        startDate = Date(15, February, 2004)
        firstCouponDate = Date(15, August, 2004)
        maturityDate = Date(15, February, 2017)

        coupon = 0.06

        tenor = Period(6, Months)
        exCouponPeriod = Period(7, Days)

        comp = Compounded
        freq = Semiannual

        schedule = Schedule(
            startDate, maturityDate, tenor,
            NullCalendar(), Unadjusted, Unadjusted,
            DateGeneration.Forward, true, firstCouponDate)
        dc = ActualActual(ActualActual.ISMA, schedule)

        bond = FixedRateBond(
            settlementDays, 100.0,
            schedule,
            DoubleVector(1, coupon),
            dc, Unadjusted, 100.0,
            issueDate, calendar, exCouponPeriod, NullCalendar())

        leg = bond.cashflows()

        cases = [
            test_case(Date(7, August, 2014), 103.0, 2.8670, 105.867, 0.04723, 2.26276, 6.54870),
            test_case(Date(8, August, 2014), 103.0, -0.1160, 102.884, 0.047235, 2.32536, 6.72531),
            test_case(Date(11, August, 2014), 103.0, -0.0660, 102.934, 0.04719, 2.31732, 6.68407)]

        for i in cases:
            accrued = bond.accruedAmount(i.settlementDate)
            self.ASSERT_CLOSE(
                "accrued amount", i.settlementDate, accrued, i.accruedAmount, 1e-3)

            npv = i.testPrice + accrued
            self.ASSERT_CLOSE(
                "NPV", i.settlementDate, npv, i.NPV, 1e-3)

            bondYield = CashFlows.yieldRate(
                leg, npv, dc, comp, freq, false, i.settlementDate)
            self.ASSERT_CLOSE(
                "bondYield", i.settlementDate, bondYield, i.bondYield, 1e-5)

            duration = CashFlows.duration(
                leg, bondYield, dc, comp, freq, Duration.Modified, false, i.settlementDate)
            self.ASSERT_CLOSE(
                "duration", i.settlementDate, duration, i.duration, 1e-5)

            convexity = CashFlows.convexity(
                leg, bondYield, dc, comp, freq, false, i.settlementDate)
            self.ASSERT_CLOSE(
                "convexity", i.settlementDate, convexity, i.convexity, 1e-4)

            calcnpv = CashFlows.npv(
                leg, bondYield, dc, comp, freq, false, i.settlementDate)
            self.ASSERT_CLOSE(
                "NPV from bondYield", i.settlementDate, calcnpv, i.NPV, 1e-3)

            calcprice = calcnpv - accrued
            self.ASSERT_CLOSE(
                "price from bondYield", i.settlementDate, calcprice, i.testPrice, 1e-3)

    def testBondFromScheduleWithDateVector(self):
        # Test calculation of South African R2048 bond
        # This requires the use of the Schedule to be constructed
        # with a custom date vector
        TEST_MESSAGE("Testing South African R2048 bond price using Schedule constructor with vector...")
        backup = SavedSettings()

        # When pricing bond from Yield To Maturity, use NullCalendar()
        calendar = NullCalendar()

        settlementDays = 3

        issueDate = Date(29, June, 2012)
        today = Date(7, September, 2015)
        evaluationDate = calendar.adjust(today)
        settlementDate = calendar.advance(evaluationDate, Period(settlementDays, Days))
        Settings.instance().evaluationDate = evaluationDate

        # For the schedule to generate correctly for Feb-28's, make maturity date on Feb 29
        maturityDate = Date(29, February, 2048)

        coupon = 0.0875
        comp = Compounded
        freq = Semiannual

        tenor = Period(6, Months)
        exCouponPeriod = Period(10, Days)

        # Generate coupon dates for 31 Aug and end of Feb each year
        # For leap years, this will generate 29 Feb, but the bond
        # actually pays coupons on 28 Feb, regardsless of whether
        # it is a leap year or not. 
        schedule = Schedule(
            issueDate, maturityDate, tenor,
            NullCalendar(), Unadjusted, Unadjusted,
            DateGeneration.Backward, true)

        # Adjust the 29 Feb's to 28 Feb
        dates = DateVector()
        for i in range(len(schedule)):
            d = schedule.date(i)
            if d.month() == February and d.dayOfMonth() == 29:
                dates.push_back(Date(28, February, d.year()))
            else:
                dates.push_back(d)

        schedule = Schedule(
            dates,
            schedule.calendar(),
            schedule.businessDayConvention(),
            schedule.terminationDateBusinessDayConvention(),
            schedule.tenor(),
            schedule.rule(),
            schedule.endOfMonth(),
            schedule.isRegular())
        dc = ActualActual(ActualActual.Bond, schedule)
        bond = FixedRateBond(
            0,
            100.0,
            schedule,
            DoubleVector(1, coupon),
            dc, Following, 100.0,
            issueDate, calendar,
            exCouponPeriod, calendar, Unadjusted, false)

        # Yield as quoted in market
        bondYield = InterestRate(0.09185, dc, comp, freq)

        calculatedPrice = BondFunctions.dirtyPrice(bond, bondYield, settlementDate)
        expectedPrice = 95.75706
        tolerance = 1e-5
        self.assertFalse(abs(calculatedPrice - expectedPrice) > tolerance)

    def testFixedRateBondWithArbitrarySchedule(self):
        TEST_MESSAGE("Testing fixed-rate bond with arbitrary schedule...")
        backup = SavedSettings()

        calendar = NullCalendar()

        settlementDays = 3

        today = Date(1, January, 2019)
        Settings.instance().evaluationDate = today

        # For the schedule to generate correctly for Feb-28's, make maturity date on Feb 29
        dates = DateVector(4)
        dates[0] = Date(1, February, 2019)
        dates[1] = Date(7, February, 2019)
        dates[2] = Date(1, April, 2019)
        dates[3] = Date(27, May, 2019)

        schedule = Schedule(dates, calendar, Unadjusted)

        coupon = 0.01
        dc = Actual365Fixed()

        bond = FixedRateBond(
            settlementDays,
            100.0,
            schedule,
            DoubleVector(1, coupon),
            dc, Following, 100.0)

        self.assertFalse(bond.frequency() != NoFrequency)

        discountCurve = YieldTermStructureHandle(
            flatRate(today, 0.03, Actual360()))
        bond.setPricingEngine(DiscountingBondEngine(discountCurve))

        # BOOST_CHECK_NO_THROW(bond.cleanPrice())

    def testThirty360BondWithSettlementOn31st(self):
        TEST_MESSAGE(
            "Testing Thirty/360 bond with settlement on 31st of the month...")

        # cusip 3130A0X70, data is from Bloomberg
        backup = SavedSettings()
        Settings.instance().evaluationDate = Date(28, July, 2017)

        datedDate = Date(13, February, 2014)
        settlement = Date(31, July, 2017)
        maturity = Date(13, August, 2018)

        dayCounter = Thirty360(Thirty360.USA)
        compounding = Compounded

        fixedBondSchedule = Schedule(
            datedDate,
            maturity,
            Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            Unadjusted, Unadjusted,
            DateGeneration.Forward, false)

        fixedRateBond = FixedRateBond(
            1,
            100,
            fixedBondSchedule,
            DoubleVector(1, 0.015),
            dayCounter,
            Unadjusted,
            100.0)

        cleanPrice = 100.0

        bondYield = BondFunctions.bondYield(
            fixedRateBond, cleanPrice, dayCounter, compounding, Semiannual, settlement)
        self.ASSERT_CLOSE(
            "bondYield", settlement, bondYield, 0.015, 1e-4)

        duration = BondFunctions.duration(
            fixedRateBond, InterestRate(bondYield, dayCounter, compounding, Semiannual), Duration.Macaulay, settlement)
        self.ASSERT_CLOSE(
            "duration", settlement, duration, 1.022, 1e-3)

        convexity = BondFunctions.convexity(
            fixedRateBond, InterestRate(bondYield, dayCounter, compounding, Semiannual), settlement) / 100
        self.ASSERT_CLOSE(
            "convexity", settlement, convexity, 0.015, 1e-3)

        accrued = BondFunctions.accruedAmount(
            fixedRateBond, settlement)
        self.ASSERT_CLOSE(
            "accrued", settlement, accrued, 0.7, 1e-6)

    def ASSERT_CLOSE(self,
                     name,
                     settlement,
                     calculated,
                     expected,
                     tolerance):
        self.assertFalse(
            abs(calculated - expected) > tolerance)

    def checkValue(self,
                   value,
                   expectedValue,
                   tolerance,
                   msg):
        self.assertFalse(
            abs(value - expectedValue) > tolerance)
