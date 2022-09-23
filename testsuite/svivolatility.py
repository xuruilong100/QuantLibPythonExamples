import unittest
from math import exp

from QuantLib import *

from utilities import *


class SviVolatilityTest(unittest.TestCase):

    def testSviSmileSection(self):
        TEST_MESSAGE(
            "Testing SviSmileSection construction...")

        today = Settings.instance().evaluationDate

        tte = 11.0 / 365
        forward = 123.45
        a = -2.21
        b = 7.61
        sigma = 0.337
        rho = 0.439
        m = 0.193
        sviParameters = [a, b, sigma, rho, m]

        strike = forward * exp(m)

        time_section = SviSmileSection(tte, forward, sviParameters)
        self.assertEqual(time_section.atmLevel(), forward)
        self.assertFalse(abs(time_section.variance(strike) - (a + b * sigma)) > 1E-10)

        date = today + Period(11, Days)

        date_section = SviSmileSection(date, forward, sviParameters)
        self.assertEqual(date_section.atmLevel(), forward)
        self.assertFalse(abs(date_section.variance(strike) - (a + b * sigma)) > 1E-10)
