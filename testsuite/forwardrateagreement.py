import unittest

from QuantLib import *

from utilities import *


class ForwardRateAgreementTest(unittest.TestCase):

    def testConstructionWithoutACurve(self):
        TEST_MESSAGE(
            "Testing forward rate agreement construction...")

        today = QuantLib.Settings.instance().evaluationDate

        curveHandle = RelinkableYieldTermStructureHandle()
        index = USDLibor(Period(3, Months), curveHandle)

        settlementDate = index.fixingCalendar().advance(
            today, Period(index.fixingDays(), Days))

        quotes = [
            SimpleQuote(),
            SimpleQuote(),
            SimpleQuote()]

        useIndexedFra = true

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

            today, helpers, index.dayCounter(), Cubic())

        curveHandle.linkTo(curve)

        fra = ForwardRateAgreement(
            settlementDate + Period(12, Months),
            settlementDate + Period(15, Months),
            Position.Long,
            0,
            1,
            index,
            curveHandle,
            useIndexedFra)

        quotes[0].setValue(0.01)
        quotes[1].setValue(0.02)
        quotes[2].setValue(0.03)

        rate = fra.forwardRate()
        self.assertFalse(abs(rate.rate() - 0.01) > 1e-6)
