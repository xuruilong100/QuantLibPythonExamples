import unittest

import numpy as np
from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):

        self.calendar = TARGET()

        self.referenceDate = self.calendar.adjust(knownGoodDefault)
        Settings.instance().evaluationDate = self.referenceDate
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.termStructure.linkTo(
            flatRate(self.referenceDate, 0.05, Actual365Fixed()))
        self.backup = SavedSettings()

        atmOptionTenors = [
            Period(1, Months), Period(6, Months), Period(1, Years),
            Period(5, Years), Period(10, Years), Period(30, Years)]

        atmSwapTenors = [
            Period(1, Years), Period(5, Years), Period(10, Years), Period(30, Years)]

        m = Matrix(len(atmOptionTenors), len(atmSwapTenors))
        m[0][0] = 0.1300
        m[0][1] = 0.1560
        m[0][2] = 0.1390
        m[0][3] = 0.1220
        m[1][0] = 0.1440
        m[1][1] = 0.1580
        m[1][2] = 0.1460
        m[1][3] = 0.1260
        m[2][0] = 0.1600
        m[2][1] = 0.1590
        m[2][2] = 0.1470
        m[2][3] = 0.1290
        m[3][0] = 0.1640
        m[3][1] = 0.1470
        m[3][2] = 0.1370
        m[3][3] = 0.1220
        m[4][0] = 0.1400
        m[4][1] = 0.1300
        m[4][2] = 0.1250
        m[4][3] = 0.1100
        m[5][0] = 0.1130
        m[5][1] = 0.1090
        m[5][2] = 0.1070
        m[5][3] = 0.0930

        self.atmVol = SwaptionVolatilityStructureHandle(
            SwaptionVolatilityMatrix(
                self.calendar,
                Following,
                atmOptionTenors,
                atmSwapTenors,
                m, Actual365Fixed()))

        optionTenors = [Period(1, Years), Period(10, Years), Period(30, Years)]
        swapTenors = [Period(2, Years), Period(10, Years), Period(30, Years)]
        strikeSpreads = [-0.020, -0.005, 0.000, 0.005, 0.020]

        nRows = len(optionTenors) * len(swapTenors)
        nCols = len(strikeSpreads)
        volSpreadsMatrix = Matrix(nRows, nCols)
        volSpreadsMatrix[0][0] = 0.0599
        volSpreadsMatrix[0][1] = 0.0049
        volSpreadsMatrix[0][2] = 0.0000
        volSpreadsMatrix[0][3] = -0.0001
        volSpreadsMatrix[0][4] = 0.0127
        volSpreadsMatrix[1][0] = 0.0729
        volSpreadsMatrix[1][1] = 0.0086
        volSpreadsMatrix[1][2] = 0.0000
        volSpreadsMatrix[1][3] = -0.0024
        volSpreadsMatrix[1][4] = 0.0098
        volSpreadsMatrix[2][0] = 0.0738
        volSpreadsMatrix[2][1] = 0.0102
        volSpreadsMatrix[2][2] = 0.0000
        volSpreadsMatrix[2][3] = -0.0039
        volSpreadsMatrix[2][4] = 0.0065
        volSpreadsMatrix[3][0] = 0.0465
        volSpreadsMatrix[3][1] = 0.0063
        volSpreadsMatrix[3][2] = 0.0000
        volSpreadsMatrix[3][3] = -0.0032
        volSpreadsMatrix[3][4] = -0.0010
        volSpreadsMatrix[4][0] = 0.0558
        volSpreadsMatrix[4][1] = 0.0084
        volSpreadsMatrix[4][2] = 0.0000
        volSpreadsMatrix[4][3] = -0.0050
        volSpreadsMatrix[4][4] = -0.0057
        volSpreadsMatrix[5][0] = 0.0576
        volSpreadsMatrix[5][1] = 0.0083
        volSpreadsMatrix[5][2] = 0.0000
        volSpreadsMatrix[5][3] = -0.0043
        volSpreadsMatrix[5][4] = -0.0014
        volSpreadsMatrix[6][0] = 0.0437
        volSpreadsMatrix[6][1] = 0.0059
        volSpreadsMatrix[6][2] = 0.0000
        volSpreadsMatrix[6][3] = -0.0030
        volSpreadsMatrix[6][4] = -0.0006
        volSpreadsMatrix[7][0] = 0.0533
        volSpreadsMatrix[7][1] = 0.0078
        volSpreadsMatrix[7][2] = 0.0000
        volSpreadsMatrix[7][3] = -0.0045
        volSpreadsMatrix[7][4] = -0.0046
        volSpreadsMatrix[8][0] = 0.0545
        volSpreadsMatrix[8][1] = 0.0079
        volSpreadsMatrix[8][2] = 0.0000
        volSpreadsMatrix[8][3] = -0.0042
        volSpreadsMatrix[8][4] = -0.0020

        volSpreads = QuoteHandleVectorVector(nRows)
        for i in range(nRows):
            temp = QuoteHandleVector()
            for j in range(nCols):
                temp.append(
                    QuoteHandle(
                        SimpleQuote(volSpreadsMatrix[i][j])))
            volSpreads[i] = temp

        self.iborIndex = Euribor6M(self.termStructure)
        swapIndexBase = EuriborSwapIsdaFixA(Period(10, Years), self.termStructure)
        shortSwapIndexBase = EuriborSwapIsdaFixA(Period(2, Years), self.termStructure)

        vegaWeightedSmileFit = false

        self.SabrVolCube2 = SwaptionVolatilityStructureHandle(
            SwaptionVolCube2(
                self.atmVol,
                optionTenors,
                swapTenors,
                strikeSpreads,
                volSpreads,
                swapIndexBase,
                shortSwapIndexBase,
                vegaWeightedSmileFit))
        self.SabrVolCube2.currentLink().enableExtrapolation()

        guess = QuoteHandleVectorVector(nRows)
        for i in range(nRows):
            temp = QuoteHandleVector()
            temp.append(QuoteHandle(SimpleQuote(0.2)))
            temp.append(QuoteHandle(SimpleQuote(0.5)))
            temp.append(QuoteHandle(SimpleQuote(0.4)))
            temp.append(QuoteHandle(SimpleQuote(0.0)))
            guess[i] = temp

        isParameterFixed = BoolVector(4, false)
        isParameterFixed[1] = true

        isAtmCalibrated = false

        self.SabrVolCube1 = SwaptionVolatilityStructureHandle(
            SwaptionVolCube1(
                self.atmVol,
                optionTenors,
                swapTenors,
                strikeSpreads,
                volSpreads,
                swapIndexBase,
                shortSwapIndexBase,
                vegaWeightedSmileFit,
                guess,
                isParameterFixed,
                isAtmCalibrated))
        self.SabrVolCube1.currentLink().enableExtrapolation()

        self.yieldCurveModels = [
            GFunctionFactory.Standard,
            GFunctionFactory.ExactYield,
            GFunctionFactory.ParallelShifts,
            GFunctionFactory.NonParallelShifts,
            GFunctionFactory.NonParallelShifts]

        zeroMeanRev = QuoteHandle(SimpleQuote(0.0))

        self.numericalPricers = []
        self.analyticPricers = []
        for j in range(len(self.yieldCurveModels)):
            if j < len(self.yieldCurveModels) - 1:
                self.numericalPricers.append(
                    NumericHaganPricer(
                        self.atmVol, self.yieldCurveModels[j], zeroMeanRev))
            else:
                self.numericalPricers.append(
                    LinearTsrPricer(self.atmVol, zeroMeanRev))

            self.analyticPricers.append(
                AnalyticHaganPricer(
                    self.atmVol, self.yieldCurveModels[j], zeroMeanRev))


class CmsTest(unittest.TestCase):

    def testFairRate(self):
        TEST_MESSAGE(
            "Testing Hagan-pricer flat-vol equivalence for coupons...")

        vars = CommonVars()

        swapIndex = SwapIndex(
            "EuriborSwapIsdaFixA",
            Period(10, Years),
            vars.iborIndex.fixingDays(),
            vars.iborIndex.currency(),
            vars.iborIndex.fixingCalendar(),
            Period(1, Years),
            Unadjusted,
            vars.iborIndex.dayCounter(),
            vars.iborIndex)

        startDate = vars.termStructure.referenceDate() + Period(20, Years)
        paymentDate = startDate + Period(1, Years)
        endDate = paymentDate
        nominal = 1.0
        infiniteCap = NullReal()
        infiniteFloor = NullReal()
        gearing = 1.0
        spread = 0.0
        coupon = CappedFlooredCmsCoupon(
            paymentDate, nominal,
            startDate, endDate,
            swapIndex.fixingDays(), swapIndex,
            gearing, spread,
            infiniteCap, infiniteFloor,
            startDate, endDate,
            vars.iborIndex.dayCounter())
        for j in range(len(vars.yieldCurveModels)):
            vars.numericalPricers[j].setSwaptionVolatility(vars.atmVol)
            coupon.setPricer(vars.numericalPricers[j])
            rate0 = coupon.rate()

            vars.analyticPricers[j].setSwaptionVolatility(vars.atmVol)
            coupon.setPricer(vars.analyticPricers[j])
            rate1 = coupon.rate()

            difference = abs(rate1 - rate0)
            tol = 2.0e-4
            linearTsr = j == len(vars.yieldCurveModels) - 1

            self.assertFalse(difference > tol)

    def testParity(self):
        TEST_MESSAGE(
            "Testing put-call parity for capped-floored CMS coupons...")

        vars = CommonVars()

        swaptionVols = [
            vars.atmVol, vars.SabrVolCube1, vars.SabrVolCube2]

        swapIndex = EuriborSwapIsdaFixA(
            Period(10, Years), vars.iborIndex.forwardingTermStructure())
        startDate = vars.termStructure.referenceDate() + Period(20, Years)
        paymentDate = startDate + Period(1, Years)
        endDate = paymentDate
        nominal = 1.0
        infiniteCap = NullReal()
        infiniteFloor = NullReal()
        gearing = 1.0
        spread = 0.0
        discount = vars.termStructure.discount(paymentDate)
        swaplet = CappedFlooredCmsCoupon(
            paymentDate, nominal,
            startDate, endDate,
            swapIndex.fixingDays(),
            swapIndex,
            gearing, spread,
            infiniteCap, infiniteFloor,
            startDate, endDate,
            vars.iborIndex.dayCounter())
        for strike in np.arange(.02, .12, 0.05):
            caplet = CappedFlooredCmsCoupon(
                paymentDate, nominal,
                startDate, endDate,
                swapIndex.fixingDays(),
                swapIndex,
                gearing, spread,
                strike, infiniteFloor,
                startDate, endDate,
                vars.iborIndex.dayCounter())
            floorlet = CappedFlooredCmsCoupon(
                paymentDate, nominal,
                startDate, endDate,
                swapIndex.fixingDays(),
                swapIndex,
                gearing, spread,
                infiniteCap, strike,
                startDate, endDate,
                vars.iborIndex.dayCounter())

            for swaptionVol in swaptionVols:
                for j in range(len(vars.yieldCurveModels)):
                    vars.numericalPricers[j].setSwaptionVolatility(swaptionVol)
                    vars.analyticPricers[j].setSwaptionVolatility(swaptionVol)
                    pricers = []
                    pricers.append(vars.numericalPricers[j])
                    pricers.append(vars.analyticPricers[j])
                    for k in range(len(pricers)):
                        swaplet.setPricer(pricers[k])
                        caplet.setPricer(pricers[k])
                        floorlet.setPricer(pricers[k])
                        swapletPrice = swaplet.price(vars.termStructure) + \
                                       nominal * swaplet.accrualPeriod() * strike * discount
                        capletPrice = caplet.price(vars.termStructure)
                        floorletPrice = floorlet.price(vars.termStructure)
                        difference = abs(capletPrice + floorletPrice - swapletPrice)
                        tol = 2.0e-5
                        linearTsr = k == 0 and j == len(vars.yieldCurveModels) - 1
                        if linearTsr:
                            tol = 1.0e-7
                        self.assertFalse(difference > tol)

    def testCmsSwap(self):
        TEST_MESSAGE(
            "Testing Hagan-pricer flat-vol equivalence for swaps...")

        vars = CommonVars()

        swapIndex = SwapIndex(
            "EuriborSwapIsdaFixA",
            Period(10, Years),
            vars.iborIndex.fixingDays(),
            vars.iborIndex.currency(),
            vars.iborIndex.fixingCalendar(),
            Period(1, Years),
            Unadjusted,
            vars.iborIndex.dayCounter(),
            vars.iborIndex)
        spread = 0.0
        swapLengths = [1, 5, 6, 10]
        n = len(swapLengths)
        cms = []
        for i in range(n):
            cms.append(
                MakeCms(
                    Period(swapLengths[i], Years),
                    swapIndex,
                    vars.iborIndex, spread,
                    Period(10, Days)).makeCms())

        for j in range(len(vars.yieldCurveModels)):
            vars.numericalPricers[j].setSwaptionVolatility(vars.atmVol)
            vars.analyticPricers[j].setSwaptionVolatility(vars.atmVol)
            for sl in range(n):
                setCouponPricer(cms[sl].leg(0), vars.numericalPricers[j])
                priceNum = cms[sl].NPV()
                setCouponPricer(cms[sl].leg(0), vars.analyticPricers[j])
                priceAn = cms[sl].NPV()

                difference = abs(priceNum - priceAn)
                tol = 2.0e-4
                linearTsr = j == len(vars.yieldCurveModels) - 1
                self.assertFalse(difference > tol)
