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
        self.today = Date(25, November, 2009)
        self.evaluationDate = self.calendar.adjust(self.today)
        Settings.instance().evaluationDate = self.evaluationDate
        self.settlementDays = 0
        self.fixingDays = 0
        self.settlement = self.calendar.advance(self.today, self.settlementDays, Days)
        self.startDate = self.settlement
        self.dcZCIIS = ActualActual(ActualActual.ISDA)
        self.dcNominal = ActualActual(ActualActual.ISDA)

        fromDate = Date(20, July, 2007)

        to = Date(20, November, 2009)
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
            216.5, 217.2, 218.4, 217.7, 216,
            212.9, 210.1, 211.4, 211.3, 211.5,
            212.8, 213.4, 213.4, 213.4, 214.4,
            -999.0, -999.0]

        interp = false

        self.hcpi = RelinkableZeroInflationTermStructureHandle()
        self.ii = UKRPI(interp, self.hcpi)
        for i in range(len(rpiSchedule)):
            self.ii.addFixing(rpiSchedule[i], fixData[i], true)

        nominalData = [
            Datum(Date(26, November, 2009), 0.475),
            Datum(Date(2, December, 2009), 0.47498),
            Datum(Date(29, December, 2009), 0.49988),
            Datum(Date(25, February, 2010), 0.59955),
            Datum(Date(18, March, 2010), 0.65361),
            Datum(Date(25, May, 2010), 0.82830),
            Datum(Date(16, September, 2010), 0.78960),
            Datum(Date(16, December, 2010), 0.93762),
            Datum(Date(17, March, 2011), 1.12037),
            Datum(Date(16, June, 2011), 1.31308),
            Datum(Date(22, September, 2011), 1.52011),
            Datum(Date(25, November, 2011), 1.78399),
            Datum(Date(26, November, 2012), 2.41170),
            Datum(Date(25, November, 2013), 2.83935),
            Datum(Date(25, November, 2014), 3.12888),
            Datum(Date(25, November, 2015), 3.34298),
            Datum(Date(25, November, 2016), 3.50632),
            Datum(Date(27, November, 2017), 3.63666),
            Datum(Date(26, November, 2018), 3.74723),
            Datum(Date(25, November, 2019), 3.83988),
            Datum(Date(25, November, 2021), 4.00508),
            Datum(Date(25, November, 2024), 4.16042),
            Datum(Date(26, November, 2029), 4.15577),
            Datum(Date(27, November, 2034), 4.04933),
            Datum(Date(25, November, 2039), 3.95217),
            Datum(Date(25, November, 2049), 3.80932),
            Datum(Date(25, November, 2059), 3.80849),
            Datum(Date(25, November, 2069), 3.72677),
            Datum(Date(27, November, 2079), 3.63082)]

        nomD = []
        nomR = []
        for i in nominalData:
            nomD.append(i.date)
            nomR.append(i.rate / 100.0)

        nominal = ZeroCurve(nomD, nomR, self.dcNominal)
        self.nominalTS = RelinkableYieldTermStructureHandle()
        self.nominalTS.linkTo(nominal)

        self.observationLag = Period(2, Months)
        self.contractObservationLag = Period(3, Months)
        self.contractObservationInterpolation = CPI.Flat

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
        zciisDataLength = 17
        self.zciisD = []
        self.zciisR = []
        for i in range(zciisDataLength):
            self.zciisD.append(zciisData[i].date)
            self.zciisR.append(zciisData[i].rate)

        helpers = makeHelpers(
            ZeroCouponInflationSwapHelper, zciisData, zciisDataLength, self.ii,
            self.observationLag,
            self.calendar, self.convention, self.dcZCIIS,
            self.nominalTS)

        baseZeroRate = zciisData[0].rate / 100.0
        pCPIts = PiecewiseZeroInflation(
            self.evaluationDate, self.calendar, self.dcZCIIS,
            self.observationLag,
            self.ii.frequency(), baseZeroRate, helpers)
        pCPIts.recalculate()
        cpiTS = pCPIts

        self.hcpi.linkTo(pCPIts)


class CPISwapTest(unittest.TestCase):

    def testConsistency(self):
        TEST_MESSAGE(
            "Checking CPI swap against inflation term structure...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        common = CommonVars()

        type = Swap.Payer
        nominal = 1000000.0
        subtractInflationNominal = true

        spread = 0.0
        floatDayCount = Actual365Fixed()
        floatPaymentConvention = ModifiedFollowing
        fixingDays = 0
        floatIndex = GBPLibor(Period(6, Months),
                              common.nominalTS)

        fixedRate = 0.1
        baseCPI = 206.1
        fixedDayCount = Actual365Fixed()
        fixedPaymentConvention = ModifiedFollowing
        fixedPaymentCalendar = UnitedKingdom()
        fixedIndex = common.ii
        contractObservationLag = common.contractObservationLag
        observationInterpolation = common.contractObservationInterpolation

        startDate = Date(2, October, 2007)
        endDate = Date(2, October, 2052)
        floatSchedule = MakeSchedule()
        floatSchedule.fromDate(startDate)
        floatSchedule.to(endDate)
        floatSchedule.withTenor(Period(6, Months))
        floatSchedule.withCalendar(UnitedKingdom())
        floatSchedule.withConvention(floatPaymentConvention)
        floatSchedule.backwards()
        floatSchedule = floatSchedule.makeSchedule()

        fixedSchedule = MakeSchedule()
        fixedSchedule.fromDate(startDate)
        fixedSchedule.to(endDate)
        fixedSchedule.withTenor(Period(6, Months))
        fixedSchedule.withCalendar(UnitedKingdom())
        fixedSchedule.withConvention(Unadjusted)
        fixedSchedule.backwards()
        fixedSchedule = fixedSchedule.makeSchedule()

        zisV = CPISwap(
            type, nominal, subtractInflationNominal,
            spread, floatDayCount, floatSchedule,
            floatPaymentConvention, fixingDays, floatIndex,
            fixedRate, baseCPI, fixedDayCount, fixedSchedule,
            fixedPaymentConvention, contractObservationLag,
            fixedIndex, observationInterpolation)
        asofDate = Settings.instance().evaluationDate

        floatFix = [0.06255, 0.05975, 0.0637, 0.018425, 0.0073438, -1, -1]
        cpiFix = [211.4, 217.2, 211.4, 213.4, -2, -2]
        for i in range(len(floatSchedule)):
            if floatSchedule[i] < common.evaluationDate:
                floatIndex.addFixing(floatSchedule[i], floatFix[i], true)

            zic = as_cpi_coupon(zisV.cpiLeg()[i])
            if bool(zic):
                if zic.fixingDate() < (common.evaluationDate - Period(1, Months)):
                    fixedIndex.addFixing(zic.fixingDate(), cpiFix[i], true)

        dse = DiscountingSwapEngine(common.nominalTS)
        zisV.setPricingEngine(dse)

        testInfLegNPV = 0.0
        for i in range(len(zisV.leg(0))):

            zicPayDate = (zisV.leg(0))[i].date()
            if zicPayDate > asofDate:
                testInfLegNPV += (zisV.leg(0))[i].amount() * common.nominalTS.discount(zicPayDate)

            zicV = as_cpi_coupon(zisV.cpiLeg()[i])
            if bool(zicV):
                diff = abs(zicV.rate() - (fixedRate * (zicV.indexFixing() / baseCPI)))
                self.assertTrue(diff < 1e-8)

        error = abs(testInfLegNPV - zisV.legNPV(0))
        self.assertTrue(error < 1e-5)

        diff = abs(1 - zisV.NPV() / 4191660.0)

        max_diff = 1e-5 if usingAtParCoupons else 3e-5

        self.assertTrue(diff < max_diff)

        common.hcpi.reset()

    def testZciisconsistency(self):
        TEST_MESSAGE(
            "Checking CPI swap against zero-coupon inflation swap...")

        common = CommonVars()

        ztype = Swap.Payer
        nominal = 1000000.0
        startDate = common.evaluationDate
        endDate = Date(25, November, 2059)
        cal = UnitedKingdom()
        paymentConvention = ModifiedFollowing
        dummyDC = ActualActual(ActualActual.ISDA)
        dc = ActualActual(ActualActual.ISDA)
        observationLag = Period(2, Months)

        quote = 0.03714
        zciis = ZeroCouponInflationSwap(
            ztype, nominal, startDate, endDate, cal, paymentConvention, dc,
            quote, common.ii, observationLag, CPI.AsIndex)

        dse = DiscountingSwapEngine(common.nominalTS)

        zciis.setPricingEngine(dse)
        self.assertTrue(abs(zciis.NPV()) < 1e-3)

        oneDate = [endDate]
        schOneDate = Schedule(oneDate, cal, paymentConvention)

        stype = Swap.Payer
        inflationNominal = nominal
        floatNominal = inflationNominal * pow(1.0 + quote, 50)
        subtractInflationNominal = true
        dummySpread = 0.0
        dummyFixedRate = 0.0
        fixingDays = 0
        baseDate = startDate - observationLag
        baseCPI = common.ii.fixing(baseDate)

        dummyFloatIndex = IborIndex(
            "dummy_idx", Period(1, Years), 1, CNYCurrency(), China(),
            Following, true, dummyDC)

        cS = CPISwap(
            stype, floatNominal, subtractInflationNominal, dummySpread, dummyDC, schOneDate,
            paymentConvention, fixingDays, dummyFloatIndex,
            dummyFixedRate, baseCPI, dummyDC, schOneDate, paymentConvention, observationLag,
            common.ii, CPI.AsIndex, inflationNominal)

        cS.setPricingEngine(dse)
        self.assertTrue(abs(cS.NPV()) < 1e-3)

        for i in range(2):
            self.assertTrue(
                abs(cS.legNPV(i) - zciis.legNPV(i)) < 1e-3)

        common.hcpi.reset()

    def testCpibondconsistency(self):
        TEST_MESSAGE(
            "Checking CPI swap against CPI bond...")

        common = CommonVars()

        type = Swap.Payer
        nominal = 1000000.0
        subtractInflationNominal = true

        spread = 0.0
        floatDayCount = Actual365Fixed()
        floatPaymentConvention = ModifiedFollowing
        fixingDays = 0
        floatIndex = GBPLibor(Period(6, Months), common.nominalTS)

        fixedRate = 0.1
        baseCPI = 206.1
        fixedDayCount = Actual365Fixed()
        fixedPaymentConvention = ModifiedFollowing
        fixedPaymentCalendar = UnitedKingdom()
        fixedIndex = common.ii
        contractObservationLag = common.contractObservationLag
        observationInterpolation = common.contractObservationInterpolation

        startDate = Date(2, October, 2007)
        endDate = Date(2, October, 2052)
        floatSchedule = MakeSchedule()
        floatSchedule.fromDate(startDate)
        floatSchedule.to(endDate)
        floatSchedule.withTenor(Period(6, Months))
        floatSchedule.withCalendar(UnitedKingdom())
        floatSchedule.withConvention(floatPaymentConvention)
        floatSchedule.backwards()
        floatSchedule = floatSchedule.makeSchedule()

        fixedSchedule = MakeSchedule()
        fixedSchedule.fromDate(startDate)
        fixedSchedule.to(endDate)
        fixedSchedule.withTenor(Period(6, Months))
        fixedSchedule.withCalendar(UnitedKingdom())
        fixedSchedule.withConvention(Unadjusted)
        fixedSchedule.backwards()
        fixedSchedule = fixedSchedule.makeSchedule()

        zisV = CPISwap(
            type, nominal, subtractInflationNominal,
            spread, floatDayCount, floatSchedule,
            floatPaymentConvention, fixingDays, floatIndex,
            fixedRate, baseCPI, fixedDayCount, fixedSchedule,
            fixedPaymentConvention, contractObservationLag,
            fixedIndex, observationInterpolation)

        floatFix = [0.06255, 0.05975, 0.0637, 0.018425, 0.0073438, -1, -1]
        cpiFix = [211.4, 217.2, 211.4, 213.4, -2, -2]
        for i in range(len(floatSchedule)):
            if floatSchedule[i] < common.evaluationDate:
                floatIndex.addFixing(floatSchedule[i], floatFix[i], true)

            zic = as_cpi_coupon(zisV.cpiLeg()[i])
            if bool(zic):
                if zic.fixingDate() < (common.evaluationDate - Period(1, Months)):
                    fixedIndex.addFixing(zic.fixingDate(), cpiFix[i], true)

        dse = DiscountingSwapEngine(common.nominalTS)
        zisV.setPricingEngine(dse)

        fixedRates = DoubleVector(1, fixedRate)
        settlementDays = 1
        growthOnly = true
        cpiB = CPIBond(
            settlementDays, nominal, growthOnly,
            baseCPI, contractObservationLag, fixedIndex,
            observationInterpolation, fixedSchedule,
            fixedRates, fixedDayCount, fixedPaymentConvention)

        dbe = DiscountingBondEngine(common.nominalTS)
        cpiB.setPricingEngine(dbe)

        self.assertTrue(
            abs(cpiB.NPV() - zisV.legNPV(0)) < 1e-5)

        common.hcpi.reset()
