import unittest
from math import sqrt, pow

from QuantLib import *

from utilities import *


class ExpectationFct(object):
    def __init__(self, calculator, t):
        self.calculator_ = calculator
        self.t_ = t

    def __call__(self, f):
        return f * self.calculator_.pdf(f, self.t_)


class FdCevTest(unittest.TestCase):

    def testLocalMartingale(self):
        TEST_MESSAGE(
            "Testing local martingale property of CEV process with PDF...")

        t = 1.0

        f0 = 2.1
        alpha = 1.75
        betas = [-2.4, 0.23, 0.9, 1.1, 1.5]

        for beta in betas:
            rndCalculator = CEVRNDCalculator(f0, alpha, beta)

            eps = 1e-10
            tol = 100 * eps

            upperBound = 10 * rndCalculator.invcdf(1 - eps, t)

            expectationValue = GaussLobattoIntegral(10000, eps)(
                ExpectationFct(rndCalculator, t), QL_EPSILON, upperBound)

            diff = expectationValue - f0

            self.assertFalse(beta < 1.0 and abs(diff) > tol)
            self.assertFalse(beta > 1.0 and diff > -tol)

            nSims = 5000
            nSteps = 2000
            dt = t / nSteps
            sqrtDt = sqrt(dt)

            stat = GeneralStatistics()
            mt = InvCumulativeMersenneTwisterGaussianRng(
                MersenneTwisterUniformRng(42))

            if beta > 1.2:
                for i in range(nSims):
                    f = f0
                    for j in range(nSteps):
                        f += alpha * pow(f, beta) * mt.next().value() * sqrtDt
                        f = max(0.0, f)

                        if f == 0.0:
                            break

                    stat.add(f - f0)

                calculated = stat.mean()
                error = stat.errorEstimate()

                self.assertFalse(abs(calculated - diff) > 2.35 * error)

    def testFdmCevOp(self):
        TEST_MESSAGE(
            "Testing FDM constant elasticity of variance (CEV) operator...")

        backup = SavedSettings()

        today = Date(22, February, 2018)
        dc = Actual365Fixed()
        Settings.instance().evaluationDate = today

        maturityDate = today + Period(12, Months)
        strike = 2.3

        optionTypes = [Option.Call, Option.Put]

        exercise = EuropeanExercise(maturityDate)

        for optionType in optionTypes:
            payoff = PlainVanillaPayoff(optionType, strike)

            rTS = flatRate(today, 0.15, dc)

            f0 = 2.1
            alpha = 0.75

            betas = [-2.0, -0.5, 0.45, 0.6, 0.9, 1.45]
            for beta in betas:
                option = VanillaOption(payoff, exercise)
                option.setPricingEngine(
                    AnalyticCEVEngine(
                        f0, alpha, beta,
                        YieldTermStructureHandle(rTS)))

                analyticNPV = option.NPV()

                eps = 1e-3

                option.setPricingEngine(
                    AnalyticCEVEngine(
                        f0 * (1 + eps), alpha, beta,
                        YieldTermStructureHandle(rTS)))
                analyticUpNPV = option.NPV()

                option.setPricingEngine(
                    AnalyticCEVEngine(
                        f0 * (1 - eps), alpha, beta,
                        YieldTermStructureHandle(rTS)))
                analyticDownNPV = option.NPV()

                analyticDelta = (analyticUpNPV - analyticDownNPV) / (2 * eps * f0)

                option.setPricingEngine(
                    FdCEVVanillaEngine(
                        f0, alpha, beta,
                        YieldTermStructureHandle(rTS),
                        100, 1000, 1, 1.0, 1e-6))

                calculatedNPV = option.NPV()
                calculatedDelta = option.delta()

                tol = 0.01
                self.assertFalse(
                    abs(calculatedNPV - analyticNPV) > tol or
                    abs(calculatedDelta - analyticDelta) > tol)
