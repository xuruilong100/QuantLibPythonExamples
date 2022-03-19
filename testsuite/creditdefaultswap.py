import unittest
from utilities import *
from QuantLib import *
from math import log


class CreditDefaultSwapTest(unittest.TestCase):

    def testCachedValue(self):
        TEST_MESSAGE("Testing credit-default swap against cached values...")

        backup = SavedSettings()

        # Initialize curves
        Settings.instance().evaluationDate = Date(9, June, 2006)
        today = Settings.instance().evaluationDate
        calendar = TARGET()

        hazardRate = QuoteHandle(
            SimpleQuote(0.01234))
        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        probabilityCurve.linkTo(
            FlatHazardRate(0, calendar, hazardRate, Actual360()))

        discountCurve = RelinkableYieldTermStructureHandle()

        discountCurve.linkTo(
            FlatForward(today, 0.06, Actual360()))

        # Build the schedule
        issueDate = calendar.advance(today, -1, Years)
        maturity = calendar.advance(issueDate, 10, Years)
        frequency = Semiannual
        convention = ModifiedFollowing

        schedule = Schedule(
            issueDate, maturity, Period(frequency), calendar,
            convention, convention, DateGeneration.Forward, false)

        # Build the CDS
        fixedRate = 0.0120
        dayCount = Actual360()
        notional = 10000.0
        recoveryRate = 0.4

        cds = CreditDefaultSwap(
            Protection.Seller, notional, fixedRate,
            schedule, convention, dayCount, true, true)
        cds.setPricingEngine(
            MidPointCdsEngine(probabilityCurve, recoveryRate, discountCurve))

        npv = 295.0153398
        fairRate = 0.007517539081

        calculatedNpv = cds.NPV()
        calculatedFairRate = cds.fairSpread()
        tolerance = 1.0e-7

        self.assertFalse(abs(calculatedNpv - npv) > tolerance)

        self.assertFalse(abs(calculatedFairRate - fairRate) > tolerance)

        cds.setPricingEngine(
            IntegralCdsEngine(
                Period(1, Days), probabilityCurve,
                recoveryRate, discountCurve))

        calculatedNpv = cds.NPV()
        calculatedFairRate = cds.fairSpread()
        tolerance = 1.0e-5

        self.assertFalse(abs(calculatedNpv - npv) > notional * tolerance * 10)

        self.assertFalse(abs(calculatedFairRate - fairRate) > tolerance)

        cds.setPricingEngine(
            IntegralCdsEngine(
                Period(1, Weeks), probabilityCurve,
                recoveryRate, discountCurve))

        calculatedNpv = cds.NPV()
        calculatedFairRate = cds.fairSpread()
        tolerance = 1.0e-5

        self.assertFalse(abs(calculatedNpv - npv) > notional * tolerance * 10)

        self.assertFalse(abs(calculatedFairRate - fairRate) > tolerance)

    def testCachedMarketValue(self):
        TEST_MESSAGE(
            "Testing credit-default swap against cached market values...")

        backup = SavedSettings()

        Settings.instance().evaluationDate = Date(9, June, 2006)
        evalDate = Settings.instance().evaluationDate
        calendar = UnitedStates(UnitedStates.GovernmentBond)

        discountDates = [
            evalDate,
            calendar.advance(evalDate, 1, Weeks, ModifiedFollowing),
            calendar.advance(evalDate, 1, Months, ModifiedFollowing),
            calendar.advance(evalDate, 2, Months, ModifiedFollowing),
            calendar.advance(evalDate, 3, Months, ModifiedFollowing),
            calendar.advance(evalDate, 6, Months, ModifiedFollowing),
            calendar.advance(evalDate, 12, Months, ModifiedFollowing),
            calendar.advance(evalDate, 2, Years, ModifiedFollowing),
            calendar.advance(evalDate, 3, Years, ModifiedFollowing),
            calendar.advance(evalDate, 4, Years, ModifiedFollowing),
            calendar.advance(evalDate, 5, Years, ModifiedFollowing),
            calendar.advance(evalDate, 6, Years, ModifiedFollowing),
            calendar.advance(evalDate, 7, Years, ModifiedFollowing),
            calendar.advance(evalDate, 8, Years, ModifiedFollowing),
            calendar.advance(evalDate, 9, Years, ModifiedFollowing),
            calendar.advance(evalDate, 10, Years, ModifiedFollowing),
            calendar.advance(evalDate, 15, Years, ModifiedFollowing)]

        dfs = [
            1.0,
            0.9990151375768731,
            0.99570502636871183,
            0.99118260474528685,
            0.98661167950906203,
            0.9732592953359388,
            0.94724424481038083,
            0.89844996737120875,
            0.85216647839921411,
            0.80775477692556874,
            0.76517289234200347,
            0.72401019553182933,
            0.68503909569219212,
            0.64797499814013748,
            0.61263171936255534,
            0.5791942350748791,
            0.43518868769953606]

        curveDayCounter = Actual360()

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(
            DiscountCurve(discountDates, dfs, curveDayCounter))

        dayCounter = Thirty360(Thirty360.BondBasis)
        dates = DateVector = [
            evalDate,
            calendar.advance(evalDate, 6, Months, ModifiedFollowing),
            calendar.advance(evalDate, 1, Years, ModifiedFollowing),
            calendar.advance(evalDate, 2, Years, ModifiedFollowing),
            calendar.advance(evalDate, 3, Years, ModifiedFollowing),
            calendar.advance(evalDate, 4, Years, ModifiedFollowing),
            calendar.advance(evalDate, 5, Years, ModifiedFollowing),
            calendar.advance(evalDate, 7, Years, ModifiedFollowing),
            calendar.advance(evalDate, 10, Years, ModifiedFollowing)]

        defaultProbabilities = [
            0.0000,
            0.0047,
            0.0093,
            0.0286,
            0.0619,
            0.0953,
            0.1508,
            0.2288,
            0.3666]

        hazardRates = DoubleVector()
        hazardRates.append(0.0)
        for i in range(1, len(dates)):
            t1 = dayCounter.yearFraction(dates[0], dates[i - 1])
            t2 = dayCounter.yearFraction(dates[0], dates[i])
            S1 = 1.0 - defaultProbabilities[i - 1]
            S2 = 1.0 - defaultProbabilities[i]
            hazardRates.append(log(S1 / S2) / (t2 - t1))

        piecewiseFlatHazardRate = RelinkableDefaultProbabilityTermStructureHandle()
        piecewiseFlatHazardRate.linkTo(
            # InterpolatedHazardRateCurve<BackwardFlat>(dates,
            HazardRateCurve(
                dates,
                hazardRates,
                Thirty360(Thirty360.BondBasis)))

        # Testing credit default swap

        # Build the schedule
        issueDate = Date(20, March, 2006)
        maturity = Date(20, June, 2013)
        cdsFrequency = Semiannual
        cdsConvention = ModifiedFollowing

        schedule = Schedule(
            issueDate, maturity, Period(cdsFrequency), calendar,
            cdsConvention, cdsConvention,
            DateGeneration.Forward, false)

        # Build the CDS
        recoveryRate = 0.25
        fixedRate = 0.0224
        dayCount = Actual360()
        cdsNotional = 100.0

        cds = CreditDefaultSwap(
            Protection.Seller, cdsNotional, fixedRate,
            schedule, cdsConvention, dayCount, true, true)
        cds.setPricingEngine(
            MidPointCdsEngine(
                piecewiseFlatHazardRate, recoveryRate, discountCurve))

        calculatedNpv = cds.NPV()
        calculatedFairRate = cds.fairSpread()

        npv = -1.364048777  # from Bloomberg we have 98.15598868 - 100.00
        fairRate = 0.0248429452  # from Bloomberg we have 0.0258378

        tolerance = 1e-9

        self.assertFalse(abs(npv - calculatedNpv) > tolerance)

        self.assertFalse(abs(fairRate - calculatedFairRate) > tolerance)

    def testImpliedHazardRate(self):
        TEST_MESSAGE("Testing implied hazard-rate for credit-default swaps...")

        backup = SavedSettings()

        # Initialize curves
        calendar = TARGET()
        today = calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = today

        h1 = 0.30
        h2 = 0.40
        dayCounter = Actual365Fixed()

        dates = DateVector(3)
        hazardRates = DoubleVector(3)
        dates[0] = today
        hazardRates[0] = h1

        dates[1] = today + Period(5, Years)
        hazardRates[1] = h1

        dates[2] = today + Period(10, Years)
        hazardRates[2] = h2

        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        probabilityCurve.linkTo(
            # InterpolatedHazardRateCurve<BackwardFlat>
            HazardRateCurve(
                dates, hazardRates, dayCounter))

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(
            FlatForward(today, 0.03, Actual360()))

        frequency = Semiannual
        convention = ModifiedFollowing

        issueDate = calendar.advance(today, -6, Months)
        fixedRate = 0.0120
        cdsDayCount = Actual360()
        notional = 10000.0
        recoveryRate = 0.4

        latestRate = NullReal()
        for n in range(6, 10 + 1):  # (n = 6 n <= 10 ++n) {

            maturity = calendar.advance(issueDate, n, Years)
            schedule = Schedule(
                issueDate, maturity, Period(frequency), calendar,
                convention, convention,
                DateGeneration.Forward, false)

            cds = CreditDefaultSwap(
                Protection.Seller, notional, fixedRate,
                schedule, convention, cdsDayCount,
                true, true)
            cds.setPricingEngine(
                MidPointCdsEngine(
                    probabilityCurve, recoveryRate, discountCurve))

            NPV = cds.NPV()
            flatRate = cds.impliedHazardRate(
                NPV, discountCurve, dayCounter, recoveryRate)

            self.assertFalse(flatRate < h1 or flatRate > h2)
            self.assertFalse(n > 6 and flatRate < latestRate)

            latestRate = flatRate

            probability = RelinkableDefaultProbabilityTermStructureHandle()
            probability.linkTo(
                FlatHazardRate(
                    today, QuoteHandle(SimpleQuote(flatRate)), dayCounter))
            cds2 = CreditDefaultSwap(
                Protection.Seller, notional, fixedRate,
                schedule, convention, cdsDayCount,
                true, true)
            cds2.setPricingEngine(
                MidPointCdsEngine(
                    probability, recoveryRate, discountCurve))

            NPV2 = cds2.NPV()
            tolerance = 1.0
            self.assertFalse(abs(NPV - NPV2) > tolerance)

    def testFairSpread(self):
        TEST_MESSAGE(
            "Testing fair-spread calculation for credit-default swaps...")

        backup = SavedSettings()

        # Initialize curves
        calendar = TARGET()
        today = calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = today

        hazardRate = QuoteHandle(
            SimpleQuote(0.01234))
        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        probabilityCurve.linkTo(
            FlatHazardRate(0, calendar, hazardRate, Actual360()))

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(
            FlatForward(today, 0.06, Actual360()))

        # Build the schedule
        issueDate = calendar.advance(today, -1, Years)
        maturity = calendar.advance(issueDate, 10, Years)
        convention = Following

        schedule = MakeSchedule()
        schedule.fromDate(issueDate)
        schedule.to(maturity)
        schedule.withFrequency(Quarterly)
        schedule.withCalendar(calendar)
        schedule.withTerminationDateConvention(convention)
        schedule.withRule(DateGeneration.TwentiethIMM)
        schedule = schedule.makeSchedule()

        # Build the CDS
        fixedRate = 0.001
        dayCount = Actual360()
        notional = 10000.0
        recoveryRate = 0.4

        engine = MidPointCdsEngine(probabilityCurve, recoveryRate, discountCurve)

        cds = CreditDefaultSwap(
            Protection.Seller, notional, fixedRate,
            schedule, convention, dayCount, true, true)
        cds.setPricingEngine(engine)

        fairRate = cds.fairSpread()

        fairCds = CreditDefaultSwap(
            Protection.Seller, notional, fairRate,
            schedule, convention, dayCount, true, true)
        fairCds.setPricingEngine(engine)

        fairNPV = fairCds.NPV()
        tolerance = 1e-9

        self.assertFalse(abs(fairNPV) > tolerance)

    def testFairUpfront(self):
        TEST_MESSAGE(
            "Testing fair-upfront calculation for credit-default swaps...")

        backup = SavedSettings()

        # Initialize curves
        calendar = TARGET()
        today = calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = today

        hazardRate = QuoteHandle(
            SimpleQuote(0.01234))
        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        probabilityCurve.linkTo(
            FlatHazardRate(0, calendar, hazardRate, Actual360()))

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(
            FlatForward(today, 0.06, Actual360()))

        # Build the schedule
        issueDate = today
        maturity = calendar.advance(issueDate, 10, Years)
        convention = Following

        schedule = MakeSchedule()
        schedule.fromDate(issueDate)
        schedule.to(maturity)
        schedule.withFrequency(Quarterly)
        schedule.withCalendar(calendar)
        schedule.withTerminationDateConvention(convention)
        schedule.withRule(DateGeneration.TwentiethIMM)
        schedule = schedule.makeSchedule()

        # Build the CDS
        fixedRate = 0.05
        upfront = 0.001
        dayCount = Actual360()
        notional = 10000.0
        recoveryRate = 0.4

        engine = MidPointCdsEngine(
            probabilityCurve, recoveryRate,
            discountCurve, true)

        cds = CreditDefaultSwap(
            Protection.Seller, notional, upfront, fixedRate,
            schedule, convention, dayCount, true, true)
        cds.setPricingEngine(engine)

        fairUpfront = cds.fairUpfront()

        fairCds = CreditDefaultSwap(
            Protection.Seller, notional,
            fairUpfront, fixedRate,
            schedule, convention, dayCount, true, true)
        fairCds.setPricingEngine(engine)

        fairNPV = fairCds.NPV()
        tolerance = 1e-9

        self.assertFalse(abs(fairNPV) > tolerance)

        # same with null upfront to begin with
        upfront = 0.0
        cds2 = CreditDefaultSwap(
            Protection.Seller, notional, upfront, fixedRate,
            schedule, convention, dayCount, true, true)
        cds2.setPricingEngine(engine)

        fairUpfront = cds2.fairUpfront()

        fairCds2 = CreditDefaultSwap(
            Protection.Seller, notional,
            fairUpfront, fixedRate,
            schedule, convention, dayCount, true, true)
        fairCds2.setPricingEngine(engine)

        fairNPV = fairCds2.NPV()

        self.assertFalse(abs(fairNPV) > tolerance)

    def testIsdaEngine(self):
        TEST_MESSAGE(
            "Testing ISDA engine calculations for credit-default swaps...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        backup = SavedSettings()

        tradeDate = Date(21, May, 2009)
        Settings.instance().evaluationDate = tradeDate

        # build an ISDA compliant yield curve
        # data comes from Markit published rates
        isdaRateHelpers = RateHelperVector()
        dep_tenors = [1, 2, 3, 6, 9, 12]
        dep_quotes = [
            0.003081, 0.005525, 0.007163, 0.012413, 0.014, 0.015488]

        for i in range(len(dep_tenors)):
            isdaRateHelpers.append(
                DepositRateHelper(
                    dep_quotes[i], Period(dep_tenors[i], Months), 2,
                    WeekendsOnly(), ModifiedFollowing,
                    false, Actual360()))

        swap_tenors = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30]
        swap_quotes = [
            0.011907, 0.01699, 0.021198, 0.02444, 0.026937, 0.028967, 0.030504,
            0.031719, 0.03279, 0.034535, 0.036217, 0.036981, 0.037246, 0.037605]

        isda_ibor = IborIndex(
            "IsdaIbor", Period(3, Months), 2, USDCurrency(), WeekendsOnly(),
            ModifiedFollowing, false, Actual360())
        for i in range(len(swap_tenors)):
            isdaRateHelpers.append(
                SwapRateHelper(
                    swap_quotes[i],
                    Period(swap_tenors[i], Years),
                    WeekendsOnly(),
                    Semiannual,
                    ModifiedFollowing,
                    Thirty360(Thirty360.BondBasis),
                    isda_ibor))

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(
            # PiecewiseYieldCurve<Discount, LogLinear>
            PiecewiseLogLinearDiscount(
                0, WeekendsOnly(), isdaRateHelpers, Actual365Fixed(), LogLinear()))

        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        termDates = [
            Date(20, June, 2010),
            Date(20, June, 2011),
            Date(20, June, 2012),
            Date(20, June, 2016),
            Date(20, June, 2019)]
        spreads = [0.001, 0.1]
        recoveries = [0.2, 0.4]

        markitValues = [
            97798.29358,  # 0.001
            97776.11889,  # 0.001
            -914971.5977,  # 0.1
            -894985.6298,  # 0.1
            186921.3594,  # 0.001
            186839.8148,  # 0.001
            -1646623.672,  # 0.1
            -1579803.626,  # 0.1
            274298.9203,
            274122.4725,
            -2279730.93,
            -2147972.527,
            592420.2297,
            591571.2294,
            -3993550.206,
            -3545843.418,
            797501.1422,
            795915.9787,
            -4702034.688,
            -4042340.999]
        # When using indexes coupons, the risk-free curve is a bit off.
        # We might skip the tests altogether and rely on running them
        # with indexed coupons disabled, but leaving them can be useful anyway.
        tolerance = 1.0e-6 if usingAtParCoupons else 1.0e-3

        l = 0

        for termDate in termDates:
            for spread in spreads:
                for recoverie in recoveries:
                    quotedTrade = MakeCreditDefaultSwap(termDate, spread)
                    quotedTrade.withNominal(10000000.)
                    quotedTrade = quotedTrade.makeCDS()

                    h = quotedTrade.impliedHazardRate(
                        0., discountCurve, Actual365Fixed(),
                        recoverie, 1e-10, CreditDefaultSwap.ISDA)

                    probabilityCurve.linkTo(
                        FlatHazardRate(0, WeekendsOnly(), h, Actual365Fixed()))

                    engine = IsdaCdsEngine(
                        probabilityCurve, recoverie, discountCurve, None, IsdaCdsEngine.Taylor,
                        IsdaCdsEngine.HalfDayBias, IsdaCdsEngine.Piecewise)

                    conventionalTrade = MakeCreditDefaultSwap(termDate, 0.01)
                    conventionalTrade.withNominal(10000000.0)
                    conventionalTrade.withPricingEngine(engine)
                    conventionalTrade = conventionalTrade.makeCDS()

                    diff = abs(
                        conventionalTrade.notional() * conventionalTrade.fairUpfront() - markitValues[l])
                    x = diff / min(
                        conventionalTrade.notional() * conventionalTrade.fairUpfront(),
                        markitValues[l])

                    self.assertTrue(
                        x < tolerance)

                    l += 1

    def testAccrualRebateAmounts(self):
        TEST_MESSAGE("Testing accrual rebate amounts on credit default swaps...")

        backup = SavedSettings()

        # The accrual values are taken from various test results on the ISDA CDS model website
        # https:#www.cdsmodel.com/cdsmodel/documentation.html.

        # Inputs
        notional = 10000000
        spread = 0.0100
        maturity = Date(20, Jun, 2014)

        # key is trade date and value is expected accrual
        # typedef map<Date, Real> InputData
        inputs = [
            (Date(18, Mar, 2009), 24166.67),
            (Date(19, Mar, 2009), 0.00),
            (Date(20, Mar, 2009), 277.78),
            (Date(23, Mar, 2009), 1111.11),
            (Date(19, Jun, 2009), 25555.56),
            (Date(20, Jun, 2009), 25833.33),
            (Date(21, Jun, 2009), 0.00),
            (Date(22, Jun, 2009), 277.78),
            (Date(18, Jun, 2014), 25277.78),
            (Date(19, Jun, 2014), 25555.56)]

        for input in inputs:
            Settings.instance().evaluationDate = input[0]
            cds = MakeCreditDefaultSwap(maturity, spread)
            cds.withNominal(notional)
            cds = cds.makeCDS()
            self.assertLess(input[1] - cds.accrualRebate().amount(), 0.01)
