import unittest
from utilities import *
from QuantLib import *
from math import exp, sqrt, log, pow
import numpy as np


def getFixedLocalVolFromHeston(hestonModel,
                               timeGrid):
    trueImpliedVolSurf = BlackVolTermStructureHandle(
        HestonBlackVolSurface(
            HestonModelHandle(hestonModel),
            AnalyticHestonEngine.AndersenPiterbarg,
            AnalyticHestonEngineIntegration.gaussLaguerre(32)))

    hestonProcess = hestonModel.process()
    localVol = NoExceptLocalVolSurface(
        trueImpliedVolSurf,
        hestonProcess.riskFreeRate(),
        hestonProcess.dividendYield(),
        hestonProcess.s0(),
        sqrt(hestonProcess.theta()))

    localVolRND = LocalVolRNDCalculator(
        hestonProcess.s0().currentLink(),
        hestonProcess.riskFreeRate().currentLink(),
        hestonProcess.dividendYield().currentLink(),
        localVol, timeGrid)

    strikes = DoubleVectorVector()
    for i in range(1, len(timeGrid)):
        t = timeGrid.at(i)
        fdm1dMesher = localVolRND.mesher(t)
        logStrikes = fdm1dMesher.locations()
        strikeSlice = DoubleVector(len(logStrikes))

        for j in range(len(logStrikes)):
            strikeSlice[j] = exp(logStrikes[j])

        strikes.append(strikeSlice)

    nStrikes = len(strikes[0])
    localVolMatrix = Matrix(nStrikes, len(timeGrid) - 1)
    for i in range(1, len(timeGrid)):
        t = timeGrid.at(i)
        strikeSlice = strikes[i - 1]

        for j in range(nStrikes):
            s = strikeSlice[j]
            localVolMatrix[j][i - 1] = localVol.localVol(t, s, True)

    todaysDate = hestonProcess.riskFreeRate().referenceDate()
    dc = hestonProcess.riskFreeRate().dayCounter()
    expiries = DoubleVector(len(timeGrid) - 1)
    for i in range(1, len(timeGrid)):
        expiries[i - 1] = timeGrid[i]

    surface = FixedLocalVolSurface(
        todaysDate, expiries,
        strikes, localVolMatrix, dc)
    return surface


def hestonPxBoundary(maturity,
                     eps,
                     model):
    pdfEngine = AnalyticPDFHestonEngine(model)
    sInit = model.process().s0().value()

    def func(x):
        return pdfEngine.cdf(x, maturity) - eps

    return Brent().solve(
        func,
        sInit * 1e-3, sInit,
        sInit * 0.001,
        1000 * sInit)


class HestonModelParams(object):
    def __init__(self,
                 r, q,
                 kappa,
                 theta,
                 rho,
                 sigma,
                 v0):
        # r, q
        # kappa, theta, rho, sigma, v0
        self.r = r
        self.q = q
        self.kappa = kappa
        self.theta = theta
        self.rho = rho
        self.sigma = sigma
        self.v0 = v0


class HestonSLVTestCase(object):
    def __init__(self,
                 hestonParams,
                 fdmParams):
        self.hestonParams = hestonParams
        self.fdmParams = fdmParams


def createSmoothImpliedVol(dc, cal):
    todaysDate = Settings.instance().evaluationDate

    times = [13, 41, 75, 165, 256, 345, 524, 703]
    dates = DateVector()
    for time in times:
        date = todaysDate + Period(time, Days)
        dates.push_back(date)

    surfaceStrikes = [
        2.222222222, 11.11111111, 44.44444444, 75.55555556, 80,
        84.44444444, 88.88888889, 93.33333333, 97.77777778, 100,
        102.2222222, 106.6666667, 111.1111111, 115.5555556, 120,
        124.4444444, 166.6666667, 222.2222222, 444.4444444, 666.6666667]

    v = [1.015873, 1.015873, 0.915873, 0.89729, 0.796493, 0.730914, 0.631335, 0.568895,
         0.851309, 0.821309, 0.781309, 0.641309, 0.635593, 0.583653, 0.508045, 0.463182,
         0.686034, 0.630534, 0.590534, 0.500534, 0.448706, 0.416661, 0.375470, 0.353442,
         0.526034, 0.482263, 0.447713, 0.387703, 0.355064, 0.337438, 0.316966, 0.306859,
         0.497587, 0.464373, 0.430764, 0.374052, 0.344336, 0.328607, 0.310619, 0.301865,
         0.479511, 0.446815, 0.414194, 0.361010, 0.334204, 0.320301, 0.304664, 0.297180,
         0.461866, 0.429645, 0.398092, 0.348638, 0.324680, 0.312512, 0.299082, 0.292785,
         0.444801, 0.413014, 0.382634, 0.337026, 0.315788, 0.305239, 0.293855, 0.288660,
         0.428604, 0.397219, 0.368109, 0.326282, 0.307555, 0.298483, 0.288972, 0.284791,
         0.420971, 0.389782, 0.361317, 0.321274, 0.303697, 0.295302, 0.286655, 0.282948,
         0.413749, 0.382754, 0.354917, 0.316532, 0.300016, 0.292251, 0.284420, 0.281164,
         0.400889, 0.370272, 0.343525, 0.307904, 0.293204, 0.286549, 0.280189, 0.277767,
         0.390685, 0.360399, 0.334344, 0.300507, 0.287149, 0.281380, 0.276271, 0.274588,
         0.383477, 0.353434, 0.327580, 0.294408, 0.281867, 0.276746, 0.272655, 0.271617,
         0.379106, 0.349214, 0.323160, 0.289618, 0.277362, 0.272641, 0.269332, 0.268846,
         0.377073, 0.347258, 0.320776, 0.286077, 0.273617, 0.269057, 0.266293, 0.266265,
         0.399925, 0.369232, 0.338895, 0.289042, 0.265509, 0.255589, 0.249308, 0.249665,
         0.423432, 0.406891, 0.373720, 0.314667, 0.281009, 0.263281, 0.246451, 0.242166,
         0.453704, 0.453704, 0.453704, 0.381255, 0.334578, 0.305527, 0.268909, 0.251367,
         0.517748, 0.517748, 0.517748, 0.416577, 0.364770, 0.331595, 0.287423, 0.264285]

    blackVolMatrix = Matrix(len(surfaceStrikes), len(dates))
    for i in range(len(surfaceStrikes)):
        for j in range(len(dates)):
            blackVolMatrix[i][j] = v[i * len(dates) + j]

    volTS = BlackVarianceSurface(
        todaysDate, cal,
        dates,
        surfaceStrikes,
        blackVolMatrix,
        dc,
        BlackVarianceSurface.ConstantExtrapolation,
        BlackVarianceSurface.ConstantExtrapolation)
    volTS.setInterpolationBicubic()

    return surfaceStrikes, dates, volTS


class FokkerPlanckFwdTestCase(object):
    def __init__(self,
                 s0, r, q, v0,
                 kappa, theta, rho, sigma,
                 xGrid, vGrid, tGridPerYear,
                 tMinGridPerYear,
                 avgEps, eps,
                 trafoType,
                 greensAlgorithm,
                 schemeType):
        self.s0 = s0
        self.r = r
        self.q = q
        self.v0 = v0
        self.kappa = kappa
        self.theta = theta
        self.rho = rho
        self.sigma = sigma
        self.xGrid = xGrid
        self.vGrid = vGrid
        self.tGridPerYear = tGridPerYear
        self.tMinGridPerYear = tMinGridPerYear
        self.avgEps = avgEps
        self.eps = eps
        self.trafoType = trafoType
        self.greensAlgorithm = greensAlgorithm
        self.schemeType = schemeType


def stationaryLogProbabilityFct(kappa,
                                theta,
                                sigma,
                                z):
    alpha = 2 * kappa * theta / (sigma * sigma)
    beta = alpha / theta
    return pow(beta, alpha) * exp(z * alpha) * \
           exp(-beta * exp(z) - GammaFunction().logValue(alpha))


def createLocalVolMatrixFromProcess(lvProcess,
                                    strikes,
                                    dates,
                                    times):
    localVol = lvProcess.localVolatility().currentLink()

    dc = localVol.dayCounter()
    todaysDate = Settings.instance().evaluationDate

    for i in range(len(times)):
        times[i] = dc.yearFraction(todaysDate, dates[i])

    surface = Matrix(len(strikes), len(dates))

    for i in range(len(strikes)):
        for j in range(len(dates)):
            try:
                surface[i][j] = localVol.localVol(
                    dates[j], strikes[i], True)
            except RuntimeError as e:
                surface[i][j] = 0.2

    return surface


def createStationaryDistributionMesher(kappa,
                                       theta,
                                       sigma,
                                       vGrid):
    qMin = 0.01
    qMax = 0.99
    dq = (qMax - qMin) / (vGrid - 1)

    rnd = SquareRootProcessRNDCalculator(
        theta, kappa, theta, sigma)

    v = DoubleVector(vGrid)
    for i in range(len(v)):
        v[i] = rnd.stationary_invcdf(qMin + i * dq)

    return FdmMesherComposite(
        Predefined1dMesher(v))


def fokkerPlanckPrice1D(mesher,
                        op,
                        payoff,
                        x0,
                        maturity,
                        tGrid):
    x = mesher.locations(0)
    p = Array(len(x), 0.0)

    upperb = 0
    for i in x:
        if i <= x0:
            upperb += 1
        else:
            break
    lowerb = upperb - 1

    if close_enough(x[upperb], x0):
        idx = upperb
        dx = (x[idx + 1] - x[idx - 1]) / 2.0
        p[idx] = 1.0 / dx
    elif close_enough(x[lowerb], x0):
        idx = lowerb
        dx = (x[idx + 1] - x[idx - 1]) / 2.0
        p[idx] = 1.0 / dx
    else:
        dx = x[upperb] - x[lowerb]
        lowerP = (x[upperb] - x0) / dx
        upperP = (x0 - x[lowerb]) / dx

        lowerIdx = lowerb
        upperIdx = upperb

        lowerDx = (x[lowerIdx + 1] - x[lowerIdx - 1]) / 2.0
        upperDx = (x[upperIdx + 1] - x[upperIdx - 1]) / 2.0

        p[lowerIdx] = lowerP / lowerDx
        p[upperIdx] = upperP / upperDx

    evolver = DouglasScheme(
        FdmSchemeDesc.Douglas().theta, op)
    dt = maturity / tGrid
    evolver.setStep(dt)

    for t in np.arange(dt, maturity + 20 * QL_EPSILON, dt):
        evolver.step(p, t)

    payoffTimesDensity = Array(len(x))
    for i in range(len(x)):
        payoffTimesDensity[i] = payoff(exp(x[i])) * p[i]

    f = CubicNaturalSpline(x, payoffTimesDensity)
    f.enableExtrapolation()
    return GaussLobattoIntegral(1000, 1e-6)(
        f, x.front(), x.back())


def fokkerPlanckPrice2D(p, mesher):
    x = DoubleVector()
    y = DoubleVector()

    layout = mesher.layout()

    x.reserve(layout.dim()[0])
    y.reserve(layout.dim()[1])

    endIter = layout.end()
    ly = layout.begin()

    while ly.notEqual(endIter):
        if ly.coordinates()[1] == 0:
            x.push_back(mesher.location(ly, 0))
        if ly.coordinates()[0] == 0:
            y.push_back(mesher.location(ly, 1))

        ly.increment()

    simpson = DiscreteSimpsonIntegral()
    integral = SafeFdmMesherIntegral(mesher, simpson)
    r = integral.integrate(p)
    return r


class q_fct(object):
    def __init__(self, v, p, alpha):
        self.v_ = v
        self.q_ = Pow(v, alpha) * p
        self.alpha_ = alpha

        self.spline_ = CubicNaturalSpline(self.v_, self.q_)

    def __call__(self, v):
        return self.spline_(v, True) * pow(v, -self.alpha_)


class HestonSLVModelTest(unittest.TestCase):
    def _hestonFokkerPlanckFwdEquationTest(self,
                                           testCase):

        backup = SavedSettings()

        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(28, December, 2014)
        Settings.instance().evaluationDate = todaysDate

        maturities = [
            Period(1, Months), Period(3, Months),
            Period(6, Months), Period(9, Months),
            Period(1, Years), Period(2, Years), Period(3, Years)]

        maturityDate = todaysDate + maturities[-1]
        maturity = dc.yearFraction(todaysDate, maturityDate)

        s0 = testCase.s0
        x0 = log(s0)
        r = testCase.r
        q = testCase.q

        kappa = testCase.kappa
        theta = testCase.theta
        rho = testCase.rho
        sigma = testCase.sigma
        v0 = testCase.v0
        alpha = 1.0 - 2 * kappa * theta / (sigma * sigma)

        spot = QuoteHandle(SimpleQuote(s0))
        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        process = HestonProcess(rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        model = HestonModel(process)

        engine = AnalyticHestonEngine(model)

        xGrid = testCase.xGrid
        vGrid = testCase.vGrid
        tGridPerYear = testCase.tGridPerYear

        transformationType = testCase.trafoType
        cPoints = Concentrating1dMesherPointVector()

        rnd = SquareRootProcessRNDCalculator(
            v0, kappa, theta, sigma)
        lowerBound = None
        upperBound = None

        if transformationType == FdmSquareRootFwdOp.Log:
            upperBound = log(rnd.stationary_invcdf(0.9995))
            lowerBound = log(0.00001)

            v0Center = log(v0)
            v0Density = 10.0
            upperBoundDensity = 100
            lowerBoundDensity = 1.0

            cPoints.append(Concentrating1dMesherPoint(lowerBound, lowerBoundDensity, false))
            cPoints.append(Concentrating1dMesherPoint(v0Center, v0Density, True))
            cPoints.append(Concentrating1dMesherPoint(upperBound, upperBoundDensity, false))

        elif transformationType == FdmSquareRootFwdOp.Plain:
            upperBound = rnd.stationary_invcdf(0.9995)
            lowerBound = rnd.stationary_invcdf(1e-5)

            v0Center = v0
            v0Density = 0.1
            lowerBoundDensity = 0.0001

            cPoints.append(Concentrating1dMesherPoint(lowerBound, lowerBoundDensity, false))
            cPoints.append(Concentrating1dMesherPoint(v0Center, v0Density, True))

        elif transformationType == FdmSquareRootFwdOp.Power:
            upperBound = rnd.stationary_invcdf(0.9995)
            lowerBound = 0.000075

            v0Center = v0
            v0Density = 1.0
            lowerBoundDensity = 0.005
            cPoints.push_back(Concentrating1dMesherPoint(lowerBound, lowerBoundDensity, false))
            cPoints.push_back(Concentrating1dMesherPoint(v0Center, v0Density, True))

        varianceMesher = Concentrating1dMesher(
            lowerBound, upperBound,
            vGrid, cPoints, 1e-12)

        sEps = 1e-4
        sLowerBound = log(hestonPxBoundary(maturity, sEps, model))
        sUpperBound = log(hestonPxBoundary(maturity, 1 - sEps, model))

        spotMesher = Concentrating1dMesher(
            sLowerBound, sUpperBound, xGrid,
            (x0, 0.1), True)

        mesher = FdmMesherComposite(
            spotMesher, varianceMesher)

        hestonFwdOp = FdmHestonFwdOp(
            mesher, process, transformationType)

        evolver = ModifiedCraigSneydScheme(
            FdmSchemeDesc.ModifiedCraigSneyd().theta,
            FdmSchemeDesc.ModifiedCraigSneyd().mu,
            hestonFwdOp)

        #  step one days using non-correlated process
        eT = 1.0 / 365
        p = FdmHestonGreensFct(
            mesher, process, testCase.trafoType).get(
            eT, testCase.greensAlgorithm)

        layout = mesher.layout()
        strikes = [50, 80, 90, 100, 110, 120, 150, 200]

        t = eT

        for maturitie in maturities:
            #  calculate step size
            nextMaturityDate = todaysDate + maturitie
            nextMaturityTime = dc.yearFraction(
                todaysDate, nextMaturityDate)

            dt = (nextMaturityTime - t) / tGridPerYear
            evolver.setStep(dt)

            for i in range(tGridPerYear):
                evolver.step(p, t + dt)
                t += dt

            avg = 0
            minv = QL_MAX_REAL
            maxv = 0
            for strike in strikes:
                payoff = PlainVanillaPayoff(
                    Option.Call if strike > s0 else Option.Put,
                    strike)

                pd = Array(len(p))

                ly = layout.begin()
                while ly.notEqual(layout.end()):
                    idx = ly.index()
                    s = exp(mesher.location(ly, 0))

                    pd[idx] = payoff(s) * p[idx]
                    if transformationType == FdmSquareRootFwdOp.Power:
                        v = mesher.location(ly, 1)
                        pd[idx] *= pow(v, -alpha)
                    ly.increment()

                calculated = fokkerPlanckPrice2D(pd, mesher) * rTS.discount(nextMaturityDate)

                exercise = EuropeanExercise(nextMaturityDate)

                option = VanillaOption(payoff, exercise)
                option.setPricingEngine(engine)

                expected = option.NPV()
                absDiff = abs(expected - calculated)
                relDiff = absDiff / max(QL_EPSILON, expected)
                diff = min(absDiff, relDiff)

                avg += diff
                minv = min(diff, minv)
                maxv = max(diff, maxv)

                self.assertFalse(diff > testCase.eps)

                avg /= len(strikes)

                self.assertFalse(avg > testCase.avgEps)

    def _lsvCalibrationTest(self,
                            testCase):
        todaysDate = Date(2, June, 2015)
        Settings.instance().evaluationDate = todaysDate
        finalDate = Date(2, June, 2020)

        dc = Actual365Fixed()

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))

        r = testCase.hestonParams.r
        q = testCase.hestonParams.q

        kappa = testCase.hestonParams.kappa
        theta = testCase.hestonParams.theta
        rho = testCase.hestonParams.rho
        sigma = testCase.hestonParams.sigma
        v0 = testCase.hestonParams.v0
        lv = 0.3

        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        hestonProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        hestonModel = HestonModelHandle(
            HestonModel(hestonProcess))

        localVol = LocalVolTermStructureHandle(
            LocalConstantVol(todaysDate, lv, dc))

        slvModel = HestonSLVFDMModel(
            localVol, hestonModel, finalDate, testCase.fdmParams)

        #  this includes a calibration of the leverage function!
        l = slvModel.leverageFunction()

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS,
            BlackVolTermStructureHandle(
                flatVol(lv, dc)))

        analyticEngine = AnalyticEuropeanEngine(bsProcess)

        strikes = [50, 75, 80, 90, 100, 110, 125, 150]
        times = [3, 6, 9, 12, 24, 36, 60]

        for time in times:
            expiry = todaysDate + Period(time, Months)
            exercise = EuropeanExercise(expiry)

            slvEngine = FdHestonVanillaEngine(
                hestonModel.currentLink(),
                int(max(101.0, 51 * time / 12.0)), 401, 101, 0,
                FdmSchemeDesc.ModifiedCraigSneyd(), l) \
                if time <= 3 else \
                FdHestonVanillaEngine(
                    hestonModel.currentLink(),
                    int(max(51.0, 51 * time / 12.0)), 201, 101, 0,
                    FdmSchemeDesc.ModifiedCraigSneyd(), l)

            for strike in strikes:
                payoff = PlainVanillaPayoff(
                    Option.Call if strike > s0 else Option.Put,
                    strike)

                option = VanillaOption(payoff, exercise)

                option.setPricingEngine(slvEngine)
                calculated = option.NPV()

                option.setPricingEngine(analyticEngine)
                expected = option.NPV()
                vega = option.vega()

                bp = GeneralizedBlackScholesProcess(
                    spot, qTS, rTS,
                    BlackVolTermStructureHandle(
                        flatVol(lv, dc)))

                tol = 0.001  # testCase.eps
                self.assertFalse(
                    abs((calculated - expected) / vega) > tol)

    def testBlackScholesFokkerPlanckFwdEquation(self):
        TEST_MESSAGE(
            "Testing Fokker-Planck forward equation for BS process...")

        backup = SavedSettings()

        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(28, December, 2012)
        Settings.instance().evaluationDate = todaysDate
        maturityDate = todaysDate + Period(2, Years)
        maturity = dc.yearFraction(todaysDate, maturityDate)

        s0 = 100
        x0 = log(s0)
        r = 0.035
        q = 0.01
        v = 0.35

        xGrid = 2 * 100 + 1
        tGrid = 400

        spot = QuoteHandle(SimpleQuote(s0))
        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))
        vTS = BlackVolTermStructureHandle(flatVol(v, dc))

        process = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, vTS)

        engine = AnalyticEuropeanEngine(process)

        uniformMesher = FdmMesherComposite(
            FdmBlackScholesMesher(
                xGrid, process, maturity, s0))

        uniformBSFwdOp = FdmBlackScholesFwdOp(
            uniformMesher, process, s0, False)

        concentratedMesher = FdmMesherComposite(
            FdmBlackScholesMesher(
                xGrid, process, maturity, s0,
                NullReal(), NullReal(), 0.0001, 1.5,
                (s0, 0.1)))

        concentratedBSFwdOp = FdmBlackScholesFwdOp(
            concentratedMesher, process, s0, False)

        shiftedMesher = FdmMesherComposite(
            FdmBlackScholesMesher(
                xGrid, process, maturity, s0,
                NullReal(), NullReal(), 0.0001, 1.5,
                (s0 * 1.1, 0.2)))

        shiftedBSFwdOp = FdmBlackScholesFwdOp(
            shiftedMesher, process, s0, False)

        exercise = EuropeanExercise(maturityDate)

        strikes = [50, 80, 100, 130, 150]

        for strike in strikes:
            payoff = PlainVanillaPayoff(Option.Call, strike)
            option = VanillaOption(payoff, exercise)
            option.setPricingEngine(engine)

            expected = option.NPV() / rTS.discount(maturityDate)
            calcUniform = fokkerPlanckPrice1D(
                uniformMesher, uniformBSFwdOp,
                payoff, x0, maturity, tGrid)
            calcConcentrated = fokkerPlanckPrice1D(
                concentratedMesher, concentratedBSFwdOp,
                payoff, x0, maturity, tGrid)
            calcShifted = fokkerPlanckPrice1D(
                shiftedMesher, shiftedBSFwdOp,
                payoff, x0, maturity, tGrid)
            tol = 0.02

            self.assertFalse(abs(expected - calcUniform) > tol)
            self.assertFalse(abs(expected - calcConcentrated) > tol)
            self.assertFalse(abs(expected - calcShifted) > tol)

    def testSquareRootZeroFlowBC(self):
        TEST_MESSAGE(
            "Testing zero-flow BC for the square root process...")

        backup = SavedSettings()

        kappa = 1.0
        theta = 0.4
        sigma = 0.8
        v_0 = 0.1
        t = 1.0

        vmin = 0.0005
        h = 0.0001

        expected = [
            [0.000548, -0.000245, -0.005657, -0.001167, -0.000024],
            [-0.000595, -0.000701, -0.003296, -0.000883, -0.000691],
            [-0.001277, -0.001320, -0.003128, -0.001399, -0.001318],
            [-0.001979, -0.002002, -0.003425, -0.002047, -0.002001],
            [-0.002715, -0.002730, -0.003920, -0.002760, -0.002730]]

        for i in range(5):
            v = vmin + i * 0.001
            vm2 = v - 2 * h
            vm1 = v - h
            v0 = v
            v1 = v + h
            v2 = v + 2 * h

            rndCalculator = SquareRootProcessRNDCalculator(
                v_0, kappa, theta, sigma)

            pm2 = rndCalculator.pdf(vm2, t)
            pm1 = rndCalculator.pdf(vm1, t)
            p0 = rndCalculator.pdf(v0, t)
            p1 = rndCalculator.pdf(v1, t)
            p2 = rndCalculator.pdf(v2, t)

            # test derivatives
            flowSym2Order = sigma * sigma * v0 / (4 * h) * (p1 - pm1) + (kappa * (v0 - theta) + sigma * sigma / 2) * p0
            flowSym4Order = sigma * sigma * v0 / (24 * h) * (-p2 + 8 * p1 - 8 * pm1 + pm2) + (kappa * (v0 - theta) + sigma * sigma / 2) * p0
            fwd1Order = sigma * sigma * v0 / (2 * h) * (p1 - p0) + (kappa * (v0 - theta) + sigma * sigma / 2) * p0
            fwd2Order = sigma * sigma * v0 / (4 * h) * (4 * p1 - 3 * p0 - p2) + (kappa * (v0 - theta) + sigma * sigma / 2) * p0
            fwd3Order = sigma * sigma * v0 / (12 * h) * (-p2 + 6 * p1 - 3 * p0 - 2 * pm1) + (kappa * (v0 - theta) + sigma * sigma / 2) * p0

            tol = 0.000002

            self.assertFalse(
                abs(expected[i][0] - flowSym2Order) > tol or
                abs(expected[i][1] - flowSym4Order) > tol or
                abs(expected[i][2] - fwd1Order) > tol or
                abs(expected[i][3] - fwd2Order) > tol or
                abs(expected[i][4] - fwd3Order) > tol)

    def testTransformedZeroFlowBC(self):
        TEST_MESSAGE(
            "Testing zero-flow BC for transformed Fokker-Planck forward equation...")

        backup = SavedSettings()
        kappa = 1.0
        theta = 0.4
        sigma = 2.0
        vGrid = 100

        mesher = createStationaryDistributionMesher(
            kappa, theta, sigma, vGrid)
        v = mesher.locations(0)

        p = Array(vGrid)
        rnd = SquareRootProcessRNDCalculator(
            theta, kappa, theta, sigma)

        for i in range(len(v)):
            p[i] = rnd.stationary_pdf(v[i])

        alpha = 1.0 - 2 * kappa * theta / (sigma * sigma)
        q = Pow(v, alpha) * p

        for i in range(int(vGrid / 2)):
            hm = v[i + 1] - v[i]
            hp = v[i + 2] - v[i + 1]

            eta = 1.0 / (hm * (hm + hp) * hp)
            a = -eta * ((hm + hp) ** 2 - hm * hm)
            b = eta * (hm + hp) ** 2
            c = -eta * hm * hm

            df = a * q[i] + b * q[i + 1] + c * q[i + 2]
            flow = 0.5 * sigma * sigma * v[i] * df + kappa * v[i] * q[i]

            tol = 1e-6
            self.assertFalse(abs(flow) > tol)

    def testSquareRootEvolveWithStationaryDensity(self):
        TEST_MESSAGE(
            "Testing Fokker-Planck forward equation for the square root process with stationary density...")

        # Documentation for this test case:
        # http://www.spanderen.de/2013/05/04/fokker-planck-equation-feller-constraint-and-boundary-conditions/

        backup = SavedSettings()

        kappa = 2.5
        theta = 0.2
        vGrid = 100
        eps = 1e-2

        for sigma in np.arange(0.2, 2.01, 0.1):
            alpha = (1.0 - 2 * kappa * theta / (sigma * sigma))

            rnd = SquareRootProcessRNDCalculator(
                theta, kappa, theta, sigma)
            vMin = rnd.stationary_invcdf(eps)
            vMax = rnd.stationary_invcdf(1 - eps)

            mesher = FdmMesherComposite(
                Uniform1dMesher(vMin, vMax, vGrid))

            v = mesher.locations(0)

            transform = FdmSquareRootFwdOp.Plain \
                if sigma < 0.75 else \
                FdmSquareRootFwdOp.Power

            vq = Array(len(v))
            vmq = Array(len(v))

            for i in range(len(v)):
                vq[i] = pow(v[i], alpha)
                vmq[i] = 1.0 / vq[i]

            p = Array(vGrid)

            for i in range(len(v)):
                p[i] = rnd.stationary_pdf(v[i])
                if transform == FdmSquareRootFwdOp.Power:
                    p[i] *= vq[i]

            op = FdmSquareRootFwdOp(
                mesher, kappa, theta,
                sigma, 0, transform)

            n = 100
            dt = 0.01
            evolver = DouglasScheme(0.5, op)
            evolver.setStep(dt)

            for i in range(1, n + 1):
                evolver.step(p, i * dt)

            expected = 1 - 2 * eps

            if transform == FdmSquareRootFwdOp.Power:
                for i in range(len(v)):
                    p[i] *= vmq[i]

            f = q_fct(v, p, alpha)

            calculated = GaussLobattoIntegral(1000000, 1e-6)(
                f, v.front(), v.back())

            tol = 0.005
            self.assertFalse(
                abs(calculated - expected) > tol)

    def testSquareRootLogEvolveWithStationaryDensity(self):
        TEST_MESSAGE(
            "Testing Fokker-Planck forward equation for the square root log process with stationary density...")

        # Documentation for this test case:
        # nowhere yet :)

        backup = SavedSettings()

        kappa = 2.5
        theta = 0.2
        vGrid = 1000
        eps = 1e-2

        for sigma in np.arange(0.2, 2.01, 0.1):
            lowerLimit = 0.001
            # should not go to very large negative values, distributions flattens with sigma
            # causing numerical instabilities log/exp evaluations

            rnd = SquareRootProcessRNDCalculator(
                theta, kappa, theta, sigma)

            vMin = max(lowerLimit, rnd.stationary_invcdf(eps))
            lowEps = max(eps, rnd.stationary_cdf(lowerLimit))

            expected = 1 - eps - lowEps
            vMax = rnd.stationary_invcdf(1 - eps)

            um = Uniform1dMesher(
                log(vMin), log(vMax), vGrid)

            mesher = FdmMesherComposite(um)

            v = mesher.locations(0)
            p = Array(vGrid)
            for i in range(len(v)):
                p[i] = stationaryLogProbabilityFct(
                    kappa, theta, sigma, v[i])

            op = FdmSquareRootFwdOp(
                mesher, kappa, theta, sigma, 0,
                FdmSquareRootFwdOp.Log)

            n = 100
            dt = 0.01
            bcSet = FdmBoundaryConditionSet()
            evolver = DouglasScheme(0.5, op)
            evolver.setStep(dt)

            for i in range(1, n + 1):
                evolver.step(p, i * dt)

            s = DiscreteSimpsonIntegral()
            il = SafeFdmMesherIntegral(
                mesher, s)

            calculated = il.integrate(p)

            tol = 0.005

            self.assertFalse(abs(calculated - expected) > tol)

    def testSquareRootFokkerPlanckFwdEquation(self):
        TEST_MESSAGE(
            "Testing Fokker-Planck forward equation for the square root process with Dirac start...")

        backup = SavedSettings()

        kappa = 1.2
        theta = 0.4
        sigma = 0.7
        v0 = theta
        alpha = 1.0 - 2 * kappa * theta / (sigma * sigma)

        maturity = 1.0

        xGrid = 1001
        tGrid = 500

        vol = sigma * sqrt(theta / (2 * kappa))
        upperBound = theta + 6 * vol
        lowerBound = max(0.0002, theta - 6 * vol)

        mesher = FdmMesherComposite(
            Uniform1dMesher(
                lowerBound, upperBound, xGrid))

        x = Array(mesher.locations(0))

        op = FdmSquareRootFwdOp(
            mesher, kappa, theta, sigma, 0)

        dt = maturity / tGrid
        n = 5

        p = Array(xGrid)
        rndCalculator = SquareRootProcessRNDCalculator(
            v0, kappa, theta, sigma)
        for i in range(len(p)):
            p[i] = rndCalculator.pdf(x[i], n * dt)

        q = Pow(x, alpha) * p

        evolver = DouglasScheme(0.5, op)
        evolver.setStep(dt)

        for t in np.arange((n + 1) * dt, maturity + 20 * QL_EPSILON, dt):
            evolver.step(p, t)
            evolver.step(q, t)

        tol = 0.002

        y = Array(len(x))

        for i in range(len(x)):
            expected = rndCalculator.pdf(x[i], maturity)
            calculated = p[i]

            self.assertFalse(abs(expected - calculated) > tol)

    @unittest.skipIf(skipSlowTest, "testHestonFokkerPlanckFwdEquation is VERY SLOW")
    def testHestonFokkerPlanckFwdEquation(self):
        TEST_MESSAGE(
            "Testing Fokker-Planck forward equation for the Heston process...")

        testCases = [
            FokkerPlanckFwdTestCase(
                100.0, 0.01, 0.02,
                # Feller constraint violated, high vol-of-vol case
                # \frac[2\kappa\theta][\sigma^2] = 2.0 * 1.0 * 0.05 / 0.2 = 0.5 < 1
                0.05, 1.0, 0.05, -0.75, sqrt(0.2),
                101, 401, 25, 25,
                0.02, 0.05,
                FdmSquareRootFwdOp.Power,
                FdmHestonGreensFct.Gaussian,
                FdmSchemeDesc.DouglasType),
            FokkerPlanckFwdTestCase(
                100.0, 0.01, 0.02,
                # Feller constraint violated, high vol-of-vol case
                # \frac[2\kappa\theta][\sigma^2] = 2.0 * 1.0 * 0.05 / 0.2 = 0.5 < 1
                0.05, 1.0, 0.05, -0.75, sqrt(0.2),
                201, 501, 10, 10,
                0.005, 0.02,
                FdmSquareRootFwdOp.Log,
                FdmHestonGreensFct.Gaussian,
                FdmSchemeDesc.HundsdorferType),
            FokkerPlanckFwdTestCase(
                100.0, 0.01, 0.02,
                # Feller constraint violated, high vol-of-vol case
                # \frac[2\kappa\theta][\sigma^2] = 2.0 * 1.0 * 0.05 / 0.2 = 0.5 < 1
                0.05, 1.0, 0.05, -0.75, sqrt(0.2),
                201, 501, 25, 25,
                0.01, 0.03,
                FdmSquareRootFwdOp.Log,
                FdmHestonGreensFct.ZeroCorrelation,
                FdmSchemeDesc.HundsdorferType),
            FokkerPlanckFwdTestCase(
                100.0, 0.01, 0.02,
                #  Feller constraint fulfilled, low vol-of-vol case
                #  \frac[2\kappa\theta][\sigma^2] = 2.0 * 1.0 * 0.05 / 0.05 = 2.0 > 1
                0.05, 1.0, 0.05, -0.75, sqrt(0.05),
                201, 401, 5, 5,
                0.01, 0.02,
                FdmSquareRootFwdOp.Plain,
                FdmHestonGreensFct.Gaussian,
                FdmSchemeDesc.HundsdorferType)]

        for testCase in testCases:
            self._hestonFokkerPlanckFwdEquationTest(testCase)

    def testHestonFokkerPlanckFwdEquationLogLVLeverage(self):
        TEST_MESSAGE(
            "Testing Fokker-Planck forward equation for the Heston process Log Transformation with leverage LV limiting case...")

        backup = SavedSettings()
        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(28, December, 2012)
        Settings.instance().evaluationDate = todaysDate

        maturityDate = todaysDate + Period(1, Years)
        maturity = dc.yearFraction(todaysDate, maturityDate)

        s0 = 100
        x0 = log(s0)
        r = 0.0
        q = 0.0

        kappa = 1.0
        theta = 1.0
        rho = -0.75
        sigma = 0.02
        v0 = theta

        transform = FdmSquareRootFwdOp.Plain

        dayCounter = Actual365Fixed()
        calendar = TARGET()

        spot = QuoteHandle(SimpleQuote(s0))
        rTS = YieldTermStructureHandle(
            flatRate(todaysDate, r, dayCounter))
        qTS = YieldTermStructureHandle(
            flatRate(todaysDate, q, dayCounter))

        hestonProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        xGrid = 201
        vGrid = 401
        tGrid = 25

        rnd = SquareRootProcessRNDCalculator(
            v0, kappa, theta, sigma)

        upperBound = rnd.stationary_invcdf(0.99)
        lowerBound = rnd.stationary_invcdf(0.01)

        beta = 10.0
        critPoints = Concentrating1dMesherPointVector()
        critPoints.push_back(Concentrating1dMesherPoint(lowerBound, beta, True))
        critPoints.push_back(Concentrating1dMesherPoint(v0, beta / 100, True))
        critPoints.push_back(Concentrating1dMesherPoint(upperBound, beta, True))

        varianceMesher = Concentrating1dMesher(
            lowerBound, upperBound, vGrid, critPoints)

        equityMesher = Concentrating1dMesher(
            log(2.0), log(600.0), xGrid,
            (x0 + 0.005, 0.1), True)

        mesher = FdmMesherComposite(
            equityMesher, varianceMesher)
        smoothSurface = createSmoothImpliedVol(
            dayCounter, calendar)
        lvProcess = BlackScholesMertonProcess(
            spot, qTS, rTS,
            BlackVolTermStructureHandle(
                smoothSurface[2]))

        #  step two days using non-correlated process
        eT = 2.0 / 365

        v = -NullReal()
        p_v = 0.0
        p = Array(mesher.layout().size(), 0.0)
        bsV0 = (lvProcess.blackVolatility().blackVol(0.0, s0, True)) ** 2
        rndCalculator = SquareRootProcessRNDCalculator(
            v0, kappa, theta, sigma)
        layout = mesher.layout()
        ly = layout.begin()
        while ly.notEqual(layout.end()):
            x = mesher.location(ly, 0)
            if v != mesher.location(ly, 1):
                v = mesher.location(ly, 1)
                #  the extreme tail probabilities of the non central
                #  chi square distribution lead to numerical exceptions
                #  on some platforms
                if abs(v - v0) < 5 * sigma * sqrt(v0 * eT):
                    p_v = rndCalculator.pdf(v, eT)
                else:
                    p_v = 0.0

            p_x = 1.0 / (sqrt(M_TWOPI * bsV0 * eT)) * exp(-0.5 * (x - x0) ** 2 / (bsV0 * eT))
            p[ly.index()] = p_v * p_x
            ly.increment()

        dt = (maturity - eT) / tGrid

        denseStrikes = [
            2.222222222, 11.11111111, 20, 25, 30, 35, 40,
            44.44444444, 50, 55, 60, 65, 70, 75.55555556,
            80, 84.44444444, 88.88888889, 93.33333333, 97.77777778, 100,
            102.2222222, 106.6666667, 111.1111111, 115.5555556, 120,
            124.4444444, 166.6666667, 222.2222222, 444.4444444, 666.6666667]

        surface = Matrix(len(denseStrikes), len(smoothSurface[1]))
        times = DoubleVector(surface.columns())

        dates = smoothSurface[1]
        m = createLocalVolMatrixFromProcess(
            lvProcess, denseStrikes, dates, times)

        leverage = FixedLocalVolSurface(
            todaysDate, dates, denseStrikes, m, dc)

        lvEngine = AnalyticEuropeanEngine(lvProcess)

        hestonFwdOp = FdmHestonFwdOp(
            mesher, hestonProcess, transform, leverage)

        evolver = HundsdorferScheme(
            FdmSchemeDesc.Hundsdorfer().theta,
            FdmSchemeDesc.Hundsdorfer().mu,
            hestonFwdOp)

        t = dt
        evolver.setStep(dt)

        for i in range(tGrid):
            evolver.step(p, t)
            t += dt

        exercise = EuropeanExercise(maturityDate)

        fdmEngine = FdBlackScholesVanillaEngine(
            lvProcess, 50, 201, 0,
            FdmSchemeDesc.Douglas(),
            True, 0.2)

        for strike in range(5, 200, 10):
            payoff = CashOrNothingPayoff(
                Option.Put, strike, 1.0)

            pd = Array(len(p))
            ly = layout.begin()
            while ly.notEqual(layout.end()):
                idx = ly.index()
                s = exp(mesher.location(ly, 0))

                pd[idx] = payoff(s) * p[idx]
                ly.increment()

            calculated = fokkerPlanckPrice2D(pd, mesher) * rTS.discount(maturityDate)

            option = VanillaOption(payoff, exercise)
            option.setPricingEngine(fdmEngine)
            expected = option.NPV()

            tol = 0.015
            self.assertFalse(abs(expected - calculated) > tol)

    def testBlackScholesFokkerPlanckFwdEquationLocalVol(self):
        TEST_MESSAGE(
            "Testing Fokker-Planck forward equation for BS Local Vol process...")

        backup = SavedSettings()
        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(5, July, 2014)
        Settings.instance().evaluationDate = todaysDate

        s0 = 100
        x0 = log(s0)
        r = 0.035
        q = 0.01

        calendar = TARGET()
        dayCounter = Actual365Fixed()

        rTS = YieldTermStructureHandle(
            flatRate(todaysDate, r, dayCounter))
        qTS = YieldTermStructureHandle(
            flatRate(todaysDate, q, dayCounter))

        smoothImpliedVol = createSmoothImpliedVol(
            dayCounter, calendar)

        strikes = smoothImpliedVol[0]
        dates = smoothImpliedVol[1]
        vTS = BlackVolTermStructureHandle(
            smoothImpliedVol[2])

        xGrid = 101
        tGrid = 51

        spot = QuoteHandle(SimpleQuote(s0))
        process = BlackScholesMertonProcess(
            spot, qTS, rTS, vTS)

        localVol = NoExceptLocalVolSurface(
            vTS, rTS, qTS, spot, 0.2)

        engine = AnalyticEuropeanEngine(process)

        for i in range(1, len(dates), 2):
            for j in range(3, len(strikes) - 3, 2):
                exDate = dates[i]
                maturityDate = exDate
                maturity = dc.yearFraction(todaysDate, maturityDate)
                exercise = EuropeanExercise(exDate)

                uniformMesher = FdmMesherComposite(
                    FdmBlackScholesMesher(
                        xGrid, process,
                        maturity, s0))

                # -- operator --
                uniformBSFwdOp = FdmLocalVolFwdOp(
                    uniformMesher,
                    spot.currentLink(),
                    rTS.currentLink(),
                    qTS.currentLink(),
                    localVol)

                concentratedMesher = FdmMesherComposite(
                    FdmBlackScholesMesher(
                        xGrid, process, maturity, s0,
                        NullReal(), NullReal(),
                        0.0001, 1.5, (s0, 0.1)))

                # -- operator --
                concentratedBSFwdOp = FdmLocalVolFwdOp(
                    concentratedMesher,
                    spot.currentLink(),
                    rTS.currentLink(),
                    qTS.currentLink(),
                    localVol)

                shiftedMesher = FdmMesherComposite(
                    FdmBlackScholesMesher(
                        xGrid, process, maturity, s0,
                        NullReal(), NullReal(),
                        0.0001, 1.5, (s0 * 1.1, 0.2)))

                # -- operator --
                shiftedBSFwdOp = FdmLocalVolFwdOp(
                    shiftedMesher,
                    spot.currentLink(),
                    rTS.currentLink(),
                    qTS.currentLink(),
                    localVol)

                payoff = PlainVanillaPayoff(
                    Option.Call, strikes[j])

                option = VanillaOption(payoff, exercise)
                option.setPricingEngine(engine)

                expected = option.NPV()
                calcUniform = fokkerPlanckPrice1D(
                    uniformMesher, uniformBSFwdOp, payoff,
                    x0, maturity, tGrid) * rTS.discount(maturityDate)
                calcConcentrated = fokkerPlanckPrice1D(
                    concentratedMesher, concentratedBSFwdOp,
                    payoff, x0, maturity, tGrid) * rTS.discount(maturityDate)
                calcShifted = fokkerPlanckPrice1D(
                    shiftedMesher, shiftedBSFwdOp, payoff,
                    x0, maturity, tGrid) * rTS.discount(maturityDate)
                tol = 0.05

                self.assertFalse(abs(expected - calcUniform) > tol)
                self.assertFalse(abs(expected - calcConcentrated) > tol)
                self.assertFalse(abs(expected - calcShifted) > tol)

    @unittest.skipIf(skipSlowTest, "testFDMCalibration is VERY SLOW")
    def testFDMCalibration(self):
        TEST_MESSAGE(
            "Testing stochastic local volatility calibration case ")

        backup = SavedSettings()
        plainParams = HestonSLVFokkerPlanckFdmParams(
            201, 301, 1000, 25, 3.0, 0, 2,
            0.1, 1e-4, 10000,
            1e-8, 1e-8, 0.0, 1.0, 1.0, 1.0, 1e-6,
            FdmHestonGreensFct.Gaussian,
            FdmSquareRootFwdOp.Plain,
            FdmSchemeDesc.ModifiedCraigSneyd())

        logParams = HestonSLVFokkerPlanckFdmParams(
            301, 601, 2000, 30, 2.0, 0, 2,
            0.1, 1e-4, 10000,
            1e-5, 1e-5, 0.0000025, 1.0, 0.1, 0.9, 1e-5,
            FdmHestonGreensFct.Gaussian,
            FdmSquareRootFwdOp.Log,
            FdmSchemeDesc.ModifiedCraigSneyd())

        powerParams = HestonSLVFokkerPlanckFdmParams(
            401, 801, 2000, 30, 2.0, 0, 2,
            0.1, 1e-3, 10000,
            1e-6, 1e-6, 0.001, 1.0, 0.001, 1.0, 1e-5,
            FdmHestonGreensFct.Gaussian,
            FdmSquareRootFwdOp.Power,
            FdmSchemeDesc.ModifiedCraigSneyd())

        testCases = [
            HestonSLVTestCase(HestonModelParams(0.035, 0.01, 1.0, 0.06, -0.75, 0.1, 0.09), plainParams),
            HestonSLVTestCase(HestonModelParams(0.035, 0.01, 1.0, 0.06, -0.75, sqrt(0.2), 0.09), logParams),
            HestonSLVTestCase(HestonModelParams(0.035, 0.01, 1.0, 0.09, -0.75, sqrt(0.2), 0.06), logParams),
            HestonSLVTestCase(HestonModelParams(0.035, 0.01, 1.0, 0.06, -0.75, 0.2, 0.09), powerParams)]

        for i in range(len(testCases)):
            self._lsvCalibrationTest(testCases[i])

    def testLocalVolsvSLVPropDensity(self):
        TEST_MESSAGE(
            "Testing local volatility vs SLV model...")

        backup = SavedSettings()
        todaysDate = Date(5, October, 2015)
        finalDate = todaysDate + Period(1, Years)
        Settings.instance().evaluationDate = todaysDate

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))
        r = 0.01
        q = 0.02

        calendar = TARGET()
        dayCounter = Actual365Fixed()

        rTS = YieldTermStructureHandle(
            flatRate(todaysDate, r, dayCounter))
        qTS = YieldTermStructureHandle(
            flatRate(todaysDate, q, dayCounter))

        vTS = BlackVolTermStructureHandle(
            createSmoothImpliedVol(dayCounter, calendar)[2])

        #  Heston parameter from implied calibration
        kappa = 2.0
        theta = 0.074
        rho = -0.51
        sigma = 0.8
        v0 = 0.1974

        hestonProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        hestonModel = HestonModelHandle(
            HestonModel(hestonProcess))

        localVol = LocalVolTermStructureHandle(
            NoExceptLocalVolSurface(
                vTS, rTS, qTS, spot, 0.3))
        localVol.enableExtrapolation(True)

        vGrid = 151
        xGrid = 51

        fdmParams = HestonSLVFokkerPlanckFdmParams(
            xGrid, vGrid, 500, 50, 100.0, 5, 2,
            0.1, 1e-4, 10000,
            1e-5, 1e-5, 0.0000025,
            1.0, 0.1, 0.9, 1e-5,
            FdmHestonGreensFct.ZeroCorrelation,
            FdmSquareRootFwdOp.Log,
            FdmSchemeDesc.ModifiedCraigSneyd())

        slvModel = HestonSLVFDMModel(
            localVol, hestonModel, finalDate, fdmParams, True)

        logEntryVector = slvModel.logEntryVector()

        squareRootRndCalculator = SquareRootProcessRNDCalculator(
            v0, kappa, theta, sigma)

        for logEntrie in logEntryVector:
            t = logEntrie.t
            if t > 0.2:
                x = Array(
                    logEntrie.mesher.getFdm1dMeshers()[0].locations())
                z = logEntrie.mesher.getFdm1dMeshers()[1].locations()
                prob = logEntrie.prob

                for i in range(len(z)):
                    tmp = Array(xGrid)
                    for j in range(i * xGrid, (i + 1) * xGrid):
                        tmp[j - i * xGrid] = prob[j]
                    pCalc = DiscreteSimpsonIntegral()(x, tmp)

                    expected = squareRootRndCalculator.pdf(exp(z[i]), t)
                    calculated = pCalc / exp(z[i])

                    self.assertFalse(
                        abs(expected - calculated) > 0.01 and
                        abs((expected - calculated) / expected) > 0.04)

    def testBarrierPricingViaHestonLocalVol(self):
        TEST_MESSAGE(
            "Testing calibration via vanilla options...")

        backup = SavedSettings()
        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(5, November, 2015)
        Settings.instance().evaluationDate = todaysDate

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))
        r = 0.1
        q = 0.025

        kappa = 2.0
        theta = 0.09
        rho = -0.75
        sigma = 0.8
        v0 = 0.19

        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        hestonProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        hestonModel = HestonModelHandle(
            HestonModel(hestonProcess))

        surf = BlackVolTermStructureHandle(
            HestonBlackVolSurface(hestonModel))

        strikeValues = [50, 75, 100, 125, 150, 200, 400]
        maturities = [
            Period(1, Months), Period(2, Months),
            Period(3, Months), Period(4, Months),
            Period(5, Months), Period(6, Months),
            Period(9, Months), Period(1, Years),
            Period(18, Months), Period(2, Years),
            Period(3, Years), Period(5, Years)]

        localVolSurface = LocalVolSurface(
            surf, rTS, qTS, spot)

        hestonEngine = AnalyticHestonEngine(
            hestonModel.currentLink(), 164)

        for strike in strikeValues:
            for maturitie in maturities:
                exerciseDate = todaysDate + maturitie
                t = dc.yearFraction(todaysDate, exerciseDate)
                impliedVol = surf.blackVol(t, strike, True)
                bsProcess = GeneralizedBlackScholesProcess(
                    spot, qTS, rTS,
                    BlackVolTermStructureHandle(
                        flatVol(impliedVol, dc)))

                analyticEngine = AnalyticEuropeanEngine(bsProcess)

                exercise = EuropeanExercise(exerciseDate)
                payoff = PlainVanillaPayoff(
                    Option.Call if spot.value() < strike else Option.Put,
                    strike)

                localVolEngine = FdBlackScholesVanillaEngine(
                    bsProcess, 201, 801, 0,
                    FdmSchemeDesc.Douglas(), True)

                option = VanillaOption(payoff, exercise)

                option.setPricingEngine(analyticEngine)
                analyticNPV = option.NPV()

                option.setPricingEngine(hestonEngine)
                hestonNPV = option.NPV()

                option.setPricingEngine(localVolEngine)
                localVolNPV = option.NPV()

                tol = 1e-3
                self.assertFalse(abs(analyticNPV - hestonNPV) > tol)
                self.assertFalse(abs(analyticNPV - localVolNPV) > tol)

    @unittest.skipIf(skipSlowTest, "testBarrierPricingMixedModels is VERY SLOW")
    def testBarrierPricingMixedModels(self):
        TEST_MESSAGE(
            "Testing Barrier pricing with mixed models...")

        backup = SavedSettings()
        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(5, November, 2015)
        exerciseDate = todaysDate + Period(1, Years)
        Settings.instance().evaluationDate = todaysDate

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))
        r = 0.05
        q = 0.02

        kappa = 2.0
        theta = 0.09
        rho = -0.75
        sigma = 0.4
        v0 = 0.19

        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        hestonProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        hestonModel = HestonModelHandle(
            HestonModel(hestonProcess))

        impliedVolSurf = BlackVolTermStructureHandle(
            HestonBlackVolSurface(hestonModel))

        localVolSurf = LocalVolTermStructureHandle(
            NoExceptLocalVolSurface(
                impliedVolSurf, rTS, qTS, spot, 0.3))

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, impliedVolSurf)

        exercise = EuropeanExercise(exerciseDate)
        payoff = PlainVanillaPayoff(Option.Put, s0)

        hestonEngine = FdHestonBarrierEngine(
            hestonModel.currentLink(), 26, 101, 51)

        localEngine = FdBlackScholesBarrierEngine(
            bsProcess, 26, 101, 0,
            FdmSchemeDesc.Douglas(), True, 0.3)

        barrier = 10.0
        barrierOption = BarrierOption(
            Barrier.DownOut, barrier, 0.0, payoff, exercise)

        barrierOption.setPricingEngine(hestonEngine)
        hestonDeltaCalculated = barrierOption.delta()

        barrierOption.setPricingEngine(localEngine)
        localDeltaCalculated = barrierOption.delta()

        localDeltaExpected = -0.439068
        hestonDeltaExpected = -0.342059
        tol = 0.001

        self.assertFalse(abs(hestonDeltaExpected - hestonDeltaCalculated) > tol)
        self.assertFalse(abs(localDeltaExpected - localDeltaCalculated) > tol)

        params = HestonSLVFokkerPlanckFdmParams(
            51, 201, 1000, 100, 3.0, 0, 2,
            0.1, 1e-4, 10000,
            1e-8, 1e-8, 0.0, 1.0, 1.0, 1.0, 1e-6,
            FdmHestonGreensFct.Gaussian,
            FdmSquareRootFwdOp.Plain,
            FdmSchemeDesc.ModifiedCraigSneyd())

        eta = [0.1, 0.2, 0.3, 0.4,
               0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        slvDeltaExpected = [
            -0.429475, -0.419749, -0.410055, -0.400339,
            -0.390616, -0.380888, -0.371156, -0.361425,
            -0.351699, -0.341995]

        for i in range(len(eta)):
            modHestonModel = HestonModelHandle(
                HestonModel(
                    HestonProcess(
                        rTS, qTS, spot, v0, kappa,
                        theta, eta[i] * sigma, rho)))

            slvModel = HestonSLVFDMModel(
                localVolSurf, modHestonModel, exerciseDate, params)

            leverageFct = slvModel.leverageFunction()

            slvEngine = FdHestonBarrierEngine(
                modHestonModel.currentLink(), 201, 801, 201, 0,
                FdmSchemeDesc.Hundsdorfer(), leverageFct)

            barrierOption = BarrierOption(
                Barrier.DownOut, barrier, 0.0, payoff, exercise)

            barrierOption.setPricingEngine(slvEngine)
            slvDeltaCalculated = barrierOption.delta()

            self.assertFalse(
                abs(slvDeltaExpected[i] - slvDeltaCalculated) > tol)

    def testMonteCarloCalibration(self):
        TEST_MESSAGE(
            "Testing Monte-Carlo Calibration...")

        backup = SavedSettings()
        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(5, January, 2016)
        maturityDate = todaysDate + Period(1, Years)
        Settings.instance().evaluationDate = todaysDate

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))
        r = 0.05
        q = 0.02

        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        localVol = LocalConstantVol(todaysDate, 0.3, dc)

        #  parameter of the "calibrated" Heston model
        kappa = 1.0
        theta = 0.06
        rho = -0.75
        sigma = 0.4
        v0 = 0.09

        hestonProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        hestonModel = HestonModel(hestonProcess)

        xGrid = 400
        nSims = [40000]

        for nSim in nSims:
            sobol = True

            leverageFct = HestonSLVMCModel(
                LocalVolTermStructureHandle(localVol),
                HestonModelHandle(hestonModel),
                SobolBrownianGeneratorFactory(
                    SobolBrownianGenerator.Diagonal,
                    1234, SobolRsg.JoeKuoD7)
                if sobol else
                MTBrownianGeneratorFactory(1234),
                maturityDate, 91, xGrid, nSim).leverageFunction()

            bsEngine = AnalyticEuropeanEngine(
                GeneralizedBlackScholesProcess(
                    spot, qTS, rTS,
                    BlackVolTermStructureHandle(
                        flatVol(0.3, dc))))

            strikes = [50, 80, 100, 120, 150, 200]
            maturities = [
                todaysDate + Period(3, Months),
                todaysDate + Period(6, Months),
                todaysDate + Period(12, Months)]

            qualityFactor = 0.0
            maxQualityFactor = 0.0
            nValues = 0

            for maturity in maturities:
                maturityTime = dc.yearFraction(
                    todaysDate, maturity)

                fdEngine = FdHestonVanillaEngine(
                    hestonModel,
                    max(26, int(maturityTime * 51)),
                    201, 51, 0,
                    FdmSchemeDesc.ModifiedCraigSneyd(),
                    leverageFct)

                exercise = EuropeanExercise(maturity)

                for strike in strikes:
                    payoff = PlainVanillaPayoff(
                        Option.Put if strike < s0 else Option.Call,
                        strike)

                    option = VanillaOption(payoff, exercise)

                    option.setPricingEngine(bsEngine)
                    bsNPV = option.NPV()
                    bsVega = option.vega()

                    if bsNPV > 0.02:
                        option.setPricingEngine(fdEngine)
                        fdmNPV = option.NPV()

                        diff = abs(fdmNPV - bsNPV) / bsVega * 1e4

                        qualityFactor += diff
                        maxQualityFactor = max(maxQualityFactor, diff)
                        nValues += 1

            self.assertFalse(qualityFactor / nValues > 7.5)
            self.assertFalse(qualityFactor / nValues > 15.0)

    def testMoustacheGraph(self):
        TEST_MESSAGE(
            "SKIP",
            "Testing double no touch pricing with SLV and mixing...")

        # backup = SavedSettings()
        #
        # #  A more detailed description of this test case can found on
        # #  https://hpcquantlib.wordpress.com/2016/01/10/monte-carlo-calibration-of-the-heston-stochastic-local-volatiltiy-model/
        # #
        # #  The comparison of Black-Scholes and SLV prices is derived
        # #  from figure 8.8 in Iain J. Clark's book,
        # #  Foreign Exchange Option Pricing: A Practitioner’s Guide
        #
        # dc = ActualActual(ActualActual.ISDA)
        # todaysDate = Date(5, January, 2016)
        # maturityDate = todaysDate + Period(1, Years)
        # Settings.instance().evaluationDate = todaysDate
        #
        # s0 = 100
        # spot = QuoteHandle(SimpleQuote(s0))
        # r = 0.02
        # q = 0.01
        #
        # #  parameter of the "calibrated" Heston model
        # kappa = 1.0
        # theta = 0.06
        # rho = -0.8
        # sigma = 0.8
        # v0 = 0.09
        #
        # rTs = YieldTermStructureHandle(flatRate(r, dc))
        # qTs = YieldTermStructureHandle(flatRate(q, dc))
        #
        # hestonModel = HestonModel(
        #     HestonProcess(
        #         rTs, qTs, spot, v0, kappa, theta, sigma, rho))
        #
        # europeanExercise = EuropeanExercise(maturityDate)
        #
        # vanillaOption = VanillaOption(
        #     PlainVanillaPayoff(Option.Call, s0),
        #     europeanExercise)
        #
        # vanillaOption.setPricingEngine(
        #     AnalyticHestonEngine(hestonModel))
        #
        # implVol = vanillaOption.impliedVolatility(
        #     vanillaOption.NPV(),
        #     GeneralizedBlackScholesProcess(
        #         spot, qTs, rTs,
        #         BlackVolTermStructureHandle(
        #             flatVol(sqrt(theta), dc))))
        #
        # analyticEngine = AnalyticDoubleBarrierBinaryEngine(
        #     GeneralizedBlackScholesProcess(
        #         spot, qTs, rTs,
        #         BlackVolTermStructureHandle(
        #             flatVol(implVol, dc))))
        #
        # expiries = DoubleVector()
        # timeStepPeriod = Period(1, Weeks)
        # expiry = todaysDate + timeStepPeriod
        # while expiry <= maturityDate:
        #     expiries.push_back(
        #         dc.yearFraction(todaysDate, expiry))
        #     expiry = expiry + timeStepPeriod
        #
        # timeGrid = TimeGrid(expiries)
        #
        # #  first build the True local vol surface from another Heston model
        # sf = getFixedLocalVolFromHeston(hestonModel, timeGrid)
        #
        # localVol = LocalVolTermStructureHandle(sf)
        #
        # sobolGeneratorFactory = SobolBrownianGeneratorFactory(
        #     SobolBrownianGenerator.Diagonal, 1234,
        #     SobolRsg.JoeKuoD7)
        #
        # xGrid = 100
        # nSim = 20000
        #
        # eta = 0.90
        # hp = HestonProcess(
        #     rTs, qTs, spot, v0, kappa,
        #     theta, eta * sigma, rho)
        # mod = HestonModel(hp)
        #
        # modHestonModel = HestonModelHandle(mod)
        #
        # leverageFct = HestonSLVMCModel(
        #     localVol, modHestonModel,
        #     sobolGeneratorFactory,
        #     maturityDate, 182,
        #     xGrid, nSim).leverageFunction()
        #
        # h = FdmSchemeDesc.Hundsdorfer()
        #
        # fdEngine = FdHestonDoubleBarrierEngine(
        #     modHestonModel.currentLink(),
        #     51, 101, 31, 0,
        #     h, leverageFct)
        #
        # expected = [
        #     0.0334, 0.1141, 0.1319, 0.0957, 0.0464, 0.0058, -0.0192,
        #     -0.0293, -0.0297, -0.0251, -0.0192, -0.0134, -0.0084, -0.0045,
        #     -0.0015, 0.0005, 0.0017, 0.0020]
        # tol = 1e-2
        #
        # for i in range(18):
        #     dist = 10.0 + 5.0 * i
        #
        #     barrier_lo = max(s0 - dist, 1e-2)
        #     barrier_hi = s0 + dist
        #     doubleBarrier = DoubleBarrierOption(
        #         DoubleBarrier.KnockOut,
        #         barrier_lo, barrier_hi, 0.0,
        #         CashOrNothingPayoff(
        #             Option.Call, 0.0, 1.0),
        #         europeanExercise)
        #
        #     doubleBarrier.setPricingEngine(analyticEngine)
        #     bsNPV = doubleBarrier.NPV()
        #
        #     doubleBarrier.setPricingEngine(fdEngine)
        #     slvNPV = doubleBarrier.NPV()
        #
        #     diff = slvNPV - bsNPV
        #     self.assertFalse(abs(diff - expected[i]) > tol)

    def testForwardSkewSLV(self):
        TEST_MESSAGE(
            "SKIP",
            "Testing the implied volatility skew of forward starting options in SLV model...")

    def testADiffusionAndDriftSlvProcess(self):
        TEST_MESSAGE(
            "SKIP",
            "Testing diffusion and drift of the SLV process...")

        # backup = SavedSettings()
        #
        # todaysDate = Date(6, June, 2020)
        # Settings.instance().evaluationDate = todaysDate
        #
        # dc = Actual365Fixed()
        # maturityDate = todaysDate + Period(6, Months)
        # maturity = dc.yearFraction(todaysDate, maturityDate)
        #
        # s0 = 100
        # spot = QuoteHandle(SimpleQuote(s0))
        # r = -0.005
        # q = 0.04
        #
        # rTS = YieldTermStructureHandle(flatRate(todaysDate, r, dc))
        # qTS = YieldTermStructureHandle(flatRate(todaysDate, q, dc))
        # hp = HestonProcess(
        #     rTS, qTS, spot, 0.1, 1.0, 0.13, 0.8, 0.4)
        # hm = HestonModel(hp)
        # tg = TimeGrid(maturity, 20)
        #
        # localVol = getFixedLocalVolFromHeston(hm, tg)
        #
        # kappa = 2.5
        # theta = 1.0
        # rho = -0.75
        # sigma = 2.4
        # v0 = 1.0
        #
        # hestonProcess = HestonProcess(
        #     rTS, qTS, spot, v0, kappa, theta, sigma, rho)
        #
        # hestonModel = HestonModelHandle(
        #     HestonModel(hestonProcess))
        #
        # slvProcess = HestonSLVProcess(
        #     hestonProcess, localVol)
        #
        # option = VanillaOption(
        #     PlainVanillaPayoff(Option.Call, s0),
        #     EuropeanExercise(maturityDate))
        # engine = FdHestonVanillaEngine(
        #     hestonModel.currentLink(),
        #     26, 201, 101, 0,
        #     FdmSchemeDesc.ModifiedCraigSneyd(),
        #     localVol)
        #
        # option.setPricingEngine(engine)
        #
        # expected = option.NPV()
        #
        # nSims = 16733
        # nTimeSteps = 40
        # df = rTS.discount(maturity)
        #
        # rsg = SobolBrownianBridgeRsg(
        #     2, nTimeSteps,
        #     SobolBrownianGenerator.Diagonal,
        #     12345,
        #     SobolRsg.JoeKuoD7)
        #
        # x = Array(2)
        # xt = Array(2)
        # dw = Array(2)
        # stats = GeneralStatistics()
        #
        # dt = maturity / nTimeSteps
        # sqrtDt = sqrt(dt)
        #
        # for i in range(nSims):
        #     t = 0.0
        #     x[0] = s0
        #     x[1] = v0
        #
        #     n = rsg.nextSequence().value()
        #
        #     for j in range(nTimeSteps):
        #         dw[0] = n[j]
        #         dw[1] = n[j + nTimeSteps]
        #
        #         #  full truncation scheme
        #         xt[0] = x[0]
        #         xt[1] = x[1] if x[1] > 0 else 0.0
        #
        #         x = slvProcess.apply(
        #             x,
        #             slvProcess.diffusion(t, xt) * sqrtDt * dw + slvProcess.drift(t, xt) * dt)
        #         t += dt
        #
        #     stats.add(df * option.payoff()(x[0]))
        #
        # calculated = stats.mean()
        # errorEstimate = stats.errorEstimate()
        #
        # diff = abs(expected - calculated)
        #
        # self.assertFalse(diff > 2.35 * errorEstimate)

    def testMonteCarloVsFdmPricing(self):
        TEST_MESSAGE(
            "Testing Monte-Carlo vs FDM Pricing for Heston SLV models...")

        backup = SavedSettings()
        dc = ActualActual(ActualActual.ISDA)
        todaysDate = Date(5, December, 2015)
        exerciseDate = todaysDate + Period(1, Years)
        Settings.instance().evaluationDate = todaysDate

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))
        r = 0.05
        q = 0.02

        kappa = 2.0
        theta = 0.18
        rho = -0.75
        sigma = 0.8
        v0 = 0.19

        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        hestonProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma, rho)

        hestonModel = HestonModel(hestonProcess)

        leverageFct = LocalConstantVol(
            todaysDate, 0.25, dc)

        slvProcess = HestonSLVProcess(
            hestonProcess, leverageFct)

        mcEngine = MakeMCPREuropeanHestonSLVEngine(slvProcess)
        mcEngine.withStepsPerYear(100)
        mcEngine.withAntitheticVariate()
        mcEngine.withSamples(10000)
        mcEngine.withSeed(1234)
        mcEngine = mcEngine.makeEngine()

        fdEngine = FdHestonVanillaEngine(
            hestonModel, 51, 401, 101, 0,
            FdmSchemeDesc.ModifiedCraigSneyd(), leverageFct)

        exercise = EuropeanExercise(exerciseDate)

        mixingProcess = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, sigma * 10, rho,
            HestonProcess.QuadraticExponentialMartingale)
        mixingModel = HestonModel(mixingProcess)

        fdEngineWithMixingFactor = FdHestonVanillaEngine(
            mixingModel, 51, 401, 101, 0,
            FdmSchemeDesc.ModifiedCraigSneyd(),
            leverageFct, 0.1)

        strikes = [s0, 1.1 * s0]
        for strike in strikes:
            payoff = PlainVanillaPayoff(Option.Call, strike)
            option = VanillaOption(payoff, exercise)
            option.setPricingEngine(fdEngine)
            priceFDM = option.NPV()
            option.setPricingEngine(fdEngineWithMixingFactor)
            priceFDMWithMix = option.NPV()
            option.setPricingEngine(mcEngine)
            priceMC = option.NPV()
            priceError = option.errorEstimate()
            self.assertFalse(priceError > 0.1)
            self.assertFalse(abs(priceFDM - priceMC) > 2.3 * priceError)
            self.assertFalse(priceFDM != priceFDMWithMix)
