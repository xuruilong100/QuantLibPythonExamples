import unittest
from utilities import *
from QuantLib import *
from math import sqrt


def maxDiff(x, y):
    diff = 0.0
    for i, j in zip(x, y):
        diff = max(diff, abs(i - j))
    return diff


def maxDiffMat(x, y):
    diff = 0.0
    for i in range(x.rows()):
        for j in range(x.columns()):
            diff = max(diff, abs(x[i][j] - y[i][j]))
    return diff


def maxRelDiff(x, y):
    diff = 0.0
    for i, j in zip(x, y):
        diff = max(diff, abs((i - j) / j))
    return diff


def maxRelDiffMat(x, y):
    diff = 0.0
    for i in range(x.rows()):
        for j in range(x.columns()):
            diff = max(diff, abs((x[i][j] - y[i][j]) / y[i][j]))
    return diff


class BrownianBridgeTest(unittest.TestCase):

    def testVariates(self):
        TEST_MESSAGE("Testing Brownian-bridge variates...")

        times = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 5.0]

        N = len(times)

        samples = 262143
        seed = 42
        sobol = SobolRsg(N, seed)
        generator = InvCumulativeSobolGaussianRsg(sobol)

        bridge = BrownianBridge(times)

        stats1 = SequenceStatistics(N)
        stats2 = SequenceStatistics(N)

        for i in range(samples):
            sample = generator.nextSequence().value()

            temp = bridge.transform(sample)
            temp = [t for t in temp]
            stats1.add(temp)

            temp[0] = temp[0] * sqrt(times[0])
            for j in range(1, N):
                temp[j] = temp[j - 1] + temp[j] * sqrt(times[j] - times[j - 1])
            stats2.add(temp)

        # normalized single variates
        expectedMean = DoubleVector(N, 0.0)
        expectedCovariance = Matrix(N, N, 0.0)
        for i in range(N):
            expectedCovariance[i][i] = 1.0

        # ifndef __FAST_MATH__
        meanTolerance = 1.0e-16
        # else
        meanTolerance = 1.0e-14
        # endif
        covTolerance = 2.5e-4

        mean = stats1.mean()
        covariance = stats1.covariance()

        maxMeanError = maxDiff(mean, expectedMean)
        maxCovError = maxDiffMat(covariance, expectedCovariance)

        self.assertFalse(maxMeanError > meanTolerance)
        self.assertFalse(maxCovError > covTolerance)

        # denormalized sums along the path
        expectedMean = DoubleVector(N, 0.0)
        expectedCovariance = Matrix(N, N)
        for i in range(N):
            for j in range(i, N):
                expectedCovariance[i][j] = expectedCovariance[j][i] = times[i]

        covTolerance = 6.0e-4

        mean = stats2.mean()
        covariance = stats2.covariance()

        maxMeanError = maxDiff(mean, expectedMean)
        maxCovError = maxDiffMat(covariance, expectedCovariance)

        self.assertFalse(maxMeanError > meanTolerance)
        self.assertFalse(maxCovError > covTolerance)

    def testPathGeneration(self):
        TEST_MESSAGE("Testing Brownian-bridge path generation...")

        times = [
            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
            0.9, 1.0, 2.0, 5.0, 7.0, 9.0, 10.0]

        grid = TimeGrid(times)

        N = len(times)

        samples = 131071
        seed = 42
        # sobol = SobolRsg(N, seed)
        sobol = UniformLowDiscrepancySequenceGenerator(N, seed)
        # gsg = InvCumulativeSobolGaussianRsg(sobol)
        gsg = GaussianLowDiscrepancySequenceGenerator(sobol)

        today = Settings.instance().evaluationDate
        x0 = QuoteHandle(SimpleQuote(100.0))
        r = YieldTermStructureHandle(
            FlatForward(today, 0.06, Actual365Fixed()))
        q = YieldTermStructureHandle(
            FlatForward(today, 0.03, Actual365Fixed()))
        sigma = BlackVolTermStructureHandle(
            BlackConstantVol(today, NullCalendar(), 0.20, Actual365Fixed()))

        process = BlackScholesMertonProcess(x0, q, r, sigma)

        generator1 = GaussianSobolPathGenerator(process, grid, gsg, false)
        generator2 = GaussianSobolPathGenerator(process, grid, gsg, true)

        stats1 = SequenceStatistics(N)
        stats2 = SequenceStatistics(N)

        temp = DoubleVector(N)

        for i in range(samples):
            path1 = generator1.next().value()
            # copy(path1.begin() + 1, path1.end(), temp.begin())
            for i in range(1, len(path1)):
                temp[i - 1] = path1[i]
            stats1.add(temp)

            path2 = generator2.next().value()
            # copy(path2.begin() + 1, path2.end(), temp.begin())
            for i in range(1, len(path2)):
                temp[i - 1] = path2[i]
            stats2.add(temp)

        expectedMean = stats1.mean()
        expectedCovariance = stats1.covariance()

        mean = stats2.mean()
        covariance = stats2.covariance()

        meanTolerance = 3.0e-5
        covTolerance = 3.0e-3

        maxMeanError = maxRelDiff(mean, expectedMean)
        maxCovError = maxRelDiffMat(covariance, expectedCovariance)

        self.assertFalse(maxMeanError > meanTolerance)
        self.assertFalse(maxCovError > covTolerance)
