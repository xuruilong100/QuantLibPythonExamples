import unittest
from utilities import *
from QuantLib import *
from math import floor


class AsianOptionTest(unittest.TestCase):
    class DiscreteAverageData(object):
        def __init__(self,
                     typeOpt,
                     underlying,
                     strike,
                     dividendYield,
                     riskFreeRate,
                     first,
                     length,
                     fixings,
                     volatility,
                     controlVariate,
                     result):
            self.typeOpt = typeOpt
            self.underlying = underlying
            self.strike = strike
            self.dividendYield = dividendYield
            self.riskFreeRate = riskFreeRate
            self.first = first
            self.length = length
            self.fixings = fixings
            self.volatility = volatility
            self.controlVariate = controlVariate
            self.result = result

    class ContinuousAverageData(object):
        def __init__(self,
                     typeOpt,
                     spot,
                     currentAverage,
                     strike,
                     dividendYield,
                     riskFreeRate,
                     volatility,
                     length,
                     elapsed,
                     result):
            self.typeOpt = typeOpt
            self.spot = spot
            self.currentAverage = currentAverage
            self.strike = strike
            self.dividendYield = dividendYield
            self.riskFreeRate = riskFreeRate
            self.volatility = volatility
            self.length = length
            self.elapsed = elapsed
            self.result = result

    class VecerData(object):
        def __init__(self,
                     spot,
                     riskFreeRate,
                     volatility,
                     strike,
                     length,
                     result,
                     tolerance):
            self.spot = spot
            self.strike = strike
            self.riskFreeRate = riskFreeRate
            self.volatility = volatility
            self.length = length
            self.result = result
            self.tolerance = tolerance

    def testAnalyticContinuousGeometricAveragePrice(self):
        TEST_MESSAGE(
            "Testing analytic continuous geometric average-price Asians...")
        # data from "Option Pricing Formulas", Haug, pag.96-97
        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(80.0)
        qRate = SimpleQuote(-0.03)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.05)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.20)
        volTS = flatVol(today, vol, dc)
        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        engine = AnalyticContinuousGeometricAveragePriceAsianEngine(
            stochProcess)

        averageType = Average.Geometric
        typeOpt = Option.Put
        strike = 85.0
        exerciseDate = today + Period(90, Days)
        pastFixings = NullSize()
        runningAccumulator = NullReal()

        payoff = PlainVanillaPayoff(typeOpt, strike)
        exercise = EuropeanExercise(exerciseDate)
        option = ContinuousAveragingAsianOption(
            averageType, payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.NPV()
        expected = 4.6922
        tolerance = 1.0e-4
        self.assertFalse(
            abs(calculated - expected) > tolerance)

        # trying to approximate the continuous version with the discrete version
        runningAccumulator = 1.0
        pastFixings = 0
        fixingDates = DateVector(exerciseDate - today + 1)
        for i in range(len(fixingDates)):
            fixingDates[i] = today + Period(i, Days)

        engine2 = AnalyticDiscreteGeometricAveragePriceAsianEngine(stochProcess)
        option2 = DiscreteAveragingAsianOption(
            averageType, runningAccumulator,
            pastFixings,
            fixingDates, payoff, exercise)
        option2.setPricingEngine(engine2)
        calculated = option2.NPV()
        tolerance = 3.0e-3

        self.assertFalse(
            abs(calculated - expected) > tolerance)

    def testAnalyticContinuousGeometricAveragePriceGreeks(self):
        TEST_MESSAGE(
            "Testing analytic continuous geometric average-price Asian greeks...")
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
        underlyings = [100.0]
        strikes = [90.0, 100.0, 110.0]
        qRates = [0.04, 0.05, 0.06]
        rRates = [0.01, 0.05, 0.15]
        lengths = [1, 2]
        vols = [0.11, 0.50, 1.20]

        dc = Actual360()
        today = Settings.instance().evaluationDate
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

        for i in range(len(types)):
            for j in range(len(strikes)):
                for k in range(len(lengths)):
                    maturity = EuropeanExercise(
                        today + Period(lengths[k], Years))
                    payoff = PlainVanillaPayoff(
                        types[i], strikes[j])
                    engine = AnalyticContinuousGeometricAveragePriceAsianEngine(process)
                    option = ContinuousAveragingAsianOption(
                        Average.Geometric, payoff, maturity)
                    option.setPricingEngine(engine)
                    pastFixings = NullSize()
                    runningAverage = NullReal()

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

                                        for ky in calculated.keys():
                                            greek = ky
                                            expct = expected[greek]
                                            calcl = calculated[greek]
                                            tol = tolerance[greek]
                                            error = relativeError(expct, calcl, u)
                                            self.assertFalse(error > tol)

    def testAnalyticContinuousGeometricAveragePriceHeston(self):
        TEST_MESSAGE("Testing analytic continuous geometric Asians under Heston...")
        # data from "Pricing of Geometric Asian Options under Heston's Stochastic
        # Volatility Model", Kim & Wee, Quantitative Finance, 14:10, 1795-1809, 2011

        # 73, 348 and 1095 are 0.2, 1.5 and 3.0 years respectively in Actual365Fixed
        days = [73, 73, 73, 73, 73, 548, 548, 548, 548, 548, 1095, 1095, 1095, 1095, 1095]
        strikes = [
            90.0, 95.0, 100.0, 105.0, 110.0, 90.0, 95.0, 100.0, 105.0, 110.0, 90.0, 95.0,
            100.0, 105.0, 110.0]

        # Prices from Table 1 (params obey Feller condition)
        prices = [
            10.6571, 6.5871, 3.4478, 1.4552, 0.4724, 16.5030, 13.7625, 11.3374, 9.2245,
            7.4122, 20.5102, 18.3060, 16.2895, 14.4531, 12.7882]

        # Prices from Table 4 (params do not obey Feller condition)
        prices_2 = [
            10.6425, 6.4362, 3.1578, 1.1936, 0.3609, 14.9955, 11.6707, 8.7767, 6.3818,
            4.5118, 18.1219, 15.2009, 12.5707, 10.2539, 8.2611]

        # 0.2 and 3.0 match to 1e-4. Unfortunatly 1.5 corresponds to 547.5 days, 547 and 548
        # bound the expected answer but are both out by ~5e-3
        tolerance = 1.0e-2
        dc = Actual365Fixed()
        today = Settings.instance().evaluationDate
        typeOpt = Option.Call
        averageType = Average.Geometric

        spot = QuoteHandle(SimpleQuote(100.0))
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.05)
        rTS = flatRate(today, rRate, dc)

        v0 = 0.09
        kappa = 1.15
        theta = 0.348
        sigma = 0.39
        rho = -0.64
        hestonProcess = HestonProcess(
            YieldTermStructureHandle(rTS),
            YieldTermStructureHandle(qTS),
            spot, v0, kappa, theta, sigma, rho)
        engine = AnalyticContinuousGeometricAveragePriceAsianHestonEngine(
            hestonProcess)

        for i in range(len(strikes)):
            strike = strikes[i]
            day = days[i]
            expected = prices[i]
            expiryDate = today + Period(day, Days)
            europeanExercise = EuropeanExercise(expiryDate)
            payoff = PlainVanillaPayoff(typeOpt, strike)
            option = ContinuousAveragingAsianOption(
                averageType, payoff, europeanExercise)
            option.setPricingEngine(engine)
            calculated = option.NPV()
            self.assertFalse(
                abs(calculated - expected) > tolerance)

        v0_2 = 0.09
        kappa_2 = 2.0
        theta_2 = 0.09
        sigma_2 = 1.0
        rho_2 = -0.3

        hestonProcess_2 = HestonProcess(
            YieldTermStructureHandle(rTS),
            YieldTermStructureHandle(qTS),
            spot, v0_2, kappa_2, theta_2, sigma_2, rho_2)
        engine_2 = AnalyticContinuousGeometricAveragePriceAsianHestonEngine(
            hestonProcess_2)

        for i in range(len(strikes)):
            strike = strikes[i]
            day = days[i]
            expected = prices_2[i]
            expiryDate = today + Period(day, Days)
            europeanExercise = EuropeanExercise(expiryDate)
            payoff = PlainVanillaPayoff(typeOpt, strike)
            option = ContinuousAveragingAsianOption(
                averageType, payoff, europeanExercise)
            option.setPricingEngine(engine_2)
            calculated = option.NPV()
            self.assertFalse(
                abs(calculated - expected) > tolerance)

    def testAnalyticDiscreteGeometricAveragePrice(self):
        TEST_MESSAGE(
            "Testing analytic discrete geometric average-price Asians...")
        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.03)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.06)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.20)
        volTS = flatVol(today, vol, dc)
        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        engine = AnalyticDiscreteGeometricAveragePriceAsianEngine(
            stochProcess)

        averageType = Average.Geometric
        runningAccumulator = 1.0
        pastFixings = 0
        futureFixings = 10
        typeOpt = Option.Call
        strike = 100.0
        payoff = PlainVanillaPayoff(typeOpt, strike)
        exerciseDate = today + Period(360, Days)
        exercise = EuropeanExercise(exerciseDate)
        fixingDates = DateVector(futureFixings)
        dt = int(360.0 / futureFixings + 0.5)
        fixingDates[0] = today + Period(dt, Days)
        for j in range(1, futureFixings):
            fixingDates[j] = fixingDates[j - 1] + Period(dt, Days)

        option = DiscreteAveragingAsianOption(
            averageType, runningAccumulator,
            pastFixings, fixingDates,
            payoff, exercise)
        option.setPricingEngine(engine)

        calculated = option.NPV()
        expected = 5.3425606635
        tolerance = 1e-10

        self.assertFalse(
            abs(calculated - expected) > tolerance)

    def testAnalyticDiscreteGeometricAveragePriceHeston(self):
        TEST_MESSAGE(
            "Testing analytic discrete geometric average-price Asians under Heston...")
        # 30-day options need wider tolerance due to uncertainty around what "weekly
        # fixing" dates mean over a 30-day month!
        tol = [
            3.0e-2, 2.0e-2, 2.0e-2, 2.0e-2, 3.0e-2, 4.0e-2, 8.0e-2, 1.0e-2,
            2.0e-2, 3.0e-2, 3.0e-2, 4.0e-2, 2.0e-2, 1.0e-2, 1.0e-2, 2.0e-2,
            3.0e-2, 4.0e-2]
        dc = Actual365Fixed()
        today = Settings.instance().evaluationDate

        spot = QuoteHandle(SimpleQuote(100.0))
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.05)
        rTS = flatRate(today, rRate, dc)

        v0 = 0.09
        kappa = 1.15
        theta = 0.0348
        sigma = 0.39
        rho = -0.64
        hestonProcess = HestonProcess(
            YieldTermStructureHandle(rTS),
            YieldTermStructureHandle(qTS),
            spot, v0, kappa, theta, sigma, rho)
        engine = AnalyticDiscreteGeometricAveragePriceAsianHestonEngine(
            hestonProcess)

        self._testDiscreteGeometricAveragePriceHeston(engine, tol)

    def testAnalyticDiscreteGeometricAverageStrike(self):
        TEST_MESSAGE(
            "Testing analytic discrete geometric average-strike Asians...")

        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.03)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.06)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.20)
        volTS = flatVol(today, vol, dc)
        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        engine = AnalyticDiscreteGeometricAverageStrikeAsianEngine(
            stochProcess)
        averageType = Average.Geometric
        runningAccumulator = 1.0
        pastFixings = 0
        futureFixings = 10
        typeOpt = Option.Call
        strike = 100.0
        payoff = PlainVanillaPayoff(typeOpt, strike)
        exerciseDate = today + Period(360, Days)
        exercise = EuropeanExercise(exerciseDate)
        fixingDates = DateVector(futureFixings)
        dt = int(360.0 / futureFixings + 0.5)
        fixingDates[0] = today + Period(dt, Days)
        for j in range(1, futureFixings):
            fixingDates[j] = fixingDates[j - 1] + Period(dt, Days)

        option = DiscreteAveragingAsianOption(
            averageType, runningAccumulator,
            pastFixings, fixingDates,
            payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.NPV()
        expected = 4.97109
        tolerance = 1e-5

        self.assertFalse(
            abs(calculated - expected) > tolerance)

    def testMCDiscreteGeometricAveragePrice(self):
        TEST_MESSAGE(
            "Testing Monte Carlo discrete geometric average-price Asians...")
        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.03)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.06)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.20)
        volTS = flatVol(today, vol, dc)
        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))
        tolerance = 4.0e-3
        engine = MCDiscreteGeometricAPEngine(
            stochProcess,
            'LowDiscrepancy',
            requiredSamples=8191)
        averageType = Average.Geometric
        runningAccumulator = 1.0
        pastFixings = 0
        futureFixings = 10
        typeOpt = Option.Call
        strike = 100.0
        payoff = PlainVanillaPayoff(typeOpt, strike)
        exerciseDate = today + Period(360, Days)
        exercise = EuropeanExercise(exerciseDate)
        fixingDates = DateVector(futureFixings)
        dt = int(360.0 / futureFixings + 0.5)
        fixingDates[0] = today + Period(dt, Days)
        for j in range(1, futureFixings):
            fixingDates[j] = fixingDates[j - 1] + Period(dt, Days)

        option = DiscreteAveragingAsianOption(
            averageType, runningAccumulator,
            pastFixings, fixingDates,
            payoff, exercise)
        option.setPricingEngine(engine)
        calculated = option.NPV()
        engine2 = AnalyticDiscreteGeometricAveragePriceAsianEngine(
            stochProcess)
        option.setPricingEngine(engine2)
        expected = option.NPV()
        self.assertFalse(abs(calculated - expected) > tolerance)

    def testMCDiscreteGeometricAveragePriceHeston(self):
        TEST_MESSAGE(
            "Testing MC discrete geometric average-price Asians under Heston...")
        # 30-day options need wider tolerance due to uncertainty around what "weekly
        # fixing" dates mean over a 30-day month!
        tol = [4.0e-2, 2.0e-2, 2.0e-2, 3.0e-2, 3.0e-2, 2.0e-2, 1.0e-1, 1.0e-2,
               2.0e-2, 2.0e-2, 2.0e-2, 1.0e-2, 2.0e-2, 1.0e-2, 1.0e-2, 1.0e-2,
               1.0e-2, 1.0e-2]
        dc = Actual365Fixed()
        today = Settings.instance().evaluationDate

        spot = QuoteHandle(SimpleQuote(100.0))
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.05)
        rTS = flatRate(today, rRate, dc)

        v0 = 0.09
        kappa = 1.15
        theta = 0.0348
        sigma = 0.39
        rho = -0.64
        hestonProcess = HestonProcess(
            YieldTermStructureHandle(rTS),
            YieldTermStructureHandle(qTS),
            spot, v0, kappa, theta, sigma, rho)
        engine = MCDiscreteGeometricAPHestonEngine(
            hestonProcess,
            'LowDiscrepancy',
            requiredSamples=65535,
            seed=43)
        self._testDiscreteGeometricAveragePriceHeston(engine, tol)

    def testMCDiscreteArithmeticAveragePrice(self):
        TEST_MESSAGE(
            "Testing Monte Carlo discrete arithmetic average-price Asians...")

        # data from "Asian Option", Levy, 1997
        # in "Exotic Options: The State of the Art",
        # edited by Clewlow, Strickland
        cases4 = [
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 2, 0.13, True, 1.3942835683),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 4, 0.13, True, 1.5852442983),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 8, 0.13, True, 1.66970673),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 12, 0.13, True, 1.6980019214),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 26, 0.13, True, 1.7255070456),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 52, 0.13, True, 1.7401553533),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 100, 0.13, True, 1.7478303712),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 250, 0.13, True, 1.7490291943),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 500, 0.13, True, 1.7515113291),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 1000, 0.13, True, 1.7537344885),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 2, 0.13, True, 1.8496053697),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 4, 0.13, True, 2.0111495205),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 8, 0.13, True, 2.0852138818),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 12, 0.13, True, 2.1105094397),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 26, 0.13, True, 2.1346526695),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 52, 0.13, True, 2.147489651),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 100, 0.13, True, 2.154728109),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 250, 0.13, True, 2.1564276565),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 500, 0.13, True, 2.1594238588),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 1000, 0.13, True, 2.1595367326),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 2, 0.13, True, 2.63315092584),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 4, 0.13, True, 2.76723962361),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 8, 0.13, True, 2.83124836881),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 12, 0.13, True, 2.84290301412),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 26, 0.13, True, 2.88179560417),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 52, 0.13, True, 2.88447044543),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 100, 0.13, True, 2.89985329603),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 250, 0.13, True, 2.90047296063),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 500, 0.13, True, 2.89813412160),
            self.DiscreteAverageData(Option.Put, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 1000, 0.13, True, 2.89703362437)]

        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.03)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.06)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.20)
        volTS = flatVol(today, vol, dc)

        averageType = Average.Arithmetic
        runningSum = 0.0
        pastFixings = 0

        for l in range(len(cases4)):
            payoff = PlainVanillaPayoff(cases4[l].typeOpt, cases4[l].strike)
            dt = cases4[l].length / (cases4[l].fixings - 1)
            timeIncrements = DoubleVector(cases4[l].fixings)
            fixingDates = DateVector(cases4[l].fixings)
            timeIncrements[0] = cases4[l].first
            fixingDates[0] = today + Period(int(timeIncrements[0] * 360 + 0.5), Days)
            for i in range(1, cases4[l].fixings):
                timeIncrements[i] = i * dt + cases4[l].first
                fixingDates[i] = today + Period(int(timeIncrements[i] * 360 + 0.5), Days)
            exercise = EuropeanExercise(fixingDates[cases4[l].fixings - 1])

            spot.setValue(cases4[l].underlying)
            qRate.setValue(cases4[l].dividendYield)
            rRate.setValue(cases4[l].riskFreeRate)
            vol.setValue(cases4[l].volatility)
            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))
            engine = MCDiscreteArithmeticAPEngine(
                stochProcess, 'LowDiscrepancy',
                requiredSamples=2047,
                controlVariate=cases4[l].controlVariate)
            option = DiscreteAveragingAsianOption(
                averageType, runningSum,
                pastFixings, fixingDates,
                payoff, exercise)
            option.setPricingEngine(engine)
            calculated = option.NPV()
            expected = cases4[l].result
            tolerance = 2.0e-2
            self.assertFalse(
                abs(calculated - expected) > tolerance)

            if cases4[l].fixings < 100:
                engine = FdBlackScholesAsianEngine(
                    stochProcess, 100, 100, 100)
                option.setPricingEngine(engine)
                calculated = option.NPV()
                self.assertFalse(
                    abs(calculated - expected) > tolerance)

    def testMCDiscreteArithmeticAveragePriceHeston(self):
        TEST_MESSAGE(
            "Testing Monte Carlo discrete arithmetic average-price Asians in Heston model...")
        # data from "A numerical method to price exotic path-dependent
        # options on an underlying described by the Heston stochastic
        # volatility model", Ballestra, Pacelli and Zirilli, Journal
        # of Banking & Finance, 2007 (section 4 - Numerical Results)
        #
        # nb. for Heston, the volatility param below is ignored
        cases = [
            self.DiscreteAverageData(Option.Call, 120.0, 100.0, 0.0, 0.05, 1.0 / 12.0, 11.0 / 12.0, 12, 0.1, False, 22.50)]
        vol = 0.3
        v0 = vol * vol
        kappa = 11.35
        theta = 0.022
        sigma = 0.618
        rho = -0.5

        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.03)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.06)
        rTS = flatRate(today, rRate, dc)

        averageType = Average.Arithmetic
        runningSum = 0.0
        pastFixings = 0

        for l in range(len(cases)):
            payoff = PlainVanillaPayoff(
                cases[l].typeOpt, cases[l].strike)
            dt = cases[l].length / (cases[l].fixings - 1)
            timeIncrements = DoubleVector(cases[l].fixings)
            fixingDates = DateVector(cases[l].fixings)
            timeIncrements[0] = cases[l].first
            fixingDates[0] = today + Period(int(timeIncrements[0] * 365.25), Days)
            for i in range(1, cases[l].fixings):
                timeIncrements[i] = i * dt + cases[l].first
                fixingDates[i] = today + Period(int(timeIncrements[i] * 365.25), Days)
            exercise = EuropeanExercise(
                fixingDates[cases[l].fixings - 1])

            spot.setValue(cases[l].underlying)
            qRate.setValue(cases[l].dividendYield)
            rRate.setValue(cases[l].riskFreeRate)

            hestonProcess = HestonProcess(
                YieldTermStructureHandle(rTS),
                YieldTermStructureHandle(qTS),
                QuoteHandle(spot),
                v0, kappa, theta, sigma, rho)

            engine = MCDiscreteArithmeticAPHestonEngine(
                hestonProcess,
                "LowDiscrepancy",
                seed=42,
                requiredSamples=32768)
            option = DiscreteAveragingAsianOption(
                averageType, runningSum,
                pastFixings, fixingDates,
                payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            expected = cases[l].result
            # Bounds given in paper, "22.48 to 22.52"
            tolerance = 2.0e-2
            self.assertFalse(
                abs(calculated - expected) > tolerance)

            # Also test the control variate version of the pricer
            engine2 = MCDiscreteArithmeticAPHestonEngine(
                hestonProcess,
                "LowDiscrepancy",
                seed=42,
                timeSteps=48,
                requiredSamples=8192,
                controlVariate=True)

            option.setPricingEngine(engine2)
            calculated = option.NPV()
            expected = cases[l].result
            tolerance = 2.50e-2
            self.assertFalse(
                abs(calculated - expected) > tolerance)

        # An additional dataset using the Heston parameters coming from "General lower
        # bounds for arithmetic Asian option prices", Applied Mathematical Finance 15(2)
        # 123-149 (2008), by Albrecher, H., Mayer, P., and Schoutens, W. The numerical
        # accuracy of prices given in Table 6 is low, but higher accuracy prices for the
        # same parameters and options are reported by in "Pricing bounds and approximations
        # for discrete arithmetic Asian options under time-changed Levy processes" by Zeng,
        # P.P., and Kwok Y.K. (2013) in Table 4.

        strikes = [60.0, 80.0, 100.0, 120.0, 140.0]
        prices = [42.5990, 29.3698, 18.2360, 10.0565, 4.9609]

        v02 = 0.0175
        kappa2 = 1.5768
        theta2 = 0.0398
        sigma2 = 0.5751
        rho2 = -0.5711

        dc2 = Actual365Fixed()
        spot2 = SimpleQuote(100.0)
        qRate2 = SimpleQuote(0.0)
        qTS2 = flatRate(today, qRate2, dc2)
        rRate2 = SimpleQuote(0.03)
        rTS2 = flatRate(today, rRate2, dc2)

        hestonProcess2 = HestonProcess(
            YieldTermStructureHandle(rTS2),
            YieldTermStructureHandle(qTS2),
            QuoteHandle(spot2),
            v02, kappa2, theta2, sigma2, rho2)

        engine3 = MCDiscreteArithmeticAPHestonEngine(
            hestonProcess2,
            "LowDiscrepancy",
            seed=42,
            timeSteps=360,
            requiredSamples=32768)
        engine4 = MCDiscreteArithmeticAPHestonEngine(
            hestonProcess2,
            "LowDiscrepancy",
            seed=42,
            timeSteps=360,
            requiredSamples=16384,
            controlVariate=True)

        fixingDates = DateVector(120)
        for i in range(1, 121):
            fixingDates[i - 1] = today + Period(i, Months)
        exercise = EuropeanExercise(fixingDates[119])

        for i in range(5):
            strike = strikes[i]
            expected = prices[i]
            payoff = PlainVanillaPayoff(Option.Call, strike)
            option = DiscreteAveragingAsianOption(
                averageType, runningSum,
                pastFixings, fixingDates,
                payoff, exercise)

            option.setPricingEngine(engine3)
            calculated = option.NPV()
            tolerance = 5.0e-2
            self.assertFalse(abs(calculated - expected) > tolerance)

            option.setPricingEngine(engine4)
            calculated = option.NPV()
            tolerance = 3.0e-2
            self.assertFalse(abs(calculated - expected) > tolerance)

    def testMCDiscreteArithmeticAverageStrike(self):
        TEST_MESSAGE(
            "Testing Monte Carlo discrete arithmetic average-strike Asians...")

        # data from "Asian Option", Levy, 1997
        # in "Exotic Options: The State of the Art",
        # edited by Clewlow, Strickland

        cases5 = [
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 2, 0.13, True, 1.51917595129),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 4, 0.13, True, 1.67940165674),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 8, 0.13, True, 1.75371215251),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 12, 0.13, True, 1.77595318693),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 26, 0.13, True, 1.81430536630),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 52, 0.13, True, 1.82269246898),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 100, 0.13, True, 1.83822402464),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 250, 0.13, True, 1.83875059026),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 500, 0.13, True, 1.83750703638),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 0.0, 11.0 / 12.0, 1000, 0.13, True, 1.83887181884),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 2, 0.13, True, 1.51154400089),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 4, 0.13, True, 1.67103508506),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 8, 0.13, True, 1.74529684070),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 12, 0.13, True, 1.76667074564),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 26, 0.13, True, 1.80528400613),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 52, 0.13, True, 1.81400883891),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 100, 0.13, True, 1.82922901451),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 250, 0.13, True, 1.82937111773),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 500, 0.13, True, 1.82826193186),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 1.0 / 12.0, 11.0 / 12.0, 1000, 0.13, True, 1.82967846654),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 2, 0.13, True, 1.49648170891),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 4, 0.13, True, 1.65443100462),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 8, 0.13, True, 1.72817806731),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 12, 0.13, True, 1.74877367895),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 26, 0.13, True, 1.78733801988),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 52, 0.13, True, 1.79624826757),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 100, 0.13, True, 1.81114186876),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 250, 0.13, True, 1.81101152587),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 500, 0.13, True, 1.81002311939),
            self.DiscreteAverageData(Option.Call, 90.0, 87.0, 0.06, 0.025, 3.0 / 12.0, 11.0 / 12.0, 1000, 0.13, True, 1.81145760308)]

        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.03)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.06)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.20)
        volTS = flatVol(today, vol, dc)

        averageType = Average.Arithmetic
        runningSum = 0.0
        pastFixings = 0

        for l in range(len(cases5)):
            payoff = PlainVanillaPayoff(
                cases5[l].typeOpt, cases5[l].strike)
            dt = cases5[l].length / (cases5[l].fixings - 1)
            timeIncrements = DoubleVector(cases5[l].fixings)
            fixingDates = DateVector(cases5[l].fixings)
            timeIncrements[0] = cases5[l].first
            fixingDates[0] = today + Period(int(timeIncrements[0] * 360 + 0.5), Days)
            for i in range(1, cases5[l].fixings):
                timeIncrements[i] = i * dt + cases5[l].first
                fixingDates[i] = today + Period(int(timeIncrements[i] * 360 + 0.5), Days)
            exercise = EuropeanExercise(
                fixingDates[cases5[l].fixings - 1])

            spot.setValue(cases5[l].underlying)
            qRate.setValue(cases5[l].dividendYield)
            rRate.setValue(cases5[l].riskFreeRate)
            vol.setValue(cases5[l].volatility)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))
            engine = MCDiscreteArithmeticASEngine(
                stochProcess,
                'LowDiscrepancy',
                seed=3456789,
                requiredSamples=1023)
            option = DiscreteAveragingAsianOption(
                averageType, runningSum,
                pastFixings, fixingDates,
                payoff, exercise)
            option.setPricingEngine(engine)

            calculated = option.NPV()
            expected = cases5[l].result
            tolerance = 2.0e-2
            self.assertFalse(
                abs(calculated - expected) > tolerance)

    def testAnalyticDiscreteGeometricAveragePriceGreeks(self):
        TEST_MESSAGE(
            "Testing discrete-averaging geometric Asian greeks...")
        baskup = SavedSettings()
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
        underlyings = [100.0]
        strikes = [90.0, 100.0, 110.0]
        qRates = [0.04, 0.05, 0.06]
        rRates = [0.01, 0.05, 0.15]
        lengths = [1, 2]
        vols = [0.11, 0.50, 1.20]

        dc = Actual360()
        today = Settings.instance().evaluationDate
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

        for i in range(len(types)):
            for j in range(len(strikes)):
                for k in range(len(lengths)):
                    maturity = EuropeanExercise(
                        today + Period(lengths[k], Years))
                    payoff = PlainVanillaPayoff(
                        types[i], strikes[j])
                    runningAverage = 120
                    pastFixings = 1
                    fixingDates = DateVector()
                    d = today + Period(3, Months)
                    while d <= maturity.lastDate():
                        fixingDates.push_back(d)
                        d = d + Period(3, Months)
                    engine = AnalyticDiscreteGeometricAveragePriceAsianEngine(
                        process)
                    option = DiscreteAveragingAsianOption(
                        Average.Geometric,
                        runningAverage, pastFixings,
                        fixingDates, payoff, maturity)
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

                                        for ky in calculated.keys():
                                            greek = ky
                                            expct = expected[greek]
                                            calcl = calculated[greek]
                                            tol = tolerance[greek]
                                            error = relativeError(expct, calcl, u)
                                            self.assertFalse(error > tol)

    def testPastFixings(self):
        TEST_MESSAGE(
            "Testing use of past fixings in Asian options...")
        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.03)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.06)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.20)
        volTS = flatVol(today, vol, dc)

        payoff = PlainVanillaPayoff(Option.Put, 100.0)
        exercise = EuropeanExercise(today + Period(1, Years))

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))

        # MC arithmetic average-price
        runningSum = 0.0
        pastFixings = 0
        fixingDates1 = DateVector()
        for i in range(13):
            fixingDates1.push_back(today + Period(i, Months))
        option1 = DiscreteAveragingAsianOption(
            Average.Arithmetic, runningSum,
            pastFixings, fixingDates1,
            payoff, exercise)

        pastFixings = 2
        runningSum = pastFixings * spot.value() * 0.8
        fixingDates2 = DateVector()
        for i in range(-2, 13):
            fixingDates2.push_back(today + Period(i, Months))
        option2 = DiscreteAveragingAsianOption(
            Average.Arithmetic, runningSum,
            pastFixings, fixingDates2,
            payoff, exercise)

        engine = MCDiscreteArithmeticAPEngine(
            stochProcess,
            "LowDiscrepancy",
            requiredSamples=2047)

        option1.setPricingEngine(engine)
        option2.setPricingEngine(engine)

        price1 = option1.NPV()
        price2 = option2.NPV()

        self.assertFalse(close(price1, price2))

    def testAllFixingsInThePast(self):
        TEST_MESSAGE(
            "SKIP",
            "Testing Asian options with all fixing dates in the past...")

    def testLevyEngine(self):
        TEST_MESSAGE(
            "Testing Levy engine for Asians options...")
        # data from Haug, "Option Pricing Formulas", p.99-100

        cases = [
            self.ContinuousAverageData(Option.Call, 6.80, 6.80, 6.90, 0.09, 0.07, 0.14, 180, 0, 0.0944),
            self.ContinuousAverageData(Option.Put, 6.80, 6.80, 6.90, 0.09, 0.07, 0.14, 180, 0, 0.2237),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 95.0, 0.05, 0.1, 0.15, 270, 0, 7.0544),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 95.0, 0.05, 0.1, 0.15, 270, 90, 5.6731),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 95.0, 0.05, 0.1, 0.15, 270, 180, 5.0806),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 95.0, 0.05, 0.1, 0.35, 270, 0, 10.1213),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 95.0, 0.05, 0.1, 0.35, 270, 90, 6.9705),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 95.0, 0.05, 0.1, 0.35, 270, 180, 5.1411),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 100.0, 0.05, 0.1, 0.15, 270, 0, 3.7845),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 100.0, 0.05, 0.1, 0.15, 270, 90, 1.9964),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 100.0, 0.05, 0.1, 0.15, 270, 180, 0.6722),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 100.0, 0.05, 0.1, 0.35, 270, 0, 7.5038),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 100.0, 0.05, 0.1, 0.35, 270, 90, 4.0687),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 100.0, 0.05, 0.1, 0.35, 270, 180, 1.4222),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 105.0, 0.05, 0.1, 0.15, 270, 0, 1.6729),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 105.0, 0.05, 0.1, 0.15, 270, 90, 0.3565),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 105.0, 0.05, 0.1, 0.15, 270, 180, 0.0004),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 105.0, 0.05, 0.1, 0.35, 270, 0, 5.4071),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 105.0, 0.05, 0.1, 0.35, 270, 90, 2.1359),
            self.ContinuousAverageData(Option.Call, 100.0, 100.0, 105.0, 0.05, 0.1, 0.35, 270, 180, 0.1552)]

        dc = Actual360()
        today = Settings.instance().evaluationDate

        for l in range(len(cases)):
            spot = SimpleQuote(cases[l].spot)
            qTS = flatRate(today, cases[l].dividendYield, dc)
            rTS = flatRate(today, cases[l].riskFreeRate, dc)
            volTS = flatVol(today, cases[l].volatility, dc)
            averageType = Average.Arithmetic
            average = SimpleQuote(cases[l].currentAverage)
            payoff = PlainVanillaPayoff(cases[l].typeOpt, cases[l].strike)

            startDate = today - Period(cases[l].elapsed, Days)
            maturity = startDate + Period(cases[l].length, Days)
            exercise = EuropeanExercise(maturity)
            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))
            engine = ContinuousArithmeticAsianLevyEngine(
                stochProcess, QuoteHandle(average), startDate)
            option = ContinuousAveragingAsianOption(
                averageType,
                payoff, exercise)
            option.setPricingEngine(engine)
            calculated = option.NPV()
            expected = cases[l].result
            tolerance = 1.0e-4
            error = abs(expected - calculated)
            self.assertFalse(error > tolerance)

    def testVecerEngine(self):
        TEST_MESSAGE("Testing Vecer engine for Asian options...")

        cases = [
            self.VecerData(1.9, 0.05, 0.5, 2.0, 1, 0.193174, 1.0e-5),
            self.VecerData(2.0, 0.05, 0.5, 2.0, 1, 0.246416, 1.0e-5),
            self.VecerData(2.1, 0.05, 0.5, 2.0, 1, 0.306220, 1.0e-4),
            self.VecerData(2.0, 0.02, 0.1, 2.0, 1, 0.055986, 2.0e-4),
            self.VecerData(2.0, 0.18, 0.3, 2.0, 1, 0.218388, 1.0e-4),
            self.VecerData(2.0, 0.0125, 0.25, 2.0, 2, 0.172269, 1.0e-4),
            self.VecerData(2.0, 0.05, 0.5, 2.0, 2, 0.350095, 2.0e-4)]

        dayCounter = Actual360()
        today = Settings.instance().evaluationDate
        typeOpt = Option.Call
        q = YieldTermStructureHandle(flatRate(today, 0.0, dayCounter))
        timeSteps = 200
        assetSteps = 200

        for i in range(len(cases)):
            u = QuoteHandle(SimpleQuote(cases[i].spot))
            r = YieldTermStructureHandle(
                flatRate(today, cases[i].riskFreeRate, dayCounter))
            sigma = BlackVolTermStructureHandle(
                flatVol(today, cases[i].volatility, dayCounter))
            process = BlackScholesMertonProcess(
                u, q, r, sigma)
            maturity = today + Period(cases[i].length * 360, Days)
            exercise = EuropeanExercise(maturity)
            payoff = PlainVanillaPayoff(typeOpt, cases[i].strike)
            average = QuoteHandle(SimpleQuote(0.0))
            option = ContinuousAveragingAsianOption(
                Average.Arithmetic, payoff, exercise)
            option.setPricingEngine(
                ContinuousArithmeticAsianVecerEngine(
                    process, average, today, timeSteps, assetSteps, -1.0, 1.0))
            calculated = option.NPV()
            error = abs(calculated - cases[i].result)
            self.assertFalse(
                error > cases[i].tolerance,
                "Failed to reproduce expected NPV")

    def _testDiscreteGeometricAveragePriceHeston(self,
                                                 engine,
                                                 tol):
        # data from "A Recursive Method for Discretely Monitored Geometric Asian Option
        # Prices", Kim, Kim, Kim & Wee, Bull. Korean Math. Soc. 53, 733-749, 2016
        days = [30, 91, 182, 365, 730, 1095, 30, 91, 182, 365, 730, 1095, 30,
                91, 182, 365, 730, 1095]
        strikes = [90, 90, 90, 90, 90, 90, 100, 100, 100, 100, 100, 100, 110,
                   110, 110, 110, 110, 110]
        # Prices from Tables 1, 2 and 3
        prices = [10.2732, 10.9554, 11.9916, 13.6950, 16.1773, 18.0146, 2.4389,
                  3.7881, 5.2132, 7.2243, 9.9948, 12.0639, 0.1012, 0.5949, 1.4444,
                  2.9479, 5.3531, 7.3315]
        dc = Actual365Fixed()
        today = Settings.instance().evaluationDate
        spot = QuoteHandle(SimpleQuote(100.0))
        qRate = SimpleQuote(0.0)
        rRate = SimpleQuote(0.05)
        v0 = 0.09
        typeOpt = Option.Call
        averageType = Average.Geometric

        runningAccumulator = 1.0
        pastFixings = 0

        for i in range(len(strikes)):

            strike = strikes[i]
            day = days[i]
            expected = prices[i]
            tolerance = tol[i]

            futureFixings = int(floor(day / 7.0))
            fixingDates = DateVector(futureFixings)
            expiryDate = today + Period(day, Days)
            for j in range(futureFixings - 1, -1, -1):
                fixingDates[j] = expiryDate - Period(j * 7, Days)

            europeanExercise = EuropeanExercise(expiryDate)
            payoff = PlainVanillaPayoff(typeOpt, strike)
            option = DiscreteAveragingAsianOption(
                averageType, runningAccumulator, pastFixings,
                fixingDates, payoff, europeanExercise)
            option.setPricingEngine(engine)
            calculated = option.NPV()
            self.assertFalse(
                abs(calculated - expected) > tolerance)
