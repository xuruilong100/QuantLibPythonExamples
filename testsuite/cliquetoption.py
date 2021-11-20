import unittest
from utilities import *
from QuantLib import *


class CliquetOptionTest(unittest.TestCase):
    def testValues(self):
        TEST_MESSAGE("Testing Cliquet option values...")

        today = Date.todaysDate()
        dc = Actual360()

        spot = SimpleQuote(60.0)
        qRate = SimpleQuote(0.04)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.08)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.30)
        volTS = flatVol(today, vol, dc)

        process = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        engine = AnalyticCliquetEngine(process)

        reset = DateVector()
        reset.push_back(today + 90)
        maturity = today + 360
        typeOpt = Option.Call
        moneyness = 1.1

        payoff = PercentageStrikePayoff(typeOpt, moneyness)
        exercise = EuropeanExercise(maturity)

        option = CliquetOption(payoff, exercise, reset)
        option.setPricingEngine(engine)

        calculated = option.NPV()
        expected = 4.4064  # Haug, p.37
        error = abs(calculated - expected)
        tolerance = 1e-4
        self.assertFalse(error > tolerance)

    def testGreeks(self):
        TEST_MESSAGE("Testing Cliquet option greeks...")
        self._testOptionGreeks(AnalyticCliquetEngine)

    def testPerformanceGreeks(self):
        TEST_MESSAGE("Testing performance option greeks...")
        self._testOptionGreeks(AnalyticPerformanceEngine)

    def testMcPerformance(self):
        TEST_MESSAGE(
            "Testing Monte Carlo performance engine against analytic results...")

        backup = SavedSettings()

        types = [Option.Call, Option.Put]
        moneyness = [0.9, 1.1]
        underlyings = [100.0]
        qRates = [0.04, 0.06]
        rRates = [0.01, 0.10]
        lengths = [2, 4]
        frequencies = [Semiannual, Quarterly]
        vols = [0.10, 0.90]

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

        process = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        for ty in types:
            for moneynes in moneyness:
                for length in lengths:
                    for frequencie in frequencies:

                        tenor = Period(frequencie)
                        maturity = EuropeanExercise(today + length * tenor)

                        payoff = PercentageStrikePayoff(ty, moneynes)

                        reset = DateVector()
                        d = today + tenor
                        while d < maturity.lastDate():
                            reset.push_back(d)
                            d += tenor
                        # for (d = today + tenor d < maturity.lastDate() d += tenor)
                        #     reset.push_back(d)

                        option = CliquetOption(payoff, maturity, reset)

                        refEngine = AnalyticPerformanceEngine(process)

                        mcEngine = MakeMCPRPerformanceEngine(process)
                        mcEngine.withBrownianBridge()
                        mcEngine.withAbsoluteTolerance(5.0e-3)
                        mcEngine.withSeed(42)
                        mcEngine = mcEngine.makeEngine()

                        for u in underlyings:
                            for m in qRates:
                                for n in rRates:
                                    for v in vols:
                                        q = m
                                        r = n
                                        spot.setValue(u)
                                        qRate.setValue(q)
                                        rRate.setValue(r)
                                        vol.setValue(v)

                                        option.setPricingEngine(refEngine)
                                        refValue = option.NPV()

                                        option.setPricingEngine(mcEngine)
                                        value = option.NPV()

                                        error = abs(refValue - value)
                                        tolerance = 1.5e-2
                                        self.assertFalse(error > tolerance)

    def _testOptionGreeks(self, T):
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
        moneyness = [0.9, 1.0, 1.1]
        underlyings = [100.0]
        qRates = [0.04, 0.05, 0.06]
        rRates = [0.01, 0.05, 0.15]
        lengths = [1, 2]
        frequencies = [Semiannual, Quarterly]
        vols = [0.11, 0.50, 1.20]

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

        process = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        for ty in types:
            for moneynes in moneyness:
                for length in lengths:
                    for frequencie in frequencies:

                        maturity = EuropeanExercise(today + Period(length, Years))
                        payoff = PercentageStrikePayoff(ty, moneynes)

                        reset = DateVector()
                        d = today + Period(frequencie)
                        while d < maturity.lastDate():
                            reset.push_back(d)
                            d += Period(frequencie)
                        # for (d = today + Period(frequencie) d < maturity.lastDate() d += Period(frequencie))
                        #     reset.push_back(d)

                        engine = T(process)

                        option = CliquetOption(payoff, maturity, reset)
                        option.setPricingEngine(engine)

                        for u in underlyings:
                            for m in qRates:
                                for n in rRates:
                                    for v in vols:

                                        q = m
                                        r = n
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
