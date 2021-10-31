import unittest
from utilities import *
from QuantLib import *
from math import sqrt, log


class HaugMertonData(object):
    def __init__(self,
                 optType,
                 strike,
                 s,
                 q,
                 r,
                 t,
                 v,
                 jumpIntensity,
                 gamma,
                 result,
                 tol):
        self.type = optType
        self.strike = strike
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.jumpIntensity = jumpIntensity
        self.gamma = gamma
        self.result = result  # result
        self.tol = tol  # tolerance


class JumpDiffusionTest(unittest.TestCase):
    def testMerton76(self):
        TEST_MESSAGE("Testing Merton 76 jump-diffusion model "
                     "for European options...")

        backup = SavedSettings()

        # The data below are from
        # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998, pag 9

        # Haug use the arbitrary truncation criterium of 11 terms in the sum,
        # which doesn't guarantee convergence up to 1e-2.
        # Using Haug's criterium Haug's values have been correctly reproduced.
        # the following values have the right 1e-2 accuracy: any value different
        # from Haug has been noted.

        values = [
            #        type, strike,   spot,    q,    r,    t,  vol, int, gamma, value, tol
            # gamma = 0.25, strike = 80
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.25, 20.67, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.25, 21.74, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.25, 23.63, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.25, 20.65, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.25, 21.70, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.25, 23.61, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.25, 20.64, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.25, 21.70, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.25, 23.61, 1e-2),  # Haug 23.28
            # gamma = 0.25, strike = 90
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.25, 11.00, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.25, 12.74, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.25, 15.40, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.25, 10.98, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.25, 12.75, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.25, 15.42, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.25, 10.98, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.25, 12.75, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.25, 15.42, 1e-2),  # Haug 15.20
            # gamma = 0.25, strike = 100
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.25, 3.42, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.25, 5.88, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.25, 8.95, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.25, 3.51, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.25, 5.96, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.25, 9.02, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.25, 3.53, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.25, 5.97, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.25, 9.03, 1e-2),  # Haug 8.89
            # gamma = 0.25, strike = 110
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.25, 0.55, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.25, 2.11, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.25, 4.67, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.25, 0.56, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.25, 2.16, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.25, 4.73, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.25, 0.56, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.25, 2.17, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.25, 4.74, 1e-2),  # Haug 4.66
            # gamma = 0.25, strike = 120
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.25, 0.10, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.25, 0.64, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.25, 2.23, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.25, 0.06, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.25, 0.63, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.25, 2.25, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.25, 0.05, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.25, 0.62, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.25, 2.25, 1e-2),  # Haug 2.21
            # gamma = 0.50, strike = 80
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.50, 20.72, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.50, 21.83, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.50, 23.71, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.50, 20.66, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.50, 21.73, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.50, 23.63, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.50, 20.65, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.50, 21.71, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.50, 23.61, 1e-2),  # Haug 23.28
            # gamma = 0.50, strike = 90
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.50, 11.04, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.50, 12.72, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.50, 15.34, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.50, 11.02, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.50, 12.76, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.50, 15.41, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.50, 11.00, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.50, 12.75, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.50, 15.41, 1e-2),  # Haug 15.18
            # gamma = 0.50, strike = 100
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.50, 3.14, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.50, 5.58, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.50, 8.71, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.50, 3.39, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.50, 5.87, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.50, 8.96, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.50, 3.46, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.50, 5.93, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.50, 9.00, 1e-2),  # Haug 8.85
            # gamma = 0.50, strike = 110
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.50, 0.53, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.50, 1.93, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.50, 4.42, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.50, 0.58, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.50, 2.11, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.50, 4.67, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.50, 0.57, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.50, 2.14, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.50, 4.71, 1e-2),  # Haug 4.62
            # gamma = 0.50, strike = 120
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.50, 0.19, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.50, 0.71, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.50, 2.15, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.50, 0.10, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.50, 0.66, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.50, 2.23, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.50, 0.07, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.50, 0.64, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.50, 2.24, 1e-2),  # Haug 2.19

            # gamma = 0.75, strike = 80
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.75, 20.79, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.75, 21.96, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.75, 23.86, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.75, 20.68, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.75, 21.78, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.75, 23.67, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.75, 20.66, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.75, 21.74, 1e-2),
            HaugMertonData(Option.Call, 80.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.75, 23.64, 1e-2),  # Haug 23.30
            # gamma = 0.75, strike = 90
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.75, 11.11, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.75, 12.75, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.75, 15.30, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.75, 11.09, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.75, 12.78, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.75, 15.39, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.75, 11.04, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.75, 12.76, 1e-2),
            HaugMertonData(Option.Call, 90.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.75, 15.40, 1e-2),  # Haug 15.17
            # gamma = 0.75, strike = 100
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.75, 2.70, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.75, 5.08, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.75, 8.24, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.75, 3.16, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.75, 5.71, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.75, 8.85, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.75, 3.33, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.75, 5.85, 1e-2),
            HaugMertonData(Option.Call, 100.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.75, 8.95, 1e-2),  # Haug 8.79
            # gamma = 0.75, strike = 110
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.75, 0.54, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.75, 1.69, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.75, 3.99, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.75, 0.62, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.75, 2.05, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.75, 4.57, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.75, 0.60, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.75, 2.11, 1e-2),
            HaugMertonData(Option.Call, 110.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.75, 4.66, 1e-2),  # Haug 4.56
            # gamma = 0.75, strike = 120
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 1.0, 0.75, 0.29, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 1.0, 0.75, 0.84, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 1.0, 0.75, 2.09, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 5.0, 0.75, 0.15, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 5.0, 0.75, 0.71, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 5.0, 0.75, 2.21, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.10, 0.25, 10.0, 0.75, 0.11, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.25, 0.25, 10.0, 0.75, 0.67, 1e-2),
            HaugMertonData(Option.Call, 120.00, 100.00, 0.00, 0.08, 0.50, 0.25, 10.0, 0.75, 2.23, 1e-2)]  # Haug 2.17

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        jumpIntensity = SimpleQuote(0.0)
        meanLogJump = SimpleQuote(0.0)
        jumpVol = SimpleQuote(0.0)

        stochProcess = Merton76Process(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS),
            QuoteHandle(jumpIntensity),
            QuoteHandle(meanLogJump),
            QuoteHandle(jumpVol))
        engine = JumpDiffusionEngine(stochProcess)

        for value in values:
            payoff = PlainVanillaPayoff(value.type, value.strike)

            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)

            jumpIntensity.setValue(value.jumpIntensity)

            # delta in Haug's notation
            jVol = value.v * sqrt(value.gamma / value.jumpIntensity)
            jumpVol.setValue(jVol)

            # z in Haug's notation
            diffusionVol = value.v * sqrt(1.0 - value.gamma)
            vol.setValue(diffusionVol)

            # Haug is assuming zero meanJump
            meanJump = 0.0
            meanLogJump.setValue(log(1.0 + meanJump) - 0.5 * jVol * jVol)

            totalVol = sqrt(value.jumpIntensity * jVol * jVol + diffusionVol * diffusionVol)
            volError = abs(totalVol - value.v)
            self.assertFalse(volError >= 1e-13)

            option = VanillaOption(payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testGreeks(self):
        TEST_MESSAGE("Testing jump-diffusion option greeks...")

        backup = SavedSettings()

        calculated = dict()
        expected = dict()
        tolerance = dict()
        tolerance["delta"] = 1.0e-4
        tolerance["gamma"] = 1.0e-4
        tolerance["theta"] = 1.1e-4
        tolerance["rho"] = 1.0e-4
        tolerance["divRho"] = 1.0e-4
        tolerance["vega"] = 1.0e-4

        types = [Option.Put, Option.Call]
        strikes = [50.0, 100.0, 150.0]
        underlyings = [100.0]
        qRates = [-0.05, 0.0, 0.05]
        rRates = [0.0, 0.01, 0.2]
        # The testsuite check fails if a too short maturity is chosen(i.e. 1 year).
        # The problem is in the theta calculation. With the finite difference(fd) method
        # we might get values too close to the jump steps, invalidating the fd methodology
        # for calculating greeks.
        residualTimes = [5.0]
        vols = [0.11]
        jInt = [1.0, 5.0]
        mLJ = [-0.20, 0.0, 0.20]
        jV = [0.01, 0.25]

        dc = Actual360()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = today

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(vol, dc))

        jumpIntensity = SimpleQuote(0.0)
        meanLogJump = SimpleQuote(0.0)
        jumpVol = SimpleQuote(0.0)

        stochProcess = Merton76Process(
            QuoteHandle(spot), qTS, rTS, volTS,
            QuoteHandle(jumpIntensity),
            QuoteHandle(meanLogJump),
            QuoteHandle(jumpVol))

        payoff = None

        # The jumpdiffusionengine greeks are very sensitive to the
        # convergence level.  A tolerance of 1.0e-08 is usually
        # sufficient to get reasonable results
        engine = JumpDiffusionEngine(stochProcess, 1e-08)

        for optType in types:
            for strike in strikes:
                for jj1 in jInt:
                    jumpIntensity.setValue(jj1)
                    for jj2 in mLJ:
                        meanLogJump.setValue(jj2)
                        for jj3 in jV:
                            jumpVol.setValue(jj3)
                            for residualTime in residualTimes:
                                exDate = today + timeToDays(residualTime)
                                exercise = EuropeanExercise(exDate)
                                for kk in range(0, 1):
                                    # option to check
                                    if kk == 0:
                                        payoff = PlainVanillaPayoff(optType, strike)

                                    if kk == 1:
                                        payoff = CashOrNothingPayoff(optType, strike, 100.0)

                                    option = EuropeanOption(payoff, exercise)
                                    option.setPricingEngine(engine)

                                    for u in underlyings:
                                        for q in qRates:
                                            for r in rRates:
                                                for v in vols:
                                                    spot.setValue(u)
                                                    qRate.setValue(q)
                                                    rRate.setValue(r)
                                                    vol.setValue(v)

                                                    value = option.NPV()
                                                    calculated["delta"] = option.delta()
                                                    calculated["gamma"] = option.gamma()
                                                    calculated["theta"] = option.theta()
                                                    calculated["rho"] = option.rho()
                                                    calculated["divRho"] = option.dividendRho()
                                                    calculated["vega"] = option.vega()

                                                    if value > spot.value() * 1.0e-5:
                                                        # perturb spot and get delta and gamma
                                                        du = u * 1.0e-5
                                                        spot.setValue(u + du)
                                                        value_p = option.NPV()
                                                        delta_p = option.delta()
                                                        spot.setValue(u - du)
                                                        value_m = option.NPV()
                                                        delta_m = option.delta()
                                                        spot.setValue(u)
                                                        expected["delta"] = (value_p - value_m) / (2 * du)
                                                        expected["gamma"] = (delta_p - delta_m) / (2 * du)

                                                        # perturb rates and get rho and dividend rho
                                                        dr = 1.0e-5
                                                        rRate.setValue(r + dr)
                                                        value_p = option.NPV()
                                                        rRate.setValue(r - dr)
                                                        value_m = option.NPV()
                                                        rRate.setValue(r)
                                                        expected["rho"] = (value_p - value_m) / (2 * dr)

                                                        dq = 1.0e-5
                                                        qRate.setValue(q + dq)
                                                        value_p = option.NPV()
                                                        qRate.setValue(q - dq)
                                                        value_m = option.NPV()
                                                        qRate.setValue(q)
                                                        expected["divRho"] = (value_p - value_m) / (2 * dq)

                                                        # perturb volatility and get vega
                                                        dv = v * 1.0e-4
                                                        vol.setValue(v + dv)
                                                        value_p = option.NPV()
                                                        vol.setValue(v - dv)
                                                        value_m = option.NPV()
                                                        vol.setValue(v)
                                                        expected["vega"] = (value_p - value_m) / (2 * dv)

                                                        # get theta from time-shifted options
                                                        dT = dc.yearFraction(today - 1, today + 1)
                                                        Settings.instance().evaluationDate = today - Period(1, Days)
                                                        value_m = option.NPV()
                                                        Settings.instance().evaluationDate = today + Period(1, Days)
                                                        value_p = option.NPV()
                                                        Settings.instance().evaluationDate = today
                                                        expected["theta"] = (value_p - value_m) / dT
                                                        # compare

                                                        for it in expected.keys():
                                                            greek = it
                                                            expct = expected[greek]
                                                            calcl = calculated[greek]
                                                            tol = tolerance[greek]
                                                            error = abs(expct - calcl)
                                                            self.assertFalse(error > tol)
