import unittest
from math import sqrt, log, exp

from QuantLib import *

from utilities import *


class TestData(object):
    def __init__(self):
        self.refDate = Date(23, February, 2018)
        Settings.instance().evaluationDate = self.refDate

        self.yts2 = YieldTermStructureHandle(
            FlatForward(self.refDate, 0.02, Actual365Fixed()))

        self.swLn = SwaptionVolatilityStructureHandle(
            ConstantSwaptionVolatility(
                self.refDate, TARGET(), Following, 0.20,
                Actual365Fixed(), ShiftedLognormal, 0.0))
        self.swSln = SwaptionVolatilityStructureHandle(
            ConstantSwaptionVolatility(
                self.refDate, TARGET(), Following, 0.10,
                Actual365Fixed(), ShiftedLognormal, 0.01))
        self.swN = SwaptionVolatilityStructureHandle(
            ConstantSwaptionVolatility(
                self.refDate, TARGET(), Following,
                0.0075, Actual365Fixed(), Normal, 0.01))

        self.reversion = QuoteHandle(SimpleQuote(0.01))
        self.cmsPricerLn = LinearTsrPricer(self.swLn, self.reversion, self.yts2)
        self.cmsPricerSln = LinearTsrPricer(self.swSln, self.reversion, self.yts2)
        self.cmsPricerN = LinearTsrPricer(self.swN, self.reversion, self.yts2)

        self.correlation = QuoteHandle(SimpleQuote(0.6))
        self.cmsspPricerLn = LognormalCmsSpreadPricer(
            self.cmsPricerLn, self.correlation, self.yts2, 32)
        self.cmsspPricerSln = LognormalCmsSpreadPricer(
            self.cmsPricerSln, self.correlation, self.yts2, 32)
        self.cmsspPricerN = LognormalCmsSpreadPricer(
            self.cmsPricerN, self.correlation, self.yts2, 32)

        self.backup = SavedSettings()


def mcReferenceValue(cpn1,
                     cpn2,
                     cap,
                     floor,
                     vol,
                     correlation):
    samples = 1000000

    acc = 0.0
    Cov = Matrix(2, 2)
    Cov[0][0] = vol.blackVariance(cpn1.fixingDate(), cpn1.index().tenor(), cpn1.indexFixing())
    Cov[1][1] = vol.blackVariance(cpn2.fixingDate(), cpn2.index().tenor(), cpn2.indexFixing())
    Cov[0][1] = sqrt(Cov[0][0] * Cov[1][1]) * correlation
    Cov[1][0] = sqrt(Cov[0][0] * Cov[1][1]) * correlation
    C = pseudoSqrt(Cov)

    atmRate = Array(2)
    adjRate = Array(2)
    avg = Array(2)
    volShift = Array(2)
    atmRate[0] = cpn1.indexFixing()
    atmRate[1] = cpn2.indexFixing()
    adjRate[0] = cpn1.adjustedFixing()
    adjRate[1] = cpn2.adjustedFixing()
    if vol.volatilityType() == ShiftedLognormal:
        volShift[0] = vol.shift(cpn1.fixingDate(), cpn1.index().tenor())
        volShift[1] = vol.shift(cpn2.fixingDate(), cpn2.index().tenor())
        avg[0] = log((adjRate[0] + volShift[0]) / (atmRate[0] + volShift[0])) - 0.5 * Cov[0][0]
        avg[1] = log((adjRate[1] + volShift[1]) / (atmRate[1] + volShift[1])) - 0.5 * Cov[1][1]
    else:
        avg[0] = adjRate[0]
        avg[1] = adjRate[1]

    icn = InverseCumulativeNormal()
    sb_ = SobolRsg(2, 42)
    w = Array(2)
    z = Array(2)
    for i in range(samples):
        seq = sb_.nextSequence().value()

        for j in range(len(seq)):
            w[j] = icn(seq[j])
        z = C * w + avg
        for j in range(2):
            if vol.volatilityType() == ShiftedLognormal:
                z[j] = (atmRate[j] + volShift[j]) * exp(z[j]) - volShift[j]

        acc += min(max(z[0] - z[1], floor), cap)

    return acc / samples


class CmsSpreadTest(unittest.TestCase):

    def testFixings(self):
        TEST_MESSAGE(
            "Testing fixings of cms spread indices...")

        d = TestData()

        cms10y = EuriborSwapIsdaFixA(Period(10, Years), d.yts2, d.yts2)
        cms2y = EuriborSwapIsdaFixA(Period(2, Years), d.yts2, d.yts2)
        cms10y2y = SwapSpreadIndex("cms10y2y", cms10y, cms2y)

        Settings.instance().enforcesTodaysHistoricFixings = false

        self.assertRaises(
            Exception, cms10y2y.fixing, d.refDate - Period(1, Days))

        try:
            cms10y2y.fixing(d.refDate)
        except Exception as e:
            NO_THROW = false
            self.assertTrue(NO_THROW)

        self.assertEqual(cms10y2y.fixing(d.refDate), cms10y.fixing(d.refDate) - cms2y.fixing(d.refDate))
        cms10y.addFixing(d.refDate, 0.05)
        self.assertEqual(cms10y2y.fixing(d.refDate), cms10y.fixing(d.refDate) - cms2y.fixing(d.refDate))
        cms2y.addFixing(d.refDate, 0.04)
        self.assertEqual(cms10y2y.fixing(d.refDate), cms10y.fixing(d.refDate) - cms2y.fixing(d.refDate))
        futureFixingDate = TARGET().adjust(d.refDate + Period(1, Years))
        self.assertEqual(
            cms10y2y.fixing(futureFixingDate),
            cms10y.fixing(futureFixingDate) - cms2y.fixing(futureFixingDate))
        IndexManager.instance().clearHistories()

        Settings.instance().enforcesTodaysHistoricFixings = true
        self.assertRaises(RuntimeError, cms10y2y.fixing, d.refDate)
        cms10y.addFixing(d.refDate, 0.05)
        self.assertRaises(RuntimeError, cms10y2y.fixing, d.refDate)
        cms2y.addFixing(d.refDate, 0.04)
        self.assertEqual(
            cms10y2y.fixing(d.refDate),
            cms10y.fixing(d.refDate) - cms2y.fixing(d.refDate))
        IndexManager.instance().clearHistories()

    @unittest.skipIf(skipSlowTest, "testCouponPricing")
    def testCouponPricing(self):
        TEST_MESSAGE(
            "Testing pricing of cms spread coupons...")

        d = TestData()
        tol = 1E-6

        cms10y = EuriborSwapIsdaFixA(Period(10, Years), d.yts2, d.yts2)
        cms2y = EuriborSwapIsdaFixA(Period(2, Years), d.yts2, d.yts2)
        cms10y2y = SwapSpreadIndex("cms10y2y", cms10y, cms2y)

        valueDate = cms10y2y.valueDate(d.refDate)
        payDate = valueDate + Period(1, Years)
        cpn1a = CmsCoupon(
            payDate, 10000.0, valueDate, payDate, cms10y.fixingDays(), cms10y,
            1.0, 0.0, Date(), Date(), Actual360(), false)
        cpn1b = CmsCoupon(
            payDate, 10000.0, valueDate, payDate, cms2y.fixingDays(),
            cms2y, 1.0, 0.0, Date(), Date(), Actual360(), false)
        cpn1 = CmsSpreadCoupon(
            payDate, 10000.0, valueDate, payDate, cms10y2y.fixingDays(),
            cms10y2y, 1.0, 0.0, Date(), Date(), Actual360(), false)
        self.assertTrue(cpn1.fixingDate() == d.refDate)
        cpn1a.setPricer(d.cmsPricerLn)
        cpn1b.setPricer(d.cmsPricerLn)
        cpn1.setPricer(d.cmsspPricerLn)

        eqTol = 1e-13

        self.assertTrue(abs(cpn1.rate() - (cpn1a.rate() - cpn1b.rate())) < eqTol)
        cms10y.addFixing(d.refDate, 0.05)
        self.assertTrue(abs(cpn1.rate() - (cpn1a.rate() - cpn1b.rate())) < eqTol)
        cms2y.addFixing(d.refDate, 0.03)
        self.assertTrue(abs(cpn1.rate() - (cpn1a.rate() - cpn1b.rate())) < eqTol)
        IndexManager.instance().clearHistories()

        cpn2a = CmsCoupon(
            Date(23, February, 2029), 10000.0,
            Date(23, February, 2028), Date(23, February, 2029), 2,
            cms10y, 1.0, 0.0, Date(), Date(), Actual360(), false)
        cpn2b = CmsCoupon(
            Date(23, February, 2029), 10000.0,
            Date(23, February, 2028), Date(23, February, 2029), 2,
            cms2y, 1.0, 0.0, Date(), Date(), Actual360(), false)

        plainCpn = CappedFlooredCmsSpreadCoupon(
            Date(23, February, 2029), 10000.0, Date(23, February, 2028),
            Date(23, February, 2029), 2, cms10y2y, 1.0, 0.0, NullReal(),
            NullReal(), Date(), Date(), Actual360(), false)
        cappedCpn = CappedFlooredCmsSpreadCoupon(
            Date(23, February, 2029), 10000.0, Date(23, February, 2028),
            Date(23, February, 2029), 2, cms10y2y, 1.0, 0.0, 0.03,
            NullReal(), Date(), Date(), Actual360(), false)
        flooredCpn = CappedFlooredCmsSpreadCoupon(
            Date(23, February, 2029), 10000.0, Date(23, February, 2028),
            Date(23, February, 2029), 2, cms10y2y, 1.0, 0.0, NullReal(),
            0.01, Date(), Date(), Actual360(), false)
        collaredCpn = CappedFlooredCmsSpreadCoupon(
            Date(23, February, 2029), 10000.0, Date(23, February, 2028),
            Date(23, February, 2029), 2, cms10y2y, 1.0, 0.0, 0.03, 0.01,
            Date(), Date(), Actual360(), false)

        cpn2a.setPricer(d.cmsPricerLn)
        cpn2b.setPricer(d.cmsPricerLn)
        plainCpn.setPricer(d.cmsspPricerLn)
        cappedCpn.setPricer(d.cmsspPricerLn)
        flooredCpn.setPricer(d.cmsspPricerLn)
        collaredCpn.setPricer(d.cmsspPricerLn)

        self.assertLess(
            abs(plainCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, QL_MAX_REAL,
                    -QL_MAX_REAL, d.swLn,
                    d.correlation.value())),
            tol)
        self.assertLess(
            abs(cappedCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, 0.03,
                    -QL_MAX_REAL, d.swLn,
                    d.correlation.value())),
            tol)
        self.assertLess(
            abs(flooredCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, QL_MAX_REAL, 0.01, d.swLn,
                    d.correlation.value())),
            tol)
        self.assertLess(
            abs(collaredCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, 0.03, 0.01, d.swLn,
                    d.correlation.value())),
            tol)

        cpn2a.setPricer(d.cmsPricerSln)
        cpn2b.setPricer(d.cmsPricerSln)
        plainCpn.setPricer(d.cmsspPricerSln)
        cappedCpn.setPricer(d.cmsspPricerSln)
        flooredCpn.setPricer(d.cmsspPricerSln)
        collaredCpn.setPricer(d.cmsspPricerSln)

        self.assertLess(
            abs(plainCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, QL_MAX_REAL,
                    -QL_MAX_REAL, d.swSln,
                    d.correlation.value())),
            tol)
        self.assertLess(
            abs(cappedCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, 0.03,
                    -QL_MAX_REAL, d.swSln,
                    d.correlation.value())),
            tol)
        self.assertLess(
            abs(flooredCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, QL_MAX_REAL, 0.01, d.swSln,
                    d.correlation.value())),
            tol)
        self.assertLess(
            abs(collaredCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, 0.03, 0.01, d.swSln,
                    d.correlation.value())),
            tol)

        cpn2a.setPricer(d.cmsPricerN)
        cpn2b.setPricer(d.cmsPricerN)
        plainCpn.setPricer(d.cmsspPricerN)
        cappedCpn.setPricer(d.cmsspPricerN)
        flooredCpn.setPricer(d.cmsspPricerN)
        collaredCpn.setPricer(d.cmsspPricerN)

        self.assertLess(
            abs(plainCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, QL_MAX_REAL,
                    -QL_MAX_REAL, d.swN,
                    d.correlation.value())),
            tol)
        self.assertLess(
            abs(cappedCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, 0.03,
                    -QL_MAX_REAL, d.swN,
                    d.correlation.value())),
            tol)
        self.assertLess(
            abs(flooredCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, QL_MAX_REAL, 0.01,
                    d.swN, d.correlation.value())),
            tol)
        self.assertLess(
            abs(collaredCpn.rate() -
                mcReferenceValue(
                    cpn2a, cpn2b, 0.03, 0.01, d.swN,
                    d.correlation.value())),
            tol)
