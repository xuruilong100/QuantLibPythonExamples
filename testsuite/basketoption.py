import unittest
from utilities import *
from QuantLib import *
from enum import Enum


class BasketType(Enum):
    MinBasket = 0
    MaxBasket = 1
    SpreadBasket = 2


def basketTypeToPayoff(basketType, p):
    if basketType == BasketType.MinBasket:
        return MinBasketPayoff(p)
    elif basketType == BasketType.MaxBasket:
        return MaxBasketPayoff(p)
    elif basketType == BasketType.SpreadBasket:
        return SpreadBasketPayoff(p)


class BasketOptionOneData(object):
    def __init__(self,
                 typeOpt,
                 strike,
                 s,
                 q,
                 r,
                 t,
                 v,
                 result,
                 tol):
        self.typeOpt = typeOpt
        self.strike = strike
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.result = result  # expected result
        self.tol = tol  # tolerance


class BasketOptionTwoData(object):
    def __init__(self,
                 basketType,
                 typeOpt,
                 strike,
                 s1,
                 s2,
                 q1,
                 q2,
                 r,
                 t,
                 v1,
                 v2,
                 rho,
                 result,
                 tol):
        self.basketType = basketType
        self.typeOpt = typeOpt
        self.strike = strike
        self.s1 = s1
        self.s2 = s2
        self.q1 = q1
        self.q2 = q2
        self.r = r
        self.t = t
        self.v1 = v1
        self.v2 = v2
        self.rho = rho
        self.result = result
        self.tol = tol


class BasketOptionThreeData(object):
    def __init__(self,
                 basketType,
                 typeOpt,
                 strike,
                 s1,
                 s2,
                 s3,
                 r,
                 t,
                 v1,
                 v2,
                 v3,
                 rho,
                 euroValue,
                 amValue):
        self.basketType = basketType
        self.typeOpt = typeOpt
        self.strike = strike
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.r = r
        self.t = t
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.rho = rho
        self.euroValue = euroValue
        self.amValue = amValue


class BasketOptionTest(unittest.TestCase):
    def testEuroTwoValues(self):
        TEST_MESSAGE("Testing two-asset European basket options...")

        # Data from:
        # Excel spreadsheet www.maths.ox.ac.uk/~firth/computing/excel.shtml
        # and
        # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 pag 56-58
        # European two asset max basket options

        values = [
            #      basketType,   optionType, strike,    s1,    s2,   q1,   q2,    r,    t,   v1,   v2,  rho, result, tol
            # data from http://www.maths.ox.ac.uk/~firth/computing/excel.shtml
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.90, 10.898, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.70, 8.483, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.50, 6.844, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.30, 5.531, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.10, 4.413, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.50, 0.70, 0.00, 4.981, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.50, 0.30, 0.00, 4.159, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.50, 0.10, 0.00, 2.597, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.50, 0.10, 0.50, 4.030, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.90, 17.565, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.70, 19.980, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.50, 21.619, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.30, 22.932, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.10, 24.049, 1.1e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 80.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.30, 16.508, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 80.0, 80.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.30, 8.049, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 80.0, 120.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.30, 30.141, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 100.0, 120.0, 120.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.30, 42.889, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.90, 11.369, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.70, 12.856, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.50, 13.890, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.30, 14.741, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.10, 15.485, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 0.50, 0.30, 0.30, 0.10, 11.893, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 0.25, 0.30, 0.30, 0.10, 8.881, 1.0e-3),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 2.00, 0.30, 0.30, 0.10, 19.268, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.90, 7.339, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.70, 5.853, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.50, 4.818, 1.0e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.30, 3.967, 1.1e-3),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Put, 100.0, 100.0, 100.0, 0.00, 0.00, 0.05, 1.00, 0.30, 0.30, 0.10, 3.223, 1.0e-3),
            #      basketType,   optionType, strike,    s1,    s2,   q1,   q2,    r,    t,   v1,   v2,  rho,  result, tol
            # data from "Option pricing formulas" VB code + spreadsheet
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 98.0, 100.0, 105.0, 0.00, 0.00, 0.05, 0.50, 0.11, 0.16, 0.63, 4.8177, 1.0e-4),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 98.0, 100.0, 105.0, 0.00, 0.00, 0.05, 0.50, 0.11, 0.16, 0.63, 11.6323, 1.0e-4),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 98.0, 100.0, 105.0, 0.00, 0.00, 0.05, 0.50, 0.11, 0.16, 0.63, 2.0376, 1.0e-4),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Put, 98.0, 100.0, 105.0, 0.00, 0.00, 0.05, 0.50, 0.11, 0.16, 0.63, 0.5731, 1.0e-4),
            BasketOptionTwoData(BasketType.MinBasket, Option.Call, 98.0, 100.0, 105.0, 0.06, 0.09, 0.05, 0.50, 0.11, 0.16, 0.63, 2.9340, 1.0e-4),
            BasketOptionTwoData(BasketType.MinBasket, Option.Put, 98.0, 100.0, 105.0, 0.06, 0.09, 0.05, 0.50, 0.11, 0.16, 0.63, 3.5224, 1.0e-4),
            # data from "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 pag 58
            BasketOptionTwoData(BasketType.MaxBasket, Option.Call, 98.0, 100.0, 105.0, 0.06, 0.09, 0.05, 0.50, 0.11, 0.16, 0.63, 8.0701, 1.0e-4),
            BasketOptionTwoData(BasketType.MaxBasket, Option.Put, 98.0, 100.0, 105.0, 0.06, 0.09, 0.05, 0.50, 0.11, 0.16, 0.63, 1.2181, 1.0e-4),
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 pag 59-60
            # Kirk approx. for a european spread option on two futures*/
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.20, 0.20, -0.5, 4.7530, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.20, 0.20, 0.0, 3.7970, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.20, 0.20, 0.5, 2.5537, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.25, 0.20, -0.5, 5.4275, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.25, 0.20, 0.0, 4.3712, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.25, 0.20, 0.5, 3.0086, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.20, 0.25, -0.5, 5.4061, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.20, 0.25, 0.0, 4.3451, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.1, 0.20, 0.25, 0.5, 2.9723, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.20, 0.20, -0.5, 10.7517, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.20, 0.20, 0.0, 8.7020, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.20, 0.20, 0.5, 6.0257, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.25, 0.20, -0.5, 12.1941, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.25, 0.20, 0.0, 9.9340, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.25, 0.20, 0.5, 7.0067, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.20, 0.25, -0.5, 12.1483, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.20, 0.25, 0.0, 9.8780, 1.0e-3),
            BasketOptionTwoData(BasketType.SpreadBasket, Option.Call, 3.0, 122.0, 120.0, 0.0, 0.0, 0.10, 0.5, 0.20, 0.25, 0.5, 6.9284, 1.0e-3)
        ]

        dc = Actual360()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = today

        spot1 = SimpleQuote(0.0)
        spot2 = SimpleQuote(0.0)

        qRate1 = SimpleQuote(0.0)
        qTS1 = flatRate(today, qRate1, dc)
        qRate2 = SimpleQuote(0.0)
        qTS2 = flatRate(today, qRate2, dc)

        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)

        vol1 = SimpleQuote(0.0)
        volTS1 = flatVol(today, vol1, dc)
        vol2 = SimpleQuote(0.0)
        volTS2 = flatVol(today, vol2, dc)

        mcRelativeErrorTolerance = 0.01
        fdRelativeErrorTolerance = 0.01

        for value in values:

            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)

            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot1.setValue(value.s1)
            spot2.setValue(value.s2)
            qRate1.setValue(value.q1)
            qRate2.setValue(value.q2)
            rRate.setValue(value.r)
            vol1.setValue(value.v1)
            vol2.setValue(value.v2)

            analyticEngine = None
            p1 = None
            p2 = None

            if value.basketType == BasketType.MaxBasket or value.basketType == BasketType.MinBasket:
                p1 = BlackScholesMertonProcess(
                    QuoteHandle(spot1), YieldTermStructureHandle(qTS1),
                    YieldTermStructureHandle(rTS), BlackVolTermStructureHandle(volTS1))
                p2 = BlackScholesMertonProcess(
                    QuoteHandle(spot2), YieldTermStructureHandle(qTS2),
                    YieldTermStructureHandle(rTS), BlackVolTermStructureHandle(volTS2))
                analyticEngine = StulzEngine(p1, p2, value.rho)
            elif value.basketType == BasketType.SpreadBasket:
                p1 = BlackProcess(
                    QuoteHandle(spot1), YieldTermStructureHandle(rTS),
                    BlackVolTermStructureHandle(volTS1))
                p2 = BlackProcess(
                    QuoteHandle(spot2), YieldTermStructureHandle(rTS),
                    BlackVolTermStructureHandle(volTS2))
                analyticEngine = KirkEngine(
                    p1, p2, value.rho)

            procs = [p1, p2]

            correlationMatrix = Matrix(2, 2, value.rho)
            for j in range(2):
                correlationMatrix[j][j] = 1.0

            process = StochasticProcessArray(
                procs, correlationMatrix)

            mcEngine = MakeMCPREuropeanBasketEngine(process)
            mcEngine.withStepsPerYear(1)
            mcEngine.withSamples(10000)
            mcEngine.withSeed(42)
            mcEngine = mcEngine.makeEngine()

            fdEngine = Fd2dBlackScholesVanillaEngine(p1, p2, value.rho, 50, 50, 15)

            basketOption = BasketOption(basketTypeToPayoff(value.basketType, payoff), exercise)

            # analytic engine
            basketOption.setPricingEngine(analyticEngine)
            calculated = basketOption.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

            # fd engine
            basketOption.setPricingEngine(fdEngine)
            calculated = basketOption.NPV()
            relError = relativeError(calculated, expected, expected)
            self.assertFalse(relError > mcRelativeErrorTolerance)

            # mc engine
            basketOption.setPricingEngine(mcEngine)
            calculated = basketOption.NPV()
            relError = relativeError(calculated, expected, value.s1)
            self.assertFalse(relError > mcRelativeErrorTolerance)

    def testBarraquandThreeValues(self):
        TEST_MESSAGE("Testing three-asset basket options "
                     "against Barraquand's values...")

        # Data from:
        # "Numerical Valuation of High Dimensional American Securities"
        # Barraquand, J. and Martineau, D.
        # Journal of Financial and Quantitative Analysis 1995 3(30) 383-405
        values = [
            # time in months is with 30 days to the month..
            # basketType, optionType,       strike,    s1,    s2,   s3,    r,    t,   v1,   v2,  v3,  rho, euro, american,
            # Table 2
            # not using 4 month case to speed up test
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.0, 8.59, 8.59),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.0, 3.84, 3.84),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.0, 0.89, 0.89),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.0, 12.55, 12.55),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.0, 7.87, 7.87),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.0, 4.26, 4.26),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.0, 15.29, 15.29),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.0, 10.72, 10.72),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.0, 6.96, 6.96),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.5, 7.78, 7.78),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.5, 3.18, 3.18),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.5, 0.82, 0.82),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.5, 10.97, 10.97),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.5, 6.69, 6.69),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.5, 3.70, 3.70),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.5, 13.23, 13.23),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.5, 9.11, 9.11),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.5, 5.98, 5.98),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 1.0, 6.53, 6.53),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 1.0, 2.38, 2.38),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 1.0, 0.74, 0.74),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 1.0, 8.51, 8.51),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 1.0, 4.92, 4.92),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 1.0, 2.97, 2.97),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 35.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 1.0, 10.04, 10.04),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 40.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 1.0, 6.64, 6.64),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 45.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 1.0, 4.61, 4.61),
            # Table 3
            BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 35.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.0, 0.00, 0.00),
            BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 40.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.0, 0.13, 0.23),
            BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.0, 2.26, 5.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put,  35.0,  40.0,  40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.0, 0.01, 0.01),
            BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 40.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.0, 0.25, 0.44),
            BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.0, 1.55, 5.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put,  35.0,  40.0,  40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.0, 0.03, 0.04),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put,  40.0,  40.0,  40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.0, 0.31, 0.57),
            BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.0, 1.41, 5.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 35.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.5, 0.00, 0.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 40.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.5, 0.38, 0.48),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 0.5, 3.00, 5.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 35.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.5, 0.07, 0.09),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 40.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.5, 0.72, 0.93),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 0.5, 2.65, 5.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 35.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.5, 0.17, 0.20),
            BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 40.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.5, 0.91, 1.19),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 0.5, 2.63, 5.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 35.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 1.0, 0.01, 0.01),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 40.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 1.0, 0.84, 0.08),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 1.00, 0.20, 0.30, 0.50, 1.0, 4.18, 5.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 35.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 1.0, 0.19, 0.19),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 40.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 1.0, 1.51, 1.56),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 4.00, 0.20, 0.30, 0.50, 1.0, 4.49, 5.00),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 35.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 1.0, 0.41, 0.42),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 40.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 1.0, 1.87, 1.96),
            # BasketOptionThreeData(BasketType.MaxBasket, Option.Put, 45.0, 40.0, 40.0, 40.0, 0.05, 7.00, 0.20, 0.30, 0.50, 1.0, 4.70, 5.20)
        ]

        dc = Actual360()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = today

        spot1 = SimpleQuote(0.0)
        spot2 = SimpleQuote(0.0)
        spot3 = SimpleQuote(0.0)

        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)

        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)

        vol1 = SimpleQuote(0.0)
        volTS1 = flatVol(today, vol1, dc)
        vol2 = SimpleQuote(0.0)
        volTS2 = flatVol(today, vol2, dc)
        vol3 = SimpleQuote(0.0)
        volTS3 = flatVol(today, vol3, dc)

        for value in values:

            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)

            exDate = today + int(value.t) * 30
            exercise = EuropeanExercise(exDate)
            amExercise = AmericanExercise(today, exDate)

            spot1.setValue(value.s1)
            spot2.setValue(value.s2)
            spot3.setValue(value.s3)
            rRate.setValue(value.r)
            vol1.setValue(value.v1)
            vol2.setValue(value.v2)
            vol3.setValue(value.v3)

            stochProcess1 = BlackScholesMertonProcess(
                QuoteHandle(spot1),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS1))

            stochProcess2 = BlackScholesMertonProcess(
                QuoteHandle(spot2),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS2))

            stochProcess3 = BlackScholesMertonProcess(
                QuoteHandle(spot3),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS3))

            procs = [stochProcess1, stochProcess2, stochProcess3]

            correlation = Matrix(3, 3, value.rho)
            for j in range(3):
                correlation[j][j] = 1.0

            # FLOATING_POINT_EXCEPTION
            process = StochasticProcessArray(procs, correlation)

            # use a 3D sobol sequence...
            # Think long and hard before moving to more than 1 timestep....
            mcQuasiEngine = MakeMCLDEuropeanBasketEngine(process)
            mcQuasiEngine.withStepsPerYear(1)
            mcQuasiEngine.withSamples(8091)
            mcQuasiEngine.withSeed(42)
            mcQuasiEngine = mcQuasiEngine.makeEngine()

            euroBasketOption = BasketOption(basketTypeToPayoff(value.basketType, payoff), exercise)
            euroBasketOption.setPricingEngine(mcQuasiEngine)

            expected = value.euroValue
            calculated = euroBasketOption.NPV()
            relError = relativeError(calculated, expected, value.s1)
            mcRelativeErrorTolerance = 0.01
            self.assertFalse(relError > mcRelativeErrorTolerance)

            requiredSamples = 1000
            timeSteps = 500
            seed = 1
            mcLSMCEngine = MakeMCPRAmericanBasketEngine(process)
            mcLSMCEngine.withSteps(timeSteps)
            mcLSMCEngine.withAntitheticVariate()
            mcLSMCEngine.withSamples(requiredSamples)
            mcLSMCEngine.withCalibrationSamples(int(requiredSamples / 4))
            mcLSMCEngine.withSeed(seed)
            mcLSMCEngine = mcLSMCEngine.makeEngine()

            amBasketOption = BasketOption(basketTypeToPayoff(value.basketType, payoff), amExercise)
            amBasketOption.setPricingEngine(mcLSMCEngine)

            expected = value.amValue
            calculated = amBasketOption.NPV()
            relError = relativeError(calculated, expected, value.s1)
            mcAmericanRelativeErrorTolerance = 0.01
            self.assertFalse(relError > mcAmericanRelativeErrorTolerance)

    def testTavellaValues(self):
        TEST_MESSAGE("Testing three-asset American basket options "
                     "against Tavella's values...")

        # Data from:
        # "Quantitative Methods in Derivatives Pricing"
        # Tavella, D. A.   -   Wiley (2002)

        values = [
            # time in months is with 30 days to the month..
            # basketType, optionType,       strike,    s1,    s2,   s3,    r,    t,   v1,   v2,  v3,  rho, euroValue, american Value,
            BasketOptionThreeData(BasketType.MaxBasket, Option.Call, 100, 100, 100, 100, 0.05, 3.00, 0.20, 0.20, 0.20, 0.0, -999, 18.082)
        ]

        dc = Actual360()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = today

        spot1 = SimpleQuote(0.0)
        spot2 = SimpleQuote(0.0)
        spot3 = SimpleQuote(0.0)

        qRate = SimpleQuote(0.1)
        qTS = flatRate(today, qRate, dc)

        rRate = SimpleQuote(0.05)
        rTS = flatRate(today, rRate, dc)

        vol1 = SimpleQuote(0.0)
        volTS1 = flatVol(today, vol1, dc)
        vol2 = SimpleQuote(0.0)
        volTS2 = flatVol(today, vol2, dc)
        vol3 = SimpleQuote(0.0)
        volTS3 = flatVol(today, vol3, dc)

        mcRelativeErrorTolerance = 0.01
        requiredSamples = 10000
        timeSteps = 20
        seed = 0

        payoff = PlainVanillaPayoff(values[0].typeOpt, values[0].strike)

        exDate = today + timeToDays(values[0].t)
        exercise = AmericanExercise(today, exDate)

        spot1.setValue(values[0].s1)
        spot2.setValue(values[0].s2)
        spot3.setValue(values[0].s3)
        vol1.setValue(values[0].v1)
        vol2.setValue(values[0].v2)
        vol3.setValue(values[0].v3)

        stochProcess1 = BlackScholesMertonProcess(
            QuoteHandle(spot1),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS1))

        stochProcess2 = BlackScholesMertonProcess(
            QuoteHandle(spot2),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS2))

        stochProcess3 = BlackScholesMertonProcess(
            QuoteHandle(spot3),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS3))

        procs = [
            stochProcess1, stochProcess2, stochProcess3]

        correlation = Matrix(3, 3, 0.0)
        for j in range(3):
            correlation[j][j] = 1.0

        correlation[1][0] = -0.25
        correlation[0][1] = -0.25
        correlation[2][0] = 0.25
        correlation[0][2] = 0.25
        correlation[2][1] = 0.3
        correlation[1][2] = 0.3

        process = StochasticProcessArray(procs, correlation)
        mcLSMCEngine = MakeMCPRAmericanBasketEngine(process)
        mcLSMCEngine.withSteps(timeSteps)
        mcLSMCEngine.withAntitheticVariate()
        mcLSMCEngine.withSamples(requiredSamples)
        mcLSMCEngine.withCalibrationSamples(int(requiredSamples / 4))
        mcLSMCEngine.withSeed(seed)
        mcLSMCEngine = mcLSMCEngine.makeEngine()

        basketOption = BasketOption(basketTypeToPayoff(
            values[0].basketType,
            payoff),
            exercise)
        basketOption.setPricingEngine(mcLSMCEngine)

        calculated = basketOption.NPV()
        expected = values[0].amValue
        errorEstimate = basketOption.errorEstimate()
        relError = relativeError(calculated, expected, values[0].s1)
        self.assertFalse(relError > mcRelativeErrorTolerance)

    def testOneDAmericanValues(self):
        oneDataValues = [
            #        type, strike,   spot,    q,    r,    t,  vol,   value, tol
            BasketOptionOneData(Option.Put, 100.00, 80.00, 0.0, 0.06, 0.5, 0.4, 21.6059, 1e-2),
            BasketOptionOneData(Option.Put, 100.00, 85.00, 0.0, 0.06, 0.5, 0.4, 18.0374, 1e-2),
            BasketOptionOneData(Option.Put, 100.00, 90.00, 0.0, 0.06, 0.5, 0.4, 14.9187, 1e-2),
            BasketOptionOneData(Option.Put, 100.00, 95.00, 0.0, 0.06, 0.5, 0.4, 12.2314, 1e-2),
            BasketOptionOneData(Option.Put, 100.00, 100.00, 0.0, 0.06, 0.5, 0.4, 9.9458, 1e-2),
            BasketOptionOneData(Option.Put, 100.00, 105.00, 0.0, 0.06, 0.5, 0.4, 8.0281, 1e-2),
            BasketOptionOneData(Option.Put, 100.00, 110.00, 0.0, 0.06, 0.5, 0.4, 6.4352, 1e-2),
            BasketOptionOneData(Option.Put, 100.00, 115.00, 0.0, 0.06, 0.5, 0.4, 5.1265, 1e-2),
            BasketOptionOneData(Option.Put, 100.00, 120.00, 0.0, 0.06, 0.5, 0.4, 4.0611, 1e-2),

            # Longstaff Schwartz 1D example
            # use constant and three Laguerre polynomials
            # 100,000 paths and 50 timesteps per year
            BasketOptionOneData(Option.Put, 40.00, 36.00, 0.0, 0.06, 1.0, 0.2, 4.478, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 36.00, 0.0, 0.06, 2.0, 0.2, 4.840, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 36.00, 0.0, 0.06, 1.0, 0.4, 7.101, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 36.00, 0.0, 0.06, 2.0, 0.4, 8.508, 1e-2),

            BasketOptionOneData(Option.Put, 40.00, 38.00, 0.0, 0.06, 1.0, 0.2, 3.250, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 38.00, 0.0, 0.06, 2.0, 0.2, 3.745, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 38.00, 0.0, 0.06, 1.0, 0.4, 6.148, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 38.00, 0.0, 0.06, 2.0, 0.4, 7.670, 1e-2),

            BasketOptionOneData(Option.Put, 40.00, 40.00, 0.0, 0.06, 1.0, 0.2, 2.314, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 40.00, 0.0, 0.06, 2.0, 0.2, 2.885, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 40.00, 0.0, 0.06, 1.0, 0.4, 5.312, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 40.00, 0.0, 0.06, 2.0, 0.4, 6.920, 1e-2),

            BasketOptionOneData(Option.Put, 40.00, 42.00, 0.0, 0.06, 1.0, 0.2, 1.617, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 42.00, 0.0, 0.06, 2.0, 0.2, 2.212, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 42.00, 0.0, 0.06, 1.0, 0.4, 4.582, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 42.00, 0.0, 0.06, 2.0, 0.4, 6.248, 1e-2),

            BasketOptionOneData(Option.Put, 40.00, 44.00, 0.0, 0.06, 1.0, 0.2, 1.110, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 44.00, 0.0, 0.06, 2.0, 0.2, 1.690, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 44.00, 0.0, 0.06, 1.0, 0.4, 3.948, 1e-2),
            BasketOptionOneData(Option.Put, 40.00, 44.00, 0.0, 0.06, 2.0, 0.4, 5.647, 1e-2)
        ]

        TEST_MESSAGE("Testing basket American options against 1-D case ...")

        dc = Actual360()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = today

        spot1 = SimpleQuote(0.0)

        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)

        rRate = SimpleQuote(0.05)
        rTS = flatRate(today, rRate, dc)

        vol1 = SimpleQuote(0.0)
        volTS1 = flatVol(today, vol1, dc)

        requiredSamples = 10000
        timeSteps = 52
        seed = 0

        stochProcess1 = BlackScholesMertonProcess(
            QuoteHandle(spot1),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS1))

        procs = [stochProcess1]

        correlation = Matrix(1, 1, 1.0)

        process = StochasticProcessArray(procs, correlation)

        mcLSMCEngine = MakeMCPRAmericanBasketEngine(process)
        mcLSMCEngine.withSteps(timeSteps)
        mcLSMCEngine.withAntitheticVariate()
        mcLSMCEngine.withSamples(requiredSamples)
        mcLSMCEngine.withCalibrationSamples(int(requiredSamples / 4))
        mcLSMCEngine.withSeed(seed)
        mcLSMCEngine = mcLSMCEngine.makeEngine()

        for i in range(len(oneDataValues)):
            payoff = PlainVanillaPayoff(oneDataValues[i].typeOpt, oneDataValues[i].strike)

            exDate = today + timeToDays(oneDataValues[i].t)
            exercise = AmericanExercise(today, exDate)

            spot1.setValue(oneDataValues[i].s)
            vol1.setValue(oneDataValues[i].v)
            rRate.setValue(oneDataValues[i].r)
            qRate.setValue(oneDataValues[i].q)

            basketOption = BasketOption(
                basketTypeToPayoff(BasketType.MaxBasket, payoff),
                exercise)
            basketOption.setPricingEngine(mcLSMCEngine)

            calculated = basketOption.NPV()
            expected = oneDataValues[i].result
            # errorEstimate = basketOption.errorEstimate()
            relError = relativeError(calculated, expected, oneDataValues[i].s)
            # error = abs(calculated-expected)

            self.assertFalse(relError > oneDataValues[i].tol)

    def testOddSamples(self):
        # This unit test is a a regression test to check for a crash in
        # monte carlo if the required sample is odd.  The crash occurred
        # because the samples array size was off by one when antithetic
        # paths were added.

        TEST_MESSAGE("Testing antithetic engine using odd sample number...")

        requiredSamples = 10001  # The important line
        timeSteps = 53
        values = [
            #        type, strike,   spot,    q,    r,    t,  vol,   value, tol
            BasketOptionOneData(Option.Put, 100.00, 80.00, 0.0, 0.06, 0.5, 0.4, 21.6059, 1e-2)
        ]

        dc = Actual360()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = today

        spot1 = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)

        rRate = SimpleQuote(0.05)
        rTS = flatRate(today, rRate, dc)

        vol1 = SimpleQuote(0.0)
        volTS1 = flatVol(today, vol1, dc)

        seed = 0

        stochProcess1 = BlackScholesMertonProcess(
            QuoteHandle(spot1),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS1))

        procs = [stochProcess1]

        correlation = Matrix(1, 1, 1.0)

        process = StochasticProcessArray(procs, correlation)

        mcLSMCEngine = MakeMCPRAmericanBasketEngine(process)
        mcLSMCEngine.withSteps(timeSteps)
        mcLSMCEngine.withAntitheticVariate()
        mcLSMCEngine.withSamples(requiredSamples)
        mcLSMCEngine.withCalibrationSamples(int(requiredSamples / 4))
        mcLSMCEngine.withSeed(seed)
        mcLSMCEngine = mcLSMCEngine.makeEngine()

        for value in values:
            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)

            exDate = today + timeToDays(value.t)
            exercise = AmericanExercise(today, exDate)

            spot1.setValue(value.s)
            vol1.setValue(value.v)
            rRate.setValue(value.r)
            qRate.setValue(value.q)

            basketOption = BasketOption(
                basketTypeToPayoff(BasketType.MaxBasket, payoff),
                exercise)
            basketOption.setPricingEngine(mcLSMCEngine)

            calculated = basketOption.NPV()
            expected = value.result
            # errorEstimate = basketOption.errorEstimate()
            relError = relativeError(calculated, expected, value.s)
            # error = abs(calculated-expected)

            self.assertFalse(relError > value.tol)

    def testLocalVolatilitySpreadOption(self):
        TEST_MESSAGE("Testing 2D local-volatility spread-option pricing...")

        dc = Actual360()
        today = Date(21, September, 2017)
        Settings.instance().evaluationDate = today
        maturity = today + Period(3, Months)

        riskFreeRate = YieldTermStructureHandle(flatRate(today, 0.07, dc))
        dividendYield = YieldTermStructureHandle(flatRate(today, 0.03, dc))

        s1 = QuoteHandle(SimpleQuote(100))
        s2 = QuoteHandle(SimpleQuote(110))

        hm1 = HestonModel(
            HestonProcess(
                riskFreeRate, dividendYield,
                s1, 0.09, 1.0, 0.06, 0.6, -0.75))
        hm2 = HestonModel(
            HestonProcess(
                riskFreeRate, dividendYield,
                s2, 0.1, 2.0, 0.07, 0.8, 0.85))

        vol1 = BlackVolTermStructureHandle(
            HestonBlackVolSurface(HestonModelHandle(hm1)))
        vol2 = BlackVolTermStructureHandle(
            HestonBlackVolSurface(HestonModelHandle(hm2)))

        basketOption = BasketOption(
            basketTypeToPayoff(
                BasketType.SpreadBasket,
                PlainVanillaPayoff(
                    Option.Call, s2.value() - s1.value())),
            EuropeanExercise(maturity))

        rho = -0.6

        bs2 = GeneralizedBlackScholesProcess(
            s2, dividendYield, riskFreeRate, vol2)
        bs1 = GeneralizedBlackScholesProcess(
            s1, dividendYield, riskFreeRate, vol1)

        basketOption.setPricingEngine(
            Fd2dBlackScholesVanillaEngine(
                bs1, bs2, rho, 11, 11, 6, 0,
                FdmSchemeDesc.Hundsdorfer(),
                True, 0.25))

        tolerance = 0.01
        expected = 2.561
        calculated = basketOption.NPV()

        self.assertFalse(abs(expected - calculated) > tolerance)

    def test2DPDEGreeks(self):
        TEST_MESSAGE("Testing Greeks of two-dimensional PDE engine...")

        s1 = 100
        s2 = 100
        r = 0.013
        v = 0.2
        rho = 0.5
        strike = s1 - s2
        maturityInDays = 1095

        dc = Actual365Fixed()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = today
        maturity = today + Period(maturityInDays, Days)

        spot1 = SimpleQuote(s1)
        spot2 = SimpleQuote(s2)

        rTS = YieldTermStructureHandle(flatRate(today, r, dc))
        vTS = BlackVolTermStructureHandle(flatVol(today, v, dc))

        p1 = BlackProcess(QuoteHandle(spot1), rTS, vTS)
        p2 = BlackProcess(QuoteHandle(spot2), rTS, vTS)

        option = BasketOption(
            SpreadBasketPayoff(
                PlainVanillaPayoff(Option.Call, strike)),
            EuropeanExercise(maturity))

        option.setPricingEngine(Fd2dBlackScholesVanillaEngine(p1, p2, rho))

        calculatedDelta = option.delta()
        calculatedGamma = option.gamma()

        option.setPricingEngine(KirkEngine(p1, p2, rho))

        eps = 1.0
        npv = option.NPV()

        spot1.setValue(s1 + eps)
        spot2.setValue(s2 + eps)
        npvUp = option.NPV()

        spot1.setValue(s1 - eps)
        spot2.setValue(s2 - eps)
        npvDown = option.NPV()

        expectedDelta = (npvUp - npvDown) / (2 * eps)
        expectedGamma = (npvUp + npvDown - 2 * npv) / (eps * eps)

        tol = 0.0005
        self.assertFalse(abs(expectedDelta - calculatedDelta) > tol)

        self.assertFalse(abs(expectedGamma - calculatedGamma) > tol)
