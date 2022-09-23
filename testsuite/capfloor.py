import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.nominals = DoubleVector(1, 100)
        self.frequency = Semiannual
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.index = Euribor6M(self.termStructure)
        self.calendar = self.index.fixingCalendar()
        self.convention = ModifiedFollowing
        self.today = self.calendar.adjust(knownGoodDefault)
        Settings.instance().evaluationDate = self.today
        self.settlementDays = 2
        self.fixingDays = 2
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)
        self.termStructure.linkTo(
            flatRate(
                self.settlement, 0.05, ActualActual(ActualActual.ISDA)))
        self.backup = SavedSettings()

    def makeLeg(self,
                startDate,
                length):
        endDate = self.calendar.advance(
            startDate, Period(length, Years), self.convention)
        schedule = Schedule(
            startDate, endDate, Period(self.frequency), self.calendar,
            self.convention, self.convention,
            DateGeneration.Forward, false)
        leg = IborLeg(schedule, self.index)
        leg.withNotionals(self.nominals)
        leg.withPaymentDayCounter(self.index.dayCounter())
        leg.withPaymentAdjustment(self.convention)
        leg.withFixingDays(self.fixingDays)
        leg = leg.makeLeg()
        return leg

    def makeEngine(self, volatility):
        vol = QuoteHandle(
            SimpleQuote(volatility))
        return BlackCapFloorEngine(self.termStructure, vol)

    def makeBachelierEngine(self, volatility):
        vol = QuoteHandle(
            SimpleQuote(volatility))
        return BachelierCapFloorEngine(self.termStructure, vol)

    def makeCapFloor(self,
                     typ,
                     leg,
                     strike,
                     volatility,
                     isLogNormal=true):
        result = None
        if typ == CapFloor.Cap:
            result = Cap(leg, DoubleVector(1, strike))

        if typ == CapFloor.Floor:
            result = Floor(leg, DoubleVector(1, strike))

        if isLogNormal:
            result.setPricingEngine(self.makeEngine(volatility))
        else:
            result.setPricingEngine(self.makeBachelierEngine(volatility))

        return result


def checkAbsError(x1, x2, tolerance):
    return abs(x1 - x2) < tolerance


def typeToString(type):
    if type == CapFloor.Cap:
        return "cap"
    if type == CapFloor.Floor:
        return "floor"
    if type == CapFloor.Collar:
        return "collar"


class CapFloorTest(unittest.TestCase):

    def testStrikeDependency(self):
        TEST_MESSAGE(
            "Testing cap/floor dependency on strike...")

        vars = CommonVars()

        lengths = [1, 2, 3, 5, 7, 10, 15, 20]
        vols = [0.01, 0.05, 0.10, 0.15, 0.20]
        strikes = [0.03, 0.04, 0.05, 0.06, 0.07]

        startDate = vars.termStructure.referenceDate()

        for length in lengths:
            for vol in vols:
                cap_values = DoubleVector()
                floor_values = DoubleVector()
                for strike in strikes:
                    leg = vars.makeLeg(startDate, length)
                    cap = vars.makeCapFloor(CapFloor.Cap, leg, strike, vol)
                    cap_values.push_back(cap.NPV())
                    floor = vars.makeCapFloor(CapFloor.Floor, leg, strike, vol)
                    floor_values.push_back(floor.NPV())

                it = 1
                while cap_values[it - 1] >= cap_values[it]:
                    it += 1
                    if it >= len(cap_values) - 1:
                        break

                self.assertFalse(it != len(cap_values) - 1)

                it = 1
                while floor_values[it - 1] <= floor_values[it]:
                    it += 1
                    if it >= len(floor_values) - 1:
                        break

                self.assertFalse(it != len(floor_values) - 1)

    def testConsistency(self):
        TEST_MESSAGE(
            "Testing consistency between cap, floor and collar...")

        vars = CommonVars()

        lengths = [1, 2, 3, 5, 7, 10, 15, 20]
        cap_rates = [0.03, 0.04, 0.05, 0.06, 0.07]
        floor_rates = [0.03, 0.04, 0.05, 0.06, 0.07]
        vols = [0.01, 0.05, 0.10, 0.15, 0.20]

        startDate = vars.termStructure.referenceDate()

        for length in lengths:
            for cap_rate in cap_rates:
                for floor_rate in floor_rates:
                    for vol in vols:

                        leg = vars.makeLeg(startDate, length)
                        cap = vars.makeCapFloor(CapFloor.Cap, leg, cap_rate, vol)
                        floor = vars.makeCapFloor(CapFloor.Floor, leg, floor_rate, vol)
                        collar = Collar(
                            leg, DoubleVector(1, cap_rate),
                            DoubleVector(1, floor_rate))
                        collar.setPricingEngine(vars.makeEngine(vol))

                        self.assertFalse(abs((cap.NPV() - floor.NPV()) - collar.NPV()) > 1e-10)

                        capletsNPV = 0.0
                        caplets = []
                        for m in range(length * 2):
                            caplets.append(cap.optionlet(m))
                            caplets[m].setPricingEngine(vars.makeEngine(vol))
                            capletsNPV += caplets[m].NPV()

                        self.assertFalse(abs(cap.NPV() - capletsNPV) > 1e-10)

                        floorletsNPV = 0.0
                        floorlets = []
                        for m in range(length * 2):
                            floorlets.append(floor.optionlet(m))
                            floorlets[m].setPricingEngine(vars.makeEngine(vol))
                            floorletsNPV += floorlets[m].NPV()

                        self.assertFalse(abs(floor.NPV() - floorletsNPV) > 1e-10)

                        collarletsNPV = 0.0
                        collarlets = []
                        for m in range(length * 2):
                            collarlets.append(collar.optionlet(m))
                            collarlets[m].setPricingEngine(vars.makeEngine(vol))
                            collarletsNPV += collarlets[m].NPV()

                        self.assertFalse(abs(collar.NPV() - collarletsNPV) > 1e-10)

    def testParity(self):
        TEST_MESSAGE(
            "Testing cap/floor parity...")

        vars = CommonVars()

        lengths = [1, 2, 3, 5, 7, 10, 15, 20]
        strikes = [0., 0.03, 0.04, 0.05, 0.06, 0.07]
        vols = [0.01, 0.05, 0.10, 0.15, 0.20]

        startDate = vars.termStructure.referenceDate()

        for length in lengths:
            for strike in strikes:
                for vol in vols:
                    leg = vars.makeLeg(startDate, length)
                    cap = vars.makeCapFloor(CapFloor.Cap, leg, strike, vol)
                    floor = vars.makeCapFloor(CapFloor.Floor, leg, strike, vol)
                    maturity = vars.calendar.advance(startDate, length, Years, vars.convention)
                    schedule = Schedule(
                        startDate, maturity, Period(vars.frequency), vars.calendar,
                        vars.convention, vars.convention, DateGeneration.Forward, false)
                    swap = VanillaSwap(
                        Swap.Payer, vars.nominals[0], schedule, strike,
                        vars.index.dayCounter(), schedule, vars.index, 0.0,
                        vars.index.dayCounter())
                    swap.setPricingEngine(
                        DiscountingSwapEngine(vars.termStructure))
                    self.assertFalse(
                        abs((cap.NPV() - floor.NPV()) - swap.NPV()) > 1.0e-10)

    def testVega(self):
        TEST_MESSAGE(
            "Testing cap/floor vega...")

        vars = CommonVars()

        lengths = [1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 30]
        vols = [0.01, 0.05, 0.10, 0.15, 0.20]
        strikes = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
        types = [CapFloor.Cap, CapFloor.Floor]

        startDate = vars.termStructure.referenceDate()
        shift = 1e-8
        tolerance = 0.005

        for length in lengths:
            for vol in vols:
                for strike in strikes:
                    for ty in types:
                        leg = vars.makeLeg(startDate, length)
                        capFloor = vars.makeCapFloor(ty, leg, strike, vol)
                        shiftedCapFloor2 = vars.makeCapFloor(ty, leg, strike, vol + shift)
                        shiftedCapFloor1 = vars.makeCapFloor(ty, leg, strike, vol - shift)
                        value1 = shiftedCapFloor1.NPV()
                        value2 = shiftedCapFloor2.NPV()
                        numericalVega = (value2 - value1) / (2 * shift)
                        if numericalVega > 1.0e-4:
                            analyticalVega = capFloor.resultScalar("vega")
                            discrepancy = abs(numericalVega - analyticalVega)
                            discrepancy /= numericalVega
                            self.assertFalse(discrepancy > tolerance)

    def testATMRate(self):
        TEST_MESSAGE(
            "Testing cap/floor ATM rate...")

        vars = CommonVars()

        lengths = [1, 2, 3, 5, 7, 10, 15, 20]
        strikes = [0., 0.03, 0.04, 0.05, 0.06, 0.07]
        vols = [0.01, 0.05, 0.10, 0.15, 0.20]

        startDate = vars.termStructure.referenceDate()

        for length in lengths:
            leg = vars.makeLeg(startDate, length)
            maturity = vars.calendar.advance(
                startDate, length, Years, vars.convention)
            schedule = Schedule(
                startDate, maturity,
                Period(vars.frequency), vars.calendar,
                vars.convention, vars.convention,
                DateGeneration.Forward, false)

            for strike in strikes:
                for vol in vols:
                    cap = vars.makeCapFloor(CapFloor.Cap, leg, strike, vol)
                    floor = vars.makeCapFloor(CapFloor.Floor, leg, strike, vol)
                    capATMRate = cap.atmRate(vars.termStructure.currentLink())
                    floorATMRate = floor.atmRate(vars.termStructure.currentLink())
                    self.assertFalse(
                        not checkAbsError(floorATMRate, capATMRate, 1.0e-10))
                    swap = VanillaSwap(
                        Swap.Payer, vars.nominals[0],
                        schedule, floorATMRate,
                        vars.index.dayCounter(),
                        schedule, vars.index, 0.0,
                        vars.index.dayCounter())
                    swap.setPricingEngine(
                        DiscountingSwapEngine(vars.termStructure))
                    swapNPV = swap.NPV()
                    self.assertFalse(not checkAbsError(swapNPV, 0, 1.0e-10))

    def testImpliedVolatility(self):
        TEST_MESSAGE(
            "Testing implied term volatility for cap and floor...")

        vars = CommonVars()

        maxEvaluations = 100
        tolerance = 1.0e-8

        types = [CapFloor.Cap, CapFloor.Floor]
        strikes = [0.02, 0.03, 0.04]
        lengths = [1, 5, 10]
        rRates = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07]
        vols = [0.01, 0.05, 0.10, 0.20, 0.30, 0.70, 0.90]

        for length in lengths:
            leg = vars.makeLeg(vars.settlement, length)

            for ty in types:
                for strike in strikes:

                    capfloor = vars.makeCapFloor(ty, leg, strike, 0.0)

                    for r in rRates:
                        for v in vols:

                            vars.termStructure.linkTo(
                                flatRate(vars.settlement, r, Actual360()))
                            capfloor.setPricingEngine(vars.makeEngine(v))

                            value = capfloor.NPV()
                            implVol = 0.0
                            try:
                                implVol = capfloor.impliedVolatility(
                                    value,
                                    vars.termStructure,
                                    0.10,
                                    tolerance,
                                    maxEvaluations,
                                    10.0e-7, 4.0,
                                    ShiftedLognormal, 0.0)

                            except Exception as e:
                                capfloor.setPricingEngine(vars.makeEngine(0.0))
                                value2 = capfloor.NPV()

                                self.assertFalse(abs(value - value2) > tolerance)

                            if abs(implVol - v) > tolerance:
                                capfloor.setPricingEngine(
                                    vars.makeEngine(implVol))
                                value2 = capfloor.NPV()
                                self.assertFalse(abs(value - value2) > tolerance)

    def testCachedValue(self):
        TEST_MESSAGE(
            "Testing Black cap/floor price against cached values...")

        vars = CommonVars()

        cachedToday = Date(14, March, 2002)
        cachedSettlement = Date(18, March, 2002)
        Settings.instance().evaluationDate = cachedToday
        vars.termStructure.linkTo(flatRate(cachedSettlement, 0.05, Actual360()))
        startDate = vars.termStructure.referenceDate()
        leg = vars.makeLeg(startDate, 20)
        cap = vars.makeCapFloor(CapFloor.Cap, leg,
                                0.07, 0.20)
        floor = vars.makeCapFloor(CapFloor.Floor, leg,
                                  0.03, 0.20)

        if not IborCouponSettings.instance().usingAtParCoupons():
            cachedCapNPV = 6.87630307745
            cachedFloorNPV = 2.65796764715

        else:
            cachedCapNPV = 6.87570026732
            cachedFloorNPV = 2.65812927959

        self.assertFalse(abs(cap.NPV() - cachedCapNPV) > 1.0e-11)
        self.assertFalse(abs(floor.NPV() - cachedFloorNPV) > 1.0e-11)

    def testCachedValueFromOptionLets(self):
        TEST_MESSAGE(
            "Testing Black cap/floor price as a sum of optionlets prices against cached values...")

        vars = CommonVars()

        cachedToday = Date(14, March, 2002)
        cachedSettlement = Date(18, March, 2002)
        Settings.instance().evaluationDate = cachedToday
        baseCurve = flatRate(cachedSettlement,
                             0.05, Actual360())
        vars.termStructure.linkTo(baseCurve)
        startDate = vars.termStructure.referenceDate()
        leg = vars.makeLeg(startDate, 20)

        cap = vars.makeCapFloor(CapFloor.Cap, leg,
                                0.07, 0.20)
        floor = vars.makeCapFloor(CapFloor.Floor, leg,
                                  0.03, 0.20)
        calculatedCapletsNPV = 0.0
        calculatedFloorletsNPV = 0.0

        if IborCouponSettings.instance().usingAtParCoupons():
            cachedCapNPV = 6.87570026732
            cachedFloorNPV = 2.65812927959

        else:
            cachedCapNPV = 6.87630307745
            cachedFloorNPV = 2.65796764715

        capletPrices = DoubleVector()
        floorletPrices = DoubleVector()

        capletPrices = cap.resultVector("optionletsPrice")
        floorletPrices = floor.resultVector("optionletsPrice")

        self.assertFalse(len(capletPrices) != 40)

        for capletPrice in capletPrices:
            calculatedCapletsNPV += capletPrice

        for floorletPrice in floorletPrices:
            calculatedFloorletsNPV += floorletPrice

        self.assertFalse(abs(calculatedCapletsNPV - cachedCapNPV) > 1.0e-11)
        self.assertFalse(abs(calculatedFloorletsNPV - cachedFloorNPV) > 1.0e-11)

    def testOptionLetsDelta(self):
        TEST_MESSAGE(
            "Testing Black caplet/floorlet delta coefficients against finite difference values...")

        vars = CommonVars()

        cachedToday = Date(14, March, 2002)
        cachedSettlement = Date(18, March, 2002)
        Settings.instance().evaluationDate = cachedToday
        baseCurve = flatRate(cachedSettlement,
                             0.05, Actual360())
        baseCurveHandle = RelinkableYieldTermStructureHandle(baseCurve)

        eps = 1.0e-6
        spread = SimpleQuote(0.0)
        spreadCurve = ZeroSpreadedTermStructure(
            baseCurveHandle,
            QuoteHandle(spread),
            Continuous,
            Annual,
            Actual360())
        vars.termStructure.linkTo(spreadCurve)
        startDate = vars.termStructure.referenceDate()
        leg = vars.makeLeg(startDate, 20)

        cap = vars.makeCapFloor(CapFloor.Cap, leg,
                                0.05, 0.20)
        floor = vars.makeCapFloor(CapFloor.Floor, leg,
                                  0.05, 0.20)

        capletsNum = len(cap.capRates())
        capletUpPrices = DoubleVector()
        capletDownPrices = DoubleVector()
        capletAnalyticDelta = DoubleVector()
        capletDiscountFactorsUp = DoubleVector()
        capletDiscountFactorsDown = DoubleVector()
        capletForwardsUp = DoubleVector()
        capletForwardsDown = DoubleVector()
        capletFDDelta = DoubleVector(capletsNum, 0.0)
        floorletNum = len(floor.floorRates())
        floorletUpPrices = DoubleVector()
        floorletDownPrices = DoubleVector()
        floorletAnalyticDelta = DoubleVector()
        floorletDiscountFactorsUp = DoubleVector()
        floorletDiscountFactorsDown = DoubleVector()
        floorletForwardsUp = DoubleVector()
        floorletForwardsDown = DoubleVector()
        floorletFDDelta = DoubleVector(floorletNum, 0.0)

        capletAnalyticDelta = cap.resultVector("optionletsDelta")
        floorletAnalyticDelta = floor.resultVector("optionletsDelta")

        spread.setValue(eps)
        capletUpPrices = cap.resultVector("optionletsPrice")
        floorletUpPrices = floor.resultVector("optionletsPrice")
        capletDiscountFactorsUp = cap.resultVector("optionletsDiscountFactor")
        floorletDiscountFactorsUp = floor.resultVector("optionletsDiscountFactor")
        capletForwardsUp = cap.resultVector("optionletsAtmForward")
        floorletForwardsUp = floor.resultVector("optionletsAtmForward")

        spread.setValue(-eps)
        capletDownPrices = cap.resultVector("optionletsPrice")
        floorletDownPrices = floor.resultVector("optionletsPrice")
        capletDiscountFactorsDown = cap.resultVector("optionletsDiscountFactor")
        floorletDiscountFactorsDown = floor.resultVector("optionletsDiscountFactor")
        capletForwardsDown = cap.resultVector("optionletsAtmForward")
        floorletForwardsDown = floor.resultVector("optionletsAtmForward")

        capLeg = cap.floatingLeg()
        floorLeg = floor.floatingLeg()

        for n in range(1, len(capletUpPrices)):
            c = as_floating_rate_coupon(capLeg[n])
            accrualFactor = c.nominal() * c.accrualPeriod() * c.gearing()
            capletFDDelta[n] = (capletUpPrices[n] / capletDiscountFactorsUp[n] -
                                capletDownPrices[n] / capletDiscountFactorsDown[n]) / \
                               (capletForwardsUp[n] - capletForwardsDown[n]) / accrualFactor

        for n in range(len(floorletUpPrices)):
            c = as_floating_rate_coupon(floorLeg[n])
            accrualFactor = c.nominal() * c.accrualPeriod() * c.gearing()
            floorletFDDelta[n] = (floorletUpPrices[n] / floorletDiscountFactorsUp[n]
                                  - floorletDownPrices[n] / floorletDiscountFactorsDown[n]) / \
                                 (floorletForwardsUp[n] - floorletForwardsDown[n]) / accrualFactor

        for n in range(0, len(capletAnalyticDelta)):
            self.assertFalse(abs(capletAnalyticDelta[n] - capletFDDelta[n]) > 1.0e-6)

        for n in range(0, len(floorletAnalyticDelta)):
            self.assertFalse(abs(floorletAnalyticDelta[n] - floorletFDDelta[n]) > 1.0e-6)

    def testBachelierOptionLetsDelta(self):
        TEST_MESSAGE(
            "Testing Bachelier caplet/floorlet delta coefficients against finite difference values...")

        vars = CommonVars()

        cachedToday = Date(14, March, 2002)
        cachedSettlement = Date(18, March, 2002)
        Settings.instance().evaluationDate = cachedToday
        baseCurve = flatRate(cachedSettlement, 0.05, Actual360())
        baseCurveHandle = RelinkableYieldTermStructureHandle(baseCurve)

        eps = 1.0e-6
        spread = SimpleQuote(0.0)
        spreadCurve = ZeroSpreadedTermStructure(
            baseCurveHandle,
            QuoteHandle(spread),
            Continuous,
            Annual,
            Actual360())
        vars.termStructure.linkTo(spreadCurve)
        startDate = vars.termStructure.referenceDate()
        leg = vars.makeLeg(startDate, 20)

        isLogNormal = false

        cap = vars.makeCapFloor(
            CapFloor.Cap, leg, 0.05, 0.01, isLogNormal)
        floor = vars.makeCapFloor(
            CapFloor.Floor, leg, 0.05, 0.01, isLogNormal)

        capletsNum = len(cap.capRates())
        capletUpPrices = DoubleVector()
        capletDownPrices = DoubleVector()
        capletAnalyticDelta = DoubleVector()
        capletDiscountFactorsUp = DoubleVector()
        capletDiscountFactorsDown = DoubleVector()
        capletForwardsUp = DoubleVector()
        capletForwardsDown = DoubleVector()
        capletFDDelta = DoubleVector(capletsNum, 0.0)
        floorletNum = len(floor.floorRates())
        floorletUpPrices = DoubleVector()
        floorletDownPrices = DoubleVector()
        floorletAnalyticDelta = DoubleVector()
        floorletDiscountFactorsUp = DoubleVector()
        floorletDiscountFactorsDown = DoubleVector()
        floorletForwardsUp = DoubleVector()
        floorletForwardsDown = DoubleVector()
        floorletFDDelta = DoubleVector(floorletNum, 0.0)

        capletAnalyticDelta = cap.resultVector("optionletsDelta")
        floorletAnalyticDelta = floor.resultVector("optionletsDelta")

        spread.setValue(eps)
        capletUpPrices = cap.resultVector("optionletsPrice")
        floorletUpPrices = floor.resultVector("optionletsPrice")
        capletDiscountFactorsUp = cap.resultVector("optionletsDiscountFactor")
        floorletDiscountFactorsUp = floor.resultVector("optionletsDiscountFactor")
        capletForwardsUp = cap.resultVector("optionletsAtmForward")
        floorletForwardsUp = floor.resultVector("optionletsAtmForward")

        spread.setValue(-eps)
        capletDownPrices = cap.resultVector("optionletsPrice")
        floorletDownPrices = floor.resultVector("optionletsPrice")
        capletDiscountFactorsDown = cap.resultVector("optionletsDiscountFactor")
        floorletDiscountFactorsDown = floor.resultVector("optionletsDiscountFactor")
        capletForwardsDown = cap.resultVector("optionletsAtmForward")
        floorletForwardsDown = floor.resultVector("optionletsAtmForward")

        capLeg = cap.floatingLeg()
        floorLeg = floor.floatingLeg()

        for n in range(1, len(capletUpPrices)):
            c = as_floating_rate_coupon(capLeg[n])
            accrualFactor = c.nominal() * c.accrualPeriod() * c.gearing()
            capletFDDelta[n] = (capletUpPrices[n] / capletDiscountFactorsUp[n] -
                                capletDownPrices[n] / capletDiscountFactorsDown[n]) / \
                               (capletForwardsUp[n] - capletForwardsDown[n]) / accrualFactor

        for n in range(0, len(floorletUpPrices)):
            c = as_floating_rate_coupon(floorLeg[n])
            accrualFactor = c.nominal() * c.accrualPeriod() * c.gearing()
            floorletFDDelta[n] = (floorletUpPrices[n] / floorletDiscountFactorsUp[n] -
                                  floorletDownPrices[n] / floorletDiscountFactorsDown[n]) / \
                                 (floorletForwardsUp[n] - floorletForwardsDown[n]) / accrualFactor

        for n in range(0, len(capletAnalyticDelta)):
            self.assertFalse(abs(capletAnalyticDelta[n] - capletFDDelta[n]) > 1.0e-6)

        for n in range(0, len(floorletAnalyticDelta)):
            self.assertFalse(abs(floorletAnalyticDelta[n] - floorletFDDelta[n]) > 1.0e-6)
