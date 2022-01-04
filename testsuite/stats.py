import unittest
from utilities import *
from QuantLib import *

data = [3.0, 4.0, 5.0, 2.0, 3.0, 4.0, 5.0, 6.0, 4.0, 7.0]
weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

Statistics = RiskStatistics


class StatisticsTest(unittest.TestCase):

    def testStatistics(self):
        TEST_MESSAGE("Testing statistics...")
        self.check(IncrementalStatistics, "IncrementalStatistics")
        self.check(Statistics, "Statistics")

    def testSequenceStatistics(self):
        TEST_MESSAGE("Testing sequence statistics...")

        self.checkSequence(SequenceStatisticsInc, "IncrementalStatistics", 5)
        self.checkSequence(SequenceStatistics, "Statistics", 5)

    def testConvergenceStatistics(self):
        TEST_MESSAGE("Testing convergence statistics...")

        self.checkConvergence(ConvergeStatisticsInc, "IncrementalStatistics")
        self.checkConvergence(ConvergeStatistics, "Statistics")

    def testIncrementalStatistics(self):
        TEST_MESSAGE("Testing incremental statistics...")

        # With QuantLib 1.7 IncrementalStatistics was changed to
        # a wrapper to the boost accumulator library. This is
        # a test of the new implementation against results from
        # the old one.

        mt = MersenneTwisterUniformRng(42)

        stat = IncrementalStatistics()

        for i in range(500000):
            x = 2.0 * (mt.nextReal() - 0.5) * 1234.0
            w = mt.nextReal()
            stat.add(x, w)

        self.assertFalse(stat.samples() != 500000)

        self.assertFalse(not close_enough(stat.weightSum(), 2.5003623600676749e+05))
        self.assertFalse(not close_enough(stat.mean(), 4.9122325964293845e-01))
        self.assertFalse(not close_enough(stat.variance(), 5.0706503959683329e+05))
        self.assertFalse(not close_enough(stat.standardDeviation(), 7.1208499464378076e+02))
        self.assertFalse(not close_enough(stat.errorEstimate(), 1.0070402569876076e+00))
        self.assertFalse(not close_enough(stat.skewness(), -1.7360169326720038e-03))
        self.assertFalse(not close_enough(stat.kurtosis(), -1.1990742562085395e+00))
        self.assertFalse(not close_enough(stat.min(), -1.2339945045639761e+03))
        self.assertFalse(not close_enough(stat.max(), 1.2339958308008499e+03))
        self.assertFalse(not close_enough(stat.downsideVariance(), 5.0786776146975247e+05))
        self.assertFalse(not close_enough(stat.downsideDeviation(), 7.1264841364431061e+02))

        # This is a test for numerical stability,
        # where the old implementation fails

        # normal_gen = InverseCumulativeRng < MersenneTwisterUniformRng, InverseCumulativeNormal > (mt)
        normal_gen = InvCumulativeMersenneTwisterGaussianRng(mt)

        stat2 = IncrementalStatistics()

        for i in range(500000):
            x = normal_gen.next().value() * 1E-1 + 1E8
            w = 1.0
            stat2.add(x, w)

        tol = 1E-5

        self.assertFalse(abs(stat2.variance() - 1E-2) > tol)

    def check(self,
              S,
              name):
        s = S()
        for i in range(len(data)):
            s.add(data[i], weights[i])

        self.assertFalse(s.samples() != len(data))

        # expected = accumulate(weights, weights + len(weights), Real(0.0))
        expected = 0.0
        for w in weights:
            expected += w
        calculated = s.weightSum()
        self.assertFalse(calculated != expected)

        # expected = *min_element(data, data + len(data))
        expected = min(data)
        calculated = s.min()
        self.assertFalse(calculated != expected)

        # expected = *max_element(data, data + len(data))
        expected = max(data)
        calculated = s.max()
        self.assertFalse(calculated != expected)

        expected = 4.3
        tolerance = 1.0e-9
        calculated = s.mean()
        self.assertFalse(abs(calculated - expected) > tolerance)

        expected = 2.23333333333
        calculated = s.variance()
        self.assertFalse(abs(calculated - expected) > tolerance)

        expected = 1.4944341181
        calculated = s.standardDeviation()
        self.assertFalse(abs(calculated - expected) > tolerance)

        expected = 0.359543071407
        calculated = s.skewness()
        self.assertFalse(abs(calculated - expected) > tolerance)

        expected = -0.151799637209
        calculated = s.kurtosis()
        self.assertFalse(abs(calculated - expected) > tolerance)

    def checkSequence(self,
                      S,
                      name,
                      dimension):
        # ss = GenericSequenceStatistics < S > (dimension)
        ss = S(dimension)

        for i in range(len(data)):
            temp = DoubleVector(dimension, data[i])
            ss.add(temp, weights[i])

        self.assertFalse(ss.samples() != len(data))

        # expected = accumulate(weights, weights + len(weights), Real(0.0))
        expected = 0.0
        for w in weights:
            expected += w
        self.assertFalse(ss.weightSum() != expected)

        # expected = *min_element(data, data + len(data))
        expected = min(data)
        calculated = ss.min()
        for i in range(dimension):
            self.assertFalse(calculated[i] != expected)

        # expected = *max_element(data, data + len(data))
        expected = max(data)
        calculated = ss.max()
        for i in range(dimension):
            self.assertFalse(calculated[i] != expected)

        expected = 4.3
        tolerance = 1.0e-9
        calculated = ss.mean()
        for i in range(dimension):
            self.assertFalse(abs(calculated[i] - expected) > tolerance)

        expected = 2.23333333333
        calculated = ss.variance()
        for i in range(dimension):
            self.assertFalse(abs(calculated[i] - expected) > tolerance)

        expected = 1.4944341181
        calculated = ss.standardDeviation()
        for i in range(dimension):
            self.assertFalse(abs(calculated[i] - expected) > tolerance)

        expected = 0.359543071407
        calculated = ss.skewness()
        for i in range(dimension):
            self.assertFalse(abs(calculated[i] - expected) > tolerance)

        expected = -0.151799637209
        calculated = ss.kurtosis()
        for i in range(dimension):
            self.assertFalse(abs(calculated[i] - expected) > tolerance)

    def checkConvergence(self, S, name):
        # stats = ConvergenceStatistics < S > ()
        stats = S()

        stats.add(1.0)
        stats.add(2.0)
        stats.add(3.0)
        stats.add(4.0)
        stats.add(5.0)
        stats.add(6.0)
        stats.add(7.0)
        stats.add(8.0)

        expectedSize1 = 3
        calculatedSize = len(stats.convergenceTable())
        self.assertFalse(calculatedSize != expectedSize1)

        expectedValue1 = 4.0
        tolerance = 1.0e-9
        calculatedValue = stats.convergenceTable()[-1][1]
        self.assertFalse(abs(calculatedValue - expectedValue1) > tolerance)

        expectedSampleSize1 = 7
        calculatedSamples = stats.convergenceTable()[-1][0]
        self.assertFalse(calculatedSamples != expectedSampleSize1)

        stats.reset()
        stats.add(1.0)
        stats.add(2.0)
        stats.add(3.0)
        stats.add(4.0)

        expectedSize2 = 2
        calculatedSize = len(stats.convergenceTable())
        self.assertFalse(calculatedSize != expectedSize2)

        expectedValue2 = 2.0
        calculatedValue = stats.convergenceTable()[-1][1]
        self.assertFalse(abs(calculatedValue - expectedValue2) > tolerance)

        expectedSampleSize2 = 3
        calculatedSamples = stats.convergenceTable()[-1][0]
        self.assertFalse(calculatedSamples != expectedSampleSize2)
