import unittest

from QuantLib import *

from utilities import *


class Datum(object):
    def __init__(self, date, rate):
        self.date = date
        self.rate = rate


def nominalTermStructure():
    evaluationDate = Date(13, August, 2007)
    return FlatForward(evaluationDate, 0.05, Actual360())


def makeHelpers(iiData,
                makeHelper):
    instruments = []
    for datum in iiData:
        maturity = datum.date
        quote = QuoteHandle(SimpleQuote(datum.rate / 100.0))
        anInstrument = makeHelper(quote, maturity)
        instruments.append(anInstrument)

    return instruments


class InflationTest(unittest.TestCase):

    def testPeriod(self):
        TEST_MESSAGE(
            "Testing inflation period...")

        days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        for year in range(1950, 2051):

            if Date.isLeap(year):
                days[2] = 29
            else:
                days[2] = 28

            for i in range(1, 12 + 1):

                d = Date(1, i, year)
                f = Monthly
                res = inflationPeriod(d, f)
                self.assertFalse(res[0] != Date(1, i, year) or res[1] != Date(days[i], i, year))

                f = Quarterly
                res = inflationPeriod(d, f)

                if i == 1 or i == 2 or i == 3:
                    self.assertFalse((res[0] != Date(1, 1, year) or res[1] != Date(31, 3, year)))

                if i == 4 or i == 5 or i == 6:
                    self.assertFalse((res[0] != Date(1, 4, year) or res[1] != Date(30, 6, year)))

                if i == 7 or i == 8 or i == 9:
                    self.assertFalse((res[0] != Date(1, 7, year) or res[1] != Date(30, 9, year)))

                if i == 10 or i == 11 or i == 12:
                    self.assertFalse((res[0] != Date(1, 10, year) or res[1] != Date(31, 12, year)))

                f = Semiannual
                res = inflationPeriod(d, f)

                if i > 0 and i < 7:
                    self.assertFalse((res[0] != Date(1, 1, year) or res[1] != Date(30, 6, year)))

                if i > 6 and i < 13:
                    self.assertFalse(
                        res[0] != Date(1, 7, year)
                        or res[1] != Date(31, 12, year))

                f = Annual
                res = inflationPeriod(d, f)

                self.assertFalse(res[0] != Date(1, 1, year) or res[1] != Date(31, 12, year))

    def testZeroIndex(self):
        TEST_MESSAGE(
            "Testing zero inflation indices...")

        backup = SavedSettings()

        euhicp = EUHICP(true)
        self.assertFalse(
            euhicp.name() != "EU HICP"
            or euhicp.frequency() != Monthly
            or euhicp.revised()
            or not euhicp.interpolated()
            or euhicp.availabilityLag() != Period(1, Months))

        ukrpi = UKRPI(false)
        self.assertFalse(
            ukrpi.name() != "UK RPI"
            or ukrpi.frequency() != Monthly
            or ukrpi.revised()
            or ukrpi.interpolated()
            or ukrpi.availabilityLag() != Period(1, Months))

        evaluationDate = Date(13, August, 2007)
        evaluationDate = UnitedKingdom().adjust(evaluationDate)
        Settings.instance().evaluationDate = evaluationDate

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
            207.3, 206.1]

        interp = false
        iir = UKRPI(interp)
        for i in range(len(fixData)):
            iir.addFixing(rpiSchedule[i], fixData[i])

        todayMinusLag = evaluationDate - iir.availabilityLag()
        lim = inflationPeriod(todayMinusLag, iir.frequency())
        todayMinusLag = lim[0]

        eps = 1.0e-8

        for i in range(len(rpiSchedule)):
            lim = inflationPeriod(rpiSchedule[i],
                                  iir.frequency())
            d = lim[0]
            while d <= lim[1]:

                if d < inflationPeriod(todayMinusLag, iir.frequency())[0]:
                    self.assertFalse(abs(iir.fixing(d) - fixData[i]) > eps)
                d += 1

        IndexManager.instance().clearHistories()

    def testZeroTermStructure(self):
        TEST_MESSAGE(
            "Testing zero inflation term structure...")

        backup = SavedSettings()

        calendar = UnitedKingdom()
        bdc = ModifiedFollowing
        evaluationDate = Date(13, August, 2007)
        evaluationDate = calendar.adjust(evaluationDate)
        Settings.instance().evaluationDate = evaluationDate

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
            207.3]

        hz = RelinkableZeroInflationTermStructureHandle()
        interp = false
        iiUKRPI = UKRPI(interp, hz)
        for i in range(len(fixData)):
            iiUKRPI.addFixing(rpiSchedule[i], fixData[i])

        ii = iiUKRPI
        nominalTS = nominalTermStructure()

        zcData = [
            Datum(Date(13, August, 2008), 2.93),
            Datum(Date(13, August, 2009), 2.95),
            Datum(Date(13, August, 2010), 2.965),
            Datum(Date(15, August, 2011), 2.98),
            Datum(Date(13, August, 2012), 3.0),
            Datum(Date(13, August, 2014), 3.06),
            Datum(Date(13, August, 2017), 3.175),
            Datum(Date(13, August, 2019), 3.243),
            Datum(Date(15, August, 2022), 3.293),
            Datum(Date(14, August, 2027), 3.338),
            Datum(Date(13, August, 2032), 3.348),
            Datum(Date(15, August, 2037), 3.348),
            Datum(Date(13, August, 2047), 3.308),
            Datum(Date(13, August, 2057), 3.228)]

        observationLag = Period(2, Months)
        dc = Thirty360(Thirty360.BondBasis)
        frequency = Monthly

        def makeHelper(quote,
                       maturity):
            return ZeroCouponInflationSwapHelper(
                quote, observationLag, maturity, calendar, bdc, dc, ii, CPI.AsIndex,
                YieldTermStructureHandle(nominalTS))

        helpers = makeHelpers(zcData, makeHelper)

        baseZeroRate = zcData[0].rate / 100.0
        pZITS = PiecewiseZeroInflation(
            evaluationDate, calendar, dc, observationLag,
            frequency, baseZeroRate, helpers)
        pZITS.recalculate()

        eps = 0.00000001
        forceLinearInterpolation = false
        for i in range(len(zcData)):
            self.assertTrue(
                abs(zcData[i].rate / 100.0 -
                    pZITS.zeroRate(
                        zcData[i].date, observationLag, forceLinearInterpolation)) < eps)
            self.assertTrue(
                abs(helpers[i].impliedQuote()
                    - zcData[i].rate / 100.0) < eps)

        hz.linkTo(pZITS)
        fromDate = hz.baseDate()
        to = hz.maxDate() - Period(1, Months)
        testIndex = MakeSchedule()
        testIndex.fromDate(fromDate)
        testIndex.to(to)
        testIndex.withTenor(Period(1, Months))
        testIndex.withCalendar(UnitedKingdom())
        testIndex.withConvention(ModifiedFollowing)
        testIndex = testIndex.makeSchedule()

        bd = hz.baseDate()
        bf = ii.fixing(bd)
        for d in testIndex:
            z = hz.zeroRate(d, Period(0, Days))
            t = hz.dayCounter().yearFraction(bd, d)
            if not ii.interpolated():
                t = hz.dayCounter().yearFraction(
                    bd, inflationPeriod(d, ii.frequency())[0])
            calc = bf * pow(1 + z, t)
            if t <= 0:
                calc = ii.fixing(d, false)
            self.assertFalse(abs(calc - ii.fixing(d, true)) / 10000.0 > eps)

        baseDate = Date(1, January, 2006)
        fixDate = Date(1, August, 2014)
        payDate = UnitedKingdom().adjust(fixDate + Period(3, Months), ModifiedFollowing)
        ind = ii

        notional = 1000000.0
        iicf = IndexedCashFlow(notional, ind, baseDate, fixDate, payDate)
        correctIndexed = ii.fixing(iicf.fixingDate()) / ii.fixing(iicf.baseDate())
        calculatedIndexed = iicf.amount() / iicf.notional()

        zii = ii
        self.assertTrue(zii, "dynamic_pointer_cast to ZeroInflationIndex fromDate UKRPI failed")
        nzcis = ZeroCouponInflationSwap(
            Swap.Payer,
            1000000.0,
            evaluationDate,
            zcData[6].date,
            calendar, bdc, dc, zcData[6].rate / 100.0,
            zii, observationLag, CPI.AsIndex)

        hTS = YieldTermStructureHandle(nominalTS)
        sppe = DiscountingSwapEngine(hTS)
        nzcis.setPricingEngine(sppe)

        self.assertTrue(abs(nzcis.NPV()) < 0.00001)

        self.checkSeasonality(hz.currentLink(), ii)

        interpYES = true
        iiUKRPIyes = UKRPI(interpYES, hz)
        for i in range(len(fixData)):
            iiUKRPIyes.addFixing(rpiSchedule[i], fixData[i])

        iiyes = iiUKRPIyes

        observationLagyes = Period(3, Months)

        def makeHelperYes(quote, maturity):
            return ZeroCouponInflationSwapHelper(
                quote, observationLagyes, maturity, calendar, bdc, dc, iiyes, CPI.AsIndex,
                YieldTermStructureHandle(nominalTS))

        helpersyes = makeHelpers(zcData, makeHelperYes)

        pZITSyes = PiecewiseZeroInflation(
            evaluationDate, calendar, dc, observationLagyes,
            frequency, baseZeroRate,
            helpersyes)
        pZITSyes.recalculate()

        forceLinearInterpolation = false
        for i in range(len(zcData)):
            self.assertTrue(
                abs(helpersyes[i].impliedQuote() - zcData[i].rate / 100.0) < eps)

        hz.linkTo(pZITSyes)

        ziiyes = iiyes
        self.assertTrue(ziiyes, "dynamic_pointer_cast to ZeroInflationIndex fromDate UKRPI-I failed")
        nzcisyes = ZeroCouponInflationSwap(
            Swap.Payer,
            1000000.0,
            evaluationDate,
            zcData[6].date,
            calendar, bdc, dc, zcData[6].rate / 100.0,
            ziiyes, observationLagyes, CPI.AsIndex)

        nzcisyes.setPricingEngine(sppe)

        self.assertTrue(abs(nzcisyes.NPV()) < 0.00001)

        self.checkSeasonality(hz.currentLink(), iiyes)

        hz.reset()
        IndexManager.instance().clearHistories()

    def testZeroIndexFutureFixing(self):
        TEST_MESSAGE(
            "Testing that zero inflation indices forecast future fixings...")

        backup = SavedSettings()

        euhicp = EUHICP(false)

        sample_date = Date(1, December, 2013)
        sample_fixing = 117.48
        euhicp.addFixing(sample_date, sample_fixing)

        evaluationDate = euhicp.fixingCalendar().adjust(sample_date + Period(2, Weeks))
        Settings.instance().evaluationDate = evaluationDate
        fixing = euhicp.fixing(sample_date)
        self.assertFalse(abs(fixing - sample_fixing) > 1e-12)

        evaluationDate = euhicp.fixingCalendar().adjust(sample_date - Period(2, Weeks))
        Settings.instance().evaluationDate = evaluationDate
        retrieved = false
        try:
            fixing = euhicp.fixing(sample_date)
            retrieved = true
        except Exception as e:
            pass

        self.assertFalse(retrieved)

        IndexManager.instance().clearHistories()

    def testInterpolatedZeroTermStructure(self):
        TEST_MESSAGE(
            "Testing interpolated zero-rate inflation curve...")

        backup = SavedSettings()

        today = Date(27, January, 2022)
        Settings.instance().evaluationDate = today

        lag = Period(3, Months)

        dates = [
            today - lag, today + Period(7, Days), today + Period(14, Days),
            today + Period(1, Months), today + Period(2, Months), today + Period(3, Months),
            today + Period(6, Months), today + Period(1, Years), today + Period(2, Years),
            today + Period(5, Years), today + Period(10, Years)]
        rates = [
            0.01, 0.01, 0.011, 0.012, 0.013, 0.015,
            0.018, 0.02, 0.025, 0.03, 0.03]

        curve = ZeroInflationCurve(
            today, TARGET(), Actual360(), lag, Monthly, dates, rates)

        nodes = curve.nodes()

        self.assertTrue(len(nodes) == len(dates))

        for i in range(len(dates)):
            self.assertTrue(dates[i] == nodes[i][0])

    def testYYIndex(self):
        TEST_MESSAGE(
            "Testing year-on-year inflation indices...")

        backup = SavedSettings()

        yyeuhicp = YYEUHICP(true)
        self.assertFalse(
            yyeuhicp.name() != "EU YY_HICP"
            or yyeuhicp.frequency() != Monthly
            or yyeuhicp.revised()
            or not yyeuhicp.interpolated()
            or yyeuhicp.ratio()
            or yyeuhicp.availabilityLag() != Period(1, Months))

        yyeuhicpr = YYEUHICPr(true)
        self.assertFalse(
            yyeuhicpr.name() != "EU YYR_HICP"
            or yyeuhicpr.frequency() != Monthly
            or yyeuhicpr.revised()
            or not yyeuhicpr.interpolated()
            or not yyeuhicpr.ratio()
            or yyeuhicpr.availabilityLag() != Period(1, Months))

        yyukrpi = YYUKRPI(false)
        self.assertFalse(
            yyukrpi.name() != "UK YY_RPI"
            or yyukrpi.frequency() != Monthly
            or yyukrpi.revised()
            or yyukrpi.interpolated()
            or yyukrpi.ratio()
            or yyukrpi.availabilityLag() != Period(1, Months))

        yyukrpir = YYUKRPIr(false)
        self.assertFalse(
            yyukrpir.name() != "UK YYR_RPI"
            or yyukrpir.frequency() != Monthly
            or yyukrpir.revised()
            or yyukrpir.interpolated()
            or not yyukrpir.ratio()
            or yyukrpir.availabilityLag() != Period(1, Months))

        evaluationDate = Date(13, August, 2007)
        evaluationDate = UnitedKingdom().adjust(evaluationDate)
        Settings.instance().evaluationDate = evaluationDate

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
            207.3]

        interp = false
        iir = YYUKRPIr(interp)
        iirYES = YYUKRPIr(true)
        for i in range(len(fixData)):
            iir.addFixing(rpiSchedule[i], fixData[i])
            iirYES.addFixing(rpiSchedule[i], fixData[i])

        todayMinusLag = evaluationDate - iir.availabilityLag()
        lim = inflationPeriod(todayMinusLag, iir.frequency())
        todayMinusLag = lim[1] + 1 - 2 * Period(iir.frequency())

        eps = 1.0e-8

        for i in range(13, len(rpiSchedule)):
            lim = inflationPeriod(rpiSchedule[i], iir.frequency())
            limBef = inflationPeriod(rpiSchedule[i - 12], iir.frequency())
            d = lim[0]
            while d <= lim[1]:

                if d < todayMinusLag:
                    expected = fixData[i] / fixData[i - 12] - 1.0
                    calculated = iir.fixing(d)
                    self.assertTrue(abs(calculated - expected) < eps)

                    dp = lim[1] + 1 - lim[0]
                    dpBef = limBef[1] + 1 - limBef[0]
                    dl = d - lim[0]

                    dlBef = NullCalendar().advance(d, -Period(1, Years), ModifiedFollowing) - limBef[0]

                    linearNow = fixData[i] + (fixData[i + 1] - fixData[i]) * dl / dp
                    linearBef = fixData[i - 12] + (fixData[i + 1 - 12] - fixData[i - 12]) * dlBef / dpBef
                    expectedYES = linearNow / linearBef - 1.0
                    calculatedYES = iirYES.fixing(d)
                    self.assertTrue(abs(expectedYES - calculatedYES) < eps)
                d += 1

        IndexManager.instance().clearHistories()

    def testYYTermStructure(self):
        TEST_MESSAGE(
            "Testing year-on-year inflation term structure...")

        backup = SavedSettings()

        calendar = UnitedKingdom()
        bdc = ModifiedFollowing
        evaluationDate = Date(13, August, 2007)
        evaluationDate = calendar.adjust(evaluationDate)
        Settings.instance().evaluationDate = evaluationDate

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
            207.3]

        hy = RelinkableYoYInflationTermStructureHandle()
        interp = false
        iir = YYUKRPIr(interp, hy)
        for i in range(len(fixData)):
            iir.addFixing(rpiSchedule[i], fixData[i])

        nominalTS = nominalTermStructure()

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

        observationLag = Period(2, Months)
        dc = Thirty360(Thirty360.BondBasis)

        def makeHelper(quote, maturity):
            return YearOnYearInflationSwapHelper(
                quote, observationLag, maturity, calendar, bdc, dc, iir,
                YieldTermStructureHandle(nominalTS))

        helpers = makeHelpers(yyData, makeHelper)

        baseYYRate = yyData[0].rate / 100.0
        pYYTS = PiecewiseYoYInflation(
            evaluationDate, calendar, dc, observationLag,
            iir.frequency(), iir.interpolated(), baseYYRate,
            helpers)
        pYYTS.recalculate()

        eps = 0.000001

        hTS = YieldTermStructureHandle(nominalTS)
        sppe = DiscountingSwapEngine(hTS)

        hy.linkTo(pYYTS)

        for j in range(1, len(yyData)):
            fromDate = nominalTS.referenceDate()
            to = yyData[j].date
            yoySchedule = MakeSchedule()
            yoySchedule.fromDate(fromDate)
            yoySchedule.to(to)
            yoySchedule.withConvention(Unadjusted)
            yoySchedule.withCalendar(calendar)
            yoySchedule.withTenor(Period(1, Years))
            yoySchedule.backwards()
            yoySchedule = yoySchedule.makeSchedule()

            yyS2 = YearOnYearInflationSwap(
                Swap.Payer,
                1000000.0,
                yoySchedule,
                yyData[j].rate / 100.0,
                dc,
                yoySchedule,
                iir,
                observationLag,
                0.0,
                dc,
                UnitedKingdom())

            yyS2.setPricingEngine(sppe)

            self.assertTrue(abs(yyS2.NPV()) < eps)

        jj = 3
        for k in range(14):
            fromDate = nominalTS.referenceDate() - Period(k, Months)
            to = yyData[jj].date - Period(k, Months)
            yoySchedule = MakeSchedule()
            yoySchedule.fromDate(fromDate)
            yoySchedule.to(to)
            yoySchedule.withConvention(Unadjusted)
            yoySchedule.withCalendar(calendar)
            yoySchedule.withTenor(Period(1, Years))
            yoySchedule.backwards()
            yoySchedule = yoySchedule.makeSchedule()

            yyS3 = YearOnYearInflationSwap(
                Swap.Payer,
                1000000.0,
                yoySchedule,
                yyData[jj].rate / 100.0,
                dc,
                yoySchedule,
                iir,
                observationLag,
                0.0,
                dc,
                UnitedKingdom())

            yyS3.setPricingEngine(sppe)

            self.assertTrue(abs(yyS3.NPV()) < 20000.0)

        hy.reset()
        IndexManager.instance().clearHistories()

    def testCpiFlatInterpolation(self):
        TEST_MESSAGE(
            "Testing CPI flat interpolation...")

        backup = SavedSettings()

        Settings.instance().evaluationDate = Date(10, February, 2022)

        testIndex = UKRPI(false)
        testIndex.addFixing(Date(1, November, 2020), 293.5)
        testIndex.addFixing(Date(1, December, 2020), 295.4)
        testIndex.addFixing(Date(1, January, 2021), 294.6)
        testIndex.addFixing(Date(1, February, 2021), 296.0)
        testIndex.addFixing(Date(1, March, 2021), 296.9)

        calculated = CPI.laggedFixing(
            testIndex, Date(10, February, 2021), Period(3, Months), CPI.Flat)
        expected = 293.5

        self.assertTrue(abs(calculated - expected) < 1e-8)

        calculated = CPI.laggedFixing(
            testIndex, Date(12, May, 2021), Period(3, Months), CPI.Flat)
        expected = 296.0

        self.assertTrue(abs(calculated - expected) < 1e-8)

        calculated = CPI.laggedFixing(
            testIndex, Date(25, June, 2021), Period(3, Months), CPI.Flat)
        expected = 296.9

        self.assertTrue(abs(calculated - expected) < 1e-8)

        IndexManager.instance().clearHistories()

    def testCpiInterpolation(self):
        TEST_MESSAGE(
            "Testing CPI linear interpolation...")

        backup = SavedSettings()

        Settings.instance().evaluationDate = Date(10, February, 2022)

        testIndex = UKRPI(false)
        testIndex.addFixing(Date(1, November, 2020), 293.5)
        testIndex.addFixing(Date(1, December, 2020), 295.4)
        testIndex.addFixing(Date(1, January, 2021), 294.6)
        testIndex.addFixing(Date(1, February, 2021), 296.0)
        testIndex.addFixing(Date(1, March, 2021), 296.9)

        calculated = CPI.laggedFixing(
            testIndex, Date(10, February, 2021), Period(3, Months), CPI.Linear)
        expected = 293.5 * (19 / 28.0) + 295.4 * (9 / 28.0)

        self.assertTrue(abs(calculated - expected) < 1e-8)

        calculated = CPI.laggedFixing(
            testIndex, Date(12, May, 2021), Period(3, Months), CPI.Linear)
        expected = 296.0 * (20 / 31.0) + 296.9 * (11 / 31.0)

        self.assertTrue(abs(calculated - expected) < 1e-8)

        self.assertRaises(
            RuntimeError, CPI.laggedFixing, testIndex, Date(25, June, 2021), Period(3, Months), CPI.Linear)

        calculated = CPI.laggedFixing(
            testIndex, Date(1, June, 2021), Period(3, Months), CPI.Linear)
        expected = 296.9

        self.assertTrue(abs(calculated - expected) < 1e-8)
        IndexManager.instance().clearHistories()

    def checkSeasonality(self,
                         hz,
                         ii):

        tolerance = 1e-12

        trueBaseDate = inflationPeriod(hz.baseDate(), ii.frequency())[1]
        seasonalityBaseDate = Date(31, January, trueBaseDate.year())

        seasonalityFactors = DoubleVector(12, 1.0)
        unitSeasonality = MultiplicativePriceSeasonality(
            seasonalityBaseDate, Monthly, seasonalityFactors)

        seasonalityFactors[0] = 1.003245
        seasonalityFactors[1] = 1.000000
        seasonalityFactors[2] = 0.999715
        seasonalityFactors[3] = 1.000495
        seasonalityFactors[4] = 1.000929
        seasonalityFactors[5] = 0.998687
        seasonalityFactors[6] = 0.995949
        seasonalityFactors[7] = 0.994682
        seasonalityFactors[8] = 0.995949
        seasonalityFactors[9] = 1.000519
        seasonalityFactors[10] = 1.003705
        seasonalityFactors[11] = 1.004186

        nonUnitSeasonality = MultiplicativePriceSeasonality(
            seasonalityBaseDate, Monthly, seasonalityFactors)

        fixingDates = DateVector(12)
        anchorDate = Date(14, January, 2013)
        for i in range(len(fixingDates)):
            fixingDates[i] = anchorDate + Period(i, Months)

        noSeasonalityFixings = DoubleVector(12, 1.0)
        for i in range(len(fixingDates)):
            noSeasonalityFixings[i] = ii.fixing(fixingDates[i], true)

        hz.setSeasonality(unitSeasonality)
        unitSeasonalityFixings = DoubleVector(12, 1.0)
        for i in range(len(fixingDates)):
            unitSeasonalityFixings[i] = ii.fixing(fixingDates[i], true)

        for i in range(len(fixingDates)):
            self.assertFalse(
                abs(noSeasonalityFixings[i] - unitSeasonalityFixings[i]) > tolerance)

        baseCpiMonth = hz.baseDate().month()
        baseCpiIndex = int(baseCpiMonth) - 1
        baseSeasonality = seasonalityFactors[baseCpiIndex]

        expectedSeasonalityFixings = DoubleVector(12, 1.0)
        for i in range(len(expectedSeasonalityFixings)):
            if not ii.interpolated():
                expectedSeasonalityFixings[i] = ii.fixing(fixingDates[i], true) * seasonalityFactors[i] / baseSeasonality
            else:
                p1 = inflationPeriod(fixingDates[i], ii.frequency())
                firstDayCurrentPeriod = p1[0]
                firstDayNextPeriod = p1[1] + Period(1, Days)
                firstMonth = firstDayCurrentPeriod.month()
                secondMonth = firstDayNextPeriod.month()
                firstMonthIndex = firstMonth - 1
                secondMonthIndex = secondMonth - 1

                observationLag = ii.zeroInflationTermStructure().observationLag()
                observationDate = fixingDates[i] + observationLag
                p2 = inflationPeriod(observationDate, ii.frequency())
                daysInPeriod = (p2[1] + Period(1, Days)) - p2[0]
                interpolationCoefficient = (observationDate - p2[0]) / daysInPeriod

                i1adj = ii.fixing(firstDayCurrentPeriod, true) * seasonalityFactors[firstMonthIndex] / baseSeasonality

                i2adj = ii.fixing(firstDayNextPeriod, true) * seasonalityFactors[secondMonthIndex] / baseSeasonality
                expectedSeasonalityFixings[i] = i1adj + (i2adj - i1adj) * interpolationCoefficient

        hz.setSeasonality(nonUnitSeasonality)
        nonUnitSeasonalityFixings = DoubleVector(12, 1.0)
        for i in range(len(fixingDates)):
            nonUnitSeasonalityFixings[i] = ii.fixing(fixingDates[i], true)

        for i in range(len(fixingDates)):
            self.assertFalse(abs(expectedSeasonalityFixings[i] - nonUnitSeasonalityFixings[i]) > tolerance)

        hz.setSeasonality()
        unsetSeasonalityFixings = DoubleVector(12, 1.0)
        for i in range(len(fixingDates)):
            unsetSeasonalityFixings[i] = ii.fixing(fixingDates[i], true)

        for i in range(len(fixingDates)):
            self.assertFalse(abs(noSeasonalityFixings[i] - unsetSeasonalityFixings[i]) > tolerance)
