import unittest
from utilities import *
from QuantLib import *
from math import sqrt, exp, sin


class HestonModelData(object):
    def __init__(self,
                 name,
                 v0,
                 kappa,
                 theta,
                 sigma,
                 rho,
                 r,
                 q):
        self.name = name
        self.v0 = v0
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.r = r
        self.q = q


hestonModels = [
    # ADI finite difference schemes for option pricing in the
    # Heston model with correlation, K.J. in t'Hout and S. Foulon,
    HestonModelData("'t Hout case 1", 0.04, 1.5, 0.04, 0.3, -0.9, 0.025, 0.0),
    HestonModelData("'t Hout case 2", 0.12, 3.0, 0.12, 0.04, 0.6, 0.01, 0.04),
    HestonModelData("'t Hout case 3", 0.0707, 0.6067, 0.0707, 0.2928, -0.7571, 0.03, 0.0),
    HestonModelData("'t Hout case 4", 0.06, 2.5, 0.06, 0.5, -0.1, 0.0507, 0.0469),
    # Efficient numerical methods for pricing American options under
    # stochastic volatility, Samuli Ikonen and Jari Toivanen,
    HestonModelData("Ikonen-Toivanen", 0.0625, 5, 0.16, 0.9, 0.1, 0.1, 0.0),
    # Not-so-complex logarithms in the Heston model,
    # Christian Kahl and Peter Jäckel
    HestonModelData("Kahl-Jaeckel", 0.16, 1.0, 0.16, 2.0, -0.8, 0.0, 0.0),
    # self defined test cases
    HestonModelData("Equity case", 0.07, 2.0, 0.04, 0.55, -0.8, 0.03, 0.035),
    HestonModelData("high correlation", 0.07, 1.0, 0.04, 0.55, 0.995, 0.02, 0.04),
    HestonModelData("low Vol-Of-Vol", 0.07, 1.0, 0.04, 0.001, -0.75, 0.04, 0.03),
    HestonModelData("kappaEqSigRho", 0.07, 0.4, 0.04, 0.5, 0.8, 0.03, 0.03)]


class HullWhiteModelData(object):
    def __init__(self, name, a, sigma):
        self.name = name
        self.a = a
        self.sigma = sigma


hullWhiteModels = [
    HullWhiteModelData("EUR-2003", 0.00883, 0.00631)]


class SchemeData(object):
    def __init__(self, name, schemeDesc):
        self.name = name
        self.schemeDesc = schemeDesc


schemes = [
    SchemeData("HV2", FdmSchemeDesc.Hundsdorfer()),
    SchemeData("HV1", FdmSchemeDesc.ModifiedHundsdorfer()),
    SchemeData("CS", FdmSchemeDesc.CraigSneyd()),
    SchemeData("MCS", FdmSchemeDesc.ModifiedCraigSneyd()),
    SchemeData("DS", FdmSchemeDesc.Douglas())]


def makeHestonProcess(params):
    spot = QuoteHandle(SimpleQuote(100))

    dayCounter = Actual365Fixed()
    rTS = YieldTermStructureHandle(flatRate(params.r, dayCounter))
    qTS = YieldTermStructureHandle(flatRate(params.q, dayCounter))

    return HestonProcess(
        rTS, qTS, spot, params.v0, params.kappa,
        params.theta, params.sigma, params.rho)


def makeVanillaOption(params):
    maturity = Settings.instance().evaluationDate + \
               Period(int(params.maturity * 365), Days)
    exercise = EuropeanExercise(maturity)
    payoff = PlainVanillaPayoff(params.optionType, params.strike)

    return VanillaOption(payoff, exercise)


class VanillaOptionData(object):
    def __init__(self, strike, maturity, optionType):
        self.strike = strike
        self.maturity = maturity
        self.optionType = optionType


class HybridHestonHullWhiteProcessTest(unittest.TestCase):
    def testBsmHullWhiteEngine(self):
        TEST_MESSAGE(
            "Testing European option pricing for a BSM process with one-factor Hull-White model...")

        backup = SavedSettings()

        dc = Actual365Fixed()

        today = Date(16, Sep, 2015)  # Date.todaysDate()
        maturity = today + Period(20, Years)

        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        qRate = SimpleQuote(0.04)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.0525)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))
        vol = SimpleQuote(0.25)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        hullWhiteModel = HullWhite(rTS, 0.00883, 0.00526)

        stochProcess = BlackScholesMertonProcess(spot, qTS, rTS, volTS)

        exercise = EuropeanExercise(maturity)

        fwd = spot.value() * qTS.discount(maturity) / rTS.discount(maturity)
        payoff = PlainVanillaPayoff(Option.Call, fwd)

        option = EuropeanOption(payoff, exercise)

        tol = 1e-8
        corr = [-0.75, -0.25, 0.0, 0.25, 0.75]
        expectedVol = [
            0.217064577, 0.243995801,
            0.256402830, 0.268236596, 0.290461343]

        for i in range(len(corr)):
            bsmhwEngine = AnalyticBSMHullWhiteEngine(
                corr[i], stochProcess, hullWhiteModel)

            option.setPricingEngine(bsmhwEngine)
            npv = option.NPV()

            compVolTS = BlackVolTermStructureHandle(
                flatVol(today, expectedVol[i], dc))

            bsProcess = BlackScholesMertonProcess(
                spot, qTS, rTS, compVolTS)
            bsEngine = AnalyticEuropeanEngine(bsProcess)

            comp = EuropeanOption(payoff, exercise)
            comp.setPricingEngine(bsEngine)

            impliedVol = comp.impliedVolatility(
                npv, bsProcess, 1e-10, 100)

            self.assertFalse(abs(impliedVol - expectedVol[i]) > tol)
            self.assertFalse(abs((comp.NPV() - npv) / npv) > tol)
            self.assertFalse(abs(comp.delta() - option.delta()) > tol)
            self.assertFalse(abs((comp.gamma() - option.gamma()) / npv) > tol)
            self.assertFalse(abs((comp.theta() - option.theta()) / npv) > tol)
            self.assertFalse(abs((comp.vega() - option.vega()) / npv) > tol)

    def testCompareBsmHWandHestonHW(self):
        TEST_MESSAGE(
            "Comparing European option pricing for a BSM process with one-factor Hull-White model...")

        backup = SavedSettings()

        dc = Actual365Fixed()

        today = Date(16, Sep, 2015)  # Date.todaysDate()

        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        dates = DateVector()
        rates = DoubleVector()
        divRates = DoubleVector()

        for i in range(40):
            dates.push_back(today + Period(i, Years))
            # FLOATING_POINT_EXCEPTION
            rates.push_back(0.01 + 0.0002 * exp(sin(i / 4.0)))
            divRates.push_back(0.02 + 0.0001 * exp(sin(i / 5.0)))

        s0 = QuoteHandle(SimpleQuote(100))
        rTS = YieldTermStructureHandle(ZeroCurve(dates, rates, dc))
        qTS = YieldTermStructureHandle(ZeroCurve(dates, divRates, dc))

        vol = SimpleQuote(0.25)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        bsmProcess = BlackScholesMertonProcess(spot, qTS, rTS, volTS)

        hestonProcess = HestonProcess(
            rTS, qTS, spot,
            vol.value() * vol.value(), 1.0,
            vol.value() * vol.value(), 1e-4, 0.0)

        hestonModel = HestonModel(hestonProcess)
        hullWhiteModel = HullWhite(rTS, 0.01, 0.01)

        bsmhwEngine = AnalyticBSMHullWhiteEngine(
            0.0, bsmProcess, hullWhiteModel)

        hestonHwEngine = AnalyticHestonHullWhiteEngine(
            hestonModel, hullWhiteModel, 128)

        tol = 1e-5
        strike = [
            0.25, 0.5, 0.75, 0.8, 0.9,
            1.0, 1.1, 1.2, 1.5, 2.0, 4.0]
        maturity = [1, 2, 3, 5, 10, 15, 20, 25, 30]
        types = [Option.Put, Option.Call]

        for ty in types:
            for j in strike:
                for l in maturity:
                    maturityDate = today + Period(l, Years)
                    exercise = EuropeanExercise(maturityDate)
                    fwd = j * spot.value() * qTS.discount(maturityDate) / rTS.discount(maturityDate)
                    payoff = PlainVanillaPayoff(ty, fwd)
                    option = EuropeanOption(payoff, exercise)
                    option.setPricingEngine(bsmhwEngine)
                    calculated = option.NPV()
                    option.setPricingEngine(hestonHwEngine)
                    expected = option.NPV()

                    self.assertFalse(
                        abs(calculated - expected) > calculated * tol and
                        abs(calculated - expected) > tol)

    def testZeroBondPricing(self):
        TEST_MESSAGE("Testing Monte-Carlo zero bond pricing...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(16, Sep, 2015)  # Date.todaysDate()

        Settings.instance().evaluationDate = today

        # construct a strange yield curve to check drifts and discounting
        # of the joint stochastic process

        dates = DateVector()
        times = DoubleVector()
        rates = DoubleVector()

        dates.push_back(today)
        rates.push_back(0.02)
        times.push_back(0.0)

        for i in range(120, 240):
            dates.push_back(today + Period(i, Months))
            rates.push_back(0.02 + 0.0002 * exp(sin(i / 8.0)))
            times.push_back(dc.yearFraction(today, dates.back()))

        maturity = dates.back() + Period(10, Years)
        dates.push_back(maturity)
        rates.push_back(0.04)
        times.push_back(dc.yearFraction(today, dates.back()))

        s0 = QuoteHandle(SimpleQuote(100))

        ts = YieldTermStructureHandle(ZeroCurve(dates, rates, dc))
        ds = YieldTermStructureHandle(flatRate(today, 0.0, dc))

        hestonProcess = HestonProcess(ts, ds, s0, 0.02, 1.0, 0.2, 0.5, -0.8)
        hwProcess = HullWhiteForwardProcess(ts, 0.05, 0.05)
        hwProcess.setForwardMeasureTime(dc.yearFraction(today, maturity))
        hwModel = HullWhite(ts, 0.05, 0.05)

        jointProcess = HybridHestonHullWhiteProcess(
            hestonProcess, hwProcess, -0.4)
        temp = DoubleVector(len(times) - 1)
        for i in range(len(temp)):
            temp[i] = times[i]
        grid = TimeGrid(temp)

        # typedef SobolBrownianBridgeRsg rsg_type
        # typedef MultiPathGenerator<rsg_type>.sample_type sample_type

        factors = jointProcess.factors()
        steps = len(grid) - 1
        rsg = SobolBrownianBridgeRsg(factors, steps)
        # MultiPathGenerator<rsg_type> generator(jointProcess, grid, rsg, False)
        generator = BrownianBridgeSobolMultiPathGenerator(
            jointProcess, grid, rsg, False)

        m = 90
        zeroStat = [GeneralStatistics() for i in range(m)]
        optionStat = [GeneralStatistics() for i in range(m)]

        nrTrails = 8191
        optionTenor = 24
        strike = 0.5

        for i in range(nrTrails):
            path = generator.next()

            for j in range(1, m):
                t = grid[j]  # zero end and option maturity
                T = grid[j + optionTenor]  # maturity of zero bond of option

                states = Array(3)
                optionStates = Array(3)
                for k in range(jointProcess.size()):
                    states[k] = path.value()[k][j]
                    optionStates[k] = path.value()[k][j + optionTenor]

                zeroBond = 1.0 / jointProcess.numeraire(t, states)
                zeroOption = zeroBond * max(
                    0.0, hwModel.discountBond(t, T, states[2]) - strike)

                zeroStat[j].add(zeroBond)
                optionStat[j].add(zeroOption)

        for j in range(1, m):
            t = grid[j]
            calculated = zeroStat[j].mean()
            expected = ts.discount(t)

            self.assertFalse(abs(calculated - expected) > 0.03)

            T = grid[j + optionTenor]

            calculated = optionStat[j].mean()
            expected = hwModel.discountBondOption(
                Option.Call, strike, t, T)

            self.assertFalse(abs(calculated - expected) > 0.0035)

    def testMcVanillaPricing(self):
        TEST_MESSAGE("Testing Monte-Carlo vanilla option pricing...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(16, Sep, 2015)  # Date.todaysDate()

        Settings.instance().evaluationDate = today

        # construct a strange yield curve to check drifts and discounting
        # of the joint stochastic process

        dates = DateVector()
        rates = DoubleVector()
        divRates = DoubleVector()

        for i in range(0, 40 + 1):
            dates.push_back(today + Period(i, Years))
            # FLOATING_POINT_EXCEPTION
            rates.push_back(0.03 + 0.0003 * exp(sin(i / 4.0)))
            divRates.push_back(0.02 + 0.0001 * exp(sin(i / 5.0)))

        maturity = today + Period(20, Years)

        s0 = QuoteHandle(SimpleQuote(100))
        rTS = YieldTermStructureHandle(ZeroCurve(dates, rates, dc))
        qTS = YieldTermStructureHandle(ZeroCurve(dates, divRates, dc))
        vol = SimpleQuote(0.25)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))

        bsmProcess = BlackScholesMertonProcess(s0, qTS, rTS, volTS)
        hestonProcess = HestonProcess(rTS, qTS, s0, 0.0625, 0.5, 0.0625, 1e-5, 0.3)
        hwProcess = HullWhiteForwardProcess(rTS, 0.01, 0.01)
        hwProcess.setForwardMeasureTime(dc.yearFraction(today, maturity))

        tol = 0.05
        corr = [-0.9, -0.5, 0.0, 0.5, 0.9]
        strike = [100]

        for i in corr:
            for j in strike:
                jointProcess = HybridHestonHullWhiteProcess(
                    hestonProcess, hwProcess, i)

                payoff = PlainVanillaPayoff(Option.Put, j)
                exercise = EuropeanExercise(maturity)

                optionHestonHW = VanillaOption(payoff, exercise)
                engine = MakeMCPRHestonHullWhiteEngine(jointProcess)
                engine.withSteps(1)
                engine.withAntitheticVariate()
                engine.withControlVariate()
                engine.withAbsoluteTolerance(tol)
                engine.withSeed(42)
                engine = engine.makeEngine()

                optionHestonHW.setPricingEngine(engine)

                hwModel = HullWhite(
                    rTS, hwProcess.a(), hwProcess.sigma())

                optionBsmHW = VanillaOption(payoff, exercise)
                optionBsmHW.setPricingEngine(
                    AnalyticBSMHullWhiteEngine(i, bsmProcess, hwModel))

                calculated = optionHestonHW.NPV()
                error = optionHestonHW.errorEstimate()
                expected = optionBsmHW.NPV()

                self.assertFalse(
                    (i != 0.0 and abs(calculated - expected) > 3 * error) or
                    (i == 0.0 and abs(calculated - expected) > 1e-4))

    def testMcPureHestonPricing(self):
        TEST_MESSAGE("Testing Monte-Carlo Heston option pricing...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(16, Sep, 2015)  # Date.todaysDate()

        Settings.instance().evaluationDate = today

        # construct a strange yield curve to check drifts and discounting
        # of the joint stochastic process

        dates = DateVector()
        rates = DoubleVector()
        divRates = DoubleVector()

        for i in range(100 + 1):
            dates.push_back(today + Period(i, Months))
            # FLOATING_POINT_EXCEPTION
            rates.push_back(0.02 + 0.0002 * exp(sin(i / 10.0)))
            divRates.push_back(0.02 + 0.0001 * exp(sin(i / 20.0)))

        maturity = today + Period(2, Years)

        s0 = QuoteHandle(SimpleQuote(100))
        rTS = YieldTermStructureHandle(
            ZeroCurve(dates, rates, dc))
        qTS = YieldTermStructureHandle(
            ZeroCurve(dates, divRates, dc))

        hestonProcess = HestonProcess(
            rTS, qTS, s0, 0.08, 1.5, 0.0625, 0.5, -0.8)
        hwProcess = HullWhiteForwardProcess(rTS, 0.1, 1e-8)
        hwProcess.setForwardMeasureTime(
            dc.yearFraction(
                today, maturity + Period(1, Years)))

        tol = 0.001
        corr = [-0.45, 0.45, 0.25]
        strike = [100, 75, 50, 150]

        for i in corr:
            for j in strike:
                jointProcess = HybridHestonHullWhiteProcess(
                    hestonProcess, hwProcess, i,
                    HybridHestonHullWhiteProcess.Euler)

                payoff = PlainVanillaPayoff(Option.Put, j)
                exercise = EuropeanExercise(maturity)

                optionHestonHW = VanillaOption(payoff, exercise)
                optionPureHeston = VanillaOption(payoff, exercise)
                optionPureHeston.setPricingEngine(
                    AnalyticHestonEngine(
                        HestonModel(hestonProcess)))

                expected = optionPureHeston.NPV()
                engine = MakeMCPRHestonHullWhiteEngine(jointProcess)
                engine.withSteps(2)
                engine.withAntitheticVariate()
                engine.withControlVariate()
                engine.withAbsoluteTolerance(tol)
                engine.withSeed(42)
                engine = engine.makeEngine()

                optionHestonHW.setPricingEngine(engine)

                calculated = optionHestonHW.NPV()
                error = optionHestonHW.errorEstimate()

                self.assertFalse(
                    abs(calculated - expected) > 3 * error and
                    abs(calculated - expected) > tol)

    def testAnalyticHestonHullWhitePricing(self):
        TEST_MESSAGE("Testing analytic Heston Hull-White option pricing...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(16, Sep, 2015)  # Date.todaysDate()

        Settings.instance().evaluationDate = today

        # construct a strange yield curve to check drifts and discounting
        # of the joint stochastic process

        dates = DateVector()
        rates = DoubleVector()
        divRates = DoubleVector()

        for i in range(40 + 1):
            dates.push_back(today + Period(i, Years))
            # FLOATING_POINT_EXCEPTION
            rates.push_back(0.03 + 0.0001 * exp(sin(i / 4.0)))
            divRates.push_back(0.02 + 0.0002 * exp(sin(i / 3.0)))

        maturity = today + Period(5, Years)
        s0 = QuoteHandle(SimpleQuote(100))
        rTS = YieldTermStructureHandle(
            ZeroCurve(dates, rates, dc))
        qTS = YieldTermStructureHandle(

            ZeroCurve(dates, divRates, dc))

        hestonProcess = HestonProcess(
            rTS, qTS, s0, 0.08, 1.5, 0.0625, 0.5, -0.8)
        hestonModel = HestonModel(hestonProcess)

        hwFwdProcess = HullWhiteForwardProcess(rTS, 0.01, 0.01)
        hwFwdProcess.setForwardMeasureTime(dc.yearFraction(today, maturity))
        hullWhiteModel = HullWhite(
            rTS, hwFwdProcess.a(), hwFwdProcess.sigma())

        tol = 0.002
        strike = [80, 120]
        types = [Option.Put, Option.Call]

        for ty in types:
            for j in strike:
                jointProcess = HybridHestonHullWhiteProcess(
                    hestonProcess, hwFwdProcess, 0.0,
                    HybridHestonHullWhiteProcess.Euler)

                payoff = PlainVanillaPayoff(ty, j)
                exercise = EuropeanExercise(maturity)

                optionHestonHW = VanillaOption(payoff, exercise)
                engine = MakeMCPRHestonHullWhiteEngine(jointProcess)
                engine.withSteps(1)
                engine.withAntitheticVariate()
                engine.withControlVariate()
                engine.withAbsoluteTolerance(tol)
                engine.withSeed(42)
                engine = engine.makeEngine()

                optionHestonHW.setPricingEngine(engine)

                optionPureHeston = VanillaOption(payoff, exercise)
                optionPureHeston.setPricingEngine(
                    AnalyticHestonHullWhiteEngine(
                        hestonModel, hullWhiteModel, 128))

                calculated = optionHestonHW.NPV()
                error = optionHestonHW.errorEstimate()
                expected = optionPureHeston.NPV()

                self.assertFalse(
                    abs(calculated - expected) > 3 * error and
                    abs(calculated - expected) > tol)

    def testCallableEquityPricing(self):
        TEST_MESSAGE("Testing the pricing of a callable equity product...")

        backup = SavedSettings()

        # For the definition of the example product see
        # Alexander Giese, On the Pricing of Auto-Callable Equity
        # Structures in the Presence of Stochastic Volatility and
        # Stochastic Interest Rates .
        # http://workshop.mathfinance.de/2006/papers/giese/slides.pdf

        maturity = 7
        dc = Actual365Fixed()
        today = Date(16, Sep, 2015)  # Date.todaysDate()

        Settings.instance().evaluationDate = today

        spot = QuoteHandle(SimpleQuote(100.0))
        qRate = SimpleQuote(0.04)
        qTS = YieldTermStructureHandle(flatRate(today, qRate, dc))
        rRate = SimpleQuote(0.04)
        rTS = YieldTermStructureHandle(flatRate(today, rRate, dc))

        hestonProcess = HestonProcess(
            rTS, qTS, spot, 0.0625, 1.0,
            0.24 * 0.24, 1e-4, 0.0)
        # FLOATING_POINT_EXCEPTION
        hwProcess = HullWhiteForwardProcess(rTS, 0.00883, 0.00526)
        hwProcess.setForwardMeasureTime(
            dc.yearFraction(
                today, today + Period(maturity + 1, Years)))

        jointProcess = HybridHestonHullWhiteProcess(
            hestonProcess, hwProcess, -0.4)

        schedule = Schedule(
            today, today + Period(maturity, Years),
            Period(1, Years), TARGET(),
            Following, Following,
            DateGeneration.Forward, False)

        times = DoubleVector(maturity + 1)
        for i in range(len(schedule)):
            times[i] = dc.yearFraction(today, schedule[i])
        # transform(schedule.begin(), schedule.end(), times.begin(),
        #     # [&](Date& d) { return dc.yearFraction(today, d) }
        #     )

        for i in range(maturity + 1):
            times[i] = i

        grid = TimeGrid(times)

        redemption = DoubleVector(maturity)
        for i in range(maturity):
            redemption[i] = 1.07 + 0.03 * i

        # typedef PseudoRandom.rsg_type rsg_type
        # rsg_type : InverseCumulativeRsg<MersenneTwisterUniformRng, InverseCumulativeNormal>
        # typedef MultiPathGenerator<rsg_type>.sample_type sample_type

        seed = 42
        # rsg_type rsg = PseudoRandom.make_sequence_generator(
        #     jointProcess.factors() * (grid.size() - 1), seed)
        g = UniformRandomSequenceGenerator(
            jointProcess.factors() * (len(grid) - 1),
            UniformRandomGenerator(seed))
        rsg = GaussianRandomSequenceGenerator(g)

        # MultiPathGenerator<rsg_type> generator(jointProcess, grid, rsg, False)
        generator = GaussianMultiPathGenerator(
            jointProcess, grid, rsg, False)
        stat = GeneralStatistics()

        antitheticPayoff = 0
        nrTrails = 40000
        for i in range(nrTrails):
            antithetic = (i % 2) != 0

            # sample_type path = antithetic ? generator.antithetic() : generator.next()
            path = generator.antithetic() if antithetic else generator.next()

            payoff = 0
            for j in range(1, maturity + 1):
                if path.value()[0][j] > spot.value():
                    states = Array(3)
                    for k in range(3):
                        states[k] = path.value()[k][j]

                    payoff = redemption[j - 1] / jointProcess.numeraire(grid[j], states)
                    break
                elif j == maturity:
                    states = Array(3)
                    for k in range(3):
                        states[k] = path.value()[k][j]

                    payoff = 1.0 / jointProcess.numeraire(grid[j], states)

            if antithetic:
                stat.add(0.5 * (antitheticPayoff + payoff))
            else:
                antitheticPayoff = payoff

        expected = 0.938
        calculated = stat.mean()
        error = stat.errorEstimate()

        self.assertFalse(abs(expected - calculated) > 3 * error)

    def testDiscretizationError(self):
        TEST_MESSAGE(
            "Testing the discretization error of the Heston Hull-White process...")

        backup = SavedSettings()

        dc = Actual360()
        today = Date(16, Sep, 2015)  # Date.todaysDate()

        Settings.instance().evaluationDate = today

        # construct a strange yield curve to check drifts and discounting
        # of the joint stochastic process

        dates = DateVector()
        rates = DoubleVector()
        divRates = DoubleVector()

        for i in range(31 + 1):
            dates.push_back(today + Period(i, Years))
            # FLOATING_POINT_EXCEPTION
            rates.push_back(0.04 + 0.0001 * exp(sin(i)))
            divRates.push_back(0.04 + 0.0001 * exp(sin(i)))

        maturity = today + Period(10, Years)
        v = 0.25

        s0 = QuoteHandle(SimpleQuote(100))
        vol = SimpleQuote(v)
        volTS = BlackVolTermStructureHandle(flatVol(today, vol, dc))
        rTS = YieldTermStructureHandle(ZeroCurve(dates, rates, dc))
        qTS = YieldTermStructureHandle(ZeroCurve(dates, divRates, dc))

        bsmProcess = BlackScholesMertonProcess(s0, qTS, rTS, volTS)

        hestonProcess = HestonProcess(
            rTS, qTS, s0, v * v, 1, v * v, 1e-6, -0.4)

        hwProcess = HullWhiteForwardProcess(rTS, 0.01, 0.01)
        hwProcess.setForwardMeasureTime(20.1472222222222222)

        tol = 0.05
        corr = [-0.85, 0.5]
        strike = [50, 100, 125]

        for i in corr:
            for j in strike:
                payoff = PlainVanillaPayoff(Option.Put, j)
                exercise = EuropeanExercise(maturity)

                optionBsmHW = VanillaOption(payoff, exercise)
                hwModel = HullWhite(
                    rTS, hwProcess.a(), hwProcess.sigma())
                optionBsmHW.setPricingEngine(
                    AnalyticBSMHullWhiteEngine(
                        i, bsmProcess, hwModel))

                expected = optionBsmHW.NPV()

                optionHestonHW = VanillaOption(payoff, exercise)
                jointProcess = HybridHestonHullWhiteProcess(
                    hestonProcess, hwProcess, i)
                engine = MakeMCPRHestonHullWhiteEngine(jointProcess)
                engine.withSteps(1)
                engine.withAntitheticVariate()
                engine.withAbsoluteTolerance(tol)
                engine.withSeed(42)
                engine = engine.makeEngine()

                optionHestonHW.setPricingEngine(engine)

                calculated = optionHestonHW.NPV()
                error = optionHestonHW.errorEstimate()

                self.assertFalse(
                    abs(calculated - expected) > 3 * error and
                    abs(calculated - expected) > 1e-5)

    def testFdmHestonHullWhiteEngine(self):
        TEST_MESSAGE("Testing the FDM Heston Hull-White engine...")

        backup = SavedSettings()

        today = Date(28, March, 2004)
        Settings.instance().evaluationDate = today
        exerciseDate = Date(28, March, 2012)
        dc = Actual365Fixed()

        s0 = QuoteHandle(SimpleQuote(100.0))

        rTS = YieldTermStructureHandle(flatRate(0.05, dc))
        qTS = YieldTermStructureHandle(flatRate(0.02, dc))

        vol = 0.30
        volTS = BlackVolTermStructureHandle(flatVol(vol, dc))

        v0 = vol * vol
        hestonProcess = HestonProcess(
            rTS, qTS, s0, v0, 1.0, v0, 0.000001, 0.0)

        stochProcess = BlackScholesMertonProcess(s0, qTS, rTS, volTS)

        hwProcess = HullWhiteProcess(rTS, 0.00883, 0.01)
        hwModel = HullWhite(
            rTS, hwProcess.a(), hwProcess.sigma())

        exercise = EuropeanExercise(exerciseDate)
        corr = [-0.85, 0.5]
        strike = [75, 120, 160]

        for i in corr:
            for j in strike:
                payoff = PlainVanillaPayoff(Option.Call, j)
                option = VanillaOption(payoff, exercise)

                option.setPricingEngine(
                    FdHestonHullWhiteVanillaEngine(
                        HestonModel(hestonProcess),
                        hwProcess, i, 50, 200, 10, 15))
                calculated = option.NPV()
                calculatedDelta = option.delta()
                calculatedGamma = option.gamma()

                option.setPricingEngine(
                    AnalyticBSMHullWhiteEngine(
                        i, stochProcess, hwModel))
                expected = option.NPV()
                expectedDelta = option.delta()
                expectedGamma = option.gamma()

                npvTol = 0.01
                self.assertFalse(
                    abs(calculated - expected) > npvTol)

                deltaTol = 0.001
                self.assertFalse(
                    abs(calculatedDelta - expectedDelta) > deltaTol)

                gammaTol = 0.001
                self.assertFalse(
                    abs(calculatedGamma - expectedGamma) > gammaTol)

    def testBsmHullWhitePricing(self):
        TEST_MESSAGE("Testing convergence speed of Heston-Hull-White engine...")

        backup = SavedSettings()

        today = Date(27, December, 2004)
        Settings.instance().evaluationDate = today

        maturity = 5.0
        equityIrCorr = -0.4
        strikes = [
            75, 85, 90, 95, 100, 105, 110,
            115, 120, 125, 130, 140, 150]
        listOfTimeStepsPerYear = [20]

        hestonModelData = HestonModelData(
            "BSM-HW Model", 0.09, 1.0, 0.09, QL_EPSILON, 0.0, 0.04, 0.03)
        hwModelData = hullWhiteModels[0]
        controlVariate = [True, False]

        hp = makeHestonProcess(hestonModelData)
        hestonModel = HestonModel(hp)

        hwProcess = HullWhiteProcess(
            hp.riskFreeRate(),
            hwModelData.a, hwModelData.sigma)
        hullWhiteModel = HullWhite(
            hp.riskFreeRate(),
            hwProcess.a(), hwProcess.sigma())

        bsmProcess = BlackScholesMertonProcess(
            hp.s0(), hp.dividendYield(), hp.riskFreeRate(),
            BlackVolTermStructureHandle(
                flatVol(
                    today, sqrt(hestonModelData.theta),
                    hp.riskFreeRate().dayCounter())))

        bsmhwEngine = AnalyticBSMHullWhiteEngine(
            equityIrCorr, bsmProcess, hullWhiteModel)

        tolWithCV = [2e-4, 2e-4, 2e-4, 2e-4, 0.01]
        tolWithOutCV = [5e-3, 5e-3, 5e-3, 5e-3, 0.02]
        for l in range(len(schemes)):
            scheme = schemes[l]
            for i in controlVariate:
                for u in listOfTimeStepsPerYear:
                    tSteps = int(maturity * u)

                    fdEngine = FdHestonHullWhiteVanillaEngine(
                        hestonModel, hwProcess, equityIrCorr, tSteps,
                        400, 2, 10, 0, i, scheme.schemeDesc)
                    fdEngine.enableMultipleStrikesCaching(strikes)

                    avgPriceDiff = 0.0
                    for strike in strikes:
                        optionData = VanillaOptionData(
                            strike, maturity, Option.Call)
                        option = makeVanillaOption(optionData)
                        option.setPricingEngine(bsmhwEngine)
                        expected = option.NPV()

                        option.setPricingEngine(fdEngine)
                        calculated = option.NPV()
                        avgPriceDiff += abs(expected - calculated) / len(strikes)  # NOLINT(bugprone-integer-division)

                    self.assertFalse(i and tolWithCV[l] < avgPriceDiff)
                    self.assertFalse((not i) and tolWithOutCV[l] < avgPriceDiff)

    def testSpatialDiscretizatinError(self):
        TEST_MESSAGE("Testing spatial convergence speed of Heston engine...")

        backup = SavedSettings()

        today = Date(27, December, 2004)
        Settings.instance().evaluationDate = today

        maturity = 1.0
        strikes = [75, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 140, 150]
        listOfTimeStepsPerYear = [40]

        tol = [0.02, 0.02, 0.02, 0.02, 0.05]
        for u in listOfTimeStepsPerYear:
            for i in range(len(schemes)):
                for j in hestonModels:
                    avgPriceDiff = 0
                    hestonProcess = makeHestonProcess(j)
                    hestonModel = HestonModel(hestonProcess)

                    analyticEngine = AnalyticHestonEngine(hestonModel, 172)

                    tSteps = int(maturity * u)

                    fdEngine = FdHestonVanillaEngine(
                        hestonModel, tSteps, 200, 40, 0,
                        schemes[i].schemeDesc)
                    fdEngine.enableMultipleStrikesCaching(strikes)

                    for strike in strikes:
                        optionData = VanillaOptionData(
                            strike, maturity, Option.Call)
                        option = makeVanillaOption(optionData)
                        option.setPricingEngine(analyticEngine)
                        expected = option.NPV()

                        option.setPricingEngine(fdEngine)
                        calculated = option.NPV()

                        avgPriceDiff += abs(expected - calculated) / len(strikes)  # NOLINT(bugprone-integer-division)

                    self.assertFalse(avgPriceDiff > tol[i])

    def testHestonHullWhiteCalibration(self):
        pass

    def testH1HWPricingEngine(self):
        backup = SavedSettings()

        # Example taken from Lech Aleksander Grzelak,
        # Equity and Foreign Exchange Hybrid Models for Pricing Long-Maturity
        # Financial Derivatives,
        # http://repository.tudelft.nl/assets/uuid:a8e1a007-bd89-481a-aee3-0e22f15ade6b/PhDThesis_main.pdf

        today = Date(15, July, 2012)
        Settings.instance().evaluationDate = today
        exerciseDate = Date(13, July, 2022)
        dc = Actual365Fixed()

        exercise = EuropeanExercise(exerciseDate)

        s0 = QuoteHandle(SimpleQuote(100.0))

        r = 0.02
        q = 0.00
        v0 = 0.05
        theta = 0.05
        kappa_v = 0.3
        sigma_v = [0.3, 0.6]
        rho_sv = -0.30
        rho_sr = 0.6
        kappa_r = 0.01
        sigma_r = 0.01

        rTS = YieldTermStructureHandle(flatRate(today, r, dc))
        qTS = YieldTermStructureHandle(flatRate(today, q, dc))

        flatVolTS = BlackVolTermStructureHandle(flatVol(today, 0.20, dc))
        bsProcess = GeneralizedBlackScholesProcess(s0, qTS, rTS, flatVolTS)

        hwProcess = HullWhiteProcess(rTS, kappa_r, sigma_r)
        hullWhiteModel = HullWhite(rTS, kappa_r, sigma_r)

        tol = 0.0001
        strikes = [40, 80, 100, 120, 180]
        expected = [
            [0.267503, 0.235742, 0.228223, 0.223461, 0.217855],
            [0.263626, 0.211625, 0.199907, 0.193502, 0.190025]]

        for j in range(len(sigma_v)):
            hestonProcess = HestonProcess(
                rTS, qTS, s0, v0, kappa_v, theta, sigma_v[j], rho_sv)
            hestonModel = HestonModel(hestonProcess)

            for i in range(len(strikes)):
                payoff = PlainVanillaPayoff(Option.Call, strikes[i])

                option = VanillaOption(payoff, exercise)

                analyticH1HWEngine = AnalyticH1HWEngine(
                    hestonModel, hullWhiteModel, rho_sr, 144)
                option.setPricingEngine(analyticH1HWEngine)
                impliedH1HW = option.impliedVolatility(option.NPV(), bsProcess)

                self.assertFalse(abs(expected[j][i] - impliedH1HW) > tol)
