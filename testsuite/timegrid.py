import unittest
from utilities import *
from QuantLib import *


class TimeGridTest(unittest.TestCase):

    def CHECK_EQUAL_COLLECTIONS(self, tg, expd):
        self.assertFalse(len(tg) != len(expd))
        for i in range(len(tg)):
            self.assertFalse(
                not close_enough(tg[i], expd[i]))

    def testConstructorAdditionalSteps(self):
        TEST_MESSAGE("Testing TimeGrid construction with additional steps...")

        tg = TimeGrid([1.0, 2.0, 4.0], 8)

        # Expect 8 evenly sized steps over the interval [0, 4].
        expected_times = [
            0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

        self.CHECK_EQUAL_COLLECTIONS(
            tg, expected_times)

    def testConstructorMandatorySteps(self):
        TEST_MESSAGE("Testing TimeGrid construction with only mandatory points...")

        tg = TimeGrid([0.0, 1.0, 2.0, 4.0])

        # grid must include all times from passed iterator.
        # Further no additional times can be added.
        expected_times = [0.0, 1.0, 2.0, 4.0]

        self.CHECK_EQUAL_COLLECTIONS(
            tg, expected_times)

    def testConstructorEvenSteps(self):
        TEST_MESSAGE("Testing TimeGrid construction with n evenly spaced points...")

        end_time = 10
        steps = 5
        tg = TimeGrid(end_time, steps)

        expected_times = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]

        self.CHECK_EQUAL_COLLECTIONS(
            tg, expected_times)

    def testConstructorEmptyIterator(self):
        TEST_MESSAGE(
            "Testing that the TimeGrid constructor raises an error for empty iterators...")

        times = DoubleVector()
        try:
            tg = TimeGrid(times)
        except Exception as e:
            print(e)

    def testConstructorNegativeValuesInIterator(self):
        TEST_MESSAGE("Testing that the TimeGrid constructor raises an error for negative time values...")

        times = [-3.0, 1.0, 4.0, 5.0]
        try:
            tg = TimeGrid(times)
        except Exception as e:
            print(e)

    def testClosestIndex(self):
        TEST_MESSAGE("Testing that the returned index is closest to the requested time...")

        tg = TimeGrid([1.0, 2.0, 5.0])
        expected_index = 3

        self.assertTrue(tg.closestIndex(4) == expected_index)

    def testClosestTime(self):
        TEST_MESSAGE("Testing that the returned time matches the requested index...")
        tg = TimeGrid([1.0, 2.0, 5.0])
        expected_time = 5

        self.assertTrue(tg.closestTime(4) == expected_time)

    def testMandatoryTimes(self):
        TEST_MESSAGE("Testing that mandatory times are recalled correctly...")
        test_times = [1.0, 2.0, 4.0]
        tg = TimeGrid(test_times, 8)

        # Mandatory times are those provided by the original iterator.
        tg_mandatory_times = tg.mandatoryTimes()
        self.CHECK_EQUAL_COLLECTIONS(
            tg_mandatory_times,
            test_times)
