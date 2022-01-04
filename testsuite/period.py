import unittest
from utilities import *
from QuantLib import *


class PeriodTest(unittest.TestCase):

    def testYearsMonthsAlgebra(self):
        TEST_MESSAGE("Testing period algebra on years/months...")

        OneYear = Period(1, Years)
        SixMonths = Period(6, Months)
        ThreeMonths = Period(3, Months)

        n = 4
        self.assertFalse(OneYear / n != ThreeMonths)
        n = 2
        self.assertFalse(OneYear / n != SixMonths)

        sum = ThreeMonths
        sum += SixMonths
        self.assertFalse(sum != Period(9, Months))

        sum += OneYear
        self.assertFalse(sum != Period(21, Months))

        TwelveMonths = Period(12, Months)
        self.assertFalse(TwelveMonths.length() != 12)
        self.assertFalse(TwelveMonths.units() != Months)

        NormalizedTwelveMonths = Period(12, Months)
        NormalizedTwelveMonths.normalize()
        self.assertFalse(NormalizedTwelveMonths.length() != 1)
        self.assertFalse(NormalizedTwelveMonths.units() != Years)

    def testWeeksDaysAlgebra(self):
        TEST_MESSAGE("Testing period algebra on weeks/days...")

        TwoWeeks = Period(2, Weeks)
        OneWeek = Period(1, Weeks)
        ThreeDays = Period(3, Days)
        OneDay = Period(1, Days)

        n = 2
        self.assertFalse(TwoWeeks / n != OneWeek)
        n = 7
        self.assertFalse(OneWeek / n != OneDay)

        sum = ThreeDays
        sum += OneDay
        self.assertFalse(sum != Period(4, Days))

        sum += OneWeek
        self.assertFalse(sum != Period(11, Days))

        SevenDays = Period(7, Days)
        self.assertFalse(SevenDays.length() != 7)
        self.assertFalse(SevenDays.units() != Days)
