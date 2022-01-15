import unittest
from utilities import *
from QuantLib import *


class DividendOptionTest(unittest.TestCase):

    def testEuropeanValues(self):
        TEST_MESSAGE(
            "Testing dividend European option values with no dividends...")

        backup = SavedSettings()

        tolerance = 1.0e-5

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.00, 0.10, 0.30]
        rRates = [0.01, 0.05, 0.15]
        lengths = [1, 2]
        vols = [0.05, 0.20, 0.70]

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

        for type in types:
            for strike in strikes:
                for length in lengths:
                    exDate = today + Period(length, Years)
                    exercise = EuropeanExercise(exDate)

                    dividendDates = DateVector()
                    dividends = DoubleVector()
                    d = today + Period(3, Months)

                    while d < exercise.lastDate():
                        dividendDates.push_back(d)
                        dividends.push_back(0.0)
                        d += Period(6, Months)

                    payoff = PlainVanillaPayoff(type, strike)

                    stochProcess = BlackScholesMertonProcess(
                        QuoteHandle(spot), qTS, rTS, volTS)

                    ref_engine = AnalyticEuropeanEngine(stochProcess)

                    engine = AnalyticDividendEuropeanEngine(stochProcess)

                    option = DividendVanillaOption(
                        payoff, exercise, dividendDates, dividends)
                    option.setPricingEngine(engine)

                    ref_option = VanillaOption(payoff, exercise)
                    ref_option.setPricingEngine(ref_engine)

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

                                    calculated = option.NPV()
                                    expected = ref_option.NPV()
                                    error = abs(calculated - expected)
                                    self.assertFalse(error > tolerance)

    @unittest.skip("Doesn't quite work.  Need to deal with date conventions")
    def testEuropeanKnownValue(self):
        TEST_MESSAGE(
            "Testing dividend European option values with known value...")

        # Reference pg. 253 - Hull - Options, Futures, and Other Derivatives 5th ed
        # Exercise 12.8

        backup = SavedSettings()

        tolerance = 1.0e-2
        expected = 3.67

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

        exDate = today + Period(6, Months)
        exercise = EuropeanExercise(exDate)

        dividendDates = [today + Period(2, Months), today + Period(5, Months)]
        dividends = [0.50, 0.50]

        payoff = PlainVanillaPayoff(Option.Call, 40.0)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        engine = AnalyticDividendEuropeanEngine(stochProcess)

        option = DividendVanillaOption(
            payoff, exercise, dividendDates, dividends)
        option.setPricingEngine(engine)

        u = 40.0
        q = 0.0
        r = 0.09
        v = 0.30
        spot.setValue(u)
        qRate.setValue(q)
        rRate.setValue(r)
        vol.setValue(v)

        calculated = option.NPV()
        error = abs(calculated - expected)
        self.assertFalse(error > tolerance)

    def testEuropeanStartLimit(self):
        TEST_MESSAGE(
            "Testing dividend European option with a dividend on today's date...")

        backup = SavedSettings()

        tolerance = 1.0e-5
        dividendValue = 10.0

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.00, 0.10, 0.30]
        rRates = [0.01, 0.05, 0.15]
        lengths = [1, 2]
        vols = [0.05, 0.20, 0.70]

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

        for type in types:
            for strike in strikes:
                for length in lengths:
                    exDate = today + Period(length, Years)
                    exercise = EuropeanExercise(exDate)

                    dividendDates = [today]
                    dividends = [dividendValue]

                    payoff = PlainVanillaPayoff(type, strike)

                    stochProcess = BlackScholesMertonProcess(
                        QuoteHandle(spot), qTS, rTS, volTS)

                    engine = AnalyticDividendEuropeanEngine(stochProcess)

                    ref_engine = AnalyticEuropeanEngine(stochProcess)

                    option = DividendVanillaOption(
                        payoff, exercise, dividendDates, dividends)
                    option.setPricingEngine(engine)

                    ref_option = VanillaOption(payoff, exercise)
                    ref_option.setPricingEngine(ref_engine)

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

                                    calculated = option.NPV()
                                    spot.setValue(u - dividendValue)
                                    expected = ref_option.NPV()
                                    error = abs(calculated - expected)
                                    self.assertFalse(error > tolerance)

    @unittest.skip("Doesn't quite work.  Need to use discounted values")
    def testEuropeanEndLimit(self):
        TEST_MESSAGE(
            "Testing dividend European option values with end limits...")

        backup = SavedSettings()

        tolerance = 1.0e-5
        dividendValue = 10.0

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.00, 0.10, 0.30]
        rRates = [0.01, 0.05, 0.15]
        lengths = [1, 2]
        vols = [0.05, 0.20, 0.70]

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

        for type in types:
            for strike in strikes:
                for length in lengths:
                    exDate = today + Period(length, Years)
                    exercise = EuropeanExercise(exDate)

                    dividendDates = [exercise.lastDate()]
                    dividends = [dividendValue]

                    payoff = PlainVanillaPayoff(type, strike)

                    refPayoff = PlainVanillaPayoff(type, strike + dividendValue)

                    stochProcess = BlackScholesMertonProcess(
                        QuoteHandle(spot), qTS, rTS, volTS)

                    engine = AnalyticDividendEuropeanEngine(stochProcess)

                    ref_engine = AnalyticEuropeanEngine(stochProcess)

                    option = DividendVanillaOption(
                        payoff, exercise, dividendDates, dividends)
                    option.setPricingEngine(engine)

                    ref_option = VanillaOption(refPayoff, exercise)
                    ref_option.setPricingEngine(ref_engine)

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

                                    calculated = option.NPV()
                                    expected = ref_option.NPV()
                                    error = abs(calculated - expected)
                                    if error > tolerance:
                                        self.assertFalse(error > tolerance)

    def testEuropeanGreeks(self):
        TEST_MESSAGE("Testing dividend European option greeks...")

        backup = SavedSettings()

        calculated = dict()
        expected = dict()
        tolerance = dict()
        tolerance["delta"] = 1.0e-5
        tolerance["gamma"] = 1.0e-5
        tolerance["theta"] = 1.0e-5
        tolerance["rho"] = 1.0e-5
        tolerance["vega"] = 1.0e-5

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.00, 0.10, 0.30]
        rRates = [0.01, 0.05, 0.15]
        lengths = [1, 2]
        vols = [0.05, 0.20, 0.40]

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

        for type in types:
            for strike in strikes:
                for length in lengths:
                    exDate = today + Period(length, Years)
                    exercise = EuropeanExercise(exDate)

                    dividendDates = DateVector()
                    dividends = DoubleVector()

                    d = today + Period(3, Months)
                    while d < exercise.lastDate():
                        dividendDates.push_back(d)
                        dividends.push_back(5.0)
                        d += Period(6, Months)

                    payoff = PlainVanillaPayoff(type, strike)

                    stochProcess = BlackScholesMertonProcess(
                        QuoteHandle(spot), qTS, rTS, volTS)

                    engine = AnalyticDividendEuropeanEngine(stochProcess)

                    option = DividendVanillaOption(payoff, exercise, dividendDates, dividends)
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

                                        # perturb risk-free rate and get rho
                                        dr = r * 1.0e-4
                                        rRate.setValue(r + dr)
                                        value_p = option.NPV()
                                        rRate.setValue(r - dr)
                                        value_m = option.NPV()
                                        rRate.setValue(r)
                                        expected["rho"] = (value_p - value_m) / (2 * dr)

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

    def testFdEuropeanValues(self):
        TEST_MESSAGE(
            "Testing finite-difference dividend European option values...")

        backup = SavedSettings()

        tolerance = 1.0e-2
        gridPoints = 400
        timeSteps = 40

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.00, 0.10, 0.30]
        rRates = [0.01, 0.05, 0.15]
        lengths = [1, 2]
        vols = [0.05, 0.20, 0.40]

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

        for type in types:
            for strike in strikes:
                for length in lengths:
                    exDate = today + Period(length, Years)
                    exercise = EuropeanExercise(exDate)

                    dividendDates = DateVector()
                    dividends = DoubleVector()
                    d = today + Period(3, Months)
                    while d < exercise.lastDate():
                        dividendDates.push_back(d)
                        dividends.push_back(5.0)
                        d += Period(6, Months)

                    payoff = PlainVanillaPayoff(type, strike)

                    stochProcess = BlackScholesMertonProcess(
                        QuoteHandle(spot), qTS, rTS, volTS)

                    engine = MakeFdBlackScholesVanillaEngine(stochProcess)
                    engine.withTGrid(timeSteps)
                    engine.withXGrid(gridPoints)
                    engine.withCashDividendModel(FdBlackScholesVanillaEngine.Escrowed)
                    engine = engine.makeEngine()

                    ref_engine = AnalyticDividendEuropeanEngine(stochProcess)

                    option = DividendVanillaOption(payoff, exercise, dividendDates, dividends)
                    option.setPricingEngine(engine)

                    ref_option = DividendVanillaOption(payoff, exercise, dividendDates, dividends)
                    ref_option.setPricingEngine(ref_engine)

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
                                    # FLOATING_POINT_EXCEPTION
                                    calculated = option.NPV()
                                    if calculated > spot.value() * 1.0e-5:
                                        expected = ref_option.NPV()
                                        error = abs(calculated - expected)
                                        self.assertFalse(error > tolerance)

    def testFdEuropeanGreeks(self):
        TEST_MESSAGE(
            "Testing finite-differences dividend European option greeks...")

        backup = SavedSettings()

        today = Date.todaysDate()
        Settings.instance().evaluationDate = today
        lengths = [1, 2]

        for length in lengths:
            exDate = today + Period(length, Years)
            exercise = EuropeanExercise(exDate)
            self._testFdGreeks(today, exercise, FdBlackScholesVanillaEngine.Spot)
            self._testFdGreeks(today, exercise, FdBlackScholesVanillaEngine.Escrowed)

    def testFdAmericanGreeks(self):
        TEST_MESSAGE(
            "Testing finite-differences dividend American option greeks...")

        backup = SavedSettings()

        today = Date.todaysDate()
        Settings.instance().evaluationDate = today
        lengths = [1, 2]

        for length in lengths:
            exDate = today + Period(length, Years)
            exercise = AmericanExercise(today, exDate)
            self._testFdGreeks(today, exercise, FdBlackScholesVanillaEngine.Spot)

    def testFdEuropeanDegenerate(self):
        TEST_MESSAGE(
            "Testing degenerate finite-differences dividend European option...")

        backup = SavedSettings()

        today = Date(27, February, 2005)
        Settings.instance().evaluationDate = today
        exDate = Date(13, April, 2005)

        exercise = EuropeanExercise(exDate)

        self._testFdDegenerate(today, exercise, FdBlackScholesVanillaEngine.Spot)
        self._testFdDegenerate(today, exercise, FdBlackScholesVanillaEngine.Escrowed)

    def testFdAmericanDegenerate(self):
        TEST_MESSAGE(
            "Testing degenerate finite-differences dividend American option...")

        backup = SavedSettings()

        today = Date(27, February, 2005)
        Settings.instance().evaluationDate = today
        exDate = Date(13, April, 2005)

        exercise = AmericanExercise(today, exDate)

        self._testFdDegenerate(today, exercise, FdBlackScholesVanillaEngine.Spot)
        self._testFdDegenerate(today, exercise, FdBlackScholesVanillaEngine.Escrowed)

    def testFdEuropeanWithDividendToday(self):
        TEST_MESSAGE(
            "Testing finite-differences dividend European option with dividend on today's date...")

        backup = SavedSettings()

        today = Date(27, February, 2005)
        Settings.instance().evaluationDate = today
        exDate = Date(13, April, 2005)

        exercise = EuropeanExercise(exDate)

        self._testFdDividendAtTZero(today, exercise, FdBlackScholesVanillaEngine.Spot)
        self._testFdDividendAtTZero(today, exercise, FdBlackScholesVanillaEngine.Escrowed)

    def testFdAmericanWithDividendToday(self):
        TEST_MESSAGE(
            "Testing finite-differences dividend American option with dividend on today's date...")

        backup = SavedSettings()

        today = Date(27, February, 2005)
        Settings.instance().evaluationDate = today
        exDate = Date(13, April, 2005)

        exercise = AmericanExercise(today, exDate)

        self._testFdDividendAtTZero(today, exercise, FdBlackScholesVanillaEngine.Spot)

    def testEscrowedDividendModel(self):
        TEST_MESSAGE("Testing finite-difference European engine "
                     "with the escrowed dividend model...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(12, October, 2019)

        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        qTS = YieldTermStructureHandle(flatRate(today, 0.063, dc))
        rTS = YieldTermStructureHandle(flatRate(today, 0.094, dc))
        volTS = BlackVolTermStructureHandle(flatVol(today, 0.3, dc))

        maturity = today + Period(1, Years)

        process = BlackScholesMertonProcess(
            spot, qTS, rTS, volTS)

        payoff = PlainVanillaPayoff(Option.Put, spot.currentLink().value())

        exercise = EuropeanExercise(maturity)

        dividendDates = [today + Period(3, Months), today + Period(9, Months)]
        dividendAmounts = [8.3, 6.8]

        option = DividendVanillaOption(
            payoff, exercise, dividendDates, dividendAmounts)

        option.setPricingEngine(
            AnalyticDividendEuropeanEngine(process))

        analyticNPV = option.NPV()
        analyticDelta = option.delta()
        engine = MakeFdBlackScholesVanillaEngine(process)
        engine.withTGrid(50)
        engine.withXGrid(200)
        engine.withDampingSteps(1)
        engine.withCashDividendModel(FdBlackScholesVanillaEngine.Escrowed)
        engine = engine.makeEngine()

        option.setPricingEngine(
            engine)

        pdeNPV = option.NPV()
        pdeDelta = option.delta()

        tol = 0.0025
        self.assertFalse(abs(pdeNPV - analyticNPV) > tol)
        self.assertFalse(abs(pdeDelta - analyticDelta) > tol)

    def _testFdGreeks(
            self,
            today,
            exercise,
            # FdBlackScholesVanillaEngine.CashDividendModel
            model):
        calculated = dict()
        expected = dict()
        tolerance = dict()
        tolerance["delta"] = 5.0e-3
        tolerance["gamma"] = 7.0e-3
        # tolerance["theta"] = 1.0e-2

        types = [Option.Call, Option.Put]
        strikes = [50.0, 99.5, 100.0, 100.5, 150.0]
        underlyings = [100.0]
        qRates = [0.00, 0.10, 0.20]
        rRates = [0.01, 0.05, 0.15]
        vols = [0.05, 0.20, 0.50]

        dc = Actual365Fixed()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = YieldTermStructureHandle(flatRate(qRate, dc))
        rRate = SimpleQuote(0.0)
        rTS = YieldTermStructureHandle(flatRate(rRate, dc))
        vol = SimpleQuote(0.0)
        volTS = BlackVolTermStructureHandle(flatVol(vol, dc))

        for tp in types:
            for strike in strikes:

                dividendDates = DateVector()
                dividends = DoubleVector()
                d = today + Period(3, Months)
                while d < exercise.lastDate():
                    dividendDates.push_back(d)
                    dividends.push_back(5.0)
                    d += Period(6, Months)

                payoff = PlainVanillaPayoff(tp, strike)

                stochProcess = BlackScholesMertonProcess(
                    QuoteHandle(spot), qTS, rTS, volTS)

                engine = MakeFdBlackScholesVanillaEngine(stochProcess)
                engine.withCashDividendModel(model)
                engine = engine.makeEngine()

                option = DividendVanillaOption(payoff, exercise,
                                               dividendDates, dividends)
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

                                # FLOATING_POINT_EXCEPTION
                                value = option.NPV()
                                calculated["delta"] = option.delta()
                                calculated["gamma"] = option.gamma()

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

                                    # perturb date and get theta

                                    #     dT = dc.yearFraction(today-1, today+1)
                                    #     Settings.instance().evaluationDate = today-1
                                    #     value_m = option.NPV()
                                    #     Settings.instance().evaluationDate = today+1
                                    #     value_p = option.NPV()
                                    #     Settings.instance().evaluationDate = today
                                    #     expected["theta"] = (value_p - value_m)/dT

                                    # compare

                                    for it in calculated.keys():
                                        greek = it
                                        expct = expected[greek]
                                        calcl = calculated[greek]
                                        tol = tolerance[greek]
                                        error = relativeError(expct, calcl, u)
                                        self.assertFalse(error > tol)

    def _testFdDegenerate(
            self,
            today,
            exercise,
            # FdBlackScholesVanillaEngine.CashDividendModel
            model):
        dc = Actual360()
        spot = SimpleQuote(54.625)
        rTS = YieldTermStructureHandle(flatRate(0.052706, dc))
        qTS = YieldTermStructureHandle(flatRate(0.0, dc))
        volTS = BlackVolTermStructureHandle(flatVol(0.282922, dc))

        process = BlackScholesMertonProcess(
            QuoteHandle(spot), qTS, rTS, volTS)

        timeSteps = 100
        gridPoints = 300

        engine = MakeFdBlackScholesVanillaEngine(process)
        engine.withTGrid(timeSteps)
        engine.withXGrid(gridPoints)
        engine.withCashDividendModel(model)
        engine = engine.makeEngine()

        payoff = PlainVanillaPayoff(Option.Call, 55.0)

        tolerance = 3.0e-3

        dividends = DoubleVector()
        dividendDates = DateVector()

        option1 = DividendVanillaOption(
            payoff, exercise, dividendDates, dividends)
        option1.setPricingEngine(engine)

        refValue = option1.NPV()

        for i in range(1, 6 + 1):
            dividends.push_back(0.0)
            dividendDates.push_back(today + i)

            option = DividendVanillaOption(
                payoff, exercise, dividendDates, dividends)
            option.setPricingEngine(engine)
            value = option.NPV()

            self.assertFalse(abs(refValue - value) > tolerance)

    def _testFdDividendAtTZero(
            self,
            today,
            exercise,
            # FdBlackScholesVanillaEngine.CashDividendModel
            model):
        dc = Actual360()
        spot = SimpleQuote(54.625)
        rTS = YieldTermStructureHandle(flatRate(0.0, dc))
        volTS = BlackVolTermStructureHandle(flatVol(0.282922, dc))

        process = BlackScholesMertonProcess(
            QuoteHandle(spot), rTS, rTS, volTS)

        timeSteps = 50
        gridPoints = 400

        engine = MakeFdBlackScholesVanillaEngine(process)
        engine.withTGrid(timeSteps)
        engine.withXGrid(gridPoints)
        engine.withCashDividendModel(model)
        engine = engine.makeEngine()

        payoff = PlainVanillaPayoff(Option.Call, 55.0)

        # today's dividend must by taken into account
        dividends = DoubleVector(1, 1.0)
        dividendDates = DateVector(1, today)

        option = DividendVanillaOption(
            payoff, exercise, dividendDates, dividends)
        option.setPricingEngine(engine)
        calculated = option.NPV()

        if model == FdBlackScholesVanillaEngine.Spot:
            try:
                t = option.theta()
            except Exception as e:
                print(e)
        if model == FdBlackScholesVanillaEngine.Escrowed:
            try:
                t = option.theta()
            except Exception as e:
                print(e)

        europeanExercise = EuropeanExercise(exercise.lastDate())
        europeanOption = DividendVanillaOption(
            payoff, europeanExercise, dividendDates, dividends)

        europeanOption.setPricingEngine(
            AnalyticDividendEuropeanEngine(process))

        expected = europeanOption.NPV()

        tol = 1e-4

        self.assertFalse(abs(calculated - expected) > tol)
