import unittest

from QuantLib import *

from utilities import *


class AutocovariancesTest(unittest.TestCase):

    def testConvolutions(self):
        TEST_MESSAGE(
            "Testing convolutions...")
        x = Array(10, 1, 1)
        conv = convolutions(x, 5)
        expected = [385, 330, 276, 224, 175, 130]
        expectedArray = Array(6)
        for i in range(6):
            expectedArray[i] = expected[i]
        delta = conv - expectedArray
        self.assertFalse(DotProduct(delta, delta) > 1.0e-6)

    def testAutoCovariances(self):
        TEST_MESSAGE(
            "Testing auto-covariances...")
        x = Array(10, 1, 1)
        tmp = autocovariances(x, 5, false)
        mean = tmp.first
        acovf = tmp.second
        expected = [8.25, 6.416667, 4.25, 1.75, -1.08333, -4.25]
        expectedArray = Array(6)
        for i in range(6):
            expectedArray[i] = expected[i]
        self.assertFalse(abs(mean - 5.5) > 1.0e-6)
        delta = acovf - expectedArray
        self.assertFalse(DotProduct(delta, delta) > 1.0e-6)

    def testAutoCorrelations(self):
        TEST_MESSAGE(
            "Testing auto-correlations...")
        x = Array(10, 1, 1)
        tmp = autocorrelations(x, 5, true)
        mean = tmp.first
        acorf = tmp.second
        expected = [
            9.166667, 0.77777778, 0.51515152,
            0.21212121, -0.13131313, -0.51515152]
        expectedArray = Array(6)
        for i in range(6):
            expectedArray[i] = expected[i]
        self.assertFalse(abs(mean - 5.5) > 1.0e-6)
        delta = acorf - expectedArray
        self.assertFalse(DotProduct(delta, delta) > 1.0e-6)
        delta = x - Array(10, -4.5, 1)
        self.assertFalse(DotProduct(delta, delta) > 1.0e-6)
