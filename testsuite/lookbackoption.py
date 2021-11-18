import unittest
from utilities import *
from QuantLib import *


class LookbackOptionData(object):
    def __init__(self,
                 typeOpt,
                 strike,
                 minmax,
                 s,
                 q,
                 r,
                 t,
                 v,
                 l,
                 t1,
                 result,
                 tol):
        self.typeOpt = typeOpt
        self.strike = strike
        self.minmax = minmax
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        # Partial-time lookback options:
        self.l = l  # level above/below actual extremum
        self.t1 = t1  # time to start of lookback period
        self.result = result  # result
        self.tol = tol  # tolerance


class LookbackOptionTest(unittest.TestCase):
    def testAnalyticContinuousFloatingLookback(self):
        TEST_MESSAGE(
            "Testing analytic continuous floating-strike lookback options...")

        values = [
            # // data from "Option Pricing Formulas", Haug, 1998, pg.61-62
            # // type,             strike, minmax, s,     q,    r,    t,    v,    l, t1, result,  tol
            LookbackOptionData(Option.Call, 0, 100, 120.0, 0.06, 0.10, 0.50, 0.30, 0, 0, 25.3533, 1.0e-4),
            # // data from "Connecting discrete and continuous path-dependent options",
            # // Broadie, Glasserman & Kou, 1999, pg.70-74
            # // type,             strike, minmax, s,     q,    r,    t,    v,    l, t1, result,  tol
            LookbackOptionData(Option.Call, 0, 100, 100.0, 0.00, 0.05, 1.00, 0.30, 0, 0, 23.7884, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 100, 100.0, 0.00, 0.05, 0.20, 0.30, 0, 0, 10.7190, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 100, 110.0, 0.00, 0.05, 0.20, 0.30, 0, 0, 14.4597, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 100, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 15.3526, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 16.8468, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 120, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 21.0645, 1.0e-4),
        ]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        for value in values:
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            payoff = FloatingTypePayoff(value.typeOpt)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = AnalyticContinuousFloatingLookbackEngine(stochProcess)

            option = ContinuousFloatingLookbackOption(value.minmax, payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

    def testAnalyticContinuousFixedLookback(self):
        TEST_MESSAGE(
            "Testing analytic continuous fixed-strike lookback options...")

        values = [
            # // data from "Option Pricing Formulas", Haug, 1998, pg.63-64
            # //type,            strike, minmax,  s,     q,    r,    t,    v,    l, t1, result,  tol
            LookbackOptionData(Option.Call, 95, 100, 100.0, 0.00, 0.10, 0.50, 0.10, 0, 0, 13.2687, 1.0e-4),
            LookbackOptionData(Option.Call, 95, 100, 100.0, 0.00, 0.10, 0.50, 0.20, 0, 0, 18.9263, 1.0e-4),
            LookbackOptionData(Option.Call, 95, 100, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 24.9857, 1.0e-4),
            LookbackOptionData(Option.Call, 100, 100, 100.0, 0.00, 0.10, 0.50, 0.10, 0, 0, 8.5126, 1.0e-4),
            LookbackOptionData(Option.Call, 100, 100, 100.0, 0.00, 0.10, 0.50, 0.20, 0, 0, 14.1702, 1.0e-4),
            LookbackOptionData(Option.Call, 100, 100, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 20.2296, 1.0e-4),
            LookbackOptionData(Option.Call, 105, 100, 100.0, 0.00, 0.10, 0.50, 0.10, 0, 0, 4.3908, 1.0e-4),
            LookbackOptionData(Option.Call, 105, 100, 100.0, 0.00, 0.10, 0.50, 0.20, 0, 0, 9.8905, 1.0e-4),
            LookbackOptionData(Option.Call, 105, 100, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 15.8512, 1.0e-4),
            LookbackOptionData(Option.Call, 95, 100, 100.0, 0.00, 0.10, 1.00, 0.10, 0, 0, 18.3241, 1.0e-4),
            LookbackOptionData(Option.Call, 95, 100, 100.0, 0.00, 0.10, 1.00, 0.20, 0, 0, 26.0731, 1.0e-4),
            LookbackOptionData(Option.Call, 95, 100, 100.0, 0.00, 0.10, 1.00, 0.30, 0, 0, 34.7116, 1.0e-4),
            LookbackOptionData(Option.Call, 100, 100, 100.0, 0.00, 0.10, 1.00, 0.10, 0, 0, 13.8000, 1.0e-4),
            LookbackOptionData(Option.Call, 100, 100, 100.0, 0.00, 0.10, 1.00, 0.20, 0, 0, 21.5489, 1.0e-4),
            LookbackOptionData(Option.Call, 100, 100, 100.0, 0.00, 0.10, 1.00, 0.30, 0, 0, 30.1874, 1.0e-4),
            LookbackOptionData(Option.Call, 105, 100, 100.0, 0.00, 0.10, 1.00, 0.10, 0, 0, 9.5445, 1.0e-4),
            LookbackOptionData(Option.Call, 105, 100, 100.0, 0.00, 0.10, 1.00, 0.20, 0, 0, 17.2965, 1.0e-4),
            LookbackOptionData(Option.Call, 105, 100, 100.0, 0.00, 0.10, 1.00, 0.30, 0, 0, 25.9002, 1.0e-4),
            LookbackOptionData(Option.Put, 95, 100, 100.0, 0.00, 0.10, 0.50, 0.10, 0, 0, 0.6899, 1.0e-4),
            LookbackOptionData(Option.Put, 95, 100, 100.0, 0.00, 0.10, 0.50, 0.20, 0, 0, 4.4448, 1.0e-4),
            LookbackOptionData(Option.Put, 95, 100, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 8.9213, 1.0e-4),
            LookbackOptionData(Option.Put, 100, 100, 100.0, 0.00, 0.10, 0.50, 0.10, 0, 0, 3.3917, 1.0e-4),
            LookbackOptionData(Option.Put, 100, 100, 100.0, 0.00, 0.10, 0.50, 0.20, 0, 0, 8.3177, 1.0e-4),
            LookbackOptionData(Option.Put, 100, 100, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 13.1579, 1.0e-4),
            LookbackOptionData(Option.Put, 105, 100, 100.0, 0.00, 0.10, 0.50, 0.10, 0, 0, 8.1478, 1.0e-4),
            LookbackOptionData(Option.Put, 105, 100, 100.0, 0.00, 0.10, 0.50, 0.20, 0, 0, 13.0739, 1.0e-4),
            LookbackOptionData(Option.Put, 105, 100, 100.0, 0.00, 0.10, 0.50, 0.30, 0, 0, 17.9140, 1.0e-4),
            LookbackOptionData(Option.Put, 95, 100, 100.0, 0.00, 0.10, 1.00, 0.10, 0, 0, 1.0534, 1.0e-4),
            LookbackOptionData(Option.Put, 95, 100, 100.0, 0.00, 0.10, 1.00, 0.20, 0, 0, 6.2813, 1.0e-4),
            LookbackOptionData(Option.Put, 95, 100, 100.0, 0.00, 0.10, 1.00, 0.30, 0, 0, 12.2376, 1.0e-4),
            LookbackOptionData(Option.Put, 100, 100, 100.0, 0.00, 0.10, 1.00, 0.10, 0, 0, 3.8079, 1.0e-4),
            LookbackOptionData(Option.Put, 100, 100, 100.0, 0.00, 0.10, 1.00, 0.20, 0, 0, 10.1294, 1.0e-4),
            LookbackOptionData(Option.Put, 100, 100, 100.0, 0.00, 0.10, 1.00, 0.30, 0, 0, 16.3889, 1.0e-4),
            LookbackOptionData(Option.Put, 105, 100, 100.0, 0.00, 0.10, 1.00, 0.10, 0, 0, 8.3321, 1.0e-4),
            LookbackOptionData(Option.Put, 105, 100, 100.0, 0.00, 0.10, 1.00, 0.20, 0, 0, 14.6536, 1.0e-4),
            LookbackOptionData(Option.Put, 105, 100, 100.0, 0.00, 0.10, 1.00, 0.30, 0, 0, 20.9130, 1.0e-4)
        ]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        for value in values:
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = AnalyticContinuousFixedLookbackEngine(stochProcess)

            option = ContinuousFixedLookbackOption(value.minmax, payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

    def testAnalyticContinuousPartialFloatingLookback(self):
        TEST_MESSAGE(
            "Testing analytic continuous partial floating-strike lookback options...")

        values = [
            # // data from "Option Pricing Formulas, Second Edition", Haug, 2006, pg.146
            # //type,         strike, minmax, s,    q,    r,    t,    v,    l,  t1,     result,   tol
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.1, 1, 0.25, 8.6524, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.1, 1, 0.5, 9.2128, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.1, 1, 0.75, 9.5567, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.1, 1, 0.25, 10.5751, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.1, 1, 0.5, 11.2601, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.1, 1, 0.75, 11.6804, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.2, 1, 0.25, 13.3402, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.2, 1, 0.5, 14.5121, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.2, 1, 0.75, 15.314, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.2, 1, 0.25, 16.3047, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.2, 1, 0.5, 17.737, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.2, 1, 0.75, 18.7171, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.3, 1, 0.25, 17.9831, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.3, 1, 0.5, 19.6618, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 90, 90, 0, 0.06, 1, 0.3, 1, 0.75, 20.8493, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.3, 1, 0.25, 21.9793, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.3, 1, 0.5, 24.0311, 1.0e-4),
            LookbackOptionData(Option.Call, 0, 110, 110, 0, 0.06, 1, 0.3, 1, 0.75, 25.4825, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.1, 1, 0.25, 2.7189, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.1, 1, 0.5, 3.4639, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.1, 1, 0.75, 4.1912, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.1, 1, 0.25, 3.3231, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.1, 1, 0.5, 4.2336, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.1, 1, 0.75, 5.1226, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.2, 1, 0.25, 7.9153, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.2, 1, 0.5, 9.5825, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.2, 1, 0.75, 11.0362, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.2, 1, 0.25, 9.6743, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.2, 1, 0.5, 11.7119, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.2, 1, 0.75, 13.4887, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.3, 1, 0.25, 13.4719, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.3, 1, 0.5, 16.1495, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 90, 90, 0, 0.06, 1, 0.3, 1, 0.75, 18.4071, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.3, 1, 0.25, 16.4657, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.3, 1, 0.5, 19.7383, 1.0e-4),
            LookbackOptionData(Option.Put, 0, 110, 110, 0, 0.06, 1, 0.3, 1, 0.75, 22.4976, 1.0e-4)
        ]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        for value in values:
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            payoff = FloatingTypePayoff(value.typeOpt)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = AnalyticContinuousPartialFloatingLookbackEngine(stochProcess)

            lookbackEnd = today + timeToDays(value.t1)
            option = ContinuousPartialFloatingLookbackOption(
                value.minmax, value.l, lookbackEnd, payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

    def testAnalyticContinuousPartialFixedLookback(self):
        TEST_MESSAGE(
            "Testing analytic continuous fixed-strike lookback options...")

        values = [
            # // data from "Option Pricing Formulas, Second Edition", Haug, 2006, pg.148
            # //type,         strike, minmax, s,    q,    r,    t,    v, l,   t1,  result,   tol
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.1, 0, 0.25, 20.2845, 1.0e-4),
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.1, 0, 0.5, 19.6239, 1.0e-4),
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.1, 0, 0.75, 18.6244, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.1, 0, 0.25, 4.0432, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.1, 0, 0.5, 3.958, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.1, 0, 0.75, 3.7015, 1.0e-4),
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.2, 0, 0.25, 27.5385, 1.0e-4),
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.2, 0, 0.5, 25.8126, 1.0e-4),
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.2, 0, 0.75, 23.4957, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.2, 0, 0.25, 11.4895, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.2, 0, 0.5, 10.8995, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.2, 0, 0.75, 9.8244, 1.0e-4),
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.3, 0, 0.25, 35.4578, 1.0e-4),
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.3, 0, 0.5, 32.7172, 1.0e-4),
            LookbackOptionData(Option.Call, 90, 0, 100, 0, 0.06, 1, 0.3, 0, 0.75, 29.1473, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.3, 0, 0.25, 19.725, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.3, 0, 0.5, 18.4025, 1.0e-4),
            LookbackOptionData(Option.Call, 110, 0, 100, 0, 0.06, 1, 0.3, 0, 0.75, 16.2976, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.1, 0, 0.25, 0.4973, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.1, 0, 0.5, 0.4632, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.1, 0, 0.75, 0.3863, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.1, 0, 0.25, 12.6978, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.1, 0, 0.5, 10.9492, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.1, 0, 0.75, 9.1555, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.2, 0, 0.25, 4.5863, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.2, 0, 0.5, 4.1925, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.2, 0, 0.75, 3.5831, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.2, 0, 0.25, 19.0255, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.2, 0, 0.5, 16.9433, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.2, 0, 0.75, 14.6505, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.3, 0, 0.25, 9.9348, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.3, 0, 0.5, 9.1111, 1.0e-4),
            LookbackOptionData(Option.Put, 90, 0, 100, 0, 0.06, 1, 0.3, 0, 0.75, 7.9267, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.3, 0, 0.25, 25.2112, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.3, 0, 0.5, 22.8217, 1.0e-4),
            LookbackOptionData(Option.Put, 110, 0, 100, 0, 0.06, 1, 0.3, 0, 0.75, 20.0566, 1.0e-4)
        ]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        for value in values:
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = AnalyticContinuousPartialFixedLookbackEngine(stochProcess)

            lookbackStart = today + timeToDays(value.t1)
            option = ContinuousPartialFixedLookbackOption(
                lookbackStart,
                payoff,
                exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

    def testMonteCarloLookback(self):
        TEST_MESSAGE("Testing Monte Carlo engines for lookback options...")

        tolerance = 0.1

        dc = Actual360()
        today = Date.todaysDate()

        strike = 90
        t = 1
        t1 = 0.25

        exDate = today + timeToDays(t)
        exercise = EuropeanExercise(exDate)

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        spot.setValue(100)
        qRate.setValue(0)
        rRate.setValue(0.06)
        vol.setValue(0.1)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))

        types = [Option.Call, Option.Put]

        for ty in types:
            payoff = PlainVanillaPayoff(ty, strike)

            # /**
            # * Partial Fixed
            # * **/

            lookbackStart = today + timeToDays(t1)
            partialFixedLookback = ContinuousPartialFixedLookbackOption(
                lookbackStart,
                payoff,
                exercise)
            engine = AnalyticContinuousPartialFixedLookbackEngine(stochProcess)
            partialFixedLookback.setPricingEngine(engine)

            analytical = partialFixedLookback.NPV()

            mcpartialfixedengine = MakeMCPRPartialFixedLookbackEngine(stochProcess)
            mcpartialfixedengine.withSteps(2000)
            mcpartialfixedengine.withAntitheticVariate()
            mcpartialfixedengine.withSeed(1)
            mcpartialfixedengine.withAbsoluteTolerance(tolerance)
            mcpartialfixedengine = mcpartialfixedengine.makeEngine()

            partialFixedLookback.setPricingEngine(mcpartialfixedengine)
            monteCarlo = partialFixedLookback.NPV()

            diff = abs(analytical - monteCarlo)

            self.assertFalse(diff > tolerance)

            # /**
            # * Fixed
            # * **/

            minMax = 100

            fixedLookback = ContinuousFixedLookbackOption(
                minMax,
                payoff,
                exercise)
            analyticalfixedengine = AnalyticContinuousFixedLookbackEngine(stochProcess)
            fixedLookback.setPricingEngine(analyticalfixedengine)

            analytical = fixedLookback.NPV()

            mcfixedengine = MakeMCPRFixedLookbackEngine(stochProcess)
            mcfixedengine.withSteps(2000)
            mcfixedengine.withAntitheticVariate()
            mcfixedengine.withSeed(1)
            mcfixedengine.withAbsoluteTolerance(tolerance)
            mcfixedengine = mcfixedengine.makeEngine()

            fixedLookback.setPricingEngine(mcfixedengine)
            monteCarlo = fixedLookback.NPV()

            diff = abs(analytical - monteCarlo)

            self.assertFalse(diff > tolerance)

            # /**
            # * Partial Floating
            # * **/

            lmd = 1
            lookbackEnd = today + timeToDays(t1)

            floatingPayoff = FloatingTypePayoff(ty)

            partialFloating = ContinuousPartialFloatingLookbackOption(
                minMax,
                lmd,
                lookbackEnd,
                floatingPayoff,
                exercise)
            analyticalpartialFloatingengine = AnalyticContinuousPartialFloatingLookbackEngine(stochProcess)
            partialFloating.setPricingEngine(analyticalpartialFloatingengine)

            analytical = partialFloating.NPV()

            mcpartialfloatingengine = MakeMCPRPartialFloatingLookbackEngine(stochProcess)
            mcpartialfloatingengine.withSteps(2000)
            mcpartialfloatingengine.withAntitheticVariate()
            mcpartialfloatingengine.withSeed(1)
            mcpartialfloatingengine.withAbsoluteTolerance(tolerance)
            mcpartialfloatingengine = mcpartialfloatingengine.makeEngine()

            partialFloating.setPricingEngine(mcpartialfloatingengine)
            monteCarlo = partialFloating.NPV()

            diff = abs(analytical - monteCarlo)

            self.assertFalse(diff > tolerance)

            # /**
            # * Floating
            # * **/

            floating = ContinuousFloatingLookbackOption(
                minMax,
                floatingPayoff,
                exercise)
            analyticalFloatingengine = AnalyticContinuousFloatingLookbackEngine(stochProcess)
            floating.setPricingEngine(analyticalFloatingengine)

            analytical = floating.NPV()

            mcfloatingengine = MakeMCPRFloatingLookbackEngine(stochProcess)
            mcfloatingengine.withSteps(2000)
            mcfloatingengine.withAntitheticVariate()
            mcfloatingengine.withSeed(1)
            mcfloatingengine.withAbsoluteTolerance(tolerance)
            mcfloatingengine = mcfloatingengine.makeEngine()

            floating.setPricingEngine(mcfloatingengine)
            monteCarlo = floating.NPV()

            diff = abs(analytical - monteCarlo)

            self.assertFalse(diff > tolerance)
