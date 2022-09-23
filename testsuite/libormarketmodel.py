import unittest
from math import exp, sqrt

import numpy as np
from QuantLib import *

from utilities import *


def makeIndex0(dates,
               rates):
    dayCounter = Actual360()

    termStructure = RelinkableYieldTermStructureHandle()

    index = Euribor6M(termStructure)

    todaysDate = index.fixingCalendar().adjust(Date(4, September, 2005))
    Settings.instance().evaluationDate = todaysDate

    dates[0] = index.fixingCalendar().advance(
        todaysDate, index.fixingDays(), Days)

    termStructure.linkTo(ZeroCurve(dates, rates, dayCounter))

    return index


def makeIndex():
    dates = [Date(4, September, 2005), Date(4, September, 2018)]
    rates = [0.039, 0.041]

    return makeIndex0(dates, rates)


def makeCapVolCurve(todaysDate):
    vols = [
        14.40, 17.15, 16.81, 16.64, 16.17,
        15.78, 15.40, 15.21, 14.86]

    dates = []
    capletVols = []
    process = LiborForwardModelProcess(10, makeIndex())

    for i in range(9):
        capletVols.append(vols[i] / 100)
        dates.append(process.fixingDates()[i + 1])

    return CapletVarianceCurve(
        todaysDate, dates,
        capletVols, Actual360())


class LiborMarketModelTest(unittest.TestCase):

    def testSimpleCovarianceModels(self):
        TEST_MESSAGE(
            "Testing simple covariance models...")

        backup = SavedSettings()

        size = 10
        tolerance = 1e-14

        corrModel = LmExponentialCorrelationModel(size, 0.1)

        recon = corrModel.correlation(0.0) - corrModel.pseudoSqrt(0.0) * transpose(corrModel.pseudoSqrt(0.0))

        for i in range(size):
            for j in range(size):
                self.assertFalse(abs(recon[i][j]) > tolerance)

        fixingTimes = DoubleVector(size)
        for i in range(size):
            fixingTimes[i] = 0.5 * i

        a = 0.2
        b = 0.1
        c = 2.1
        d = 0.3

        volaModel = LmLinearExponentialVolatilityModel(fixingTimes, a, b, c, d)

        covarProxy = LfmCovarianceProxy(volaModel, corrModel)

        process = LiborForwardModelProcess(size, makeIndex())

        liborModel = LiborForwardModel(process, volaModel, corrModel)

        for t in np.arange(0, 4.6, 0.31):
            recon = covarProxy.covariance(t) - covarProxy.diffusion(t) * transpose(covarProxy.diffusion(t))

            for i in range(size):
                for j in range(size):
                    self.assertFalse(abs(recon[i][j]) > tolerance)

            volatility = volaModel.volatility(t)

            for k in range(size):
                expected = 0
                if k > 2 * t:
                    T = fixingTimes[k]
                    expected = (a * (T - t) + d) * exp(-b * (T - t)) + c

                self.assertFalse(abs(expected - volatility[k]) > tolerance)

    @unittest.skip("testCapletPricing: irregular fixings are not (yet) supported")
    def testCapletPricing(self):
        TEST_MESSAGE(
            "Testing caplet pricing...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        backup = SavedSettings()

        size = 10
        tolerance = 1e-12 if usingAtParCoupons else 1e-5

        index = makeIndex()
        process = LiborForwardModelProcess(size, index)

        capVolCurve = makeCapVolCurve(Settings.instance().evaluationDate)

        variances = LfmHullWhiteParameterization(
            process, capVolCurve).covariance(0.0).diagonal()

        volaModel = LmFixedVolatilityModel(
            Sqrt(variances), process.fixingTimes())

        corrModel = LmExponentialCorrelationModel(size, 0.3)

        model = LiborForwardModel(process, volaModel, corrModel)

        termStructure = process.index().forwardingTermStructure()

        engine1 = AnalyticCapFloorEngine(model, termStructure)

        cap1 = Cap(process.cashFlows(), DoubleVector(size, 0.04))
        cap1.setPricingEngine(engine1)

        expected = 0.015853935178
        calculated = cap1.NPV()

        self.assertFalse(abs(expected - calculated) > tolerance)

    @unittest.skip("testCalibration: irregular fixings are not (yet) supported")
    def testCalibration(self):
        TEST_MESSAGE(
            "Testing calibration of a Libor forward model...")

        backup = SavedSettings()

        size = 14
        tolerance = 8e-3

        capVols = [
            0.145708, 0.158465, 0.166248, 0.168672,
            0.169007, 0.167956, 0.166261, 0.164239,
            0.162082, 0.159923, 0.157781, 0.155745,
            0.153776, 0.151950, 0.150189, 0.148582,
            0.147034, 0.145598, 0.144248]

        swaptionVols = [
            0.170595, 0.166844, 0.158306, 0.147444,
            0.136930, 0.126833, 0.118135, 0.175963,
            0.166359, 0.155203, 0.143712, 0.132769,
            0.122947, 0.114310, 0.174455, 0.162265,
            0.150539, 0.138734, 0.128215, 0.118470,
            0.110540, 0.169780, 0.156860, 0.144821,
            0.133537, 0.123167, 0.114363, 0.106500,
            0.164521, 0.151223, 0.139670, 0.128632,
            0.119123, 0.110330, 0.103114, 0.158956,
            0.146036, 0.134555, 0.124393, 0.115038,
            0.106996, 0.100064]

        index = makeIndex()
        process = LiborForwardModelProcess(size, index)
        termStructure = index.forwardingTermStructure()

        volaModel = LmExtLinearExponentialVolModel(
            process.fixingTimes(),
            0.5, 0.6, 0.1, 0.1)

        corrModel = LmLinearExponentialCorrelationModel(size, 0.5, 0.8)

        model = LiborForwardModel(process, volaModel, corrModel)

        swapVolIndex = 0
        dayCounter = index.forwardingTermStructure().dayCounter()

        calibrationHelpers = CalibrationHelperVector()

        for i in range(2, size):
            maturity = i * index.tenor()
            capVol = QuoteHandle(
                SimpleQuote(capVols[i - 2]))

            caphelper = CapHelper(
                maturity, capVol, index, Annual,
                index.dayCounter(), true, termStructure,
                BlackCalibrationHelper.ImpliedVolError)

            caphelper.setPricingEngine(
                AnalyticCapFloorEngine(model, termStructure))

            calibrationHelpers.append(caphelper)

            if i <= int(size / 2):

                for j in range(1, int(size / 2) + 1):
                    leng = j * index.tenor()
                    swaptionVol = QuoteHandle(
                        SimpleQuote(swaptionVols[swapVolIndex]))

                    swaptionHelper = SwaptionHelper(
                        maturity, leng, swaptionVol, index,
                        index.tenor(), dayCounter,
                        index.dayCounter(),
                        termStructure,
                        BlackCalibrationHelper.ImpliedVolError)

                    swaptionHelper.setPricingEngine(
                        LfmSwaptionEngine(model, termStructure))

                    calibrationHelpers.append(swaptionHelper)
                    swapVolIndex += 1

        om = LevenbergMarquardt(1e-6, 1e-6, 1e-6)
        model.calibrate(
            calibrationHelpers, om,
            EndCriteria(2000, 100, 1e-6, 1e-6, 1e-6))

        calculated = 0.0
        for i in range(len(calibrationHelpers)):
            diff = calibrationHelpers[i].calibrationError()
            calculated += diff * diff

        self.assertFalse(sqrt(calculated) > tolerance)

    def testSwaptionPricing(self):
        TEST_MESSAGE(
            "Testing forward swap and swaption pricing...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        backup = SavedSettings()

        size = 10
        steps = 8 * size

        tolerance = 1e-12 if usingAtParCoupons else 1e-6

        dates = [Date(4, September, 2005), Date(4, September, 2011)]
        rates = [0.04, 0.08]

        index = makeIndex0(dates, rates)

        process = LiborForwardModelProcess(size, index)

        corrModel = LmExponentialCorrelationModel(size, 0.5)

        volaModel = LmLinearExponentialVolatilityModel(
            process.fixingTimes(), 0.291, 1.483, 0.116, 0.00001)

        process.setCovarParam(LfmCovarianceProxy(volaModel, corrModel))

        tmp = process.fixingTimes()
        grid = TimeGrid(tmp, steps)

        location = []
        for i in range(len(tmp)):
            j = 0
            for g in range(len(grid)):
                if close(grid[g], tmp[i]):
                    break
                else:
                    j = j + 1

            location.append(j)

        rsg = GaussianRandomSequenceGenerator(
            UniformRandomSequenceGenerator(
                process.factors() * (len(grid) - 1),
                UniformRandomGenerator(42)))

        nrTrails = 5000
        generator = GaussianMultiPathGenerator(
            process, grid, rsg, false)

        liborModel = LiborForwardModel(process, volaModel, corrModel)

        calendar = index.fixingCalendar()
        dayCounter = index.forwardingTermStructure().dayCounter()
        convention = index.businessDayConvention()

        settlement = index.forwardingTermStructure().referenceDate()

        for i in range(1, size):
            for j in range(1, size - i + 1):
                fwdStart = settlement + Period(6 * i, Months)
                fwdMaturity = fwdStart + Period(6 * j, Months)

                schedule = Schedule(
                    fwdStart, fwdMaturity, index.tenor(), calendar,
                    convention, convention, DateGeneration.Forward, false)

                swapRate = 0.0404
                forwardSwap = VanillaSwap(
                    Swap.Receiver, 1.0,
                    schedule, swapRate, dayCounter,
                    schedule, index, 0.0, index.dayCounter())
                forwardSwap.setPricingEngine(
                    DiscountingSwapEngine(index.forwardingTermStructure()))

                expected = forwardSwap.fairRate()
                calculated = liborModel.S_0(i - 1, i + j - 1)

                self.assertFalse(abs(expected - calculated) > tolerance)

                swapRate = forwardSwap.fairRate()
                forwardSwap = VanillaSwap(
                    Swap.Receiver, 1.0,
                    schedule, swapRate, dayCounter,
                    schedule, index, 0.0, index.dayCounter())
                forwardSwap.setPricingEngine(DiscountingSwapEngine(index.forwardingTermStructure()))

                if i == j and i <= size / 2:
                    engine = LfmSwaptionEngine(
                        liborModel,
                        index.forwardingTermStructure())
                    exercise = EuropeanExercise(process.fixingDates()[i])

                    swaption = Swaption(forwardSwap, exercise)
                    swaption.setPricingEngine(engine)

                    stat = GeneralStatistics()

                    for n in range(nrTrails):
                        path = generator.antithetic() if (n % 2) != 0 else generator.next()

                        rates = DoubleVector(size)
                        for k in range(process.size()):
                            rates[k] = path.value()[k][location[i]]

                        dis = process.discountBond(rates)

                        npv = 0.0
                        for m in range(i, i + j):
                            npv += (swapRate - rates[m]) * (process.accrualEndTimes()[m] - process.accrualStartTimes()[m]) * dis[m]

                        stat.add(max(npv, 0.0))

                    self.assertFalse(
                        abs(swaption.NPV() - stat.mean()) > stat.errorEstimate() * 2.35)
