import unittest

from QuantLib import *

from utilities import *


class Datum(object):
    def __init__(self,
                 date,
                 rate):
        self.date = date
        self.rate = rate


def makeHelpers(
        iiData,
        ii,
        observationLag,
        calendar,
        bdc,
        dc,
        yTS):
    instruments = []
    for datum in iiData:
        maturity = datum.date
        quote = QuoteHandle(SimpleQuote(datum.rate / 100.0))
        h = ZeroCouponInflationSwapHelper(
            quote, observationLag, maturity, calendar,
            bdc, dc, ii, CPI.AsIndex, yTS)
        instruments.append(h)

    return instruments


class CommonVars(object):

    def __init__(self):
        self.calendar = UnitedKingdom()
        self.convention = ModifiedFollowing
        self.today = Date(25, November, 2009)
        self.evaluationDate = self.calendar.adjust(self.today)
        Settings.instance().evaluationDate = self.evaluationDate
        self.dayCounter = ActualActual(ActualActual.ISDA)

        fromDate = Date(20, July, 2007)
        to = Date(20, November, 2009)
        rpiSchedule = MakeSchedule()
        rpiSchedule.fromDate(fromDate)
        rpiSchedule.to(to)
        rpiSchedule.withTenor(Period(1, Months))
        rpiSchedule.withCalendar(UnitedKingdom())
        rpiSchedule.withConvention(ModifiedFollowing)
        rpiSchedule = rpiSchedule.makeSchedule()

        interp = false
        self.cpiTS = RelinkableZeroInflationTermStructureHandle()
        self.ii = UKRPI(interp, self.cpiTS)

        fixData = [
            206.1, 207.3, 208.0, 208.9, 209.7, 210.9,
            209.8, 211.4, 212.1, 214.0, 215.1, 216.8,
            216.5, 217.2, 218.4, 217.7, 216,
            212.9, 210.1, 211.4, 211.3, 211.5,
            212.8, 213.4, 213.4, 213.4, 214.4]
        for i in range(len(fixData)):
            self.ii.addFixing(rpiSchedule[i], fixData[i])
        self.yTS = RelinkableYieldTermStructureHandle()
        self.yTS.linkTo(FlatForward(self.evaluationDate, 0.05, self.dayCounter))

        observationLag = Period(2, Months)

        zciisData = [
            Datum(Date(25, November, 2010), 3.0495),
            Datum(Date(25, November, 2011), 2.93),
            Datum(Date(26, November, 2012), 2.9795),
            Datum(Date(25, November, 2013), 3.029),
            Datum(Date(25, November, 2014), 3.1425),
            Datum(Date(25, November, 2015), 3.211),
            Datum(Date(25, November, 2016), 3.2675),
            Datum(Date(25, November, 2017), 3.3625),
            Datum(Date(25, November, 2018), 3.405),
            Datum(Date(25, November, 2019), 3.48),
            Datum(Date(25, November, 2021), 3.576),
            Datum(Date(25, November, 2024), 3.649),
            Datum(Date(26, November, 2029), 3.751),
            Datum(Date(27, November, 2034), 3.77225),
            Datum(Date(25, November, 2039), 3.77),
            Datum(Date(25, November, 2049), 3.734),
            Datum(Date(25, November, 2059), 3.714), ]

        helpers = makeHelpers(
            zciisData, self.ii,
            observationLag, self.calendar, self.convention,
            self.dayCounter, self.yTS)

        baseZeroRate = zciisData[0].rate / 100.0
        self.cpiTS.linkTo(PiecewiseZeroInflation(
            self.evaluationDate, self.calendar, self.dayCounter, observationLag,
            self.ii.frequency(), baseZeroRate, helpers))


class InflationCPIBondTest(unittest.TestCase):

    def testCleanPrice(self):
        TEST_MESSAGE(
            "Testing clean prices of CPI bonds...")

        IndexManager.instance().clearHistories()

        common = CommonVars()

        notional = 1000000.0
        fixedRates = DoubleVector(1, 0.1)
        fixedDayCount = Actual365Fixed()
        fixedPaymentConvention = ModifiedFollowing
        fixedPaymentCalendar = UnitedKingdom()
        fixedIndex = common.ii
        contractObservationLag = Period(3, Months)
        observationInterpolation = CPI.Flat
        settlementDays = 3
        growthOnly = true

        baseCPI = 206.1

        startDate = Date(2, October, 2007)
        endDate = Date(2, October, 2052)
        fixedSchedule = MakeSchedule()
        fixedSchedule.fromDate(startDate)
        fixedSchedule.to(endDate)
        fixedSchedule.withTenor(Period(6, Months))
        fixedSchedule.withCalendar(UnitedKingdom())
        fixedSchedule.withConvention(Unadjusted)
        fixedSchedule.backwards()
        fixedSchedule = fixedSchedule.makeSchedule()

        bond = CPIBond(
            settlementDays, notional, growthOnly,
            baseCPI, contractObservationLag, fixedIndex,
            observationInterpolation, fixedSchedule,
            fixedRates, fixedDayCount, fixedPaymentConvention)

        engine = DiscountingBondEngine(common.yTS)
        bond.setPricingEngine(engine)

        storedPrice = 383.01816406
        calculated = bond.cleanPrice()
        tolerance = 1.0e-8
        self.assertFalse(abs(calculated - storedPrice) > tolerance)
