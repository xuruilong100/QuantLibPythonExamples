import unittest

import numpy as np
from QuantLib import *

from utilities import *


class EngineType(object):
    Analytic = "Analytic"
    JR = "JR"
    CRR = "CRR"
    EQP = "EQP"
    TGEO = "TGEO"
    TIAN = "TIAN"
    LR = "LR"
    JOSHI = "JOSHI"
    FiniteDifferences = "FiniteDifferences"
    Integral = "Integral"
    PseudoMonteCarlo = "PseudoMonteCarlo"
    QuasiMonteCarlo = "QuasiMonteCarlo"
    FFT = "FFT"


def makeProcess(u,
                q,
                r,
                vol):
    return BlackScholesMertonProcess(
        QuoteHandle(u),
        YieldTermStructureHandle(q),
        YieldTermStructureHandle(r),
        BlackVolTermStructureHandle(vol))


def makeOption(payoff,
               exercise,
               u,
               q,
               r,
               vol,
               engineType,
               binomialSteps,
               samples):
    stochProcess = makeProcess(u, q, r, vol)

    engine = None

    if engineType == "Analytic":
        engine = AnalyticEuropeanEngine(stochProcess)
    elif engineType == "JR":
        engine = BinomialJRVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == "CRR":
        engine = BinomialCRRVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == "EQP":
        engine = BinomialEQPVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == "TGEO":
        engine = BinomialTrigeorgisVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == "TIAN":
        engine = BinomialTianVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == "LR":
        engine = BinomialLRVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == "JOSHI":
        engine = BinomialJ4VanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == "FiniteDifferences":
        engine = FdBlackScholesVanillaEngine(
            stochProcess, binomialSteps, samples)
    elif engineType == "Integral":
        engine = IntegralEngine(stochProcess)
    elif engineType == "PseudoMonteCarlo":
        engine = MakeMCPREuropeanEngine(stochProcess)
        engine.withSteps(1)
        engine.withSamples(samples)
        engine.withSeed(42)
        engine = engine.makeEngine()
    elif engineType == "QuasiMonteCarlo":
        engine = MakeMCLDEuropeanEngine(stochProcess)
        engine.withSteps(1)
        engine.withSamples(samples)
        engine = engine.makeEngine()
    elif engineType == "FFT":
        engine = FFTVanillaEngine(stochProcess)

    option = EuropeanOption(payoff, exercise)
    option.setPricingEngine(engine)

    return option


class EuropeanOptionData(object):
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
        self.s = s
        self.q = q
        self.r = r
        self.t = t
        self.v = v
        self.result = result
        self.tol = tol


class EuropeanOptionTest(unittest.TestCase):

    def testValues(self):
        TEST_MESSAGE(
            "Testing European option values...")
        backup = SavedSettings()

        values = [
            EuropeanOptionData(Option.Call, 65.00, 60.00, 0.00, 0.08, 0.25, 0.30, 2.1334, 1.0e-4),
            EuropeanOptionData(Option.Put, 95.00, 100.00, 0.05, 0.10, 0.50, 0.20, 2.4648, 1.0e-4),
            EuropeanOptionData(Option.Put, 19.00, 19.00, 0.10, 0.10, 0.75, 0.28, 1.7011, 1.0e-4),
            EuropeanOptionData(Option.Call, 19.00, 19.00, 0.10, 0.10, 0.75, 0.28, 1.7011, 1.0e-4),
            EuropeanOptionData(Option.Call, 1.60, 1.56, 0.08, 0.06, 0.50, 0.12, 0.0291, 1.0e-4),
            EuropeanOptionData(Option.Put, 70.00, 75.00, 0.05, 0.10, 0.50, 0.35, 4.0870, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.15, 0.0205, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.15, 1.8734, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.15, 9.9413, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.25, 0.3150, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.25, 3.1217, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.25, 10.3556, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.35, 0.9474, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.35, 4.3693, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.35, 11.1381, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.15, 0.8069, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.15, 4.0232, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.15, 10.5769, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.25, 2.7026, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.25, 6.6997, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.25, 12.7857, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.35, 4.9329, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.35, 9.3679, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.35, 15.3086, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.15, 9.9210, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.15, 1.8734, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.15, 0.0408, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.25, 10.2155, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.25, 3.1217, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.25, 0.4551, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.35, 10.8479, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.35, 4.3693, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.35, 1.2376, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.15, 10.3192, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.15, 4.0232, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.15, 1.0646, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.25, 12.2149, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.25, 6.6997, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.25, 3.2734, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.35, 14.4452, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.35, 9.3679, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.35, 5.7963, 1.0e-4),
            EuropeanOptionData(Option.Call, 40.00, 42.00, 0.08, 0.04, 0.75, 0.35, 5.0975, 1.0e-4)]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        for value in values:
            payoff = PlainVanillaPayoff(
                value.typeOpt, value.strike)
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = AnalyticEuropeanEngine(stochProcess)

            option = EuropeanOption(payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = value.tol

            self.assertFalse(error > tolerance)

            engine = FdBlackScholesVanillaEngine(stochProcess, 200, 400)
            option.setPricingEngine(engine)
            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = 1.0e-3

            self.assertFalse(error > tolerance)

    def testGreekValues(self):
        TEST_MESSAGE(
            "Testing European option greek values...")
        backup = SavedSettings()

        values = [
            EuropeanOptionData(Option.Call, 100.00, 105.00, 0.10, 0.10, 0.500000, 0.36, 0.5946, 0),
            EuropeanOptionData(Option.Put, 100.00, 105.00, 0.10, 0.10, 0.500000, 0.36, -0.3566, 0),
            EuropeanOptionData(Option.Put, 100.00, 105.00, 0.10, 0.10, 0.500000, 0.36, -4.8775, 0),
            EuropeanOptionData(Option.Call, 60.00, 55.00, 0.00, 0.10, 0.750000, 0.30, 0.0278, 0),
            EuropeanOptionData(Option.Put, 60.00, 55.00, 0.00, 0.10, 0.750000, 0.30, 0.0278, 0),
            EuropeanOptionData(Option.Call, 60.00, 55.00, 0.00, 0.10, 0.750000, 0.30, 18.9358, 0),
            EuropeanOptionData(Option.Put, 60.00, 55.00, 0.00, 0.10, 0.750000, 0.30, 18.9358, 0),
            EuropeanOptionData(Option.Put, 405.00, 430.00, 0.05, 0.07, 1.0 / 12.0, 0.20, -31.1924, 0),
            EuropeanOptionData(Option.Put, 405.00, 430.00, 0.05, 0.07, 1.0 / 12.0, 0.20, -0.0855, 0),
            EuropeanOptionData(Option.Call, 75.00, 72.00, 0.00, 0.09, 1.000000, 0.19, 38.7325, 0),
            EuropeanOptionData(Option.Put, 490.00, 500.00, 0.05, 0.08, 0.250000, 0.15, 42.2254, 0)]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        engine = AnalyticEuropeanEngine(stochProcess)

        i = -1

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.delta()
        error = abs(calculated - values[i].result)
        tolerance = 1e-4
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.delta()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.elasticity()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.gamma()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.gamma()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.vega()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.vega()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.theta()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.thetaPerDay()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.rho()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

        i += 1
        payoff = PlainVanillaPayoff(values[i].typeOpt, values[i].strike)
        exDate = today + timeToDays(values[i].t)
        exercise = EuropeanExercise(exDate)
        spot.setValue(values[i].s)
        qRate.setValue(values[i].q)
        rRate.setValue(values[i].r)
        vol.setValue(values[i].v)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.dividendRho()
        error = abs(calculated - values[i].result)
        self.assertFalse(error > tolerance)

    def testGreeks(self):
        TEST_MESSAGE(
            "Testing analytic European option greeks...")
        backup = SavedSettings()

        calculated = dict()
        expected = dict()
        tolerance = dict()

        tolerance["delta"] = 1.0e-5
        tolerance["gamma"] = 1.0e-5
        tolerance["theta"] = 1.0e-5
        tolerance["rho"] = 1.0e-5
        tolerance["divRho"] = 1.0e-5
        tolerance["vega"] = 1.0e-5

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.04, 0.05, 0.06]
        rRates = [0.01, 0.05, 0.15]
        residualTimes = [1.0, 2.0]
        vols = [0.11, 0.50, 1.20]

        dc = Actual360()
        today = knownGoodDefault
        Settings.instance().evaluationDate = today

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(vol, dc))

        for ty in types:
            for strike in strikes:
                for residualTime in residualTimes:
                    exDate = today + timeToDays(residualTime)
                    exercise = EuropeanExercise(exDate)
                    payoff = None
                    for kk in range(4):

                        if kk == 0:
                            payoff = PlainVanillaPayoff(ty, strike)
                        elif kk == 1:
                            payoff = CashOrNothingPayoff(ty, strike, 100.0)
                        elif kk == 2:
                            payoff = AssetOrNothingPayoff(ty, strike)
                        elif kk == 3:
                            payoff = GapPayoff(ty, strike, 100.0)

                        stochProcess = BlackScholesMertonProcess(
                            QuoteHandle(spot), qTS, rTS, volTS)

                        engine = AnalyticEuropeanEngine(stochProcess)

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

                                            du = u * 1.0e-4
                                            spot.setValue(u + du)
                                            value_p = option.NPV()
                                            delta_p = option.delta()
                                            spot.setValue(u - du)
                                            value_m = option.NPV()
                                            delta_m = option.delta()
                                            spot.setValue(u)
                                            expected["delta"] = (value_p - value_m) / (2 * du)
                                            expected["gamma"] = (delta_p - delta_m) / (2 * du)

                                            dr = r * 1.0e-4
                                            rRate.setValue(r + dr)
                                            value_p = option.NPV()
                                            rRate.setValue(r - dr)
                                            value_m = option.NPV()
                                            rRate.setValue(r)
                                            expected["rho"] = (value_p - value_m) / (2 * dr)

                                            dq = q * 1.0e-4
                                            qRate.setValue(q + dq)
                                            value_p = option.NPV()
                                            qRate.setValue(q - dq)
                                            value_m = option.NPV()
                                            qRate.setValue(q)
                                            expected["divRho"] = (value_p - value_m) / (2 * dq)

                                            dv = v * 1.0e-4
                                            vol.setValue(v + dv)
                                            value_p = option.NPV()
                                            vol.setValue(v - dv)
                                            value_m = option.NPV()
                                            vol.setValue(v)
                                            expected["vega"] = (value_p - value_m) / (2 * dv)

                                            dT = dc.yearFraction(today - 1, today + 1)
                                            Settings.instance().evaluationDate = today - 1
                                            value_m = option.NPV()
                                            Settings.instance().evaluationDate = today + 1
                                            value_p = option.NPV()
                                            Settings.instance().evaluationDate = today
                                            expected["theta"] = (value_p - value_m) / dT

                                            for greek in calculated.keys():
                                                expct = expected[greek]
                                                calcl = calculated[greek]
                                                tol = tolerance[greek]
                                                error = relativeError(expct, calcl, u)

                                                self.assertFalse(error > tol)

    def testImpliedVol(self):
        TEST_MESSAGE(
            "Testing European option implied volatility...")
        backup = SavedSettings()

        maxEvaluations = 100
        tolerance = 1.0e-6

        types = [Option.Call, Option.Put]
        strikes = [90.0, 99.5, 100.0, 100.5, 110.0]
        lengths = [36, 180, 360, 1080]

        underlyings = [90.0, 95.0, 99.9, 100.0, 100.1, 105.0, 110.0]
        qRates = [0.01, 0.05, 0.10]
        rRates = [0.01, 0.05, 0.10]
        vols = [0.01, 0.20, 0.30, 0.70, 0.90]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        for ty in types:
            for strike in strikes:
                for length in lengths:

                    exDate = today + Period(length, Days)
                    exercise = EuropeanExercise(exDate)
                    payoff = PlainVanillaPayoff(ty, strike)
                    option = makeOption(
                        payoff, exercise, spot, qTS, rTS, volTS,
                        EngineType.Analytic, NullSize(), NullSize())
                    process = makeProcess(spot, qTS, rTS, volTS)

                    for u in underlyings:
                        for q in qRates:
                            for r in rRates:
                                for v in vols:

                                    spot.setValue(u)
                                    qRate.setValue(q)
                                    rRate.setValue(r)
                                    vol.setValue(v)

                                    value = option.NPV()
                                    implVol = 0.0

                                    if value != 0.0:

                                        vol.setValue(v * 0.5)
                                        if abs(value - option.NPV()) <= 1.0e-12:
                                            continue
                                        try:
                                            implVol = option.impliedVolatility(
                                                value, process,
                                                tolerance, maxEvaluations)
                                        except Exception:
                                            self.fail("implied vol calculation failed.")

                                    if abs(implVol - v) > tolerance:
                                        vol.setValue(implVol)
                                        value2 = option.NPV()
                                        error = relativeError(value, value2, u)
                                        self.assertFalse(error > tolerance)

    def testImpliedVolContainment(self):
        TEST_MESSAGE(
            "Testing self-containment of implied volatility calculation...")
        backup = SavedSettings()

        maxEvaluations = 100
        tolerance = 1.0e-6

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(100.0)
        underlying = QuoteHandle(spot)
        qRate = SimpleQuote(0.05)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.03)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.20)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        exerciseDate = today + Period(1, Years)
        exercise = EuropeanExercise(exerciseDate)
        payoff = PlainVanillaPayoff(Option.Call, 100.0)
        process = BlackScholesMertonProcess(underlying, qTS, rTS, volTS)
        engine = AnalyticEuropeanEngine(process)

        option1 = EuropeanOption(payoff, exercise)
        option1.setPricingEngine(engine)
        option2 = EuropeanOption(payoff, exercise)
        option2.setPricingEngine(engine)

        refValue = option2.NPV()

        f = Flag()
        f.registerWith(option2)
        option1.impliedVolatility(
            refValue * 1.5, process,
            tolerance, maxEvaluations)

        self.assertFalse(f.isUp())

        option2.recalculate()

        self.assertFalse(
            abs(option2.NPV() - refValue) >= 1.0e-8)

        vol.setValue(vol.value() * 1.5)

        self.assertFalse(not f.isUp())
        self.assertFalse(
            abs(option2.NPV() - refValue) <= 1.0e-8)

    def testJRBinomialEngines(self):
        TEST_MESSAGE(
            "Testing JR binomial European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.JR
        steps = 251
        samples = NullSize()
        relativeTol = dict()
        relativeTol["value"] = 0.002
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(
            engine, steps, samples, relativeTol, True)

    def testCRRBinomialEngines(self):
        TEST_MESSAGE(
            "Testing CRR binomial European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.CRR
        steps = 501
        samples = NullSize()
        relativeTol = dict()
        relativeTol["value"] = 0.002
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(
            engine, steps, samples, relativeTol, True)

    def testEQPBinomialEngines(self):
        TEST_MESSAGE(
            "Testing EQP binomial European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.EQP
        steps = 501
        samples = NullSize()
        relativeTol = dict()
        relativeTol["value"] = 0.02
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(
            engine, steps, samples, relativeTol, True)

    def testTGEOBinomialEngines(self):
        TEST_MESSAGE(
            "Testing TGEO binomial European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.TGEO
        steps = 251
        samples = NullSize()
        relativeTol = dict()
        relativeTol["value"] = 0.002
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(
            engine, steps, samples, relativeTol, True)

    def testTIANBinomialEngines(self):
        TEST_MESSAGE(
            "Testing TIAN binomial European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.TIAN
        steps = 251
        samples = NullSize()
        relativeTol = dict()
        relativeTol["value"] = 0.002
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(
            engine, steps, samples, relativeTol, True)

    def testLRBinomialEngines(self):
        TEST_MESSAGE(
            "Testing LR binomial European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.LR
        steps = 251
        samples = NullSize()
        relativeTol = dict()
        relativeTol["value"] = 1.0e-6
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(
            engine, steps, samples, relativeTol, True)

    def testJOSHIBinomialEngines(self):
        TEST_MESSAGE(
            "Testing Joshi binomial European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.JOSHI
        steps = 251
        samples = NullSize()
        relativeTol = dict()
        relativeTol["value"] = 1.0e-7
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(
            engine, steps, samples, relativeTol, True)

    def testFdEngines(self):
        TEST_MESSAGE(
            "Testing finite-difference European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.FiniteDifferences
        timeSteps = 500
        gridPoints = 500
        relativeTol = dict()
        relativeTol["value"] = 1.0e-4
        relativeTol["delta"] = 1.0e-6
        relativeTol["gamma"] = 1.0e-6
        relativeTol["theta"] = 1.0e-3
        self._testEngineConsistency(
            engine, timeSteps, gridPoints, relativeTol, True)

    def testIntegralEngines(self):
        TEST_MESSAGE(
            "Testing integral engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.Integral
        timeSteps = 300
        gridPoints = 300
        relativeTol = dict()
        relativeTol["value"] = 0.0001
        self._testEngineConsistency(
            engine, timeSteps, gridPoints, relativeTol)

    def testQmcEngines(self):
        TEST_MESSAGE(
            "Testing Quasi Monte Carlo European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.QuasiMonteCarlo
        steps = NullSize()
        samples = 4095
        relativeTol = dict()
        relativeTol["value"] = 0.01
        self._testEngineConsistency(
            engine, steps, samples, relativeTol)

    def testMcEngines(self):
        TEST_MESSAGE(
            "Testing Monte Carlo European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.PseudoMonteCarlo
        steps = NullSize()
        samples = 40000
        relativeTol = dict()
        relativeTol["value"] = 0.01
        self._testEngineConsistency(
            engine, steps, samples, relativeTol)

    def testFFTEngines(self):
        TEST_MESSAGE(
            "Testing FFT European engines against analytic results...")

        backup = SavedSettings()

        engine = EngineType.FFT
        steps = NullSize()
        samples = NullSize()
        relativeTol = dict()
        relativeTol["value"] = 0.01
        self._testEngineConsistency(
            engine, steps, samples, relativeTol)

    def testLocalVolatility(self):
        TEST_MESSAGE(
            "Testing finite-differences with local volatility...")

        backup = SavedSettings()
        settlementDate = Date(5, July, 2002)
        Settings.instance().evaluationDate = settlementDate

        dayCounter = Actual365Fixed()
        calendar = TARGET()
        t = [13, 41, 75, 165, 256, 345, 524, 703]
        r = [0.0357, 0.0349, 0.0341, 0.0355,
             0.0359, 0.0368, 0.0386, 0.0401]

        rates = DoubleVector(1, 0.0357)
        dates = DateVector(1, settlementDate)

        for i in range(8):
            dates.push_back(settlementDate + Period(t[i], Days))
            rates.push_back(r[i])

        rTS = ZeroCurve(dates, rates, dayCounter)
        qTS = flatRate(settlementDate, 0.0, dayCounter)

        s0 = SimpleQuote(4500.00)

        tmp = [
            100, 500, 2000, 3400, 3600, 3800, 4000, 4200, 4400, 4500,
            4600, 4800, 5000, 5200, 5400, 5600, 7500, 10000, 20000, 30000]
        strikes = tmp

        v = [1.015873, 1.015873, 1.015873, 0.89729, 0.796493, 0.730914, 0.631335, 0.568895,
             0.711309, 0.711309, 0.711309, 0.641309, 0.635593, 0.583653, 0.508045, 0.463182,
             0.516034, 0.500534, 0.500534, 0.500534, 0.448706, 0.416661, 0.375470, 0.353442,
             0.516034, 0.482263, 0.447713, 0.387703, 0.355064, 0.337438, 0.316966, 0.306859,
             0.497587, 0.464373, 0.430764, 0.374052, 0.344336, 0.328607, 0.310619, 0.301865,
             0.479511, 0.446815, 0.414194, 0.361010, 0.334204, 0.320301, 0.304664, 0.297180,
             0.461866, 0.429645, 0.398092, 0.348638, 0.324680, 0.312512, 0.299082, 0.292785,
             0.444801, 0.413014, 0.382634, 0.337026, 0.315788, 0.305239, 0.293855, 0.288660,
             0.428604, 0.397219, 0.368109, 0.326282, 0.307555, 0.298483, 0.288972, 0.284791,
             0.420971, 0.389782, 0.361317, 0.321274, 0.303697, 0.295302, 0.286655, 0.282948,
             0.413749, 0.382754, 0.354917, 0.316532, 0.300016, 0.292251, 0.284420, 0.281164,
             0.400889, 0.370272, 0.343525, 0.307904, 0.293204, 0.286549, 0.280189, 0.277767,
             0.390685, 0.360399, 0.334344, 0.300507, 0.287149, 0.281380, 0.276271, 0.274588,
             0.383477, 0.353434, 0.327580, 0.294408, 0.281867, 0.276746, 0.272655, 0.271617,
             0.379106, 0.349214, 0.323160, 0.289618, 0.277362, 0.272641, 0.269332, 0.268846,
             0.377073, 0.347258, 0.320776, 0.286077, 0.273617, 0.269057, 0.266293, 0.266265,
             0.399925, 0.369232, 0.338895, 0.289042, 0.265509, 0.255589, 0.249308, 0.249665,
             0.423432, 0.406891, 0.373720, 0.314667, 0.281009, 0.263281, 0.246451, 0.242166,
             0.453704, 0.453704, 0.453704, 0.381255, 0.334578, 0.305527, 0.268909, 0.251367,
             0.517748, 0.517748, 0.517748, 0.416577, 0.364770, 0.331595, 0.287423, 0.264285]

        blackVolMatrix = Matrix(len(strikes), len(dates) - 1)

        for i in range(len(strikes)):
            for j in range(1, len(dates)):
                blackVolMatrix[i][j - 1] = v[i * (len(dates) - 1) + j - 1]

        volTS = BlackVarianceSurface(
            settlementDate, calendar,
            dates[1:],
            strikes, blackVolMatrix,
            dayCounter)

        volTS.setInterpolationBicubic()
        process = makeProcess(s0, qTS, rTS, volTS)

        schemeDescs = {
            "Douglas": FdmSchemeDesc.Douglas(),
            "Crank-Nicolson": FdmSchemeDesc.CrankNicolson(),
            "Mod. Craig-Sneyd": FdmSchemeDesc.ModifiedCraigSneyd()}

        for i in range(2, len(dates), 2):
            for j in range(3, len(dates) - 5, 5):
                exDate = dates[i]
                payoff = PlainVanillaPayoff(Option.Call, strikes[j])
                exercise = EuropeanExercise(exDate)
                option = EuropeanOption(payoff, exercise)
                option.setPricingEngine(
                    AnalyticEuropeanEngine(process))

                tol = 0.001
                expectedNPV = option.NPV()
                expectedDelta = option.delta()
                expectedGamma = option.gamma()

                option.setPricingEngine(
                    FdBlackScholesVanillaEngine(process, 200, 400))

                calculatedNPV = option.NPV()
                calculatedDelta = option.delta()
                calculatedGamma = option.gamma()

                self.assertFalse(abs(expectedNPV - calculatedNPV) > tol * expectedNPV)
                self.assertFalse(abs(expectedDelta - calculatedDelta) > tol * expectedDelta)
                self.assertFalse(abs(expectedGamma - calculatedGamma) > tol * expectedGamma)

                for k in schemeDescs.keys():
                    option.setPricingEngine(
                        FdBlackScholesVanillaEngine(
                            process, 25, 100, 0,
                            schemeDescs[k], True, 0.35))
                    calculatedNPV = option.NPV()
                    self.assertFalse(
                        abs(expectedNPV - calculatedNPV) > tol * expectedNPV)

    def testAnalyticEngineDiscountCurve(self):
        TEST_MESSAGE(
            "Testing separate discount curve for analytic European engine...")

        backup = SavedSettings()

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(1000.0)
        qRate = SimpleQuote(0.01)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.015)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.02)
        volTS = flatVol(today, vol, dc)
        discRate = SimpleQuote(0.015)
        discTS = flatRate(today, discRate, dc)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        engineSingleCurve = AnalyticEuropeanEngine(stochProcess)
        engineMultiCurve = AnalyticEuropeanEngine(
            stochProcess,
            YieldTermStructureHandle(discTS))
        payoff = PlainVanillaPayoff(Option.Call, 1025.0)
        exDate = today + Period(1, Years)
        exercise = EuropeanExercise(exDate)

        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(engineSingleCurve)
        npvSingleCurve = option.NPV()
        option.setPricingEngine(engineMultiCurve)
        npvMultiCurve = option.NPV()

        self.assertEqual(npvSingleCurve, npvMultiCurve)

        discRate.setValue(0.023)
        npvMultiCurve = option.NPV()
        self.assertNotEqual(npvSingleCurve, npvMultiCurve)

    def testPDESchemes(self):
        TEST_MESSAGE(
            "Testing different PDE schemes to solve Black-Scholes PDEs...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(18, February, 2018)

        spot = QuoteHandle(SimpleQuote(100.0))
        qTS = YieldTermStructureHandle(flatRate(today, 0.06, dc))
        rTS = YieldTermStructureHandle(flatRate(today, 0.1, dc))
        volTS = BlackVolTermStructureHandle(flatVol(today, 0.35, dc))

        maturity = today + Period(6, Months)

        process = BlackScholesMertonProcess(
            spot, qTS, rTS, volTS)

        analytic = AnalyticEuropeanEngine(process)

        douglas = FdBlackScholesVanillaEngine(
            process, 15, 100, 0, FdmSchemeDesc.Douglas())

        crankNicolson = FdBlackScholesVanillaEngine(
            process, 15, 100, 0, FdmSchemeDesc.CrankNicolson())

        implicitEuler = FdBlackScholesVanillaEngine(
            process, 500, 100, 0, FdmSchemeDesc.ImplicitEuler())

        explicitEuler = FdBlackScholesVanillaEngine(
            process, 1000, 100, 0, FdmSchemeDesc.ExplicitEuler())

        methodOfLines = FdBlackScholesVanillaEngine(
            process, 1, 100, 0, FdmSchemeDesc.MethodOfLines())

        hundsdorfer = FdBlackScholesVanillaEngine(
            process, 10, 100, 0, FdmSchemeDesc.Hundsdorfer())

        craigSneyd = FdBlackScholesVanillaEngine(
            process, 10, 100, 0, FdmSchemeDesc.CraigSneyd())

        modCraigSneyd = FdBlackScholesVanillaEngine(
            process, 15, 100, 0, FdmSchemeDesc.ModifiedCraigSneyd())

        trBDF2 = FdBlackScholesVanillaEngine(
            process, 15, 100, 0, FdmSchemeDesc.TrBDF2())

        engines = {
            "Douglas": douglas,
            "Crank-Nicolson": crankNicolson,
            "Implicit-Euler": implicitEuler,
            "Explicit-Euler": explicitEuler,
            "Method-of-Lines": methodOfLines,
            "Hundsdorfer": hundsdorfer,
            "Craig-Sneyd": craigSneyd,
            "Modified Craig-Sneyd": modCraigSneyd,
            "TR-BDF2": trBDF2}

        nEngines = len(engines)

        payoff = PlainVanillaPayoff(Option.Put, spot.value())
        exercise = EuropeanExercise(maturity)

        option = VanillaOption(payoff, exercise)
        option.setPricingEngine(analytic)
        expected = option.NPV()

        tol = 0.006

        for i in engines.keys():
            option.setPricingEngine(engines[i])
            calculated = option.NPV()

            diff = abs(expected - calculated)

            self.assertFalse(diff > tol)

        dividendOption = DividendVanillaOption(
            payoff, exercise,
            DateVector(1, today + Period(3, Months)),
            DoubleVector(1, 5.0))

        dividendPrices = Array(nEngines)
        for i, k in zip(range(nEngines), engines.keys()):
            dividendOption.setPricingEngine(engines[k])
            dividendPrices[i] = dividendOption.NPV()

        expectedDiv = 0.0
        for p in dividendPrices:
            expectedDiv += p
        expectedDiv /= nEngines

        for i in range(nEngines):
            calculated = dividendPrices[i]
            diff = abs(expectedDiv - calculated)
            self.assertFalse(diff > tol)

        idxDouglas = 0
        for i in engines.keys():
            if i != "Douglas":
                idxDouglas += 1
            else:
                break

        douglasNPV = dividendPrices[idxDouglas]

        idxCrankNicolson = 0
        for i in engines.keys():
            if i != "Crank-Nicolson":
                idxCrankNicolson += 1
            else:
                break

        crankNicolsonNPV = dividendPrices[idxCrankNicolson]
        schemeTol = 1e-12
        schemeDiff = abs(crankNicolsonNPV - douglasNPV)
        self.assertFalse(schemeDiff > schemeTol)

    def testDouglasVsCrankNicolson(self):
        TEST_MESSAGE(
            "Testing Douglas vs Crank-Nicolson scheme for finite-difference European PDE engines...")
        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(18, October, 2018)

        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        qTS = YieldTermStructureHandle(flatRate(today, 0.02, dc))
        rTS = YieldTermStructureHandle(flatRate(today, 0.075, dc))
        volTS = BlackVolTermStructureHandle(flatVol(today, 0.25, dc))

        process = BlackScholesMertonProcess(
            spot, qTS, rTS, volTS)

        option = VanillaOption(
            PlainVanillaPayoff(Option.Put, spot.value() + 2),
            EuropeanExercise(today + Period(6, Months)))

        option.setPricingEngine(
            AnalyticEuropeanEngine(process))

        npv = option.NPV()
        schemeTol = 1e-12
        npvTol = 1e-2

        for theta in np.arange(0.2, 0.81, 0.1):
            option.setPricingEngine(
                FdBlackScholesVanillaEngine(
                    process, 500, 100, 0,
                    FdmSchemeDesc(
                        FdmSchemeDesc.CrankNicolsonType, theta, 0.0)))

            crankNicolsonNPV = option.NPV()
            npvDiff = abs(crankNicolsonNPV - npv)

            self.assertFalse(npvDiff > npvTol)

            option.setPricingEngine(
                FdBlackScholesVanillaEngine(
                    process, 500, 100, 0,
                    FdmSchemeDesc(
                        FdmSchemeDesc.DouglasType, theta, 0.0)))

            douglasNPV = option.NPV()
            schemeDiff = abs(crankNicolsonNPV - douglasNPV)
            self.assertFalse(schemeDiff > schemeTol)

    def testFdEngineWithNonConstantParameters(self):
        TEST_MESSAGE(
            "Testing finite-difference European engine with non-constant parameters...")
        backup = SavedSettings()

        u = 190.0
        v = 0.2

        dc = Actual360()
        today = knownGoodDefault
        Settings.instance().evaluationDate = today

        spot = SimpleQuote(u)
        volTS = flatVol(today, v, dc)
        dates = DateVector(5)
        rates = DoubleVector(5)

        dates[0] = today
        rates[0] = 0.0
        dates[1] = today + Period(90, Days)
        rates[1] = 0.001
        dates[2] = today + Period(180, Days)
        rates[2] = 0.002
        dates[3] = today + Period(270, Days)
        rates[3] = 0.005
        dates[4] = today + Period(360, Days)
        rates[4] = 0.01

        rTS = ForwardCurve(dates, rates, dc)
        r = rTS.zeroRate(dates[4], dc, Continuous)

        process = BlackScholesProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))

        exercise = EuropeanExercise(today + Period(360, Days))
        payoff = PlainVanillaPayoff(Option.Call, 190.0)

        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(AnalyticEuropeanEngine(process))

        expected = option.NPV()
        timeSteps = 200
        gridPoints = 201

        option.setPricingEngine(
            FdBlackScholesVanillaEngine(
                process, timeSteps, gridPoints))
        calculated = option.NPV()

        tolerance = 0.01
        error = abs(expected - calculated)

        self.assertFalse(error > tolerance)

    def _testEngineConsistency(self,
                               engine,
                               binomialSteps,
                               samples,
                               tolerance,
                               testGreeks=False):

        types = [Option.Call, Option.Put]
        strikes = [75.0, 100.0, 125.0]
        lengths = [1]

        underlyings = [100.0]
        qRates = [0.00, 0.05]
        rRates = [0.01, 0.05, 0.15]
        vols = [0.11, 0.50, 1.20]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        for ty in types:
            for strike in strikes:
                for length in lengths:
                    exDate = today + Period(360 * length, Days)
                    exercise = EuropeanExercise(exDate)
                    payoff = PlainVanillaPayoff(ty, strike)

                    refOption = makeOption(
                        payoff, exercise, spot, qTS, rTS, volTS,
                        EngineType.Analytic, NullSize(), NullSize())

                    option = makeOption(
                        payoff, exercise, spot, qTS, rTS, volTS,
                        engine, binomialSteps, samples)
                    for u in underlyings:
                        for q in qRates:
                            for r in rRates:
                                for v in vols:

                                    spot.setValue(u)
                                    qRate.setValue(q)
                                    rRate.setValue(r)
                                    vol.setValue(v)

                                    expected = dict()
                                    calculated = dict()

                                    expected["value"] = refOption.NPV()
                                    calculated["value"] = option.NPV()

                                    if testGreeks and option.NPV() > spot.value() * 1.0e-5:
                                        expected["delta"] = refOption.delta()
                                        expected["gamma"] = refOption.gamma()
                                        expected["theta"] = refOption.theta()
                                        calculated["delta"] = option.delta()
                                        calculated["gamma"] = option.gamma()
                                        calculated["theta"] = option.theta()

                                    for greek in calculated.keys():
                                        expct = expected[greek]
                                        calcl = calculated[greek]
                                        tol = tolerance[greek]
                                        error = relativeError(expct, calcl, u)

                                        self.assertFalse(error > tol)
