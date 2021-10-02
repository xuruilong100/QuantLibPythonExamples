import unittest
from utilities import *
from QuantLib import *
from math import exp, sqrt


def getCalibrationError(options):
    sse = 0
    for option in options:
        diff = option.calibrationError() * 100.0
        sse += diff * diff

    return sse


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


class BatesModelTest(unittest.TestCase):
    _hestonModels = [
        # ADI finite difference schemes for option pricing in the
        # Heston model with correlation, K.J. in t'Hout and S. Foulon,
        HestonModelData("'t Hout case 1", 0.04, 1.5, 0.04, 0.3, -0.9, 0.025, 0.0),
        # Efficient numerical methods for pricing American options under
        # stochastic volatility, Samuli Ikonen and Jari Toivanen,
        HestonModelData("Ikonen-Toivanen", 0.0625, 5, 0.16, 0.9, 0.1, 0.1, 0.0),
        # Not-so-complex logarithms in the Heston model,
        # Christian Kahl and Peter Jäckel
        HestonModelData("Kahl-Jaeckel", 0.16, 1.0, 0.16, 2.0, -0.8, 0.0, 0.0),
        # self defined test cases
        HestonModelData("Equity case", 0.07, 2.0, 0.04, 0.55, -0.8, 0.03, 0.035)]

    def testAnalyticVsBlack(self):
        TEST_MESSAGE("Testing analytic Bates engine against Black formula...")

        backup = SavedSettings()

        settlementDate = Date.todaysDate()
        Settings.instance().evaluationDate = settlementDate

        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = settlementDate + Period(6, Months)

        payoff = PlainVanillaPayoff(Option.Put, 30)
        exercise = EuropeanExercise(exerciseDate)

        riskFreeTS = YieldTermStructureHandle(flatRate(0.1, dayCounter))
        dividendTS = YieldTermStructureHandle(flatRate(0.04, dayCounter))
        s0 = QuoteHandle(SimpleQuote(32.0))

        yearFraction = dayCounter.yearFraction(settlementDate, exerciseDate)
        forwardPrice = s0.value() * exp((0.1 - 0.04) * yearFraction)
        expected = blackFormula(
            payoff.optionType(),
            payoff.strike(),
            forwardPrice,
            sqrt(0.05 * yearFraction)) * exp(-0.1 * yearFraction)
        v0 = 0.05
        kappa = 5.0
        theta = 0.05
        sigma = 1.0e-4
        rho = 0.0
        lambda_ = 0.0001
        nu = 0.0
        delta = 0.0001

        option = VanillaOption(payoff, exercise)

        process = BatesProcess(
            riskFreeTS, dividendTS, s0, v0,
            kappa, theta, sigma, rho,
            lambda_, nu, delta)

        engine = BatesEngine(
            BatesModel(process), 64)

        option.setPricingEngine(engine)
        calculated = option.NPV()

        tolerance = 2.0e-7
        error = abs(calculated - expected)
        self.assertFalse(error > tolerance)

        engine = BatesDetJumpEngine(
            BatesDetJumpModel(process, 1.0, 0.0001),
            64)

        option.setPricingEngine(engine)
        calculated = option.NPV()

        error = abs(calculated - expected)
        self.assertFalse(error > tolerance)

        engine = BatesDoubleExpEngine(
            BatesDoubleExpModel(process, 0.0001, 0.0001, 0.0001),
            64)

        option.setPricingEngine(engine)
        calculated = option.NPV()

        error = abs(calculated - expected)
        self.assertFalse(error > tolerance)

        engine = BatesDoubleExpDetJumpEngine(
            BatesDoubleExpDetJumpModel(
                process, 0.0001, 0.0001,
                0.0001, 0.5, 1.0, 0.0001),
            64)

        option.setPricingEngine(engine)
        calculated = option.NPV()

        error = abs(calculated - expected)
        self.assertFalse(error > tolerance)

    def testAnalyticAndMcVsJumpDiffusion(self):
        TEST_MESSAGE("Testing analytic Bates engine against Merton-76 engine...")

        backup = SavedSettings()

        settlementDate = Date.todaysDate()
        Settings.instance().evaluationDate = settlementDate

        dayCounter = ActualActual(ActualActual.ISDA)

        payoff = PlainVanillaPayoff(Option.Put, 95)

        riskFreeTS = YieldTermStructureHandle(flatRate(0.1, dayCounter))
        dividendTS = YieldTermStructureHandle(flatRate(0.04, dayCounter))
        s0 = QuoteHandle(SimpleQuote(100))

        v0 = 0.0433
        # FLOATING_POINT_EXCEPTION
        vol = SimpleQuote(sqrt(v0))
        volTS = flatVol(settlementDate, vol, dayCounter)

        kappa = 0.5
        theta = v0
        sigma = 1.0e-4
        rho = 0.0

        jumpIntensity = SimpleQuote(2)
        meanLogJump = SimpleQuote(-0.2)
        jumpVol = SimpleQuote(0.2)

        batesProcess = BatesProcess(
            riskFreeTS, dividendTS, s0, v0,
            kappa, theta, sigma, rho,
            jumpIntensity.value(),
            meanLogJump.value(),
            jumpVol.value())

        mertonProcess = Merton76Process(
            s0, dividendTS, riskFreeTS,
            BlackVolTermStructureHandle(volTS),
            QuoteHandle(jumpIntensity),
            QuoteHandle(meanLogJump),
            QuoteHandle(jumpVol))

        batesEngine = BatesEngine(
            BatesModel(batesProcess), 160)

        mcTol = 0.1
        mcBatesEngine = MakeMCPREuropeanHestonEngine(batesProcess)
        mcBatesEngine.withStepsPerYear(2)
        mcBatesEngine.withAntitheticVariate()
        mcBatesEngine.withAbsoluteTolerance(mcTol)
        mcBatesEngine.withSeed(1234)
        mcBatesEngine = mcBatesEngine.makeEngine()

        mertonEngine = JumpDiffusionEngine(
            mertonProcess, 1e-10, 1000)

        for i in range(1, 6, 2):
            exerciseDate = settlementDate + Period(i, Years)
            exercise = EuropeanExercise(exerciseDate)

            batesOption = VanillaOption(payoff, exercise)

            batesOption.setPricingEngine(batesEngine)
            calculated = batesOption.NPV()

            batesOption.setPricingEngine(mcBatesEngine)
            mcCalculated = batesOption.NPV()

            mertonOption = EuropeanOption(payoff, exercise)
            mertonOption.setPricingEngine(mertonEngine)
            expected = mertonOption.NPV()

            tolerance = 2e-8
            relError = abs(calculated - expected) / expected
            self.assertFalse(relError > tolerance)

            mcError = abs(expected - mcCalculated)
            self.assertFalse(mcError > 3 * mcTol)

    def testAnalyticVsMCPricing(self):
        TEST_MESSAGE("Testing analytic Bates engine against Monte-Carlo engine...")

        backup = SavedSettings()

        settlementDate = Date(30, March, 2007)
        Settings.instance().evaluationDate = settlementDate

        dayCounter = ActualActual(ActualActual.ISDA)
        exerciseDate = Date(30, March, 2012)

        payoff = PlainVanillaPayoff(Option.Put, 100)
        exercise = EuropeanExercise(exerciseDate)

        for hestonModel in self._hestonModels:
            riskFreeTS = YieldTermStructureHandle(flatRate(hestonModel.r, dayCounter))
            dividendTS = YieldTermStructureHandle(flatRate(hestonModel.q, dayCounter))
            s0 = QuoteHandle(SimpleQuote(100))

            batesProcess = BatesProcess(
                riskFreeTS, dividendTS, s0, hestonModel.v0,
                hestonModel.kappa, hestonModel.theta,
                hestonModel.sigma, hestonModel.rho,
                2.0, -0.2, 0.1)

            mcTolerance = 0.5
            mcEngine = MakeMCPREuropeanHestonEngine(batesProcess)
            mcEngine.withStepsPerYear(20)
            mcEngine.withAntitheticVariate()
            mcEngine.withAbsoluteTolerance(mcTolerance)
            mcEngine.withSeed(1234)
            mcEngine = mcEngine.makeEngine()

            batesModel = BatesModel(batesProcess)

            fdEngine = FdBatesVanillaEngine(batesModel, 50, 100, 30)

            analyticEngine = BatesEngine(batesModel, 160)

            option = VanillaOption(payoff, exercise)

            option.setPricingEngine(mcEngine)
            calculated = option.NPV()

            option.setPricingEngine(analyticEngine)
            expected = option.NPV()

            option.setPricingEngine(fdEngine)
            fdCalculated = option.NPV()

            mcError = abs(calculated - expected)
            self.assertFalse(mcError > 3 * mcTolerance)

            fdTolerance = 0.2
            fdError = abs(fdCalculated - expected)
            self.assertFalse(fdError > fdTolerance)

    def testDAXCalibration(self):
        # this example is taken from A. Sepp
        # Pricing European-Style Options under Jump Diffusion Processes
        # with Stochstic Volatility: Applications of Fourier Transform
        # http://math.ut.ee/~spartak/papers/stochjumpvols.pdf

        TEST_MESSAGE(
            "Testing Bates model calibration using DAX volatility data...")

        backup = SavedSettings()

        settlementDate = Date(5, July, 2002)
        Settings.instance().evaluationDate = settlementDate

        dayCounter = Actual365Fixed()
        calendar = TARGET()

        t = [13, 41, 75, 165, 256, 345, 524, 703]
        r = [0.0357, 0.0349, 0.0341, 0.0355, 0.0359, 0.0368, 0.0386, 0.0401]

        dates = DateVector()
        rates = DoubleVector()
        dates.push_back(settlementDate)
        rates.push_back(0.0357)
        for i in range(8):
            dates.push_back(settlementDate + Period(t[i], Days))
            rates.push_back(r[i])

        # FLOATING_POINT_EXCEPTION
        riskFreeTS = YieldTermStructureHandle(ZeroCurve(dates, rates, dayCounter))

        dividendTS = YieldTermStructureHandle(
            flatRate(settlementDate, 0.0, dayCounter))

        v = [
            0.6625, 0.4875, 0.4204, 0.3667, 0.3431, 0.3267, 0.3121, 0.3121,
            0.6007, 0.4543, 0.3967, 0.3511, 0.3279, 0.3154, 0.2984, 0.2921,
            0.5084, 0.4221, 0.3718, 0.3327, 0.3155, 0.3027, 0.2919, 0.2889,
            0.4541, 0.3869, 0.3492, 0.3149, 0.2963, 0.2926, 0.2819, 0.2800,
            0.4060, 0.3607, 0.3330, 0.2999, 0.2887, 0.2811, 0.2751, 0.2775,
            0.3726, 0.3396, 0.3108, 0.2781, 0.2788, 0.2722, 0.2661, 0.2686,
            0.3550, 0.3277, 0.3012, 0.2781, 0.2781, 0.2661, 0.2661, 0.2681,
            0.3428, 0.3209, 0.2958, 0.2740, 0.2688, 0.2627, 0.2580, 0.2620,
            0.3302, 0.3062, 0.2799, 0.2631, 0.2573, 0.2533, 0.2504, 0.2544,
            0.3343, 0.2959, 0.2705, 0.2540, 0.2504, 0.2464, 0.2448, 0.2462,
            0.3460, 0.2845, 0.2624, 0.2463, 0.2425, 0.2385, 0.2373, 0.2422,
            0.3857, 0.2860, 0.2578, 0.2399, 0.2357, 0.2327, 0.2312, 0.2351,
            0.3976, 0.2860, 0.2607, 0.2356, 0.2297, 0.2268, 0.2241, 0.2320]

        s0 = QuoteHandle(SimpleQuote(4468.17))
        strike = [
            3400, 3600, 3800, 4000, 4200, 4400,
            4500, 4600, 4800, 5000, 5200, 5400, 5600]

        v0 = 0.0433
        vol = SimpleQuote(sqrt(v0))

        kappa = 1.0
        theta = v0
        sigma = 1.0
        rho = 0.0
        lambda_ = 1.1098
        nu = -0.1285
        delta = 0.1702

        process = BatesProcess(
            riskFreeTS, dividendTS, s0, v0,
            kappa, theta, sigma, rho, lambda_, nu, delta)

        batesModel = BatesModel(process)

        batesEngine = BatesEngine(batesModel, 64)

        options = BlackCalibrationHelperVector()

        for s in range(13):
            for m in range(8):
                vol = QuoteHandle(
                    SimpleQuote(v[s * 8 + m]))

                maturity = Period(int((t[m] + 3.0) / 7.0), Weeks)  # round to weeks

                # this is the calibration helper for the bates models
                options.push_back(
                    HestonModelHelper(
                        maturity, calendar,
                        s0.value(), strike[s], vol,
                        riskFreeTS, dividendTS,
                        BlackCalibrationHelper.ImpliedVolError))
                options.back().setPricingEngine(batesEngine)

        optionsClone = CalibrationHelperVector()
        for option in options:
            optionsClone.append(option)

        # check calibration engine
        om = LevenbergMarquardt()
        batesModel.calibrate(
            optionsClone,
            om, EndCriteria(400, 40, 1.0e-8, 1.0e-8, 1.0e-8))

        expected = 36.6
        calculated = getCalibrationError(options)

        self.assertFalse(abs(calculated - expected) > 2.5)

        # check pricing of derived engines
        pricingEngines = []

        process = BatesProcess(
            riskFreeTS, dividendTS, s0, v0,
            kappa, theta, sigma, rho, 1.0, -0.1, 0.1)

        pricingEngines.append(
            BatesDetJumpEngine(
                BatesDetJumpModel(process), 64))

        hestonProcess = HestonProcess(
            riskFreeTS, dividendTS, s0, v0,
            kappa, theta, sigma, rho)

        pricingEngines.append(
            BatesDoubleExpEngine(
                BatesDoubleExpModel(
                    hestonProcess, 1.0),
                64))

        pricingEngines.append(
            BatesDoubleExpDetJumpEngine(
                BatesDoubleExpDetJumpModel(
                    hestonProcess, 1.0),
                64))

        expectedValues = [5896.37, 5499.29, 6497.89]

        tolerance = 0.1
        for i in range(len(pricingEngines)):
            for option in options:
                option.setPricingEngine(pricingEngines[i])

            calculated = abs(getCalibrationError(options))
            self.assertFalse(
                abs(calculated - expectedValues[i]) > tolerance)
