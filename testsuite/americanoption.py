import unittest
from utilities import *
from QuantLib import *


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


class AmericanOptionTest(unittest.TestCase):

    def _testFdGreeks(self,
                      Engine,
                      testName):
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

                                            self.assertFalse(error > tol)

    def testBaroneAdesiWhaleyValues(self):
        TEST_MESSAGE(
            "Testing Barone-Adesi and Whaley approximation for American options...")

        values = [
            # type, strike, spot, q, r, t, vol, values
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.15, 0.0206),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.15, 1.8771),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.15, 10.0089),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.25, 0.3159),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.25, 3.1280),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.25, 10.3919),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.35, 0.9495),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.35, 4.3777),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.35, 11.1679),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.15, 0.8208),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.15, 4.0842),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.15, 10.8087),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.25, 2.7437),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.25, 6.8015),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.25, 13.0170),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.35, 5.0063),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.35, 9.5106),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.35, 15.5689),
            AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.15, 10.0000),
            AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.15, 1.8770),
            AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.15, 0.0410),
            AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.25, 10.2533),
            AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.25, 3.1277),
            AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.25, 0.4562),
            AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.35, 10.8787),
            AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.35, 4.3777),
            AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.35, 1.2402),
            AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.15, 10.5595),
            AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.15, 4.0842),
            AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.15, 1.0822),
            AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.25, 12.4419),
            AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.25, 6.8014),
            AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.25, 3.3226),
            AmericanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.35, 14.6945),
            AmericanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.35, 9.5104),
            AmericanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.35, 5.8823),
            AmericanOptionData(Option.Put, 100.00, 100.00, 0.00, 0.00, 0.50, 0.15, 4.2294)]

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
            self.assertFalse(error > tolerance)

    def testBjerksundStenslandValues(self):
        TEST_MESSAGE(
            "Testing Bjerksund and Stensland approximation, for American options...")

        values = [
            #      type, strike,   spot,    q,    r,    t,  vol,   value, tol
            # from "Option pricing formulas", Haug, McGraw-Hill 1998, pag 27
            AmericanOptionData(Option.Call, 40.00, 42.00, 0.08, 0.04, 0.75, 0.35, 5.2704),
            # from "Option pricing formulas", Haug, McGraw-Hill 1998, VBA code
            AmericanOptionData(Option.Put, 40.00, 36.00, 0.00, 0.06, 1.00, 0.20, 4.4531),
            # ATM option with very small volatility, reference value taken from R
            AmericanOptionData(Option.Call, 100, 100, 0.05, 0.05, 1.0, 0.0021, 0.08032314),
            # ATM option with very small volatility,
            # reference value taken from Barone-Adesi and Whaley Approximation
            AmericanOptionData(Option.Call, 100, 100, 0.05, 0.05, 1.0, 0.0001, 0.003860656),
            AmericanOptionData(Option.Call, 100, 99.99, 0.05, 0.05, 1.0, 0.0001, 0.00081),
            # ITM option with a very small volatility
            AmericanOptionData(Option.Call, 100, 110, 0.05, 0.05, 1.0, 0.0001, 10.0),
            AmericanOptionData(Option.Put, 110, 100, 0.05, 0.05, 1.0, 0.0001, 10.0),
            # ATM option with a very large volatility
            AmericanOptionData(Option.Put, 100, 110, 0.05, 0.05, 1.0, 10, 94.89543)]

        today = Date.todaysDate()
        dc = Actual360()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)
        tolerance = 5.0e-5

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
            self.assertFalse(error > tolerance)

    def testJuValues(self):
        TEST_MESSAGE("Testing Ju approximation for American options...")

        values = [
            #        type, strike,   spot,    q,    r,    t,     vol,   value, tol
            # These values are from Exhibit 3 - Short dated Put Options
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 0.006),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 0.201),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 0.433),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 0.851),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 1.576),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 1.984),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 5.000),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 5.084),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 5.260),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 0.078),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 0.697),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 1.218),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 1.309),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 2.477),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 3.161),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 5.059),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 5.699),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 6.231),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 0.247),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 1.344),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 2.150),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 1.767),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 3.381),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 4.342),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 5.288),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 6.501),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 7.367),

            # Type in Exhibits 4 and 5 if you have some spare time -)

            #        type, strike,   spot,    q,    r,    t,     vol,   value, tol
            # values from Exhibit 6 - Long dated Call Options with dividends
            AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.03, 3.0, 0.2, 2.605),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.03, 3.0, 0.2, 5.182),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.03, 3.0, 0.2, 9.065),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.03, 3.0, 0.2, 14.430),
            AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.03, 3.0, 0.2, 21.398),
            AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.03, 3.0, 0.4, 11.336),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.03, 3.0, 0.4, 15.711),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.03, 3.0, 0.4, 20.760),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.03, 3.0, 0.4, 26.440),
            AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.03, 3.0, 0.4, 32.709),
            AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.00001, 3.0, 0.3, 5.552),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.00001, 3.0, 0.3, 8.868),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.00001, 3.0, 0.3, 13.158),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.00001, 3.0, 0.3, 18.458),
            AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.00001, 3.0, 0.3, 24.786),
            AmericanOptionData(Option.Call, 100.00, 80.00, 0.03, 0.07, 3.0, 0.3, 12.177),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.03, 0.07, 3.0, 0.3, 17.411),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.03, 0.07, 3.0, 0.3, 23.402),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.03, 0.07, 3.0, 0.3, 30.028),
            AmericanOptionData(Option.Call, 100.00, 120.00, 0.03, 0.07, 3.0, 0.3, 37.177)]

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
            self.assertFalse(error > tolerance)

    def testFdValues(self):
        TEST_MESSAGE("Testing finite-difference engine, for American options...")

        values = [
            #        type, strike,   spot,    q,    r,    t,     vol,   value, tol
            # These values are from Exhibit 3 - Short dated Put Options
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 0.006),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 0.201),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 0.433),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 0.851),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 1.576),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 1.984),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.2, 5.000),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.2, 5.084),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.2, 5.260),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 0.078),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 0.697),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 1.218),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 1.309),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 2.477),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 3.161),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.3, 5.059),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.3, 5.699),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.3, 6.231),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 0.247),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 1.344),
            AmericanOptionData(Option.Put, 35.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 2.150),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 1.767),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 3.381),
            AmericanOptionData(Option.Put, 40.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 4.342),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.0833, 0.4, 5.288),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.3333, 0.4, 6.501),
            AmericanOptionData(Option.Put, 45.00, 40.00, 0.0, 0.0488, 0.5833, 0.4, 7.367),

            # Type in Exhibits 4 and 5 if you have some spare time -)

            #        type, strike,   spot,    q,    r,    t,     vol,   value, tol
            # values from Exhibit 6 - Long dated Call Options with dividends
            AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.03, 3.0, 0.2, 2.605),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.03, 3.0, 0.2, 5.182),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.03, 3.0, 0.2, 9.065),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.03, 3.0, 0.2, 14.430),
            AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.03, 3.0, 0.2, 21.398),
            AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.03, 3.0, 0.4, 11.336),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.03, 3.0, 0.4, 15.711),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.03, 3.0, 0.4, 20.760),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.03, 3.0, 0.4, 26.440),
            AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.03, 3.0, 0.4, 32.709),
            AmericanOptionData(Option.Call, 100.00, 80.00, 0.07, 0.00001, 3.0, 0.3, 5.552),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.07, 0.00001, 3.0, 0.3, 8.868),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.07, 0.00001, 3.0, 0.3, 13.158),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.07, 0.00001, 3.0, 0.3, 18.458),
            AmericanOptionData(Option.Call, 100.00, 120.00, 0.07, 0.00001, 3.0, 0.3, 24.786),
            AmericanOptionData(Option.Call, 100.00, 80.00, 0.03, 0.07, 3.0, 0.3, 12.177),
            AmericanOptionData(Option.Call, 100.00, 90.00, 0.03, 0.07, 3.0, 0.3, 17.411),
            AmericanOptionData(Option.Call, 100.00, 100.00, 0.03, 0.07, 3.0, 0.3, 23.402),
            AmericanOptionData(Option.Call, 100.00, 110.00, 0.03, 0.07, 3.0, 0.3, 30.028),
            AmericanOptionData(Option.Call, 100.00, 120.00, 0.03, 0.07, 3.0, 0.3, 37.177)]

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
            self.assertFalse(error > tolerance)

    def testFdAmericanGreeks(self):
        TEST_MESSAGE("Testing finite-differences American option greeks...")
        self._testFdGreeks(
            FdBlackScholesVanillaEngine, 'testFdAmericanGreeks')

    def testFdShoutGreeks(self):
        TEST_MESSAGE("Testing finite-differences shout option greeks...")
        self._testFdGreeks(
            FdBlackScholesShoutEngine, 'testFdShoutGreeks')

    def testFDShoutNPV(self):
        TEST_MESSAGE("Testing finite-differences shout option pricing...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(4, February, 2021)
        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        q = YieldTermStructureHandle(flatRate(0.03, dc))
        r = YieldTermStructureHandle(flatRate(0.06, dc))

        volTS = BlackVolTermStructureHandle(flatVol(0.25, dc))
        process = BlackScholesMertonProcess(
            spot, q, r, volTS)

        maturityDate = today + Period(5, Years)

        class TestDescription(object):
            def __init__(self, strike, type, expected):
                self.strike = strike
                self.type = type
                self.expected = expected

        testDescriptions = [
            TestDescription(105, Option.Put, 19.136),
            TestDescription(105, Option.Call, 28.211),
            TestDescription(120, Option.Put, 28.02),
            TestDescription(80, Option.Call, 40.785)]

        engine = FdBlackScholesShoutEngine(
            process, 400, 200)

        for desc in testDescriptions:
            strike = desc.strike
            type = desc.type

            option = VanillaOption(
                PlainVanillaPayoff(type, strike),
                AmericanExercise(maturityDate))

            option.setPricingEngine(engine)

            expected = desc.expected
            tol = 2e-2
            calculated = option.NPV()
            diff = abs(calculated - expected)

            self.assertFalse(diff > tol)

    def testZeroVolFDShoutNPV(self):
        TEST_MESSAGE("Testing zero volatility shout option pricing with discrete dividends...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(14, February, 2021)
        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        q = YieldTermStructureHandle(flatRate(0.03, dc))
        r = YieldTermStructureHandle(flatRate(0.07, dc))

        volTS = BlackVolTermStructureHandle(flatVol(1e-6, dc))
        process = BlackScholesMertonProcess(
            spot, q, r, volTS)

        maturityDate = today + Period(1, Years)
        dividendDate = today + Period(3, Months)

        option = DividendVanillaOption(
            PlainVanillaPayoff(Option.Put, 100.0),
            AmericanExercise(today, maturityDate),
            [dividendDate],
            [10.0])

        option.setPricingEngine(
            FdBlackScholesVanillaEngine(process, 50, 50))

        americanNPV = option.NPV()

        option.setPricingEngine(
            FdBlackScholesShoutEngine(process, 50, 50))

        shoutNPV = option.NPV()
        df = r.discount(maturityDate) / r.discount(dividendDate)

        tol = 1e-3
        diff = abs(americanNPV - shoutNPV / df)

        self.assertFalse(diff > tol)

    def testLargeDividendShoutNPV(self):
        TEST_MESSAGE("Testing zero strike shout option pricing with discrete dividends...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(21, February, 2021)
        Settings.instance().evaluationDate = today

        s0 = 100.0
        vol = 0.25

        q = YieldTermStructureHandle(flatRate(0.00, dc))
        r = YieldTermStructureHandle(flatRate(0.00, dc))
        vTS = BlackVolTermStructureHandle(flatVol(vol, dc))

        process = BlackScholesMertonProcess(
            QuoteHandle(SimpleQuote(s0)), q, r, vTS)

        maturityDate = today + Period(6, Months)
        dividendDate = today + Period(3, Months)
        divAmount = 30.0

        strike = 80.0
        divOption = DividendVanillaOption(
            PlainVanillaPayoff(Option.Call, strike),
            AmericanExercise(today, maturityDate),
            [dividendDate],
            [divAmount])

        divOption.setPricingEngine(
            FdBlackScholesShoutEngine(process, 100, 400))

        calculated = divOption.NPV()

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, strike),
            AmericanExercise(today, dividendDate))

        option.setPricingEngine(
            FdBlackScholesShoutEngine(process, 100, 400))

        expected = option.NPV() * r.discount(maturityDate) / r.discount(dividendDate)

        tol = 5e-2
        diff = abs(expected - calculated)

        self.assertFalse(diff > tol)

    def testEscrowedVsSpotAmericanOption(self):
        TEST_MESSAGE("Testing escrowed vs spot dividend model for American options...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(27, February, 2021)
        Settings.instance().evaluationDate = today

        vol = SimpleQuote(0.3)

        process = BlackScholesMertonProcess(
            QuoteHandle(SimpleQuote(100)),
            YieldTermStructureHandle(flatRate(0.08, dc)),
            YieldTermStructureHandle(flatRate(0.04, dc)),
            BlackVolTermStructureHandle(flatVol(vol, dc)))

        maturityDate = today + Period(12, Months)
        dividendDate = today + Period(10, Months)
        divAmount = 10.0

        strike = 100.0
        option = DividendVanillaOption(
            PlainVanillaPayoff(Option.Call, strike),
            AmericanExercise(today, maturityDate),
            [dividendDate],
            [divAmount])

        option.setPricingEngine(
            FdBlackScholesVanillaEngine(process, 100, 400))

        spotNpv = option.NPV()
        spotDelta = option.delta()

        vol.setValue(100 / 90. * 0.3)

        engine = MakeFdBlackScholesVanillaEngine(process)
        engine.withTGrid(100)
        engine.withXGrid(400)
        engine.withCashDividendModel(FdBlackScholesVanillaEngine.Escrowed)

        engine = engine.makeEngine()

        option.setPricingEngine(engine)

        escrowedNpv = option.NPV()
        escrowedDelta = option.delta()

        diffNpv = abs(escrowedNpv - spotNpv)
        tol = 1e-2

        self.assertFalse(diffNpv > tol)

        diffDelta = abs(escrowedDelta - spotDelta)

        self.assertFalse(diffDelta > tol)

    def testTodayIsDividendDate(self):
        TEST_MESSAGE("Testing escrowed vs spot dividend model on dividend dates for American options...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(27, February, 2021)
        Settings.instance().evaluationDate = today

        vol = SimpleQuote(0.3)

        process = BlackScholesMertonProcess(
            QuoteHandle(SimpleQuote(100)),
            YieldTermStructureHandle(flatRate(0.05, dc)),
            YieldTermStructureHandle(flatRate(0.07, dc)),
            BlackVolTermStructureHandle(flatVol(vol, dc)))

        maturityDate = today + Period(12, Months)
        divDate1 = today
        divDate2 = today + Period(11, Months)
        divAmount = 5.0

        spotEngine = FdBlackScholesVanillaEngine(process, 100, 400)

        escrowedEngine = MakeFdBlackScholesVanillaEngine(process)
        escrowedEngine.withTGrid(100)
        escrowedEngine.withXGrid(400)
        escrowedEngine.withCashDividendModel(FdBlackScholesVanillaEngine.Escrowed)

        escrowedEngine = escrowedEngine.makeEngine()

        strike = 90.0
        option = DividendVanillaOption(
            PlainVanillaPayoff(Option.Put, strike),
            AmericanExercise(today, maturityDate),
            [divDate1, divDate2],
            [divAmount, divAmount])

        option.setPricingEngine(spotEngine)

        spotNpv = option.NPV()
        spotDelta = option.delta()

        vol.setValue(100 / 95. * 0.3)

        option.setPricingEngine(escrowedEngine)

        escrowedNpv = option.NPV()
        escrowedDelta = option.delta()

        diffNpv = abs(escrowedNpv - spotNpv)
        tol = 5e-2

        self.assertFalse(diffNpv > tol)

        diffDelta = abs(escrowedDelta - spotDelta)

        tol = 1e-3
        self.assertFalse(diffDelta > tol)

        optionTomorrow = DividendVanillaOption(
            PlainVanillaPayoff(Option.Put, strike),
            AmericanExercise(today, maturityDate),
            [today + Period(1, Days), divDate2],
            [divAmount, divAmount])

        vol.setValue(0.3)

        optionTomorrow.setPricingEngine(spotEngine)
        spotNpv = optionTomorrow.NPV()

        vol.setValue(100 / 95.0 * 0.3)
        optionTomorrow.setPricingEngine(escrowedEngine)

        escrowedNpv = optionTomorrow.NPV()

        diffNpv = abs(escrowedNpv - spotNpv)
        tol = 5e-2

        self.assertFalse(diffNpv > tol)
