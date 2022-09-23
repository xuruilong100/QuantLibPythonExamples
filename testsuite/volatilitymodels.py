import unittest

from QuantLib import *

from utilities import *


class VolatilityModelsTest(unittest.TestCase):

    def testConstruction(self):
        TEST_MESSAGE(
            "Testing volatility model construction...")

        ts = RealTimeSeries()
        ts[Date(25, March, 2005)] = 1.2
        ts[Date(29, March, 2005)] = 2.3
        ts[Date(15, March, 2005)] = 0.3

        sle = SimpleLocalEstimator(1 / 360.0)
        locale = sle.calculate(ts)

        ce = ConstantEstimator(1)
        sv = ce.calculate(locale)
        s = sv[Date(25, March, 2005)]
