import unittest
from math import log, sqrt

from QuantLib import *

from utilities import *


class NormalCLVModelTest(unittest.TestCase):

    def testBSCumlativeDistributionFunction(self):
        TEST_MESSAGE(
            "Testing Black-Scholes cumulative distribution function with constant volatility...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(22, June, 2016)
        Settings.instance().evaluationDate = today
        maturity = today + Period(6, Months)

        s0 = 100
        rRate = 0.1
        qRate = 0.05
        vol = 0.25

        spot = QuoteHandle(SimpleQuote(s0))
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, volTS)

        m = NormalCLVModel(
            bsProcess, DateVector(), 5)
        rndCalculator = BSMRNDCalculator(bsProcess)

        tol = 1e5 * QL_EPSILON
        t = dc.yearFraction(today, maturity)
        for x in range(10, 400, 10):
            calculated = m.cdf(maturity, x)
            expected = rndCalculator.cdf(log(x), t)

            self.assertFalse(abs(calculated - expected) > tol)

    def testHestonCumlativeDistributionFunction(self):
        TEST_MESSAGE(
            "Testing Heston cumulative distribution function...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(22, June, 2016)
        Settings.instance().evaluationDate = today
        maturity = today + Period(1, Years)

        s0 = 100
        v0 = 0.01
        rRate = 0.1
        qRate = 0.05
        kappa = 2.0
        theta = 0.09
        sigma = 0.4
        rho = -0.75

        spot = QuoteHandle(SimpleQuote(s0))
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))

        process = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        hestonVolTS = BlackVolTermStructureHandle(
            HestonBlackVolSurface(
                HestonModelHandle(HestonModel(process))))

        m = NormalCLVModel(
            GeneralizedBlackScholesProcess(
                spot, qTS, rTS, hestonVolTS),
            DateVector(), 5)

        rndCalculator = HestonRNDCalculator(process)

        tol = 1e-6
        t = dc.yearFraction(today, maturity)
        for x in range(10, 400, 25):
            calculated = m.cdf(maturity, x)
            expected = rndCalculator.cdf(log(x), t)

            self.assertFalse(abs(calculated - expected) > tol)

    def testIllustrative1DExample(self):
        TEST_MESSAGE(
            "Testing illustrative 1D example of normal CLV model...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(22, June, 2016)
        Settings.instance().evaluationDate = today

        beta = 0.5
        alpha = 0.2
        rho = -0.9
        gamma = 0.2

        speed = 1.3
        level = 0.1
        vol = 0.25
        x0 = 1.0

        s0 = 1.0
        rRate = 0.03
        qRate = 0.0

        spot = QuoteHandle(SimpleQuote(s0))
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))

        sabrVol = BlackVolTermStructureHandle(
            SABRVolTermStructure(
                alpha, beta, gamma, rho, s0, rRate, today, dc))

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, sabrVol)

        ouProcess = OrnsteinUhlenbeckProcess(
            speed, vol, x0, level)

        maturityDates = [
            today + Period(18, Days),
            today + Period(90, Days),
            today + Period(180, Days),
            today + Period(360, Days),
            today + Period(720, Days)]

        m = NormalCLVModel(bsProcess, ouProcess, maturityDates, 4)

        maturities = [maturityDates[0], maturityDates[2], maturityDates[4]]

        x = [[1.070, 0.984, 0.903, 0.817],
             [0.879, 0.668, 0.472, 0.261],
             [0.528, 0.282, 0.052, -0.194]]

        s = [[1.104, 1.035, 0.969, 0.895],
             [1.328, 1.122, 0.911, 0.668],
             [1.657, 1.283, 0.854, 0.339]]

        c = [2.3344, 0.7420, -0.7420, -2.3344]

        tol = 0.001
        for i in range(len(maturities)):
            t = dc.yearFraction(today, maturities[i])

            for j in range(len(x[0])):
                calculatedX = m.collocationPointsX(maturities[i])[j]
                expectedX = x[i][j]

                self.assertFalse(abs(calculatedX - expectedX) > tol)

                calculatedS = m.collocationPointsY(maturities[i])[j]
                expectedS = s[i][j]
                self.assertFalse(abs(calculatedS - expectedS) > tol)

                expectation = ouProcess.expectation(0.0, ouProcess.x0(), t)
                stdDeviation = ouProcess.stdDeviation(0.0, ouProcess.x0(), t)

                calculatedG = m.g(t, expectation + stdDeviation * c[j])
                self.assertFalse(abs(calculatedG - expectedS) > tol)

    def testMonteCarloBSOptionPricing(self):
        TEST_MESSAGE(
            "Testing Monte Carlo BS option pricing...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(22, June, 2016)
        Settings.instance().evaluationDate = today
        maturity = today + Period(1, Years)
        t = dc.yearFraction(today, maturity)

        strike = 110
        payoff = PlainVanillaPayoff(Option.Call, strike)
        exercise = EuropeanExercise(maturity)

        speed = 2.3
        level = 100
        sigma = 0.35
        x0 = 100.0

        s0 = x0
        vol = 0.25
        rRate = 0.10
        qRate = 0.04

        spot = QuoteHandle(SimpleQuote(s0))
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, vTS)

        ouProcess = OrnsteinUhlenbeckProcess(
            speed, sigma, x0, level)

        maturities = [today + Period(6, Months), maturity]

        m = NormalCLVModel(bsProcess, ouProcess, maturities, 8)

        nSims = 32767

        ld = InvCumulativeSobolGaussianRsg(SobolRsg(1, 23455))

        stat = RiskStatistics()
        for i in range(nSims):
            dw = ld.nextSequence().value()[0]

            o_t = ouProcess.evolve(0, x0, t, dw)
            s = m.g(t, o_t)

            stat.add(payoff(s))

        calculated = stat.mean() * rTS.discount(maturity)

        option = VanillaOption(payoff, exercise)
        option.setPricingEngine(
            AnalyticEuropeanEngine(bsProcess))
        expected = option.NPV()

        tol = 0.01
        self.assertFalse(abs(calculated - expected) > tol)

        fdmOption = VanillaOption(
            CustomCLVModelPayoff(
                lambda _x: m.g(t, _x),
                payoff.optionType(),
                payoff.strike()),
            exercise)

        fdmOption.setPricingEngine(
            FdOrnsteinUhlenbeckVanillaEngine(
                ouProcess, rTS.currentLink(), 50, 800))

        calculated = fdmOption.NPV()
        self.assertFalse(abs(calculated - expected) > tol)

    @unittest.skipIf(skipSlowTest, "testMoustacheGraph is VERY SLOW")
    def testMoustacheGraph(self):
        TEST_MESSAGE(
            "Testing no-touch pricing with normal CLV model...")

        backup = SavedSettings()

        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(5, Aug, 2016)
        maturityDate = todaysDate + Period(1, Years)
        maturityTime = dc.yearFraction(todaysDate, maturityDate)

        Settings.instance().evaluationDate = todaysDate

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))
        r = 0.02
        q = 0.01

        kappa = 1.0
        theta = 0.06
        rho = -0.8
        sigma = 0.8
        v0 = 0.09

        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        hestonModel = HestonModel(
            HestonProcess(
                rTS, qTS, spot, v0, kappa, theta, sigma, rho))

        vTS = BlackVolTermStructureHandle(
            HestonBlackVolSurface(
                HestonModelHandle(hestonModel)))

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, vTS)

        speed = -0.80
        level = 100
        sigmaOU = 0.15
        x0 = 100

        ouProcess = OrnsteinUhlenbeckProcess(
            speed, sigmaOU, x0, level)

        europeanExercise = EuropeanExercise(maturityDate)

        vanillaOption = VanillaOption(
            PlainVanillaPayoff(Option.Call, s0),
            europeanExercise)

        vanillaOption.setPricingEngine(
            AnalyticHestonEngine(hestonModel))

        atmVol = vanillaOption.impliedVolatility(
            vanillaOption.NPV(),
            GeneralizedBlackScholesProcess(
                spot, qTS, rTS,
                BlackVolTermStructureHandle(
                    flatVol(sqrt(theta), dc))))

        analyticEngine = AnalyticDoubleBarrierBinaryEngine(
            GeneralizedBlackScholesProcess(
                spot, qTS, rTS,
                BlackVolTermStructureHandle(
                    flatVol(atmVol, dc))))

        maturities = DateVector(1, todaysDate + Period(2, Weeks))
        while maturities.back() < maturityDate:
            maturities.append(maturities.back() + Period(2, Weeks))

        m = NormalCLVModel(bsProcess, ouProcess, maturities, 8)

        n = 18
        barrier_lo = Array(n)
        barrier_hi = Array(n)
        bsNPV = Array(n)

        payoff = CashOrNothingPayoff(Option.Call, 0.0, 1.0)

        for i in range(n):
            dist = 10.0 + 5.0 * i

            barrier_lo[i] = max(s0 - dist, 1e-2)
            barrier_hi[i] = s0 + dist
            doubleBarrier = DoubleBarrierOption(
                DoubleBarrier.KnockOut, barrier_lo[i], barrier_hi[i], 0.0,
                payoff,
                europeanExercise)

            doubleBarrier.setPricingEngine(analyticEngine)
            bsNPV[i] = doubleBarrier.NPV()

        factors = 1
        tSteps = 200
        grid = TimeGrid(maturityTime, tSteps)

        pathGenerator = BrownianBridgeSobolPathGenerator(
            ouProcess, grid, SobolBrownianBridgeRsg(factors, tSteps), false)

        nSims = 100000

        stats = [GeneralStatistics() for i in range(n)]
        df = rTS.discount(maturityDate)

        for i in range(nSims):
            touch = BoolVector(n, false)

            path = pathGenerator.next()
            s = 0.0
            for j in range(1, tSteps + 1):
                t = grid.at(j)
                s = m.g(t, path.value()[j])

                for u in range(n):
                    if s <= barrier_lo[u] or s >= barrier_hi[u]:
                        touch[u] = true

            for u in range(n):
                if touch[u]:
                    stats[u].add(0.0)

                else:
                    stats[u].add(df * payoff(s))

        expected = [
            0.00931214, 0.0901481, 0.138982, 0.112059, 0.0595901,
            0.0167549, -0.00906787, -0.0206768, -0.0225628, -0.0203593,
            -0.016036, -0.0116629, -0.00728792, -0.00328821,
            -0.000158562, 0.00502041, 0.00347706, 0.00238216]

        tol = 1e-5
        for u in range(n):
            calculated = stats[u].mean() - bsNPV[u]

            self.assertFalse(abs(calculated - expected[u]) > tol)
