import unittest
from math import floor

from QuantLib import *

from utilities import *


class CommonVars(object):
    def __init__(self):
        self.nominalEUR = YieldTermStructureHandle()
        self.nominalGBP = YieldTermStructureHandle()
        self.yoyEU = RelinkableYoYInflationTermStructureHandle()
        self.yoyUK = RelinkableYoYInflationTermStructureHandle()
        self.cStrikesEU = DoubleVector()
        self.fStrikesEU = DoubleVector()
        self.cfMaturitiesEU = PeriodVector()
        self.cPriceEU = Matrix()
        self.fPriceEU = Matrix()
        self.yoyIndexUK = None
        self.yoyIndexEU = None
        self.cStrikesUK = DoubleVector()
        self.fStrikesUK = DoubleVector()
        self.cfMaturitiesUK = PeriodVector()
        self.cPriceUK = Matrix()
        self.fPriceUK = Matrix()
        self.priceSurfEU = None

    def reset(self):
        self.nominalEUR = YieldTermStructureHandle()
        self.nominalGBP = YieldTermStructureHandle()
        self.priceSurfEU = None
        self.yoyEU.reset()
        self.yoyUK.reset()
        self.yoyIndexUK = None
        self.yoyIndexEU = None
        self.cPriceEU = Matrix()
        self.fPriceEU = Matrix()
        self.cPriceUK = Matrix()
        self.fPriceUK = Matrix()
        self.cStrikesEU.clear()
        self.fStrikesEU.clear()
        self.cStrikesUK.clear()
        self.fStrikesUK.clear()
        self.cfMaturitiesEU.clear()
        self.cfMaturitiesUK.clear()

    def setup(self):

        eval = Date(23, 11, 2007)
        Settings.instance().evaluationDate = eval

        self.yoyIndexUK = YYUKRPIr(true, self.yoyUK)
        self.yoyIndexEU = YYEUHICPr(true, self.yoyEU)

        timesEUR = [
            0.0109589, 0.0684932, 0.263014, 0.317808, 0.567123, 0.816438,
            1.06575, 1.31507, 1.56438, 2.0137, 3.01918, 4.01644,
            5.01644, 6.01644, 7.01644, 8.01644, 9.02192, 10.0192,
            12.0192, 15.0247, 20.0301, 25.0356, 30.0329, 40.0384,
            50.0466]
        ratesEUR = [
            0.0415600, 0.0426840, 0.0470980, 0.0458506, 0.0449550, 0.0439784,
            0.0431887, 0.0426604, 0.0422925, 0.0424591, 0.0421477, 0.0421853,
            0.0424016, 0.0426969, 0.0430804, 0.0435011, 0.0439368, 0.0443825,
            0.0452589, 0.0463389, 0.0472636, 0.0473401, 0.0470629, 0.0461092,
            0.0450794]

        timesGBP = [
            0.008219178, 0.010958904, 0.01369863, 0.019178082, 0.073972603,
            0.323287671, 0.57260274, 0.821917808, 1.071232877, 1.320547945,
            1.506849315, 2.002739726, 3.002739726, 4.002739726, 5.005479452,
            6.010958904, 7.008219178, 8.005479452, 9.008219178, 10.00821918,
            12.01369863, 15.0109589, 20.01369863, 25.01917808, 30.02191781,
            40.03287671, 50.03561644, 60.04109589, 70.04931507]
        ratesGBP = [
            0.0577363, 0.0582314, 0.0585265, 0.0587165, 0.0596598,
            0.0612506, 0.0589676, 0.0570512, 0.0556147, 0.0546082,
            0.0549492, 0.053801, 0.0529333, 0.0524068, 0.0519712,
            0.0516615, 0.0513711, 0.0510433, 0.0507974, 0.0504833,
            0.0498998, 0.0490464, 0.04768, 0.0464862, 0.045452,
            0.0437699, 0.0425311, 0.0420073, 0.041151]

        r = []
        d = []
        nTimesEUR = len(timesEUR)
        nTimesGBP = len(timesGBP)
        for i in range(nTimesEUR):
            r.append(ratesEUR[i])
            ys = int(floor(timesEUR[i]))
            ds = int(((timesEUR[i] - ys) * 365))
            dd = eval + Period(ys, Years) + Period(ds, Days)
            d.append(dd)

        euriborTS = CubicZeroCurve(d, r, Actual365Fixed())
        nominalHeur = YieldTermStructureHandle(euriborTS, false)
        self.nominalEUR = nominalHeur

        d.clear()
        r.clear()
        for i in range(nTimesGBP):
            r.append(ratesGBP[i])
            ys = int(floor(timesGBP[i]))
            ds = int(((timesGBP[i] - ys) * 365))
            dd = eval + Period(ys, Years) + Period(ds, Days)
            d.append(dd)

        gbpLiborTS = CubicZeroCurve(d, r, Actual365Fixed())
        nominalHgbp = YieldTermStructureHandle(gbpLiborTS, false)
        self.nominalGBP = nominalHgbp

        yoyEUrates = [
            0.0237951,
            0.0238749, 0.0240334, 0.0241934, 0.0243567, 0.0245323,
            0.0247213, 0.0249348, 0.0251768, 0.0254337, 0.0257258,
            0.0260217, 0.0263006, 0.0265538, 0.0267803, 0.0269378,
            0.0270608, 0.0271363, 0.0272, 0.0272512, 0.0272927,
            0.027317, 0.0273615, 0.0273811, 0.0274063, 0.0274307,
            0.0274625, 0.027527, 0.0275952, 0.0276734, 0.027794]

        d.clear()
        r.clear()
        baseDate = TARGET().advance(eval, -2, Months, ModifiedFollowing)
        for i in range(len(yoyEUrates)):
            dd = TARGET().advance(baseDate, i, Years, ModifiedFollowing)
            d.append(dd)
            r.append(yoyEUrates[i])

        indexIsInterpolated = true

        pYTSEU = YoYInflationCurve(
            eval, TARGET(), Actual365Fixed(), Period(2, Months), Monthly,
            indexIsInterpolated, d, r)
        self.yoyEU.linkTo(pYTSEU)

        ncStrikesEU = 6
        nfStrikesEU = 6
        ncfMaturitiesEU = 7
        capStrikesEU = [0.02, 0.025, 0.03, 0.035, 0.04, 0.05]
        capMaturitiesEU = [
            Period(3, Years), Period(5, Years), Period(7, Years),
            Period(10, Years), Period(15, Years), Period(20, Years), Period(30, Years)]
        capPricesEU = [
            (116.225, 204.945, 296.285, 434.29, 654.47, 844.775, 1132.33),
            (34.305, 71.575, 114.1, 184.33, 307.595, 421.395, 602.35),
            (6.37, 19.085, 35.635, 66.42, 127.69, 189.685, 296.195),
            (1.325, 5.745, 12.585, 26.945, 58.95, 94.08, 158.985),
            (0.501, 2.37, 5.38, 13.065, 31.91, 53.95, 96.97),
            (0.501, 0.695, 1.47, 4.415, 12.86, 23.75, 46.7)]

        floorStrikesEU = [-0.01, 0.00, 0.005, 0.01, 0.015, 0.02]
        floorPricesEU = [
            (0.501, 0.851, 2.44, 6.645, 16.23, 26.85, 46.365),
            (0.501, 2.236, 5.555, 13.075, 28.46, 44.525, 73.08),
            (1.025, 3.935, 9.095, 19.64, 39.93, 60.375, 96.02),
            (2.465, 7.885, 16.155, 31.6, 59.34, 86.21, 132.045),
            (6.9, 17.92, 32.085, 56.08, 95.95, 132.85, 194.18),
            (23.52, 47.625, 74.085, 114.355, 175.72, 229.565, 316.285)]

        self.cStrikesEU.clear()
        self.fStrikesEU.clear()
        self.cfMaturitiesEU.clear()
        for i in capStrikesEU:
            self.cStrikesEU.append(i)
        for i in floorStrikesEU:
            self.fStrikesEU.append(i)
        for i in capMaturitiesEU:
            self.cfMaturitiesEU.append(i)
        tcPriceEU = Matrix(ncStrikesEU, ncfMaturitiesEU)
        tfPriceEU = Matrix(nfStrikesEU, ncfMaturitiesEU)
        for i in range(ncStrikesEU):
            for j in range(ncfMaturitiesEU):
                tcPriceEU[i][j] = capPricesEU[i][j]

        for i in range(nfStrikesEU):
            for j in range(ncfMaturitiesEU):
                tfPriceEU[i][j] = floorPricesEU[i][j]

        self.cPriceEU = tcPriceEU
        self.fPriceEU = tfPriceEU

    def setupPriceSurface(self):

        fixingDays = 0
        lag = 3
        yyLag = Period(lag, Months)
        baseRate = 1
        dc = Actual365Fixed()
        cal = TARGET()
        bdc = ModifiedFollowing
        pn = self.nominalEUR.currentLink()
        n = YieldTermStructureHandle(pn, false)

        cfEUprices = YoYInflationCapFloorTermPriceSurface(

            fixingDays,
            yyLag, self.yoyIndexEU, baseRate,
            n, dc,
            cal, bdc,
            self.cStrikesEU, self.fStrikesEU, self.cfMaturitiesEU,
            self.cPriceEU, self.fPriceEU)

        self.priceSurfEU = cfEUprices


class InflationVolTest(unittest.TestCase):

    def testYoYPriceSurfaceToATM(self):
        TEST_MESSAGE(
            "Testing conversion fromDate YoY cap-floor surface "
            "to YoY inflation term structure...")

        backup = SavedSettings()

        vars = CommonVars()
        vars.setup()
        vars.setupPriceSurface()

        yyATMt = vars.priceSurfEU.atmYoYSwapTimeRates()
        yyATMd = vars.priceSurfEU.atmYoYSwapDateRates()

        crv = [
            0.024586, 0.0247575, 0.0249396, 0.0252596,
            0.0258498, 0.0262883, 0.0267915]
        swaps = [
            0.024586, 0.0247575, 0.0249396, 0.0252596,
            0.0258498, 0.0262883, 0.0267915]
        ayoy = [
            0.0247659, 0.0251437, 0.0255945, 0.0265234,
            0.0280457, 0.0285534, 0.0295884]
        eps = 2e-5
        for i in range(len(yyATMt[0])):
            self.assertTrue(abs(yyATMt[1][i] - crv[i]) < eps)

        for i in range(len(yyATMd[0])):
            self.assertTrue(
                abs(vars.priceSurfEU.atmYoYSwapRate(yyATMd[0][i]) - swaps[i]) < eps)

        for i in range(len(yyATMd[0])):
            self.assertTrue(
                abs(vars.priceSurfEU.atmYoYRate(yyATMd[0][i]) - ayoy[i]) < eps)

        vars.reset()

    def testYoYPriceSurfaceToVol(self):
        TEST_MESSAGE(
            "Testing conversion fromDate YoY price surface "
            "to YoY volatility surface...")

        backup = SavedSettings()
        vars = CommonVars()
        vars.setup()

        vars.setupPriceSurface()

        hVS = YoYOptionletVolatilitySurfaceHandle(false)

        yoyPricerUD = YoYInflationUnitDisplacedBlackCapFloorEngine(
            vars.yoyIndexEU, hVS, vars.nominalEUR)

        yoyOptionletStripper = InterpolatedYoYInflationOptionletStripper()

        settlementDays = 0
        cal = TARGET()
        bdc = ModifiedFollowing
        dc = Actual365Fixed()

        capFloorPrices = vars.priceSurfEU
        lag = vars.priceSurfEU.observationLag()

        slope = -0.5

        yoySurf = KInterpolatedYoYInflationOptionletVolatilitySurface(
            settlementDays,
            cal, bdc, dc, lag, capFloorPrices,
            yoyPricerUD, yoyOptionletStripper,
            slope)

        volATyear1 = [
            0.0128, 0.0093, 0.0083, 0.0073, 0.0064,
            0.0058, 0.0042, 0.0046, 0.0053, 0.0064,
            0.0098]
        volATyear3 = [
            0.0079, 0.0058, 0.0051, 0.0045, 0.0039,
            0.0035, 0.0026, 0.0028, 0.0033, 0.0039,
            0.0060]

        d = yoySurf.baseDate() + Period(1, Years)
        someSlice = yoySurf.Dslice(d)

        n = len(someSlice[0])
        eps = 0.0001
        for i in range(n):
            self.assertTrue(
                abs(someSlice[1][i] - volATyear1[i]) < eps)

        d = yoySurf.baseDate() + Period(3, Years)

        someOtherSlice = yoySurf.Dslice(d)
        n = len(someOtherSlice[0])
        for i in range(n):
            self.assertTrue(abs(someOtherSlice[1][i] - volATyear3[i]) < eps)

        vars.reset()
