import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.calendar = TARGET()

        self.today = self.calendar.adjust(knownGoodDefault)
        Settings.instance().evaluationDate = self.today

        self.dayCounter = Actual360()
        self.frequency = Annual
        self.settlementDays = 3

        self.issueDate = self.calendar.advance(self.today, 2, Days)
        self.maturityDate = self.calendar.advance(self.issueDate, 10, Years)

        self.issueDate = self.calendar.advance(self.maturityDate, -10, Years)

        self.underlying = RelinkableQuoteHandle()
        self.dividendYield = RelinkableYieldTermStructureHandle()
        self.riskFreeRate = RelinkableYieldTermStructureHandle()
        self.volatility = RelinkableBlackVolTermStructureHandle()

        self.underlying.linkTo(SimpleQuote(50.0))
        self.dividendYield.linkTo(flatRate(self.today, 0.02, self.dayCounter))
        self.riskFreeRate.linkTo(flatRate(self.today, 0.05, self.dayCounter))
        self.volatility.linkTo(flatVol(self.today, 0.15, self.dayCounter))

        self.process = BlackScholesMertonProcess(
            self.underlying, self.dividendYield, self.riskFreeRate, self.volatility)

        self.creditSpread = RelinkableQuoteHandle()
        self.creditSpread.linkTo(SimpleQuote(0.005))

        self.no_callability = CallabilitySchedule()

        self.faceAmount = 100.0
        self.redemption = 100.0
        self.conversionRatio = self.redemption / self.underlying.value()
        self.backup = SavedSettings()


class ConvertibleBondTest(unittest.TestCase):

    def testBond(self):

        TEST_MESSAGE(
            "Testing out-of-the-money convertible bonds against vanilla bonds...")

        vars = CommonVars()

        vars.conversionRatio = 1.0e-16

        euExercise = EuropeanExercise(vars.maturityDate)
        amExercise = AmericanExercise(vars.issueDate, vars.maturityDate)

        timeSteps = 1001
        engine = BinomialCRRConvertibleEngine(
            vars.process, timeSteps, vars.creditSpread)

        discountCurve = YieldTermStructureHandle(
            ForwardSpreadedTermStructure(
                vars.riskFreeRate, vars.creditSpread))

        schedule = MakeSchedule()
        schedule.fromDate(vars.issueDate)
        schedule.to(vars.maturityDate)
        schedule.withFrequency(Once)
        schedule.withCalendar(vars.calendar)
        schedule.backwards()
        schedule = schedule.makeSchedule()

        euZero = ConvertibleZeroCouponBond(
            euExercise, vars.conversionRatio,
            vars.no_callability,
            vars.issueDate, vars.settlementDays,
            vars.dayCounter, schedule,
            vars.redemption)
        euZero.setPricingEngine(engine)

        amZero = ConvertibleZeroCouponBond(
            amExercise, vars.conversionRatio,
            vars.no_callability,
            vars.issueDate, vars.settlementDays,
            vars.dayCounter, schedule,
            vars.redemption)
        amZero.setPricingEngine(engine)

        zero = ZeroCouponBond(
            vars.settlementDays, vars.calendar,
            100.0, vars.maturityDate,
            Following, vars.redemption, vars.issueDate)

        bondEngine = DiscountingBondEngine(discountCurve)
        zero.setPricingEngine(bondEngine)

        tolerance = 1.0e-2 * (vars.faceAmount / 100.0)

        error = abs(euZero.NPV() - zero.settlementValue())
        self.assertFalse(error > tolerance)

        error = abs(amZero.NPV() - zero.settlementValue())
        self.assertFalse(error > tolerance)

        coupons = DoubleVector(1, 0.05)

        schedule = MakeSchedule()
        schedule.fromDate(vars.issueDate)
        schedule.to(vars.maturityDate)
        schedule.withFrequency(vars.frequency)
        schedule.withCalendar(vars.calendar)
        schedule.backwards()
        schedule = schedule.makeSchedule()

        euFixed = ConvertibleFixedCouponBond(
            euExercise, vars.conversionRatio,
            vars.no_callability,
            vars.issueDate, vars.settlementDays,
            coupons, vars.dayCounter,
            schedule, vars.redemption)
        euFixed.setPricingEngine(engine)

        amFixed = ConvertibleFixedCouponBond(
            amExercise, vars.conversionRatio,
            vars.no_callability,
            vars.issueDate, vars.settlementDays,
            coupons, vars.dayCounter,
            schedule, vars.redemption)
        amFixed.setPricingEngine(engine)

        fixed = FixedRateBond(
            vars.settlementDays, vars.faceAmount, schedule,
            coupons, vars.dayCounter, Following,
            vars.redemption, vars.issueDate)

        fixed.setPricingEngine(bondEngine)

        tolerance = 2.0e-2 * (vars.faceAmount / 100.0)

        error = abs(euFixed.NPV() - fixed.settlementValue())
        self.assertFalse(error > tolerance)

        error = abs(amFixed.NPV() - fixed.settlementValue())
        self.assertFalse(error > tolerance)

        index = Euribor1Y(discountCurve)
        fixingDays = 2
        gearings = DoubleVector(1, 1.0)
        spreads = DoubleVector()

        euFloating = ConvertibleFloatingRateBond(
            euExercise, vars.conversionRatio,
            vars.no_callability,
            vars.issueDate, vars.settlementDays,
            index, fixingDays, spreads,
            vars.dayCounter, schedule,
            vars.redemption)
        euFloating.setPricingEngine(engine)

        amFloating = ConvertibleFloatingRateBond(
            amExercise, vars.conversionRatio,
            vars.no_callability,
            vars.issueDate, vars.settlementDays,
            index, fixingDays, spreads,
            vars.dayCounter, schedule,
            vars.redemption)
        amFloating.setPricingEngine(engine)

        pricer = BlackIborCouponPricer(
            OptionletVolatilityStructureHandle())

        floatSchedule = Schedule(
            vars.issueDate, vars.maturityDate,
            Period(vars.frequency),
            vars.calendar, Following, Following,
            DateGeneration.Backward, false)

        floating = FloatingRateBond(
            vars.settlementDays, vars.faceAmount, floatSchedule,
            index, vars.dayCounter, Following, fixingDays,
            gearings, spreads,
            DoubleVector(), DoubleVector(),
            false,
            vars.redemption, vars.issueDate)

        floating.setPricingEngine(bondEngine)
        setCouponPricer(floating.cashflows(), pricer)

        tolerance = 2.0e-2 * (vars.faceAmount / 100.0)

        error = abs(euFloating.NPV() - floating.settlementValue())
        self.assertFalse(error > tolerance)

        error = abs(amFloating.NPV() - floating.settlementValue())
        self.assertFalse(error > tolerance)

    def testOption(self):

        TEST_MESSAGE(
            "Testing zero-coupon convertible bonds against vanilla option...")

        vars = CommonVars()

        euExercise = EuropeanExercise(vars.maturityDate)

        vars.settlementDays = 0

        timeSteps = 2001
        engine = BinomialCRRConvertibleEngine(
            vars.process, timeSteps, vars.creditSpread)
        vanillaEngine = BinomialCRRVanillaEngine(
            vars.process, timeSteps)

        vars.creditSpread.linkTo(SimpleQuote(0.0))

        conversionStrike = vars.redemption / vars.conversionRatio
        payoff = PlainVanillaPayoff(Option.Call, conversionStrike)

        schedule = MakeSchedule()
        schedule.fromDate(vars.issueDate)
        schedule.to(vars.maturityDate)
        schedule.withFrequency(Once)
        schedule.withCalendar(vars.calendar)
        schedule.backwards()
        schedule = schedule.makeSchedule()

        euZero = ConvertibleZeroCouponBond(
            euExercise, vars.conversionRatio,
            vars.no_callability,
            vars.issueDate, vars.settlementDays,
            vars.dayCounter, schedule,
            vars.redemption)
        euZero.setPricingEngine(engine)

        euOption = VanillaOption(payoff, euExercise)
        euOption.setPricingEngine(vanillaEngine)

        tolerance = 5.0e-2 * (vars.faceAmount / 100.0)

        expected = vars.faceAmount / 100.0 * (
                vars.redemption * vars.riskFreeRate.discount(vars.maturityDate) +
                vars.conversionRatio * euOption.NPV())
        error = abs(euZero.NPV() - expected)
        self.assertFalse(error > tolerance)

    def testRegression(self):
        TEST_MESSAGE(
            "Testing fixed-coupon convertible bond in known regression case...")

        backup = SavedSettings()

        today = Date(23, December, 2008)
        tomorrow = today + 1

        Settings.instance().evaluationDate = tomorrow

        u = QuoteHandle(SimpleQuote(2.9084382818797443))

        dates = DateVector(25)
        forwards = DoubleVector(25)
        dates[0] = Date(29, December, 2008)
        forwards[0] = 0.0025999342800
        dates[1] = Date(5, January, 2009)
        forwards[1] = 0.0025999342800
        dates[2] = Date(29, January, 2009)
        forwards[2] = 0.0053123275500
        dates[3] = Date(27, February, 2009)
        forwards[3] = 0.0197049598721
        dates[4] = Date(30, March, 2009)
        forwards[4] = 0.0220524845296
        dates[5] = Date(29, June, 2009)
        forwards[5] = 0.0217076395643
        dates[6] = Date(29, December, 2009)
        forwards[6] = 0.0230349627478
        dates[7] = Date(29, December, 2010)
        forwards[7] = 0.0087631647476
        dates[8] = Date(29, December, 2011)
        forwards[8] = 0.0219084299499
        dates[9] = Date(31, December, 2012)
        forwards[9] = 0.0244798766219
        dates[10] = Date(30, December, 2013)
        forwards[10] = 0.0267885498456
        dates[11] = Date(29, December, 2014)
        forwards[11] = 0.0266922867562
        dates[12] = Date(29, December, 2015)
        forwards[12] = 0.0271052126386
        dates[13] = Date(29, December, 2016)
        forwards[13] = 0.0268829891648
        dates[14] = Date(29, December, 2017)
        forwards[14] = 0.0264594744498
        dates[15] = Date(31, December, 2018)
        forwards[15] = 0.0273450367424
        dates[16] = Date(30, December, 2019)
        forwards[16] = 0.0294852614749
        dates[17] = Date(29, December, 2020)
        forwards[17] = 0.0285556119719
        dates[18] = Date(29, December, 2021)
        forwards[18] = 0.0305557764659
        dates[19] = Date(29, December, 2022)
        forwards[19] = 0.0292244738422
        dates[20] = Date(29, December, 2023)
        forwards[20] = 0.0263917004194
        dates[21] = Date(29, December, 2028)
        forwards[21] = 0.0239626970243
        dates[22] = Date(29, December, 2033)
        forwards[22] = 0.0216417108090
        dates[23] = Date(29, December, 2038)
        forwards[23] = 0.0228343838422
        dates[24] = Date(31, December, 2199)
        forwards[24] = 0.0228343838422

        r = YieldTermStructureHandle(
            ForwardCurve(dates, forwards, Actual360()))

        sigma = BlackVolTermStructureHandle(
            BlackConstantVol(
                tomorrow, NullCalendar(), 21.685235548092248,
                Thirty360(Thirty360.BondBasis)))

        process = BlackProcess(u, r, sigma)

        spread = QuoteHandle(SimpleQuote(0.11498700678012874))

        issueDate = Date(23, July, 2008)
        maturityDate = Date(1, August, 2013)
        calendar = UnitedStates(UnitedStates.GovernmentBond)
        schedule = MakeSchedule()
        schedule.fromDate(issueDate)
        schedule.to(maturityDate)
        schedule.withTenor(Period(6, Months))
        schedule.withCalendar(calendar)
        schedule.withConvention(Unadjusted)
        schedule = schedule.makeSchedule()

        settlementDays = 3
        exercise = EuropeanExercise(maturityDate)
        conversionRatio = 100.0 / 20.3175
        coupons = DoubleVector(len(schedule) - 1, 0.05)
        dayCounter = Thirty360(Thirty360.BondBasis)
        no_callability = CallabilitySchedule()
        no_dividends = DividendSchedule()
        redemption = 100.0

        bond = ConvertibleFixedCouponBond(
            exercise, conversionRatio,
            no_callability,
            issueDate, settlementDays,
            coupons, dayCounter,
            schedule, redemption)
        bond.setPricingEngine(
            BinomialCRRConvertibleEngine(
                process, 600, spread, no_dividends))

        try:
            x = bond.NPV()
        except Exception as e:
            print(e)
