import unittest

from QuantLib import *

from utilities import *


class SingleCase(object):
    def __init__(self,
                 calendar,
                 convention,
                 start,
                 period,
                 endOfMonth,
                 result):
        self.calendar = calendar
        self.convention = convention
        self.start = start
        self.period = period
        self.endOfMonth = endOfMonth
        self.result = result


class BusinessDayConventionTest(unittest.TestCase):

    def testConventions(self):
        TEST_MESSAGE(
            "Testing business day conventions...")
        testCases = [
            SingleCase(SouthAfrica(), Following, Date(3, February, 2015), Period(1, Months), false, Date(3, March, 2015)),
            SingleCase(SouthAfrica(), Following, Date(3, February, 2015), Period(4, Days), false, Date(9, February, 2015)),
            SingleCase(SouthAfrica(), Following, Date(31, January, 2015), Period(1, Months), true, Date(27, February, 2015)),
            SingleCase(SouthAfrica(), Following, Date(31, January, 2015), Period(1, Months), false, Date(2, March, 2015)),
            SingleCase(SouthAfrica(), ModifiedFollowing, Date(3, February, 2015), Period(1, Months), false, Date(3, March, 2015)),
            SingleCase(SouthAfrica(), ModifiedFollowing, Date(3, February, 2015), Period(4, Days), false, Date(9, February, 2015)),
            SingleCase(SouthAfrica(), ModifiedFollowing, Date(31, January, 2015), Period(1, Months), true, Date(27, February, 2015)),
            SingleCase(SouthAfrica(), ModifiedFollowing, Date(31, January, 2015), Period(1, Months), false, Date(27, February, 2015)),
            SingleCase(SouthAfrica(), ModifiedFollowing, Date(25, March, 2015), Period(1, Months), false, Date(28, April, 2015)),
            SingleCase(SouthAfrica(), ModifiedFollowing, Date(7, February, 2015), Period(1, Months), false, Date(9, March, 2015)),
            SingleCase(SouthAfrica(), Preceding, Date(3, March, 2015), Period(-1, Months), false, Date(3, February, 2015)),
            SingleCase(SouthAfrica(), Preceding, Date(3, February, 2015), Period(-2, Days), false, Date(30, January, 2015)),
            SingleCase(SouthAfrica(), Preceding, Date(1, March, 2015), Period(-1, Months), true, Date(30, January, 2015)),
            SingleCase(SouthAfrica(), Preceding, Date(1, March, 2015), Period(-1, Months), false, Date(30, January, 2015)),
            SingleCase(SouthAfrica(), ModifiedPreceding, Date(3, March, 2015), Period(-1, Months), false, Date(3, February, 2015)),
            SingleCase(SouthAfrica(), ModifiedPreceding, Date(3, February, 2015), Period(-2, Days), false, Date(30, January, 2015)),
            SingleCase(SouthAfrica(), ModifiedPreceding, Date(1, March, 2015), Period(-1, Months), true, Date(2, February, 2015)),
            SingleCase(SouthAfrica(), ModifiedPreceding, Date(1, March, 2015), Period(-1, Months), false, Date(2, February, 2015)),
            SingleCase(SouthAfrica(), Unadjusted, Date(3, February, 2015), Period(1, Months), false, Date(3, March, 2015)),
            SingleCase(SouthAfrica(), Unadjusted, Date(3, February, 2015), Period(4, Days), false, Date(9, February, 2015)),
            SingleCase(SouthAfrica(), Unadjusted, Date(31, January, 2015), Period(1, Months), true, Date(27, February, 2015)),
            SingleCase(SouthAfrica(), Unadjusted, Date(31, January, 2015), Period(1, Months), false, Date(28, February, 2015)),
            SingleCase(SouthAfrica(), HalfMonthModifiedFollowing, Date(3, February, 2015), Period(1, Months), false, Date(3, March, 2015)),
            SingleCase(SouthAfrica(), HalfMonthModifiedFollowing, Date(3, February, 2015), Period(4, Days), false, Date(9, February, 2015)),
            SingleCase(SouthAfrica(), HalfMonthModifiedFollowing, Date(31, January, 2015), Period(1, Months), true, Date(27, February, 2015)),
            SingleCase(SouthAfrica(), HalfMonthModifiedFollowing, Date(31, January, 2015), Period(1, Months), false, Date(27, February, 2015)),
            SingleCase(SouthAfrica(), HalfMonthModifiedFollowing, Date(3, January, 2015), Period(1, Weeks), false, Date(12, January, 2015)),
            SingleCase(SouthAfrica(), HalfMonthModifiedFollowing, Date(21, March, 2015), Period(1, Weeks), false, Date(30, March, 2015)),
            SingleCase(SouthAfrica(), HalfMonthModifiedFollowing, Date(7, February, 2015), Period(1, Months), false, Date(9, March, 2015)),
            SingleCase(SouthAfrica(), Nearest, Date(3, February, 2015), Period(1, Months), false, Date(3, March, 2015)),
            SingleCase(SouthAfrica(), Nearest, Date(3, February, 2015), Period(4, Days), false, Date(9, February, 2015)),
            SingleCase(SouthAfrica(), Nearest, Date(16, April, 2015), Period(1, Months), false, Date(15, May, 2015)),
            SingleCase(SouthAfrica(), Nearest, Date(17, April, 2015), Period(1, Months), false, Date(18, May, 2015)),
            SingleCase(SouthAfrica(), Nearest, Date(4, March, 2015), Period(1, Months), false, Date(2, April, 2015)),
            SingleCase(SouthAfrica(), Nearest, Date(2, April, 2015), Period(1, Months), false, Date(4, May, 2015))]

        n = len(testCases)
        for i in range(n):
            calendar = testCases[i].calendar
            result = calendar.advance(
                testCases[i].start,
                testCases[i].period,
                testCases[i].convention,
                testCases[i].endOfMonth)

            self.assertTrue(result == testCases[i].result)
