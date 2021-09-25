import unittest
from utilities import *
from QuantLib import *
from math import sqrt, log, exp
import numpy as np


class CalibrationData(object):
    def __init__(self,
                 spot,
                 rTS,
                 qTS,
                 calibrationSet):
        self.spot = spot
        self.rTS = rTS
        self.qTS = qTS
        self.calibrationSet = calibrationSet


class CalibrationResults(object):
    def __init__(self,
                 calibrationType,
                 interpolationType,
                 maxError,
                 avgError,
                 lvMaxError,
                 lvAvgError):
        self.calibrationType = calibrationType
        self.interpolationType = interpolationType
        self.maxError = maxError
        self.avgError = avgError
        self.lvMaxError = lvMaxError
        self.lvAvgError = lvAvgError


def AndreasenHugeExampleData():
    # This is the example market data from the original paper
    # Andreasen J., Huge B., 2010. Volatility Interpolation
    # https://ssrn.com/abstract=1694972

    spot = QuoteHandle(SimpleQuote(2772.7))
    maturityTimes = [
        0.025, 0.101, 0.197, 0.274, 0.523, 0.772,
        1.769, 2.267, 2.784, 3.781, 4.778, 5.774]

    raw = [
        [0.5131, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.3366, 0.3291, 0.0000, 0.0000],
        [0.5864, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.3178, 0.3129, 0.3008, 0.0000],
        [0.6597, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.3019, 0.2976, 0.2975, 0.0000],
        [0.7330, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.2863, 0.2848, 0.2848, 0.0000],
        [0.7697, 0.0000, 0.0000, 0.0000, 0.3262, 0.3079, 0.3001, 0.2843, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.8063, 0.0000, 0.0000, 0.0000, 0.3058, 0.2936, 0.2876, 0.2753, 0.2713, 0.2711, 0.2711, 0.2722, 0.2809],
        [0.8430, 0.0000, 0.0000, 0.0000, 0.2887, 0.2798, 0.2750, 0.2666, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.8613, 0.3365, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.8796, 0.3216, 0.2906, 0.2764, 0.2717, 0.2663, 0.2637, 0.2575, 0.2555, 0.2580, 0.2585, 0.2611, 0.2693],
        [0.8979, 0.3043, 0.2797, 0.2672, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.9163, 0.2880, 0.2690, 0.2578, 0.2557, 0.2531, 0.2519, 0.2497, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.9346, 0.2724, 0.2590, 0.2489, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.9529, 0.2586, 0.2488, 0.2405, 0.2407, 0.2404, 0.2411, 0.2418, 0.2410, 0.2448, 0.2469, 0.2501, 0.2584],
        [0.9712, 0.2466, 0.2390, 0.2329, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.9896, 0.2358, 0.2300, 0.2253, 0.2269, 0.2284, 0.2299, 0.2347, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [1.0079, 0.2247, 0.2213, 0.2184, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [1.0262, 0.2159, 0.2140, 0.2123, 0.2142, 0.2173, 0.2198, 0.2283, 0.2275, 0.2322, 0.2384, 0.2392, 0.2486],
        [1.0445, 0.2091, 0.2076, 0.2069, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [1.0629, 0.2056, 0.2024, 0.2025, 0.2039, 0.2074, 0.2104, 0.2213, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [1.0812, 0.2045, 0.1982, 0.1984, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [1.0995, 0.2025, 0.1959, 0.1944, 0.1962, 0.1988, 0.2022, 0.2151, 0.2161, 0.2219, 0.2269, 0.2305, 0.2399],
        [1.1178, 0.1933, 0.1929, 0.1920, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [1.1362, 0.0000, 0.0000, 0.0000, 0.1902, 0.1914, 0.1950, 0.2091, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [1.1728, 0.0000, 0.0000, 0.0000, 0.1885, 0.1854, 0.1888, 0.2039, 0.2058, 0.2122, 0.2186, 0.2223, 0.2321],
        [1.2095, 0.0000, 0.0000, 0.0000, 0.1867, 0.1811, 0.1839, 0.1990, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [1.2461, 0.0000, 0.0000, 0.0000, 0.1871, 0.1785, 0.1793, 0.1945, 0.0000, 0.2054, 0.2103, 0.2164, 0.2251],
        [1.3194, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.1988, 0.2054, 0.2105, 0.2190],
        [1.3927, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.1930, 0.2002, 0.2054, 0.2135],
        [1.4660, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.1849, 0.1964, 0.2012, 0.0000]]

    dc = Actual365Fixed()
    today = Date(1, March, 2010)

    rTS = YieldTermStructureHandle(flatRate(today, 0.0, dc))
    qTS = YieldTermStructureHandle(flatRate(today, 0.0, dc))

    nStrikes = len(raw)
    nMaturities = len(maturityTimes)

    noneZero = 0
    for i in range(len(raw)):
        for j in range(len(raw[i]) - 1):
            if raw[i][j] != 0.0:
                noneZero += 1

    calibrationSet = CalibrationSet()
    calibrationSet.reserve(noneZero - nStrikes)

    for i in range(len(raw)):
        strike = spot.value() * raw[i][0]
        for j in range(1, len(raw[i])):
            if raw[i][j] > QL_EPSILON:
                maturity = today + Period(
                    int(365 * maturityTimes[j - 1]), Days)
                impliedVol = raw[i][j]

                calibrationSet.append(
                    CalibrationPair(
                        VanillaOption(
                            PlainVanillaPayoff(
                                Option.Put if strike < spot.value() else Option.Call,
                                strike),
                            EuropeanExercise(maturity)),
                        SimpleQuote(impliedVol)))

    data = CalibrationData(
        spot, rTS, qTS, calibrationSet)

    return data


def BorovkovaExampleData():
    # see Svetlana Borovkova, Ferry J. Permana
    # Implied volatility in oil markets
    # http://www.researchgate.net/publication/46493859_Implied_volatility_in_oil_markets

    dc = Actual365Fixed()
    today = Date(4, January, 2018)
    rTS = YieldTermStructureHandle(flatRate(today, 0.025, dc))
    qTS = YieldTermStructureHandle(flatRate(today, 0.085, dc))
    spot = QuoteHandle(SimpleQuote(100.0))

    b1 = 0.35
    b2 = 0.03
    b3 = 0.005
    b4 = -0.02
    b5 = -0.005

    strikes = [35, 50, 75, 100, 125, 150, 200, 300]
    maturityMonths = [1, 3, 6, 9, 12, 15, 18, 24]

    calibrationSet = CalibrationSet()

    for i in range(len(strikes)):
        strike = strikes[i]
        for j in range(len(maturityMonths)):
            maturityDate = today + Period(maturityMonths[j], Months)
            t = dc.yearFraction(today, maturityDate)
            fwd = spot.value() * qTS.discount(t) / rTS.discount(t)
            mn = log(fwd / strike) / sqrt(t)
            vol = b1 + b2 * mn + b3 * mn * mn + b4 * t + b5 * mn * t

            if abs(mn) < 3.71 * vol:
                calibrationSet.push_back(
                    CalibrationPair(
                        VanillaOption(
                            PlainVanillaPayoff(
                                Option.Call, strike),
                            EuropeanExercise(maturityDate)),
                        SimpleQuote(vol)))

    data = CalibrationData(spot, rTS, qTS, calibrationSet)
    return data


def arbitrageData():
    dc = Actual365Fixed()
    today = Date(4, January, 2018)
    rTS = YieldTermStructureHandle(flatRate(today, 0.013, dc))
    qTS = YieldTermStructureHandle(flatRate(today, 0.03, dc))
    spot = QuoteHandle(SimpleQuote(100.0))

    strikes = [100, 100, 100, 150]
    maturities = [1, 3, 6, 6]
    vols = [0.25, 0.35, 0.05, 0.35]

    calibrationSet = CalibrationSet()

    for i in range(len(strikes)):
        strike = strikes[i]
        maturityDate = today + Period(maturities[i], Months)
        vol = vols[i]

        calibrationSet.push_back(
            CalibrationPair(
                VanillaOption(
                    PlainVanillaPayoff(
                        Option.Call, strike),
                    EuropeanExercise(maturityDate)),
                SimpleQuote(vol)))
    data = CalibrationData(spot, rTS, qTS, calibrationSet)
    return data


def sabrData():
    dc = Actual365Fixed()
    today = Date(4, January, 2018)

    alpha = 0.15
    beta = 0.8
    nu = 0.5
    rho = -0.48
    forward = 0.03
    maturityInYears = 20

    maturityDate = today + Period(maturityInYears, Years)
    maturity = dc.yearFraction(today, maturityDate)

    calibrationSet = CalibrationSet()
    strikes = [0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.06]

    for i in range(len(strikes)):
        strike = strikes[i]
        vol = sabrVolatility(
            strike, forward, maturity, alpha, beta, nu, rho)
        calibrationSet.push_back(
            CalibrationPair(
                VanillaOption(
                    PlainVanillaPayoff(Option.Call, strike),
                    EuropeanExercise(maturityDate)),
                SimpleQuote(vol)))

    rTS = YieldTermStructureHandle(flatRate(today, forward, dc))
    qTS = YieldTermStructureHandle(flatRate(today, forward, dc))
    spot = QuoteHandle(SimpleQuote(forward))
    data = CalibrationData(
        spot, rTS, qTS, calibrationSet)
    parameter = DoubleVector()
    for i in [alpha, beta, nu, rho, forward, maturity]:
        parameter.push_back(i)

    return (data, parameter)


class AndreasenHugeVolatilityInterplTest(unittest.TestCase):

    def testAndreasenHugePut(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge example with Put calibration...")
        data = AndreasenHugeExampleData()
        expected = CalibrationResults(
            AndreasenHugeVolatilityInterpl.Put,
            AndreasenHugeVolatilityInterpl.CubicSpline,
            0.0015, 0.00035,
            0.0020, 0.00035)
        self._testAndreasenHugeVolatilityInterpolation(data, expected)

    def testAndreasenHugeCall(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge example with Call calibration...")
        data = AndreasenHugeExampleData()
        expected = CalibrationResults(
            AndreasenHugeVolatilityInterpl.Call,
            AndreasenHugeVolatilityInterpl.CubicSpline,
            0.0015, 0.00035,
            0.0020, 0.00035)
        self._testAndreasenHugeVolatilityInterpolation(data, expected)

    def testAndreasenHugeCallPut(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge example with instantaneous Call and Put calibration...")
        data = AndreasenHugeExampleData()
        expected = CalibrationResults(
            AndreasenHugeVolatilityInterpl.CallPut,
            AndreasenHugeVolatilityInterpl.CubicSpline,
            0.0015, 0.00035,
            0.0020, 0.00035)
        self._testAndreasenHugeVolatilityInterpolation(data, expected)

    def testLinearInterpolation(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge example with linear interpolation...")
        data = AndreasenHugeExampleData()
        expected = CalibrationResults(
            AndreasenHugeVolatilityInterpl.CallPut,
            AndreasenHugeVolatilityInterpl.Linear,
            0.0020, 0.00015,
            0.0040, 0.00035)
        self._testAndreasenHugeVolatilityInterpolation(data, expected)

    def testPiecewiseConstantInterpolation(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge example with piecewise constant interpolation...")
        data = AndreasenHugeExampleData()
        expected = CalibrationResults(
            AndreasenHugeVolatilityInterpl.CallPut,
            AndreasenHugeVolatilityInterpl.PiecewiseConstant,
            0.0025, 0.00025,
            0.0040, 0.00035)
        self._testAndreasenHugeVolatilityInterpolation(data, expected)

    def testTimeDependentInterestRates(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge volatility interpolation with time dependent interest rates and dividend yield...")
        backup = SavedSettings()
        data = AndreasenHugeExampleData()
        dc = data.rTS.dayCounter()
        today = data.rTS.referenceDate()
        Settings.instance().evaluationDate = today
        r = DoubleVector()
        q = DoubleVector()
        for i in [0.0167, 0.023, 0.03234, 0.034, 0.038, 0.042, 0.047, 0.053]:
            r.append(i)
        for i in [0.01, 0.011, 0.013, 0.014, 0.02, 0.025, 0.067, 0.072]:
            q.append(i)
        dates = [
            today,
            today + Period(41, Days),
            today + Period(75, Days), today + Period(165, Days),
            today + Period(256, Days), today + Period(345, Days),
            today + Period(524, Days), today + Period(2190, Days)]

        rTS = YieldTermStructureHandle(ZeroCurve(dates, r, dc))
        qTS = YieldTermStructureHandle(ZeroCurve(dates, q, dc))

        origData = AndreasenHugeExampleData()
        calibrationSet = origData.calibrationSet
        spot = origData.spot
        hestonModel = HestonModel(
            HestonProcess(rTS, qTS, spot, 0.09, 2.0, 0.09, 0.4, -0.75))
        hestonEngine = AnalyticHestonEngine(
            hestonModel,
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.discreteTrapezoid(128))

        calibrationSetCopy = CalibrationSet()
        calibrationSetCopy.reserve(calibrationSet.size())

        for i in range(calibrationSet.size()):
            option = calibrationSet[i][0]
            payoff = as_plain_vanilla_payoff(option.payoff())
            strike = payoff.strike()
            optionType = payoff.optionType()
            t = dc.yearFraction(today, option.exercise().lastDate())
            discount = rTS.discount(t)
            fwd = spot.value() * qTS.discount(t) / discount
            option.setPricingEngine(hestonEngine)
            npv = option.NPV()
            impliedVol = blackFormulaImpliedStdDevLiRS(
                optionType, strike, fwd, npv,
                discount, 0.0, NullReal(), 1.0, 1e-12) / sqrt(t)

            calibrationSetCopy.push_back(
                CalibrationPair(
                    option, SimpleQuote(impliedVol)))

        irData = CalibrationData(spot, rTS, qTS, calibrationSetCopy)
        expected = CalibrationResults(
            AndreasenHugeVolatilityInterpl.CallPut,
            AndreasenHugeVolatilityInterpl.CubicSpline,
            0.0020, 0.0003,
            0.0020, 0.0004)
        self._testAndreasenHugeVolatilityInterpolation(irData, expected)

    def testSingleOptionCalibration(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge volatility interpolation with a single option...")
        backup = SavedSettings()
        dc = Actual365Fixed()
        today = Date(4, January, 2018)
        rTS = YieldTermStructureHandle(flatRate(today, 0.025, dc))
        qTS = YieldTermStructureHandle(flatRate(today, 0.085, dc))
        calibrationSet = CalibrationSet()
        strike = 10.0
        vol = 0.3
        maturity = today + Period(1, Years)
        spot = QuoteHandle(SimpleQuote(strike))
        calibrationSet.push_back(
            CalibrationPair(
                VanillaOption(
                    PlainVanillaPayoff(Option.Call, strike),
                    EuropeanExercise(maturity)),
                SimpleQuote(vol)))

        interpl = [
            AndreasenHugeVolatilityInterpl.Linear,
            AndreasenHugeVolatilityInterpl.CubicSpline,
            AndreasenHugeVolatilityInterpl.PiecewiseConstant]
        calibrationType = [
            AndreasenHugeVolatilityInterpl.Call,
            AndreasenHugeVolatilityInterpl.Put,
            AndreasenHugeVolatilityInterpl.CallPut]

        for i in range(len(interpl)):
            for j in range(len(calibrationType)):
                andreasenHugeVolInterplation = AndreasenHugeVolatilityInterpl(
                    calibrationSet, spot, rTS, qTS,
                    interpl[i], calibrationType[j], 50)
                volatilityAdapter = AndreasenHugeVolatilityAdapter(
                    andreasenHugeVolInterplation)
                calculated = volatilityAdapter.blackVol(maturity, strike)
                expected = vol
                self.assertFalse(
                    abs(calculated - expected) > 1e-4,
                    "Failed to reproduce single option calibration")

    def testArbitrageFree(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge volatility interpolation gives arbitrage free prices...")
        backup = SavedSettings()
        data = [BorovkovaExampleData(), arbitrageData()]

        for i in range(len(data)):
            spot = data[i].spot
            calibrationSet = data[i].calibrationSet
            rTS = data[i].rTS
            qTS = data[i].qTS
            dc = rTS.dayCounter()
            today = rTS.referenceDate()
            andreasenHugeVolInterplation = AndreasenHugeVolatilityInterpl(
                calibrationSet, spot, rTS, qTS,
                AndreasenHugeVolatilityInterpl.CubicSpline,
                AndreasenHugeVolatilityInterpl.CallPut, 5000)
            volatilityAdapter = AndreasenHugeVolatilityAdapter(
                andreasenHugeVolInterplation)

            for m in np.arange(-0.7, 0.7, 0.05):
                for weeks in range(6, 52):
                    maturityDate = today + Period(weeks, Weeks)
                    t = dc.yearFraction(today, maturityDate)
                    fwd = spot.value() * qTS.discount(t) / rTS.discount(t)

                    # J. Gatheral, Arbitrage-free SVI volatility surfaces
                    # http://mfe.baruch.cuny.edu/wp-content/uploads/2013/01/OsakaSVI2012.pdf

                    eps = 0.025
                    k = fwd * exp(m)
                    km = fwd * exp(m - eps)
                    kp = fwd * exp(m + eps)

                    w = volatilityAdapter.blackVariance(t, k, True)
                    w_p = volatilityAdapter.blackVariance(t, kp, True)
                    w_m = volatilityAdapter.blackVariance(t, km, True)

                    w1 = (w_p - w_m) / (2 * eps)
                    w2 = (w_p + w_m - 2 * w) / (eps * eps)

                    g_k = (1 - m * w1 / (2 * w)) ** 2 - w1 * w1 / 4 * (1 / w + 0.25) + 0.5 * w2

                    self.assertFalse(
                        g_k < 0,
                        "No-arbitrage condition g_k >= 0 failed")

                    deltaT = 1.0 / 365.
                    fwdpt = spot.value() * qTS.discount(t + deltaT) / rTS.discount(t + deltaT)

                    kpt = fwdpt * exp(m)
                    w_pt = volatilityAdapter.blackVariance(t + deltaT, kpt, True)

                    w_t = (w_pt - w) / deltaT

                    self.assertFalse(
                        w_t < -1e-8,
                        "No-arbitrage condition w_t >= 0 failed")

    def testBarrierOptionPricing(self):
        TEST_MESSAGE(
            "Testing Barrier option pricing with Andreasen-Huge local volatility surface...")
        backup = SavedSettings()
        dc = Actual365Fixed()
        today = Date(4, January, 2018)
        rTS = YieldTermStructureHandle(flatRate(today, 0.01, dc))
        qTS = YieldTermStructureHandle(flatRate(today, 0.03, dc))
        spot = QuoteHandle(SimpleQuote(100.0))

        hestonModel = HestonModel(
            HestonProcess(
                rTS, qTS, spot, 0.04, 2.0, 0.04, 0.4, -0.75))
        hestonVol = HestonBlackVolSurface(
            HestonModelHandle(hestonModel))
        dupireLocalVolProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, BlackVolTermStructureHandle(hestonVol))

        strikes = [25, 50, 75, 90, 100, 110, 125, 150, 200, 400]
        maturityMonths = [1, 3, 6, 9, 12]

        calibrationSet = CalibrationSet()

        for i in range(len(strikes)):
            strike = strikes[i]
            for j in range(len(maturityMonths)):
                maturityDate = today + Period(maturityMonths[j], Months)
                t = dc.yearFraction(today, maturityDate)
                vol = hestonVol.blackVol(t, strike)
                mn = log(spot.value() / strike) / sqrt(t)

                if abs(mn) < 3.07 * vol:
                    calibrationSet.push_back(
                        CalibrationPair(
                            VanillaOption(
                                PlainVanillaPayoff(Option.Call, strike),
                                EuropeanExercise(maturityDate)),
                            SimpleQuote(vol)))

        andreasenHugeVolInterplation = AndreasenHugeVolatilityInterpl(
            calibrationSet, spot, rTS, qTS)
        localVolAdapter = AndreasenHugeLocalVolAdapter(
            andreasenHugeVolInterplation)
        andreasenHugeLocalVolProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS,
            BlackVolTermStructureHandle(hestonVol),
            LocalVolTermStructureHandle(localVolAdapter))

        strike = 120.0
        barrier = 80.0
        rebate = 0.0
        maturity = today + Period(1, Years)
        barrierType = Barrier.DownOut

        barrierOption = BarrierOption(
            barrierType, barrier, rebate,
            PlainVanillaPayoff(Option.Put, strike),
            EuropeanExercise(maturity))
        barrierOption.setPricingEngine(
            FdBlackScholesBarrierEngine(
                dupireLocalVolProcess, 50, 100, 0,
                FdmSchemeDesc.Douglas(), True, 0.2))
        dupireNPV = barrierOption.NPV()
        barrierOption.setPricingEngine(
            FdBlackScholesBarrierEngine(
                andreasenHugeLocalVolProcess, 200, 400, 0,
                FdmSchemeDesc.Douglas(), True, 0.25))
        andreasenHugeNPV = barrierOption.NPV()
        tol = 0.15
        diff = abs(andreasenHugeNPV - dupireNPV)
        self.assertFalse(
            diff > tol,
            "failed to reproduce barrier prices with Andreasen-Huge local volatility surface")

    def testPeterAndFabiensExample(self):
        TEST_MESSAGE(
            "Testing Peter's and Fabien's SABR example...")
        backup = SavedSettings()
        sd = sabrData()
        data = sd[0]
        parameter = sd[1]
        andreasenHugeVolInterplation = AndreasenHugeVolatilityInterpl(
            data.calibrationSet, data.spot, data.rTS, data.qTS)
        volAdapter = AndreasenHugeVolatilityAdapter(
            andreasenHugeVolInterplation)

        alpha = parameter[0]
        beta = parameter[1]
        nu = parameter[2]
        rho = parameter[3]
        forward = parameter[4]
        maturity = parameter[5]

        for strike in np.arange(0.02, 0.06, 0.001):
            sabrVol = sabrVolatility(
                strike, forward, maturity, alpha, beta, nu, rho)
            ahVol = volAdapter.blackVol(maturity, strike, True)
            tol = 0.0005
            diff = abs(sabrVol - ahVol)

            self.assertFalse(
                np.isnan(ahVol) or ahVol is None or diff > 0.005,
                "failed to reproduce SABR volatility with Andreasen-Huge interpolation")

    def testDifferentOptimizers(self):
        TEST_MESSAGE(
            "Testing different optimizer for Andreasen-Huge volatility interpolation...")
        data = sabrData()[0]
        optimizationMethods = [
            LevenbergMarquardt(), BFGS(), Simplex(0.2)]

        for i in range(len(optimizationMethods)):
            optimizationMethod = optimizationMethods[i]
            avgError = AndreasenHugeVolatilityInterpl(
                data.calibrationSet,
                data.spot,
                data.rTS, data.qTS,
                AndreasenHugeVolatilityInterpl.CubicSpline,
                AndreasenHugeVolatilityInterpl.Call,
                400,
                NullReal(),
                NullReal(),
                optimizationMethod).calibrationError().third()

            self.assertFalse(
                np.isnan(avgError) or avgError is None or avgError > 0.0001,
                "failed to calibrate Andreasen-Huge volatility interpolation with different optimizera")

    def testMovingReferenceDate(self):
        TEST_MESSAGE(
            "Testing that reference date of adapter surface moves along with evaluation date...")

        backup = SavedSettings()
        today = Date(4, January, 2018)
        Settings.instance().evaluationDate = today
        dc = Actual365Fixed()
        maturity = today + Period(1, Months)
        ts = YieldTermStructureHandle(flatRate(0.04, dc))
        s0 = 100.0
        impliedVol = 0.2
        spot = QuoteHandle(SimpleQuote(s0))
        calibrationSet = CalibrationSet()
        calibrationSet.push_back(
            CalibrationPair(
                VanillaOption(
                    PlainVanillaPayoff(Option.Call, s0),
                    EuropeanExercise(maturity)),
                SimpleQuote(impliedVol)))
        andreasenHugeVolInterplation = AndreasenHugeVolatilityInterpl(
            calibrationSet, spot, ts, ts)
        tol = 1e-8
        volatilityAdapter = AndreasenHugeVolatilityAdapter(
            andreasenHugeVolInterplation, tol)
        localVolAdapter = AndreasenHugeLocalVolAdapter(
            andreasenHugeVolInterplation)

        volRefDate = volatilityAdapter.referenceDate()
        localRefDate = localVolAdapter.referenceDate()

        self.assertFalse(
            volRefDate != today or localRefDate != today,
            "reference dates should match today's date")
        modToday = Date(15, January, 2018)
        Settings.instance().evaluationDate = modToday
        modVolRefDate = volatilityAdapter.referenceDate()
        modLocalRefDate = localVolAdapter.referenceDate()

        self.assertFalse(
            modVolRefDate != modToday or modLocalRefDate != modToday,
            "reference dates should match modified today's date")

        modImpliedVol = volatilityAdapter.blackVol(maturity, s0, True)
        diff = abs(modImpliedVol - impliedVol)

        self.assertFalse(
            diff > 10 * tol,
            "modified implied vol should match direct calculation")

    def testFlatVolCalibration(self):
        TEST_MESSAGE(
            "Testing Andreasen-Huge example with flat volatility surface...")

        backup = SavedSettings()
        ref = Date(1, November, 2019)
        dc = Actual365Fixed()
        Settings.instance().evaluationDate = ref

        expiries = [
            ref + Period(1, Months), ref + Period(3, Months), ref + Period(6, Months),
            ref + Period(9, Months), ref + Period(1, Years), ref + Period(2, Years),
            ref + Period(3, Years), ref + Period(4, Years), ref + Period(5, Years),
            ref + Period(7, Years), ref + Period(10, Years)]
        moneyness = [
            0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]

        spot = QuoteHandle(SimpleQuote(100.0))
        rTS = YieldTermStructureHandle(flatRate(ref, 0.02, dc))
        qTS = YieldTermStructureHandle(flatRate(ref, 0.0, dc))
        vol = SimpleQuote(0.18)
        calibrationSet = CalibrationSet()

        for i in range(len(expiries)):
            expiry = expiries[i]
            exercise = EuropeanExercise(expiry)
            t = rTS.timeFromReference(expiry)
            fwd = spot.value() / rTS.discount(t) * qTS.discount(t)
            for j in range(len(moneyness)):
                strike = fwd * moneyness[j]
                mn = log(fwd / strike) / sqrt(t)

                if abs(mn) < 3.72 * vol.value():
                    option = VanillaOption(
                        PlainVanillaPayoff(
                            Option.Call if strike > fwd else Option.Put,
                            strike),
                        exercise)
                    calibrationSet.push_back(CalibrationPair(option, vol))

        flatVolData = CalibrationData(
            spot, rTS, qTS, calibrationSet)
        expected = CalibrationResults(
            AndreasenHugeVolatilityInterpl.Put,
            AndreasenHugeVolatilityInterpl.CubicSpline,
            1e-10, 1e-10,
            0.0006, 0.0002)

        self._testAndreasenHugeVolatilityInterpolation(
            flatVolData, expected)

    def _testAndreasenHugeVolatilityInterpolation(self,
                                                  data,
                                                  expected):
        backup = SavedSettings()
        rTS = data.rTS
        qTS = data.qTS
        dc = rTS.dayCounter()
        today = rTS.referenceDate()
        Settings.instance().evaluationDate = today
        spot = data.spot
        calibrationSet = data.calibrationSet

        andreasenHugeVolInterplation = AndreasenHugeVolatilityInterpl(
            calibrationSet, spot,
            rTS, qTS,
            expected.interpolationType,
            expected.calibrationType)

        error = andreasenHugeVolInterplation.calibrationError()
        maxError = error.second()
        avgError = error.third()

        self.assertFalse(
            maxError > expected.maxError or avgError > expected.avgError,
            'Failed to reproduce calibration error')

        volatilityAdapter = AndreasenHugeVolatilityAdapter(
            andreasenHugeVolInterplation, 1e-12)

        localVolAdapter = AndreasenHugeLocalVolAdapter(
            andreasenHugeVolInterplation)

        localVolProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS,
            BlackVolTermStructureHandle(volatilityAdapter),
            LocalVolTermStructureHandle(localVolAdapter))

        lvAvgError = 0.0
        lvMaxError = 0.0

        n = 0
        for i in range(calibrationSet.size()):
            option = calibrationSet[i][0]
            payoff = as_plain_vanilla_payoff(option.payoff())
            strike = payoff.strike()
            optionType = payoff.optionType()
            t = dc.yearFraction(today, option.exercise().lastDate())
            expectedVol = calibrationSet[i][1].value()
            calculatedVol = volatilityAdapter.blackVol(t, strike, True)
            diffVol = abs(expectedVol - calculatedVol)
            tol = max(1e-10, 1.01 * maxError)

            self.assertFalse(
                diffVol > tol,
                "Failed to reproduce calibration option price")

            fdEngine = FdBlackScholesVanillaEngine(
                localVolProcess, max(30, int(100.0 * t)),
                200, 0, FdmSchemeDesc.Douglas(), True)

            option.setPricingEngine(fdEngine)
            discount = rTS.discount(t)
            fwd = spot.value() * qTS.discount(t) / discount
            lvImpliedVol = blackFormulaImpliedStdDevLiRS(
                optionType, strike, fwd, option.NPV(),
                discount, 0.0, NullReal(), 1.0, 1e-12) / sqrt(t)
            lvError = abs(lvImpliedVol - expectedVol)
            lvMaxError = max(lvError, lvMaxError)
            lvAvgError = (n * lvAvgError + lvError) / (n + 1)
            n += 1

        self.assertFalse(
            lvMaxError > expected.lvMaxError or avgError > expected.lvAvgError,
            "Failed to reproduce local volatility calibration error")
