import unittest

from QuantLib import *

from utilities import *


class SofrQuotes(object):
    def __init__(self,
                 freq,
                 month,
                 year,
                 price,
                 averagingMethod):
        self.freq = freq
        self.month = month
        self.year = year
        self.price = price

        self.averagingMethod = averagingMethod


class SofrFuturesTest(unittest.TestCase):

    def testBootstrap(self):
        TEST_MESSAGE(
            "Testing bootstrap over SOFR futures...")

        backup = SavedSettings()

        today = Date(26, October, 2018)
        Settings.instance().evaluationDate = today

        sofrQuotes = [
            SofrQuotes(Monthly, Oct, 2018, 97.8175, RateAveraging.Simple),
            SofrQuotes(Monthly, Nov, 2018, 97.770, RateAveraging.Simple),
            SofrQuotes(Monthly, Dec, 2018, 97.685, RateAveraging.Simple),
            SofrQuotes(Monthly, Jan, 2019, 97.595, RateAveraging.Simple),
            SofrQuotes(Monthly, Feb, 2019, 97.590, RateAveraging.Simple),
            SofrQuotes(Monthly, Mar, 2019, 97.525, RateAveraging.Simple),
            SofrQuotes(Quarterly, Mar, 2019, 97.440, RateAveraging.Compound),
            SofrQuotes(Quarterly, Jun, 2019, 97.295, RateAveraging.Compound),
            SofrQuotes(Quarterly, Sep, 2019, 97.220, RateAveraging.Compound),
            SofrQuotes(Quarterly, Dec, 2019, 97.170, RateAveraging.Compound),
            SofrQuotes(Quarterly, Mar, 2020, 97.160, RateAveraging.Compound),
            SofrQuotes(Quarterly, Jun, 2020, 97.165, RateAveraging.Compound),
            SofrQuotes(Quarterly, Sep, 2020, 97.175, RateAveraging.Compound), ]

        index = Sofr()
        index.addFixing(Date(1, October, 2018), 0.0222)
        index.addFixing(Date(2, October, 2018), 0.022)
        index.addFixing(Date(3, October, 2018), 0.022)
        index.addFixing(Date(4, October, 2018), 0.0218)
        index.addFixing(Date(5, October, 2018), 0.0216)
        index.addFixing(Date(9, October, 2018), 0.0215)
        index.addFixing(Date(10, October, 2018), 0.0215)
        index.addFixing(Date(11, October, 2018), 0.0217)
        index.addFixing(Date(12, October, 2018), 0.0218)
        index.addFixing(Date(15, October, 2018), 0.0221)
        index.addFixing(Date(16, October, 2018), 0.0218)
        index.addFixing(Date(17, October, 2018), 0.0218)
        index.addFixing(Date(18, October, 2018), 0.0219)
        index.addFixing(Date(19, October, 2018), 0.0219)
        index.addFixing(Date(22, October, 2018), 0.0218)
        index.addFixing(Date(23, October, 2018), 0.0217)
        index.addFixing(Date(24, October, 2018), 0.0218)
        index.addFixing(Date(25, October, 2018), 0.0219)

        helpers = []
        for sofrQuote in sofrQuotes:
            helpers.append(SofrFutureRateHelper(
                sofrQuote.price, sofrQuote.month, sofrQuote.year, sofrQuote.freq))

        curve = PiecewiseLinearDiscount(
            today, helpers, Actual365Fixed(), Linear())

        sofr = Sofr(YieldTermStructureHandle(curve))
        sf = OvernightIndexFuture(sofr, Date(20, March, 2019), Date(19, June, 2019))

        expected_price = 97.44
        tolerance = 1.0e-9

        error = abs(sf.NPV() - expected_price)
        self.assertFalse(error > tolerance)
