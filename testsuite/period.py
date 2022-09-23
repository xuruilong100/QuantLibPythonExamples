import unittest

from QuantLib import *

from utilities import *


class PeriodTest(unittest.TestCase):

    def testYearsMonthsAlgebra(self):
        TEST_MESSAGE(
            "Testing period algebra on years/months...")

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
        TEST_MESSAGE(
            "Testing period algebra on weeks/days...")

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

    def testNormalization(self):

        TEST_MESSAGE(
            "Testing period normalization...")

        test_values = [
            Period(0, Days), Period(0, Weeks), Period(0, Months), Period(0, Years), Period(3, Days),
            Period(7, Days), Period(14, Days), Period(30, Days), Period(60, Days), Period(365, Days),
            Period(1, Weeks), Period(2, Weeks), Period(4, Weeks), Period(8, Weeks), Period(52, Weeks),
            Period(1, Months), Period(2, Months), Period(6, Months), Period(12, Months), Period(18, Months),
            Period(24, Months), Period(1, Years), Period(2, Years)]

        for p1 in test_values:
            n1 = p1.normalized()
            self.assertFalse(n1 != p1)

            for p2 in test_values:
                n2 = p2.normalized()
                comparison = (p1 == p2)

                if comparison:
                    self.assertFalse(n1.units() != n2.units() or n1.length() != n2.length())

                if n1.units() == n2.units() and n1.length() == n2.length():
                    self.assertFalse(p1 != p2)
