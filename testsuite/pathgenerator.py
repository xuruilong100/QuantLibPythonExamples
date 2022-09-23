import unittest

from QuantLib import *

from utilities import *


class PathGeneratorTest(unittest.TestCase):

    def testPathGenerator(self):
        TEST_MESSAGE(
            "Testing 1-D path generation against cached values...")

        backup = SavedSettings()

        Settings.instance().evaluationDate = Date(26, April, 2005)

        x0 = QuoteHandle(SimpleQuote(100.0))
        r = YieldTermStructureHandle(flatRate(0.05, Actual360()))
        q = YieldTermStructureHandle(flatRate(0.02, Actual360()))
        sigma = BlackVolTermStructureHandle(flatVol(0.20, Actual360()))

        self._testSingle(
            BlackScholesMertonProcess(x0, q, r, sigma),
            "Black-Scholes", false, 26.13784357783, 467.2928561411)

        self._testSingle(
            BlackScholesMertonProcess(x0, q, r, sigma),
            "Black-Scholes", true, 60.28215549393, 202.6143139999)

        self._testSingle(
            GeometricBrownianMotionProcess(100.0, 0.03, 0.20),
            "geometric Brownian", false, 27.62223714065, 483.6026514084)

        self._testSingle(
            OrnsteinUhlenbeckProcess(0.1, 0.20),
            "Ornstein-Uhlenbeck", false, -0.8372003433557, 0.8372003433557)

        self._testSingle(
            SquareRootProcess(0.1, 0.1, 0.20, 10.0),
            "square-root", false, 1.70608664108, 6.024200546031)

    def testMultiPathGenerator(self):
        TEST_MESSAGE(
            "Testing n-D path generation against cached values...")

        backup = SavedSettings()

        Settings.instance().evaluationDate = Date(26, April, 2005)

        x0 = QuoteHandle(SimpleQuote(100.0))
        r = YieldTermStructureHandle(flatRate(0.05, Actual360()))
        q = YieldTermStructureHandle(flatRate(0.02, Actual360()))
        sigma = BlackVolTermStructureHandle(flatVol(0.20, Actual360()))

        correlation = Matrix(3, 3)
        correlation[0][0] = 1.0
        correlation[0][1] = 0.9
        correlation[0][2] = 0.7
        correlation[1][0] = 0.9
        correlation[1][1] = 1.0
        correlation[1][2] = 0.4
        correlation[2][0] = 0.7
        correlation[2][1] = 0.4
        correlation[2][2] = 1.0

        processes = StochasticProcess1DVector(3)

        processes[0] = BlackScholesMertonProcess(x0, q, r, sigma)
        processes[1] = BlackScholesMertonProcess(x0, q, r, sigma)
        processes[2] = BlackScholesMertonProcess(x0, q, r, sigma)
        process = StochasticProcessArray(processes, correlation)

        result1 = [
            188.2235868185,
            270.6713069569,
            113.0431145652]
        result1a = [
            64.89105742957,
            45.12494404804,
            108.0475146914]
        self._testMultiple(process, "Black-Scholes", result1, result1a)

        processes[0] = GeometricBrownianMotionProcess(100.0, 0.03, 0.20)
        processes[1] = GeometricBrownianMotionProcess(100.0, 0.03, 0.20)
        processes[2] = GeometricBrownianMotionProcess(100.0, 0.03, 0.20)
        process = StochasticProcessArray(processes, correlation)
        result2 = [
            174.8266131680,
            237.2692443633,
            119.1168555440]
        result2a = [
            57.69082393020,
            38.50016862915,
            116.4056510107]
        self._testMultiple(process, "geometric Brownian", result2, result2a)

        processes[0] = OrnsteinUhlenbeckProcess(0.1, 0.20)
        processes[1] = OrnsteinUhlenbeckProcess(0.1, 0.20)
        processes[2] = OrnsteinUhlenbeckProcess(0.1, 0.20)
        process = StochasticProcessArray(processes, correlation)
        result3 = [
            0.2942058437284,
            0.5525006418386,
            0.02650931054575]
        result3a = [
            -0.2942058437284,
            -0.5525006418386,
            -0.02650931054575]
        self._testMultiple(process, "Ornstein-Uhlenbeck", result3, result3a)

        processes[0] = SquareRootProcess(0.1, 0.1, 0.20, 10.0)
        processes[1] = SquareRootProcess(0.1, 0.1, 0.20, 10.0)
        processes[2] = SquareRootProcess(0.1, 0.1, 0.20, 10.0)
        process = StochasticProcessArray(processes, correlation)
        result4 = [
            4.279510844897,
            4.943783503533,
            3.590930385958]
        result4a = [
            2.763967737724,
            2.226487196647,
            3.503859264341]
        self._testMultiple(process, "square-root", result4, result4a)

    def _testSingle(self,
                    process,
                    tag,
                    brownianBridge,
                    expected,
                    antithetic):
        seed = 42
        length = 10
        timeSteps = 12
        rsg = GaussianRandomSequenceGenerator(
            UniformRandomSequenceGenerator(
                timeSteps, UniformRandomGenerator(seed)))
        generator = GaussianPathGenerator(
            process, length, timeSteps,
            rsg, brownianBridge)

        for i in range(100):
            generator.next()

        sample = generator.next()
        calculated = sample.value().back()
        error = abs(calculated - expected)
        tolerance = 2.0e-8
        self.assertFalse(error > tolerance)

        sample = generator.antithetic()
        calculated = sample.value().back()
        error = abs(calculated - antithetic)
        tolerance = 2.0e-7
        self.assertFalse(error > tolerance)

    def _testMultiple(self,
                      process,
                      tag,
                      expected,
                      antithetic):
        seed = 42
        length = 10
        timeSteps = 12
        assets = process.size()
        rsg = GaussianRandomSequenceGenerator(
            UniformRandomSequenceGenerator(
                timeSteps * assets, UniformRandomGenerator(seed)))

        generator = GaussianMultiPathGenerator(
            process,
            TimeGrid(length, timeSteps),
            rsg, false)

        for i in range(100):
            generator.next()

        sample = generator.next()

        calculated = Array(assets)

        tolerance = 2.0e-7
        for j in range(assets):
            calculated[j] = sample.value()[j].back()
        for j in range(assets):
            error = abs(calculated[j] - expected[j])
            self.assertFalse(error > tolerance)

        sample = generator.antithetic()
        for j in range(assets):
            calculated[j] = sample.value()[j].back()
        for j in range(assets):
            error = abs(calculated[j] - antithetic[j])
            self.assertFalse(error > tolerance)
