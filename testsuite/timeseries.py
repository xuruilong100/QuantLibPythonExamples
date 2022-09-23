import unittest

from QuantLib import *

from utilities import *


class TimeSeriesTest(unittest.TestCase):

    def testConstruction(self):
        TEST_MESSAGE(
            "Testing time series construction...")

        ts = RealTimeSeries()
        ts[Date(25, March, 2005)] = 1.2
        ts[Date(29, March, 2005)] = 2.3
        ts[Date(15, March, 2005)] = 0.3

        cur = (ts.dates()[0], ts.values()[0])
        self.assertFalse(cur[0] != Date(15, March, 2005))
        self.assertFalse(cur[1] != 0.3)

        ts[Date(15, March, 2005)] = 4.0
        cur = (ts.dates()[0], ts.values()[0])
        self.assertFalse(cur[1] != 4.0)

        ts[Date(15, March, 2005)] = 3.5
        cur = (ts.dates()[0], ts.values()[0])
        self.assertFalse(cur[1] != 3.5)

    def testIntervalPrice(self):
        TEST_MESSAGE(
            "Testing time series interval price...")

        date = [Date(25, March, 2005), Date(29, March, 2005)]

        o = [1.3, 2.3]
        c = [2.3, 3.4]
        h = [3.4, 3.5]
        l = [3.4, 3.2]

        tsiq = IntervalPrice.makeSeries(
            date, o, c, h, l)

    def testIterators(self):
        TEST_MESSAGE(
            "Testing time series iterators...")

        dates = [
            Date(25, March, 2005),
            Date(29, March, 2005),
            Date(15, March, 2005)]

        prices = [25, 23, 20]

        ts = RealTimeSeries(dates, prices)

        self.assertFalse(ts.dates()[0] != Date(15, March, 2005))

        self.assertFalse(ts.values()[0] != 20)

        dates = ts.dates()
        self.assertFalse(dates[0] != Date(15, March, 2005))

        prices = ts.values()
        self.assertFalse(prices[0] != 20)

        self.assertFalse(ts.lastDate() != Date(29, March, 2005))
