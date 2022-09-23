import unittest

from QuantLib import *

from utilities import *

data = [
    (Date(1, February, 2012), 100),
    (Date(1, July, 2013), 150),
    (Date(5, January, 2014), 50)]
sampleEvents = data

eventsStart = Date(1, January, 2011)
eventsEnd = Date(31, December, 2014)


class CommonVars(object):

    def __init__(self):
        self.calendar = TARGET()
        self.today = self.calendar.adjust(knownGoodDefault)
        Settings.instance().evaluationDate = self.today
        self.faceAmount = 1000000.0
        self.backup = SavedSettings()


class CatBondTest(unittest.TestCase):

    def testEventSetForWholeYears(self):
        TEST_MESSAGE(
            "Testing that catastrophe events are split correctly for periods of whole years...")

        catRisk = EventSet(sampleEvents, eventsStart, eventsEnd)
        simulation = catRisk.newSimulation(
            Date(1, January, 2015), Date(31, December, 2015))

        self.assertTrue(simulation)

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(rst[0])
        self.assertEqual(0, len(path))

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(rst[0])
        self.assertEqual(1, len(path))
        self.assertEqual(Date(1, February, 2015), path[0][0])
        self.assertEqual(100, path[0][1])

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(rst[0])
        self.assertEqual(1, len(path))
        self.assertEqual(Date(1, July, 2015), path[0][0])
        self.assertEqual(150, path[0][1])

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(rst[0])
        self.assertEqual(1, len(path))
        self.assertEqual(Date(5, January, 2015), path[0][0])
        self.assertEqual(50, path[0][1])

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(not rst[0])

    def testEventSetForIrregularPeriods(self):
        TEST_MESSAGE(
            "Testing that catastrophe events are split correctly for irregular periods...")

        catRisk = EventSet(sampleEvents, eventsStart, eventsEnd)
        simulation = catRisk.newSimulation(
            Date(2, January, 2015), Date(5, January, 2016))

        self.assertTrue(simulation)

        rst = simulation.nextPath()
        path = rst[1]

        self.assertTrue(rst[0])
        self.assertEqual(0, len(path))

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(rst[0])
        self.assertEqual(2, len(path))
        self.assertEqual(Date(1, July, 2015), path[0][0])
        self.assertEqual(150, path[0][1])
        self.assertEqual(Date(5, January, 2016), path[1][0])
        self.assertEqual(50, path[1][1])

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(not rst[0])

    def testEventSetForNoEvents(self):
        TEST_MESSAGE(
            "Testing that catastrophe events are split correctly when there are no simulated events...")

        emptyEvents = []
        catRisk = EventSet(emptyEvents, eventsStart, eventsEnd)
        simulation = catRisk.newSimulation(
            Date(2, January, 2015), Date(5, January, 2016))

        self.assertTrue(simulation)

        rst = simulation.nextPath()
        path = rst[1]

        self.assertTrue(rst[0])
        self.assertEqual(0, len(path))

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(rst[0])
        self.assertEqual(0, len(path))

        rst = simulation.nextPath()
        path = rst[1]
        self.assertTrue(not rst[0])

    def testBetaRisk(self):
        TEST_MESSAGE(
            "Testing that beta risk gives correct terminal distribution...")

        PATHS = 1000000
        catRisk = BetaRisk(100.0, 100.0, 10.0, 15.0)
        simulation = catRisk.newSimulation(
            Date(2, January, 2015), Date(2, January, 2018))
        self.assertTrue(simulation)

        sum = 0.0
        sumSquares = 0.0
        poissonSum = 0.0
        poissonSumSquares = 0.0

        for i in range(PATHS):
            rst = simulation.nextPath()
            path = rst[1]
            self.assertTrue(rst[0])
            processValue = 0.0
            for j in path:
                processValue += j[1]
            sum += processValue
            sumSquares += processValue * processValue
            poissonSum += len(path)
            poissonSumSquares += len(path) * len(path)

        poissonMean = poissonSum / PATHS
        self.assertFalse(
            abs(3.0 / 100.0 - poissonMean) /
            min(abs(3.0 / 100.0), abs(poissonMean)) > 2 / 100.0)
        poissonVar = poissonSumSquares / PATHS - poissonMean * poissonMean
        self.assertFalse(
            abs(3.0 / 100.0 - poissonVar) /
            min(abs(3.0 / 100.0), abs(poissonVar)) > 5 / 100.0)

        expectedMean = 3.0 * 10.0 / 100.0
        actualMean = sum / PATHS
        self.assertFalse(
            abs(expectedMean - actualMean) / min(
                abs(expectedMean), abs(actualMean)) > 1 / 100.0)

        expectedVar = 3.0 * (15.0 * 15.0 + 10 * 10) / 100.0
        actualVar = sumSquares / PATHS - actualMean * actualMean
        self.assertFalse(
            abs(expectedVar - actualVar) / min(
                abs(expectedVar), abs(actualVar)) > 1 / 100.0)

    def testRiskFreeAgainstFloatingRateBond(self):
        TEST_MESSAGE(
            "Testing floating-rate cat bond against risk-free floating-rate bond...")

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

        pricer = BlackIborCouponPricer(
            OptionletVolatilityStructureHandle())

        sch = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2008),
            Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)

        noCatRisk = EventSet(
            [], Date(1, Jan, 2000), Date(31, Dec, 2010))

        paymentOffset = NoOffset()
        notionalRisk = DigitalNotionalRisk(paymentOffset, 100)

        bond1 = FloatingRateBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        catBond1 = FloatingCatBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            notionalRisk,
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        bondEngine = DiscountingBondEngine(riskFreeRate)
        bond1.setPricingEngine(bondEngine)
        setCouponPricer(bond1.cashflows(), pricer)

        catBondEngine = MonteCarloCatBondEngine(noCatRisk, riskFreeRate)
        catBond1.setPricingEngine(catBondEngine)
        setCouponPricer(catBond1.cashflows(), pricer)

        cachedPrice1 = 99.874646 if usingAtParCoupons else 99.874645

        price = bond1.cleanPrice()
        catPrice = catBond1.cleanPrice()
        self.assertFalse(
            abs(price - cachedPrice1) > tolerance or abs(catPrice - price) > tolerance)

        bond2 = FloatingRateBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        catBond2 = FloatingCatBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            notionalRisk,
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        bondEngine2 = DiscountingBondEngine(discountCurve)
        bond2.setPricingEngine(bondEngine2)
        setCouponPricer(bond2.cashflows(), pricer)

        catBondEngine2 = MonteCarloCatBondEngine(noCatRisk, discountCurve)
        catBond2.setPricingEngine(catBondEngine2)
        setCouponPricer(catBond2.cashflows(), pricer)

        cachedPrice2 = 97.955904

        price = bond2.cleanPrice()
        catPrice = catBond2.cleanPrice()
        self.assertFalse(abs(price - cachedPrice2) > tolerance or abs(catPrice - price) > tolerance)

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

        catBond3 = FloatingCatBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            notionalRisk,
            ModifiedFollowing, fixingDays,
            DoubleVector(), spreads,
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        bond3.setPricingEngine(bondEngine2)
        setCouponPricer(bond3.cashflows(), pricer)

        catBond3.setPricingEngine(catBondEngine2)
        setCouponPricer(catBond3.cashflows(), pricer)

        cachedPrice3 = 98.495459 if usingAtParCoupons else 98.495458

        price = bond3.cleanPrice()
        catPrice = catBond3.cleanPrice()
        self.assertFalse(abs(price - cachedPrice3) > tolerance or abs(catPrice - price) > tolerance)

    def testCatBondInDoomScenario(self):
        TEST_MESSAGE(
            "Testing floating-rate cat bond in a doom scenario (certain default)...")

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

        sch = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2008),
            Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)

        events = []
        events.append((Date(30, November, 2004), 1000))
        doomCatRisk = EventSet(
            events,
            Date(30, November, 2004), Date(30, November, 2008))

        paymentOffset = NoOffset()
        notionalRisk = DigitalNotionalRisk(paymentOffset, 100)

        catBond = FloatingCatBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            notionalRisk,
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        catBondEngine = MonteCarloCatBondEngine(doomCatRisk, discountCurve)
        catBond.setPricingEngine(catBondEngine)
        setCouponPricer(catBond.cashflows(), pricer)

        price = catBond.cleanPrice()
        self.assertEqual(0, price)

        lossProbability = catBond.lossProbability()
        exhaustionProbability = catBond.exhaustionProbability()
        expectedLoss = catBond.expectedLoss()

        self.assertFalse(
            abs(1.0 - lossProbability) / min(
                abs(1.0), abs(lossProbability)) > tolerance / 100.0)
        self.assertFalse(
            abs(1.0 - exhaustionProbability) / min(
                abs(1.0), abs(exhaustionProbability)) > tolerance / 100.0)
        self.assertFalse(
            abs(1.0 - expectedLoss) / min(
                abs(1.0), abs(expectedLoss)) > tolerance / 100.0)

    def testCatBondWithDoomOnceInTenYears(self):
        TEST_MESSAGE(
            "Testing floating-rate cat bond in a doom once in 10 years scenario...")

        vars = CommonVars()

        today = Date(22, November, 2004)
        Settings.instance().evaluationDate = today

        settlementDays = 1

        riskFreeRate = YieldTermStructureHandle(flatRate(today, 0.025, Actual360()))
        discountCurve = YieldTermStructureHandle(flatRate(today, 0.03, Actual360()))

        index = USDLibor(Period(6, Months), riskFreeRate)
        fixingDays = 1

        tolerance = 1.0e-6

        pricer = BlackIborCouponPricer(
            OptionletVolatilityStructureHandle())

        sch = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2008),
            Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)

        events = []
        events.append((Date(30, November, 2008), 1000))
        doomCatRisk = EventSet(
            events, Date(30, November, 2004), Date(30, November, 2044))

        noCatRisk = EventSet(
            [], Date(1, Jan, 2000), Date(31, Dec, 2010))

        paymentOffset = NoOffset()
        notionalRisk = DigitalNotionalRisk(paymentOffset, 100)

        catBond = FloatingCatBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            notionalRisk,
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        catBondEngine = MonteCarloCatBondEngine(doomCatRisk, discountCurve)
        catBond.setPricingEngine(catBondEngine)
        setCouponPricer(catBond.cashflows(), pricer)

        price = catBond.cleanPrice()
        bondYield = catBond.bondYield(
            ActualActual(ActualActual.ISMA), Simple, Annual)
        lossProbability = catBond.lossProbability()
        exhaustionProbability = catBond.exhaustionProbability()
        expectedLoss = catBond.expectedLoss()

        self.assertFalse(
            abs(0.1 - lossProbability) / min(
                abs(0.1), abs(lossProbability)) > tolerance / 100.0)
        self.assertFalse(
            abs(0.1 - exhaustionProbability) / min(
                abs(0.1), abs(exhaustionProbability)) > tolerance / 100.0)
        self.assertFalse(
            abs(0.1 - expectedLoss) / min(
                abs(0.1), abs(expectedLoss)) > tolerance / 100.0)

        catBondEngineRF = MonteCarloCatBondEngine(noCatRisk, discountCurve)
        catBond.setPricingEngine(catBondEngineRF)

        riskFreePrice = catBond.cleanPrice()
        riskFreeYield = catBond.bondYield(
            ActualActual(ActualActual.ISMA), Simple, Annual)
        riskFreeLossProbability = catBond.lossProbability()
        riskFreeExhaustionProbability = catBond.exhaustionProbability()
        riskFreeExpectedLoss = catBond.expectedLoss()

        self.assertFalse(
            abs(0.0 - riskFreeLossProbability) > tolerance / 100.0)
        self.assertFalse(
            abs(0.0 - riskFreeExhaustionProbability) > tolerance / 100.0)
        self.assertTrue(abs(riskFreeExpectedLoss) < tolerance)

        self.assertFalse(
            abs(riskFreePrice * 0.9 - price) / min(
                abs(riskFreePrice * 0.9), abs(price)) > tolerance / 100.0)
        self.assertLess(riskFreeYield, bondYield)

    def testCatBondWithDoomOnceInTenYearsProportional(self):
        TEST_MESSAGE(
            "Testing floating-rate cat bond in a doom once in 10 years scenario with proportional notional reduction...")

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

        sch = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2008),
            Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)

        events = []
        events.append((Date(30, November, 2008), 1000))
        doomCatRisk = EventSet(
            events, Date(30, November, 2004), Date(30, November, 2044))

        noCatRisk = EventSet(
            [], Date(1, Jan, 2000), Date(31, Dec, 2010))

        paymentOffset = NoOffset()
        notionalRisk = ProportionalNotionalRisk(paymentOffset, 500, 1500)

        catBond = FloatingCatBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            notionalRisk,
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        catBondEngine = MonteCarloCatBondEngine(doomCatRisk, discountCurve)
        catBond.setPricingEngine(catBondEngine)
        setCouponPricer(catBond.cashflows(), pricer)

        price = catBond.cleanPrice()
        bondYield = catBond.bondYield(ActualActual(ActualActual.ISMA), Simple, Annual)
        lossProbability = catBond.lossProbability()
        exhaustionProbability = catBond.exhaustionProbability()
        expectedLoss = catBond.expectedLoss()

        self.assertFalse(
            abs(0.1 - lossProbability) / min(
                abs(0.1), abs(lossProbability)) > tolerance / 100.0)
        self.assertFalse(
            abs(0.0 - exhaustionProbability) > tolerance / 100.0)
        self.assertFalse(
            abs(0.05 - expectedLoss) / min(
                abs(0.05), abs(expectedLoss)) > tolerance / 100.0)

        catBondEngineRF = MonteCarloCatBondEngine(noCatRisk, discountCurve)
        catBond.setPricingEngine(catBondEngineRF)

        riskFreePrice = catBond.cleanPrice()
        riskFreeYield = catBond.bondYield(ActualActual(ActualActual.ISMA), Simple, Annual)
        riskFreeLossProbability = catBond.lossProbability()
        riskFreeExpectedLoss = catBond.expectedLoss()

        self.assertFalse(
            abs(0.0 - riskFreeLossProbability) > tolerance / 100.0)
        self.assertTrue(abs(riskFreeExpectedLoss) < tolerance / 100.0)

        self.assertFalse(
            abs(riskFreePrice * 0.95 - price) / min(
                abs(riskFreePrice * 0.95), abs(price)) > tolerance / 100.0)
        self.assertLess(riskFreeYield, bondYield)

    def testCatBondWithGeneratedEventsProportional(self):
        TEST_MESSAGE(
            "Testing floating-rate cat bond in a generated scenario with proportional notional reduction...")

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

        sch = Schedule(
            Date(30, November, 2004),
            Date(30, November, 2008),
            Period(Semiannual),
            UnitedStates(UnitedStates.GovernmentBond),
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)

        betaCatRisk = BetaRisk(5000, 50, 500, 500)

        noCatRisk = EventSet(
            [], Date(1, Jan, 2000), Date(31, Dec, 2010))

        paymentOffset = NoOffset()
        notionalRisk = ProportionalNotionalRisk(paymentOffset, 500, 1500)

        catBond = FloatingCatBond(
            settlementDays, vars.faceAmount, sch,
            index, ActualActual(ActualActual.ISMA),
            notionalRisk,
            ModifiedFollowing, fixingDays,
            DoubleVector(), DoubleVector(),
            DoubleVector(), DoubleVector(),
            false,
            100.0, Date(30, November, 2004))

        catBondEngine = MonteCarloCatBondEngine(betaCatRisk, discountCurve)
        catBond.setPricingEngine(catBondEngine)
        setCouponPricer(catBond.cashflows(), pricer)

        price = catBond.cleanPrice()
        bondYield = catBond.bondYield(
            ActualActual(ActualActual.ISMA), Simple, Annual)
        lossProbability = catBond.lossProbability()
        exhaustionProbability = catBond.exhaustionProbability()
        expectedLoss = catBond.expectedLoss()

        self.assertTrue(lossProbability < 1.0 and lossProbability > 0.0)
        self.assertTrue(exhaustionProbability < 1.0 and exhaustionProbability > 0.0)
        self.assertTrue(expectedLoss > 0.0)

        catBondEngineRF = MonteCarloCatBondEngine(noCatRisk, discountCurve)
        catBond.setPricingEngine(catBondEngineRF)

        riskFreePrice = catBond.cleanPrice()
        riskFreeYield = catBond.bondYield(
            ActualActual(ActualActual.ISMA), Simple, Annual)
        riskFreeLossProbability = catBond.lossProbability()
        riskFreeExpectedLoss = catBond.expectedLoss()

        self.assertFalse(
            abs(0.0 - riskFreeLossProbability) > tolerance / 100.0)
        self.assertTrue(abs(riskFreeExpectedLoss) < tolerance)

        self.assertGreater(riskFreePrice, price)
        self.assertLess(riskFreeYield, bondYield)
