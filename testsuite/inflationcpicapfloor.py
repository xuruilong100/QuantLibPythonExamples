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
                N,
                ii,
                observationLag,
                calendar,
                bdc,
                dc,
                discountCurve):
    instruments = []
    for i in range(N):
        maturity = iiData[i].date
        quote = QuoteHandle(SimpleQuote(iiData[i].rate / 100.0))
        anInstrument = U(
            quote, observationLag, maturity,
            calendar, bdc, dc, ii,
            CPI.AsIndex, discountCurve)
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
        self.today = Date(1, June, 2010)
        self.evaluationDate = self.calendar.adjust(self.today)
        Settings.instance().evaluationDate = self.evaluationDate
        self.settlementDays = 0
        self.fixingDays = 0
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)
        self.startDate = self.settlement
        self.dcZCIIS = ActualActual(ActualActual.ISDA)
        self.dcNominal = ActualActual(ActualActual.ISDA)

        fromDate = Date(1, July, 2007)
        to = Date(1, June, 2010)
        rpiSchedule = MakeSchedule()
        rpiSchedule.fromDate(fromDate)
        rpiSchedule.to(to)
        rpiSchedule.withTenor(Period(1, Months))
        rpiSchedule.withCalendar(UnitedKingdom())
        rpiSchedule.withConvention(ModifiedFollowing)
        rpiSchedule = rpiSchedule.makeSchedule()
        fixData = [
            206.1, 207.3, 208.0, 208.9, 209.7, 210.9,
            209.8, 211.4, 212.1, 214.0, 215.1, 216.8,
            216.5, 217.2, 218.4, 217.7, 216.0, 212.9,
            210.1, 211.4, 211.3, 211.5, 212.8, 213.4,
            213.4, 214.4, 215.3, 216.0, 216.6, 218.0,
            217.9, 219.2, 220.7, 222.8, -999, -999,
            -999]

        interp = false

        self.hcpi = RelinkableZeroInflationTermStructureHandle()
        ii = UKRPI(interp, self.hcpi)
        for i in range(len(rpiSchedule)):
            ii.addFixing(rpiSchedule[i], fixData[i], true)

        nominalData = [
            Datum(Date(2, June, 2010), 0.499997),
            Datum(Date(3, June, 2010), 0.524992),
            Datum(Date(8, June, 2010), 0.524974),
            Datum(Date(15, June, 2010), 0.549942),
            Datum(Date(22, June, 2010), 0.549913),
            Datum(Date(1, July, 2010), 0.574864),
            Datum(Date(2, August, 2010), 0.624668),
            Datum(Date(1, September, 2010), 0.724338),
            Datum(Date(16, September, 2010), 0.769461),
            Datum(Date(1, December, 2010), 0.997501),
            Datum(Date(17, March, 2011), 0.916996),
            Datum(Date(16, June, 2011), 0.984339),
            Datum(Date(22, September, 2011), 1.06085),
            Datum(Date(22, December, 2011), 1.141788),
            Datum(Date(1, June, 2012), 1.504426),
            Datum(Date(3, June, 2013), 1.92064),
            Datum(Date(2, June, 2014), 2.290824),
            Datum(Date(1, June, 2015), 2.614394),
            Datum(Date(1, June, 2016), 2.887445),
            Datum(Date(1, June, 2017), 3.122128),
            Datum(Date(1, June, 2018), 3.322511),
            Datum(Date(3, June, 2019), 3.483997),
            Datum(Date(1, June, 2020), 3.616896),
            Datum(Date(1, June, 2022), 3.8281),
            Datum(Date(2, June, 2025), 4.0341),
            Datum(Date(3, June, 2030), 4.070854),
            Datum(Date(1, June, 2035), 4.023202),
            Datum(Date(1, June, 2040), 3.954748),
            Datum(Date(1, June, 2050), 3.870953),
            Datum(Date(1, June, 2060), 3.85298),
            Datum(Date(2, June, 2070), 3.757542),
            Datum(Date(3, June, 2080), 3.651379)]

        nomD = []
        nomR = []
        for i in nominalData:
            nomD.append(i.date)
            nomR.append(i.rate / 100.0)

        nominalTS = ZeroCurve(nomD, nomR, self.dcNominal)
        self.nominalUK = RelinkableYieldTermStructureHandle()
        self.nominalUK.linkTo(nominalTS)

        self.observationLag = Period(2, Months)
        self.contractObservationLag = Period(3, Months)
        self.contractObservationInterpolation = CPI.Flat

        zciisData = [
            Datum(Date(1, June, 2011), 3.087),
            Datum(Date(1, June, 2012), 3.12),
            Datum(Date(1, June, 2013), 3.059),
            Datum(Date(1, June, 2014), 3.11),
            Datum(Date(1, June, 2015), 3.15),
            Datum(Date(1, June, 2016), 3.207),
            Datum(Date(1, June, 2017), 3.253),
            Datum(Date(1, June, 2018), 3.288),
            Datum(Date(1, June, 2019), 3.314),
            Datum(Date(1, June, 2020), 3.401),
            Datum(Date(1, June, 2022), 3.458),
            Datum(Date(1, June, 2025), 3.52),
            Datum(Date(1, June, 2030), 3.655),
            Datum(Date(1, June, 2035), 3.668),
            Datum(Date(1, June, 2040), 3.695),
            Datum(Date(1, June, 2050), 3.634),
            Datum(Date(1, June, 2060), 3.629), ]
        zciisDataLength = 17
        self.zciisD = []
        self.zciisR = []
        for i in range(zciisDataLength):
            self.zciisD.append(zciisData[i].date)
            self.zciisR.append(zciisData[i].rate)

        helpers = makeHelpers(
            ZeroCouponInflationSwapHelper,
            zciisData, zciisDataLength, ii,
            self.observationLag,
            self.calendar, self.convention, self.dcZCIIS,
            YieldTermStructureHandle(nominalTS))

        self.baseZeroRate = zciisData[0].rate / 100.0
        pCPIts = PiecewiseZeroInflation(
            self.evaluationDate, self.calendar, self.dcZCIIS,
            self.observationLag,
            ii.frequency(), self.baseZeroRate,
            helpers)
        pCPIts.recalculate()
        self.cpiUK = RelinkableZeroInflationTermStructureHandle()
        self.cpiUK.linkTo(pCPIts)
        self.hii = RelinkableZeroInflationIndexHandle()
        self.hii.linkTo(ii)

        self.hcpi.linkTo(pCPIts)

        cfMat = [
            Period(3, Years), Period(5, Years), Period(7, Years),
            Period(10, Years), Period(15, Years), Period(20, Years),
            Period(30, Years)]
        cStrike = [0.03, 0.04, 0.05, 0.06]
        fStrike = [-0.01, 0, 0.01, 0.02]
        ncStrikes = 4
        nfStrikes = 4
        ncfMaturities = 7

        cPrice = [
            (227.6, 100.27, 38.8, 14.94),
            (345.32, 127.9, 40.59, 14.11),
            (477.95, 170.19, 50.62, 16.88),
            (757.81, 303.95, 107.62, 43.61),
            (1140.73, 481.89, 168.4, 63.65),
            (1537.6, 607.72, 172.27, 54.87),
            (2211.67, 839.24, 184.75, 45.03)]
        fPrice = [
            (15.62, 28.38, 53.61, 104.6),
            (21.45, 36.73, 66.66, 129.6),
            (24.45, 42.08, 77.04, 152.24),
            (39.25, 63.52, 109.2, 203.44),
            (36.82, 63.62, 116.97, 232.73),
            (39.7, 67.47, 121.79, 238.56),
            (41.48, 73.9, 139.75, 286.75)]

        self.cStrikesUK = []
        self.fStrikesUK = []
        self.cfMaturitiesUK = []
        for i in range(ncStrikes):
            self.cStrikesUK.append(cStrike[i])
        for i in range(nfStrikes):
            self.fStrikesUK.append(fStrike[i])
        for i in range(ncfMaturities):
            self.cfMaturitiesUK.append(cfMat[i])
        self.cPriceUK = Matrix(ncStrikes, ncfMaturities)
        self.fPriceUK = Matrix(nfStrikes, ncfMaturities)
        for i in range(ncStrikes):
            for j in range(ncfMaturities):
                self.cPriceUK[i][j] = cPrice[j][i] / 10000.0

        for i in range(nfStrikes):
            for j in range(ncfMaturities):
                self.fPriceUK[i][j] = fPrice[j][i] / 10000.0


class InflationCPICapFloorTest(unittest.TestCase):

    def testCpicapfloorpricesurface(self):
        TEST_MESSAGE(
            "Checking CPI cap/floor against price surface...")

        common = CommonVars()

        nominal = 1.0

        cpiSurf = CPICapFloorSurface(
            nominal,
            common.baseZeroRate,
            common.observationLag,
            common.calendar,
            common.convention,
            common.dcZCIIS,
            common.hii,
            common.nominalUK,
            common.cStrikesUK,
            common.fStrikesUK,
            common.cfMaturitiesUK,
            common.cPriceUK,
            common.fPriceUK)

        for i in range(len(common.fStrikesUK)):

            qK = common.fStrikesUK[i]
            nMat = len(common.cfMaturitiesUK)
            for j in range(nMat):
                t = common.cfMaturitiesUK[j]
                a = common.fPriceUK[i][j]
                b = cpiSurf.floorPrice(t, qK)

                self.assertTrue(abs(a - b) < 1e-7)

        for i in range(len(common.cStrikesUK)):

            qK = common.cStrikesUK[i]
            nMat = len(common.cfMaturitiesUK)
            for j in range(nMat):
                t = common.cfMaturitiesUK[j]
                a = common.cPriceUK[i][j]
                b = cpiSurf.capPrice(t, qK)

                self.assertTrue(abs(a - b) < 1e-7)

        premium = cpiSurf.price(Period(3, Years), 0.01)
        expPremium = common.fPriceUK[2][0]
        self.assertFalse(abs(premium - expPremium) > 1e-12)

        common.hcpi.reset()

    def testCpicapfloorpricer(self):
        TEST_MESSAGE(
            "Checking CPI cap/floor pricer...")

        common = CommonVars()
        nominal = 1.0

        cpiCFpriceSurf = CPICapFloorSurface(
            nominal,
            common.baseZeroRate,
            common.observationLag,
            common.calendar,
            common.convention,
            common.dcZCIIS,
            common.hii,
            common.nominalUK,
            common.cStrikesUK,
            common.fStrikesUK,
            common.cfMaturitiesUK,
            common.cPriceUK,
            common.fPriceUK)

        common.cpiCFsurfUK = cpiCFpriceSurf

        startDate = Settings.instance().evaluationDate
        maturity = startDate + Period(3, Years)
        fixCalendar = UnitedKingdom()
        payCalendar = UnitedKingdom()
        fixConvention = Unadjusted
        payConvention = ModifiedFollowing
        strike = 0.03
        baseCPI = common.hii.fixing(
            fixCalendar.adjust(startDate - common.observationLag, fixConvention))
        observationInterpolation = CPI.AsIndex
        aCap = CPICapFloor(
            Option.Call,
            nominal,
            startDate,
            baseCPI,
            maturity,
            fixCalendar,
            fixConvention,
            payCalendar,
            payConvention,
            strike,
            common.hii,
            common.observationLag,
            observationInterpolation)

        cpiCFsurfUKh = CPICapFloorTermPriceSurfaceHandle(common.cpiCFsurfUK)
        engine = InterpolatingCPICapFloorEngine(cpiCFsurfUKh)

        aCap.setPricingEngine(engine)

        cached = common.cPriceUK[0][0]

        self.assertTrue(abs(cached - aCap.NPV()) < 1e-10)

        common.hcpi.reset()
