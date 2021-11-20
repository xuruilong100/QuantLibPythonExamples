import unittest
from utilities import *
from QuantLib import *
from math import exp


class ForwardOptionData(object):
    def __init__(self,
                 optType,
                 moneyness,
                 s,
                 q,
                 r,
                 start,
                 t,
                 v,
                 result,
                 tol):
        self.type = optType
        self.moneyness = moneyness
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.start = start  # time to reset
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.result = result  # expected result
        self.tol = tol  # tolerance


class ForwardOptionTest(unittest.TestCase):
    def testValues(self):
        TEST_MESSAGE("Testing forward option values...")

        # The data below are from
        # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998        
        values = [
            # type, moneyness, spot,  div, rate,start,   t,  vol, result, tol
            # "Option pricing formulas", pag. 37
            ForwardOptionData(Option.Call, 1.1, 60.0, 0.04, 0.08, 0.25, 1.0, 0.30, 4.4064, 1.0e-4),
            # "Option pricing formulas", VBA code
            ForwardOptionData(Option.Put, 1.1, 60.0, 0.04, 0.08, 0.25, 1.0, 0.30, 8.2971, 1.0e-4)
        ]

        dc = Actual360()
        today = Date(16, Sep, 2015)
        Settings.instance().evaluationDate = today

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = ForwardEuropeanEngine(stochProcess)

        for value in values:
            payoff = PlainVanillaPayoff(value.type, 0.0)
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)
            reset = today + timeToDays(value.start)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            option = ForwardVanillaOption(value.moneyness, reset, payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = 1e-4
            self.assertFalse(error > tolerance)

    def testGreeks(self):
        TEST_MESSAGE("Testing forward option greeks...")

        backup = SavedSettings()

        self._testForwardGreeks(ForwardEuropeanEngine)

    def testPerformanceValues(self):
        TEST_MESSAGE("Testing forward performance option values...")

        # The data below are the performance equivalent of the
        # forward options tested above and taken from
        # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998        
        values = [
            # type, moneyness, spot,  div, rate,start, maturity,  vol,                       result, tol
            ForwardOptionData(Option.Call, 1.1, 60.0, 0.04, 0.08, 0.25, 1.0, 0.30, 4.4064 / 60 * exp(-0.04 * 0.25), 1.0e-4),
            ForwardOptionData(Option.Put, 1.1, 60.0, 0.04, 0.08, 0.25, 1.0, 0.30, 8.2971 / 60 * exp(-0.04 * 0.25), 1.0e-4)
        ]

        dc = Actual360()
        today = Date(16, Sep, 2015)
        Settings.instance().evaluationDate = today

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = ForwardPerformanceEuropeanEngine(
            stochProcess)

        for value in values:
            payoff = PlainVanillaPayoff(value.type, 0.0)
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)
            reset = today + timeToDays(value.start)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            option = ForwardVanillaOption(value.moneyness, reset, payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            error = abs(calculated - value.result)
            tolerance = 1e-4
            self.assertFalse(error > tolerance)

    def testPerformanceGreeks(self):
        TEST_MESSAGE("Testing forward performance option greeks...")

        backup = SavedSettings()

        self._testForwardGreeks(ForwardPerformanceEuropeanEngine)

    @unittest.skip("not implemented")
    def testGreeksInitialization(self):
        TEST_MESSAGE(
            "Testing forward option greeks initialization...")

    def testMCPrices(self):
        TEST_MESSAGE("Testing forward option MC prices...")

        tol = [0.002, 0.001, 0.0006, 5e-4, 5e-4]

        timeSteps = 100
        numberOfSamples = 5000
        mcSeed = 42

        q = 0.04
        r = 0.01
        sigma = 0.11
        s = 100

        dc = Actual360()
        backup = SavedSettings()
        today = Date(16, Sep, 2015)
        Settings.instance().evaluationDate = today

        spot = SimpleQuote(s)
        qRate = SimpleQuote(q)
        qTS = YieldTermStructureHandle(flatRate(qRate, dc))
        rRate = SimpleQuote(r)
        rTS = YieldTermStructureHandle(flatRate(rRate, dc))
        vol = SimpleQuote(sigma)
        volTS = BlackVolTermStructureHandle(flatVol(vol, dc))

        stochProcess = BlackScholesMertonProcess(QuoteHandle(spot), qTS, rTS, volTS)

        analyticEngine = ForwardEuropeanEngine(stochProcess)

        mcEngine = MakeMCPRForwardEuropeanBSEngine(stochProcess)
        mcEngine.withSteps(timeSteps)
        mcEngine.withSamples(numberOfSamples)
        mcEngine.withSeed(mcSeed)
        mcEngine = mcEngine.makeEngine()

        exDate = today + Period(1, Years)
        exercise = EuropeanExercise(exDate)
        reset = today + Period(6, Months)
        payoff = PlainVanillaPayoff(Option.Call, 0.0)

        moneyness = [0.8, 0.9, 1.0, 1.1, 1.2]

        for moneyness_index in range(len(moneyness)):
            option = ForwardVanillaOption(moneyness[moneyness_index], reset, payoff, exercise)

            option.setPricingEngine(analyticEngine)
            analyticPrice = option.NPV()

            option.setPricingEngine(mcEngine)
            mcPrice = option.NPV()

            error = relativeError(analyticPrice, mcPrice, s)
            self.assertFalse(error > tol[moneyness_index])

    def testHestonMCPrices(self):
        TEST_MESSAGE("Testing forward option Heston MC prices...")

        optionTypes = [Option.Call, Option.Put]

        mcForwardStartTolerance = [
            [7e-4,  # Call, moneyness=0.8
             8e-4,  # Call, moneyness=0.9
             6e-4,  # Call, moneyness=1.0
             5e-4,  # Call, moneyness=1.1
             5e-4],  # Call, moneyness=1.2
            [6e-4,  # Put, moneyness=0.8
             5e-4,  # Put, moneyness=0.9
             6e-4,  # Put, moneyness=1.0
             0.001,  # Put, moneyness=1.1
             0.001]];  # Put, moneyness=1.2

        tol = [[9e-4,  # Call, moneyness=0.8
                9e-4,  # Call, moneyness=0.9
                6e-4,  # Call, moneyness=1.0
                5e-4,  # Call, moneyness=1.1
                5e-4],  # Call, moneyness=1.2
               [6e-4,  # Put, moneyness=0.8
                5e-4,  # Put, moneyness=0.9
                8e-4,  # Put, moneyness=1.0
                0.002,  # Put, moneyness=1.1
                0.002]];  # Put, moneyness=1.2

        for type_index in range(len(optionTypes)):

            mcTolerance = 5e-4
            analyticTolerance = 5e-4

            timeSteps = 50
            numberOfSamples = 4095
            mcSeed = 42

            q = 0.04
            r = 0.01
            sigma_bs = 0.245
            s = 100

            # Test 1: Set up an equivalent flat Heston and compare to analytical BS pricing
            v0 = sigma_bs * sigma_bs
            kappa = 1e-8
            theta = sigma_bs * sigma_bs
            sigma = 1e-8
            rho = -0.93

            dc = Actual360()
            backup = SavedSettings()
            today = Date(16, Sep, 2015)
            Settings.instance().evaluationDate = today

            exDate = today + Period(1, Years)
            exercise = EuropeanExercise(exDate)
            reset = today + Period(6, Months)
            payoff = PlainVanillaPayoff(optionTypes[type_index], 0.0)

            spot = SimpleQuote(s)
            qRate = SimpleQuote(q)
            qTS = YieldTermStructureHandle(flatRate(qRate, dc))
            rRate = SimpleQuote(r)
            rTS = YieldTermStructureHandle(flatRate(rRate, dc))
            vol = SimpleQuote(sigma_bs)
            volTS = BlackVolTermStructureHandle(flatVol(vol, dc))

            bsProcess = BlackScholesMertonProcess(
                QuoteHandle(spot), qTS, rTS, volTS)

            analyticEngine = ForwardEuropeanEngine(bsProcess)

            hestonProcess = HestonProcess(
                rTS, qTS, QuoteHandle(spot), v0, kappa, theta, sigma, rho)

            mcEngine = MakeMCLDForwardEuropeanHestonEngine(hestonProcess)
            mcEngine.withSteps(timeSteps)
            mcEngine.withSamples(numberOfSamples)
            mcEngine.withSeed(mcSeed)
            mcEngine = mcEngine.makeEngine()

            moneyness = [0.8, 0.9, 1.0, 1.1, 1.2]

            for moneyness_index in range(len(moneyness)):
                option = ForwardVanillaOption(moneyness[moneyness_index], reset, payoff, exercise)

                option.setPricingEngine(analyticEngine)
                analyticPrice = option.NPV()

                option.setPricingEngine(mcEngine)
                mcPrice = option.NPV()

                mcError = relativeError(analyticPrice, mcPrice, s)
                self.assertFalse(mcError > mcForwardStartTolerance[type_index][moneyness_index])

            # Test 2: Using an arbitrary Heston model, check that prices match semi-analytical
            # Heston prices when reset date is t=0
            v0 = sigma_bs * sigma_bs
            kappa = 1.0
            theta = 0.08
            sigma = 0.39
            rho = -0.93

            reset = today

            hestonProcessSmile = HestonProcess(rTS, qTS, QuoteHandle(spot), v0, kappa, theta, sigma, rho)

            hestonModel = HestonModel(hestonProcessSmile)

            analyticHestonEngine = AnalyticHestonEngine(hestonModel, 96)

            mcEngineSmile = MakeMCLDForwardEuropeanHestonEngine(hestonProcessSmile)
            mcEngineSmile.withSteps(timeSteps)
            mcEngineSmile.withSamples(numberOfSamples)
            mcEngineSmile.withSeed(mcSeed)
            mcEngineSmile = mcEngineSmile.makeEngine()

            analyticForwardHestonEngine = AnalyticHestonForwardEuropeanEngine(hestonProcessSmile)

            for moneyness_index in range(len(moneyness)):
                strike = s * moneyness[moneyness_index]
                vanillaPayoff = PlainVanillaPayoff(optionTypes[type_index], strike)

                vanillaOption = VanillaOption(vanillaPayoff, exercise)
                forwardOption = ForwardVanillaOption(moneyness[moneyness_index], reset, payoff, exercise)

                vanillaOption.setPricingEngine(analyticHestonEngine)
                analyticPrice = vanillaOption.NPV()

                forwardOption.setPricingEngine(mcEngineSmile)
                mcPrice = forwardOption.NPV()

                mcError = relativeError(analyticPrice, mcPrice, s)
                tolerance = tol[type_index][moneyness_index]
                self.assertFalse(mcError > tolerance)

                # T=0, testing the Analytic Pricer's T=0 analytical solution
                forwardOption.setPricingEngine(analyticForwardHestonEngine)
                hestonAnalyticPrice = forwardOption.NPV()

                analyticError = relativeError(analyticPrice, hestonAnalyticPrice, s)
                self.assertFalse(analyticError > analyticTolerance)

    def testHestonAnalyticalVsMCPrices(self):
        TEST_MESSAGE("Testing Heston analytic vs MC prices...")

        optionTypes = [Option.Call, Option.Put]

        tol = [[0.002,  # Call, moneyness=0.8, CV:false
                0.002,  # Call, moneyness=0.8, CV:true
                0.001,  # Call, moneyness=1.0, CV:false
                0.001,  # Call, moneyness=1.8, CV:true
                0.001,  # Call, moneyness=1.2, CV:false
                0.001],  # Call, moneyness=1.2, CV:true
               [0.001,  # Put, moneyness=0.8, CV:false
                0.001,  # Put, moneyness=0.8, CV:true
                0.003,  # Put, moneyness=1.0, CV:false
                0.003,  # Put, moneyness=1.0, CV:true
                0.003,  # Put, moneyness=1.2, CV:false
                0.003]]  # Put, moneyness=1.2, CV:true

        for option_type_index in range(len(optionTypes)):

            timeSteps = 50
            numberOfSamples = 5000
            mcSeed = 42

            q = 0.03
            r = 0.005
            s = 100

            vol = 0.3
            v0 = vol * vol
            kappa = 11.35
            theta = 0.022
            sigma = 0.618
            rho = -0.5

            dc = Actual360()
            backup = SavedSettings()
            today = Date(16, Sep, 2015)
            Settings.instance().evaluationDate = today

            exDate = today + Period(1, Years)
            exercise = EuropeanExercise(exDate)
            reset = today + Period(6, Months)
            payoff = PlainVanillaPayoff(optionTypes[option_type_index], 0.0)

            spot = SimpleQuote(s)
            qRate = SimpleQuote(q)
            qTS = YieldTermStructureHandle(flatRate(qRate, dc))
            rRate = SimpleQuote(r)
            rTS = YieldTermStructureHandle(flatRate(rRate, dc))

            hestonProcess = HestonProcess(
                rTS, qTS, QuoteHandle(spot), v0, kappa, theta, sigma, rho)

            mcEngine = MakeMCPRForwardEuropeanHestonEngine(hestonProcess)
            mcEngine.withSteps(timeSteps)
            mcEngine.withSamples(numberOfSamples)
            mcEngine.withSeed(mcSeed)
            mcEngine = mcEngine.makeEngine()

            mcEngineCv = MakeMCPRForwardEuropeanHestonEngine(hestonProcess)
            mcEngineCv.withSteps(timeSteps)
            mcEngineCv.withSamples(numberOfSamples)
            mcEngineCv.withSeed(mcSeed)
            mcEngineCv.withControlVariate(True)
            mcEngineCv = mcEngineCv.makeEngine()

            analyticEngine = AnalyticHestonForwardEuropeanEngine(hestonProcess)

            moneyness = [0.8, 1.0, 1.2]

            tol_2nd_index = 0

            while tol_2nd_index < len(moneyness):
                m = moneyness[tol_2nd_index]
                option = ForwardVanillaOption(m, reset, payoff, exercise)

                option.setPricingEngine(analyticEngine)
                analyticPrice = option.NPV()

                option.setPricingEngine(mcEngine)
                mcPrice = option.NPV()
                error = relativeError(analyticPrice, mcPrice, s)
                tolerance = tol[option_type_index][tol_2nd_index]
                self.assertFalse(error > tolerance)

                option.setPricingEngine(mcEngineCv)
                mcPriceCv = option.NPV()
                errorCv = relativeError(analyticPrice, mcPriceCv, s)
                tol_2nd_index += 1
                tolerance = tol[option_type_index][tol_2nd_index]
                tol_2nd_index += 1
                self.assertFalse(errorCv > tolerance)

    def _testForwardGreeks(self, Engine):

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
        startMonths = [6, 9]
        vols = [0.11, 0.50, 1.20]

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

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = Engine(stochProcess)

        for optType in types:
            for moneynes in moneyness:
                for length in lengths:
                    for startMonth in startMonths:

                        exDate = today + Period(length, Years)
                        exercise = EuropeanExercise(exDate)

                        reset = today + Period(startMonth, Months)

                        payoff = PlainVanillaPayoff(optType, 0.0)

                        option = ForwardVanillaOption(
                            moneynes, reset, payoff, exercise)
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
                                            dT = dc.yearFraction(today - Period(1, Days), today + Period(1, Days))
                                            Settings.instance().evaluationDate = today - Period(1, Days)
                                            value_m = option.NPV()
                                            Settings.instance().evaluationDate = today + Period(1, Days)
                                            value_p = option.NPV()
                                            Settings.instance().evaluationDate = today
                                            expected["theta"] = (value_p - value_m) / dT

                                            # compare
                                            # std.map<std.string, Real>.iterator it
                                            for it in calculated.keys():
                                                greek = it
                                                expct = expected[greek]
                                                calcl = calculated[greek]
                                                tol = tolerance[greek]
                                                error = relativeError(expct, calcl, u)
                                                self.assertFalse(error > tol)
