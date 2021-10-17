import unittest
from utilities import *
from QuantLib import *
import numpy as np


class HestonTestData(object):
    def __init__(self,
                 kappa,
                 theta,
                 sigma,
                 rho,
                 r,
                 q,
                 T,
                 K):
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.r = r
        self.q = q
        self.T = T
        self.K = K


class NewBarrierOptionData(object):
    def __init__(self,
                 barrierType,
                 barrier,
                 rebate,
                 optType,
                 strike,
                 s,
                 q,
                 r,
                 t,
                 v):
        self.barrierType = barrierType
        self.barrier = barrier
        self.rebate = rebate
        self.optType = optType
        self.strike = strike
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility


class FdHestonTest(unittest.TestCase):
    def testFdmHestonVarianceMesher(self):
        TEST_MESSAGE("Testing FDM Heston variance mesher...")

        backup = SavedSettings()

        today = Date(22, February, 2018)
        dc = Actual365Fixed()
        Settings.instance().evaluationDate = today

        process = HestonProcess(
            YieldTermStructureHandle(flatRate(0.02, dc)),
            YieldTermStructureHandle(flatRate(0.02, dc)),
            QuoteHandle(SimpleQuote(100.0)),
            0.09, 1.0, 0.09, 0.2, -0.5)

        mesher = FdmHestonVarianceMesher(5, process, 1.0)

        locations = mesher.locations()

        expected = [
            0.0, 6.652314e-02, 9.000000e-02, 1.095781e-01, 2.563610e-01]

        tol = 1e-6
        for i in range(len(locations)):
            diff = abs(expected[i] - locations[i])

            self.assertFalse(diff > tol)

        lVol = LocalConstantVol(today, 2.5, dc)

        constSlvMesher = FdmHestonLocalVolatilityVarianceMesher(5, process, lVol, 1.0)

        expectedVol = 2.5 * mesher.volaEstimate()
        calculatedVol = constSlvMesher.volaEstimate()

        diff = abs(calculatedVol - expectedVol)
        self.assertFalse(diff > tol)

        alpha = 0.01

        class ParableLocalVolatilityImpl(object):
            def __init__(self, s0, alpha):
                self.s0 = s0
                self.alpha = alpha

            def __call__(self, t, s):
                return self.alpha * ((self.s0 - s) ** 2 + 25.0)

        parableLocalVolImpl = ParableLocalVolatilityImpl(100.0, alpha)
        leverageFct = CustomicLocalVolatility(
            parableLocalVolImpl, today, NullCalendar(), Following, dc)

        slvMesher = FdmHestonLocalVolatilityVarianceMesher(
            5, process, leverageFct, 0.5, 1, 0.01)

        initialVolEstimate = FdmHestonVarianceMesher(
            5, process, 0.5, 1, 0.01).volaEstimate()

        leverageAvg = 0.455881 / (1 - 0.02)

        volaEstExpected = 0.5 * (leverageAvg + leverageFct.localVol(0, 100)) * initialVolEstimate

        volaEstCalculated = slvMesher.volaEstimate()

        self.assertFalse(
            abs(volaEstExpected - volaEstCalculated) > 0.001)

    def testFdmHestonBarrier(self):
        TEST_MESSAGE(
            "Testing FDM with barrier option for Heston model vs Black-Scholes model...")

        backup = SavedSettings()

        s0 = QuoteHandle(SimpleQuote(100.0))

        rTS = YieldTermStructureHandle(flatRate(0.05, Actual365Fixed()))
        qTS = YieldTermStructureHandle(flatRate(0.0, Actual365Fixed()))

        hestonProcess = HestonProcess(
            rTS, qTS, s0, 0.04, 2.5, 0.04, 0.66, -0.8)

        Settings.instance().evaluationDate = Date(28, March, 2004)
        exerciseDate = Date(28, March, 2005)

        exercise = EuropeanExercise(exerciseDate)

        payoff = PlainVanillaPayoff(Option.Call, 100)

        barrierOption = BarrierOption(
            Barrier.UpOut, 135, 0.0, payoff, exercise)

        barrierOption.setPricingEngine(
            FdHestonBarrierEngine(
                HestonModel(hestonProcess),
                50, 400, 100))

        tol = 0.01
        npvExpected = 9.1530
        deltaExpected = 0.5218
        gammaExpected = -0.0354

        self.assertFalse(abs(barrierOption.NPV() - npvExpected) > tol)
        self.assertFalse(abs(barrierOption.delta() - deltaExpected) > tol)
        self.assertFalse(abs(barrierOption.gamma() - gammaExpected) > tol)

    def testFdmHestonBarrierVsBlackScholes(self):
        TEST_MESSAGE("Testing FDM with barrier option in Heston model...")

        backup = SavedSettings()

        values = [
            # /* The data below are from
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 pag. 72
            # */
            #            barrierType, barrier, rebate,         type, strike,     s,    q,    r,    t,    v
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, 100, 100.0, 0.00, 0.08, 1.00, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, 90, 100.0, 0.00, 0.08, 0.25, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, 90, 100.0, 0.00, 0.08, 0.25, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, 100, 100.0, 0.00, 0.08, 0.40, 0.25),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.15),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, 100, 100.0, 0.00, 0.08, 0.40, 0.35),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.15),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, 110, 100.0, 0.00, 0.00, 1.00, 0.20),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, 110, 100.0, 0.00, 0.08, 1.00, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, 110, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.25),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, 110, 100.0, 0.00, 0.04, 1.00, 0.15),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 1.00, 0.15),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, 90, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, 100, 100.0, 0.04, 0.08, 0.50, 0.30),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, 110, 100.0, 0.04, 0.08, 0.50, 0.30)]

        dc = Actual365Fixed()
        todaysDate = Date(28, March, 2004)
        exerciseDate = Date(28, March, 2005)
        Settings.instance().evaluationDate = todaysDate

        spot = QuoteHandle(SimpleQuote(0.0))
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(vol, dc))

        bsProcess = BlackScholesMertonProcess(spot, qTS, rTS, volTS)

        analyticEngine = AnalyticBarrierEngine(bsProcess)

        for value in values:
            exDate = todaysDate + timeToDays(value.t, 365)
            exercise = EuropeanExercise(exDate)

            as_simple_quote(spot.currentLink()).setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            payoff = PlainVanillaPayoff(value.optType, value.strike)

            barrierOption = BarrierOption(
                value.barrierType,
                value.barrier,
                value.rebate,
                payoff, exercise)

            v0 = vol.value() * vol.value()
            hestonProcess = HestonProcess(
                rTS, qTS, spot, v0, 1.0, v0, 0.005, 0.0)

            barrierOption.setPricingEngine(
                FdHestonBarrierEngine(
                    HestonModel(hestonProcess),
                    200, 101, 3))

            calculatedHE = barrierOption.NPV()

            barrierOption.setPricingEngine(analyticEngine)
            expected = barrierOption.NPV()

            tol = 0.0025
            self.assertFalse(abs(calculatedHE - expected) / expected > tol)

    def testFdmHestonAmerican(self):
        TEST_MESSAGE("Testing FDM with American option in Heston model...")

        backup = SavedSettings()

        s0 = QuoteHandle(SimpleQuote(100.0))

        rTS = YieldTermStructureHandle(flatRate(0.05, Actual365Fixed()))
        qTS = YieldTermStructureHandle(flatRate(0.0, Actual365Fixed()))

        hestonProcess = HestonProcess(
            rTS, qTS, s0, 0.04, 2.5, 0.04, 0.66, -0.8)

        Settings.instance().evaluationDate = Date(28, March, 2004)
        exerciseDate = Date(28, March, 2005)

        exercise = AmericanExercise(exerciseDate)

        payoff = PlainVanillaPayoff(Option.Put, 100)

        option = VanillaOption(payoff, exercise)
        engine = FdHestonVanillaEngine(
            HestonModel(hestonProcess),
            200, 100, 50)
        option.setPricingEngine(engine)

        tol = 0.01
        npvExpected = 5.66032
        deltaExpected = -0.30065
        gammaExpected = 0.02202

        self.assertFalse(abs(option.NPV() - npvExpected) > tol)
        self.assertFalse(abs(option.delta() - deltaExpected) > tol)
        self.assertFalse(abs(option.gamma() - gammaExpected) > tol)

    def testFdmHestonIkonenToivanen(self):
        TEST_MESSAGE("Testing FDM Heston for Ikonen and Toivanen tests...")

        # check prices of american puts as given in:
        # From Efficient numerical methods for pricing American options under 
        # stochastic volatility, Samuli Ikonen, Jari Toivanen, 
        # http://users.jyu.fi/~tene/papers/reportB12-05.pdf

        backup = SavedSettings()

        rTS = YieldTermStructureHandle(flatRate(0.10, Actual360()))
        qTS = YieldTermStructureHandle(flatRate(0.0, Actual360()))

        Settings.instance().evaluationDate = Date(28, March, 2004)
        exerciseDate = Date(26, June, 2004)

        exercise = AmericanExercise(exerciseDate)

        payoff = PlainVanillaPayoff(Option.Put, 10)

        option = VanillaOption(payoff, exercise)

        strikes = [8, 9, 10, 11, 12]
        expected = [2.00000, 1.10763, 0.520038, 0.213681, 0.082046]
        tol = 0.001

        for i in range(len(strikes)):
            s0 = QuoteHandle(SimpleQuote(strikes[i]))
            hestonProcess = HestonProcess(
                rTS, qTS, s0, 0.0625, 5, 0.16, 0.9, 0.1)

            engine = FdHestonVanillaEngine(
                HestonModel(
                    hestonProcess),
                100, 400)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            self.assertFalse(abs(calculated - expected[i]) > tol)

    def testFdmHestonEuropeanWithDividends(self):
        TEST_MESSAGE(
            "Testing FDM with European option with dividends in Heston model...")

        backup = SavedSettings()

        s0 = QuoteHandle(SimpleQuote(100.0))

        rTS = YieldTermStructureHandle(flatRate(0.05, Actual365Fixed()))
        qTS = YieldTermStructureHandle(flatRate(0.0, Actual365Fixed()))

        hestonProcess = HestonProcess(rTS, qTS, s0, 0.04, 2.5, 0.04, 0.66, -0.8)

        Settings.instance().evaluationDate = Date(28, March, 2004)
        exerciseDate = Date(28, March, 2005)

        exercise = AmericanExercise(exerciseDate)

        payoff = PlainVanillaPayoff(Option.Put, 100)

        dividends = DoubleVector(1, 5.0)
        dividendDates = DateVector(1, Date(28, September, 2004))

        option = DividendVanillaOption(
            payoff, exercise, dividendDates, dividends)
        engine = FdHestonVanillaEngine(
            HestonModel(hestonProcess),
            50, 100, 50)
        option.setPricingEngine(engine)

        tol = 0.01
        gammaTol = 0.001
        npvExpected = 7.38216
        deltaExpected = -0.397902
        gammaExpected = 0.027747

        self.assertFalse(abs(option.NPV() - npvExpected) > tol)
        self.assertFalse(abs(option.delta() - deltaExpected) > tol)
        self.assertFalse(abs(option.gamma() - gammaExpected) > gammaTol)

    def testFdmHestonConvergence(self):
        # convergence tests based on
        # ADI finite difference schemes for option pricing in the
        # Heston model with correlation, K.J. in t'Hout and S. Foulon

        TEST_MESSAGE("Testing FDM Heston convergence...")

        backup = SavedSettings()

        values = [
            HestonTestData(1.5, 0.04, 0.3, -0.9, 0.025, 0.0, 1.0, 100),
            HestonTestData(3.0, 0.12, 0.04, 0.6, 0.01, 0.04, 1.0, 100),
            HestonTestData(0.6067, 0.0707, 0.2928, -0.7571, 0.03, 0.0, 3.0, 100),
            HestonTestData(2.5, 0.06, 0.5, -0.1, 0.0507, 0.0469, 0.25, 100)]

        schemes = [
            FdmSchemeDesc.Hundsdorfer(),
            FdmSchemeDesc.ModifiedCraigSneyd(),
            FdmSchemeDesc.ModifiedHundsdorfer(),
            FdmSchemeDesc.CraigSneyd(),
            FdmSchemeDesc.TrBDF2(),
            FdmSchemeDesc.CrankNicolson()]

        tn = [60]
        v0 = [0.04]

        todaysDate = Date(28, March, 2004)
        Settings.instance().evaluationDate = todaysDate

        s0 = QuoteHandle(SimpleQuote(75.0))

        for scheme in schemes:
            for value in values:
                for j in tn:
                    for k in v0:
                        rTS = YieldTermStructureHandle(flatRate(value.r, Actual365Fixed()))
                        qTS = YieldTermStructureHandle(flatRate(value.q, Actual365Fixed()))

                        hestonProcess = HestonProcess(
                            rTS, qTS, s0, k, value.kappa,
                            value.theta, value.sigma, value.rho)

                        exerciseDate = todaysDate + Period(int(value.T * 365), Days)
                        exercise = EuropeanExercise(exerciseDate)

                        payoff = PlainVanillaPayoff(Option.Call, value.K)

                        option = VanillaOption(payoff, exercise)
                        engine = FdHestonVanillaEngine(
                            HestonModel(hestonProcess),
                            j, 101, 51, 0, scheme)
                        option.setPricingEngine(engine)

                        calculated = option.NPV()

                        analyticEngine = AnalyticHestonEngine(
                            HestonModel(hestonProcess),
                            144)

                        option.setPricingEngine(analyticEngine)
                        expected = option.NPV()
                        self.assertFalse(
                            abs(expected - calculated) / expected > 0.02 and
                            abs(expected - calculated) > 0.002)

    def testFdmHestonBlackScholes(self):
        TEST_MESSAGE("Testing FDM Heston with Black Scholes model...")

        backup = SavedSettings()

        Settings.instance().evaluationDate = Date(28, March, 2004)
        exerciseDate = Date(26, June, 2004)

        rTS = YieldTermStructureHandle(flatRate(0.10, Actual360()))
        qTS = YieldTermStructureHandle(flatRate(0.0, Actual360()))
        volTS = BlackVolTermStructureHandle(
            flatVol(rTS.referenceDate(), 0.25, rTS.dayCounter()))

        exercise = EuropeanExercise(exerciseDate)

        payoff = PlainVanillaPayoff(Option.Put, 10)

        option = VanillaOption(payoff, exercise)

        strikes = [8, 9, 10, 11, 12]
        tol = 0.0001

        for strike in strikes:
            s0 = QuoteHandle(SimpleQuote(strike))

            bsProcess = GeneralizedBlackScholesProcess(s0, qTS, rTS, volTS)

            option.setPricingEngine(AnalyticEuropeanEngine(bsProcess))

            expected = option.NPV()

            hestonProcess = HestonProcess(
                rTS, qTS, s0, 0.0625, 1, 0.0625, 0.0001, 0.0)

            # Hundsdorfer scheme
            option.setPricingEngine(
                FdHestonVanillaEngine(
                    HestonModel(hestonProcess),
                    100, 400, 3))

            calculated = option.NPV()
            self.assertFalse(abs(calculated - expected) > tol)

            # Explicit scheme
            option.setPricingEngine(
                FdHestonVanillaEngine(
                    HestonModel(hestonProcess),
                    4000, 400, 3, 0,
                    FdmSchemeDesc.ExplicitEuler()))

            calculated = option.NPV()
            self.assertFalse(abs(calculated - expected) > tol)

    def testFdmHestonIntradayPricing(self):
        TEST_MESSAGE("Testing FDM Heston intraday pricing ...")
        backup = SavedSettings()

        optType = Option.Put
        underlying = 36
        strike = underlying
        dividendYield = 0.00
        riskFreeRate = 0.06
        v0 = 0.2
        kappa = 1.0
        theta = v0
        sigma = 0.0065
        rho = -0.75
        dayCounter = Actual365Fixed()

        maturity = Date(17, May, 2014, 17, 30, 0)

        europeanExercise = EuropeanExercise(maturity)
        payoff = PlainVanillaPayoff(optType, strike)
        option = VanillaOption(payoff, europeanExercise)

        s0 = QuoteHandle(SimpleQuote(underlying))
        flatVolTS = RelinkableBlackVolTermStructureHandle()
        flatTermStructure = RelinkableYieldTermStructureHandle()
        flatDividendTS = RelinkableYieldTermStructureHandle()
        process = HestonProcess(
            flatTermStructure, flatDividendTS, s0,
            v0, kappa, theta, sigma, rho)
        model = HestonModel(process)
        fdm = FdHestonVanillaEngine(model, 20, 100, 26, 0)
        option.setPricingEngine(fdm)

        gammaExpected = [
            1.46757, 1.54696, 1.6408, 1.75409, 1.89464,
            2.07548, 2.32046, 2.67944, 3.28164, 4.64096]

        for i in range(10):
            now = Date(17, May, 2014, 15, i * 15, 0)
            Settings.instance().evaluationDate = now

            flatTermStructure.linkTo(
                FlatForward(now, riskFreeRate, dayCounter))
            flatDividendTS.linkTo(
                FlatForward(now, dividendYield, dayCounter))

            gammaCalculated = option.gamma()
            self.assertFalse(
                abs(gammaCalculated - gammaExpected[i]) > 1e-4)

    def testMethodOfLinesAndCN(self):
        TEST_MESSAGE("Testing method of lines to solve Heston PDEs...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(21, February, 2018)

        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        qTS = YieldTermStructureHandle(flatRate(today, 0.0, dc))
        rTS = YieldTermStructureHandle(flatRate(today, 0.0, dc))

        v0 = 0.09
        kappa = 1.0
        theta = v0
        sigma = 0.4
        rho = -0.75

        maturity = today + Period(3, Months)

        model = HestonModel(
            HestonProcess(
                rTS, qTS, spot, v0, kappa,
                theta, sigma, rho))

        xGrid = 21
        vGrid = 7

        fdmDefault = FdHestonVanillaEngine(
            model, 10, xGrid, vGrid, 0)

        fdmMol = FdHestonVanillaEngine(
            model, 10, xGrid, vGrid, 0,
            FdmSchemeDesc.MethodOfLines())

        payoff = PlainVanillaPayoff(Option.Put, spot.value())

        option = VanillaOption(
            payoff, AmericanExercise(maturity))

        option.setPricingEngine(fdmMol)
        calculatedMoL = option.NPV()

        option.setPricingEngine(fdmDefault)
        expected = option.NPV()

        tol = 0.005
        diffMoL = abs(expected - calculatedMoL)

        self.assertFalse(diffMoL > tol)

        fdmCN = FdHestonVanillaEngine(
            model, 10, xGrid, vGrid, 0,
            FdmSchemeDesc.CrankNicolson())
        option.setPricingEngine(fdmCN)

        calculatedCN = option.NPV()
        diffCN = abs(expected - calculatedCN)

        self.assertFalse(diffCN > tol)

        barrierOption = BarrierOption(
            Barrier.DownOut, 85.0, 10.0,
            payoff, EuropeanExercise(maturity))

        barrierOption.setPricingEngine(
            FdHestonBarrierEngine(model, 100, 31, 11))

        expectedBarrier = barrierOption.NPV()

        barrierOption.setPricingEngine(
            FdHestonBarrierEngine(
                model, 100, 31, 11, 0,
                FdmSchemeDesc.MethodOfLines()))

        calculatedBarrierMoL = barrierOption.NPV()

        barrierTol = 0.01
        barrierDiffMoL = abs(expectedBarrier - calculatedBarrierMoL)

        self.assertFalse(barrierDiffMoL > barrierTol)

        barrierOption.setPricingEngine(
            FdHestonBarrierEngine(
                model, 100, 31, 11, 0,
                FdmSchemeDesc.CrankNicolson()))

        calculatedBarrierCN = barrierOption.NPV()
        barrierDiffCN = abs(expectedBarrier - calculatedBarrierCN)

        self.assertFalse(barrierDiffCN > barrierTol)

    def testSpuriousOscillations(self):
        TEST_MESSAGE(
            "Testing for spurious oscillations when solving the Heston PDEs...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(7, June, 2018)

        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        qTS = YieldTermStructureHandle(flatRate(today, 0.1, dc))
        rTS = YieldTermStructureHandle(flatRate(today, 0.0, dc))

        v0 = 0.005
        kappa = 1.0
        theta = 0.005
        sigma = 0.4
        rho = -0.75

        maturity = today + Period(1, Years)

        process = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        model = HestonModel(process)

        hestonEngine = FdHestonVanillaEngine(
            model, 6, 200, 13, 0, FdmSchemeDesc.TrBDF2())

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, spot.value()),
            EuropeanExercise(maturity))

        option.setupArguments(hestonEngine.getArguments())

        descs = [
            (FdmSchemeDesc.CraigSneyd(), "Craig-Sneyd", True),
            (FdmSchemeDesc.Hundsdorfer(), "Hundsdorfer", True),
            (FdmSchemeDesc.ModifiedHundsdorfer(), "Mod. Hundsdorfer", True),
            (FdmSchemeDesc.Douglas(), "Douglas", True),
            (FdmSchemeDesc.CrankNicolson(), "Crank-Nicolson", True),
            (FdmSchemeDesc.ImplicitEuler(), "Implicit", False),
            (FdmSchemeDesc.TrBDF2(), "TR-BDF2", False)]

        for desc in descs:
            solver = FdmHestonSolver(
                HestonProcessHandle(process),
                hestonEngine.getSolverDesc(1.0),
                desc[0])

            gammas = DoubleVector()
            for x in np.arange(99.0, 101.001, 0.1):
                gammas.push_back(solver.gammaAt(x, v0))

            maximum = QL_MIN_REAL
            for i in range(1, len(gammas)):
                diff = abs(gammas[i] - gammas[i - 1])
                if diff > maximum:
                    maximum = diff

            tol = 0.01
            hasSpuriousOscillations = maximum > tol

            self.assertFalse(hasSpuriousOscillations != desc[2])
