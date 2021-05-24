import unittest
from utilities import *
from QuantLib import *


class AmericanOptionTest(unittest.TestCase):
    class AmericanOptionData(object):
        def __init__(self,
                     optType,
                     strike,
                     s,
                     q,
                     r,
                     t,
                     v,
                     result):
            self.optType = optType
            self.strike = strike
            self.s = s  # spot
            self.q = q  # dividend
            self.r = r  # risk - free        rate
            self.t = t  # time        to        maturity
            self.v = v  # volatility
            self.result = result  # expected        result

    def _testFdGreeks(self, Engine, testName):
        backup = SavedSettings()
        calculated = dict()
        expected = dict()
        tolerance = dict()
        tolerance["delta"] = 7.0e-4
        tolerance["gamma"] = 2.0e-4

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.04, 0.05, 0.06]
        rRates = [0.01, 0.05, 0.15]
        years = [1, 2]
        vols = [0.11, 0.50, 1.20]

        today = Date.todaysDate()
        dc = Actual360()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        for i in range(len(types)):
            for j in range(len(strikes)):
                for k in range(len(years)):
                    exDate = today + Period(years[k], Years)
                    exercise = AmericanExercise(today, exDate)
                    payoff = PlainVanillaPayoff(types[i], strikes[j])
                    stochProcess = BlackScholesMertonProcess(
                        QuoteHandle(spot), qTS, rTS, volTS)

                    engine = Engine(stochProcess)
                    option = VanillaOption(payoff, exercise)
                    option.setPricingEngine(engine)

                    for l in range(len(underlyings)):
                        for m in range(len(qRates)):
                            for n in range(len(rRates)):
                                for p in range(len(vols)):
                                    u = underlyings[l]
                                    q = qRates[m]
                                    r = rRates[n]
                                    v = vols[p]

                                    spot.setValue(u)
                                    qRate.setValue(q)
                                    rRate.setValue(r)
                                    vol.setValue(v)

                                    value = option.NPV()
                                    calculated["delta"] = option.delta()
                                    calculated["gamma"] = option.gamma()

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

                                        for greek in calculated.keys():
                                            expct = expected[greek]
                                            calcl = calculated[greek]
                                            tol = tolerance[greek]
                                            error = relativeError(expct, calcl, u)

                                            self.assertFalse(
                                                error > tol,
                                                'case {0} fails in {1}'.format(i, testName))

    def testBaroneAdesiWhaleyValues(self):
        TEST_MESSAGE(
            "Testing Barone-Adesi and Whaley approximation for American options...")

        values = [
            # type, strike, spot, q, r, t, vol, values
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.15, 0.0206),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.15, 1.8771),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.15, 10.0089),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.25, 0.3159),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.25, 3.1280),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.25, 10.3919),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.35, 0.9495),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.35, 4.3777),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.35, 11.1679),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.15, 0.8208),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.15, 4.0842),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.15, 10.8087),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.25, 2.7437),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.25, 6.8015),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.25, 13.0170),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.35, 5.0063),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.35, 9.5106),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.35, 15.5689),
            self.AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.15, 10.0000),
            self.AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.15, 1.8770),
            self.AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.15, 0.0410),
            self.AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.25, 10.2533),
            self.AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.25, 3.1277),
            self.AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.25, 0.4562),
            self.AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.35, 10.8787),
            self.AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.35, 4.3777),
            self.AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.35, 1.2402),
            self.AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.15, 10.5595),
            self.AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.15, 4.0842),
            self.AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.15, 1.0822),
            self.AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.25, 12.4419),
            self.AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.25, 6.8014),
            self.AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.25, 3.3226),
            self.AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.35, 14.6945),
            self.AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.35, 9.5104),
            self.AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.35, 5.8823),
            self.AmericanOptionData(Option.Put, 100.00, 100.00, 0.00, 0.00, 0.50, 0.15, 4.2294)]

        today = Date.todaysDate()
        dc = Actual360()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)
        tolerance = 3.0e-3

        for i in range(len(values)):
            payoff = PlainVanillaPayoff(values[i].optType, values[i].strike)
            exDate = today + Period(int(values[i].t * 360 + 0.5), Days)
            exercise = AmericanExercise(today, exDate)

            spot.setValue(values[i].s)
            qRate.setValue(values[i].q)
            rRate.setValue(values[i].r)
            vol.setValue(values[i].v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = BaroneAdesiWhaleyApproximationEngine(stochProcess)
            option = VanillaOption(payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - values[i].result)
            self.assertFalse(
                error > tolerance,
                'case {0} fails in testBaroneAdesiWhaleyValues'.format(i))

    def testBjerksundStenslandValues(self):
        TEST_MESSAGE(
            "Testing Bjerksund and Stensland approximation, for American options...")

        values = [
            #      type, strike,   spot,    q,    r,    t,  vol,   value, tol
            # from "Option pricing formulas", Haug, McGraw-Hill 1998, pag 27
            self.AmericanOptionData(Option.Call, 40.00, 42.00, 0.08, 0.04, 0.75, 0.35, 5.2704),
            # from "Option pricing formulas", Haug, McGraw-Hill 1998, VBA code
            self.AmericanOptionData(Option.Put, 40.00, 36.00, 0.00, 0.06, 1.00, 0.20, 4.4531),
            # ATM option with very small volatility, reference value taken from R
            self.AmericanOptionData(Option.Call, 100, 100, 0.05, 0.05, 1.0, 0.0021, 0.08032314),
            # ATM option with very small volatility,
            # reference value taken from Barone-Adesi and Whaley Approximation
            self.AmericanOptionData(Option.Call, 100, 100, 0.05, 0.05, 1.0, 0.0001, 0.003860656),
            self.AmericanOptionData(Option.Call, 100, 99.99, 0.05, 0.05, 1.0, 0.0001, 0.00081),
            # ITM option with a very small volatility
            self.AmericanOptionData(Option.Call, 100, 110, 0.05, 0.05, 1.0, 0.0001, 10.0),
            self.AmericanOptionData(Option.Put, 110, 100, 0.05, 0.05, 1.0, 0.0001, 10.0),
            # ATM option with a very large volatility
            self.AmericanOptionData(Option.Put, 100, 110, 0.05, 0.05, 1.0, 10, 94.89543)]

        today = Date.todaysDate()
        dc = Actual360()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)
        tolerance = 5.0e-3

        for i in range(len(values)):
            payoff = PlainVanillaPayoff(
                values[i].optType, values[i].strike)
            exDate = today + Period(int(values[i].t * 360 + 0.5), Days)
            exercise = AmericanExercise(today, exDate)

            spot.setValue(values[i].s)
            qRate.setValue(values[i].q)
            rRate.setValue(values[i].r)
            vol.setValue(values[i].v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = BjerksundStenslandApproximationEngine(
                stochProcess)
            option = VanillaOption(payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - values[i].result)
            self.assertFalse(
                error > tolerance,
                'case {0} fails in testBjerksundStenslandValues'.format(i))

    def testJuValues(self):
        TEST_MESSAGE("Testing Ju approximation for American options...")

        values = [
            #        type, strike,   spot,    q,    r,    t,     vol,   value, tol
            # These values are from Exhibit 3 - Short dated Put Options
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 0.006),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 0.201),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 0.433),

            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 0.851),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 1.576),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 1.984),

            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 5.000),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 5.084),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 5.260),

            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 0.078),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 0.697),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 1.218),

            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 1.309),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 2.477),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 3.161),

            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 5.059),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 5.699),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 6.231),

            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 0.247),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 1.344),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 2.150),

            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 1.767),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 3.381),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 4.342),

            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 5.288),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 6.501),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 7.367),

            # Type in Exhibits 4 and 5 if you have some spare time -)

            #        type, strike,   spot,    q,    r,    t,     vol,   value, tol
            # values from Exhibit 6 - Long dated Call Options with dividends
            self.AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.03, 3.0, 0.2, 2.605),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.03, 3.0, 0.2, 5.182),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.03, 3.0, 0.2, 9.065),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.03, 3.0, 0.2, 14.430),
            self.AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.03, 3.0, 0.2, 21.398),

            self.AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.03, 3.0, 0.4, 11.336),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.03, 3.0, 0.4, 15.711),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.03, 3.0, 0.4, 20.760),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.03, 3.0, 0.4, 26.440),
            self.AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.03, 3.0, 0.4, 32.709),

            self.AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.00001, 3.0, 0.3, 5.552),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.00001, 3.0, 0.3, 8.868),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.00001, 3.0, 0.3, 13.158),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.00001, 3.0, 0.3, 18.458),
            self.AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.00001, 3.0, 0.3, 24.786),

            self.AmericanOptionData(Option.Call, 100.00, 80.00, 0.03, 0.07, 3.0, 0.3, 12.177),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.03, 0.07, 3.0, 0.3, 17.411),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.03, 0.07, 3.0, 0.3, 23.402),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.03, 0.07, 3.0, 0.3, 30.028),
            self.AmericanOptionData(Option.Call, 100.00, 120.00, 0.03, 0.07, 3.0, 0.3, 37.177)]

        today = Date.todaysDate()
        dc = Actual360()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        tolerance = 1.0e-3

        for i in range(len(values)):
            payoff = PlainVanillaPayoff(
                values[i].optType, values[i].strike)
            exDate = today + Period(int(values[i].t * 360 + 0.5), Days)
            exercise = AmericanExercise(today, exDate)

            spot.setValue(values[i].s)
            qRate.setValue(values[i].q)
            rRate.setValue(values[i].r)
            vol.setValue(values[i].v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = JuQuadraticApproximationEngine(
                stochProcess)
            option = VanillaOption(payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - values[i].result)
            self.assertFalse(
                error > tolerance,
                'case {0} fails in testJuValues'.format(i))

    def testFdValues(self):
        TEST_MESSAGE("Testing finite-difference engine, for American options...")

        values = [
            #        type, strike,   spot,    q,    r,    t,     vol,   value, tol
            # These values are from Exhibit 3 - Short dated Put Options
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 0.006),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 0.201),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 0.433),

            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 0.851),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 1.576),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 1.984),

            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 5.000),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 5.084),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 5.260),

            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 0.078),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 0.697),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 1.218),

            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 1.309),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 2.477),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 3.161),

            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 5.059),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 5.699),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 6.231),

            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 0.247),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 1.344),
            self.AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 2.150),

            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 1.767),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 3.381),
            self.AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 4.342),

            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 5.288),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 6.501),
            self.AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 7.367),

            # Type in Exhibits 4 and 5 if you have some spare time -)

            #        type, strike,   spot,    q,    r,    t,     vol,   value, tol
            # values from Exhibit 6 - Long dated Call Options with dividends
            self.AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.03, 3.0, 0.2, 2.605),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.03, 3.0, 0.2, 5.182),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.03, 3.0, 0.2, 9.065),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.03, 3.0, 0.2, 14.430),
            self.AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.03, 3.0, 0.2, 21.398),

            self.AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.03, 3.0, 0.4, 11.336),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.03, 3.0, 0.4, 15.711),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.03, 3.0, 0.4, 20.760),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.03, 3.0, 0.4, 26.440),
            self.AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.03, 3.0, 0.4, 32.709),

            self.AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.00001, 3.0, 0.3, 5.552),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.00001, 3.0, 0.3, 8.868),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.00001, 3.0, 0.3, 13.158),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.00001, 3.0, 0.3, 18.458),
            self.AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.00001, 3.0, 0.3, 24.786),

            self.AmericanOptionData(Option.Call, 100.00, 80.00, 0.03, 0.07, 3.0, 0.3, 12.177),
            self.AmericanOptionData(Option.Call, 100.00, 90.00, 0.03, 0.07, 3.0, 0.3, 17.411),
            self.AmericanOptionData(Option.Call, 100.00, 100.00, 0.03, 0.07, 3.0, 0.3, 23.402),
            self.AmericanOptionData(Option.Call, 100.00, 110.00, 0.03, 0.07, 3.0, 0.3, 30.028),
            self.AmericanOptionData(Option.Call, 100.00, 120.00, 0.03, 0.07, 3.0, 0.3, 37.177)]

        today = Date.todaysDate()
        dc = Actual360()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        tolerance = 8.0e-2

        for i in range(len(values)):
            payoff = PlainVanillaPayoff(
                values[i].optType, values[i].strike)
            exDate = today + Period(int(values[i].t * 360 + 0.5), Days)
            exercise = AmericanExercise(today, exDate)

            spot.setValue(values[i].s)
            qRate.setValue(values[i].q)
            rRate.setValue(values[i].r)
            vol.setValue(values[i].v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = FdBlackScholesVanillaEngine(
                stochProcess, 100, 100)
            option = VanillaOption(payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - values[i].result)
            self.assertFalse(
                error > tolerance,
                'case {0} fails in testFdValues'.format(i))

    def testFdAmericanGreeks(self):
        TEST_MESSAGE("Testing finite-differences American option greeks...")
        self._testFdGreeks(
            FdBlackScholesVanillaEngine, 'testFdAmericanGreeks')

    def testFdShoutGreeks(self):
        TEST_MESSAGE("Testing finite-differences shout option greeks...")
        self._testFdGreeks(
            FDCNShoutEngine, 'testFdShoutGreeks')
