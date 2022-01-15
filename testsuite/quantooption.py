import unittest
from utilities import *
from QuantLib import *
from math import sqrt, log


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
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.fxr = fxr  # fx risk-free rate
        self.fxv = fxv  # fx volatility
        self.corr = corr  # correlation
        self.result = result  # expected result
        self.tol = tol  # tolerance


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
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.start = start  # time to reset
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.fxr = fxr  # fx risk-free rate
        self.fxv = fxv  # fx volatility
        self.corr = corr  # correlation
        self.result = result  # expected result
        self.tol = tol  # tolerance


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
        self.s = s  # spot
        self.strike = strike
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.fxr = fxr  # fx risk-free rate
        self.fxv = fxv  # fx volatility
        self.corr = corr  # correlation
        self.result = result  # expected result
        self.tol = tol  # tolerance


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
        self.s = s  # spot
        self.strike = strike
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.fxr = fxr  # fx risk-free rate
        self.fxv = fxv  # fx volatility
        self.corr = corr  # correlation
        self.result = result  # expected result
        self.tol = tol  # tolerance


class QuantoOptionTest(unittest.TestCase):

    def testValues(self):
        TEST_MESSAGE("Testing quanto option values...")

        backup = SavedSettings()

        # /* The data below are from
        #    from "Option pricing formulas", E.G. Haug, McGraw-Hill 1998

        values = [
            #       type, strike,  spot,  div, rate,   t, vol, fx risk-free rate, fx volatility, correlation,     result, tol
            # "Option pricing formulas", pag 105-106
            QuantoOptionData(Option.Call, 105.0, 100.0, 0.04, 0.08, 0.5, 0.2, 0.05, 0.10, 0.3, 5.3280 / 1.5, 1.0e-4),
            # "Option pricing formulas", VBA code
            QuantoOptionData(Option.Put, 105.0, 100.0, 0.04, 0.08, 0.5, 0.2, 0.05, 0.10, 0.3, 8.1636, 1.0e-4)]

        dc = Actual360()
        today = Date.todaysDate()

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
        TEST_MESSAGE("Testing quanto option greeks...")

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
        today = Date(16, Sep, 2015)
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

        for type in types:
            for strike in strikes:
                for length in lengths:

                    exDate = today + Period(length, Years)
                    exercise = EuropeanExercise(exDate)

                    payoff = PlainVanillaPayoff(type, strike)

                    option = QuantoVanillaOption(payoff, exercise)
                    option.setPricingEngine(engine)

                    for u in underlyings:
                        for m in qRates:
                            for n in rRates:
                                for v in vols:
                                    for fxr in rRates:
                                        for fxv in vols:
                                            for corr in correlations:

                                                q = m
                                                r = n
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
                                                    # perturb spot and get delta and gamma
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

                                                    # perturb rates and get rho and dividend rho
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

                                                    # perturb volatility and get vega
                                                    dv = v * 1.0e-4
                                                    vol.setValue(v + dv)
                                                    value_p = option.NPV()
                                                    vol.setValue(v - dv)
                                                    value_m = option.NPV()
                                                    vol.setValue(v)
                                                    expected["vega"] = (value_p - value_m) / (2 * dv)

                                                    # perturb fx rate and get qrho
                                                    dfxr = fxr * 1.0e-4
                                                    fxRate.setValue(fxr + dfxr)
                                                    value_p = option.NPV()
                                                    fxRate.setValue(fxr - dfxr)
                                                    value_m = option.NPV()
                                                    fxRate.setValue(fxr)
                                                    expected["qrho"] = (value_p - value_m) / (2 * dfxr)

                                                    # perturb fx volatility and get qvega
                                                    dfxv = fxv * 1.0e-4
                                                    fxVol.setValue(fxv + dfxv)
                                                    value_p = option.NPV()
                                                    fxVol.setValue(fxv - dfxv)
                                                    value_m = option.NPV()
                                                    fxVol.setValue(fxv)
                                                    expected["qvega"] = (value_p - value_m) / (2 * dfxv)

                                                    # perturb correlation and get qlambda
                                                    dcorr = corr * 1.0e-4
                                                    correlation.setValue(corr + dcorr)
                                                    value_p = option.NPV()
                                                    correlation.setValue(corr - dcorr)
                                                    value_m = option.NPV()
                                                    correlation.setValue(corr)
                                                    expected["qlambda"] = (value_p - value_m) / (2 * dcorr)

                                                    # perturb date and get theta
                                                    dT = dc.yearFraction(today - 1, today + 1)
                                                    Settings.instance().evaluationDate = today - 1
                                                    value_m = option.NPV()
                                                    Settings.instance().evaluationDate = today + 1
                                                    value_p = option.NPV()
                                                    Settings.instance().evaluationDate = today
                                                    expected["theta"] = (value_p - value_m) / dT

                                                    # compare
                                                    for it in calculated.keys():
                                                        greek = it
                                                        expct = expected[greek]
                                                        calcl = calculated[greek]
                                                        tol = tolerance[greek]
                                                        error = relativeError(expct, calcl, u)
                                                        if error > tol:
                                                            self.assertFalse(error > tol)

    def testForwardValues(self):
        TEST_MESSAGE("Testing quanto-forward option values...")

        backup = SavedSettings()

        values = [
            #   type, moneyness,  spot,  div, risk-free rate, reset, maturity,  vol, fx risk-free rate, fx vol, corr,     result, tol
            # reset=0.0, quanto (not-forward) options
            QuantoForwardOptionData(Option.Call, 1.05, 100.0, 0.04, 0.08, 0.00, 0.5, 0.20, 0.05, 0.10, 0.3, 5.3280 / 1.5, 1.0e-4),
            QuantoForwardOptionData(Option.Put, 1.05, 100.0, 0.04, 0.08, 0.00, 0.5, 0.20, 0.05, 0.10, 0.3, 8.1636, 1.0e-4),
            # reset!=0.0, quanto-forward options (cursory checked against FinCAD 7)
            QuantoForwardOptionData(Option.Call, 1.05, 100.0, 0.04, 0.08, 0.25, 0.5, 0.20, 0.05, 0.10, 0.3, 2.0171, 1.0e-4),
            QuantoForwardOptionData(Option.Put, 1.05, 100.0, 0.04, 0.08, 0.25, 0.5, 0.20, 0.05, 0.10, 0.3, 6.7296, 1.0e-4)]

        dc = Actual360()
        today = Date.todaysDate()

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
        TEST_MESSAGE("Testing quanto-forward option greeks...")

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
        today = Date.todaysDate()
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

        for type in types:
            for moneynes in moneyness:
                for length in lengths:
                    for startMonth in startMonths:

                        exDate = today + Period(length, Years)
                        exercise = EuropeanExercise(exDate)

                        reset = today + Period(startMonth, Months)

                        payoff = PlainVanillaPayoff(type, 0.0)

                        option = QuantoForwardVanillaOption(moneynes, reset, payoff, exercise)
                        option.setPricingEngine(engine)

                        for u in underlyings:
                            for m in qRates:
                                for n in rRates:
                                    for v in vols:
                                        for fxr in rRates:
                                            for fxv in vols:
                                                for corr in correlations:

                                                    q = m
                                                    r = n
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
                                                        # perturb spot and get delta and gamma
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

                                                        # perturb rates and get rho and dividend rho
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

                                                        # perturb volatility and get vega
                                                        dv = v * 1.0e-4
                                                        vol.setValue(v + dv)
                                                        value_p = option.NPV()
                                                        vol.setValue(v - dv)
                                                        value_m = option.NPV()
                                                        vol.setValue(v)
                                                        expected["vega"] = (value_p - value_m) / (2 * dv)

                                                        # perturb fx rate and get qrho
                                                        dfxr = fxr * 1.0e-4
                                                        fxRate.setValue(fxr + dfxr)
                                                        value_p = option.NPV()
                                                        fxRate.setValue(fxr - dfxr)
                                                        value_m = option.NPV()
                                                        fxRate.setValue(fxr)
                                                        expected["qrho"] = (value_p - value_m) / (2 * dfxr)

                                                        # perturb fx volatility and get qvega
                                                        dfxv = fxv * 1.0e-4
                                                        fxVol.setValue(fxv + dfxv)
                                                        value_p = option.NPV()
                                                        fxVol.setValue(fxv - dfxv)
                                                        value_m = option.NPV()
                                                        fxVol.setValue(fxv)
                                                        expected["qvega"] = (value_p - value_m) / (2 * dfxv)

                                                        # perturb correlation and get qlambda
                                                        dcorr = corr * 1.0e-4
                                                        correlation.setValue(corr + dcorr)
                                                        value_p = option.NPV()
                                                        correlation.setValue(corr - dcorr)
                                                        value_m = option.NPV()
                                                        correlation.setValue(corr)
                                                        expected["qlambda"] = (value_p - value_m) / (2 * dcorr)

                                                        # perturb date and get theta
                                                        dT = dc.yearFraction(today - 1, today + 1)
                                                        Settings.instance().evaluationDate = today - 1
                                                        value_m = option.NPV()
                                                        Settings.instance().evaluationDate = today + 1
                                                        value_p = option.NPV()
                                                        Settings.instance().evaluationDate = today
                                                        expected["theta"] = (value_p - value_m) / dT

                                                        # compare

                                                        for it in calculated.keys():
                                                            greek = it
                                                            expct = expected[greek]
                                                            calcl = calculated[greek]
                                                            tol = tolerance[greek]
                                                            error = relativeError(expct, calcl, u)
                                                            self.assertFalse(error > tol)

    def testForwardPerformanceValues(self):
        TEST_MESSAGE("Testing quanto-forward-performance option values...")

        backup = SavedSettings()

        values = [
            #   type, moneyness,  spot,  div, risk-free rate, reset, maturity,  vol, fx risk-free rate, fx vol, corr,     result, tol
            # reset=0.0, quanto-(not-forward)-performance options
            # exactly one hundredth of the non-performance version
            QuantoForwardOptionData(Option.Call, 1.05, 100.0, 0.04, 0.08, 0.00, 0.5, 0.20, 0.05, 0.10, 0.3, 5.3280 / 150, 1.0e-4),
            QuantoForwardOptionData(Option.Put, 1.05, 100.0, 0.04, 0.08, 0.00, 0.5, 0.20, 0.05, 0.10, 0.3, 0.0816, 1.0e-4),
            # reset!=0.0, quanto-forward-performance options (roughly one hundredth of the non-performance version)
            QuantoForwardOptionData(Option.Call, 1.05, 100.0, 0.04, 0.08, 0.25, 0.5, 0.20, 0.05, 0.10, 0.3, 0.0201, 1.0e-4),
            QuantoForwardOptionData(Option.Put, 1.05, 100.0, 0.04, 0.08, 0.25, 0.5, 0.20, 0.05, 0.10, 0.3, 0.0672, 1.0e-4)]

        dc = Actual360()
        today = Date.todaysDate()

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
            #     = PercentageStrikePayoff(values[i].type,
            #     values[i].moneyness))

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
        TEST_MESSAGE("Testing quanto-barrier option values...")

        backup = SavedSettings()

        values = [
            # TODO:  Bench results against an existing prop calculator
            # barrierType, barrier, rebate, type, spot, strike,
            # q, r, T, vol, fx risk-free rate, fx vol, corr, result, tol
            QuantoBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, 100, 90, 0.04, 0.0212, 0.50, 0.25, 0.05, 0.2, 0.3, 8.247, 0.5),
            QuantoBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, 100, 90, 0.04, 0.0212, 0.50, 0.25, 0.05, 0.2, 0.3, 2.274, 0.5),
            QuantoBarrierOptionData(Barrier.DownIn, 95.0, 0, Option.Put, 100, 90, 0.04, 0.0212, 0.50, 0.25, 0.05, 0.2, 0.3, 2.85, 0.5), ]

        dc = Actual360()
        today = Date.todaysDate()

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
        TEST_MESSAGE("Testing quanto-double-barrier option values...")

        backup = SavedSettings()

        values = [
            # barrierType,           bar.lo, bar.hi, rebate,         type, spot,  strk,    q,   r,    T,  vol, fx rate, fx vol, corr, result, tol
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, 0, Option.Call, 100, 100.0, 0.00, 0.1, 0.25, 0.15, 0.05, 0.2, 0.3, 3.4623, 1.0e-4),
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, 0, Option.Call, 100, 100.0, 0.00, 0.1, 0.50, 0.15, 0.05, 0.2, 0.3, 0.5236, 1.0e-4),
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, 0, Option.Put, 100, 100.0, 0.00, 0.1, 0.25, 0.15, 0.05, 0.2, 0.3, 1.1320, 1.0e-4),
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, 0, Option.Call, 100, 102.0, 0.00, 0.1, 0.25, 0.25, 0.05, 0.2, 0.3, 2.6313, 1.0e-4),
            QuantoDoubleBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, 0, Option.Call, 100, 102.0, 0.00, 0.1, 0.50, 0.15, 0.05, 0.2, 0.3, 1.9305, 1.0e-4)]

        dc = Actual360()
        today = Date.todaysDate()

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
        TEST_MESSAGE("Testing FDM quanto helper...")

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
        TEST_MESSAGE("Testing quanto-option values with PDEs...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(21, April, 2019)

        values = [
            #    type,    strike,  spot,   div, domestic rate,  t,   vol, foreign rate, fx vol, correlation, result,     tol
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
        TEST_MESSAGE("Testing American quanto-option values with PDEs...")

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
