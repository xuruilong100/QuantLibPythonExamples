import unittest

from QuantLib import *

from utilities import *


class VarianceGammaProcessData(object):
    def __init__(self,
                 s,
                 q,
                 r,
                 sigma,
                 nu,
                 theta):
        self.s = s
        self.q = q
        self.r = r
        self.sigma = sigma
        self.nu = nu
        self.theta = theta


class VarianceGammaOptionData(object):
    def __init__(self,
                 type,
                 strike,
                 t):
        self.type = type
        self.strike = strike
        self.t = t


class VarianceGammaTest(unittest.TestCase):

    def testVarianceGamma(self):
        TEST_MESSAGE(
            "Testing variance-gamma model for European options...")

        backup = SavedSettings()

        processes = [
            VarianceGammaProcessData(6000, 0.00, 0.05, 0.20, 0.05, -0.50),
            VarianceGammaProcessData(6000, 0.02, 0.05, 0.15, 0.01, -0.50)]

        options = [
            VarianceGammaOptionData(Option.Call, 5550, 1.0),
            VarianceGammaOptionData(Option.Call, 5600, 1.0),
            VarianceGammaOptionData(Option.Call, 5650, 1.0),
            VarianceGammaOptionData(Option.Call, 5700, 1.0),
            VarianceGammaOptionData(Option.Call, 5750, 1.0),
            VarianceGammaOptionData(Option.Call, 5800, 1.0),
            VarianceGammaOptionData(Option.Call, 5850, 1.0),
            VarianceGammaOptionData(Option.Call, 5900, 1.0),
            VarianceGammaOptionData(Option.Call, 5950, 1.0),
            VarianceGammaOptionData(Option.Call, 6000, 1.0),
            VarianceGammaOptionData(Option.Call, 6050, 1.0),
            VarianceGammaOptionData(Option.Call, 6100, 1.0),
            VarianceGammaOptionData(Option.Call, 6150, 1.0),
            VarianceGammaOptionData(Option.Call, 6200, 1.0),
            VarianceGammaOptionData(Option.Call, 6250, 1.0),
            VarianceGammaOptionData(Option.Call, 6300, 1.0),
            VarianceGammaOptionData(Option.Call, 6350, 1.0),
            VarianceGammaOptionData(Option.Call, 6400, 1.0),
            VarianceGammaOptionData(Option.Call, 6450, 1.0),
            VarianceGammaOptionData(Option.Call, 6500, 1.0),
            VarianceGammaOptionData(Option.Call, 6550, 1.0),
            VarianceGammaOptionData(Option.Put, 5550, 1.0)]

        results = [
            [955.1637, 922.7529, 890.9872, 859.8739, 829.4197, 799.6303, 770.5104, 742.0640,
             714.2943, 687.2032, 660.7921, 635.0613, 610.0103, 585.6379, 561.9416, 538.9186,
             516.5649, 494.8760, 473.8464, 453.4700, 433.7400, 234.4870],
            [732.8705, 698.5542, 665.1404, 632.6498, 601.1002, 570.5068, 540.8824, 512.2367,
             484.5766, 457.9064, 432.2273, 407.5381, 383.8346, 361.1102, 339.3559, 318.5599,
             298.7087, 279.7864, 261.7751, 244.6552, 228.4057, 130.9974]]

        tol = 0.01

        dc = Actual360()
        today = knownGoodDefault

        for i in range(len(processes)):
            spot = SimpleQuote(processes[i].s)
            qRate = SimpleQuote(processes[i].q)
            qTS = flatRate(today, qRate, dc)
            rRate = SimpleQuote(processes[i].r)
            rTS = flatRate(today, rRate, dc)

            stochProcess = VarianceGammaProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                processes[i].sigma,
                processes[i].nu,
                processes[i].theta)

            analyticEngine = VarianceGammaEngine(stochProcess)

            fftEngine = FFTVarianceGammaEngine(stochProcess)

            optionList = []
            payoffs = []
            for j in range(len(options)):
                exDate = today + timeToDays(options[j].t)
                exercise = EuropeanExercise(exDate)

                payoff = PlainVanillaPayoff(
                    options[j].type, options[j].strike)
                payoffs.append(payoff)

                option = EuropeanOption(payoff, exercise)
                option.setPricingEngine(analyticEngine)

                calculated = option.NPV()
                expected = results[i][j]
                error = abs(calculated - expected)

                self.assertFalse(error > tol)

                optionList.append(option)

            fftEngine.precalculate(optionList)
            for j in range(len(options)):
                option = optionList[j]
                option.setPricingEngine(fftEngine)

                calculated = option.NPV()
                expected = results[i][j]
                error = abs(calculated - expected)
                self.assertFalse(error > tol)

    def testSingularityAtZero(self):
        TEST_MESSAGE(
            "Testing variance-gamma model integration around zero...")

        backup = SavedSettings()

        stock = 100
        strike = 98
        sigma = 0.12
        mu = -0.14
        kappa = 0.2

        valuation = Date(1, Jan, 2017)
        maturity = Date(10, Jan, 2017)
        discountCounter = Thirty360(Thirty360.BondBasis)

        Settings.instance().evaluationDate = valuation

        exercise = EuropeanExercise(maturity)
        payoff = PlainVanillaPayoff(Option.Call, strike)
        option = VanillaOption(payoff, exercise)

        dividend = YieldTermStructureHandle(
            FlatForward(valuation, 0.0, discountCounter))
        disc = YieldTermStructureHandle(
            FlatForward(valuation, 0.05, discountCounter))
        S0 = QuoteHandle(SimpleQuote(stock))
        process = VarianceGammaProcess(
            S0, dividend, disc, sigma, kappa, mu)

        option.setPricingEngine(VarianceGammaEngine(process))

        option.NPV()
