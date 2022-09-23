import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.settlementDays = 2
        self.nominal = 1000000.0
        self.fixedConvention = Unadjusted
        self.fixedFrequency = Annual
        self.fixedDayCount = Thirty360(Thirty360.BondBasis)
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.index = Euribor6M(self.termStructure)
        self.floatingConvention = self.index.businessDayConvention()
        self.floatingTenor = self.index.tenor()
        self.calendar = self.index.fixingCalendar()
        self.today = self.calendar.adjust(knownGoodDefault)
        Settings.instance().evaluationDate = self.today
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)
        self.termStructure.linkTo(flatRate(self.settlement, 0.05, Actual365Fixed()))
        self.backup = SavedSettings()

    def makeSwaption(self,
                     swap,
                     exercise,
                     volatility,
                     settlementType=Settlement.Physical,
                     settlementMethod=Settlement.PhysicalOTC,
                     model=BlackSwaptionEngine.SwapRate):
        vol = QuoteHandle(SimpleQuote(volatility))
        engine = BlackSwaptionEngine(
            self.termStructure, vol, Actual365Fixed(), 0.0, model)

        result = Swaption(
            swap,
            EuropeanExercise(exercise),
            settlementType,
            settlementMethod)
        result.setPricingEngine(engine)
        return result

    def makeEngine(self,
                   volatility,
                   model=BlackSwaptionEngine.SwapRate):
        h = QuoteHandle(SimpleQuote(volatility))
        return BlackSwaptionEngine(
            self.termStructure, h, Actual365Fixed(), 0.0, model)


def makeConstVolEngine(Engine,
                       discountCurve,
                       volatility):
    h = QuoteHandle(SimpleQuote(volatility))
    return Engine(discountCurve, h)


exercises = [
    Period(1, Years), Period(2, Years), Period(3, Years),
    Period(5, Years), Period(7, Years), Period(10, Years)]
lengths = [
    Period(1, Years), Period(2, Years), Period(3, Years),
    Period(5, Years), Period(7, Years), Period(10, Years),
    Period(15, Years), Period(20, Years)]
type = [Swap.Receiver, Swap.Payer]


class SwaptionTest(unittest.TestCase):

    def testStrikeDependency(self):
        TEST_MESSAGE(
            "Testing swaption dependency on strike...")

        vars = CommonVars()

        strikes = [0.03, 0.04, 0.05, 0.06, 0.07]

        for exercise in exercises:
            for length in lengths:
                for k in type:
                    exerciseDate = vars.calendar.advance(vars.today, exercise)
                    startDate = vars.calendar.advance(
                        exerciseDate, vars.settlementDays, Days)
                    values = DoubleVector()
                    values_cash = DoubleVector()
                    vol = 0.20
                    for strike in strikes:
                        swap = MakeVanillaSwap(
                            length, vars.index, strike, Period(0, Days))
                        swap.withEffectiveDate(startDate)
                        swap.withFixedLegTenor(Period(1, Years))
                        swap.withFixedLegDayCount(vars.fixedDayCount)
                        swap.withFloatingLegSpread(0.0)
                        swap.withType(k)
                        swap = swap.makeVanillaSwap()
                        swaption = vars.makeSwaption(swap, exerciseDate, vol)

                        values.append(swaption.NPV())
                        swaption_cash = vars.makeSwaption(
                            swap, exerciseDate, vol,
                            Settlement.Cash, Settlement.ParYieldCurve)
                        values_cash.append(swaption_cash.NPV())

                    if k == Swap.Payer:
                        it = 1
                        while values[it - 1] >= values[it]:
                            it += 1
                            if it >= len(values) - 1:
                                break
                        self.assertFalse(it != len(values) - 1)

                        it_cash = 1
                        while values_cash[it_cash - 1] >= values_cash[it_cash]:
                            it_cash += 1
                            if it_cash >= len(values_cash) - 1:
                                break
                        self.assertFalse(it_cash != len(values_cash) - 1)

                    else:
                        it = 1
                        while values[it - 1] <= values[it]:
                            it += 1
                            if it >= len(values) - 1:
                                break

                        self.assertFalse(it != len(values) - 1)

                        it_cash = 1
                        while values_cash[it_cash - 1] <= values_cash[it_cash]:
                            it_cash += 1
                            if it_cash >= len(values_cash) - 1:
                                break
                        self.assertFalse(it_cash != len(values_cash) - 1)

    def testSpreadDependency(self):
        TEST_MESSAGE(
            "Testing swaption dependency on spread...")

        vars = CommonVars()

        spreads = [-0.002, -0.001, 0.0, 0.001, 0.002]

        for exercise in exercises:
            for length in lengths:
                for k in type:
                    exerciseDate = vars.calendar.advance(vars.today, exercise)
                    startDate = vars.calendar.advance(
                        exerciseDate, vars.settlementDays, Days)

                    values = DoubleVector()
                    values_cash = DoubleVector()
                    for spread in spreads:
                        swap = MakeVanillaSwap(
                            length, vars.index, 0.06, Period(0, Days))
                        swap.withFixedLegTenor(Period(1, Years))
                        swap.withFixedLegDayCount(vars.fixedDayCount)
                        swap.withEffectiveDate(startDate)
                        swap.withFloatingLegSpread(spread)
                        swap.withType(k)
                        swap = swap.makeVanillaSwap()
                        swaption = vars.makeSwaption(swap, exerciseDate, 0.20)

                        values.append(swaption.NPV())
                        swaption_cash = vars.makeSwaption(
                            swap, exerciseDate, 0.20,
                            Settlement.Cash, Settlement.ParYieldCurve)
                        values_cash.append(swaption_cash.NPV())

                    if k == Swap.Payer:
                        it = 1
                        while values[it - 1] <= values[it]:
                            it += 1
                            if it >= len(values) - 1:
                                break
                        self.assertFalse(it != len(values) - 1)

                        it_cash = 1
                        while values_cash[it_cash - 1] <= values_cash[it_cash]:
                            it_cash += 1
                            if it_cash >= len(values_cash) - 1:
                                break
                        self.assertFalse(it_cash != len(values_cash) - 1)

                    else:
                        it = 1
                        while values[it - 1] >= values[it]:
                            it += 1
                            if it >= len(values) - 1:
                                break
                        self.assertFalse(it != len(values) - 1)

                        it_cash = 1
                        while values_cash[it_cash - 1] >= values_cash[it_cash]:
                            it_cash += 1
                            if it_cash >= len(values_cash) - 1:
                                break
                        self.assertFalse(it_cash != len(values_cash) - 1)

    def testSpreadTreatment(self):
        TEST_MESSAGE(
            "Testing swaption treatment of spread...")

        vars = CommonVars()

        spreads = [-0.002, -0.001, 0.0, 0.001, 0.002]

        for exercise in exercises:
            for length in lengths:
                for k in type:
                    exerciseDate = vars.calendar.advance(vars.today, exercise)
                    startDate = vars.calendar.advance(
                        exerciseDate, vars.settlementDays, Days)
                    for spread in spreads:
                        swap = MakeVanillaSwap(
                            length, vars.index, 0.06, Period(0, Days))
                        swap.withFixedLegTenor(Period(1, Years))
                        swap.withFixedLegDayCount(vars.fixedDayCount)
                        swap.withEffectiveDate(startDate)
                        swap.withFloatingLegSpread(spread)
                        swap.withType(k)
                        swap = swap.makeVanillaSwap()

                        correction = spread * swap.floatingLegBPS() / swap.fixedLegBPS()
                        equivalentSwap = MakeVanillaSwap(
                            length, vars.index, 0.06 + correction, Period(0, Days))
                        equivalentSwap.withFixedLegTenor(Period(1, Years))
                        equivalentSwap.withFixedLegDayCount(vars.fixedDayCount)
                        equivalentSwap.withEffectiveDate(startDate)
                        equivalentSwap.withFloatingLegSpread(0.0)
                        equivalentSwap.withType(k)
                        equivalentSwap = equivalentSwap.makeVanillaSwap()
                        swaption1 = vars.makeSwaption(swap, exerciseDate, 0.20)
                        swaption2 = vars.makeSwaption(equivalentSwap, exerciseDate, 0.20)
                        swaption1_cash = vars.makeSwaption(
                            swap, exerciseDate, 0.20,
                            Settlement.Cash, Settlement.ParYieldCurve)
                        swaption2_cash = vars.makeSwaption(
                            equivalentSwap, exerciseDate, 0.20,
                            Settlement.Cash, Settlement.ParYieldCurve)
                        self.assertFalse(
                            abs(swaption1.NPV() - swaption2.NPV()) > 1.0e-6)
                        self.assertFalse(
                            abs(swaption1_cash.NPV() - swaption2_cash.NPV()) > 1.0e-6)

    def testCachedValue(self):
        TEST_MESSAGE(
            "Testing swaption value against cached value...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        vars.today = Date(13, March, 2002)
        vars.settlement = Date(15, March, 2002)
        Settings.instance().evaluationDate = vars.today
        vars.termStructure.linkTo(flatRate(vars.settlement, 0.05, Actual365Fixed()))
        exerciseDate = vars.calendar.advance(vars.settlement, Period(5, Years))
        startDate = vars.calendar.advance(exerciseDate, vars.settlementDays, Days)
        swap = MakeVanillaSwap(Period(10, Years), vars.index, 0.06, Period(0, Days))
        swap.withEffectiveDate(startDate)
        swap.withFixedLegTenor(Period(1, Years))
        swap.withFixedLegDayCount(vars.fixedDayCount)
        swap = swap.makeVanillaSwap()

        swaption = vars.makeSwaption(swap, exerciseDate, 0.20)

        cachedNPV = 0.036418158579 if usingAtParCoupons else 0.036421429684

        self.assertFalse(abs(swaption.NPV() - cachedNPV) > 1.0e-12)

    def testCashSettledSwaptions(self):
        TEST_MESSAGE(
            "Testing cash settled swaptions modified annuity...")

        vars = CommonVars()

        strike = 0.05

        for exercise in exercises:
            for length in lengths:

                exerciseDate = vars.calendar.advance(vars.today, exercise)
                startDate = vars.calendar.advance(exerciseDate, vars.settlementDays, Days)
                maturity = vars.calendar.advance(startDate, length, vars.floatingConvention)
                floatSchedule = Schedule(
                    startDate, maturity, vars.floatingTenor,
                    vars.calendar, vars.floatingConvention,
                    vars.floatingConvention,
                    DateGeneration.Forward, false)
                fixedSchedule_u = Schedule(
                    startDate, maturity,
                    Period(vars.fixedFrequency),
                    vars.calendar, Unadjusted, Unadjusted,
                    DateGeneration.Forward, true)
                swap_u360 = VanillaSwap(
                    type[0], vars.nominal,
                    fixedSchedule_u, strike, Thirty360(Thirty360.BondBasis),
                    floatSchedule, vars.index, 0.0,
                    vars.index.dayCounter())

                swap_u365 = VanillaSwap(
                    type[0], vars.nominal,
                    fixedSchedule_u, strike, Actual365Fixed(),
                    floatSchedule, vars.index, 0.0,
                    vars.index.dayCounter())

                fixedSchedule_a = Schedule(
                    startDate, maturity,
                    Period(vars.fixedFrequency),
                    vars.calendar, ModifiedFollowing,
                    ModifiedFollowing,
                    DateGeneration.Forward, true)
                swap_a360 = VanillaSwap(
                    type[0], vars.nominal,
                    fixedSchedule_a, strike, Thirty360(Thirty360.BondBasis),
                    floatSchedule, vars.index, 0.0,
                    vars.index.dayCounter())

                swap_a365 = VanillaSwap(
                    type[0], vars.nominal,
                    fixedSchedule_a, strike, Actual365Fixed(),
                    floatSchedule, vars.index, 0.0,
                    vars.index.dayCounter())

                swapEngine = DiscountingSwapEngine(vars.termStructure)

                swap_u360.setPricingEngine(swapEngine)
                swap_a360.setPricingEngine(swapEngine)
                swap_u365.setPricingEngine(swapEngine)
                swap_a365.setPricingEngine(swapEngine)

                swapFixedLeg_u360 = swap_u360.fixedLeg()
                swapFixedLeg_a360 = swap_a360.fixedLeg()
                swapFixedLeg_u365 = swap_u365.fixedLeg()
                swapFixedLeg_a365 = swap_a365.fixedLeg()

                termStructure_u360 = YieldTermStructureHandle(
                    FlatForward(
                        vars.settlement, swap_u360.fairRate(),
                        Thirty360(Thirty360.BondBasis), Compounded,
                        vars.fixedFrequency))
                termStructure_a360 = YieldTermStructureHandle(
                    FlatForward(
                        vars.settlement, swap_a360.fairRate(),
                        Thirty360(Thirty360.BondBasis), Compounded,
                        vars.fixedFrequency))
                termStructure_u365 = YieldTermStructureHandle(
                    FlatForward(
                        vars.settlement, swap_u365.fairRate(),
                        Actual365Fixed(), Compounded,
                        vars.fixedFrequency))
                termStructure_a365 = YieldTermStructureHandle(
                    FlatForward(
                        vars.settlement, swap_a365.fairRate(),
                        Actual365Fixed(), Compounded,
                        vars.fixedFrequency))

                annuity_u360 = swap_u360.fixedLegBPS() / 0.0001
                annuity_u360 = -annuity_u360 if swap_u360.type() == Swap.Payer else annuity_u360
                annuity_a365 = swap_a365.fixedLegBPS() / 0.0001
                annuity_a365 = -annuity_a365 if swap_a365.type() == Swap.Payer else annuity_a365
                annuity_a360 = swap_a360.fixedLegBPS() / 0.0001
                annuity_a360 = -annuity_a360 if swap_a360.type() == Swap.Payer else annuity_a360
                annuity_u365 = swap_u365.fixedLegBPS() / 0.0001
                annuity_u365 = -annuity_u365 if swap_u365.type() == Swap.Payer else annuity_u365

                cashannuity_u360 = 0.0

                for s in swapFixedLeg_u360:
                    cashannuity_u360 += s.amount() / strike * termStructure_u360.discount(s.date())

                cashannuity_u365 = 0.
                for s in swapFixedLeg_u365:
                    cashannuity_u365 += s.amount() / strike * termStructure_u365.discount(s.date())

                cashannuity_a360 = 0.
                for s in swapFixedLeg_a360:
                    cashannuity_a360 += s.amount() / strike * termStructure_a360.discount(s.date())

                cashannuity_a365 = 0.
                for s in swapFixedLeg_a365:
                    cashannuity_a365 += s.amount() / strike * termStructure_a365.discount(s.date())

                swaption_p_u360 = vars.makeSwaption(
                    swap_u360, exerciseDate, 0.20)
                value_p_u360 = swaption_p_u360.NPV()

                swaption_c_u360 = vars.makeSwaption(
                    swap_u360, exerciseDate, 0.20,
                    Settlement.Cash, Settlement.ParYieldCurve)
                value_c_u360 = swaption_c_u360.NPV()

                npv_ratio_u360 = value_c_u360 / value_p_u360
                annuity_ratio_u360 = cashannuity_u360 / annuity_u360

                swaption_p_a365 = vars.makeSwaption(
                    swap_a365, exerciseDate, 0.20)
                value_p_a365 = swaption_p_a365.NPV()

                swaption_c_a365 = vars.makeSwaption(
                    swap_a365, exerciseDate, 0.20,
                    Settlement.Cash, Settlement.ParYieldCurve)
                value_c_a365 = swaption_c_a365.NPV()

                npv_ratio_a365 = value_c_a365 / value_p_a365
                annuity_ratio_a365 = cashannuity_a365 / annuity_a365

                swaption_p_a360 = vars.makeSwaption(
                    swap_a360, exerciseDate, 0.20)
                value_p_a360 = swaption_p_a360.NPV()

                swaption_c_a360 = vars.makeSwaption(
                    swap_a360, exerciseDate, 0.20,
                    Settlement.Cash, Settlement.ParYieldCurve)
                value_c_a360 = swaption_c_a360.NPV()

                npv_ratio_a360 = value_c_a360 / value_p_a360
                annuity_ratio_a360 = cashannuity_a360 / annuity_a360

                swaption_p_u365 = vars.makeSwaption(
                    swap_u365, exerciseDate, 0.20)
                value_p_u365 = swaption_p_u365.NPV()
                swaption_c_u365 = vars.makeSwaption(
                    swap_u365, exerciseDate, 0.20,
                    Settlement.Cash, Settlement.ParYieldCurve)
                value_c_u365 = swaption_c_u365.NPV()
                npv_ratio_u365 = value_c_u365 / value_p_u365
                annuity_ratio_u365 = cashannuity_u365 / annuity_u365

                self.assertFalse(abs(annuity_ratio_u360 - npv_ratio_u360) > 1e-10)
                self.assertFalse(abs(annuity_ratio_a365 - npv_ratio_a365) > 1e-10)
                self.assertFalse(abs(annuity_ratio_a360 - npv_ratio_a360) > 1e-10)
                self.assertFalse(abs(annuity_ratio_u365 - npv_ratio_u365) > 1e-10)

    def testImpliedVolatility(self):
        TEST_MESSAGE(
            "Testing implied volatility for swaptions...")

        vars = CommonVars()

        maxEvaluations = 100
        tolerance = 1.0e-08

        types = [Settlement.Physical, Settlement.Cash]
        methods = [Settlement.PhysicalOTC, Settlement.ParYieldCurve]
        strikes = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07]
        vols = [0.01, 0.05, 0.10, 0.20, 0.30, 0.70, 0.90]

        for exercise in exercises:
            for length in lengths:
                exerciseDate = vars.calendar.advance(vars.today, exercise)
                startDate = vars.calendar.advance(
                    exerciseDate, vars.settlementDays, Days)

                for strike in strikes:
                    for k in type:
                        swap = MakeVanillaSwap(
                            length, vars.index, strike, Period(0, Days))
                        swap.withEffectiveDate(startDate)
                        swap.withFixedLegTenor(Period(1, Years))
                        swap.withFixedLegDayCount(vars.fixedDayCount)
                        swap.withFloatingLegSpread(0.0)
                        swap.withType(k)
                        swap = swap.makeVanillaSwap()
                        for h in range(len(types)):
                            for vol in vols:
                                swaption = vars.makeSwaption(
                                    swap, exerciseDate, vol, types[h], methods[h],
                                    BlackSwaptionEngine.DiscountCurve)

                                value = swaption.NPV()
                                implVol = 0.0
                                try:
                                    implVol = swaption.impliedVolatility(
                                        value, vars.termStructure,
                                        0.10, tolerance,
                                        maxEvaluations,
                                        1.0e-7, 4.0,
                                        ShiftedLognormal, 0.0)

                                except Exception as e:
                                    swaption.setPricingEngine(
                                        vars.makeEngine(
                                            0.0, BlackSwaptionEngine.DiscountCurve))
                                    value2 = swaption.NPV()
                                    if abs(value - value2) < tolerance:
                                        continue

                                    self.assertFalse(abs(value - value2) < tolerance)

                                if abs(implVol - vol) > tolerance:
                                    swaption.setPricingEngine(
                                        vars.makeEngine(
                                            implVol, BlackSwaptionEngine.DiscountCurve))
                                    value2 = swaption.NPV()
                                    self.assertFalse(abs(value - value2) > tolerance)

    def testVega(self):
        TEST_MESSAGE(
            "Testing swaption vega...")

        vars = CommonVars()

        types = [Settlement.Physical, Settlement.Cash]
        methods = [Settlement.PhysicalOTC, Settlement.ParYieldCurve]
        strikes = [0.03, 0.04, 0.05, 0.06, 0.07]
        vols = [0.01, 0.20, 0.30, 0.70, 0.90]
        shift = 1e-8
        for exercise in exercises:
            exerciseDate = vars.calendar.advance(vars.today, exercise)
            startDate = vars.calendar.advance(
                exerciseDate,
                Period(vars.settlementDays, Days))
            for length in lengths:
                for strike in strikes:
                    for h in range(len(type)):
                        swap = MakeVanillaSwap(
                            length, vars.index, strike, Period(0, Days))
                        swap.withEffectiveDate(startDate)
                        swap.withFixedLegTenor(Period(1, Years))
                        swap.withFixedLegDayCount(vars.fixedDayCount)
                        swap.withFloatingLegSpread(0.0)
                        swap.withType(type[h])
                        swap = swap.makeVanillaSwap()
                        for vol in vols:
                            swaption = vars.makeSwaption(
                                swap, exerciseDate, vol, types[h], methods[h])

                            swaption1 = vars.makeSwaption(
                                swap, exerciseDate, vol - shift, types[h], methods[h])
                            swaption2 = vars.makeSwaption(
                                swap, exerciseDate, vol + shift, types[h], methods[h])

                            swaptionNPV = swaption.NPV()
                            numericalVegaPerPoint = (swaption2.NPV() - swaption1.NPV()) / (200.0 * shift)

                            if swaptionNPV > 0.0:
                                if numericalVegaPerPoint / swaptionNPV > 1.0e-7:
                                    analyticalVegaPerPoint = swaption.resultScalar("vega") / 100.0
                                    discrepancy = abs(analyticalVegaPerPoint - numericalVegaPerPoint)
                                    discrepancy /= numericalVegaPerPoint
                                    tolerance = 0.015
                                    self.assertFalse(discrepancy > tolerance)

    def testSwaptionDeltaInBlackModel(self):
        TEST_MESSAGE(
            "Testing swaption delta in Black model...")

        self.checkSwaptionDelta(BlackSwaptionEngine, false)

    def testSwaptionDeltaInBachelierModel(self):
        TEST_MESSAGE(
            "Testing swaption delta in Bachelier model...")

        self.checkSwaptionDelta(BachelierSwaptionEngine, true)

    def checkSwaptionDelta(self, Engine, useBachelierVol):

        vars = CommonVars()
        today = vars.today
        calendar = vars.calendar

        bump = 1.e-4
        epsilon = 1.e-10

        projectionCurveHandle = RelinkableYieldTermStructureHandle()

        projectionRate = 0.01
        projectionQuoteHandle = RelinkableQuoteHandle()

        projectionCurve = FlatForward(
            today, projectionQuoteHandle, Actual365Fixed())
        projectionCurveHandle.linkTo(projectionCurve)

        discountHandle = YieldTermStructureHandle(
            FlatForward(
                today,
                QuoteHandle(SimpleQuote(0.0085)),
                Actual365Fixed()))
        swapEngine = DiscountingSwapEngine(discountHandle)

        idx = Euribor6M(projectionCurveHandle)

        types = [Settlement.Physical, Settlement.Cash]
        methods = [
            Settlement.PhysicalOTC, Settlement.CollateralizedCashPrice]

        strikes = [0.03, 0.04, 0.05, 0.06, 0.07]
        vols = [0.0, 0.10, 0.20, 0.30, 0.70, 0.90]

        for vol in vols:
            for exercise in exercises:
                for length in lengths:
                    for strike in strikes:
                        for h in range(len(type)):
                            volatility = vol / 100.0 if useBachelierVol else vol
                            swaptionEngine = makeConstVolEngine(
                                Engine, discountHandle, volatility)

                            exerciseDate = calendar.advance(today, exercise)
                            startDate = calendar.advance(exerciseDate, Period(2, Days))
                            projectionQuoteHandle.linkTo(SimpleQuote(projectionRate))

                            underlying = MakeVanillaSwap(length, idx, strike, Period(0, Days))
                            underlying.withEffectiveDate(startDate)
                            underlying.withFixedLegTenor(Period(1, Years))
                            underlying.withFixedLegDayCount(Thirty360(Thirty360.BondBasis))
                            underlying.withFloatingLegSpread(0.0)
                            underlying.withType(type[h])
                            underlying = underlying.makeVanillaSwap()
                            underlying.setPricingEngine(swapEngine)

                            fairRate = underlying.fairRate()

                            swaption = Swaption(
                                underlying, EuropeanExercise(exerciseDate),
                                types[h], methods[h])
                            swaption.setPricingEngine(swaptionEngine)

                            value = swaption.NPV()
                            delta = swaption.resultScalar("delta") * bump

                            projectionQuoteHandle.linkTo(
                                SimpleQuote(projectionRate + bump))

                            bumpedFairRate = underlying.fairRate()
                            bumpedValue = swaption.NPV()
                            bumpedDelta = swaption.resultScalar("delta") * bump

                            deltaBump = bumpedFairRate - fairRate
                            approxDelta = (bumpedValue - value) / deltaBump * bump

                            lowerBound = min(delta, bumpedDelta) - epsilon
                            upperBound = max(delta, bumpedDelta) + epsilon

                            checkIsCorrect = (lowerBound < approxDelta) and (approxDelta < upperBound)

                            self.assertFalse(not checkIsCorrect)
