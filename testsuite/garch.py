import unittest
from utilities import *
from QuantLib import *

expected_calc = [
    0.452769, 0.513323, 0.530141, 0.5350841, 0.536558,
    0.536999, 0.537132, 0.537171, 0.537183, 0.537187]


class GARCHTest(unittest.TestCase):
    @unittest.skip('skip testCalibration')
    def testCalibration(self):
        pass

    def testCalculation(self):
        TEST_MESSAGE("Testing GARCH model calculation...")

        d = Date(7, July, 1962)
        ts = RealTimeSeries()
        garch = Garch11(0.2, 0.3, 0.4)

        r = 0.1
        for i in range(10):
            ts[d] = r
            d += 1

        tsout = garch.calculate(ts)

        for i in range(len(tsout)):
            t = (tsout.dates()[i], tsout.values()[i])
            self._check_ts(t)

    def _check_ts(self, x):
        self.assertFalse(
            x[0].serialNumber() < 22835 or x[0].serialNumber() > 22844)
        error = abs(x[1] - expected_calc[x[0].serialNumber() - 22835])
        self.assertFalse(error > 1.0e-6)
