import unittest
from utilities import *
from QuantLib import *
from math import sin, exp, log, sqrt, sinh


class SwingPdePricing(object):
    def __init__(self,
                 process,
                 option,
                 shape):
        self.process_ = process
        self.option_ = option
        self.shape_ = shape

    def __call__(self, x):
        rTS = flatRate(0.0, Actual365Fixed())

        gridX = 200
        gridY = 100
        gridT = 100

        self.option_.setPricingEngine(
            FdExtOUJumpVanillaEngine(
                self.process_, rTS,
                int(gridT / x), int(gridX / x), int(gridY / x), self.shape_))

        r = self.option_.NPV()

        return r


def createKlugeProcess():
    x0 = Array(2)
    x0[0] = 3.0
    x0[1] = 0.0

    beta = 5.0
    eta = 2.0
    jumpIntensity = 1.0
    speed = 1.0
    volatility = 2.0

    ouProcess = ExtendedOrnsteinUhlenbeckProcess(
        speed, volatility, 3.0,
        # constant<Real, Real>(x0[0]),
        lambda x: 3.0)

    return ExtOUWithJumpsProcess(
        ouProcess,
        0.0, beta, jumpIntensity, eta)


class SwingOptionTest(unittest.TestCase):

    def testExtendedOrnsteinUhlenbeckProcess(self):
        TEST_MESSAGE("Testing extended Ornstein-Uhlenbeck process...")

        backup = SavedSettings()

        speed = 2.5
        vol = 0.70
        level = 1.43

        discr = [
            ExtendedOrnsteinUhlenbeckProcess.MidPoint,
            ExtendedOrnsteinUhlenbeckProcess.Trapezodial,
            ExtendedOrnsteinUhlenbeckProcess.GaussLobatto]

        # f    =[ constant<Real, Real>(level),
        #         add<Real>(1.0),
        #         static_cast<Real(*)(Real)>(sin) ]
        f = [
            lambda x: level,
            lambda x: x + 1.0,
            lambda x: sin(x)]

        for n in range(len(f)):
            refProcess = ExtendedOrnsteinUhlenbeckProcess(
                speed, vol, 0.0, f[n],
                ExtendedOrnsteinUhlenbeckProcess.GaussLobatto, 1e-6)

            for i in range(len(discr) - 1):
                eouProcess = ExtendedOrnsteinUhlenbeckProcess(
                    speed, vol, 0.0, f[n], discr[i])

                T = 10
                nTimeSteps = 10000

                dt = T / nTimeSteps
                t = 0.0
                q = 0.0
                p = 0.0

                rng = GaussianRandomGenerator(UniformRandomGenerator(1234))

                for j in range(nTimeSteps):
                    dw = rng.next().value()
                    q = eouProcess.evolve(t, q, dt, dw)
                    p = refProcess.evolve(t, p, dt, dw)

                    self.assertFalse(abs(q - p) > 1e-6)
                    t += dt

    def testFdBSSwingOption(self):
        TEST_MESSAGE("Testing Black-Scholes vanilla swing option pricing...")

        backup = SavedSettings()

        settlementDate = Date(16, Sep, 2015) # Date.todaysDate()
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        maturityDate = settlementDate + Period(12, Months)

        strike = 30
        payoff = PlainVanillaPayoff(Option.Put, strike)
        forward = VanillaForwardPayoff(Option.Put, strike)

        exerciseDates = DateVector(1, settlementDate + Period(1, Months))
        while exerciseDates.back() < maturityDate:
            exerciseDates.push_back(exerciseDates.back() + Period(1, Months))

        swingExercise = SwingExercise(exerciseDates)

        riskFreeTS = YieldTermStructureHandle(flatRate(0.14, dayCounter))
        dividendTS = YieldTermStructureHandle(flatRate(0.02, dayCounter))
        volTS = BlackVolTermStructureHandle(
            flatVol(settlementDate, 0.4, dayCounter))

        s0 = QuoteHandle(SimpleQuote(30.0))

        process = BlackScholesMertonProcess(s0, dividendTS, riskFreeTS, volTS)
        engine = FdSimpleBSSwingEngine(process, 50, 200)

        bermudanOption = VanillaOption(payoff, swingExercise)
        bermudanOption.setPricingEngine(
            FdBlackScholesVanillaEngine(process, 50, 200))
        bermudanOptionPrices = bermudanOption.NPV()

        for i in range(len(exerciseDates)):
            exerciseRights = i + 1

            swingOption = VanillaSwingOption(forward, swingExercise,
                                             0, exerciseRights)
            swingOption.setPricingEngine(engine)
            swingOptionPrice = swingOption.NPV()

            upperBound = exerciseRights * bermudanOptionPrices

            self.assertFalse(swingOptionPrice - upperBound > 0.01)

            lowerBound = 0.0
            for j in range(len(exerciseDates) - i - 1, len(exerciseDates)):
                europeanOption = VanillaOption(
                    payoff, EuropeanExercise(exerciseDates[j]))
                europeanOption.setPricingEngine(
                    AnalyticEuropeanEngine(process))
                lowerBound += europeanOption.NPV()

            self.assertFalse(lowerBound - swingOptionPrice > 4e-2)

    @unittest.skipIf(skipSlowTest, 'testExtOUJumpSwingOption is VERY SLOW')
    def testExtOUJumpSwingOption(self):
        TEST_MESSAGE(
            "Testing simple swing option pricing for Kluge model...")

        backup = SavedSettings()

        settlementDate = Date(16, Sep, 2015) # Date.todaysDate()
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        maturityDate = settlementDate + Period(12, Months)

        strike = 30
        payoff = PlainVanillaPayoff(Option.Put, strike)
        forward = VanillaForwardPayoff(Option.Put, strike)

        exerciseDates = DateVector(1, settlementDate + Period(1, Months))
        while exerciseDates.back() < maturityDate:
            exerciseDates.push_back(exerciseDates.back() + Period(1, Months))

        swingExercise = SwingExercise(exerciseDates)

        exerciseTimes = DoubleVector(len(exerciseDates))
        for i in range(len(exerciseTimes)):
            exerciseTimes[i] = dayCounter.yearFraction(
                settlementDate, exerciseDates[i])

        grid = TimeGrid(exerciseTimes, 60)
        exerciseIndex = SizeVector(len(exerciseDates))
        for i in range(exerciseIndex.size()):
            exerciseIndex[i] = grid.closestIndex(exerciseTimes[i])

        jumpProcess = createKlugeProcess()

        irRate = 0.1
        rTS = flatRate(settlementDate, irRate, dayCounter)

        swingEngine = FdSimpleExtOUJumpSwingEngine(
            jumpProcess, rTS, 25, 50, 25)

        vanillaEngine = FdExtOUJumpVanillaEngine(
            jumpProcess, rTS, 25, 50, 25)

        bermudanOption = VanillaOption(payoff, swingExercise)
        bermudanOption.setPricingEngine(vanillaEngine)
        bermudanOptionPrices = bermudanOption.NPV()

        nrTrails = 16000
        rsg = GaussianRandomSequenceGenerator(
            UniformRandomSequenceGenerator(
                jumpProcess.factors() * (len(grid) - 1),
                UniformRandomGenerator(421)))

        generator = GaussianMultiPathGenerator(
            jumpProcess, grid, rsg, false)

        for i in range(len(exerciseDates)):
            exerciseRights = i + 1

            swingOption = VanillaSwingOption(
                forward, swingExercise, 0, exerciseRights)
            swingOption.setPricingEngine(swingEngine)
            swingOptionPrice = swingOption.NPV()

            upperBound = exerciseRights * bermudanOptionPrices

            self.assertFalse(swingOptionPrice - upperBound > 2e-2)

            lowerBound = 0.0
            for j in range(len(exerciseDates) - i - 1, len(exerciseDates)):
                europeanOption = VanillaOption(
                    payoff, EuropeanExercise(exerciseDates[j]))
                europeanOption.setPricingEngine(
                    vanillaEngine)
                lowerBound += europeanOption.NPV()

            self.assertFalse(lowerBound - swingOptionPrice > 2e-2)

            # use MC plus perfect forecast to find an upper bound
            npv = GeneralStatistics()
            for n in range(nrTrails):
                path = generator.next()

                exerciseValues = [0.0] * len(exerciseTimes)
                for k in range(len(exerciseTimes)):
                    x = path.value()[0][exerciseIndex[k]]
                    y = path.value()[1][exerciseIndex[k]]
                    s = exp(x + y)

                    exerciseValues[k] = payoff(s) * rTS.discount(exerciseDates[k])

                exerciseValues.sort(reverse=True)
                # sort(exerciseValues.begin(), exerciseValues.end(),
                #     greater<Real>())
                npCashFlows = 0.0
                for i in range(exerciseRights):
                    npCashFlows += exerciseValues[i]

                # npCashFlows                    = accumulate(exerciseValues.begin(),
                #         exerciseValues.begin() + exerciseRights, Real(0.0))
                npv.add(npCashFlows)

            mcUpperBound = npv.mean()
            mcErrorUpperBound = npv.errorEstimate()
            self.assertFalse(swingOptionPrice - mcUpperBound > 2.36 * mcErrorUpperBound)

    def testFdmExponentialJump1dMesher(self):
        TEST_MESSAGE("Testing finite difference mesher for the Kluge model...")

        backup = SavedSettings()

        x = Array(2, 1.0)
        beta = 100.0
        eta = 1.0 / 0.4
        jumpIntensity = 4.0
        dummySteps = 2

        mesher = ExponentialJump1dMesher(
            dummySteps, beta, jumpIntensity, eta)

        ouProcess = ExtendedOrnsteinUhlenbeckProcess(
            1.0, 1.0, x[0],
            lambda x: 1.0)
        jumpProcess = ExtOUWithJumpsProcess(
            ouProcess, x[1], beta, jumpIntensity, eta)

        dt = 1.0 / (10.0 * beta)
        n = 1000000

        path = [0.0] * n
        mt = GaussianRandomGenerator(UniformRandomGenerator(123))
        dw = Array(3)
        for i in range(n):
            dw[0] = mt.next().value()
            dw[1] = mt.next().value()
            dw[2] = mt.next().value()
            x = jumpProcess.evolve(0.0, x, dt, dw)
            path[i] = x[1]

        path.sort()

        relTol1 = 2e-3
        relTol2 = 2e-2
        threshold = 0.9

        # for (x = 1e-12 x < 1.0 x *= 10) {
        #     v = mesher.jumpSizeDistribution(x)
        for i in range(-12, 0):
            x = 10 ** i
            v = mesher.jumpSizeDistribution(x)

            # iter = lower_bound(path.begin(), path.end(), x)
            # q = distance(path.begin(), iter) / Real(n)
            iter = 0
            for p in path:
                if p >= x:
                    break
                else:
                    iter += 1
            q = iter / n
            self.assertTrue(
                abs(q - v) < relTol1
                or ((v < threshold) and abs(q - v) < relTol2),
                "can not reproduce jump distribution")

    @unittest.skipIf(skipSlowTest, 'testExtOUJumpVanillaEngine is VERY SLOW')
    def testExtOUJumpVanillaEngine(self):
        TEST_MESSAGE(
            "Testing finite difference pricer for the Kluge model...")

        backup = SavedSettings()

        jumpProcess = createKlugeProcess()

        today = Date(16, Sep, 2015)
        Settings.instance().evaluationDate = today

        dc = ActualActual(ActualActual.ISDA)
        maturityDate = today + Period(12, Months)
        maturity = dc.yearFraction(today, maturityDate)

        irRate = 0.1
        rTS = flatRate(today, irRate, dc)
        payoff = PlainVanillaPayoff(Option.Call, 30)
        exercise = EuropeanExercise(maturityDate)

        engine = FdExtOUJumpVanillaEngine(jumpProcess, rTS, 25, 200, 50)

        option = VanillaOption(payoff, exercise)
        option.setPricingEngine(engine)
        fdNPV = option.NPV()

        steps = 100
        nrTrails = 200000
        grid = TimeGrid(maturity, steps)

        rsg = GaussianRandomSequenceGenerator(
            UniformRandomSequenceGenerator(
                jumpProcess.factors() * (len(grid) - 1),
                UniformRandomGenerator(421)))

        npv = GeneralStatistics()
        generator = GaussianMultiPathGenerator(jumpProcess, grid, rsg, false)

        for n in range(nrTrails):
            path = generator.next()

            x = path.value()[0].back()
            y = path.value()[1].back()

            cashflow = payoff(exp(x + y))
            npv.add(cashflow * rTS.discount(maturity))

        mcNPV = npv.mean()
        mcError = npv.errorEstimate()

        self.assertFalse(abs(fdNPV - mcNPV) > 3.0 * mcError)

    def testKlugeChFVanillaPricing(self):
        TEST_MESSAGE("Testing Kluge PDE Vanilla Pricing in"
                     " comparison to moment matching...")

        backup = SavedSettings()

        settlementDate = Date(22, November, 2019)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = Actual365Fixed()
        maturityDate = settlementDate + Period(6, Months)
        t = dayCounter.yearFraction(settlementDate, maturityDate)

        f0 = 30

        x0 = 0.0
        y0 = 0.0

        beta = 5.0
        eta = 5.0
        lmbd = 4.0
        alpha = 4.0
        sig = 1.0

        klugeProcess = ExtOUWithJumpsProcess(
            ExtendedOrnsteinUhlenbeckProcess(
                alpha, sig, x0,
                # constant<Real, Real>(0.0),
                lambda x: 0.0),
            y0, beta, lmbd, eta)

        strike = f0

        option = VanillaOption(
            PlainVanillaPayoff(Option.Call, strike),
            EuropeanExercise(maturityDate))

        shape = Shape()

        ps = log(f0) - \
             sig * sig / (4 * alpha) * (1 - exp(-2 * alpha * t)) - \
             lmbd / beta * log((eta - exp(-beta * t)) / (eta - 1.0))

        shape.push_back(DoublePair(t, ps))

        expected = RichardsonExtrapolation(
            SwingPdePricing(klugeProcess, option, shape), 4.0)(2.0, 1.5)

        stdDev = sqrt((((2 - 2 * exp(-2 * beta * t)) * lmbd)
                       / (beta * eta * eta) + ((1 - exp(-2 * alpha * t)) * sig * sig) / alpha) / 2.)

        bsNPV = blackFormula(Option.Call, strike, f0, stdDev)

        g1 = ((2 - 2 * exp(-3 * beta * t)) * lmbd) / (beta * eta * eta * eta) / (stdDev * stdDev * stdDev)

        g2 = 3 * (exp((alpha + beta) * t) *
                  (2 * alpha * exp(2 * alpha * t) * (-1 + exp(2 * beta * t)) * lmbd +
                   beta * exp(2 * beta * t) * (-1 + exp(2 * alpha * t)) * eta * eta * sig * sig) ** 2 +
                  16 * alpha * alpha * beta * exp((5 * alpha + 3 * beta) * t) * lmbd * sinh(2 * beta * t)) / \
             (4. * alpha * alpha * beta * beta * exp(5 * (alpha + beta) * t) * eta * eta * eta * eta) / \
             (stdDev * stdDev * stdDev * stdDev) - 3.0

        d = (log(f0 / strike) + 0.5 * stdDev * stdDev) / stdDev

        # Jurczenko E., Maillet B. and Negrea B.,
        # Multi-Moment Approximate Option Pricing Models:
        # A General Comparison (Part 1)
        # https:#papers.ssrn.com/sol3/papers.cfm?abstract_id=300922
        n = NormalDistribution()
        q3 = 1 / Factorial.get(3) * f0 * stdDev * (2 * stdDev - d) * n(d)
        q4 = 1 / Factorial.get(4) * f0 * stdDev * (d * d - 3 * d * stdDev - 1) * n(d)
        q5 = 10 / Factorial.get(6) * f0 * stdDev * (
                d * d * d * d - 5 * d * d * d * stdDev - 6 * d * d + 15 * d * stdDev + 3) * n(d)

        # Corrado C. and T. Su, (1996-b),
        # “Skewness and Kurtosis in S&P 500 IndexReturns Implied by Option Prices”,
        # Journal of Financial Research 19 (2), 175-192.
        ccs3 = bsNPV + g1 * q3
        ccs4 = ccs3 + g2 * q4

        # Rubinstein M., (1998), “Edgeworth Binomial Trees”,
        # Journal of Derivatives 5 (3), 20-27.
        cr = ccs4 + g1 * g1 * q5

        expectedImplVol = blackFormulaImpliedStdDevLiRS(
            Option.Call, strike, f0, expected, 1.0) / sqrt(t)

        bsImplVol = blackFormulaImpliedStdDevLiRS(
            Option.Call, strike, f0, bsNPV, 1.0) / sqrt(t)

        ccs3ImplVol = blackFormulaImpliedStdDevLiRS(
            Option.Call, strike, f0, ccs3, 1.0) / sqrt(t)

        ccs4ImplVol = blackFormulaImpliedStdDevLiRS(
            Option.Call, strike, f0, ccs4, 1.0) / sqrt(t)

        crImplVol = blackFormulaImpliedStdDevLiRS(
            Option.Call, strike, f0, cr, 1.0) / sqrt(t)

        tol = [0.01, 0.0075, 0.005, 0.004]
        methods = [
            "Second Order", "Third Order", "Fourth Order", "Rubinstein"]

        calculated = [bsImplVol, ccs3ImplVol, ccs4ImplVol, crImplVol]

        for i in range(4):
            diff = abs(calculated[i] - expectedImplVol)
            self.assertFalse(diff > tol[i])
