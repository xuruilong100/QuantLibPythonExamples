import unittest
from math import exp, sqrt, log10, log

import numpy as np
from QuantLib import *

from utilities import *


class HestonParameter(object):
    def __init__(self,
                 v0,
                 kappa,
                 theta,
                 sigma,
                 rho):
        self.v0 = v0
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho


class HestonProcessDiscretizationDesc(object):
    def __init__(self,
                 discretization,
                 nSteps,
                 name):
        self.discretization = discretization
        self.nSteps = nSteps
        self.name = name


class CalibrationMarketData(object):
    def __init__(self,
                 s0,
                 riskFreeTS,
                 dividendYield,
                 options):
        self.s0 = s0
        self.riskFreeTS = riskFreeTS
        self.dividendYield = dividendYield
        self.options = options


def getDAXCalibrationMarketData():
    settlementDate = Settings.instance().evaluationDate

    dayCounter = Actual365Fixed()
    calendar = TARGET()

    t = [13, 41, 75, 165, 256, 345, 524, 703]
    r = [0.0357, 0.0349, 0.0341, 0.0355, 0.0359, 0.0368, 0.0386, 0.0401]

    dates = DateVector()
    rates = DoubleVector()
    dates.push_back(settlementDate)
    rates.push_back(0.0357)

    for i in range(8):
        dates.push_back(settlementDate + Period(t[i], Days))
        rates.push_back(r[i])

    riskFreeTS = YieldTermStructureHandle(
        ZeroCurve(dates, rates, dayCounter))
    dividendYield = YieldTermStructureHandle(
        flatRate(settlementDate, 0.0, dayCounter))

    v = [0.6625, 0.4875, 0.4204, 0.3667, 0.3431, 0.3267, 0.3121, 0.3121,
         0.6007, 0.4543, 0.3967, 0.3511, 0.3279, 0.3154, 0.2984, 0.2921,
         0.5084, 0.4221, 0.3718, 0.3327, 0.3155, 0.3027, 0.2919, 0.2889,
         0.4541, 0.3869, 0.3492, 0.3149, 0.2963, 0.2926, 0.2819, 0.2800,
         0.4060, 0.3607, 0.3330, 0.2999, 0.2887, 0.2811, 0.2751, 0.2775,
         0.3726, 0.3396, 0.3108, 0.2781, 0.2788, 0.2722, 0.2661, 0.2686,
         0.3550, 0.3277, 0.3012, 0.2781, 0.2781, 0.2661, 0.2661, 0.2681,
         0.3428, 0.3209, 0.2958, 0.2740, 0.2688, 0.2627, 0.2580, 0.2620,
         0.3302, 0.3062, 0.2799, 0.2631, 0.2573, 0.2533, 0.2504, 0.2544,
         0.3343, 0.2959, 0.2705, 0.2540, 0.2504, 0.2464, 0.2448, 0.2462,
         0.3460, 0.2845, 0.2624, 0.2463, 0.2425, 0.2385, 0.2373, 0.2422,
         0.3857, 0.2860, 0.2578, 0.2399, 0.2357, 0.2327, 0.2312, 0.2351,
         0.3976, 0.2860, 0.2607, 0.2356, 0.2297, 0.2268, 0.2241, 0.2320]

    s0 = QuoteHandle(SimpleQuote(4468.17))
    strike = [
        3400, 3600, 3800, 4000, 4200, 4400,
        4500, 4600, 4800, 5000, 5200, 5400, 5600]
    options = CalibrationHelperVector()

    for s in range(13):
        for m in range(8):
            vol = QuoteHandle(
                SimpleQuote(v[s * 8 + m]))
            maturity = Period(
                int((t[m] + 3) / 7.0), Weeks)
            options.push_back(
                HestonModelHelper(
                    maturity, calendar,
                    s0, strike[s], vol,
                    riskFreeTS, dividendYield,
                    BlackCalibrationHelper.ImpliedVolError))

    marketData = CalibrationMarketData(
        s0, riskFreeTS, dividendYield, options)

    return marketData


class HestonModelTest(unittest.TestCase):

    def _reportOnIntegrationMethodTest(self,
                                       option,
                                       model,
                                       integration,
                                       formula,
                                       isAdaptive,
                                       expected,
                                       tol,
                                       valuations,
                                       method):

        if integration.isAdaptiveIntegration() != isAdaptive:
            self.fail(
                method + " is not an adaptive integration routine")

        engine = AnalyticHestonEngine(
            model, formula, integration, 1e-9)

        option.setPricingEngine(engine)
        calculated = option.NPV()

        error = abs(calculated - expected)

        self.assertFalse(error > tol)
        self.assertFalse(
            valuations != NullSize() and
            valuations != engine.numberOfEvaluations())

    def testBlackCalibration(self):
        TEST_MESSAGE(
            "Testing Heston model calibration using a flat volatility surface...")

        backup = SavedSettings()

        today = knownGoodDefault
        Settings.instance().evaluationDate = today

        dayCounter = Actual360()
        calendar = NullCalendar()

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.04, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.50, dayCounter))

        optionMaturities = PeriodVector()
        optionMaturities.push_back(Period(1, Months))
        optionMaturities.push_back(Period(2, Months))
        optionMaturities.push_back(Period(3, Months))
        optionMaturities.push_back(Period(6, Months))
        optionMaturities.push_back(Period(9, Months))
        optionMaturities.push_back(Period(1, Years))
        optionMaturities.push_back(Period(2, Years))

        options = CalibrationHelperVector()
        s0 = QuoteHandle(SimpleQuote(1.0))
        vol = QuoteHandle(SimpleQuote(0.1))
        volatility = vol.value()

        for i in range(len(optionMaturities)):
            for moneyness in np.arange(-1.0, 2.0, 1.0):
                tau = dayCounter.yearFraction(
                    riskFreeTS.referenceDate(),
                    calendar.advance(
                        riskFreeTS.referenceDate(),
                        optionMaturities[i]))
                fwdPrice = s0.value() * dividendTS.discount(tau) / riskFreeTS.discount(tau)
                strikePrice = fwdPrice * exp(-moneyness * volatility * sqrt(tau))

                options.push_back(
                    HestonModelHelper(
                        optionMaturities[i], calendar,
                        s0, strikePrice, vol,
                        riskFreeTS, dividendTS))

        for sigma in np.arange(0.1, 0.7, 0.2):
            v0 = 0.01
            kappa = 0.2
            theta = 0.02
            rho = -0.75

            process = HestonProcess(
                riskFreeTS, dividendTS,
                s0, v0, kappa, theta,
                sigma, rho)

            model = HestonModel(process)
            engine = AnalyticHestonEngine(model, 96)

            for i in range(len(options)):
                as_black_helper(options[i]).setPricingEngine(engine)

            om = LevenbergMarquardt(1e-8, 1e-8, 1e-8)
            model.calibrate(
                options,
                om,
                EndCriteria(
                    400, 40, 1.0e-8, 1.0e-8, 1.0e-8))

            tolerance = 3.0e-3

            self.assertFalse(
                model.sigma() > tolerance)
            self.assertFalse(
                abs(model.kappa() * (model.theta() - volatility * volatility)) > tolerance)
            self.assertFalse(
                abs(model.v0() - volatility * volatility) > tolerance)

    def testDAXCalibration(self):
        TEST_MESSAGE(
            "Testing Heston model calibration using DAX volatility data...")

        backup = SavedSettings()
        settlementDate = Date(5, July, 2002)
        Settings.instance().evaluationDate = settlementDate
        marketData = getDAXCalibrationMarketData()

        riskFreeTS = marketData.riskFreeTS
        dividendTS = marketData.dividendYield
        s0 = marketData.s0

        options = marketData.options

        v0 = 0.1
        kappa = 1.0
        theta = 0.1
        sigma = 0.5
        rho = -0.5

        process = HestonProcess(
            riskFreeTS, dividendTS, s0, v0, kappa, theta, sigma, rho)

        model = HestonModel(process)

        engines = [
            AnalyticHestonEngine(model, 64),
            COSHestonEngine(model, 12, 75),
            ExponentialFittingHestonEngine(model)]

        params = model.params()

        for j in range(len(engines)):
            model.setParams(params)
            for i in range(len(options)):
                as_black_helper(options[i]).setPricingEngine(engines[j])
            om = LevenbergMarquardt(1e-8, 1e-8, 1e-8)
            model.calibrate(
                options, om,
                EndCriteria(400, 40, 1.0e-8, 1.0e-8, 1.0e-8))

            sse = 0
            for i in range(13 * 8):
                diff = options[i].calibrationError() * 100.0
                sse += diff * diff

            expected = 177.2

            self.assertFalse(abs(sse - expected) > 1.0)

    def testAnalyticVsBlack(self):
        TEST_MESSAGE(
            "Testing analytic Heston engine against Black formula...")

        backup = SavedSettings()
        settlementDate = knownGoodDefault
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = settlementDate + Period(6, Months)

        payoff = PlainVanillaPayoff(Option.Put, 30)
        exercise = EuropeanExercise(exerciseDate)

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.1, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.04, dayCounter))

        s0 = QuoteHandle(SimpleQuote(32.0))
        v0 = 0.05
        kappa = 5.0
        theta = 0.05
        sigma = 1.0e-4
        rho = 0.0

        process = HestonProcess(
            riskFreeTS, dividendTS, s0, v0, kappa, theta, sigma, rho)

        option = VanillaOption(payoff, exercise)
        engine = AnalyticHestonEngine(
            HestonModel(process), 144)

        option.setPricingEngine(engine)
        calculated = option.NPV()

        yearFraction = dayCounter.yearFraction(
            settlementDate, exerciseDate)
        forwardPrice = 32 * exp((0.1 - 0.04) * yearFraction)
        expected = blackFormula(
            payoff.optionType(),
            payoff.strike(),
            forwardPrice,
            sqrt(0.05 * yearFraction)) * exp(-0.1 * yearFraction)

        error = abs(calculated - expected)
        tolerance = 2.0e-7

        self.assertFalse(error > tolerance)

        engine = FdHestonVanillaEngine(
            HestonModel(process),
            200, 200, 100)
        option.setPricingEngine(engine)

        calculated = option.NPV()
        error = abs(calculated - expected)
        tolerance = 1.0e-3

        self.assertFalse(error > tolerance)

    def testAnalyticVsCached(self):
        TEST_MESSAGE(
            "Testing analytic Heston engine against cached values...")

        backup = SavedSettings()
        settlementDate = Date(27, December, 2004)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = Date(28, March, 2005)

        payoff = PlainVanillaPayoff(Option.Call, 1.05)
        exercise = EuropeanExercise(exerciseDate)

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.0225, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.02, dayCounter))

        s0 = QuoteHandle(SimpleQuote(1.0))
        v0 = 0.1
        kappa = 3.16
        theta = 0.09
        sigma = 0.4
        rho = -0.2

        process = HestonProcess(
            riskFreeTS, dividendTS, s0, v0, kappa, theta, sigma, rho)

        option = VanillaOption(payoff, exercise)
        engine = AnalyticHestonEngine(
            HestonModel(process), 64)

        option.setPricingEngine(engine)
        expected1 = 0.0404774515
        calculated1 = option.NPV()
        tolerance = 1.0e-8

        self.assertFalse(abs(calculated1 - expected1) > tolerance)

        K = [0.9, 1.0, 1.1]
        expected2 = [0.1330371, 0.0641016, 0.0270645]
        calculated2 = []
        for i in range(6):
            exerciseDate = Date(8 + int(i / 3), September, 2005)
            payoff = PlainVanillaPayoff(Option.Call, K[i % 3])
            exercise = EuropeanExercise(exerciseDate)

            riskFreeTS = YieldTermStructureHandle(
                flatRate(0.05, dayCounter))
            dividendTS = YieldTermStructureHandle(
                flatRate(0.02, dayCounter))
            s = riskFreeTS.discount(0.7) / dividendTS.discount(0.7)
            s0 = QuoteHandle(SimpleQuote(s))
            process = HestonProcess(
                riskFreeTS, dividendTS, s0, 0.09, 1.2, 0.08, 1.8, -0.45)
            option = VanillaOption(payoff, exercise)
            engine = AnalyticHestonEngine(
                HestonModel(process))
            option.setPricingEngine(engine)
            calculated2.append(option.NPV())

        t1 = dayCounter.yearFraction(settlementDate, Date(8, September, 2005))
        t2 = dayCounter.yearFraction(settlementDate, Date(9, September, 2005))

        for i in range(3):
            interpolated = calculated2[i] + (calculated2[i + 3] - calculated2[i]) / (t2 - t1) * (0.7 - t1)
            self.assertFalse(abs(interpolated - expected2[i]) > 100 * tolerance)

    def testKahlJaeckelCase(self):
        TEST_MESSAGE(
            "Testing MC and FD Heston engines for the Kahl-Jaeckel example...")

        backup = SavedSettings()
        settlementDate = Date(30, March, 2007)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = Date(30, March, 2017)

        payoff = PlainVanillaPayoff(Option.Call, 200)
        exercise = EuropeanExercise(exerciseDate)
        option = VanillaOption(payoff, exercise)
        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.0, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.0, dayCounter))

        s0 = QuoteHandle(SimpleQuote(100.0))
        v0 = 0.16
        theta = v0
        kappa = 1.0
        sigma = 2.0
        rho = -0.8

        descriptions = [
            HestonProcessDiscretizationDesc(
                HestonProcess.NonCentralChiSquareVariance,
                10, "NonCentralChiSquareVariance"),
            HestonProcessDiscretizationDesc(
                HestonProcess.QuadraticExponentialMartingale,
                100, "QuadraticExponentialMartingale")]

        tolerance = 0.2
        expected = 4.95212

        for i in range(len(descriptions)):
            process = HestonProcess(
                riskFreeTS, dividendTS, s0, v0,
                kappa, theta, sigma, rho,
                descriptions[i].discretization)

            engine = MakeMCPREuropeanHestonEngine(process)
            engine.withSteps(descriptions[i].nSteps)
            engine.withAntitheticVariate()
            engine.withAbsoluteTolerance(tolerance)
            engine.withSeed(1234)
            engine = engine.makeEngine()

            option.setPricingEngine(engine)

            calculated = option.NPV()
            errorEstimate = option.errorEstimate()

            self.assertFalse(abs(calculated - expected) > 2.34 * errorEstimate)
            self.assertFalse(errorEstimate > tolerance)

        engine = MakeMCLDEuropeanHestonEngine(
            HestonProcess(
                riskFreeTS, dividendTS, s0, v0,
                kappa, theta, sigma, rho,
                HestonProcess.BroadieKayaExactSchemeLaguerre))
        engine.withSteps(1)
        engine.withSamples(1023)
        engine = engine.makeEngine()

        option.setPricingEngine(engine)

        calculated = option.NPV()
        self.assertFalse(
            abs(calculated - expected) > 0.5 * tolerance)

        hestonModel = HestonModel(
            HestonProcess(
                riskFreeTS, dividendTS, s0, v0,
                kappa, theta, sigma, rho))
        option.setPricingEngine(
            FdHestonVanillaEngine(
                hestonModel, 200, 401, 101))
        calculated = option.NPV()
        error = abs(calculated - expected)
        self.assertFalse(error > 5.0e-2)

        option.setPricingEngine(
            AnalyticHestonEngine(hestonModel, 1e-6, 1000))
        calculated = option.NPV()
        error = abs(calculated - expected)
        self.assertFalse(error > 0.00002)

        option.setPricingEngine(
            COSHestonEngine(hestonModel, 16, 400))
        calculated = option.NPV()
        error = abs(calculated - expected)
        self.assertFalse(error > 0.00002)

        option.setPricingEngine(
            ExponentialFittingHestonEngine(hestonModel))
        calculated = option.NPV()
        error = abs(calculated - expected)
        self.assertFalse(error > 0.00002)

    def testMcVsCached(self):
        TEST_MESSAGE(
            "Testing Monte Carlo Heston engine against cached values...")

        backup = SavedSettings()
        settlementDate = Date(27, December, 2004)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = Date(28, March, 2005)

        payoff = PlainVanillaPayoff(Option.Put, 1.05)
        exercise = EuropeanExercise(exerciseDate)

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.7, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.4, dayCounter))

        s0 = QuoteHandle(SimpleQuote(1.05))
        process = HestonProcess(
            riskFreeTS, dividendTS, s0,
            0.3, 1.16, 0.2, 0.8, 0.8,
            HestonProcess.QuadraticExponentialMartingale)

        option = VanillaOption(payoff, exercise)

        engine = MakeMCPREuropeanHestonEngine(process)
        engine.withStepsPerYear(11)
        engine.withAntitheticVariate()
        engine.withSamples(50000)
        engine.withSeed(1234)
        engine = engine.makeEngine()

        option.setPricingEngine(engine)

        expected = 0.0632851308977151
        calculated = option.NPV()
        errorEstimate = option.errorEstimate()
        tolerance = 7.5e-4

        self.assertFalse(
            abs(calculated - expected) > 2.34 * errorEstimate)
        self.assertFalse(
            errorEstimate > tolerance)

    def testFdBarrierVsCached(self):
        TEST_MESSAGE(
            "Testing FD barrier Heston engine against cached values...")

        backup = SavedSettings()
        dc = Actual360()
        today = knownGoodDefault
        Settings.instance().evaluationDate = today

        s0 = QuoteHandle(SimpleQuote(100.0))
        rTS = YieldTermStructureHandle(
            flatRate(0.08, dc))
        qTS = YieldTermStructureHandle(
            flatRate(0.04, dc))

        exDate = today + Period(int(0.5 * 360 + 0.5), Days)
        exercise = EuropeanExercise(exDate)
        payoff = PlainVanillaPayoff(Option.Call, 90.0)
        process = HestonProcess(
            rTS, qTS, s0, 0.25 * 0.25, 1.0, 0.25 * 0.25, 0.001, 0.0)
        engine = FdHestonBarrierEngine(
            HestonModel(process),
            200, 400, 100)

        option = BarrierOption(
            Barrier.DownOut, 95.0, 3.0, payoff, exercise)
        option.setPricingEngine(engine)

        calculated = option.NPV()
        expected = 9.0246
        error = abs(calculated - expected)
        self.assertFalse(error > 1.0e-3)

        option = BarrierOption(
            Barrier.DownIn, 95.0, 3.0, payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.NPV()
        expected = 7.7627
        error = abs(calculated - expected)
        self.assertFalse(error > 1.0e-3)

    def testFdVanillaVsCached(self):
        TEST_MESSAGE(
            "Testing FD vanilla Heston engine against cached values...")

        backup = SavedSettings()
        settlementDate = Date(27, December, 2004)
        Settings.instance().evaluationDate = settlementDate

        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = Date(28, March, 2005)

        payoff = PlainVanillaPayoff(Option.Put, 1.05)
        exercise = EuropeanExercise(exerciseDate)

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.7, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.4, dayCounter))

        s0 = QuoteHandle(SimpleQuote(1.05))

        option = VanillaOption(payoff, exercise)

        process = HestonProcess(
            riskFreeTS, dividendTS, s0,
            0.3, 1.16, 0.2, 0.8, 0.8)

        engine = MakeFdHestonVanillaEngine(
            HestonModel(process))
        engine.withTGrid(100)
        engine.withXGrid(200)
        engine.withVGrid(100)
        engine = engine.makeEngine()
        option.setPricingEngine(engine)

        expected = 0.06325
        calculated = option.NPV()
        error = abs(calculated - expected)
        tolerance = 1.0e-4
        self.assertFalse(error > tolerance)

        TEST_MESSAGE(
            "Testing FD vanilla Heston engine for discrete dividends...")

        payoff = PlainVanillaPayoff(Option.Call, 95.0)
        s0 = QuoteHandle(SimpleQuote(100.0))

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.05, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.0, dayCounter))

        exerciseDate = Date(28, March, 2006)
        exercise = EuropeanExercise(exerciseDate)

        dividendDates = DateVector()
        dividends = DoubleVector()

        d = settlementDate + Period(3, Months)

        while d < exercise.lastDate():
            dividendDates.push_back(d)
            dividends.push_back(1.0)
            d += Period(6, Months)

        divOption = DividendVanillaOption(
            payoff, exercise,
            dividendDates, dividends)
        process = HestonProcess(
            riskFreeTS, dividendTS, s0,
            0.04, 1.0, 0.04, 0.001, 0.0)
        engine = MakeFdHestonVanillaEngine(HestonModel(process))
        engine.withTGrid(200)
        engine.withXGrid(400)
        engine.withVGrid(100)
        engine = engine.makeEngine()

        divOption.setPricingEngine(engine)
        calculated = divOption.NPV()

        expected = 12.946
        error = abs(calculated - expected)
        tolerance = 5.0e-3
        self.assertFalse(error > tolerance)

        TEST_MESSAGE(
            "Testing FD vanilla Heston engine for american exercise...")

        dividendTS = YieldTermStructureHandle(
            flatRate(0.03, dayCounter))
        process = HestonProcess(
            riskFreeTS, dividendTS, s0,
            0.04, 1.0, 0.04, 0.001, 0.0)
        payoff = PlainVanillaPayoff(Option.Put, 95.0)
        exercise = AmericanExercise(
            settlementDate, exerciseDate)
        option = VanillaOption(payoff, exercise)
        engine = MakeFdHestonVanillaEngine(HestonModel(process))
        engine.withTGrid(200)
        engine.withXGrid(400)
        engine.withVGrid(100)
        engine = engine.makeEngine()
        option.setPricingEngine(engine)
        calculated = option.NPV()

        volTS = BlackVolTermStructureHandle(
            flatVol(
                settlementDate, 0.2, dayCounter))
        ref_process = BlackScholesMertonProcess(
            s0, dividendTS, riskFreeTS, volTS)
        ref_engine = FdBlackScholesVanillaEngine(
            ref_process, 200, 400)

        option.setPricingEngine(ref_engine)
        expected = option.NPV()

        error = abs(calculated - expected)
        tolerance = 1.0e-3

        self.assertFalse(error > tolerance)

    def testDifferentIntegrals(self):
        TEST_MESSAGE(
            "Testing different numerical Heston integration algorithms...")

        backup = SavedSettings()
        settlementDate = Date(27, December, 2004)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.05, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.03, dayCounter))
        strikes = [0.5, 0.7, 1.0, 1.25, 1.5, 2.0]
        maturities = [1, 2, 3, 12, 60, 120, 360]
        types = [Option.Put, Option.Call]

        equityfx = HestonParameter(0.07, 2.0, 0.04, 0.55, -0.8)
        highCorr = HestonParameter(0.07, 1.0, 0.04, 0.55, 0.995)
        lowVolOfVol = HestonParameter(0.07, 1.0, 0.04, 0.025, -0.75)
        highVolOfVol = HestonParameter(0.07, 1.0, 0.04, 5.0, -0.75)
        kappaEqSigRho = HestonParameter(0.07, 0.4, 0.04, 0.5, 0.8)

        params = [
            equityfx,
            highCorr,
            lowVolOfVol,
            highVolOfVol,
            kappaEqSigRho]

        tol = [1e-3, 1e-3, 0.2, 0.01, 1e-3]
        idx = 0
        for p in params:
            s0 = QuoteHandle(SimpleQuote(1.0))
            process = HestonProcess(
                riskFreeTS, dividendTS,
                s0, p.v0, p.kappa,
                p.theta, p.sigma, p.rho)
            model = HestonModel(process)
            lobattoEngine = AnalyticHestonEngine(
                model, 1e-10, 1000000)
            laguerreEngine = AnalyticHestonEngine(model, 128)
            legendreEngine = AnalyticHestonEngine(
                model, AnalyticHestonEngine.Gatheral,
                AnalyticHestonEngineIntegration.gaussLegendre(512))
            chebyshevEngine = AnalyticHestonEngine(
                model, AnalyticHestonEngine.Gatheral,
                AnalyticHestonEngineIntegration.gaussChebyshev(512))
            chebyshev2ndEngine = AnalyticHestonEngine(
                model, AnalyticHestonEngine.Gatheral,
                AnalyticHestonEngineIntegration.gaussChebyshev2nd(512))

            maxLegendreDiff = 0.0
            maxChebyshevDiff = 0.0
            maxChebyshev2ndDiff = 0.0
            maxLaguerreDiff = 0.0

            for i in range(len(maturities)):
                exercise = EuropeanExercise(
                    settlementDate + Period(maturities[i], Months))
                for j in range(len(strikes)):
                    for k in range(len(types)):
                        payoff = PlainVanillaPayoff(types[k], strikes[j])
                        option = VanillaOption(payoff, exercise)
                        option.setPricingEngine(lobattoEngine)
                        lobattoNPV = option.NPV()

                        option.setPricingEngine(laguerreEngine)
                        laguerre = option.NPV()

                        option.setPricingEngine(legendreEngine)
                        legendre = option.NPV()

                        option.setPricingEngine(chebyshevEngine)
                        chebyshev = option.NPV()

                        option.setPricingEngine(chebyshev2ndEngine)
                        chebyshev2nd = option.NPV()

                        maxLaguerreDiff = max(
                            maxLaguerreDiff, abs(lobattoNPV - laguerre))
                        maxLegendreDiff = max(
                            maxLegendreDiff, abs(lobattoNPV - legendre))
                        maxChebyshevDiff = max(
                            maxChebyshevDiff, abs(lobattoNPV - chebyshev))
                        maxChebyshev2ndDiff = max(
                            maxChebyshev2ndDiff, abs(lobattoNPV - chebyshev2nd))

            maxDiff = max(
                max(max(maxLaguerreDiff, maxLegendreDiff),
                    maxChebyshevDiff),
                maxChebyshev2ndDiff)
            tr = tol[idx]
            idx += 1
            self.assertFalse(maxDiff > tr)

    def testMultipleStrikesEngine(self):
        TEST_MESSAGE(
            "Testing multiple-strikes FD Heston engine...")

        backup = SavedSettings()
        settlementDate = Date(27, December, 2004)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = Date(28, March, 2005)

        exercise = EuropeanExercise(exerciseDate)

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.06, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.02, dayCounter))

        s0 = QuoteHandle(SimpleQuote(1.05))

        process = HestonProcess(
            riskFreeTS, dividendTS, s0, 0.16,
            2.5, 0.09, 0.8, -0.8)

        model = HestonModel(process)
        strikes = DoubleVector()
        strikes.push_back(1.0)
        strikes.push_back(0.5)
        strikes.push_back(0.75)
        strikes.push_back(1.5)
        strikes.push_back(2.0)

        singleStrikeEngine = FdHestonVanillaEngine(model, 20, 400, 50)
        multiStrikeEngine = FdHestonVanillaEngine(model, 20, 400, 50)
        multiStrikeEngine.enableMultipleStrikesCaching(strikes)

        relTol = 5e-3

        for i in range(len(strikes)):
            payoff = PlainVanillaPayoff(Option.Put, strikes[i])
            aOption = VanillaOption(payoff, exercise)
            aOption.setPricingEngine(multiStrikeEngine)

            npvCalculated = aOption.NPV()
            deltaCalculated = aOption.delta()
            gammaCalculated = aOption.gamma()
            thetaCalculated = aOption.theta()

            aOption.setPricingEngine(singleStrikeEngine)
            npvExpected = aOption.NPV()
            deltaExpected = aOption.delta()
            gammaExpected = aOption.gamma()
            thetaExpected = aOption.theta()

            self.assertFalse(
                abs(npvCalculated - npvExpected) / npvExpected > relTol)
            self.assertFalse(
                abs(deltaCalculated - deltaExpected) / deltaExpected > relTol)
            self.assertFalse(
                abs(gammaCalculated - gammaExpected) / gammaExpected > relTol)
            self.assertFalse(
                abs(thetaCalculated - thetaExpected) / thetaExpected > relTol)

    def testAnalyticPiecewiseTimeDependent(self):
        TEST_MESSAGE(
            "Testing analytic piecewise time dependent Heston prices...")

        backup = SavedSettings()
        settlementDate = Date(27, December, 2004)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = Date(28, March, 2005)

        payoff = PlainVanillaPayoff(Option.Call, 1.0)
        exercise = EuropeanExercise(exerciseDate)

        dates = DateVector()
        dates.push_back(settlementDate)
        dates.push_back(Date(1, January, 2007))

        irates = DoubleVector()
        irates.push_back(0.0)
        irates.push_back(0.2)

        riskFreeTS = YieldTermStructureHandle(
            ZeroCurve(dates, irates, dayCounter))

        qrates = DoubleVector()
        qrates.push_back(0.0)
        qrates.push_back(0.3)

        dividendTS = YieldTermStructureHandle(
            ZeroCurve(dates, qrates, dayCounter))

        v0 = 0.1
        s0 = QuoteHandle(SimpleQuote(1.0))

        theta = ConstantParameter(0.09, PositiveConstraint())
        kappa = ConstantParameter(3.16, PositiveConstraint())
        sigma = ConstantParameter(4.40, PositiveConstraint())
        rho = ConstantParameter(-0.8, BoundaryConstraint(-1.0, 1.0))

        model = PiecewiseTimeDependentHestonModel(
            riskFreeTS, dividendTS,
            s0, v0, theta, kappa,
            sigma, rho, TimeGrid(20.0, 2))

        option = VanillaOption(payoff, exercise)
        hestonProcess = HestonProcess(
            riskFreeTS, dividendTS, s0, v0,
            kappa(0.0), theta(0.0), sigma(0.0), rho(0.0))
        hestonModel = HestonModel(hestonProcess)
        option.setPricingEngine(
            AnalyticHestonEngine(hestonModel))

        expected = option.NPV()
        option.setPricingEngine(
            AnalyticPTDHestonEngine(model))

        calculatedGatheral = option.NPV()
        self.assertFalse(
            abs(calculatedGatheral - expected) > 1e-12)

        option.setPricingEngine(
            AnalyticPTDHestonEngine(
                model,
                AnalyticPTDHestonEngine.AndersenPiterbarg,
                AnalyticHestonEngineIntegration.gaussLaguerre(164)))
        calculatedAndersenPiterbarg = option.NPV()
        self.assertFalse(
            abs(calculatedAndersenPiterbarg - expected) > 1e-8)

    def testDAXCalibrationOfTimeDependentModel(self):
        TEST_MESSAGE(
            "Testing time-dependent Heston model calibration...")

        backup = SavedSettings()
        settlementDate = Date(5, July, 2002)
        Settings.instance().evaluationDate = settlementDate
        marketData = getDAXCalibrationMarketData()

        riskFreeTS = marketData.riskFreeTS
        dividendTS = marketData.dividendYield
        s0 = marketData.s0

        options = marketData.options

        modelTimes = DoubleVector()
        modelTimes.push_back(0.25)
        modelTimes.push_back(10.0)
        modelGrid = TimeGrid(modelTimes)

        v0 = 0.1
        sigma = ConstantParameter(0.5, PositiveConstraint())
        theta = ConstantParameter(0.1, PositiveConstraint())
        rho = ConstantParameter(-0.5, BoundaryConstraint(-1.0, 1.0))

        pTimes = DoubleVector(1, 0.25)
        kappa = PiecewiseConstantParameter(pTimes, PositiveConstraint())

        for i in range(len(pTimes) + 1):
            kappa.setParam(i, 10.0)

        model = PiecewiseTimeDependentHestonModel(
            riskFreeTS, dividendTS,
            s0, v0, theta, kappa,
            sigma, rho, modelGrid)

        engines = [
            AnalyticPTDHestonEngine(model),
            AnalyticPTDHestonEngine(
                model,
                AnalyticPTDHestonEngine.AndersenPiterbarg,
                AnalyticHestonEngineIntegration.gaussLaguerre(64)),
            AnalyticPTDHestonEngine(
                model,
                AnalyticPTDHestonEngine.AndersenPiterbarg,
                AnalyticHestonEngineIntegration.discreteTrapezoid(72))]

        for j in range(len(engines)):
            engine = engines[j]
            for i in range(len(options)):
                as_black_helper(options[i]).setPricingEngine(engine)

            om = LevenbergMarquardt(1e-8, 1e-8, 1e-8)
            model.calibrate(
                options, om,
                EndCriteria(400, 40, 1.0e-8, 1.0e-8, 1.0e-8))

            sse = 0
            for i in range(13 * 8):
                diff = options[i].calibrationError() * 100.0
                sse += diff * diff

            expected = 74.4
            self.assertFalse(abs(sse - expected) > 1.0)

    def testAlanLewisReferencePrices(self):
        TEST_MESSAGE(
            "Testing Alan Lewis reference prices...")

        backup = SavedSettings()
        settlementDate = Date(5, July, 2002)
        Settings.instance().evaluationDate = settlementDate
        maturityDate = Date(5, July, 2003)
        exercise = EuropeanExercise(maturityDate)

        dayCounter = Actual365Fixed()
        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.01, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.02, dayCounter))

        s0 = QuoteHandle(SimpleQuote(100.0))
        v0 = 0.04
        rho = -0.5
        sigma = 1.0
        kappa = 4.0
        theta = 0.25

        process = HestonProcess(
            riskFreeTS, dividendTS, s0, v0, kappa, theta, sigma, rho)
        model = HestonModel(process)

        laguerreEngine = AnalyticHestonEngine(model, 128)
        gaussLobattoEngine = AnalyticHestonEngine(model, QL_EPSILON, 100000)
        cosEngine = COSHestonEngine(model, 20, 400)
        exponentialFittingEngine = ExponentialFittingHestonEngine(model)

        andersenPiterbargEngine = AnalyticHestonEngine(
            model,
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.discreteTrapezoid(92),
            QL_EPSILON)

        strikes = [80, 90, 100, 110, 120]
        types = [Option.Put, Option.Call]
        engines = [
            laguerreEngine, gaussLobattoEngine,
            cosEngine, andersenPiterbargEngine,
            exponentialFittingEngine]

        expectedResults = [
            [7.958878113256768285213263077598987193482161301733,
             26.774758743998854221382195325726949201687074848341],
            [12.017966707346304987709573290236471654992071308187,
             20.933349000596710388139445766564068085476194042256],
            [17.055270961270109413522653999411000974895436309183,
             16.070154917028834278213466703938231827658768230714],
            [23.017825898442800538908781834822560777763225722188,
             12.132211516709844867860534767549426052805766831181],
            [29.811026202682471843340682293165857439167301370697,
             9.024913483457835636553375454092357136489051667150]]

        tol = 1e-12

        for i in range(len(strikes)):
            strike = strikes[i]
            for j in range(len(types)):
                typeOpt = types[j]
                for k in range(len(engines)):
                    engine = engines[k]
                    payoff = PlainVanillaPayoff(typeOpt, strike)

                    option = VanillaOption(payoff, exercise)
                    option.setPricingEngine(engine)

                    expected = expectedResults[i][j]
                    calculated = option.NPV()
                    relError = abs(calculated - expected) / expected

                    self.assertFalse(relError > tol)

    def testAnalyticPDFHestonEngine(self):
        TEST_MESSAGE(
            "Testing analytic PDF Heston engine...")

        backup = SavedSettings()
        settlementDate = Date(5, January, 2014)
        Settings.instance().evaluationDate = settlementDate

        dayCounter = Actual365Fixed()
        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.07, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.185, dayCounter))

        s0 = QuoteHandle(SimpleQuote(100.0))
        v0 = 0.1
        rho = -0.5
        sigma = 1.0
        kappa = 4.0
        theta = 0.05

        model = HestonModel(
            HestonProcess(
                riskFreeTS, dividendTS,
                s0, v0, kappa, theta, sigma, rho))

        tol = 1e-6
        pdfEngine = AnalyticPDFHestonEngine(model, tol)
        analyticEngine = AnalyticHestonEngine(model, 178)

        maturityDate = Date(5, July, 2014)
        maturity = dayCounter.yearFraction(
            settlementDate, maturityDate)

        exercise = EuropeanExercise(maturityDate)

        for strike in range(40, 190, 20):
            vanillaPayoff = PlainVanillaPayoff(Option.Call, strike)

            planVanillaOption = VanillaOption(vanillaPayoff, exercise)

            planVanillaOption.setPricingEngine(pdfEngine)
            calculated = planVanillaOption.NPV()

            planVanillaOption.setPricingEngine(analyticEngine)
            expected = planVanillaOption.NPV()

            self.assertFalse(abs(calculated - expected) > 3 * tol)

        for strike in range(40, 190, 10):
            digitalOption = VanillaOption(
                CashOrNothingPayoff(
                    Option.Call, strike, 1.0),
                exercise)
            digitalOption.setPricingEngine(pdfEngine)
            calculated = digitalOption.NPV()

            eps = 0.01
            longCall = VanillaOption(
                PlainVanillaPayoff(Option.Call, strike - eps),
                exercise)
            longCall.setPricingEngine(analyticEngine)

            shortCall = VanillaOption(
                PlainVanillaPayoff(Option.Call, strike + eps),
                exercise)
            shortCall.setPricingEngine(analyticEngine)

            expected = (longCall.NPV() - shortCall.NPV()) / (2 * eps)

            self.assertFalse(
                abs(calculated - expected) > tol)

            d = riskFreeTS.discount(maturityDate)
            expectedCDF = 1.0 - expected / d
            calculatedCDF = pdfEngine.cdf(strike, maturity)

            self.assertFalse(
                abs(expectedCDF - calculatedCDF) > tol)

    def testExpansionOnAlanLewisReference(self):
        TEST_MESSAGE(
            "Testing expansion on Alan Lewis reference prices...")

        backup = SavedSettings()
        settlementDate = Date(5, July, 2002)
        Settings.instance().evaluationDate = settlementDate
        maturityDate = Date(5, July, 2003)
        exercise = EuropeanExercise(maturityDate)

        dayCounter = Actual365Fixed()
        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.01, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.02, dayCounter))

        s0 = QuoteHandle(SimpleQuote(100.0))
        v0 = 0.04
        rho = -0.5
        sigma = 1.0
        kappa = 4.0
        theta = 0.25

        process = HestonProcess(
            riskFreeTS, dividendTS, s0, v0,
            kappa, theta, sigma, rho)
        model = HestonModel(process)

        lpp2Engine = HestonExpansionEngine(
            model, HestonExpansionEngine.LPP2)

        lpp3Engine = HestonExpansionEngine(
            model, HestonExpansionEngine.LPP3)

        strikes = [80, 90, 100, 110, 120]
        types = [Option.Put, Option.Call]
        engines = [
            lpp2Engine, lpp3Engine]

        expectedResults = [
            [7.958878113256768285213263077598987193482161301733,
             26.774758743998854221382195325726949201687074848341],
            [12.017966707346304987709573290236471654992071308187,
             20.933349000596710388139445766564068085476194042256],
            [17.055270961270109413522653999411000974895436309183,
             16.070154917028834278213466703938231827658768230714],
            [23.017825898442800538908781834822560777763225722188,
             12.132211516709844867860534767549426052805766831181],
            [29.811026202682471843340682293165857439167301370697,
             9.024913483457835636553375454092357136489051667150]]

        tol = [1.003e-2, 3.645e-3]

        for i in range(len(strikes)):
            strike = strikes[i]
            for j in range(len(types)):
                typeOpt = types[j]
                for k in range(len(engines)):
                    engine = engines[k]
                    payoff = PlainVanillaPayoff(typeOpt, strike)

                    option = VanillaOption(payoff, exercise)
                    option.setPricingEngine(engine)

                    expected = expectedResults[i][j]
                    calculated = option.NPV()
                    relError = abs(calculated - expected) / expected

                    self.assertFalse(relError > tol[k])

    def testExpansionOnFordeReference(self):
        TEST_MESSAGE(
            "Testing expansion on Forde reference prices...")

        backup = SavedSettings()

        forward = 100.0
        v0 = 0.04
        rho = -0.4
        sigma = 0.2
        kappa = 1.15
        theta = 0.04

        terms = [0.1, 1.0, 5.0, 10.0]

        strikes = [60, 80, 90, 100, 110, 120, 140]

        referenceVols = [
            [0.27284673574924445, 0.22360758200372477, 0.21023988547031242, 0.1990674789471587,
             0.19118230678920461, 0.18721342919371017, 0.1899869903378507],
            [0.25200775151345, 0.2127275920953156, 0.20286528150874591, 0.19479398358151515,
             0.18872591728967686, 0.18470857955411824, 0.18204457060905446],
            [0.21637821506229973, 0.20077227130455172, 0.19721753043236154, 0.1942233023784151,
             0.191693211401571, 0.18955229722896752, 0.18491727548069495],
            [0.20672925973965342, 0.198583062164427, 0.19668274423922746, 0.1950420231354201,
             0.193610364344706, 0.1923502827886502, 0.18934360917857015]]

        tol = [
            [0.06, 0.03, 0.03, 0.02],
            [0.15, 0.08, 0.04, 0.02],
            [0.06, 0.08, 1.0, 1.0]]
        tolAtm = [
            [4e-6, 7e-4, 2e-3, 9e-4],
            [7e-6, 4e-4, 9e-4, 4e-4],
            [4e-4, 3e-2, 0.28, 1.0]]

        for j in range(len(terms)):
            term = terms[j]
            lpp2 = LPP2HestonExpansion(
                kappa, theta, sigma, v0, rho, term)
            lpp3 = LPP3HestonExpansion(
                kappa, theta, sigma, v0, rho, term)
            forde = FordeHestonExpansion(
                kappa, theta, sigma, v0, rho, term)
            expansions = [lpp2, lpp3, forde]

            for i in range(len(strikes)):
                strike = strikes[i]
                for k in range(len(expansions)):
                    expansion = expansions[k]
                    expected = referenceVols[j][i]
                    calculated = expansion.impliedVolatility(strike, forward)
                    relError = abs(calculated - expected) / expected
                    refTol = tolAtm[k][j] if strike == forward else tol[k][j]

                    self.assertFalse(relError > refTol)

    def testAllIntegrationMethods(self):
        TEST_MESSAGE(
            "Testing semi-analytic Heston pricing with all integration methods...")

        backup = SavedSettings()
        settlementDate = Date(7, February, 2017)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = Actual365Fixed()

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.05, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.075, dayCounter))

        s0 = QuoteHandle(SimpleQuote(100.0))

        v0 = 0.1
        rho = -0.75
        sigma = 0.4
        kappa = 4.0
        theta = 0.05

        model = HestonModel(
            HestonProcess(
                riskFreeTS, dividendTS,
                s0, v0, kappa, theta, sigma, rho))

        payoff = PlainVanillaPayoff(Option.Put, s0.value())

        maturityDate = settlementDate + Period(1, Years)
        exercise = EuropeanExercise(maturityDate)

        option = VanillaOption(payoff, exercise)

        tol = 1e-8
        expected = 10.147041515497

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussLaguerre(),
            AnalyticHestonEngine.Gatheral,
            False, expected, tol, 256,
            "Gauss-Laguerre with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussLaguerre(),
            AnalyticHestonEngine.BranchCorrection,
            False, expected, tol, 256,
            "Gauss-Laguerre with branch correction")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussLaguerre(),
            AnalyticHestonEngine.AndersenPiterbarg,
            False, expected, tol, 128,
            "Gauss-Laguerre with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussLegendre(),
            AnalyticHestonEngine.Gatheral,
            False, expected, tol, 256,
            "Gauss-Legendre with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussLegendre(),
            AnalyticHestonEngine.BranchCorrection,
            False, expected, tol, 256,
            "Gauss-Legendre with branch correction")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussLegendre(256),
            AnalyticHestonEngine.AndersenPiterbarg,
            False, expected, 1e-4, 256,
            "Gauss-Legendre with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussChebyshev(512),
            AnalyticHestonEngine.Gatheral,
            False, expected, 1e-4, 1024,
            "Gauss-Chebyshev with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussChebyshev(512),
            AnalyticHestonEngine.BranchCorrection,
            False, expected, 1e-4, 1024, "Gauss-Chebyshev with branch correction")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussChebyshev(512),
            AnalyticHestonEngine.AndersenPiterbarg,
            False, expected, 1e-4, 512,
            "Gauss-Laguerre with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussChebyshev2nd(512),
            AnalyticHestonEngine.Gatheral,
            False, expected, 2e-4, 1024,
            "Gauss-Chebyshev2nd with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussChebyshev2nd(512),
            AnalyticHestonEngine.BranchCorrection,
            False, expected, 2e-4, 1024,
            "Gauss-Chebyshev2nd with branch correction")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussChebyshev2nd(512),
            AnalyticHestonEngine.AndersenPiterbarg,
            False, expected, 2e-4, 512,
            "Gauss-Chebyshev2nd with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.discreteSimpson(512),
            AnalyticHestonEngine.Gatheral,
            False, expected, tol, 1024,
            "Discrete Simpson rule with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.discreteSimpson(64),
            AnalyticHestonEngine.AndersenPiterbarg,
            False, expected, tol, 64,
            "Discrete Simpson rule with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.discreteTrapezoid(512),
            AnalyticHestonEngine.Gatheral,
            False, expected, 2e-4, 1024,
            "Discrete Trapezoid rule with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.discreteTrapezoid(64),
            AnalyticHestonEngine.AndersenPiterbarg,
            False, expected, tol, 64,
            "Discrete Trapezoid rule with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussLobatto(
                tol, NullReal()),
            AnalyticHestonEngine.Gatheral,
            True, expected, tol, NullSize(),
            "Gauss-Lobatto with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussLobatto(tol, NullReal()),
            AnalyticHestonEngine.AndersenPiterbarg,
            True, expected, tol, NullSize(),
            "Gauss-Lobatto with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussKronrod(tol),
            AnalyticHestonEngine.Gatheral,
            True, expected, tol, NullSize(),
            "Gauss-Konrod with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.gaussKronrod(tol),
            AnalyticHestonEngine.AndersenPiterbarg,
            True, expected, tol, NullSize(),
            "Gauss-Konrod with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.simpson(tol),
            AnalyticHestonEngine.Gatheral,
            True, expected, 1e-6, NullSize(),
            "Simpson with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.simpson(tol),
            AnalyticHestonEngine.AndersenPiterbarg,
            True, expected, 1e-6, NullSize(),
            "Simpson with Andersen Piterbarg control variate")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.trapezoid(tol),
            AnalyticHestonEngine.Gatheral,
            True, expected, 1e-6, NullSize(),
            "Trapezoid with Gatheral logarithm")

        self._reportOnIntegrationMethodTest(
            option, model,
            AnalyticHestonEngineIntegration.trapezoid(tol),
            AnalyticHestonEngine.AndersenPiterbarg,
            True, expected, 1e-6, NullSize(),
            "Trapezoid with Andersen Piterbarg control variate")

    @unittest.skip("testCosHestonCumulants")
    def testCosHestonCumulants(self):
        TEST_MESSAGE(
            "Testing Heston COS cumulants...")

    def testCosHestonEngine(self):
        TEST_MESSAGE(
            "Testing Heston pricing via COS method...")

        SavedSettings()
        settlementDate = Date(7, February, 2017)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = Actual365Fixed()

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.15, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.07, dayCounter))

        s0 = QuoteHandle(SimpleQuote(100.0))

        v0 = 0.1
        rho = -0.75
        sigma = 1.8
        kappa = 4.0
        theta = 0.22

        model = HestonModel(
            HestonProcess(
                riskFreeTS, dividendTS,
                s0, v0, kappa, theta, sigma, rho))

        maturityDate = settlementDate + Period(1, Years)
        exercise = EuropeanExercise(maturityDate)
        cosEngine = COSHestonEngine(model, 25, 600)

        payoffs = [
            PlainVanillaPayoff(Option.Call, s0.value() + 20),
            PlainVanillaPayoff(Option.Call, s0.value() + 150),
            PlainVanillaPayoff(Option.Put, s0.value() - 20),
            PlainVanillaPayoff(Option.Put, s0.value() - 90)]

        expected = [
            9.364410588426075, 0.01036797658132471,
            5.319092971836708, 0.01032681906278383]

        tol = 1e-10

        for i in range(len(payoffs)):
            option = VanillaOption(payoffs[i], exercise)

            option.setPricingEngine(cosEngine)
            calculated = option.NPV()

            error = abs(expected[i] - calculated)

            self.assertFalse(error > tol)

    def testCharacteristicFct(self):
        TEST_MESSAGE(
            "Testing Heston characteristic function...")

        backup = SavedSettings()
        settlementDate = Date(30, March, 2017)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = Actual365Fixed()

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.35, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.17, dayCounter))

        s0 = QuoteHandle(SimpleQuote(100.0))

        v0 = 0.1
        rho = -0.85
        sigma = 0.8
        kappa = 2.0
        theta = 0.15

        model = HestonModel(
            HestonProcess(
                riskFreeTS, dividendTS,
                s0, v0, kappa, theta, sigma, rho))

        u = [1.0, 0.45, 3, 4]
        t = [0.01, 23.2, 3.2]

        cosEngine = COSHestonEngine(model)
        analyticEngine = AnalyticHestonEngine(model)

        tol = 100 * QL_EPSILON

        for i in range(len(u)):
            for j in range(len(t)):
                c = cosEngine.chF(u[i], t[j])
                a = analyticEngine.chF(complex(u[i], 0.0), t[j])

                error = np.abs(a - c)

                self.assertFalse(error > tol)

    def testAndersenPiterbargPricing(self):
        TEST_MESSAGE(
            "Testing Andersen-Piterbarg method to price under the Heston model...")

        backup = SavedSettings()
        settlementDate = Date(30, March, 2017)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = Actual365Fixed()

        riskFreeTS = YieldTermStructureHandle(
            flatRate(0.10, dayCounter))
        dividendTS = YieldTermStructureHandle(
            flatRate(0.06, dayCounter))

        s0 = QuoteHandle(SimpleQuote(100.0))

        v0 = 0.1
        rho = 0.80
        sigma = 0.75
        kappa = 1.0
        theta = 0.1

        model = HestonModel(
            HestonProcess(
                riskFreeTS, dividendTS,
                s0, v0, kappa, theta, sigma, rho))

        andersenPiterbargLaguerreEngine = AnalyticHestonEngine(
            model,
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.gaussLaguerre())

        andersenPiterbargLobattoEngine = AnalyticHestonEngine(
            model,
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.gaussLobatto(
                NullReal(), 1e-9, 10000),
            1e-9)

        andersenPiterbargSimpsonEngine = AnalyticHestonEngine(
            model,
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.discreteSimpson(256),
            1e-8)

        andersenPiterbargTrapezoidEngine = AnalyticHestonEngine(
            model,
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.discreteTrapezoid(164),
            1e-8)

        andersenPiterbargTrapezoidEngine2 = AnalyticHestonEngine(
            model,
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.trapezoid(1e-8, 256),
            1e-8)

        andersenPiterbargExponentialFittingEngine = ExponentialFittingHestonEngine(model)

        engines = [
            andersenPiterbargLaguerreEngine,
            andersenPiterbargLobattoEngine,
            andersenPiterbargSimpsonEngine,
            andersenPiterbargTrapezoidEngine,
            andersenPiterbargTrapezoidEngine2,
            andersenPiterbargExponentialFittingEngine]

        algos = [
            "Gauss-Laguerre",
            "Gauss-Lobatto",
            "Discrete Simpson",
            "Discrete Trapezoid",
            "Trapezoid",
            "Exponential Fitting"]

        analyticEngine = AnalyticHestonEngine(model, 178)

        maturityDates = [
            settlementDate + Period(1, Days),
            settlementDate + Period(1, Weeks),
            settlementDate + Period(1, Years),
            settlementDate + Period(10, Years)]

        optionTypes = [Option.Call, Option.Put]
        strikes = [50, 75, 90, 100, 110, 130, 150, 200]

        tol = 1e-7

        for u in range(len(maturityDates)):
            exercise = EuropeanExercise(maturityDates[u])
            for i in range(len(optionTypes)):
                for j in range(len(strikes)):
                    option = VanillaOption(
                        PlainVanillaPayoff(
                            optionTypes[i], strikes[j]),
                        exercise)

                    option.setPricingEngine(analyticEngine)
                    expected = option.NPV()

                    for k in range(len(engines)):
                        option.setPricingEngine(engines[k])
                        calculated = option.NPV()

                        error = abs(calculated - expected)

                        self.assertFalse(error > tol)

    def testAndersenPiterbargControlVariateIntegrand(self):
        TEST_MESSAGE(
            "Testing Andersen-Piterbarg Integrand with control variate...")

        backup = SavedSettings()
        settlementDate = Date(17, April, 2017)
        Settings.instance().evaluationDate = settlementDate
        maturityDate = settlementDate + Period(2, Years)

        dayCounter = Actual365Fixed()
        r = 0.075
        q = 0.05
        rTS = YieldTermStructureHandle(
            flatRate(r, dayCounter))
        qTS = YieldTermStructureHandle(
            flatRate(q, dayCounter))

        maturity = dayCounter.yearFraction(
            settlementDate, maturityDate)
        df = rTS.discount(maturity)

        s0 = QuoteHandle(SimpleQuote(100.0))
        fwd = s0.value() * qTS.discount(maturity) / df

        strike = 150
        sx = log(strike)
        dd = log(s0.value() * qTS.discount(maturity) / df)

        v0 = 0.08
        rho = -0.8
        sigma = 0.5
        kappa = 4.0
        theta = 0.05

        hestonModel = HestonModel(
            HestonProcess(
                rTS, qTS,
                s0, v0, kappa, theta, sigma, rho))

        cosEngine = COSHestonEngine(hestonModel)

        engine = AnalyticHestonEngine(
            hestonModel,
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.gaussLaguerre())

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, strike),
            EuropeanExercise(maturityDate))
        option.setPricingEngine(engine)

        refNPV = option.NPV()

        implStdDev = blackFormulaImpliedStdDev(
            Option.Call, strike, fwd, refNPV, df)

        var = cosEngine.var(maturity)
        stdDev = sqrt(var)

        d = (log(s0.value() / strike) + (r - q) * maturity + 0.5 * var) / stdDev

        skew = cosEngine.skew(maturity)
        kurt = cosEngine.kurtosis(maturity)

        n = NormalDistribution()

        q3 = 1 / 6. * s0.value() * stdDev * (2 * stdDev - d) * n(d)
        q4 = 1 / 24. * s0.value() * stdDev * (d * d - 3 * d * stdDev - 1) * n(d)
        q5 = 1 / 72. * s0.value() * stdDev * (d * d * d * d - 5 * d * d * d * stdDev - 6 * d * d + 15 * d * stdDev + 3) * n(d)

        bsNPV = blackFormula(
            Option.Call, strike, fwd, stdDev, df)

        variances = [
            v0 * maturity,
            ((1 - exp(-kappa * maturity)) * (v0 - theta) / (kappa * maturity) + theta) * maturity,
            var,
            (blackFormulaImpliedStdDev(
                Option.Call, strike, fwd,
                bsNPV + skew * q3, df)) ** 2,
            (blackFormulaImpliedStdDev(
                Option.Call, strike, fwd,
                bsNPV + skew * q3 + kurt * q4, df)) ** 2,
            (blackFormulaImpliedStdDev(
                Option.Call, strike, fwd,
                bsNPV + skew * q3 + kurt * q4 + skew * skew * q5, df)) ** 2,
            implStdDev ** 2,
            -8.0 * log(engine.chF(complex(0, -0.5), maturity).real)]

        for i in range(len(variances)):
            sigmaBS = sqrt(variances[i] / maturity)
            for logu in np.arange(log(0.001), log(15), log(1.05)):
                u = exp(logu)
                z = complex(u, -0.5)

                phiBS = np.exp(
                    -0.5 * sigmaBS * sigmaBS * maturity * (z * z + complex(-z.imag, z.real)))

                ex = np.exp(complex(0.0, u * (dd - sx)))

                chf = engine.chF(z, maturity)

                orig = (-ex * chf / (u * u + 0.25)).real
                cv = (ex * (phiBS - chf) / (u * u + 0.25)).real
                self.assertFalse(abs(cv) > 0.03)

    def testAndersenPiterbargConvergence(self):
        TEST_MESSAGE(
            "Testing Andersen-Piterbarg pricing convergence...")

        backup = SavedSettings()
        settlementDate = Date(5, July, 2002)
        Settings.instance().evaluationDate = settlementDate
        maturityDate = Date(5, July, 2003)

        dayCounter = Actual365Fixed()
        rTS = YieldTermStructureHandle(
            flatRate(0.01, dayCounter))
        qTS = YieldTermStructureHandle(
            flatRate(0.02, dayCounter))
        s0 = QuoteHandle(SimpleQuote(100.0))

        v0 = 0.04
        rho = -0.5
        sigma = 1.0
        kappa = 4.0
        theta = 0.25

        hestonModel = HestonModel(
            HestonProcess(
                rTS, qTS,
                s0, v0, kappa, theta, sigma, rho))

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, s0.value()),
            EuropeanExercise(maturityDate))

        reference = 16.070154917028834278213466703938231827658768230714
        diffs = [
            0.0892433814611486298,
            0.00013096156482816923,
            1.34107015270501506e-07,
            1.22913235145460931e-10,
            1.24344978758017533e-13]

        for n in range(10, 50, 10):
            option.setPricingEngine(
                AnalyticHestonEngine(
                    hestonModel,
                    AnalyticHestonEngine.AndersenPiterbarg,
                    AnalyticHestonEngineIntegration.discreteTrapezoid(n),
                    1e-13))

            calculatedDiff = abs(option.NPV() - reference)

            self.assertFalse(
                calculatedDiff > 1.25 * diffs[int(n / 10) - 1])

    def testPiecewiseTimeDependentChFvsHestonChF(self):
        TEST_MESSAGE(
            "Testing piecewise time dependent ChF vs Heston ChF...")

        backup = SavedSettings()
        settlementDate = Date(5, July, 2017)
        Settings.instance().evaluationDate = settlementDate
        maturityDate = Date(5, July, 2018)

        dayCounter = Actual365Fixed()
        rTS = YieldTermStructureHandle(
            flatRate(0.01, dayCounter))
        qTS = YieldTermStructureHandle(
            flatRate(0.02, dayCounter))
        s0 = QuoteHandle(SimpleQuote(100.0))

        v0 = 0.04
        rho = -0.5
        sigma = 1.0
        kappa = 4.0
        theta = 0.25

        thetaP = ConstantParameter(theta, PositiveConstraint())
        kappaP = ConstantParameter(kappa, PositiveConstraint())
        sigmaP = ConstantParameter(sigma, PositiveConstraint())
        rhoP = ConstantParameter(rho, BoundaryConstraint(-1.0, 1.0))

        analyticEngine = AnalyticHestonEngine(
            HestonModel(
                HestonProcess(
                    rTS, qTS, s0, v0, kappa, theta, sigma, rho)))

        ptdHestonEngine = AnalyticPTDHestonEngine(
            PiecewiseTimeDependentHestonModel(
                rTS, qTS, s0, v0, thetaP, kappaP, sigmaP, rhoP,
                TimeGrid(
                    dayCounter.yearFraction(
                        settlementDate, maturityDate), 10)))

        tol = 100 * QL_EPSILON

        for r in np.arange(0.1, 4, 0.25):
            for phi in range(0, 360, 60):
                for t in np.arange(0.1, 1.0, 0.3):
                    z = r * np.exp(complex(0, phi))

                    a = analyticEngine.chF(z, t)
                    b = ptdHestonEngine.chF(z, t)
                    self.assertFalse(np.abs(a - b) > tol)

    @unittest.skip("testPiecewiseTimeDependentComparison")
    def testPiecewiseTimeDependentComparison(self):
        TEST_MESSAGE(
            "Testing piecewise time dependent ChF vs Heston ChF...")

    def testPiecewiseTimeDependentChFAsymtotic(self):
        TEST_MESSAGE(
            "Testing piecewise time dependent ChF vs Heston ChF...")

        backup = SavedSettings()
        settlementDate = Date(5, July, 2017)
        Settings.instance().evaluationDate = settlementDate
        maturityDate = settlementDate + Period(13, Months)

        dc = Actual365Fixed()
        maturity = dc.yearFraction(settlementDate, maturityDate)
        rTS = YieldTermStructureHandle(
            flatRate(0.0, dc))

        modelTimes = DoubleVector()
        modelTimes.push_back(0.01)
        modelTimes.push_back(0.5)
        modelTimes.push_back(2.0)

        modelGrid = TimeGrid(modelTimes)

        v0 = 0.1
        pTimes = modelTimes[0:(len(modelTimes) - 1)]

        sigma = PiecewiseConstantParameter(pTimes, PositiveConstraint())
        theta = PiecewiseConstantParameter(pTimes, PositiveConstraint())
        kappa = PiecewiseConstantParameter(pTimes, PositiveConstraint())
        rho = PiecewiseConstantParameter(pTimes, BoundaryConstraint(-1.0, 1.0))

        sigmas = [0.01, 0.2, 0.6]
        thetas = [0.16, 0.06, 0.36]
        kappas = [1.0, 0.3, 4.0]
        rhos = [0.5, -0.75, -0.25]

        for i in range(3):
            sigma.setParam(i, sigmas[i])
            theta.setParam(i, thetas[i])
            kappa.setParam(i, kappas[i])
            rho.setParam(i, rhos[i])

        s0 = QuoteHandle(SimpleQuote(100.0))
        ptdModel = PiecewiseTimeDependentHestonModel(
            rTS, rTS, s0, v0, theta, kappa,
            sigma, rho, modelGrid)
        eps = 1e-8

        ptdHestonEngine = AnalyticPTDHestonEngine(
            ptdModel,
            AnalyticPTDHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.discreteTrapezoid(128),
            eps)
        D_u_inf = -complex(sqrt(1 - rhos[0] * rhos[0]), rhos[0]) / sigmas[0]
        dd = complex(
            kappas[0],
            (2 * kappas[0] * rhos[0] - sigmas[0]) / (2 * sqrt(1 - rhos[0] * rhos[0]))) / (sigmas[0] * sigmas[0])

        C_u_inf = complex(0.0, 0.0)
        cc = complex(0.0, 0.0)
        clog = complex(0.0, 0.0)
        for i in range(3):
            kappa = kappas[i]
            theta = thetas[i]
            sigma = sigmas[i]
            rho = rhos[i]
            tau = min(maturity, modelGrid[i + 1]) - modelGrid[i]
            C_u_inf += -kappa * theta * tau / sigma * \
                       complex(sqrt(1 - rho * rho), rho)

            cc += kappa * complex(
                2 * kappa,
                (2 * kappa * rho - sigma) / sqrt(1 - rho * rho)) * tau * theta / (2 * sigma * sigma)
            Di = sigma / sigmas[i + 1] * complex(
                sqrt(1 - rhos[i + 1] * rhos[i + 1]),
                rhos[i + 1]) if i < 2 else complex(0.0, 0.0)

            clog += 2 * kappa * theta / (sigma * sigma) * \
                    np.log(1.0 - (Di - complex(sqrt(1 - rho * rho), rho)) / (Di + complex(sqrt(1 - rho * rho), -rho)))

        epsilon = eps * M_PI / s0.value()
        uM = AnalyticHestonEngineIntegration.andersenPiterbargIntegrationLimit(
            -(C_u_inf + D_u_inf * v0).real, epsilon, v0, maturity)
        expectedUM = 18.6918883427
        self.assertFalse(abs(uM - expectedUM) > 1e-5)

        u = 1e8
        expectedlnChF = ptdHestonEngine.lnChF(complex(u, 0.0), maturity)
        calculatedAsympotic = (D_u_inf * u + dd) * v0 + C_u_inf * u + cc + clog
        self.assertFalse(
            np.abs(expectedlnChF - calculatedAsympotic) > 0.01)

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, s0.value()),
            EuropeanExercise(maturityDate))
        option.setPricingEngine(ptdHestonEngine)

        expectedNPV = 17.43851162589377
        calculatedNPV = option.NPV()
        diffNPV = abs(expectedNPV - calculatedNPV)
        self.assertFalse(diffNPV > 1e-9)

    def testSmallSigmaExpansion(self):
        TEST_MESSAGE(
            "Testing small sigma expansion of the characteristic function...")

        backup = SavedSettings()
        settlementDate = Date(20, March, 2020)
        Settings.instance().evaluationDate = settlementDate
        maturityDate = settlementDate + Period(2, Years)
        dc = Actual365Fixed()
        t = dc.yearFraction(settlementDate, maturityDate)
        rTS = YieldTermStructureHandle(
            flatRate(0.0, dc))
        spot = QuoteHandle(SimpleQuote(100))
        theta = 0.1 * 0.1
        v0 = theta + 0.02
        kappa = 1.25
        sigma = 1e-9
        rho = -0.9

        hestonModel = HestonModel(
            HestonProcess(
                rTS, rTS, spot, v0, kappa, theta, sigma, rho))
        engine = AnalyticHestonEngine(hestonModel)
        expectedChF = complex(
            0.990463578538352651, 2.60693475987521132e-12)
        calculatedChF = engine.chF(complex(0.55, -0.5), t)

        diffChF = np.abs(expectedChF - calculatedChF)
        tolChF = 1e-12
        self.assertFalse(diffChF > tolChF)

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, 120.0),
            EuropeanExercise(maturityDate))

        option.setPricingEngine(
            AnalyticHestonEngine(
                hestonModel,
                AnalyticHestonEngine.AndersenPiterbarg,
                AnalyticHestonEngineIntegration.gaussLaguerre(192)))

        calculatedNPV = option.NPV()

        stdDev = sqrt(((1 - exp(-kappa * t)) * (v0 - theta) / (kappa * t) + theta) * t)

        expectedNPV = blackFormula(
            Option.Call, 120.0, 100.0, stdDev)

        diffNPV = abs(calculatedNPV - expectedNPV)
        tolNPV = 50 * sigma

        self.assertFalse(diffNPV > tolNPV)

    def testSmallSigmaExpansion4ExpFitting(self):
        TEST_MESSAGE(
            "Testing small sigma expansion for the exponential fitting Heston engine...")

        backup = SavedSettings()
        todaysDate = Date(13, March, 2020)
        Settings.instance().evaluationDate = todaysDate

        dc = Actual365Fixed()
        rTS = YieldTermStructureHandle(
            flatRate(0.05, dc))
        qTS = YieldTermStructureHandle(
            flatRate(0.075, dc))
        spot = QuoteHandle(SimpleQuote(100))

        maturityDate = Date(14, March, 2021)
        maturity = dc.yearFraction(todaysDate, maturityDate)
        fwd = spot.value() * qTS.discount(maturity) / rTS.discount(maturity)

        v0 = 0.04
        rho = -0.5
        kappa = 4.0
        theta = 0.04

        moneyness = 0.1
        strike = exp(-moneyness * sqrt(theta * maturity)) * fwd

        expected = blackFormula(
            Option.Call, strike, fwd,
            sqrt(v0 * maturity), rTS.discount(maturity))

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, strike),
            EuropeanExercise(maturityDate))

        for logSigma in np.arange(log10(1e-4), log10(1e-12), log10(0.1)):
            sigma = 10.0 ** logSigma
            option.setPricingEngine(
                ExponentialFittingHestonEngine(
                    HestonModel(
                        HestonProcess(
                            rTS, qTS, spot, v0, kappa,
                            theta, sigma, rho))))
            calculated = option.NPV()

            diff = abs(expected - calculated)

            self.assertFalse(diff > 0.01 * sigma)

        kappas = [0.5, 1.0, 4.0]
        thetas = [0.04, 0.09]
        v0s = [0.025, 0.20]
        maturities = [1, 31, 182, 1850]

        for mat in maturities:
            maturityDate = todaysDate + Period(mat, Days)
            df = rTS.discount(maturityDate)
            fwd = spot.value() * qTS.discount(maturityDate) / df

            exercise = EuropeanExercise(maturityDate)

            t = dc.yearFraction(todaysDate, maturityDate)

            optionType = Option.Call

            for kappa in kappas:
                for theta in thetas:
                    for v0 in v0s:
                        engine = ExponentialFittingHestonEngine(
                            HestonModel(
                                HestonProcess(
                                    rTS, qTS, spot, v0,
                                    kappa, theta, 1e-13, -0.8)))

                        stdDev = sqrt(((1 - exp(-kappa * t)) * (v0 - theta) / (kappa * t) + theta) * t)

                        for logStrike in np.arange(
                                log(spot.value() * exp(-10 * stdDev)),
                                log(strike < spot.value() * exp(10 * stdDev)),
                                log(1.2)):
                            strike = exp(logStrike)
                            option = VanillaOption(
                                PlainVanillaPayoff(
                                    optionType, strike),
                                exercise)

                            option.setPricingEngine(engine)
                            calculated = option.NPV()

                            expected = blackFormula(
                                optionType, strike, fwd, stdDev, df)

                            diff = abs(expected - calculated)

                            self.assertFalse(diff > 1e-10)

                            optionType = Option.Put if optionType == Option.Call else Option.Call

    def testExponentialFitting4StrikesAndMaturities(self):
        TEST_MESSAGE(
            "Testing exponential fitting Heston engine with high precision results for large moneyness...")

        backup = SavedSettings()
        todaysDate = Date(13, May, 2020)
        Settings.instance().evaluationDate = todaysDate

        dc = Actual365Fixed()
        rTS = YieldTermStructureHandle(
            flatRate(0.0507, dc))
        qTS = YieldTermStructureHandle(
            flatRate(0.0469, dc))
        s0 = QuoteHandle(SimpleQuote(1.0))
        moneyness = [
            -20, -10, -5, 2.5, 1, 0, 1, 2.5, 5, 10, 20]
        maturities = [
            Period(1, Days),
            Period(1, Months),
            Period(1, Years),
            Period(10, Years)]

        v0 = 0.04
        rho = -0.6
        sigma = 0.75
        kappa = 2.5
        theta = 0.06

        referenceValues = [
            1.1631865252540813e-58,
            1.06426822273258466e-49,
            6.92896489110422086e-16,
            8.19515526286263236e-06,
            0.000625608178476390504,
            0.00417261379371945684,
            0.000625608178476390504,
            8.19515526286263236e-06,
            1.92308901296741414e-10,
            1.57327901822368115e-23,
            5.7830515043285098e-58,
            3.56081886910098813e-48,
            2.9489071194212509e-23,
            1.54181757781090727e-11,
            0.000367960011879847279,
            0.00493886106106039818,
            0.0227152343265593776,
            0.00493886106106039818,
            0.000367960011879847279,
            3.06653474407784574e-06,
            8.86665241279348934e-11,
            1.51206812371708868e-20,
            4.18506719865401643e-29,
            2.46637786897559908e-15,
            1.75338784910563671e-08,
            0.00284789176080218294,
            0.0199133097064688458,
            0.0776848755698912041,
            0.0199133097064688458,
            0.00284789176080218294,
            0.00012462190796343504,
            2.59755319566692257e-07,
            1.13853114743124721e-12,
            4.27612073892114211e-39,
            1.08387452075906664e-25,
            4.15179522944463802e-11,
            0.00134157732880653131,
            0.029018582813884912,
            0.176405213088554197,
            0.029018582813884912,
            0.00134157732880653131,
            5.43674074281991917e-06,
            6.51443921040230507e-11,
            9.25756999394709285e-21]

        model = HestonModel(
            HestonProcess(
                rTS, qTS, s0, v0, kappa,
                theta, sigma, rho))

        engine = ExponentialFittingHestonEngine(model)

        idx = 0
        for i in range(len(maturities)):
            maturityDate = todaysDate + maturities[i]
            t = dc.yearFraction(todaysDate, maturityDate)

            exercise = EuropeanExercise(maturityDate)

            df = rTS.discount(t)
            fwd = s0.value() * qTS.discount(t) / df

            for j in range(len(moneyness)):
                strike = exp(-moneyness[j] * sqrt(theta * t)) * fwd
                for k in range(2):
                    payoff = PlainVanillaPayoff(
                        Option.Put if k != 0 else Option.Call,
                        strike)
                    option = VanillaOption(payoff, exercise)
                    option.setPricingEngine(engine)

                    calculated = option.NPV()

                    if payoff.optionType() == Option.Call:
                        if fwd < strike:
                            expected = referenceValues[idx]
                        else:
                            expected = (fwd - strike) * df + referenceValues[idx]
                    elif fwd > strike:
                        expected = referenceValues[idx]
                    else:
                        expected = referenceValues[idx] - (fwd - strike) * df
                    diff = abs(calculated - expected)
                    self.assertFalse(diff > 1e-12)
                idx += 1

    @unittest.skip("testHestonEngineIntegration")
    def testHestonEngineIntegration(self):
        TEST_MESSAGE(
            "Testing Heston engine integration signature...")

    def testOptimalControlVariateChoice(self):
        TEST_MESSAGE(
            "Testing optimal control variate choice for the Heston model...")

        v0 = 0.0225
        rho = 0.5
        sigma = 2.0
        kappa = 0.1
        theta = 0.01
        t = 2.0

        calculated = AnalyticHestonEngine.optimalControlVariate(
            t, v0, kappa, theta, sigma, rho)

        self.assertFalse(
            calculated != AnalyticHestonEngine.AsymptoticChF)

        calculated = AnalyticHestonEngine.optimalControlVariate(
            t, v0, kappa, theta, 0.2, rho)

        self.assertFalse(
            calculated != AnalyticHestonEngine.AndersenPiterbargOptCV)

        calculated = AnalyticHestonEngine.optimalControlVariate(
            t, 0.2, kappa, theta, sigma, rho)

        self.assertFalse(
            calculated != AnalyticHestonEngine.AndersenPiterbargOptCV)

    def testAsymptoticControlVariate(self):
        TEST_MESSAGE(
            "Testing Heston asymptotic control variate...")

        backup = SavedSettings()
        todaysDate = Date(4, August, 2020)
        Settings.instance().evaluationDate = todaysDate
        dc = Actual365Fixed()
        rTS = YieldTermStructureHandle(
            flatRate(0.0, dc))
        s0 = QuoteHandle(SimpleQuote(1.0))

        v0 = 0.0225
        rho = 0.5
        sigma = 2.0
        kappa = 0.1
        theta = 0.01

        model = HestonModel(
            HestonProcess(
                rTS, rTS, s0, v0, kappa,
                theta, sigma, rho))
        maturityDate = todaysDate + Period(2, Years)
        t = dc.yearFraction(todaysDate, maturityDate)
        exercise = EuropeanExercise(maturityDate)

        moneynesses = [-15, -10, -5, 0, 5, 10, 15]
        expected = [
            0.0074676425640918,
            0.008680823863233695,
            0.010479611906112223,
            0.023590088942038945,
            0.0019575784806211706,
            0.0005490310253748906,
            0.0001657118753134695]
        engines = [
            AnalyticHestonEngine(
                model,
                AnalyticHestonEngine.OptimalCV,
                AnalyticHestonEngineIntegration.gaussLobatto(
                    1e-10, 1e-10, 100000)),
            AnalyticHestonEngine(
                model,
                AnalyticHestonEngine.OptimalCV,
                AnalyticHestonEngineIntegration.gaussLaguerre(96)),
            ExponentialFittingHestonEngine(model)]

        for j in range(len(engines)):
            for i in range(len(moneynesses)):
                moneyness = moneynesses[i]

                strike = exp(-moneyness * sqrt(theta * t))

                payoff = PlainVanillaPayoff(
                    Option.Call if strike > 1.0 else Option.Put,
                    strike)

                engine = engines[j]

                option = VanillaOption(payoff, exercise)
                option.setPricingEngine(engine)

                calculated = option.NPV()
                diff = abs(calculated - expected[i])

                self.assertFalse(diff > 5e-8)

    def testLocalVolFromHestonModel(self):
        TEST_MESSAGE(
            "Testing Local Volatility pricing from Heston Model...")

        backup = SavedSettings()

        todaysDate = Date(28, June, 2021)
        Settings.instance().evaluationDate = todaysDate

        dc = Actual365Fixed()

        dates = DateVector(4)
        dates[0] = todaysDate
        dates[1] = todaysDate + Period(90, Days)
        dates[2] = todaysDate + Period(180, Days)
        dates[3] = todaysDate + Period(1, Years)
        rates = DoubleVector(4)
        rates[0] = 0.075
        rates[1] = 0.05
        rates[2] = 0.075
        rates[3] = 0.1
        rTS = YieldTermStructureHandle(
            ZeroCurve(dates, rates, dc))

        dates = DateVector(3)
        dates[0] = todaysDate
        dates[1] = todaysDate + Period(90, Days)
        dates[2] = todaysDate + Period(1, Years)
        rates = DoubleVector(3)
        rates[0] = 0.06
        rates[1] = 0.04
        rates[2] = 0.12
        qTS = YieldTermStructureHandle(
            ZeroCurve(dates, rates, dc))

        s0 = QuoteHandle(SimpleQuote(100.0))

        v0 = 0.1
        rho = -0.75
        sigma = 0.8
        kappa = 1.0
        theta = 0.16

        hestonModel = HestonModel(
            HestonProcess(
                rTS, qTS, s0, v0, kappa, theta, sigma, rho))

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, 120.0),
            EuropeanExercise(todaysDate + Period(1, Years)))

        option.setPricingEngine(
            AnalyticHestonEngine(
                hestonModel,
                AnalyticHestonEngine.OptimalCV,
                AnalyticHestonEngineIntegration.gaussLaguerre(192)))

        expected = option.NPV()

        option.setPricingEngine(
            FdBlackScholesVanillaEngine(
                BlackScholesMertonProcess(
                    s0, qTS, rTS,
                    BlackVolTermStructureHandle(
                        HestonBlackVolSurface(
                            HestonModelHandle(hestonModel),
                            AnalyticHestonEngine.OptimalCV,
                            AnalyticHestonEngineIntegration.gaussLaguerre(24)))),
                25, 125, 1, FdmSchemeDesc.Douglas(), True, 0.4))

        calculated = option.NPV()

        tol = 0.002
        diff = abs(calculated - expected)
        self.assertFalse(diff > tol)
