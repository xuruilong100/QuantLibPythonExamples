import unittest
from math import sqrt

from QuantLib import *

from utilities import *


class RiskStatisticsTest(unittest.TestCase):

    def testResults(self):
        TEST_MESSAGE(
            "Testing risk measures...")

        igs = IncrementalGaussianStatistics()
        s = RiskStatistics()

        averages = [-100.0, -1.0, 0.0, 1.0, 100.0]
        sigmas = [0.1, 1.0, 100.0]

        N = int(pow(2.0, 16)) - 1

        data = DoubleVector(N)
        weights = DoubleVector(N)

        for i in range(len(averages)):
            for j in range(len(sigmas)):

                normal = NormalDistribution(averages[i], sigmas[j])
                cumulative = CumulativeNormalDistribution(averages[i], sigmas[j])
                inverseCum = InverseCumulativeNormal(averages[i], sigmas[j])

                rng = SobolRsg(1)
                dataMin = QL_MAX_REAL
                dataMax = QL_MIN_REAL
                for k in range(N):
                    data[k] = inverseCum(rng.nextSequence().value()[0])
                    dataMin = min(dataMin, data[k])
                    dataMax = max(dataMax, data[k])
                    weights[k] = 1.0

                igs.addSequence(data, weights)
                s.addSequence(data, weights)

                self.assertFalse(igs.samples() != N)
                self.assertFalse(s.samples() != N)

                tolerance = 1e-10
                expected = 0.0
                for w in weights:
                    expected += w
                calculated = igs.weightSum()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.weightSum()
                self.assertFalse(abs(calculated - expected) > tolerance)

                tolerance = 1e-12
                expected = dataMin
                calculated = igs.min()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.min()
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = dataMax
                calculated = igs.max()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.max()
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = averages[i]

                tolerance = 1.0e-13 if expected == 0.0 else abs(expected) * 1.0e-13
                calculated = igs.mean()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.mean()
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = sigmas[j] * sigmas[j]
                tolerance = expected * 1.0e-1
                calculated = igs.variance()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.variance()
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = sigmas[j]
                tolerance = expected * 1.0e-1
                calculated = igs.standardDeviation()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.standardDeviation()
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = 0.0
                tolerance = 1.0e-4
                calculated = igs.skewness()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.skewness()
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = 0.0
                tolerance = 1.0e-1
                calculated = igs.kurtosis()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.kurtosis()
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = averages[i]

                tolerance = 1.0e-3 if expected == 0.0 else abs(expected * 1.0e-3)
                calculated = igs.gaussianPercentile(0.5)
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.gaussianPercentile(0.5)
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.percentile(0.5)
                self.assertFalse(abs(calculated - expected) > tolerance)

                upper_tail = averages[i] + 2.0 * sigmas[j]
                lower_tail = averages[i] - 2.0 * sigmas[j]
                twoSigma = cumulative(upper_tail)

                expected = max(upper_tail, 0.0)

                tolerance = 1.0e-3 if expected == 0.0 else abs(expected * 1.0e-3)
                calculated = igs.gaussianPotentialUpside(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.gaussianPotentialUpside(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.potentialUpside(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)

                h = StatsHolder(s.mean(), s.standardDeviation())

                test = GaussianStatisticsHolder(h)
                expected = s.gaussianPotentialUpside(twoSigma)
                calculated = test.gaussianPotentialUpside(twoSigma)
                self.assertFalse(not close(calculated, expected))

                expected = -min(lower_tail, 0.0)

                tolerance = 1.0e-3 if expected == 0.0 else abs(expected * 1.0e-3)
                calculated = igs.gaussianValueAtRisk(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.gaussianValueAtRisk(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.valueAtRisk(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)

                if averages[i] > 0.0 and sigmas[j] < averages[i]:
                    igs.reset()
                    s.reset()
                    continue

                expected = -min(averages[i] - sigmas[j] * sigmas[j] * normal(lower_tail) / (1.0 - twoSigma), 0.0)

                tolerance = 1.0e-4 if expected == 0.0 else abs(expected * 1.0e-2)
                calculated = igs.gaussianExpectedShortfall(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.gaussianExpectedShortfall(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.expectedShortfall(twoSigma)
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = 0.5

                tolerance = 1.0e-3 if expected == 0.0 else abs(expected * 1.0e-3)
                calculated = igs.gaussianShortfall(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.gaussianShortfall(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.shortfall(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = sigmas[j] / sqrt(2.0 * M_PI) * 2.0
                tolerance = expected * 1.0e-3
                calculated = igs.gaussianAverageShortfall(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.gaussianAverageShortfall(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.averageShortfall(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = sigmas[j] * sigmas[j]
                tolerance = expected * 1.0e-1
                calculated = igs.gaussianRegret(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.gaussianRegret(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.regret(averages[i])
                self.assertFalse(abs(calculated - expected) > tolerance)

                expected = s.downsideVariance()

                tolerance = 1.0e-3 if expected == 0.0 else abs(expected * 1.0e-3)
                calculated = igs.downsideVariance()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = igs.gaussianDownsideVariance()
                self.assertFalse(abs(calculated - expected) > tolerance)

                if averages[i] == 0.0:
                    expected = sigmas[j] * sigmas[j]
                tolerance = expected * 1.0e-3
                calculated = igs.downsideVariance()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = igs.gaussianDownsideVariance()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.downsideVariance()
                self.assertFalse(abs(calculated - expected) > tolerance)
                calculated = s.gaussianDownsideVariance()
                self.assertFalse(abs(calculated - expected) > tolerance)

                igs.reset()
                s.reset()
