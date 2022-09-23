import unittest

from QuantLib import *

from utilities import *


class TestCase(object):
    def __init__(self,
                 x,
                 precision,
                 closest,
                 up,
                 down,
                 floor,
                 ceiling):
        self.x = x
        self.precision = precision
        self.closest = closest
        self.up = up
        self.down = down
        self.floor = floor
        self.ceiling = ceiling


testData = [
    TestCase(0.86313513, 5, 0.86314, 0.86314, 0.86313, 0.86314, 0.86313),
    TestCase(0.86313, 5, 0.86313, 0.86313, 0.86313, 0.86313, 0.86313),
    TestCase(-7.64555346, 1, -7.6, -7.7, -7.6, -7.6, -7.6),
    TestCase(0.13961605, 2, 0.14, 0.14, 0.13, 0.14, 0.13),
    TestCase(0.14344179, 4, 0.1434, 0.1435, 0.1434, 0.1434, 0.1434),
    TestCase(-4.74315016, 2, -4.74, -4.75, -4.74, -4.74, -4.74),
    TestCase(-7.82772074, 5, -7.82772, -7.82773, -7.82772, -7.82772, -7.82772),
    TestCase(2.74137947, 3, 2.741, 2.742, 2.741, 2.741, 2.741),
    TestCase(2.13056714, 1, 2.1, 2.2, 2.1, 2.1, 2.1),
    TestCase(-1.06228670, 1, -1.1, -1.1, -1.0, -1.0, -1.1),
    TestCase(8.29234094, 4, 8.2923, 8.2924, 8.2923, 8.2923, 8.2923),
    TestCase(7.90185598, 2, 7.90, 7.91, 7.90, 7.90, 7.90),
    TestCase(-0.26738058, 1, -0.3, -0.3, -0.2, -0.2, -0.3),
    TestCase(1.78128713, 1, 1.8, 1.8, 1.7, 1.8, 1.7),
    TestCase(4.23537260, 1, 4.2, 4.3, 4.2, 4.2, 4.2),
    TestCase(3.64369953, 4, 3.6437, 3.6437, 3.6436, 3.6437, 3.6436),
    TestCase(6.34542470, 2, 6.35, 6.35, 6.34, 6.35, 6.34),
    TestCase(-0.84754962, 4, -0.8475, -0.8476, -0.8475, -0.8475, -0.8475),
    TestCase(4.60998652, 1, 4.6, 4.7, 4.6, 4.6, 4.6),
    TestCase(6.28794223, 3, 6.288, 6.288, 6.287, 6.288, 6.287),
    TestCase(7.89428221, 2, 7.89, 7.90, 7.89, 7.89, 7.89)]


class RoundingTest(unittest.TestCase):

    def testClosest(self):
        TEST_MESSAGE(
            "Testing closest decimal rounding...")

        for i in testData:
            digits = i.precision
            closest = ClosestRounding(digits)
            calculated = closest(i.x)
            expected = i.closest
            self.assertFalse(not close(calculated, expected, 1))

    def testUp(self):
        TEST_MESSAGE(
            "Testing upward decimal rounding...")

        for i in testData:
            digits = i.precision
            up = UpRounding(digits)
            calculated = up(i.x)
            expected = i.up
            self.assertFalse(not close(calculated, expected, 1))

    def testDown(self):
        TEST_MESSAGE(
            "Testing downward decimal rounding...")

        for i in testData:
            digits = i.precision
            down = DownRounding(digits)
            calculated = down(i.x)
            expected = i.down
            self.assertFalse(not close(calculated, expected, 1))

    def testFloor(self):
        TEST_MESSAGE(
            "Testing floor decimal rounding...")

        for i in testData:
            digits = i.precision
            floor = FloorTruncation(digits)
            calculated = floor(i.x)
            expected = i.floor
            self.assertFalse(not close(calculated, expected, 1))

    def testCeiling(self):
        TEST_MESSAGE(
            "Testing ceiling decimal rounding...")

        for i in testData:
            digits = i.precision
            ceiling = CeilingTruncation(digits)
            calculated = ceiling(i.x)
            expected = i.ceiling
            self.assertFalse(not close(calculated, expected, 1))
