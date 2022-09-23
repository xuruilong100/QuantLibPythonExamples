import unittest

from QuantLib import *

from utilities import *


class RngTraitsTest(unittest.TestCase):

    def testGaussian(self):
        TEST_MESSAGE(
            "Testing Gaussian pseudo-random number generation...")

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
        TEST_MESSAGE(
            "Testing Poisson pseudo-random number generation...")

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
        TEST_MESSAGE(
            "Testing custom Poisson pseudo-random number generation...")

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

    def testRanLux(self):
        TEST_MESSAGE(
            "Testing known RanLux sequence...")

        ranlux3 = Ranlux3UniformRng(2938723)
        ranlux4 = Ranlux4UniformRng(4390109)

        ranlux3_expected = [
            0.307448851544538826, 0.666313657894363587, 0.698528013702823358, 0.0217381272445322793,
            0.862964516238161394, 0.909193419106014034, 0.674484308686746914, 0.849607570377191479,
            0.054626078713596371, 0.416474163715683687]

        ranlux4_expected = [
            0.222209169374078641, 0.420181950405986271, 0.0302156663005135329, 0.0836259809475237148,
            0.480549766594993599, 0.723472021829124401, 0.905819507194266293, 0.54072519936540786,
            0.445908421479817463, 0.651084788437518824]

        for i in range(10010):
            ranlux3.next()
            ranlux4.next()

        for i in range(10):
            self.assertFalse(not close_enough(ranlux3.next().value(), ranlux3_expected[i]))
            self.assertFalse(not close_enough(ranlux4.next().value(), ranlux4_expected[i]))
