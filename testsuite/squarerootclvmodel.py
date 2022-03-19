import unittest
from utilities import *
from QuantLib import *
from math import exp, sqrt
from scipy.stats import ncx2

chi_squared_type = ncx2


class SquareRootCLVCalibrationFunction(object):

    def __init__(self,
                 strikes,
                 resetDates,
                 maturityDates,
                 bsProcess,
                 refVols,
                 nScenarios=10000):
        self.strikes_ = strikes
        self.resetDates_ = resetDates
        self.maturityDates_ = maturityDates
        self.bsProcess_ = bsProcess
        self.refVols_ = refVols
        self.nScenarios_ = nScenarios
        # c=DateSet(resetDates.begin(), resetDates.end())
        # c.insert(maturityDates.begin(), maturityDates.end())
        self.calibrationDates_ = DateVector()
        # self.calibrationDates_.insert(
        #     calibrationDates_.begin(), c.begin(), c.end())
        for d in resetDates:
            self.calibrationDates_.append(d)
        for d in maturityDates:
            self.calibrationDates_.append(d)

    def value(self, params):
        diff = self.values(params)

        retVal = 0.0
        for i in diff:
            retVal += i * i

        return retVal

    def values(self, params):
        theta = params[0]
        kappa = params[1]
        sigma = params[2]
        x0 = params[3]

        vol = SimpleQuote(0.1)

        rTS = self.bsProcess_.riskFreeRate()
        qTS = self.bsProcess_.dividendYield()
        spot = QuoteHandle(SimpleQuote(
            self.bsProcess_.x0()))

        # fwdEngine=ForwardVanillaEngine<AnalyticEuropeanEngine>
        fwdEngine = ForwardEuropeanEngine(
            GeneralizedBlackScholesProcess(
                spot, qTS, rTS,
                BlackVolTermStructureHandle(
                    flatVol(
                        rTS.referenceDate(), vol, rTS.dayCounter()))))

        sqrtProcess = SquareRootProcess(theta, kappa, sigma, x0)

        clvSqrtModel = SquareRootCLVModel(
            self.bsProcess_, sqrtProcess,
            self.calibrationDates_,
            14, 1 - 1e-14, 1e-14)

        # gSqrt = clvSqrtModel.g()

        retVal = Array(len(self.resetDates_) * len(self.strikes_))

        for i in range(len(self.resetDates_)):
            resetDate = self.resetDates_[i]
            maturityDate = self.maturityDates_[i]

            t0 = self.bsProcess_.time(resetDate)
            t1 = self.bsProcess_.time(maturityDate)

            df = 4 * theta * kappa / (sigma * sigma)
            ncp = 4 * kappa * exp(-kappa * t0) / (sigma * sigma * (1 - exp(-kappa * t0))) * x0

            # typedef boost.math.non_central_chi_squared_distribution<Real> chi_squared_type

            dist = chi_squared_type(df, ncp)

            ncp1 = 4 * kappa * exp(-kappa * (t1 - t0)) / (sigma * sigma * (1 - exp(-kappa * (t1 - t0))))

            # LowDiscrepancy.ursg_type ursg = LowDiscrepancy.ursg_type(2, 1235UL)
            ursg = SobolRsg(2, 1235)

            # vector<GeneralStatistics> stats(strikes_.size())
            stats = [GeneralStatistics() for i in range(len(self.strikes_))]

            for j in range(self.nScenarios_):
                path = ursg.nextSequence().value()

                # x1 = boost.math.quantile(dist, path[0])
                x1 = dist.ppf(path[0])
                u1 = sigma * sigma * (1 - exp(-kappa * t0)) / (4 * kappa) * x1

                # x2 = boost.math.quantile(chi_squared_type(df, ncp1 * u1), path[1])
                x2 = chi_squared_type(df, ncp1 * u1).ppf(path[1])
                u2 = sigma * sigma * (1 - exp(-kappa * (t1 - t0))) / (4 * kappa) * x2
                X2 = u2 * 4 * kappa / (sigma * sigma * (1 - exp(-kappa * t1)))

                s1 = clvSqrtModel.g(t0, x1)
                s2 = clvSqrtModel.g(t1, X2)

                for k in range(len(self.strikes_)):
                    strike = self.strikes_[k]

                    payoff = s1 * max(0.0, strike - s2 / s1) if strike < 1.0 else s1 * max(0.0, s2 / s1 - strike)

                    stats[k].add(payoff)

            exercise = EuropeanExercise(maturityDate)

            dF = self.bsProcess_.riskFreeRate().discount(maturityDate)

            for k in range(len(self.strikes_)):
                strike = self.strikes_[k]
                npv = stats[k].mean() * dF

                payoff = PlainVanillaPayoff(
                    Option.Put if strike < 1.0 else Option.Call, strike)

                fwdOption = ForwardVanillaOption(
                    strike, resetDate, payoff, exercise)

                implVol = ImpliedVolatilityHelper.calculate(
                    fwdOption, fwdEngine, vol, npv, 1e-8, 200, 1e-4, 2.0)

                idx = k + i * len(self.strikes_)
                retVal[idx] = implVol - self.refVols_[idx]

        return retVal


class NonZeroConstraint(object):

    def test(self, params):
        theta = params[0]
        kappa = params[1]
        sigma = params[2]
        x0 = params[3]

        return sigma >= 0.001 and kappa > 1e-6 and theta > 0.001 and x0 > 1e-4

    def upperBound(self, params):
        # upper=[ 1.0, 1.0, 1.0, 2.0 ]
        upper = Array(4)
        upper[0] = 1.0
        upper[1] = 1.0
        upper[2] = 1.0
        upper[3] = 2.0

        return upper

    def lowerBound(self, params):
        # lower=[ 0.001, 0.001, 0.001, 1e-4 ]
        lower = Array(4)
        lower[0] = 0.001
        lower[1] = .001
        lower[2] = 0.001
        lower[3] = 1e-4

        return lower


class SquareRootCLVModelTest(unittest.TestCase):

    def testSquareRootCLVVanillaPricing(self):
        TEST_MESSAGE(
            "Testing vanilla option pricing with square-root kernel process...")

        backup = SavedSettings()

        todaysDate = Date(5, Oct, 2016)
        Settings.instance().evaluationDate = todaysDate

        dc = ActualActual(ActualActual.ISDA)
        maturityDate = todaysDate + Period(3, Months)
        maturity = dc.yearFraction(todaysDate, maturityDate)

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))

        r = 0.08
        q = 0.03
        vol = 0.3

        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))
        volTS = BlackVolTermStructureHandle(flatVol(todaysDate, vol, dc))
        fwd = s0 * qTS.discount(maturity) / rTS.discount(maturity)

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, volTS)

        kappa = 1.0
        theta = 0.06
        sigma = 0.2
        x0 = 0.09

        sqrtProcess = SquareRootProcess(theta, kappa, sigma, x0)

        maturityDates = DateVector(1, maturityDate)

        model = SquareRootCLVModel(
            bsProcess, sqrtProcess, maturityDates, 14, 1 - 1e-14, 1e-14)

        x = model.collocationPointsX(maturityDate)
        y = model.collocationPointsY(maturityDate)

        g = SafeLagrangeInterpolation(x, y)

        df = 4 * theta * kappa / (sigma * sigma)
        ncp = 4 * kappa * exp(-kappa * maturity) / (sigma * sigma * (1 - exp(-kappa * maturity))) * sqrtProcess.x0()

        # typedef boost.math.non_central_chi_squared_distribution<Real> chi_squared_type
        dist = chi_squared_type(df, ncp)

        strikes = [50, 75, 100, 125, 150, 200]
        for strike in strikes:
            optionType = Option.Call if strike > fwd else Option.Put

            expected = BlackCalculator(
                optionType, strike, fwd,
                sqrt(volTS.blackVariance(maturity, strike)),
                rTS.discount(maturity)).value()

            # clvModelPayoff=CLVModelPayoff (optionType, strike, g)
            clvModelPayoff = CustomCLVModelPayoff(g, optionType, strike)

            # f = lambda xi:clvModelPayoff(xi) * boost.math.pdf(dist, xi)
            f = lambda xi: clvModelPayoff(xi) * dist.pdf(xi)

            calculated = GaussLobattoIntegral(1000, 1e-6)(
                f, x[0], x[-1]) * rTS.discount(maturity)

            tol = 5e-3
            self.assertFalse(abs(expected - calculated) > tol)

    def testSquareRootCLVMappingFunction(self):
        TEST_MESSAGE(
            "Testing mapping function of the square-root kernel process...")

        backup = SavedSettings()

        todaysDate = Date(16, Oct, 2016)
        Settings.instance().evaluationDate = todaysDate
        maturityDate = todaysDate + Period(1, Years)

        dc = Actual365Fixed()

        s0 = 100
        spot = QuoteHandle(SimpleQuote(s0))

        r = 0.05
        q = 0.02

        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        # SABR
        beta = 0.95
        alpha = 0.2
        rho = -0.9
        gamma = 0.8

        sabrVol = BlackVolTermStructureHandle(
            SABRVolTermStructure(
                alpha, beta, gamma, rho, s0, r, todaysDate, dc))

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, sabrVol)

        calibrationDates = DateVector(1, todaysDate + Period(3, Months))
        calibrationDates.reserve(int(daysBetween(todaysDate, maturityDate) / 7 + 1))
        while calibrationDates.back() < maturityDate:
            calibrationDates.append(
                calibrationDates.back() + Period(1, Weeks))

        # sqrt process
        kappa = 1.0
        theta = 0.09
        sigma = 0.2
        x0 = 0.09

        sqrtProcess = SquareRootProcess(theta, kappa, sigma, x0)

        model = SquareRootCLVModel(
            bsProcess, sqrtProcess, calibrationDates, 14, 1 - 1e-10, 1e-10)

        # ext.function<Real(Time, Real)> g = model.g()

        strikes = [80, 100, 120]
        offsets = [92, 182, 183, 184, 185, 186, 365]
        for offset in offsets:
            m = todaysDate + Period(offset, Days)
            t = dc.yearFraction(todaysDate, m)

            df = 4 * theta * kappa / (sigma * sigma)
            ncp = 4 * kappa * exp(-kappa * t) / (sigma * sigma * (1 - exp(-kappa * t))) * sqrtProcess.x0()

            dist = chi_squared_type(df, ncp)

            fwd = s0 * qTS.discount(m) / rTS.discount(m)

            for strike in strikes:
                optionType = Option.Call if strike > fwd else Option.Put

                expected = BlackCalculator(
                    optionType, strike, fwd,
                    sqrt(sabrVol.blackVariance(m, strike)),
                    rTS.discount(m)).value()

                clvModelPayoff = CustomCLVModelPayoff(
                    # [&](x) { return g(t, x) },
                    lambda x: model.g(t, x),
                    optionType, strike)

                f = lambda xi: clvModelPayoff(xi) * dist.pdf(xi)

                x = model.collocationPointsX(m)
                calculated = GaussLobattoIntegral(1000, 1e-3)(
                    f, x[0], x[-1]) * rTS.discount(m)

                tol = 0.075

                self.assertFalse(
                    abs(expected) > 0.01 and
                    abs((calculated - expected) / calculated) > tol)

    @unittest.skip("VERY VERY SLOW")
    def testForwardSkew(self):
        TEST_MESSAGE(
            "Testing forward skew dynamics with square-root kernel process...")

        backup = SavedSettings()

        todaysDate = Date(16, Oct, 2016)
        Settings.instance().evaluationDate = todaysDate
        endDate = todaysDate + Period(4, Years)

        dc = Actual365Fixed()

        # Heston model is used to generate an arbitrage free volatility surface
        s0 = 100
        r = 0.1
        q = 0.05
        v0 = 0.09
        kappa = 1.0
        theta = 0.09
        sigma = 0.3
        rho = -0.75

        spot = QuoteHandle(SimpleQuote(s0))
        rTS = YieldTermStructureHandle(flatRate(r, dc))
        qTS = YieldTermStructureHandle(flatRate(q, dc))

        hestonModel = HestonModel(
            HestonProcess(
                rTS, qTS, spot, v0, kappa, theta, sigma, rho))

        blackVol = BlackVolTermStructureHandle(
            HestonBlackVolSurface(
                HestonModelHandle(hestonModel)))

        localVol = LocalVolTermStructureHandle(
            NoExceptLocalVolSurface(
                blackVol, rTS, qTS, spot, sqrt(theta)))

        sTheta = 0.389302
        sKappa = 0.1101849
        sSigma = 0.275368
        sX0 = 0.466809

        sqrtProcess = SquareRootProcess(
            sTheta, sKappa, sSigma, sX0)

        bsProcess = GeneralizedBlackScholesProcess(
            spot, qTS, rTS, blackVol)

        calibrationDates = DateVector(1, todaysDate + Period(6, Months))
        while calibrationDates.back() < endDate:
            calibrationDates.append(calibrationDates.back() + Period(3, Months))

        # clvCalibrationDates = DateSet(
        #     calibrationDates.begin(), calibrationDates.end())
        clvCalibrationDates = DateSet()
        for d in calibrationDates:
            clvCalibrationDates.insert(d)

        tmpDate = todaysDate + Period(1, Days)
        while tmpDate < todaysDate + Period(1, Years):
            clvCalibrationDates.insert(tmpDate)
            tmpDate += Period(1, Weeks)

        dateVec = DateVector()
        for d in clvCalibrationDates:
            dateVec.append(d)

        clvSqrtModel = SquareRootCLVModel(
            bsProcess,
            sqrtProcess,
            dateVec,
            14, 1 - 1e-14, 1e-14)

        # ext.function<Real(Time, Real)> gSqrt = clvSqrtModel.g()

        vol = SimpleQuote(0.1)

        # fwdEngine=ForwardVanillaEngine<AnalyticEuropeanEngine >(
        fwdEngine = ForwardEuropeanEngine(
            GeneralizedBlackScholesProcess(
                spot, qTS, rTS,
                BlackVolTermStructureHandle(
                    flatVol(todaysDate, vol, dc))))

        # forward skew of the Heston-SLV model
        mandatoryTimes = DoubleVector()
        # mandatoryTimes.reserve(calibrationDates.size())
        for calibrationDate in calibrationDates:
            mandatoryTimes.append(
                dc.yearFraction(todaysDate, calibrationDate))

        tSteps = 200
        grid = TimeGrid(mandatoryTimes, tSteps)

        resetDates = DateVector()
        maturityDates = DateVector()
        resetIndices = SizeVector()
        maturityIndices = SizeVector()
        for i in range(len(calibrationDates) - 2):
            resetDates.append(calibrationDates[i])
            maturityDates.append(calibrationDates[i + 2])

            resetTime = mandatoryTimes[i]
            maturityTime = mandatoryTimes[i + 2]

            resetIndices.append(grid.closestIndex(resetTime) - 1)
            maturityIndices.append(grid.closestIndex(maturityTime) - 1)

        strikes = [
            0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2,
            1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

        nScenarios = 20000
        refVols = Array(len(resetIndices) * len(strikes))

        # finite difference calibration of Heston SLV model

        # define Heston Stochastic Local model
        eta = 0.25
        corr = -0.0

        hestonProcess4slv = HestonProcess(
            rTS, qTS, spot, v0, kappa, theta, eta * sigma, corr)

        hestonModel4slv = HestonModelHandle(
            HestonModel(hestonProcess4slv))

        logParams = HestonSLVFokkerPlanckFdmParams(
            301, 601, 1000, 30, 2.0, 0, 2,
            0.1, 1e-4, 10000,
            1e-5, 1e-5, 0.0000025, 1.0, 0.1, 0.9, 1e-5,
            FdmHestonGreensFct.Gaussian,
            FdmSquareRootFwdOp.Log,
            FdmSchemeDesc.ModifiedCraigSneyd())

        leverageFctFDM = HestonSLVFDMModel(
            localVol, hestonModel4slv, endDate, logParams).leverageFunction()

        #  calibrating to forward volatility dynamics

        fdmSlvProcess = HestonSLVProcess(
            hestonProcess4slv, leverageFctFDM)

        # vector<vector<GeneralStatistics> > slvStats(
        #     len(calibrationDates) - 2,
        #     vector<GeneralStatistics>(len(strikes)))

        slvStats = []
        for i in range(len(calibrationDates) - 2):
            slvStats.append(
                [GeneralStatistics() for j in range(len(strikes))])

        # typedef SobolBrownianBridgeRsg rsg_type
        # typedef MultiPathGenerator<rsg_type>.sample_type sample_type

        factors = fdmSlvProcess.factors()

        # pathGen=MultiPathGenerator<rsg_type>(
        pathGen = BrownianBridgeSobolMultiPathGenerator(
            fdmSlvProcess, grid, SobolBrownianBridgeRsg(factors, len(grid) - 1), false)

        for k in range(nScenarios):
            path = pathGen.next()

            for i in range(resetIndices.size()):
                S_t1 = path.value()[0][resetIndices[i]]
                S_T1 = path.value()[0][maturityIndices[i]]

                for j in range(len(strikes)):
                    strike = strikes[j]
                    slvStats[i][j].add(
                        S_t1 * max(0.0, strike - S_T1 / S_t1) if (strike < 1.0) else S_t1 * max(0.0, S_T1 / S_t1 - strike))

        for i in range(len(resetIndices)):
            resetDate = calibrationDates[i]
            maturityDate = calibrationDates[i + 2]
            df = rTS.discount(maturityDate)

            exercise = EuropeanExercise(maturityDate)

            for j in range(len(strikes)):
                strike = strikes[j]
                npv = slvStats[i][j].mean() * df

                payoff = PlainVanillaPayoff(
                    Option.Put if strike < 1.0 else Option.Call, strike)

                fwdOption = ForwardVanillaOption(
                    strike, resetDate, payoff, exercise)

                implVol = ImpliedVolatilityHelper.calculate(
                    fwdOption, fwdEngine, vol, npv, 1e-8, 200, 1e-4, 2.0)

                idx = j + i * len(strikes)
                refVols[idx] = implVol

        costFunction = CustomCostFunction(
            SquareRootCLVCalibrationFunction(
                # Array(strikes, strikes + len(strikes)),
                strikes,
                resetDates,
                maturityDates,
                bsProcess,
                refVols,
                nScenarios))

        nonZeroConstraint = CustomConstraint(NonZeroConstraint())

        constraint = CompositeConstraint(
            nonZeroConstraint,
            FellerConstraint())

        params = Array(4)
        params[0] = sTheta
        params[1] = sKappa
        params[2] = sSigma
        params[3] = sX0

        #    Optimization would take too long
        #
        #    Problem prob(costFunction, nonZeroConstraint, params)
        #
        #    Simplex simplex(0.05)
        #    simplex.minimize(prob, EndCriteria(400, 40, 1.0e-8, 1.0e-8, 1.0e-8))

        tol = 0.5
        costValues = costFunction.values(params)
        costValue = costFunction.value(params)

        self.assertFalse(costValue > tol)

        maturityDate = todaysDate + Period(1, Years)
        maturityTime = bsProcess.time(maturityDate)

        europeanExercise = EuropeanExercise(maturityDate)

        vanillaATMOption = VanillaOption(
            PlainVanillaPayoff(
                Option.Call,
                s0 * qTS.discount(maturityDate) / rTS.discount(maturityDate)),
            europeanExercise)

        vanillaATMOption.setPricingEngine(
            AnalyticHestonEngine(hestonModel))

        atmVol = vanillaATMOption.impliedVolatility(
            vanillaATMOption.NPV(),
            GeneralizedBlackScholesProcess(spot, qTS, rTS,
                                           BlackVolTermStructureHandle(flatVol(sqrt(theta), dc))))

        analyticEngine = AnalyticDoubleBarrierBinaryEngine(
            GeneralizedBlackScholesProcess(
                spot, qTS, rTS,
                BlackVolTermStructureHandle(flatVol(atmVol, dc))))

        fdSLVEngine = FdHestonDoubleBarrierEngine(
            hestonModel4slv.currentLink(),
            51, 201, 51, 1,
            FdmSchemeDesc.Hundsdorfer(), leverageFctFDM)

        n = 16
        barrier_lo = Array(n)
        barrier_hi = Array(n)
        bsNPV = Array(n)
        slvNPV = Array(n)

        payoff = CashOrNothingPayoff(Option.Call, 0.0, 1.0)

        for i in range(n):
            dist = 20.0 + 5.0 * i

            barrier_lo[i] = max(s0 - dist, 1e-2)
            barrier_hi[i] = s0 + dist
            doubleBarrier = DoubleBarrierOption(
                DoubleBarrier.KnockOut, barrier_lo[i], barrier_hi[i], 0.0,
                payoff,
                europeanExercise)

            doubleBarrier.setPricingEngine(analyticEngine)
            bsNPV[i] = doubleBarrier.NPV()

            doubleBarrier.setPricingEngine(fdSLVEngine)
            slvNPV[i] = doubleBarrier.NPV()

        bGrid = TimeGrid(maturityTime, tSteps)

        # PseudoRandom.ursg_type ursg = PseudoRandom.ursg_type(tSteps, 1235UL)
        ursg = MersenneTwisterUniformRsg(tSteps, 1235)

        # vector<GeneralStatistics> stats(n)
        stats = [GeneralStatistics() for i in range(n)]

        df = 4 * sTheta * sKappa / (sSigma * sSigma)

        for i in range(nScenarios):
            touch = BoolVector(n, false)

            path = ursg.nextSequence().value()

            x = sX0

            for j in range(tSteps):
                t0 = bGrid.at(j)
                t1 = bGrid.at(j + 1)

                ncp = 4 * sKappa * exp(-sKappa * (t1 - t0)) / (sSigma * sSigma * (1 - exp(-sKappa * (t1 - t0)))) * x

                # boost.math.non_central_chi_squared_distribution<Real>  dist(df, ncp)
                dist = ncx2(df, ncp)

                # u = boost.math.quantile(dist, path[j])
                u = dist.ppf(path[j])

                x = sSigma * sSigma * (1 - exp(-sKappa * (t1 - t0))) / (4 * sKappa) * u

                X = x * 4 * sKappa / (sSigma * sSigma * (1 - exp(-sKappa * t1)))

                s = clvSqrtModel.g(t1, X)

                if t1 > 0.05:
                    for u in range(n):
                        if s <= barrier_lo[u] or s >= barrier_hi[u]:
                            touch[u] = true

            for u in range(n):
                if touch[u]:
                    stats[u].add(0.0)

                else:
                    stats[u].add(rTS.discount(maturityDate))

        for u in range(n):
            calculated = stats[u].mean()
            error = stats[u].errorEstimate()
            expected = slvNPV[u]

            tol = 2.35 * error

            self.assertFalse(abs(calculated - expected) > tol)
