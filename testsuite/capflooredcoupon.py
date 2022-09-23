import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.length = 20
        self.volatility = 0.20
        self.nominal = 100.
        self.nominals = DoubleVector(self.length, self.nominal)
        self.frequency = Annual
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.index = Euribor1Y(self.termStructure)
        self.calendar = self.index.fixingCalendar()
        self.convention = ModifiedFollowing
        self.today = self.calendar.adjust(knownGoodDefault)
        Settings.instance().evaluationDate = self.today
        self.settlementDays = 2
        self.fixingDays = 2
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)
        self.startDate = self.settlement
        self.termStructure.linkTo(
            flatRate(
                self.settlement, 0.05, ActualActual(ActualActual.ISDA)))
        self.backup = SavedSettings()

    def makeFixedLeg(self,
                     startDate,
                     length):

        endDate = self.calendar.advance(
            startDate, length, Years, self.convention)
        schedule = Schedule(
            startDate, endDate, Period(self.frequency), self.calendar,
            self.convention, self.convention,
            DateGeneration.Forward, false)
        coupons = DoubleVector(length, 0.0)
        leg = FixedRateLeg(schedule)
        leg.withNotionals(self.nominals)
        leg.withCouponRates(coupons, Thirty360(Thirty360.BondBasis))
        leg = leg.makeLeg()
        return leg

    def makeFloatingLeg(self,
                        startDate,
                        length,
                        gearing=1.0,
                        spread=0.0):

        endDate = self.calendar.advance(
            startDate, length, Years, self.convention)
        schedule = Schedule(
            startDate, endDate, Period(self.frequency), self.calendar,
            self.convention, self.convention,
            DateGeneration.Forward, false)
        gearingVector = DoubleVector(length, gearing)
        spreadVector = DoubleVector(length, spread)
        leg = IborLeg(schedule, self.index)
        leg.withNotionals(self.nominals)
        leg.withPaymentDayCounter(self.index.dayCounter())
        leg.withPaymentAdjustment(self.convention)
        leg.withFixingDays(self.fixingDays)
        leg.withGearings(gearingVector)
        leg.withSpreads(spreadVector)
        leg = leg.makeLeg()
        return leg

    def makeCapFlooredLeg(self,
                          startDate,
                          length,
                          caps,
                          floors,
                          volatility,
                          gearing=1.0,
                          spread=0.0):

        endDate = self.calendar.advance(
            startDate, length, Years, self.convention)
        schedule = Schedule(
            startDate, endDate, Period(self.frequency), self.calendar,
            self.convention, self.convention,
            DateGeneration.Forward, false)
        vol = OptionletVolatilityStructureHandle(
            ConstantOptionletVolatility(
                0, self.calendar, Following,
                volatility, Actual365Fixed()))

        pricer = BlackIborCouponPricer(vol)
        gearingVector = DoubleVector(length, gearing)
        spreadVector = DoubleVector(length, spread)

        leg = IborLeg(schedule, self.index)
        leg.withNotionals(self.nominals)
        leg.withPaymentDayCounter(self.index.dayCounter())
        leg.withPaymentAdjustment(self.convention)
        leg.withFixingDays(self.fixingDays)
        leg.withGearings(gearingVector)
        leg.withSpreads(spreadVector)
        leg.withCaps(caps)
        leg.withFloors(floors)
        leg = leg.makeLeg()

        iborLeg = leg
        setCouponPricer(iborLeg, pricer)
        return iborLeg

    def makeEngine(self, volatility):
        vol = QuoteHandle(
            SimpleQuote(volatility))
        return BlackCapFloorEngine(self.termStructure, vol)

    def makeCapFloor(self,
                     type,
                     leg,
                     capStrike,
                     floorStrike,
                     volatility):
        result = None
        if type == CapFloor.Cap:
            result = Cap(leg, DoubleVector(1, capStrike))

        if type == CapFloor.Floor:
            result = Floor(leg, DoubleVector(1, floorStrike))

        if type == CapFloor.Collar:
            result = Collar(
                leg,
                DoubleVector(1, capStrike),
                DoubleVector(1, floorStrike))

        result.setPricingEngine(self.makeEngine(volatility))
        return result


class CapFlooredCouponTest(unittest.TestCase):

    def testLargeRates(self):
        TEST_MESSAGE(
            "Testing degenerate collared coupon...")

        vars = CommonVars()

        caps = DoubleVector(vars.length, 100.0)
        floors = DoubleVector(vars.length, 0.0)
        tolerance = 1e-10

        fixedLeg = vars.makeFixedLeg(vars.startDate, vars.length)
        floatLeg = vars.makeFloatingLeg(vars.startDate, vars.length)
        collaredLeg = vars.makeCapFlooredLeg(
            vars.startDate, vars.length,
            caps, floors, vars.volatility)

        engine = DiscountingSwapEngine(vars.termStructure)
        vanillaLeg = Swap(fixedLeg, floatLeg)
        collarLeg = Swap(fixedLeg, collaredLeg)
        vanillaLeg.setPricingEngine(engine)
        collarLeg.setPricingEngine(engine)

        self.assertFalse(abs(vanillaLeg.NPV() - collarLeg.NPV()) > tolerance)

    def testDecomposition(self):
        TEST_MESSAGE(
            "Testing collared coupon against its decomposition...")

        vars = CommonVars()

        tolerance = 1e-12
        floorstrike = 0.05
        capstrike = 0.10
        caps = DoubleVector(vars.length, capstrike)
        caps0 = DoubleVector()
        floors = DoubleVector(vars.length, floorstrike)
        floors0 = DoubleVector()
        gearing_p = 0.5
        spread_p = 0.002
        gearing_n = -1.5
        spread_n = 0.12

        fixedLeg = vars.makeFixedLeg(
            vars.startDate, vars.length)

        floatLeg = vars.makeFloatingLeg(
            vars.startDate, vars.length)

        floatLeg_p = vars.makeFloatingLeg(
            vars.startDate, vars.length, gearing_p, spread_p)

        floatLeg_n = vars.makeFloatingLeg(
            vars.startDate, vars.length, gearing_n, spread_n)

        vanillaLeg = Swap(fixedLeg, floatLeg)

        vanillaLeg_p = Swap(fixedLeg, floatLeg_p)

        vanillaLeg_n = Swap(fixedLeg, floatLeg_n)

        engine = DiscountingSwapEngine(vars.termStructure)
        vanillaLeg.setPricingEngine(engine)
        vanillaLeg_p.setPricingEngine(engine)
        vanillaLeg_n.setPricingEngine(engine)

        cappedLeg = vars.makeCapFlooredLeg(
            vars.startDate, vars.length,
            caps, floors0, vars.volatility)
        capLeg = Swap(fixedLeg, cappedLeg)
        capLeg.setPricingEngine(engine)
        cap = Cap(floatLeg, DoubleVector(1, capstrike))
        cap.setPricingEngine(vars.makeEngine(vars.volatility))
        npvVanilla = vanillaLeg.NPV()
        npvCappedLeg = capLeg.NPV()
        npvCap = cap.NPV()
        error = abs(npvCappedLeg - (npvVanilla - npvCap))
        self.assertFalse(error > tolerance)

        flooredLeg = vars.makeCapFlooredLeg(
            vars.startDate, vars.length,
            caps0, floors, vars.volatility)
        floorLeg = Swap(fixedLeg, flooredLeg)
        floorLeg.setPricingEngine(engine)
        floor = Floor(floatLeg, DoubleVector(1, floorstrike))
        floor.setPricingEngine(vars.makeEngine(vars.volatility))
        npvFlooredLeg = floorLeg.NPV()
        npvFloor = floor.NPV()
        error = abs(npvFlooredLeg - (npvVanilla + npvFloor))
        self.assertFalse(error > tolerance)

        collaredLeg = vars.makeCapFlooredLeg(
            vars.startDate, vars.length,
            caps, floors, vars.volatility)
        collarLeg = Swap(fixedLeg, collaredLeg)
        collarLeg.setPricingEngine(engine)
        collar = Collar(
            floatLeg,
            DoubleVector(1, capstrike),
            DoubleVector(1, floorstrike))
        collar.setPricingEngine(vars.makeEngine(vars.volatility))
        npvCollaredLeg = collarLeg.NPV()
        npvCollar = collar.NPV()
        error = abs(npvCollaredLeg - (npvVanilla - npvCollar))
        self.assertFalse(error > tolerance)

        cappedLeg_p = vars.makeCapFlooredLeg(
            vars.startDate, vars.length, caps, floors0,
            vars.volatility, gearing_p, spread_p)
        capLeg_p = Swap(fixedLeg, cappedLeg_p)
        capLeg_p.setPricingEngine(engine)
        cap_p = Cap(floatLeg_p, DoubleVector(1, capstrike))
        cap_p.setPricingEngine(vars.makeEngine(vars.volatility))
        npvVanilla = vanillaLeg_p.NPV()
        npvCappedLeg = capLeg_p.NPV()
        npvCap = cap_p.NPV()
        error = abs(npvCappedLeg - (npvVanilla - npvCap))
        self.assertFalse(error > tolerance)

        cappedLeg_n = vars.makeCapFlooredLeg(
            vars.startDate, vars.length, caps, floors0,
            vars.volatility, gearing_n, spread_n)
        capLeg_n = Swap(fixedLeg, cappedLeg_n)
        capLeg_n.setPricingEngine(engine)
        floor_n = Floor(
            floatLeg, DoubleVector(1, (capstrike - spread_n) / gearing_n))
        floor_n.setPricingEngine(vars.makeEngine(vars.volatility))
        npvVanilla = vanillaLeg_n.NPV()
        npvCappedLeg = capLeg_n.NPV()
        npvFloor = floor_n.NPV()
        error = abs(npvCappedLeg - (npvVanilla + gearing_n * npvFloor))
        self.assertFalse(error > tolerance)

        flooredLeg_p1 = vars.makeCapFlooredLeg(
            vars.startDate, vars.length, caps0, floors,
            vars.volatility, gearing_p, spread_p)
        floorLeg_p1 = Swap(fixedLeg, flooredLeg_p1)
        floorLeg_p1.setPricingEngine(engine)
        floor_p1 = Floor(floatLeg_p, DoubleVector(1, floorstrike))
        floor_p1.setPricingEngine(vars.makeEngine(vars.volatility))
        npvVanilla = vanillaLeg_p.NPV()
        npvFlooredLeg = floorLeg_p1.NPV()
        npvFloor = floor_p1.NPV()
        error = abs(npvFlooredLeg - (npvVanilla + npvFloor))
        self.assertFalse(error > tolerance)

        flooredLeg_n = vars.makeCapFlooredLeg(
            vars.startDate, vars.length, caps0, floors,
            vars.volatility, gearing_n, spread_n)
        floorLeg_n = Swap(fixedLeg, flooredLeg_n)
        floorLeg_n.setPricingEngine(engine)
        cap_n = Cap(floatLeg, DoubleVector(1, (floorstrike - spread_n) / gearing_n))
        cap_n.setPricingEngine(vars.makeEngine(vars.volatility))
        npvVanilla = vanillaLeg_n.NPV()
        npvFlooredLeg = floorLeg_n.NPV()
        npvCap = cap_n.NPV()
        error = abs(npvFlooredLeg - (npvVanilla - gearing_n * npvCap))
        self.assertFalse(error > tolerance)

        collaredLeg_p = vars.makeCapFlooredLeg(
            vars.startDate, vars.length, caps, floors,
            vars.volatility, gearing_p, spread_p)
        collarLeg_p1 = Swap(fixedLeg, collaredLeg_p)
        collarLeg_p1.setPricingEngine(engine)
        collar_p = Collar(
            floatLeg_p,
            DoubleVector(1, capstrike),
            DoubleVector(1, floorstrike))
        collar_p.setPricingEngine(vars.makeEngine(vars.volatility))
        npvVanilla = vanillaLeg_p.NPV()
        npvCollaredLeg = collarLeg_p1.NPV()
        npvCollar = collar_p.NPV()
        error = abs(npvCollaredLeg - (npvVanilla - npvCollar))
        self.assertFalse(error > tolerance)

        collaredLeg_n = vars.makeCapFlooredLeg(
            vars.startDate, vars.length, caps, floors,
            vars.volatility, gearing_n, spread_n)
        collarLeg_n1 = Swap(fixedLeg, collaredLeg_n)
        collarLeg_n1.setPricingEngine(engine)
        collar_n = Collar(
            floatLeg,
            DoubleVector(1, (floorstrike - spread_n) / gearing_n),
            DoubleVector(1, (capstrike - spread_n) / gearing_n))
        collar_n.setPricingEngine(vars.makeEngine(vars.volatility))
        npvVanilla = vanillaLeg_n.NPV()
        npvCollaredLeg = collarLeg_n1.NPV()
        npvCollar = collar_n.NPV()
        error = abs(npvCollaredLeg - (npvVanilla - gearing_n * npvCollar))
        self.assertFalse(error > tolerance)
