import unittest
from utilities import *
from QuantLib import *


class FSquared(object):
    def __init__(self):
        pass

    def __call__(self, x):
        return x * x


class SampledCurveTest(unittest.TestCase):

    def testConstruction(self):
        TEST_MESSAGE("Testing sampled curve construction...")

        curve = SampledCurve(BoundedGrid(-10.0, 10.0, 100))
        f2 = FSquared()
        curve.sample(f2)
        expected = 100.0
        self.assertFalse(abs(curve.value(0) - expected) > 1e-5)

        curve.setValue(0, 2.0)
        self.assertFalse(abs(curve.value(0) - 2.0) > 1e-5)

        value = curve.values()
        value[1] = 3.0
        self.assertFalse(abs(curve.value(1) - 3.0) > 1e-5)

        curve.shiftGrid(10.0)
        self.assertFalse(abs(curve.gridValue(0) - 0.0) > 1e-5)
        self.assertFalse(abs(curve.value(0) - 2.0) > 1e-5)

        curve.sample(f2)
        curve.regrid(BoundedGrid(0.0, 20.0, 200))
        tolerance = 1.0e-2
        for i in range(curve.size()):
            grid = curve.gridValue(i)
            value = curve.value(i)
            expected = f2(grid)
            self.assertFalse(abs(value - expected) > tolerance)
