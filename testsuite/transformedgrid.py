import unittest

from QuantLib import *

from utilities import *


class PlusOne(object):
    def __init__(self):
        pass

    def __call__(self, x):
        return x + 1


class TransformedGridTest(unittest.TestCase):

    def testConstruction(self):
        TEST_MESSAGE(
            "Testing transformed grid construction...")

        p1 = PlusOne()
        grid = BoundedGrid(0, 100, 100)
        tg = TransformedGrid(grid, p1)
        self.assertFalse(abs(tg.grid(0) - 0.0) > 1e-5)
        self.assertFalse(abs(tg.transformedGrid(0) - 1.0) > 1e-5)
