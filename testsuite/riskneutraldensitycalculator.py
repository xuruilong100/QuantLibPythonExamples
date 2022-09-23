import unittest
from math import exp, sqrt, log, pow

import numpy as np
from QuantLib import *

from utilities import *


class SquareRootProcessParams(object):
    def __init__(self,
                 v0,
                 kappa,
                 theta,
                 sigma):
        self.v0 = v0
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma


class DumasParametricVolSurface(object):
    def __init__(self,
                 b1,
                 b2,
                 b3,
                 b4,
                 b5,
                 spot,
                 rTS,
                 qTS):
        self.b1_ = b1
        self.b2_ = b2
        self.b3_ = b3
        self.b4_ = b4
        self.b5_ = b5
        self.spot_ = spot
        self.rTS_ = rTS
        self.qTS_ = qTS

    def __call__(self, t, strike):
        if t < QL_EPSILON:
            return self.b1_

        fwd = self.spot_.value() * self.qTS_.discount(t) / self.rTS_.discount(t)
        mn = log(fwd / strike) / sqrt(t)

        v = self.b1_ + self.b2_ * mn + self.b3_ * mn * mn + \
            self.b4_ * t + self.b5_ * mn * t

        return v


def adaptiveTimeGrid(maxStepsPerYear,
                     minStepsPerYear,
                     decay,
                     endTime):
    maxDt = 1.0 / maxStepsPerYear
    minDt = 1.0 / minStepsPerYear

    t = 0.0
    times = DoubleVector(1, t)
    while t < endTime:
        dt = maxDt * exp(-decay * t) + minDt * (1.0 - exp(-decay * t))
        t += dt
        times.push_back(min(endTime, t))

    return times


class ProbWeightedPayoff(object):
    def __init__(self,
                 t,
                 payoff,
                 calc):
        self.t_ = t
        self.payoff_ = payoff
        self.calc_ = calc

    def __call__(self, x):
        return self.calc_.pdf(x, self.t_) * self.payoff_(exp(x))


class RiskNeutralDensityCalculatorTest(unittest.TestCase):

    def testDensityAgainstOptionPrices(self):
        TEST_MESSAGE(
            "Testing density against option prices...")

        backup = SavedSettings()

        dayCounter = Actual365Fixed()
        todaysDate = Settings.instance().evaluationDate

        s0 = 100
        spot = QuoteHandle(
            SimpleQuote(s0))

        r = 0.075
        q = 0.04
        v = 0.27

        rTS = YieldTermStructureHandle(flatRate(todaysDate, r, dayCounter))
        qTS = YieldTermStructureHandle(flatRate(todaysDate, q, dayCounter))

        bsmProcess = BlackScholesMertonProcess(
            spot, qTS, rTS,
            BlackVolTermStructureHandle(
                flatVol(v, dayCounter)))

        bsm = BSMRNDCalculator(bsmProcess)
        times = [0.5, 1.0, 2.0]
        strikes = [75.0, 100.0, 150.0]

        for t in times:
            stdDev = v * sqrt(t)
            df = rTS.discount(t)
            fwd = s0 * qTS.discount(t) / df

            for strike in strikes:
                xs = log(strike)
                blackCalc = BlackCalculator(
                    Option.Put, strike, fwd, stdDev, df)

                tol = 10 * sqrt(QL_EPSILON)
                calculatedCDF = bsm.cdf(xs, t)
                expectedCDF = blackCalc.strikeSensitivity() / df

                self.assertFalse(abs(calculatedCDF - expectedCDF) > tol)

                deltaStrike = strike * sqrt(QL_EPSILON)

                calculatedPDF = bsm.pdf(xs, t)
                expectedPDF = strike / df * (
                        BlackCalculator(
                            Option.Put, strike + deltaStrike,
                            fwd, stdDev, df).strikeSensitivity() -
                        BlackCalculator(
                            Option.Put, strike - deltaStrike,
                            fwd, stdDev, df).strikeSensitivity()) / \
                              (2 * deltaStrike)

                self.assertFalse(abs(calculatedPDF - expectedPDF) > tol)

    def testBSMagainstHestonRND(self):
        TEST_MESSAGE(
            "Testing Black-Scholes-Merton and Heston densities...")

        backup = SavedSettings()

        dayCounter = Actual365Fixed()
        todaysDate = Settings.instance().evaluationDate

        s0 = 10
        spot = QuoteHandle(SimpleQuote(s0))

        r = 0.155
        q = 0.0721
        v = 0.27

        kappa = 1.0
        theta = v * v
        rho = -0.75
        v0 = v * v
        sigma = 0.0001

        rTS = YieldTermStructureHandle(flatRate(todaysDate, r, dayCounter))
        qTS = YieldTermStructureHandle(flatRate(todaysDate, q, dayCounter))

        bsmProcess = BlackScholesMertonProcess(
            spot, qTS, rTS,
            BlackVolTermStructureHandle(
                flatVol(v, dayCounter)))

        bsm = BSMRNDCalculator(bsmProcess)
        heston = HestonRNDCalculator(
            HestonProcess(
                rTS, qTS, spot,
                v0, kappa, theta, sigma, rho), 1e-8)

        times = [0.5, 1.0, 2.0]
        strikes = [7.5, 10, 15]
        probs = [1e-6, 0.01, 0.5, 0.99, 1.0 - 1e-6]

        for t in times:
            for strike in strikes:
                xs = log(strike)

                expectedPDF = bsm.pdf(xs, t)
                calculatedPDF = heston.pdf(xs, t)

                tol = 1e-4
                self.assertFalse(abs(expectedPDF - calculatedPDF) > tol)

                expectedCDF = bsm.cdf(xs, t)
                calculatedCDF = heston.cdf(xs, t)

                self.assertFalse(abs(expectedCDF - calculatedCDF) > tol)

            for prob in probs:
                expectedInvCDF = bsm.invcdf(prob, t)
                calculatedInvCDF = heston.invcdf(prob, t)

                tol = 1e-3
                self.assertFalse(abs(expectedInvCDF - calculatedInvCDF) > tol)

    def testLocalVolatilityRND(self):
        TEST_MESSAGE(
            "Testing Fokker-Planck forward equation for local "
            "volatility process to calculate risk neutral densities...")

        backup = SavedSettings()

        dayCounter = Actual365Fixed()
        todaysDate = Date(28, Dec, 2012)
        Settings.instance().evaluationDate = todaysDate

        r = 0.015
        q = 0.025
        s0 = 100
        v = 0.25

        spot = SimpleQuote(s0)
        rTS = flatRate(todaysDate, r, dayCounter)
        qTS = flatRate(todaysDate, q, dayCounter)

        timeGrid = TimeGrid(1.0, 101)

        constVolCalc = LocalVolRNDCalculator(
            spot, rTS, qTS,
            LocalConstantVol(todaysDate, v, dayCounter),
            timeGrid, 201)

        rTol = 0.01
        atol = 0.005
        for t in np.arange(0.1, 0.99, 0.015):
            stdDev = v * sqrt(t)
            xm = -0.5 * stdDev * stdDev + log(s0 * qTS.discount(t) / rTS.discount(t))

            gaussianPDF = NormalDistribution(xm, stdDev)
            gaussianCDF = CumulativeNormalDistribution(xm, stdDev)
            gaussianInvCDF = InverseCumulativeNormal(xm, stdDev)

            for x in np.arange(xm - 3 * stdDev, xm + 3 * stdDev, 0.05):
                expectedPDF = gaussianPDF(x)
                calculatedPDF = constVolCalc.pdf(x, t)
                absDiffPDF = abs(expectedPDF - calculatedPDF)

                self.assertFalse(
                    absDiffPDF > atol or absDiffPDF / expectedPDF > rTol)

                expectedCDF = gaussianCDF(x)
                calculatedCDF = constVolCalc.cdf(x, t)
                absDiffCDF = abs(expectedCDF - calculatedCDF)

                self.assertFalse(absDiffCDF > atol)

                expectedX = x
                calculatedX = constVolCalc.invcdf(expectedCDF, t)
                absDiffX = abs(expectedX - calculatedX)

                self.assertFalse(
                    absDiffX > atol or absDiffX / expectedX > rTol)

        tl = timeGrid.at(len(timeGrid) - 5)
        xl = constVolCalc.mesher(tl).locations()[0]
        self.assertFalse(
            not (constVolCalc.pdf(xl + 0.0001, tl) > 0.0 and
                 constVolCalc.pdf(xl - 0.0001, tl) == 0.0))

        b1 = 0.25
        b2 = 0.03
        b3 = 0.005
        b4 = -0.02
        b5 = -0.005

        blackVolImpl = DumasParametricVolSurface(
            b1, b2, b3, b4, b5, spot, rTS, qTS)

        dumasVolSurface = CustomBlackVolatility(
            blackVolImpl,
            0, NullCalendar(), Following,
            rTS.dayCounter())

        bsmProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(dumasVolSurface))

        localVolSurface = NoExceptLocalVolSurface(
            BlackVolTermStructureHandle(dumasVolSurface),
            YieldTermStructureHandle(rTS),
            YieldTermStructureHandle(qTS),
            QuoteHandle(spot), b1)

        adaptiveGrid = adaptiveTimeGrid(400, 50, 5.0, 3.0)

        dumasTimeGrid = TimeGrid(adaptiveGrid)

        dumasVolCalc = LocalVolRNDCalculator(
            spot, rTS, qTS, localVolSurface,
            dumasTimeGrid, 401, 0.1, 1e-8)

        strikes = [25, 50, 95, 100, 105, 150, 200, 400]
        maturities = [
            todaysDate + Period(1, Weeks), todaysDate + Period(1, Months),
            todaysDate + Period(3, Months), todaysDate + Period(6, Months),
            todaysDate + Period(12, Months), todaysDate + Period(18, Months),
            todaysDate + Period(2, Years), todaysDate + Period(3, Years)]

        for maturity in maturities:
            expiry = rTS.dayCounter().yearFraction(todaysDate, maturity)

            engine = FdBlackScholesVanillaEngine(
                bsmProcess, max(51, int(expiry * 101)),
                201, 0, FdmSchemeDesc.Douglas(), true, b1)

            exercise = EuropeanExercise(maturity)

            for strike in strikes:
                payoff = PlainVanillaPayoff(
                    Option.Call if strike > spot.value() else Option.Put, strike)

                option = VanillaOption(payoff, exercise)
                option.setPricingEngine(engine)
                expected = option.NPV()

                tx = max(
                    dumasTimeGrid.at(1),
                    dumasTimeGrid.closestTime(expiry))
                x = dumasVolCalc.mesher(tx).locations()

                probWeightedPayoff = ProbWeightedPayoff(
                    expiry, payoff, dumasVolCalc)

                df = rTS.discount(expiry)
                calculated = GaussLobattoIntegral(10000, 1e-10)(
                    probWeightedPayoff, x[0], x[-1]) * df

                absDiff = abs(expected - calculated)

                self.assertFalse(absDiff > 0.5 * atol)

    def testSquareRootProcessRND(self):
        TEST_MESSAGE(
            "Testing probability density for a square root process...")

        params = [
            SquareRootProcessParams(0.17, 1.0, 0.09, 0.5),
            SquareRootProcessParams(1.0, 0.6, 0.1, 0.75),
            SquareRootProcessParams(0.005, 0.6, 0.1, 0.05)]

        for param in params:
            rndCalculator = SquareRootProcessRNDCalculator(
                param.v0, param.kappa, param.theta, param.sigma)

            t = 0.75
            tInfty = 60.0 / param.kappa

            tol = 1e-10

            v = 1e-5
            while v < 1.0:

                cdfCalculated = rndCalculator.cdf(v, t)
                cdfExpected = GaussLobattoIntegral(10000, 0.01 * tol)(
                    lambda x: rndCalculator.pdf(x, t), 0, v)

                self.assertFalse(abs(cdfCalculated - cdfExpected) > tol)
                if cdfExpected < (1 - 1e-6) and cdfExpected > 1e-6:
                    vCalculated = rndCalculator.invcdf(cdfCalculated, t)
                    self.assertFalse(abs(v - vCalculated) > tol)

                statPdfCalculated = rndCalculator.pdf(v, tInfty)
                statPdfExpected = rndCalculator.stationary_pdf(v)

                self.assertFalse(abs(statPdfCalculated - statPdfExpected) > tol)

                statCdfCalculated = rndCalculator.cdf(v, tInfty)
                statCdfExpected = rndCalculator.stationary_cdf(v)

                self.assertFalse(abs(statCdfCalculated - statCdfExpected) > tol)

                v += 0.005 if v < param.theta else 0.1

            for q in np.arange(1e-5, 1.0, 0.001):
                statInvCdfCalculated = rndCalculator.invcdf(q, tInfty)
                statInvCdfExpected = rndCalculator.stationary_invcdf(q)

                self.assertFalse(abs(statInvCdfCalculated - statInvCdfExpected) > tol)

    def testMassAtZeroCEVProcessRND(self):
        TEST_MESSAGE(
            "Testing the mass at zero for a "
            "constant elasticity of variance (CEV) process...")

        f0 = 100.0
        t = 2.75

        params = [
            [0.1, 1.6],
            [0.01, 2.0],
            [10.0, 0.35],
            [50.0, 0.1]]

        tol = 1e-4

        for param in params:
            alpha = param[0]
            beta = param[1]

            calculator = CEVRNDCalculator(f0, alpha, beta)

            ax = 15.0 * sqrt(t) * alpha * pow(f0, beta)

            calculated = GaussLobattoIntegral(1000, 1e-8)(
                lambda x: calculator.pdf(x, t),
                max(QL_EPSILON, f0 - ax), f0 + ax) + calculator.massAtZero(t)

            self.assertFalse(abs(calculated - 1.0) > tol)

    def testCEVCDF(self):
        TEST_MESSAGE(
            "Testing CDF for a constant elasticity of variance (CEV) process...")

        f0 = 2.1
        t = 0.75

        alpha = 0.1
        betas = [0.45, 1.25]

        tol = 1e-6
        for i in range(1, len(betas)):
            beta = betas[i]
            calculator = CEVRNDCalculator(f0, alpha, beta)

            for x in np.arange(1.3, 3.1, 0.1):
                cdfValue = calculator.cdf(x, t)
                calculated = calculator.invcdf(cdfValue, t)

                self.assertFalse(abs(x - calculated) > tol)

    def testBlackScholesWithSkew(self):
        TEST_MESSAGE(
            "Testing probability density for a BSM process "
            "with strike dependent volatility vs local volatility...")

        backup = SavedSettings()

        todaysDate = Date(3, Oct, 2016)
        Settings.instance().evaluationDate = todaysDate

        dc = Actual365Fixed()
        maturityDate = todaysDate + Period(3, Months)
        maturity = dc.yearFraction(todaysDate, maturityDate)

        r = 0.08
        q = 0.03
        s0 = 100
        v0 = 0.06
        kappa = 1.0
        theta = 0.06
        sigma = 0.4
        rho = -0.75

        rTS = YieldTermStructureHandle(flatRate(todaysDate, r, dc))
        qTS = YieldTermStructureHandle(flatRate(todaysDate, q, dc))
        spot = QuoteHandle(SimpleQuote(s0))

        hestonProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        hestonSurface = BlackVolTermStructureHandle(
            HestonBlackVolSurface(
                HestonModelHandle(HestonModel(hestonProcess)),
                AnalyticHestonEngine.AndersenPiterbarg,
                AnalyticHestonEngineIntegration.discreteTrapezoid(64)))

        timeGrid = TimeGrid(maturity, 51)

        localVol = NoExceptLocalVolSurface(
            hestonSurface, rTS, qTS, spot, sqrt(theta))

        localVolCalc = LocalVolRNDCalculator(
            spot.currentLink(), rTS.currentLink(),
            qTS.currentLink(), localVol,
            timeGrid, 151, 0.25)

        hestonCalc = HestonRNDCalculator(hestonProcess)

        gbsmCalc = GBSMRNDCalculator(
            BlackScholesMertonProcess(
                spot, qTS, rTS, hestonSurface))

        strikes = [85, 75, 90, 110, 125, 150]

        for strike in strikes:
            logStrike = log(strike)

            expected = hestonCalc.cdf(logStrike, maturity)
            calculatedGBSM = gbsmCalc.cdf(strike, maturity)

            gbsmTol = 1e-5
            self.assertFalse(abs(expected - calculatedGBSM) > gbsmTol)

            calculatedLocalVol = localVolCalc.cdf(logStrike, maturity)
            localVolTol = 1e-3
            self.assertFalse(abs(expected - calculatedLocalVol) > localVolTol)

        for strike in strikes:
            logStrike = log(strike)

            expected = hestonCalc.pdf(logStrike, maturity) / strike
            calculatedGBSM = gbsmCalc.pdf(strike, maturity)

            gbsmTol = 1e-5
            self.assertFalse(abs(expected - calculatedGBSM) > gbsmTol)

            calculatedLocalVol = localVolCalc.pdf(logStrike, maturity) / strike
            localVolTol = 1e-4
            self.assertFalse(abs(expected - calculatedLocalVol) > localVolTol)

        quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]
        for quantile in quantiles:
            expected = exp(hestonCalc.invcdf(quantile, maturity))
            calculatedGBSM = gbsmCalc.invcdf(quantile, maturity)

            gbsmTol = 1e-3
            self.assertFalse(abs(expected - calculatedGBSM) > gbsmTol)

            calculatedLocalVol = exp(localVolCalc.invcdf(quantile, maturity))
            localVolTol = 0.1
            self.assertFalse(abs(expected - calculatedLocalVol) > localVolTol)
