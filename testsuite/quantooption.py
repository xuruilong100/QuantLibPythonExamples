import unittest
from math import sqrt, log

from QuantLib import *

from utilities import *


class QuantoOptionData(object):
    def __init__(self,
                 typeOpt,
                 strike,
                 s,
                 q,
                 r,
                 t,
                 v,
                 fxr,
                 fxv,
                 corr,
                 result,
                 tol, ):
        self.typeOpt = typeOpt
        self.strike = strike
        self.s = s
        self.q = q
        self.r = r
        self.t = t
        self.v = v
        self.fxr = fxr
        self.fxv = fxv
        self.corr = corr
        self.result = result
        self.tol = tol


class QuantoForwardOptionData(object):
    def __init__(self,
                 typeOpt,
                 moneyness,
                 s,
                 q,
                 r,
                 start,
                 t,
                 v,
                 fxr,
                 fxv,
                 corr,
                 result,
                 tol, ):
        self.typeOpt = typeOpt
        self.moneyness = moneyness
        self.s = s
        self.q = q
        self.r = r
        self.start = start
        self.t = t
        self.v = v
        self.fxr = fxr
        self.fxv = fxv
        self.corr = corr
        self.result = result
        self.tol = tol


class QuantoBarrierOptionData(object):
    def __init__(self,
                 barrierType,
                 barrier,
                 rebate,
                 typeOpt,
                 s,
                 strike,
                 q,
                 r,
                 t,
                 v,
                 fxr,
                 fxv,
                 corr,
                 result,
                 tol, ):
        self.barrierType = barrierType
        self.barrier = barrier
        self.rebate = rebate
        self.typeOpt = typeOpt
        self.s = s
        self.strike = strike
        self.q = q
        self.r = r
        self.t = t
        self.v = v
        self.fxr = fxr
        self.fxv = fxv
        self.corr = corr
        self.result = result
        self.tol = tol


class QuantoDoubleBarrierOptionData(object):
    def __init__(self,
                 barrierType,
                 barrier_lo,
                 barrier_hi,
                 rebate,
                 typeOpt,
                 s,
                 strike,
                 q,
                 r,
                 t,
                 v,
                 fxr,
                 fxv,
                 corr,
                 result,
                 tol):
        self.barrierType = barrierType
        self.barrier_lo = barrier_lo
        self.barrier_hi = barrier_hi
        self.rebate = rebate
        self.typeOpt = typeOpt
        self.s = s
        self.strike = strike
        self.q = q
        self.r = r
        self.t = t
        self.v = v
        self.fxr = fxr
        self.fxv = fxv
        self.corr = corr
        self.result = result
        self.tol = tol


class QuantoOptionTest(unittest.TestCase):

    def testValues(self):
        TEST_MESSAGE(
            "Testing quanto option values...")

        backup = SavedSettings()

        values = [
            QuantoOptionData(Option.Call, 105.0, 100.0, 0.04, 0.08, 0.5, 0.2, 0.05, 0.10, 0.3, 5.3280 / 1.5, 1.0e-4),
            QuantoOptionData(Option.Put, 105.0, 100.0, 0.04, 0.08, 0.5, 0.2, 0.05, 0.10, 0.3, 8.1636, 1.0e-4)]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        fxRate = SimpleQuote(0.0)
        fxrTS = YieldTermStructureHandle(flatRate(today, fxRate, dc))
        fxVol = SimpleQuote(0.0)
        fxVolTS = BlackVolTermStructureHandle(flatVol(today, fxVol, dc))
        correlation = SimpleQuote(0.0)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS,
            volTS)
        engine = QuantoVanillaEngine(
            stochProcess, fxrTS, fxVolTS,
            QuoteHandle(correlation))

        for value in values:
            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            fxRate.setValue(value.fxr)
            fxVol.setValue(value.fxv)
            correlation.setValue(value.corr)

            option = QuantoVanillaOption(payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = 1e-4
            self.assertFalse(error > tolerance)

    def testGreeks(self):
        TEST_MESSAGE(
            "Testing quanto option greeks...")

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
        tolerance["qrho"] = 1.0e-5
        tolerance["qvega"] = 1.0e-5
        tolerance["qlambda"] = 1.0e-5

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.04, 0.05]
        rRates = [0.01, 0.05, 0.15]
        lengths = [2]
        vols = [0.11, 1.20]
        correlations = [0.10, 0.90]

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
        fxRate = SimpleQuote(0.0)
        fxrTS = YieldTermStructureHandle(flatRate(fxRate, dc))
        fxVol = SimpleQuote(0.0)
        fxVolTS = BlackVolTermStructureHandle(flatVol(fxVol, dc))
        correlation = SimpleQuote(0.0)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = QuantoVanillaEngine(
            stochProcess, fxrTS, fxVolTS,
            QuoteHandle(correlation))

        for ty in types:
            for strike in strikes:
                for length in lengths:

                    exDate = today + Period(length, Years)
                    exercise = EuropeanExercise(exDate)

                    payoff = PlainVanillaPayoff(ty, strike)

                    option = QuantoVanillaOption(payoff, exercise)
                    option.setPricingEngine(engine)

                    for u in underlyings:
                        for q in qRates:
                            for r in rRates:
                                for v in vols:
                                    for fxr in rRates:
                                        for fxv in vols:
                                            for corr in correlations:

                                                spot.setValue(u)
                                                qRate.setValue(q)
                                                rRate.setValue(r)
                                                vol.setValue(v)
                                                fxRate.setValue(fxr)
                                                fxVol.setValue(fxv)
                                                correlation.setValue(corr)

                                                value = option.NPV()
                                                calculated["delta"] = option.delta()
                                                calculated["gamma"] = option.gamma()
                                                calculated["theta"] = option.theta()
                                                calculated["rho"] = option.rho()
                                                calculated["divRho"] = option.dividendRho()
                                                calculated["vega"] = option.vega()
                                                calculated["qrho"] = option.qrho()
                                                calculated["qvega"] = option.qvega()
                                                calculated["qlambda"] = option.qlambda()

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

                                                    dfxr = fxr * 1.0e-4
                                                    fxRate.setValue(fxr + dfxr)
                                                    value_p = option.NPV()
                                                    fxRate.setValue(fxr - dfxr)
                                                    value_m = option.NPV()
                                                    fxRate.setValue(fxr)
                                                    expected["qrho"] = (value_p - value_m) / (2 * dfxr)

                                                    dfxv = fxv * 1.0e-4
                                                    fxVol.setValue(fxv + dfxv)
                                                    value_p = option.NPV()
                                                    fxVol.setValue(fxv - dfxv)
                                                    value_m = option.NPV()
                                                    fxVol.setValue(fxv)
                                                    expected["qvega"] = (value_p - value_m) / (2 * dfxv)

                                                    dcorr = corr * 1.0e-4
                                                    correlation.setValue(corr + dcorr)
                                                    value_p = option.NPV()
                                                    correlation.setValue(corr - dcorr)
                                                    value_m = option.NPV()
                                                    correlation.setValue(corr)
                                                    expected["qlambda"] = (value_p - value_m) / (2 * dcorr)

                                                    dT = dc.yearFraction(today - 1, today + 1)
                                                    Settings.instance().evaluationDate = today - 1
                                                    value_m = option.NPV()
                                                    Settings.instance().evaluationDate = today + 1
                                                    value_p = option.NPV()
                                                    Settings.instance().evaluationDate = today
                                                    expected["theta"] = (value_p - value_m) / dT

                                                    for it in calculated.keys():
                                                        greek = it
                                                        expct = expected[greek]
                                                        calcl = calculated[greek]
                                                        tol = tolerance[greek]
                                                        error = relativeError(expct, calcl, u)
                                                        if error > tol:
                                                            self.assertFalse(error > tol)

    def testForwardValues(self):
        TEST_MESSAGE(
            "Testing quanto-forward option values...")

        backup = SavedSettings()

        values = [
            QuantoForwardOptionData(Option.Call, 1.05, 100.0, 0.04, 0.08, 0.00, 0.5, 0.20, 0.05, 0.10, 0.3, 5.3280 / 1.5, 1.0e-4),
            QuantoForwardOptionData(Option.Put, 1.05, 100.0, 0.04, 0.08, 0.00, 0.5, 0.20, 0.05, 0.10, 0.3, 8.1636, 1.0e-4),
            QuantoForwardOptionData(Option.Call, 1.05, 100.0, 0.04, 0.08, 0.25, 0.5, 0.20, 0.05, 0.10, 0.3, 2.0171, 1.0e-4),
            QuantoForwardOptionData(Option.Put, 1.05, 100.0, 0.04, 0.08, 0.25, 0.5, 0.20, 0.05, 0.10, 0.3, 6.7296, 1.0e-4)]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        fxRate = SimpleQuote(0.0)
        fxrTS = YieldTermStructureHandle(flatRate(today, fxRate, dc))
        fxVol = SimpleQuote(0.0)
        fxVolTS = BlackVolTermStructureHandle(flatVol(today, fxVol, dc))
        correlation = SimpleQuote(0.0)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = QuantoForwardVanillaEngine(
            stochProcess, fxrTS, fxVolTS,
            QuoteHandle(correlation))

        for value in values:
            payoff = PlainVanillaPayoff(value.typeOpt, 0.0)
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)
            reset = today + timeToDays(value.start)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            fxRate.setValue(value.fxr)
            fxVol.setValue(value.fxv)
            correlation.setValue(value.corr)

            option = QuantoForwardVanillaOption(
                value.moneyness, reset, payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = 1e-4
            self.assertFalse(error > tolerance)

    def testForwardGreeks(self):
        TEST_MESSAGE(
            "Testing quanto-forward option greeks...")

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
        tolerance["qrho"] = 1.0e-5
        tolerance["qvega"] = 1.0e-5
        tolerance["qlambda"] = 1.0e-5

        types = [Option.Call, Option.Put]
        moneyness = [0.9, 1.0, 1.1]
        underlyings = [100.0]
        qRates = [0.04, 0.05]
        rRates = [0.01, 0.05, 0.15]
        lengths = [2]
        startMonths = [6, 9]
        vols = [0.11, 1.20]
        correlations = [0.10, 0.90]

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
        fxRate = SimpleQuote(0.0)
        fxrTS = YieldTermStructureHandle(flatRate(fxRate, dc))
        fxVol = SimpleQuote(0.0)
        fxVolTS = BlackVolTermStructureHandle(flatVol(fxVol, dc))
        correlation = SimpleQuote(0.0)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = QuantoForwardVanillaEngine(
            stochProcess, fxrTS, fxVolTS,
            QuoteHandle(correlation))

        for ty in types:
            for moneynes in moneyness:
                for length in lengths:
                    for startMonth in startMonths:

                        exDate = today + Period(length, Years)
                        exercise = EuropeanExercise(exDate)

                        reset = today + Period(startMonth, Months)

                        payoff = PlainVanillaPayoff(ty, 0.0)

                        option = QuantoForwardVanillaOption(moneynes, reset, payoff, exercise)
                        option.setPricingEngine(engine)

                        for u in underlyings:
                            for q in qRates:
                                for r in rRates:
                                    for v in vols:
                                        for fxr in rRates:
                                            for fxv in vols:
                                                for corr in correlations:

                                                    spot.setValue(u)
                                                    qRate.setValue(q)
                                                    rRate.setValue(r)
                                                    vol.setValue(v)
                                                    fxRate.setValue(fxr)
                                                    fxVol.setValue(fxv)
                                                    correlation.setValue(corr)

                                                    value = option.NPV()
                                                    calculated["delta"] = option.delta()
                                                    calculated["gamma"] = option.gamma()
                                                    calculated["theta"] = option.theta()
                                                    calculated["rho"] = option.rho()
                                                    calculated["divRho"] = option.dividendRho()
                                                    calculated["vega"] = option.vega()
                                                    calculated["qrho"] = option.qrho()
                                                    calculated["qvega"] = option.qvega()
                                                    calculated["qlambda"] = option.qlambda()

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

                                                        dfxr = fxr * 1.0e-4
                                                        fxRate.setValue(fxr + dfxr)
                                                        value_p = option.NPV()
                                                        fxRate.setValue(fxr - dfxr)
                                                        value_m = option.NPV()
                                                        fxRate.setValue(fxr)
                                                        expected["qrho"] = (value_p - value_m) / (2 * dfxr)

                                                        dfxv = fxv * 1.0e-4
                                                        fxVol.setValue(fxv + dfxv)
                                                        value_p = option.NPV()
                                                        fxVol.setValue(fxv - dfxv)
                                                        value_m = option.NPV()
                                                        fxVol.setValue(fxv)
                                                        expected["qvega"] = (value_p - value_m) / (2 * dfxv)

                                                        dcorr = corr * 1.0e-4
                                                        correlation.setValue(corr + dcorr)
                                                        value_p = option.NPV()
                                                        correlation.setValue(corr - dcorr)
                                                        value_m = option.NPV()
                                                        correlation.setValue(corr)
                                                        expected["qlambda"] = (value_p - value_m) / (2 * dcorr)

                                                        dT = dc.yearFraction(today - 1, today + 1)
                                                        Settings.instance().evaluationDate = today - 1
                                                        value_m = option.NPV()
                                                        Settings.instance().evaluationDate = today + 1
                                                        value_p = option.NPV()
                                                        Settings.instance().evaluationDate = today
                                                        expected["theta"] = (value_p - value_m) / dT

                                                        for it in calculated.keys():
                                                            greek = it
                                                            expct = expected[greek]
                                                            calcl = calculated[greek]
                                                            tol = tolerance[greek]
                                                            error = relativeError(expct, calcl, u)
                                                            self.assertFalse(error > tol)

    def testForwardPerformanceValues(self):
        TEST_MESSAGE(
            "Testing quanto-forward-performance option values...")

        backup = SavedSettings()

        values = [
            QuantoForwardOptionData(Option.Call, 1.05, 100.0, 0.04, 0.08, 0.00, 0.5, 0.20, 0.05, 0.10, 0.3, 5.3280 / 150, 1.0e-4),
            QuantoForwardOptionData(Option.Put, 1.05, 100.0, 0.04, 0.08, 0.00, 0.5, 0.20, 0.05, 0.10, 0.3, 0.0816, 1.0e-4),
            QuantoForwardOptionData(Option.Call, 1.05, 100.0, 0.04, 0.08, 0.25, 0.5, 0.20, 0.05, 0.10, 0.3, 0.0201, 1.0e-4),
            QuantoForwardOptionData(Option.Put, 1.05, 100.0, 0.04, 0.08, 0.25, 0.5, 0.20, 0.05, 0.10, 0.3, 0.0672, 1.0e-4)]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        fxRate = SimpleQuote(0.0)
        fxrTS = YieldTermStructureHandle(flatRate(today, fxRate, dc))
        fxVol = SimpleQuote(0.0)
        fxVolTS = BlackVolTermStructureHandle(flatVol(today, fxVol, dc))
        correlation = SimpleQuote(0.0)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = QuantoForwardVanillaPerformanceEngine(
            stochProcess, fxrTS, fxVolTS,
            QuoteHandle(correlation))

        for value in values:
            payoff = PlainVanillaPayoff(value.typeOpt, 0.0)

            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)
            reset = today + timeToDays(value.start)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            fxRate.setValue(value.fxr)
            fxVol.setValue(value.fxv)
            correlation.setValue(value.corr)

            option = QuantoForwardVanillaOption(
                value.moneyness, reset, payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = 1e-4
            self.assertFalse(error > tolerance)

    def testBarrierValues(self):
        TEST_MESSAGE(
            "Testing quanto-barrier option values...")

        backup = SavedSettings()

        values = [
            QuantoBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, 100, 90, 0.04, 0.0212, 0.50, 0.25, 0.05, 0.2, 0.3, 8.247, 0.5),
            QuantoBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, 100, 90, 0.04, 0.0212, 0.50, 0.25, 0.05, 0.2, 0.3, 2.274, 0.5),
            QuantoBarrierOptionData(Barrier.DownIn, 95.0, 0, Option.Put, 100, 90, 0.04, 0.0212, 0.50, 0.25, 0.05, 0.2, 0.3, 2.85, 0.5), ]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        fxRate = SimpleQuote(0.0)
        fxrTS = YieldTermStructureHandle(flatRate(today, fxRate, dc))
        fxVol = SimpleQuote(0.0)
        fxVolTS = BlackVolTermStructureHandle(flatVol(today, fxVol, dc))
        correlation = SimpleQuote(0.0)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = QuantoBarrierEngine(
            stochProcess, fxrTS, fxVolTS,
            QuoteHandle(correlation))

        for value in values:
            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)

            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            fxRate.setValue(value.fxr)
            fxVol.setValue(value.fxv)
            correlation.setValue(value.corr)

            option = QuantoBarrierOption(
                value.barrierType, value.barrier, value.rebate, payoff, exercise)

            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = value.tol

            self.assertFalse(error > tolerance)

    def testDoubleBarrierValues(self):
        TEST_MESSAGE(
            "Testing quanto-double-barrier option values...")

        backup = SavedSettings()

        values = [
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, 0, Option.Call, 100, 100.0, 0.00, 0.1, 0.25, 0.15, 0.05, 0.2, 0.3, 3.4623, 1.0e-4),
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, 0, Option.Call, 100, 100.0, 0.00, 0.1, 0.50, 0.15, 0.05, 0.2, 0.3, 0.5236, 1.0e-4),
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, 0, Option.Put, 100, 100.0, 0.00, 0.1, 0.25, 0.15, 0.05, 0.2, 0.3, 1.1320, 1.0e-4),
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, 0, Option.Call, 100, 102.0, 0.00, 0.1, 0.25, 0.25, 0.05, 0.2, 0.3, 2.6313, 1.0e-4),
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, 0, Option.Call, 100, 102.0, 0.00, 0.1, 0.50, 0.15, 0.05, 0.2, 0.3, 1.9305, 1.0e-4)]

        dc = Actual360()
        today = knownGoodDefault

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        fxRate = SimpleQuote(0.0)
        fxrTS = YieldTermStructureHandle(flatRate(today, fxRate, dc))
        fxVol = SimpleQuote(0.0)
        fxVolTS = BlackVolTermStructureHandle(flatVol(today, fxVol, dc))
        correlation = SimpleQuote(0.0)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = QuantoDoubleBarrierEngine(
            stochProcess, fxrTS, fxVolTS,
            QuoteHandle(correlation))

        for value in values:
            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)

            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            fxRate.setValue(value.fxr)
            fxVol.setValue(value.fxv)
            correlation.setValue(value.corr)

            option = QuantoDoubleBarrierOption(
                value.barrierType, value.barrier_lo, value.barrier_hi,
                value.rebate, payoff, exercise)

            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = value.tol

            self.assertFalse(error > tolerance)

    def testFDMQuantoHelper(self):
        TEST_MESSAGE(
            "Testing FDM quanto helper...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(22, April, 2019)

        s = 100
        domesticR = 0.1
        foreignR = 0.2
        q = 0.3
        vol = 0.3
        fxVol = 0.2

        exchRateATMlevel = 1.0
        equityFxCorrelation = -0.75

        domesticTS = YieldTermStructureHandle(
            flatRate(today, domesticR, dc))

        divTS = YieldTermStructureHandle(
            flatRate(today, q, dc))

        volTS = BlackVolTermStructureHandle(
            flatVol(today, vol, dc))

        spot = QuoteHandle(SimpleQuote(s))

        bsmProcess = BlackScholesMertonProcess(
            spot, divTS, domesticTS, volTS)

        foreignTS = flatRate(today, foreignR, dc)

        fxVolTS = flatVol(today, fxVol, dc)

        fdmQuantoHelper = FdmQuantoHelper(
            domesticTS.currentLink(),
            foreignTS, fxVolTS,
            equityFxCorrelation, exchRateATMlevel)

        calculatedQuantoAdj = fdmQuantoHelper.quantoAdjustment(vol, 0.0, 1.0)

        expectedQuantoAdj = domesticR - foreignR + equityFxCorrelation * vol * fxVol

        tol = 1e-10
        self.assertFalse(abs(calculatedQuantoAdj - expectedQuantoAdj) > tol)

        maturityDate = today + Period(6, Months)
        maturityTime = dc.yearFraction(today, maturityDate)

        eps = 0.0002
        scalingFactor = 1.25

        mesher = FdmBlackScholesMesher(
            3, bsmProcess, maturityTime, s,
            NullReal(), NullReal(), eps, scalingFactor,
            (NullReal(), NullReal()),
            DividendSchedule(),
            fdmQuantoHelper)

        normInvEps = InverseCumulativeNormal()(1 - eps)
        sigmaSqrtT = vol * sqrt(maturityTime)

        qQuanto = q + expectedQuantoAdj
        expectedDriftRate = domesticR - qQuanto

        logFwd = log(s) + expectedDriftRate * maturityTime
        xMin = logFwd - sigmaSqrtT * normInvEps * scalingFactor
        xMax = log(s) + sigmaSqrtT * normInvEps * scalingFactor

        loc = mesher.locations()

        self.assertFalse(
            abs(loc[0] - xMin) > tol or abs(loc[len(loc) - 1] - xMax) > tol)

    def testPDEOptionValues(self):
        TEST_MESSAGE(
            "Testing quanto-option values with PDEs...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(21, April, 2019)

        values = [
            QuantoOptionData(Option.Call, 105.0, 100.0, 0.04, 0.08, 0.5, 0.2, 0.05, 0.10, 0.3, NullReal(), NullReal()),
            QuantoOptionData(Option.Call, 100.0, 100.0, 0.16, 0.08, 0.25, 0.15, 0.05, 0.20, -0.3, NullReal(), NullReal()),
            QuantoOptionData(Option.Call, 105.0, 100.0, 0.04, 0.08, 0.5, 0.2, 0.05, 0.10, 0.3, NullReal(), NullReal()),
            QuantoOptionData(Option.Put, 105.0, 100.0, 0.04, 0.08, 0.5, 0.2, 0.05, 0.10, 0.3, NullReal(), NullReal()),
            QuantoOptionData(Option.Call, 0.0, 100.0, 0.04, 0.08, 0.3, 0.3, 0.05, 0.10, 0.75, NullReal(), NullReal()), ]

        for value in values:

            calculated = dict()
            expected = dict()
            tolerance = dict()
            tolerance["npv"] = 2e-4
            tolerance["delta"] = 1e-4
            tolerance["gamma"] = 1e-4
            tolerance["theta"] = 1e-4

            spot = QuoteHandle(SimpleQuote(value.s))

            strike = value.strike

            domesticTS = YieldTermStructureHandle(flatRate(today, value.r, dc))
            divTS = YieldTermStructureHandle(flatRate(today, value.q, dc))
            volTS = BlackVolTermStructureHandle(flatVol(today, value.v, dc))

            bsmProcess = BlackScholesMertonProcess(
                spot, divTS, domesticTS, volTS)

            foreignTS = YieldTermStructureHandle(flatRate(today, value.fxr, dc))
            fxVolTS = BlackVolTermStructureHandle(flatVol(today, value.fxv, dc))

            exchRateATMlevel = 1.0
            equityFxCorrelation = value.corr

            quantoHelper = FdmQuantoHelper(
                domesticTS.currentLink(),
                foreignTS.currentLink(),
                fxVolTS.currentLink(),
                equityFxCorrelation, exchRateATMlevel)

            payoff = PlainVanillaPayoff(value.typeOpt, strike)
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            option = VanillaOption(payoff, exercise)

            pdeEngine = FdBlackScholesVanillaEngine(
                bsmProcess, quantoHelper, int(value.t * 200), 500, 1)

            option.setPricingEngine(pdeEngine)

            calculated["npv"] = option.NPV()
            calculated["delta"] = option.delta()
            calculated["gamma"] = option.delta()
            calculated["theta"] = option.delta()

            analyticEngine = QuantoVanillaEngine(
                bsmProcess, foreignTS, fxVolTS,
                QuoteHandle(
                    SimpleQuote(equityFxCorrelation)))

            option.setPricingEngine(analyticEngine)

            expected["npv"] = option.NPV()
            expected["delta"] = option.delta()
            expected["gamma"] = option.delta()
            expected["theta"] = option.delta()

            for it in calculated.keys():
                greek = it
                expct = expected[greek]
                calcl = calculated[greek]
                error = abs(expct - calcl)
                tol = tolerance[greek]

                self.assertFalse(error > tol)

    def testAmericanQuantoOption(self):
        TEST_MESSAGE(
            "Testing American quanto-option values with PDEs...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(21, April, 2019)
        maturity = today + Period(9, Months)
        Settings.instance().evaluationDate = today

        s = 100
        domesticR = 0.025
        foreignR = 0.075
        q = 0.03
        vol = 0.3
        fxVol = 0.15

        exchRateATMlevel = 1.0
        equityFxCorrelation = -0.75

        domesticTS = YieldTermStructureHandle(
            flatRate(today, domesticR, dc))

        divTS = YieldTermStructureHandle(
            flatRate(today, q, dc))

        volTS = BlackVolTermStructureHandle(
            flatVol(today, vol, dc))

        spot = QuoteHandle(SimpleQuote(s))

        bsmProcess = BlackScholesMertonProcess(
            spot, divTS, domesticTS, volTS)

        foreignTS = flatRate(today, foreignR, dc)

        fxVolTS = flatVol(today, fxVol, dc)

        quantoHelper = FdmQuantoHelper(
            domesticTS.currentLink(),
            foreignTS,
            fxVolTS,
            equityFxCorrelation,
            exchRateATMlevel)

        strike = 105.0

        option = DividendVanillaOption(
            PlainVanillaPayoff(Option.Call, strike),
            AmericanExercise(maturity),
            DateVector(1, today + Period(6, Months)),
            DoubleVector(1, 8.0))

        option.setPricingEngine(
            FdBlackScholesVanillaEngine(
                bsmProcess, quantoHelper, 100, 400, 1))

        tol = 1e-4
        expected = 8.90611734
        bsCalculated = option.NPV()

        self.assertFalse(abs(expected - bsCalculated) > tol)

        option.setPricingEngine(
            FdBlackScholesVanillaEngine(
                bsmProcess, quantoHelper, 100, 400, 1))

        localVolCalculated = option.NPV()
        self.assertFalse(abs(expected - localVolCalculated) > tol)

        tolBetweenBSandLocalVol = 1e-6
        self.assertFalse(
            abs(bsCalculated - localVolCalculated) > tolBetweenBSandLocalVol)

        v0 = vol * vol
        kappa = 1.0
        theta = v0
        sigma = 1e-4
        rho = 0.0

        hestonModel = HestonModel(
            HestonProcess(
                domesticTS, divTS, spot, v0,
                kappa, theta, sigma, rho))

        option.setPricingEngine(
            FdHestonVanillaEngine(
                hestonModel, quantoHelper, 100, 400, 3, 1))

        hestonCalculated = option.NPV()

        self.assertFalse(abs(expected - hestonCalculated) > tol)

        localConstVol = LocalConstantVol(today, 2.0, dc)

        hestonModel05 = HestonModel(
            HestonProcess(
                domesticTS, divTS, spot, 0.25 * v0,
                kappa, 0.25 * theta, sigma, rho))

        option.setPricingEngine(
            FdHestonVanillaEngine(
                hestonModel05, quantoHelper, 100, 400, 3, 1,
                FdmSchemeDesc.Hundsdorfer(), localConstVol))

        hestoSlvCalculated = option.NPV()

        self.assertFalse(abs(expected - hestoSlvCalculated) > tol)
