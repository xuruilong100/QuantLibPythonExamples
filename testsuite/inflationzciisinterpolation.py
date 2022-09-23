import unittest

from QuantLib import *

from utilities import *


class Result(object):
    def __init__(self,
                 index=None,
                 helpers=None,
                 curve=None,
                 swap=None):
        self.index = index
        self.helpers = helpers
        self.curve = curve
        self.swap = swap


class Setup(object):
    def __init__(self,
                 indexIsInterpolated,
                 observationInterpolation):
        self.indexIsInterpolated = indexIsInterpolated
        self.observationInterpolation = observationInterpolation
        self.calendar = UnitedKingdom()
        self.unadjustedEvaluationDate = Date(13, August, 2007)
        self.evaluationDate = self.calendar.adjust(self.unadjustedEvaluationDate)
        Settings.instance().evaluationDate = self.evaluationDate

        self.nominalTermStructure = FlatForward(
            self.evaluationDate, 0.05, Actual360())

        self.bdc = ModifiedFollowing
        self.dc = Thirty360(Thirty360.BondBasis)
        self.observationLag = Period(3, Months)

        self.swapType = ZeroCouponInflationSwap.Payer
        self.swapNomimal = 1000000.00

        self.indexFixingScheduleFrom = Date(1, January, 2005)
        self.indexFixingScheduleTo = Date(13, August, 2007)

    def str(self):
        if self.observationInterpolation == CPI.AsIndex:
            return "CPI.AsIndex"
        if self.observationInterpolation == CPI.Flat:
            return "CPI.Flat"
        if self.observationInterpolation == CPI.Linear:
            return "CPI.Linear"


fixData = [
    189.9, 189.9, 189.6, 190.5, 191.6, 192.0, 192.2, 192.2, 192.6, 193.1, 193.3,
    193.6, 194.1, 193.4, 194.2, 195.0, 196.5, 197.7, 198.5, 198.5, 199.2, 200.1,
    200.4, 201.1, 202.7, 201.6, 203.1, 204.4, 205.4, 206.2, 207.3]


def makeUKRPI(setup,
              hz):
    rpiSchedule = MakeSchedule()
    rpiSchedule.fromDate(setup.indexFixingScheduleFrom)
    rpiSchedule.to(setup.indexFixingScheduleTo)
    rpiSchedule.withTenor(Period(1, Months))
    rpiSchedule.withCalendar(setup.calendar)
    rpiSchedule.withConvention(setup.bdc)
    rpiSchedule = rpiSchedule.makeSchedule()

    ukrpi = UKRPI(setup.indexIsInterpolated, hz)
    for i in range(len(fixData)):
        ukrpi.addFixing(rpiSchedule[i], fixData[i])

    return ukrpi


class Datum(object):
    def __init__(self, date, rate):
        self.date = date
        self.rate = rate


zcData = [
    Datum(Date(13, August, 2008), 2.93), Datum(Date(13, August, 2009), 2.95),
    Datum(Date(13, August, 2010), 2.965), Datum(Date(15, August, 2011), 2.98),
    Datum(Date(13, August, 2012), 3.0), Datum(Date(13, August, 2014), 3.06),
    Datum(Date(13, August, 2017), 3.175), Datum(Date(13, August, 2019), 3.243),
    Datum(Date(15, August, 2022), 3.293), Datum(Date(14, August, 2027), 3.338),
    Datum(Date(13, August, 2032), 3.348), Datum(Date(15, August, 2037), 3.348),
    Datum(Date(13, August, 2047), 3.308), Datum(Date(13, August, 2057), 3.228)]


def makeHelpers(setup,
                index):
    def makeHelper(quote,
                   maturity):
        return ZeroCouponInflationSwapHelper(
            quote, setup.observationLag, maturity,
            setup.calendar, setup.bdc, setup.dc, index,
            setup.observationInterpolation,
            YieldTermStructureHandle(setup.nominalTermStructure))

    instruments = []
    for datum in zcData:
        maturity = datum.date
        quote = QuoteHandle(SimpleQuote(datum.rate / 100.0))
        anInstrument = makeHelper(quote, maturity)
        instruments.append(anInstrument)

    return instruments


def makeZeroInflationCurve(setup,
                           index,
                           helpers):
    frequency = Monthly

    baseZeroRate = zcData[0].rate / 100.0
    pZITS = PiecewiseZeroInflation(
        setup.evaluationDate, setup.calendar, setup.dc,
        setup.observationLag, frequency,
        baseZeroRate, helpers)
    pZITS.recalculate()

    return pZITS


def makeZeroCouponInflationSwap(setup,
                                index,
                                curve):
    maturity = zcData[6].date
    fixedRate = zcData[6].rate / 100.0

    return ZeroCouponInflationSwap(
        setup.swapType, setup.swapNomimal,
        setup.evaluationDate, maturity, setup.calendar,
        setup.bdc, setup.dc, fixedRate, index, setup.observationLag,
        setup.observationInterpolation)


def makeResult(setup):
    result = Result()

    hz = RelinkableZeroInflationTermStructureHandle()

    result.index = makeUKRPI(setup, hz)
    result.helpers = makeHelpers(setup, result.index)
    result.curve = makeZeroInflationCurve(setup, result.index, result.helpers)
    result.swap = makeZeroCouponInflationSwap(setup, result.index, result.curve)

    hz.linkTo(result.curve)

    return result


def runTest(setup):
    TEST_MESSAGE(
        "Testing ZCIIS " + setup.str() + "...")

    result = makeResult(setup)


class InflationZCIISInterpolationTest(unittest.TestCase):

    def testAsIndexNotInterpolated(self):
        backup = SavedSettings()

        indexIsInterpolated = false
        setup = Setup(indexIsInterpolated, CPI.AsIndex)

        runTest(setup)

    def testAsIndexInterpolated(self):
        backup = SavedSettings()

        indexIsInterpolated = true
        setup = Setup(indexIsInterpolated, CPI.AsIndex)

        runTest(setup)

    def testFlatNotInterpolated(self):
        backup = SavedSettings()

        indexIsInterpolated = false
        setup = Setup(indexIsInterpolated, CPI.Flat)

        runTest(setup)

    def testFlatInterpolated(self):
        backup = SavedSettings()

        indexIsInterpolated = true
        setup = Setup(indexIsInterpolated, CPI.Flat)

        runTest(setup)

    def testLinearNotInterpolated(self):
        backup = SavedSettings()

        indexIsInterpolated = false
        setup = Setup(indexIsInterpolated, CPI.Linear)

        runTest(setup)

    def testLinearInterpolated(self):
        backup = SavedSettings()

        indexIsInterpolated = true
        setup = Setup(indexIsInterpolated, CPI.Linear)

        runTest(setup)
