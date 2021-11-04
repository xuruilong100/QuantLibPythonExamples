import unittest
from utilities import *
from QuantLib import *
from math import sqrt, pow, log, exp


class SabrMonteCarloPricer(object):
    def __init__(self,
                 f0,
                 maturity,
                 payoff,
                 alpha,
                 beta,
                 nu,
                 rho):
        self.f0_ = f0
        self.maturity_ = maturity
        self.payoff_ = payoff
        self.alpha_ = alpha
        self.beta_ = beta
        self.nu_ = nu
        self.rho_ = rho

    def __call__(self, dt):
        nSims = 64 * 1024
        timeStepsPerYear = 1. / dt
        timeSteps = int(self.maturity_ * timeStepsPerYear + 1e-8)

        sqrtDt = sqrt(dt)
        w = sqrt(1.0 - self.rho_ * self.rho_)

        logAlpha = log(self.alpha_)

        rsg = SobolBrownianBridgeRsg(
            2, timeSteps,
            SobolBrownianGenerator.Diagonal,
            12345)

        stats = GeneralStatistics()

        for i in range(nSims):
            f = self.f0_
            a = logAlpha

            n = rsg.nextSequence().value()

            for j in range(timeSteps):  # (int j = 0 j < timeSteps && f > 0.0 ++j) [

                r1 = n[j]
                r2 = self.rho_ * r1 + n[j + timeSteps] * w

                # simple Euler method
                f += exp(a) * pow(f, self.beta_) * r1 * sqrtDt
                if f <= 0.0:
                    break
                a += -0.5 * self.nu_ * self.nu_ * dt + self.nu_ * r2 * sqrtDt

            f = max(0.0, f)
            stats.add(self.payoff_(f))

        return stats.mean()


# Example and reference values are taken from
# B. Chen, C.W. Oosterlee, H. Weide,
# Efficient unbiased simulation scheme for the SABR stochastic volatility model.
# https://http://ta.twi.tudelft.nl/mf/users/oosterle/oosterlee/SABRMC.pdf

class OsterleeReferenceResults(object):
    data_ = [
        [0.0610, 0.0604], [0.0468, 0.0463], [0.0347, 0.0343],
        [0.0632, 0.0625], [0.0512, 0.0506], [0.0406, 0.0400],
        [0.0635, 0.0630], [0.0523, 0.0520], [0.0422, 0.0421]]

    def __init__(self, i):
        self.i_ = i

    def __call__(self, t):
        i = None
        if close_enough(t, 1 / 16.):
            i = 0
        elif close_enough(t, 1 / 32.):
            i = 1
        # else
        #     QL_FAIL("unmatched reference result lookup")

        return self.data_[self.i_][i]


class FdSabrTest(unittest.TestCase):
    def testFdmSabrOp(self):
        TEST_MESSAGE("Testing FDM SABR operator...")

        backup = SavedSettings()

        today = Date(22, February, 2018)
        dc = Actual365Fixed()
        Settings.instance().evaluationDate = today

        maturityDate = today + Period(2, Years)
        maturityTime = dc.yearFraction(today, maturityDate)

        strike = 1.5

        exercise = EuropeanExercise(maturityDate)

        putPayoff = PlainVanillaPayoff(Option.Put, strike)
        callPayoff = PlainVanillaPayoff(Option.Call, strike)

        optionPut = VanillaOption(putPayoff, exercise)
        optionCall = VanillaOption(callPayoff, exercise)

        rTS = YieldTermStructureHandle(flatRate(today, 0.0, dc))

        f0 = 1.0
        alpha = 0.35
        nu = 1.0
        rho = 0.25

        betas = [0.25, 0.6]

        bsProcess = GeneralizedBlackScholesProcess(
            QuoteHandle(SimpleQuote(f0)),
            rTS, rTS, BlackVolTermStructureHandle(flatVol(0.2, dc)))

        for beta in betas:
            pdeEngine = FdSabrVanillaEngine(
                f0, alpha, beta, nu, rho, rTS, 100, 400, 100)

            optionPut.setPricingEngine(pdeEngine)
            pdePut = optionPut.NPV()

            # check put/call parity
            optionCall.setPricingEngine(pdeEngine)
            pdeCall = optionCall.NPV()

            pdeFwd = pdeCall - pdePut

            parityDiff = abs(pdeFwd - (f0 - strike))
            parityTol = 1e-4
            self.assertFalse(parityDiff > parityTol)

            putPdeImplVol = optionPut.impliedVolatility(
                optionPut.NPV(), bsProcess, 1e-6)

            mcSabr = SabrMonteCarloPricer(
                f0, maturityTime, putPayoff,
                alpha, beta, nu, rho)

            mcNPV = RichardsonExtrapolation(
                mcSabr, 1 / 4.0)(4.0, 2.0)

            putMcImplVol = optionPut.impliedVolatility(
                mcNPV, bsProcess, 1e-6)

            volDiff = abs(putPdeImplVol - putMcImplVol)

            volTol = 5e-3
            self.assertFalse(volDiff > volTol)

    def testFdmSabrCevPricing(self):
        TEST_MESSAGE("Testing FDM CEV pricing with trivial SABR model...")

        backup = SavedSettings()

        today = Date(3, January, 2019)
        dc = Actual365Fixed()
        Settings.instance().evaluationDate = today

        maturityDate = today + Period(12, Months)

        betas = [0.1, 0.9]
        strikes = [0.9, 1.5]

        f0 = 1.2
        alpha = 0.35
        nu = 1e-3
        rho = 0.25

        rTS = YieldTermStructureHandle(flatRate(today, 0.05, dc))

        exercise = EuropeanExercise(maturityDate)

        optionTypes = [Option.Put, Option.Call]

        tol = 5e-5

        for optionType in optionTypes:
            for strike in strikes:
                payoff = PlainVanillaPayoff(optionType, strike)
                option = VanillaOption(payoff, exercise)

                for beta in betas:
                    option.setPricingEngine(
                        FdSabrVanillaEngine(
                            f0, alpha, beta, nu, rho, rTS, 100, 400, 3))

                    calculated = option.NPV()

                    option.setPricingEngine(
                        AnalyticCEVEngine(
                            f0, alpha, beta, rTS))

                    expected = option.NPV()

                    self.assertFalse(abs(expected - calculated) > tol)

    def testFdmSabrVsVolApproximation(self):
        TEST_MESSAGE("Testing FDM SABR vs approximations...")

        backup = SavedSettings()

        today = Date(8, January, 2019)
        dc = Actual365Fixed()
        Settings.instance().evaluationDate = today

        maturityDate = today + Period(6, Months)
        maturityTime = dc.yearFraction(today, maturityDate)

        rTS = YieldTermStructureHandle(flatRate(today, 0.05, dc))

        f0 = 100

        bsProcess = GeneralizedBlackScholesProcess(
            QuoteHandle(SimpleQuote(f0)),
            rTS, rTS,
            BlackVolTermStructureHandle(flatVol(0.2, dc)))

        alpha = 0.35
        beta = 0.85
        nu = 0.75
        rho = 0.85

        strikes = [90, 100, 110]
        optionTypes = [Option.Put, Option.Call]

        tol = 2.5e-3
        for optionType in optionTypes:
            for strike in strikes:
                option = VanillaOption(
                    PlainVanillaPayoff(optionType, strike),
                    EuropeanExercise(maturityDate))

                option.setPricingEngine(
                    FdSabrVanillaEngine(
                        f0, alpha, beta, nu, rho, rTS, 25, 100, 50))

                fdmVol = option.impliedVolatility(option.NPV(), bsProcess)

                hagenVol = sabrVolatility(
                    strike, f0, maturityTime, alpha, beta, nu, rho)

                diff = abs(fdmVol - hagenVol)

                self.assertFalse(abs(fdmVol - hagenVol) > tol)

    def testOosterleeTestCaseIV(self):
        TEST_MESSAGE("Testing Chen, Oosterlee and Weide test case IV...")

        backup = SavedSettings()

        today = Date(8, January, 2019)
        dc = Actual365Fixed()
        Settings.instance().evaluationDate = today

        rTS = YieldTermStructureHandle(flatRate(today, 0.0, dc))

        f0 = 0.07
        alpha = 0.4
        nu = 0.8
        beta = 0.4
        rho = -0.6

        maturities = [
            Period(2, Years), Period(5, Years), Period(10, Years)]

        strikes = [0.4 * f0, f0, 1.6 * f0]

        tol = 0.00035
        for i in range(len(maturities)):
            maturityDate = today + maturities[i]
            maturityTime = dc.yearFraction(today, maturityDate)

            timeSteps = int(5 * maturityTime)

            engine = FdSabrVanillaEngine(
                f0, alpha, beta, nu, rho, rTS, timeSteps, 200, 21)

            exercise = EuropeanExercise(maturityDate)

            for j in range(len(strikes)):
                payoff = PlainVanillaPayoff(Option.Call, strikes[j])

                option = VanillaOption(payoff, exercise)
                option.setPricingEngine(engine)

                calculated = option.NPV()

                referenceResuts = OsterleeReferenceResults(i * 3 + j)

                expected = RichardsonExtrapolation(
                    referenceResuts, 1 / 16., 1)(2.)

                diff = abs(calculated - expected)
                self.assertFalse(diff > tol)

    def testBenchOpSabrCase(self):
        TEST_MESSAGE("Testing SABR BenchOp problem...")

        # von Sydow, L, Milovanović, S, Larsson, E, In't Hout, K,
        # Wiktorsson, M, Oosterlee, C.W, Shcherbakov, V, Wyns, M,
        # Leitao Rodriguez, A, Jain, S, et al. (2018)
        # BENCHOP–SLV: the BENCHmarking project in Option
        # Pricing–Stochastic and Local Volatility problems
        # https://ir.cwi.nl/pub/28249

        backup = SavedSettings()

        today = Date(8, January, 2019)
        dc = Actual365Fixed()
        Settings.instance().evaluationDate = today

        rTS = YieldTermStructureHandle(flatRate(today, 0.0, dc))

        maturityInYears = [2, 10]

        f0s = [0.5, 0.07]
        alphas = [0.5, 0.4]
        nus = [0.4, 0.8]
        betas = [0.5, 0.5]
        rhos = [0.0, -0.6]

        expected = [
            [0.221383196830866, 0.193836689413803, 0.166240814653231],
            [0.052450313614407, 0.046585753491306, 0.039291470612989]]

        gridX = 400
        gridY = 25
        gridT = 10
        factor = 2
        tol = 2e-4

        for i in range(len(f0s)):

            maturity = today + Period(maturityInYears[i] * 365, Days)
            T = dc.yearFraction(today, maturity)

            f0 = f0s[i]
            alpha = alphas[i]
            nu = nus[i]
            beta = betas[i]
            rho = rhos[i]

            strikes = [
                f0 * exp(-0.1 * sqrt(T)), f0, f0 * exp(0.1 * sqrt(T))]

            for j in range(len(strikes)):
                strike = strikes[j]

                option = VanillaOption(
                    PlainVanillaPayoff(Option.Call, strike),
                    EuropeanExercise(maturity))

                option.setPricingEngine(
                    FdSabrVanillaEngine(
                        f0, alpha, beta, nu, rho, rTS,
                        int(gridT * factor),
                        int(gridX * factor),
                        int(gridY * sqrt(factor))))

                calculated = option.NPV()
                diff = abs(calculated - expected[i][j])

                self.assertFalse(diff > tol)
