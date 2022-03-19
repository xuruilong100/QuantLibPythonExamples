import unittest
from utilities import *
from QuantLib import *


class ForwardRateAgreementTest(unittest.TestCase):

    def testConstructionWithoutACurve(self):
        TEST_MESSAGE("Testing forward rate agreement construction...")

        today = QuantLib.Settings.instance().evaluationDate

        # set up the index
        curveHandle = RelinkableYieldTermStructureHandle()
        index = USDLibor(Period(3, Months), curveHandle)

        # determine the settlement date for a FRA
        settlementDate = index.fixingCalendar().advance(
            today, Period(index.fixingDays(), Days))

        # set up quotes with no values
        quotes = [
            SimpleQuote(),
            SimpleQuote(),
            SimpleQuote()]

        # useIndexedFra = false # ifdef QL_USE_INDEXED_COUPON
        useIndexedFra = true  # else

        # set up the curve (this bit is a very rough sketch - i'm actually using swaps !)
        helpers = RateHelperVector()
        helpers.append(
            FraRateHelper(
                QuoteHandle(quotes[0]),
                Period(1, Years), index,
                Pillar.LastRelevantDate, Date(),
                useIndexedFra))
        helpers.append(
            FraRateHelper(
                QuoteHandle(quotes[1]),
                Period(2, Years), index,
                Pillar.LastRelevantDate, Date(),
                useIndexedFra))
        helpers.append(
            FraRateHelper(
                QuoteHandle(quotes[2]),
                Period(3, Years), index,
                Pillar.LastRelevantDate, Date(),
                useIndexedFra))
        curve = PiecewiseCubicForward(
            # PiecewiseYieldCurve<ForwardRate, QuantLib.Cubic>(
            today, helpers, index.dayCounter())

        curveHandle.linkTo(curve)

        # set up the instrument to price
        fra = ForwardRateAgreement(
            settlementDate + Period(12, Months),
            settlementDate + Period(15, Months),
            Position.Long,
            0,
            1,
            index,
            curveHandle,
            useIndexedFra)

        # finally put values in the quotes
        quotes[0].setValue(0.01)
        quotes[1].setValue(0.02)
        quotes[2].setValue(0.03)

        rate = fra.forwardRate()
        self.assertFalse(abs(rate.rate() - 0.01) > 1e-6)
