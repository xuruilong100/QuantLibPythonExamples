import unittest
from utilities import *
from QuantLib import *


class RngTraitsTest(unittest.TestCase):
    def testGaussian(self):
        TEST_MESSAGE("Testing Gaussian pseudo-random number generation...")

        # rsg = PseudoRandom.make_sequence_generator(100, 1234)
        rsg = InvCumulativeMersenneTwisterGaussianRsg(
            MersenneTwisterUniformRsg(100, 1234))

        values = rsg.nextSequence().value()
        sum = 0.0
        for value in values:
            sum += value

        stored = 4.09916
        tolerance = 1.0e-5
        self.assertFalse(abs(sum - stored) > tolerance)

    def testDefaultPoisson(self):
        TEST_MESSAGE("Testing Poisson pseudo-random number generation...")

        # PoissonPseudoRandom.icInstance =InverseCumulativePoisson()
        # rsg = PoissonPseudoRandom.make_sequence_generator(100, 1234)
        icInstance = InverseCumulativePoisson()
        rsg = InvCumulativeMersenneTwisterPoissonRsg(
            MersenneTwisterUniformRsg(100, 1234),
            icInstance)

        values = rsg.nextSequence().value()
        sum = 0.0
        for value in values:
            sum += value

        stored = 108.0
        self.assertFalse(not close(sum, stored))

    def testCustomPoisson(self):
        TEST_MESSAGE("Testing custom Poisson pseudo-random number generation...")

        # PoissonPseudoRandom.icInstance =InverseCumulativePoisson(4.0)
        # rsg =PoissonPseudoRandom.make_sequence_generator(100, 1234)
        icInstance = InverseCumulativePoisson(4.0)
        rsg = InvCumulativeMersenneTwisterPoissonRsg(
            MersenneTwisterUniformRsg(100, 1234),
            icInstance)

        values = rsg.nextSequence().value()
        sum = 0.0
        for value in values:
            sum += value

        stored = 409.0
        self.assertFalse(not close(sum, stored))
