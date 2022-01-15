import unittest
from utilities import *
from QuantLib import *
from math import exp


class DigitalOptionData(object):
    def __init__(self,
                 typeOpt,
                 strike,
                 s,
                 q,
                 r,
                 t,
                 v,
                 result,
                 tol,
                 knockin):
        self.typeOpt = typeOpt
        self.strike = strike
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.result = result  # expected result
        self.tol = tol  # tolerance
        self.knockin = knockin  # true if knock-in


class DigitalOptionTest(unittest.TestCase):

    def testCashOrNothingEuropeanValues(self):
        TEST_MESSAGE("Testing European cash-or-nothing digital option...")

        values = [
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 - pag 88
            #        type, strike,  spot,    q,    r,    t,  vol,  value, tol
            DigitalOptionData(Option.Put, 80.00, 100.0, 0.06, 0.06, 0.75, 0.35, 2.6710, 1e-4, true)]

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
            payoff = CashOrNothingPayoff(value.typeOpt, value.strike, 10.0)

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

            opt = VanillaOption(payoff, exercise)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testAssetOrNothingEuropeanValues(self):
        TEST_MESSAGE("Testing European asset-or-nothing digital option...")

        # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 - pag 90
        values = [
            #        type, strike, spot,    q,    r,    t,  vol,   value, tol
            DigitalOptionData(Option.Put, 65.00, 70.0, 0.05, 0.07, 0.50, 0.27, 20.2069, 1e-4, true)]

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
            payoff = AssetOrNothingPayoff(value.typeOpt, value.strike)

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

            opt = VanillaOption(payoff, exercise)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testGapEuropeanValues(self):
        TEST_MESSAGE("Testing European gap digital option...")

        # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 - pag 88
        values = [
            #        type, strike, spot,    q,    r,    t,  vol,   value, tol
            DigitalOptionData(Option.Call, 50.00, 50.0, 0.00, 0.09, 0.50, 0.20, -0.0053, 1e-4, true)]

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
            payoff = GapPayoff(value.typeOpt, value.strike, 57.00)

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

            opt = VanillaOption(payoff, exercise)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testCashAtHitOrNothingAmericanValues(self):
        TEST_MESSAGE("Testing American cash-(at-hit)-or-nothing "
                     "digital option...")

        values = [
            #        type, strike,   spot,    q,    r,   t,  vol,   value, tol
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 - pag 95, case 1,2
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 9.7264, 1e-4, true),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 11.6553, 1e-4, true),
            # the following cases are not taken from a reference paper or book
            # in the money options (guaranteed immediate payoff)
            DigitalOptionData(Option.Call, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 15.0000, 1e-16, true),
            DigitalOptionData(Option.Put, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 15.0000, 1e-16, true),
            # non null dividend (cross-tested with MC simulation)
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.20, 0.10, 0.5, 0.20, 12.2715, 1e-4, true),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.20, 0.10, 0.5, 0.20, 8.9109, 1e-4, true),
            DigitalOptionData(Option.Call, 100.00, 105.00, 0.20, 0.10, 0.5, 0.20, 15.0000, 1e-16, true),
            DigitalOptionData(Option.Put, 100.00, 95.00, 0.20, 0.10, 0.5, 0.20, 15.0000, 1e-16, true)]

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
            payoff = CashOrNothingPayoff(value.typeOpt, value.strike, 15.00)

            exDate = today + timeToDays(value.t)
            amExercise = AmericanExercise(today, exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))
            engine = AnalyticDigitalAmericanEngine(stochProcess)

            opt = VanillaOption(payoff, amExercise)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testAssetAtHitOrNothingAmericanValues(self):
        TEST_MESSAGE("Testing American asset-(at-hit)-or-nothing "
                     "digital option...")

        values = [
            #        type, strike,   spot,    q,    r,   t,  vol,   value, tol
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 - pag 95, case 3,4
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 64.8426, 1e-04, true),  # Haug value is wrong here, Haug VBA code is right
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 77.7017, 1e-04, true),  # Haug value is wrong here, Haug VBA code is right
            # data from Haug VBA code results
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.01, 0.10, 0.5, 0.20, 65.7811, 1e-04, true),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.01, 0.10, 0.5, 0.20, 76.8858, 1e-04, true),
            # in the money options  (guaranteed immediate payoff = spot)
            DigitalOptionData(Option.Call, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 105.0000, 1e-16, true),
            DigitalOptionData(Option.Put, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 95.0000, 1e-16, true),
            DigitalOptionData(Option.Call, 100.00, 105.00, 0.01, 0.10, 0.5, 0.20, 105.0000, 1e-16, true),
            DigitalOptionData(Option.Put, 100.00, 95.00, 0.01, 0.10, 0.5, 0.20, 95.0000, 1e-16, true)]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.04)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.01)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.25)
        volTS = flatVol(today, vol, dc)

        for value in values:
            payoff = AssetOrNothingPayoff(value.typeOpt, value.strike)

            exDate = today + timeToDays(value.t)
            amExercise = AmericanExercise(today, exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))
            engine = AnalyticDigitalAmericanEngine(stochProcess)

            opt = VanillaOption(payoff, amExercise)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testCashAtExpiryOrNothingAmericanValues(self):
        TEST_MESSAGE("Testing American cash-(at-expiry)-or-nothing "
                     "digital option...")

        values = [
            #        type, strike,   spot,    q,    r,   t,  vol,   value, tol
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 - pag 95, case 5,6,9,10
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 9.3604, 1e-4, true),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 11.2223, 1e-4, true),
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 4.9081, 1e-4, false),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 3.0461, 1e-4, false),
            # in the money options (guaranteed discounted payoff)
            DigitalOptionData(Option.Call, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 15.0000 * exp(-0.05), 1e-12, true),
            DigitalOptionData(Option.Put, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 15.0000 * exp(-0.05), 1e-12, true),
            # out of bonds case
            DigitalOptionData(Option.Call, 2.37, 2.33, 0.07, 0.43, 0.19, 0.005, 0.0000, 1e-4, false)]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.04)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.01)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.25)
        volTS = flatVol(today, vol, dc)

        for value in values:

            payoff = CashOrNothingPayoff(value.typeOpt, value.strike, 15.0)

            exDate = today + timeToDays(value.t)
            amExercise = AmericanExercise(today, exDate, true)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            if value.knockin:
                engine = AnalyticDigitalAmericanEngine(stochProcess)
            else:
                engine = AnalyticDigitalAmericanKOEngine(stochProcess)

            opt = VanillaOption(payoff, amExercise)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testAssetAtExpiryOrNothingAmericanValues(self):
        TEST_MESSAGE("Testing American asset-(at-expiry)-or-nothing "
                     "digital option...")

        values = [
            #        type, strike,   spot,    q,    r,   t,  vol,   value, tol
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 - pag 95, case 7,8,11,12
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 64.8426, 1e-04, true),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 77.7017, 1e-04, true),
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 40.1574, 1e-04, false),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 17.2983, 1e-04, false),
            # data from Haug VBA code results
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.01, 0.10, 0.5, 0.20, 65.5291, 1e-04, true),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.01, 0.10, 0.5, 0.20, 76.5951, 1e-04, true),
            # in the money options (guaranteed discounted payoff = forward * riskFreeDiscount
            #                                                    = spot * dividendDiscount)
            DigitalOptionData(Option.Call, 100.00, 105.00, 0.00, 0.10, 0.5, 0.20, 105.0000, 1e-12, true),
            DigitalOptionData(Option.Put, 100.00, 95.00, 0.00, 0.10, 0.5, 0.20, 95.0000, 1e-12, true),
            DigitalOptionData(Option.Call, 100.00, 105.00, 0.01, 0.10, 0.5, 0.20, 105.0000 * exp(-0.005), 1e-12, true),
            DigitalOptionData(Option.Put, 100.00, 95.00, 0.01, 0.10, 0.5, 0.20, 95.0000 * exp(-0.005), 1e-12, true)]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.04)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.01)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.25)
        volTS = flatVol(today, vol, dc)

        for value in values:

            payoff = AssetOrNothingPayoff(value.typeOpt, value.strike)

            exDate = today + timeToDays(value.t)
            amExercise = AmericanExercise(today, exDate, true)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            if value.knockin:
                engine = AnalyticDigitalAmericanEngine(stochProcess)
            else:
                engine = AnalyticDigitalAmericanKOEngine(stochProcess)

            opt = VanillaOption(payoff, amExercise)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testCashAtHitOrNothingAmericanGreeks(self):
        TEST_MESSAGE("Testing American cash-(at-hit)-or-nothing "
                     "digital option greeks...")

        backup = SavedSettings()

        calculated = dict()
        expected = dict()
        tolerance = dict()
        tolerance["delta"] = 5.0e-5
        tolerance["gamma"] = 5.0e-5
        # tolerance["theta"]  = 5.0e-5
        tolerance["rho"] = 5.0e-5
        # tolerance["divRho"] = 5.0e-5
        # tolerance["vega"]   = 5.0e-5

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.5, 150.0]
        cashPayoff = 100.0
        underlyings = [100]
        qRates = [0.04, 0.05, 0.06]
        rRates = [0.01, 0.05, 0.15]
        vols = [0.11, 0.5, 1.2]

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

        # there is no cycling on different residual times
        exDate = today + 360
        exercise = EuropeanExercise(exDate)
        amExercise = AmericanExercise(today, exDate, false)
        exercises = [exercise, amExercise]

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        euroEngine = AnalyticEuropeanEngine(stochProcess)

        amEngine = AnalyticDigitalAmericanEngine(stochProcess)

        engines = [euroEngine, amEngine]

        knockin = true
        for j in range(len(engines)):
            for type in types:
                for strike in strikes:
                    payoff = CashOrNothingPayoff(type, strike, cashPayoff)

                    opt = VanillaOption(payoff, exercises[j])
                    opt.setPricingEngine(engines[j])

                    for u in underlyings:
                        for q in qRates:
                            for r in rRates:
                                for v in vols:
                                    # test data
                                    spot.setValue(u)
                                    qRate.setValue(q)
                                    rRate.setValue(r)
                                    vol.setValue(v)

                                    # theta, dividend rho and vega are not available for
                                    # digital option with american exercise. Greeks of
                                    # digital options with european payoff are tested
                                    # in the europeanoption.cpp test
                                    value = opt.NPV()
                                    calculated["delta"] = opt.delta()
                                    calculated["gamma"] = opt.gamma()
                                    # calculated["theta"]  = opt.theta()
                                    calculated["rho"] = opt.rho()
                                    # calculated["divRho"] = opt.dividendRho()
                                    # calculated["vega"]   = opt.vega()

                                    if value > 1.0e-6:
                                        # perturb spot and get delta and gamma
                                        du = u * 1.0e-4
                                        spot.setValue(u + du)
                                        value_p = opt.NPV()
                                        delta_p = opt.delta()
                                        spot.setValue(u - du)
                                        value_m = opt.NPV()
                                        delta_m = opt.delta()
                                        spot.setValue(u)
                                        expected["delta"] = (value_p - value_m) / (2 * du)
                                        expected["gamma"] = (delta_p - delta_m) / (2 * du)

                                        # perturb rates and get rho and dividend rho
                                        dr = r * 1.0e-4
                                        rRate.setValue(r + dr)
                                        value_p = opt.NPV()
                                        rRate.setValue(r - dr)
                                        value_m = opt.NPV()
                                        rRate.setValue(r)
                                        expected["rho"] = (value_p - value_m) / (2 * dr)

                                        # Spread dq = q*1.0e-4
                                        # qRate.setValue(q+dq)
                                        # value_p = opt.NPV()
                                        # qRate.setValue(q-dq)
                                        # value_m = opt.NPV()
                                        # qRate.setValue(q)
                                        # expected["divRho"] = (value_p - value_m)/(2*dq)

                                        # # perturb volatility and get vega
                                        # dv = v*1.0e-4
                                        # vol.setValue(v+dv)
                                        # value_p = opt.NPV()
                                        # vol.setValue(v-dv)
                                        # value_m = opt.NPV()
                                        # vol.setValue(v)
                                        # expected["vega"] = (value_p - value_m)/(2*dv)

                                        # # perturb date and get theta
                                        # dT = dc.yearFraction(today-1, today+1)
                                        # Settings.instance().setEvaluationDate(today-1)
                                        # value_m = opt.NPV()
                                        # Settings.instance().setEvaluationDate(today+1)
                                        # value_p = opt.NPV()
                                        # Settings.instance().setEvaluationDate(today)
                                        # expected["theta"] = (value_p - value_m)/dT

                                        # check
                                        for it in calculated.keys():
                                            greek = it
                                            expct = expected[greek]
                                            calcl = calculated[greek]
                                            tol = tolerance[greek]
                                            error = relativeError(expct, calcl, value)
                                            self.assertFalse(error > tol)

    def testMCCashAtHit(self):
        TEST_MESSAGE("Testing Monte Carlo cash-(at-hit)-or-nothing "
                     "American engine...")

        backup = SavedSettings()

        values = [
            #        type, strike,   spot,    q,    r,   t,  vol,   value, tol
            DigitalOptionData(Option.Put, 100.00, 105.00, 0.20, 0.10, 0.5, 0.20, 12.2715, 1e-2, true),
            DigitalOptionData(Option.Call, 100.00, 95.00, 0.20, 0.10, 0.5, 0.20, 8.9109, 1e-2, true)]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        timeStepsPerYear = 90
        maxSamples = 1000000
        seed = 1

        for value in values:
            payoff = CashOrNothingPayoff(value.typeOpt, value.strike, 15.0)
            exDate = today + timeToDays(value.t)
            amExercise = AmericanExercise(today, exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            requiredSamples = int(pow(2.0, 14) - 1)
            mcldEngine = MakeMCLDDigitalEngine(stochProcess)
            mcldEngine.withStepsPerYear(timeStepsPerYear)
            mcldEngine.withBrownianBridge()
            mcldEngine.withSamples(requiredSamples)
            mcldEngine.withMaxSamples(maxSamples)
            mcldEngine.withSeed(seed)
            mcldEngine = mcldEngine.makeEngine()

            opt = VanillaOption(payoff, amExercise)
            opt.setPricingEngine(mcldEngine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)
