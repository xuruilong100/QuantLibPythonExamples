import unittest

from QuantLib import *

from utilities import *


class Datum(object):
    def __init__(self,
                 date,
                 rate):
        self.date = date
        self.rate = rate


def makeHelpers(U,
                iiData,
                ii,
                observationLag,
                calendar,
                bdc,
                dc,
                discountCurve):
    instruments = []
    for datum in iiData:
        maturity = datum.date
        quote = QuoteHandle(SimpleQuote(datum.rate / 100.0))
        anInstrument = U(
            quote, observationLag, maturity,
            calendar, bdc, dc, ii, discountCurve)
        instruments.append(anInstrument)

    return instruments


class CommonVars(object):
    def __init__(self):
        self.nominals = DoubleVector(1, 1000000)
        self.frequency = Annual
        self.volatility = 0.01
        self.length = 7
        self.calendar = UnitedKingdom()
        self.convention = ModifiedFollowing
        self.today = Date(13, August, 2007)
        self.evaluationDate = self.calendar.adjust(self.today)
        Settings.instance().evaluationDate = self.evaluationDate
        self.settlementDays = 0
        self.fixingDays = 0
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)
        self.startDate = self.settlement
        self.dc = Thirty360(Thirty360.BondBasis)

        fromDate = Date(1, January, 2005)
        to = Date(13, August, 2007)
        rpiSchedule = MakeSchedule()
        rpiSchedule.fromDate(fromDate)
        rpiSchedule.to(to)
        rpiSchedule.withTenor(Period(1, Months))
        rpiSchedule.withCalendar(UnitedKingdom())
        rpiSchedule.withConvention(ModifiedFollowing)
        rpiSchedule = rpiSchedule.makeSchedule()
        fixData = [
            189.9, 189.9, 189.6, 190.5, 191.6, 192.0,
            192.2, 192.2, 192.6, 193.1, 193.3, 193.6,
            194.1, 193.4, 194.2, 195.0, 196.5, 197.7,
            198.5, 198.5, 199.2, 200.1, 200.4, 201.1,
            202.7, 201.6, 203.1, 204.4, 205.4, 206.2,
            207.3, -999.0, -999]

        interp = false
        self.hy = RelinkableYoYInflationTermStructureHandle()
        self.iir = YYUKRPIr(interp, self.hy)
        for i in range(len(rpiSchedule)):
            self.iir.addFixing(rpiSchedule[i], fixData[i])

        nominalFF = FlatForward(self.evaluationDate, 0.05, ActualActual(ActualActual.ISDA))
        self.nominalTS = RelinkableYieldTermStructureHandle()
        self.nominalTS.linkTo(nominalFF)

        self.observationLag = Period(2, Months)

        yyData = [
            Datum(Date(13, August, 2008), 2.95),
            Datum(Date(13, August, 2009), 2.95),
            Datum(Date(13, August, 2010), 2.93),
            Datum(Date(15, August, 2011), 2.955),
            Datum(Date(13, August, 2012), 2.945),
            Datum(Date(13, August, 2013), 2.985),
            Datum(Date(13, August, 2014), 3.01),
            Datum(Date(13, August, 2015), 3.035),
            Datum(Date(13, August, 2016), 3.055),
            Datum(Date(13, August, 2017), 3.075),
            Datum(Date(13, August, 2019), 3.105),
            Datum(Date(15, August, 2022), 3.135),
            Datum(Date(13, August, 2027), 3.155),
            Datum(Date(13, August, 2032), 3.145),
            Datum(Date(13, August, 2037), 3.145)]

        helpers = makeHelpers(
            YearOnYearInflationSwapHelper, yyData, self.iir,
            self.observationLag,
            self.calendar, self.convention, self.dc,
            self.nominalTS)

        baseYYRate = yyData[0].rate / 100.0
        pYYTS = PiecewiseYoYInflation(
            self.evaluationDate, self.calendar, self.dc, self.observationLag,
            self.iir.frequency(), self.iir.interpolated(), baseYYRate,
            helpers)
        pYYTS.recalculate()
        self.yoyTS = pYYTS

        self.hy.linkTo(pYYTS)

    def makeYoYLeg(self,
                   startDate,
                   length,
                   gearing=1.0,
                   spread=0.0):
        ii = self.iir
        endDate = self.calendar.advance(startDate, Period(length, Years), Unadjusted)
        schedule = Schedule(
            startDate, endDate, Period(self.frequency), self.calendar,
            Unadjusted, Unadjusted,
            DateGeneration.Forward, false)

        gearingVector = DoubleVector(length, gearing)
        spreadVector = DoubleVector(length, spread)

        yoyLeg = yoyInflationLeg(schedule, self.calendar, ii, self.observationLag)
        yoyLeg.withNotionals(self.nominals)
        yoyLeg.withPaymentDayCounter(self.dc)
        yoyLeg.withGearings(gearingVector)
        yoyLeg.withSpreads(spreadVector)
        yoyLeg.withPaymentAdjustment(self.convention)
        yoyLeg = yoyLeg.makeLeg()

        return yoyLeg

    def makeFixedLeg(self, startDate, length):

        endDate = self.calendar.advance(startDate, length, Years,
                                        self.convention)
        schedule = Schedule(startDate, endDate, Period(self.frequency), self.calendar,
                            self.convention, self.convention,
                            DateGeneration.Forward, false)
        coupons = DoubleVector(length, 0.0)
        leg = FixedRateLeg(schedule)
        leg.withNotionals(self.nominals)
        leg.withCouponRates(coupons, self.dc)
        leg = leg.makeLeg()
        return leg

    def makeYoYCapFlooredLeg(self,
                             which,
                             startDate,
                             length,
                             caps,
                             floors,
                             volatility,
                             gearing=1.0,
                             spread=0.0):

        vol = YoYOptionletVolatilitySurfaceHandle(
            ConstantYoYOptionletVolatility(
                volatility,
                self.settlementDays,
                self.calendar,
                self.convention,
                self.dc,
                self.observationLag,
                self.frequency,
                self.iir.interpolated()))

        pricer = None
        if which == 0:
            pricer = BlackYoYInflationCouponPricer(vol, self.nominalTS)
        elif which == 1:
            pricer = UnitDisplacedBlackYoYInflationCouponPricer(vol, self.nominalTS)
        elif which == 2:
            pricer = BachelierYoYInflationCouponPricer(vol, self.nominalTS)

        gearingVector = DoubleVector(length, gearing)
        spreadVector = DoubleVector(length, spread)

        ii = self.iir
        endDate = self.calendar.advance(startDate, Period(length, Years), Unadjusted)
        schedule = Schedule(
            startDate, endDate, Period(self.frequency), self.calendar,
            Unadjusted, Unadjusted,
            DateGeneration.Forward, false)

        yoyLeg = yoyInflationLeg(schedule, self.calendar, ii, self.observationLag)
        yoyLeg.withNotionals(self.nominals)
        yoyLeg.withPaymentDayCounter(self.dc)
        yoyLeg.withPaymentAdjustment(self.convention)
        yoyLeg.withGearings(gearingVector)
        yoyLeg.withSpreads(spreadVector)
        yoyLeg.withCaps(caps)
        yoyLeg.withFloors(floors)
        yoyLeg = yoyLeg.makeLeg()

        setCouponPricer(yoyLeg, pricer)

        return yoyLeg

    def makeEngine(self, volatility, which):

        yyii = self.iir

        vol = YoYOptionletVolatilitySurfaceHandle(
            ConstantYoYOptionletVolatility(
                volatility,
                self.settlementDays,
                self.calendar,
                self.convention,
                self.dc,
                self.observationLag,
                self.frequency,
                self.iir.interpolated()))

        if which == 0:
            return YoYInflationBlackCapFloorEngine(self.iir, vol, self.nominalTS)
        elif which == 1:
            return YoYInflationUnitDisplacedBlackCapFloorEngine(
                self.iir, vol, self.nominalTS)
        elif which == 2:
            return YoYInflationBachelierCapFloorEngine(self.iir, vol, self.nominalTS)

    def makeYoYCapFloor(self,
                        type,
                        leg,
                        strike,
                        volatility,
                        which):
        result = None
        if type == YoYInflationCapFloor.Cap:
            result = YoYInflationCap(leg, DoubleVector(1, strike))
        elif type == YoYInflationCapFloor.Floor:
            result = YoYInflationFloor(leg, DoubleVector(1, strike))

        result.setPricingEngine(self.makeEngine(volatility, which))
        return result


class InflationCapFlooredCouponTest(unittest.TestCase):

    def testDecomposition(self):

        TEST_MESSAGE(
            "Testing collared coupon against its decomposition...")

        vars = CommonVars()

        tolerance = 1e-10

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

        fixedLeg = vars.makeFixedLeg(vars.startDate, vars.length)
        floatLeg = vars.makeYoYLeg(vars.startDate, vars.length)
        floatLeg_p = vars.makeYoYLeg(vars.startDate, vars.length, gearing_p, spread_p)
        floatLeg_n = vars.makeYoYLeg(vars.startDate, vars.length, gearing_n, spread_n)

        vanillaLeg = Swap(fixedLeg, floatLeg)
        vanillaLeg_p = Swap(fixedLeg, floatLeg_p)
        vanillaLeg_n = Swap(fixedLeg, floatLeg_n)

        engine = DiscountingSwapEngine(vars.nominalTS)

        vanillaLeg.setPricingEngine(engine)
        vanillaLeg_p.setPricingEngine(engine)
        vanillaLeg_n.setPricingEngine(engine)

        whichPricer = 0

        cappedLeg = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length,
            caps, floors0, vars.volatility)
        capLeg = Swap(fixedLeg, cappedLeg)
        capLeg.setPricingEngine(engine)
        cap = YoYInflationCap(floatLeg, DoubleVector(1, capstrike))
        cap.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvVanilla = vanillaLeg.NPV()
        npvCappedLeg = capLeg.NPV()
        npvCap = cap.NPV()
        error = abs(npvCappedLeg - (npvVanilla - npvCap))
        self.assertFalse(error > tolerance)

        flooredLeg = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length,
            caps0, floors, vars.volatility)
        floorLeg = Swap(fixedLeg, flooredLeg)
        floorLeg.setPricingEngine(engine)
        floor = YoYInflationFloor(floatLeg, DoubleVector(1, floorstrike))
        floor.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvFlooredLeg = floorLeg.NPV()
        npvFloor = floor.NPV()
        error = abs(npvFlooredLeg - (npvVanilla + npvFloor))
        self.assertFalse(error > tolerance)

        collaredLeg = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length,
            caps, floors, vars.volatility)
        collarLeg = Swap(fixedLeg, collaredLeg)
        collarLeg.setPricingEngine(engine)
        collar = YoYInflationCollar(
            floatLeg,
            DoubleVector(1, capstrike),
            DoubleVector(1, floorstrike))
        collar.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvCollaredLeg = collarLeg.NPV()
        npvCollar = collar.NPV()
        error = abs(npvCollaredLeg - (npvVanilla - npvCollar))
        self.assertFalse(error > tolerance)

        cappedLeg_p = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length, caps, floors0,
            vars.volatility, gearing_p, spread_p)
        capLeg_p = Swap(fixedLeg, cappedLeg_p)
        capLeg_p.setPricingEngine(engine)
        cap_p = YoYInflationCap(floatLeg_p, DoubleVector(1, capstrike))
        cap_p.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvVanilla = vanillaLeg_p.NPV()
        npvCappedLeg = capLeg_p.NPV()
        npvCap = cap_p.NPV()
        error = abs(npvCappedLeg - (npvVanilla - npvCap))
        self.assertFalse(error > tolerance)

        cappedLeg_n = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length, caps, floors0,
            vars.volatility, gearing_n, spread_n)
        capLeg_n = Swap(fixedLeg, cappedLeg_n)
        capLeg_n.setPricingEngine(engine)
        floor_n = YoYInflationFloor(floatLeg, DoubleVector(1, (capstrike - spread_n) / gearing_n))
        floor_n.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvVanilla = vanillaLeg_n.NPV()
        npvCappedLeg = capLeg_n.NPV()
        npvFloor = floor_n.NPV()
        error = abs(npvCappedLeg - (npvVanilla + gearing_n * npvFloor))
        self.assertFalse(error > tolerance)

        flooredLeg_p1 = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length, caps0, floors,
            vars.volatility, gearing_p, spread_p)
        floorLeg_p1 = Swap(fixedLeg, flooredLeg_p1)
        floorLeg_p1.setPricingEngine(engine)
        floor_p1 = YoYInflationFloor(floatLeg_p, DoubleVector(1, floorstrike))
        floor_p1.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvVanilla = vanillaLeg_p.NPV()
        npvFlooredLeg = floorLeg_p1.NPV()
        npvFloor = floor_p1.NPV()
        error = abs(npvFlooredLeg - (npvVanilla + npvFloor))
        self.assertFalse(error > tolerance)

        flooredLeg_n = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length, caps0, floors,
            vars.volatility, gearing_n, spread_n)
        floorLeg_n = Swap(fixedLeg, flooredLeg_n)
        floorLeg_n.setPricingEngine(engine)
        cap_n = YoYInflationCap(floatLeg, DoubleVector(1, (floorstrike - spread_n) / gearing_n))
        cap_n.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvVanilla = vanillaLeg_n.NPV()
        npvFlooredLeg = floorLeg_n.NPV()
        npvCap = cap_n.NPV()
        error = abs(npvFlooredLeg - (npvVanilla - gearing_n * npvCap))
        self.assertFalse(error > tolerance)

        collaredLeg_p = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length, caps, floors,
            vars.volatility, gearing_p, spread_p)
        collarLeg_p1 = Swap(fixedLeg, collaredLeg_p)
        collarLeg_p1.setPricingEngine(engine)
        collar_p = YoYInflationCollar(
            floatLeg_p,
            DoubleVector(1, capstrike),
            DoubleVector(1, floorstrike))
        collar_p.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvVanilla = vanillaLeg_p.NPV()
        npvCollaredLeg = collarLeg_p1.NPV()
        npvCollar = collar_p.NPV()
        error = abs(npvCollaredLeg - (npvVanilla - npvCollar))
        self.assertFalse(error > tolerance)

        collaredLeg_n = vars.makeYoYCapFlooredLeg(
            whichPricer, vars.startDate, vars.length, caps, floors,
            vars.volatility, gearing_n, spread_n)
        collarLeg_n1 = Swap(fixedLeg, collaredLeg_n)
        collarLeg_n1.setPricingEngine(engine)
        collar_n = YoYInflationCollar(
            floatLeg,
            DoubleVector(1, (floorstrike - spread_n) / gearing_n),
            DoubleVector(1, (capstrike - spread_n) / gearing_n))
        collar_n.setPricingEngine(vars.makeEngine(vars.volatility, whichPricer))
        npvVanilla = vanillaLeg_n.NPV()
        npvCollaredLeg = collarLeg_n1.NPV()
        npvCollar = collar_n.NPV()
        error = abs(npvCollaredLeg - (npvVanilla - gearing_n * npvCollar))
        self.assertFalse(error > tolerance)

        vars.hy.reset()

    def testInstrumentEquality(self):

        TEST_MESSAGE(
            "Testing inflation capped/floored coupon against"
            " inflation capfloor instrument...")

        vars = CommonVars()

        lengths = [1, 2, 3, 5, 7, 10, 15, 20]
        strikes = [0.01, 0.025, 0.029, 0.03, 0.031, 0.035, 0.07]
        vols = [0.001, 0.005, 0.010, 0.015, 0.020]

        for whichPricer in range(3):
            for length in lengths:
                for strike in strikes:
                    for vol in vols:
                        leg = vars.makeYoYLeg(vars.evaluationDate, length)

                        cap = vars.makeYoYCapFloor(
                            YoYInflationCapFloor.Cap, leg, strike, vol, whichPricer)

                        floor = vars.makeYoYCapFloor(
                            YoYInflationCapFloor.Floor, leg, strike, vol, whichPricer)

                        fromDate = vars.nominalTS.referenceDate()
                        to = fromDate + Period(length, Years)
                        yoySchedule = MakeSchedule()
                        yoySchedule.fromDate(fromDate)
                        yoySchedule.to(to)
                        yoySchedule.withTenor(Period(1, Years))
                        yoySchedule.withCalendar(UnitedKingdom())
                        yoySchedule.withConvention(Unadjusted)
                        yoySchedule.backwards()
                        yoySchedule = yoySchedule.makeSchedule()

                        swap = YearOnYearInflationSwap(
                            Swap.Payer,
                            1000000.0,
                            yoySchedule,
                            0.0,
                            vars.dc,
                            yoySchedule,
                            vars.iir,
                            vars.observationLag,
                            0.0,
                            vars.dc,
                            UnitedKingdom())

                        hTS = vars.nominalTS
                        sppe = DiscountingSwapEngine(hTS)
                        swap.setPricingEngine(sppe)

                        leg2 = vars.makeYoYCapFlooredLeg(
                            whichPricer, fromDate, length,
                            DoubleVector(length, strike),
                            DoubleVector(),
                            vol,
                            1.0,
                            0.0)

                        leg3 = vars.makeYoYCapFlooredLeg(
                            whichPricer, fromDate, length,
                            DoubleVector(),
                            DoubleVector(length, strike),
                            vol,
                            1.0,
                            0.0)

                        capped = CashFlows.npv(leg2, vars.nominalTS.currentLink(), false)
                        self.assertFalse(abs(capped - (swap.NPV() - cap.NPV())) > 1.0e-6)

                        floored = CashFlows.npv(leg3, vars.nominalTS.currentLink(), false)
                        self.assertFalse(abs(floored - (swap.NPV() + floor.NPV())) > 1.0e-6)

        vars.hy.reset()
