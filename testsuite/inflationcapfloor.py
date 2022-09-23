import unittest

from QuantLib import *

from utilities import *


class Datum(object):
    def __init__(self, date, rate):
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
        self.nominals = DoubleVector(1, 1000000.0)

        self.frequency = Annual

        self.calendar = UnitedKingdom()
        self.convention = ModifiedFollowing
        self.today = Date(13, August, 2007)
        self.evaluationDate = self.calendar.adjust(self.today)
        Settings.instance().evaluationDate = self.evaluationDate
        self.settlementDays = 0
        self.fixingDays = 0
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)
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
            YearOnYearInflationSwapHelper,
            yyData, self.iir,
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

    def cleanUp(self):
        IndexManager.instance().clearHistories()

    def makeYoYLeg(self,
                   startDate,
                   length):
        ii = self.iir
        endDate = self.calendar.advance(
            startDate, Period(length, Years), Unadjusted)
        schedule = Schedule(
            startDate, endDate, Period(self.frequency), self.calendar,
            Unadjusted, Unadjusted,
            DateGeneration.Forward, false)
        leg = yoyInflationLeg(schedule, self.calendar, ii,
                              self.observationLag,
                              )
        leg.withNotionals(self.nominals)
        leg.withPaymentDayCounter(self.dc)
        leg.withPaymentAdjustment(self.convention)
        leg = leg.makeLeg()
        return leg

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
            return YoYInflationBlackCapFloorEngine(
                self.iir, vol, self.nominalTS)
        elif which == 1:
            return YoYInflationUnitDisplacedBlackCapFloorEngine(
                self.iir, vol, self.nominalTS)
        elif which == 2:
            return YoYInflationBachelierCapFloorEngine(
                self.iir, vol, self.nominalTS)

    def makeYoYCapFloor(self,
                        type,
                        leg,
                        strike,
                        volatility,
                        which):
        result = None
        if type == YoYInflationCapFloor.Cap:
            result = YoYInflationCap(leg, DoubleVector(1, strike))
        if type == YoYInflationCapFloor.Floor:
            result = YoYInflationFloor(leg, DoubleVector(1, strike))

        result.setPricingEngine(self.makeEngine(volatility, which))
        return result


class InflationCapFloorTest(unittest.TestCase):

    def testConsistency(self):

        TEST_MESSAGE(
            "Testing consistency between yoy inflation cap,"
            " floor and collar...")

        vars = CommonVars()

        lengths = [1, 2, 3, 5, 7, 10, 15, 20]
        cap_rates = [0.01, 0.025, 0.029, 0.03, 0.031, 0.035, 0.07]
        floor_rates = [0.01, 0.025, 0.029, 0.03, 0.031, 0.035, 0.07]
        vols = [0.001, 0.005, 0.010, 0.015, 0.020]

        for whichPricer in range(3):
            for length in lengths:
                for cap_rate in cap_rates:
                    for floor_rate in floor_rates:
                        for vol in vols:

                            leg = vars.makeYoYLeg(vars.evaluationDate, length)

                            cap = vars.makeYoYCapFloor(
                                YoYInflationCapFloor.Cap, leg, cap_rate, vol, whichPricer)

                            floor = vars.makeYoYCapFloor(
                                YoYInflationCapFloor.Floor, leg, floor_rate, vol, whichPricer)

                            collar = YoYInflationCollar(
                                leg, DoubleVector(1, cap_rate), DoubleVector(1, floor_rate))
                            collar.setPricingEngine(vars.makeEngine(vol, whichPricer))

                            self.assertFalse(abs((cap.NPV() - floor.NPV()) - collar.NPV()) > 1e-6)

                            capletsNPV = 0.0
                            caplets = []
                            for m in range(length * 1):
                                caplets.append(cap.optionlet(m))
                                caplets[m].setPricingEngine(vars.makeEngine(vol, whichPricer))
                                capletsNPV += caplets[m].NPV()

                            self.assertFalse(abs(cap.NPV() - capletsNPV) > 1e-6)

                            floorletsNPV = 0.0
                            floorlets = []
                            for m in range(length * 1):
                                floorlets.append(floor.optionlet(m))
                                floorlets[m].setPricingEngine(vars.makeEngine(vol, whichPricer))
                                floorletsNPV += floorlets[m].NPV()

                            self.assertFalse(abs(floor.NPV() - floorletsNPV) > 1e-6)

                            collarletsNPV = 0.0
                            collarlets = []
                            for m in range(length * 1):
                                collarlets.append(collar.optionlet(m))
                                collarlets[m].setPricingEngine(vars.makeEngine(vol, whichPricer))
                                collarletsNPV += collarlets[m].NPV()

                            self.assertFalse(abs(collar.NPV() - collarletsNPV) > 1e-6)

        vars.hy.reset()
        vars.cleanUp()

    def testParity(self):

        TEST_MESSAGE(
            "Testing yoy inflation cap/floor parity...")

        vars = CommonVars()

        lengths = [1, 2, 3, 5, 7, 10, 15, 20]
        strikes = [0., 0.025, 0.029, 0.03, 0.031, 0.035, 0.07]
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
                            Swap.Payer, 1000000.0,
                            yoySchedule,
                            strike, vars.dc, yoySchedule, vars.iir,
                            vars.observationLag,
                            0.0,
                            vars.dc, UnitedKingdom())

                        hTS = vars.nominalTS
                        sppe = DiscountingSwapEngine(hTS)
                        swap.setPricingEngine(sppe)

                        self.assertFalse(abs((cap.NPV() - floor.NPV()) - swap.NPV()) > 1.0e-6)

        vars.hy.reset()
        vars.cleanUp()

    def testCachedValue(self):

        TEST_MESSAGE(
            "Testing Black yoy inflation cap/floor price"
            " against cached values...")

        vars = CommonVars()
        vars.observationLag = Period()
        whichPricer = 0

        K = 0.0295
        j = 2
        leg = vars.makeYoYLeg(vars.evaluationDate, j)
        cap = vars.makeYoYCapFloor(YoYInflationCapFloor.Cap, leg, K, 0.01, whichPricer)
        floor = vars.makeYoYCapFloor(YoYInflationCapFloor.Floor, leg, K, 0.01, whichPricer)

        cachedCapNPVblack = 219.452
        cachedFloorNPVblack = 314.641

        self.assertTrue(abs(cap.NPV() - cachedCapNPVblack) < 0.02)
        self.assertTrue(abs(floor.NPV() - cachedFloorNPVblack) < 0.02)

        whichPricer = 1

        cap = vars.makeYoYCapFloor(YoYInflationCapFloor.Cap, leg, K, 0.01, whichPricer)
        floor = vars.makeYoYCapFloor(YoYInflationCapFloor.Floor, leg, K, 0.01, whichPricer)

        cachedCapNPVdd = 9114.61
        cachedFloorNPVdd = 9209.8

        self.assertTrue(abs(cap.NPV() - cachedCapNPVdd) < 0.22)
        self.assertTrue(abs(floor.NPV() - cachedFloorNPVdd) < 0.22)

        whichPricer = 2

        cap = vars.makeYoYCapFloor(YoYInflationCapFloor.Cap, leg, K, 0.01, whichPricer)

        floor = vars.makeYoYCapFloor(YoYInflationCapFloor.Floor, leg, K, 0.01, whichPricer)

        cachedCapNPVbac = 8852.4
        cachedFloorNPVbac = 8947.59

        self.assertTrue(abs(cap.NPV() - cachedCapNPVbac) < 0.22)
        self.assertTrue(abs(floor.NPV() - cachedFloorNPVbac) < 0.22)

        vars.hy.reset()
        vars.cleanUp()
