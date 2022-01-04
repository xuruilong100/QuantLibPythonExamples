import unittest
from utilities import *
from QuantLib import *


class TimeSeriesTest(unittest.TestCase):

    def testConstruction(self):
        TEST_MESSAGE("Testing time series construction...")

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
        TEST_MESSAGE("Testing time series interval price...")

        date = [Date(25, March, 2005), Date(29, March, 2005)]

        o = [1.3, 2.3]
        c = [2.3, 3.4]
        h = [3.4, 3.5]
        l = [3.4, 3.2]

        tsiq = IntervalPrice.makeSeries(
            date, o, c, h, l)

    def testIterators(self):
        TEST_MESSAGE("Testing time series iterators...")

        dates = [
            Date(25, March, 2005),
            Date(29, March, 2005),
            Date(15, March, 2005)]

        prices = [25, 23, 20]

        ts = RealTimeSeries(dates, prices)

        # projection iterators

        # std.copy(ts.cbegin_time(), ts.cend_time(), dates.begin())
        self.assertFalse(ts.dates()[0] != Date(15, March, 2005))

        # std.copy(ts.cbegin_values(), ts.cend_values(), prices.begin())
        self.assertFalse(ts.values()[0] != 20)

        dates = ts.dates()
        self.assertFalse(dates[0] != Date(15, March, 2005))

        prices = ts.values()
        self.assertFalse(prices[0] != 20)

        # unordered container
        # typedef TimeSeries<int, boost.unordered_map<Date, int> >
        #     TimeSeriesUnordered
        # TimeSeriesUnordered ts1
        # d0(25, March, 2005), d1(25, April, 2005), d = d0
        # UnitedStates calendar(UnitedStates.NYSE)
        # for (i = 0 d < d1 ++i, d = calendar.advance(d, 1, Days)) {
        #     ts1[d] = i
        # }

        # d = d0
        # for (i = 0 d < d1 ++i, d = calendar.advance(d, 1, Days)) {
        #     if (ts1[d] != int(i)) {
        #         BOOST_ERROR("value does not match")
        #     }
        # }

        # reverse iterators

        # std.vector<std.pair<Date, Real> > data(prices.size())
        # std.copy(ts.crbegin(), ts.crend(), data.begin())
        # self.assertFalse(ts.values()[2] != 20)
        # self.assertFalse(ts.dates()[2] != Date(15, March, 2005))

        # std.copy(ts.crbegin_time(), ts.crend_time(), dates.begin())
        # self.assertFalse(ts.dates()[0] != Date(29, March, 2005))

        # std.copy(ts.crbegin_values(), ts.crend_values(), prices.begin())
        # self.assertFalse(ts.values()[0] != 23)

        # The following should not compile:
        # std.transform(ts1.crbegin(), ts1.crend(), prices.begin(),
        #                TimeSeriesUnordered.get_value)
        # std.copy(ts1.crbegin_values(), ts1.crend_values(), prices.begin())
        # ts1.lastDate()

        # last date 
        self.assertFalse(ts.lastDate() != Date(29, March, 2005))
