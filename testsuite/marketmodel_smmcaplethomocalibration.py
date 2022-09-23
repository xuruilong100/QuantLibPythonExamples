import unittest
from math import sqrt

from QuantLib import *

from utilities import *


class CommonVars(object):
    def __init__(self):
        self.todaysDate_, self.startDate_, self.endDate_ = None, None, None
        self.rateTimes_ = DoubleVector()
        self.accruals_ = DoubleVector()
        self.calendar_ = None
        self.dayCounter_ = None
        self.todaysForwards_ = DoubleVector()
        self.todaysSwaps_ = DoubleVector()
        self.coterminalAnnuity_ = DoubleVector()
        self.numberOfFactors_ = None
        self.alpha_, self.alphaMax_, self.alphaMin_ = None, None, None
        self.displacement_ = None
        self.todaysDiscounts_ = DoubleVector()
        self.swaptionDisplacedVols_ = DoubleVector()
        self.swaptionVols_ = DoubleVector()
        self.capletDisplacedVols_ = DoubleVector()
        self.capletVols_ = DoubleVector()
        self.a_, self.b_, self.c_, self.d_ = None, None, None, None
        self.longTermCorrelation_, self.beta_ = None, None
        self.measureOffset_ = None
        self.seed_ = None
        self.paths_, self.trainingPaths_ = None, None
        self.printReport_ = false

    def setup(self):

        self.calendar_ = NullCalendar()
        self.todaysDate_ = Settings.instance().evaluationDate

        self.endDate_ = self.todaysDate_ + Period(66, Months)
        dates = Schedule(
            self.todaysDate_, self.endDate_, Period(Semiannual),
            self.calendar_, Following, Following, DateGeneration.Backward, false)
        self.rateTimes_ = DoubleVector(len(dates) - 1)
        self.accruals_ = DoubleVector(len(self.rateTimes_) - 1)
        self.dayCounter_ = SimpleDayCounter()
        for i in range(1, len(dates)):
            self.rateTimes_[i - 1] = self.dayCounter_.yearFraction(self.todaysDate_, dates[i])
        for i in range(1, len(self.rateTimes_)):
            self.accruals_[i - 1] = self.rateTimes_[i] - self.rateTimes_[i - 1]

        self.todaysForwards_ = DoubleVector(self.accruals_.size())
        self.numberOfFactors_ = 3
        self.alpha_ = 0.0
        self.alphaMax_ = 1.0
        self.alphaMin_ = -1.0
        self.displacement_ = 0.0
        for i in range(len(self.todaysForwards_)):
            self.todaysForwards_[i] = 0.03 + 0.0025 * i

        curveState_lmm = LMMCurveState(self.rateTimes_)
        curveState_lmm.setOnForwardRates(self.todaysForwards_)
        self.todaysSwaps_ = curveState_lmm.coterminalSwapRates()

        todaysDiscounts_ = DoubleVector(len(self.rateTimes_))
        todaysDiscounts_[0] = 0.95
        for i in range(1, len(self.rateTimes_)):
            todaysDiscounts_[i] = todaysDiscounts_[i - 1] / (1.0 + self.todaysForwards_[i - 1] * self.accruals_[i - 1])

        self.a_ = 0.0
        self.b_ = 0.17
        self.c_ = 1.0
        self.d_ = 0.10

        mktCapletVols = [
            0.1640,
            0.1740,
            0.1840,
            0.1940,
            0.1840,
            0.1740,
            0.1640,
            0.1540,
            0.1440,
            0.1340376439125532]

        self.capletVols_.resize(len(self.todaysSwaps_))
        for i in range(len(self.todaysSwaps_)):
            self.capletVols_[i] = mktCapletVols[i]

        self.longTermCorrelation_ = 0.5
        self.beta_ = 0.2
        self.measureOffset_ = 5

        self.seed_ = 42

        self.paths_ = 127
        self.trainingPaths_ = 31

        self.paths_ = 32767
        self.trainingPaths_ = 8191


class MarketModelType(object):
    ExponentialCorrelationFlatVolatility = 1
    ExponentialCorrelationAbcdVolatility = 2

    def __init__(self):
        pass


class MeasureType(object):
    ProductSuggested = 1
    Terminal = 2
    MoneyMarket = 3
    MoneyMarketPlus = 4

    def __init__(self):
        pass


class EvolverType(object):
    Ipc, Pc, NormalPc = 1, 3, 4

    def __init__(self):
        pass


class MarketModelSmmCapletHomoCalibrationTest(unittest.TestCase):

    def testFunction(self):

        TEST_MESSAGE(
            "Testing max homogeneity caplet calibration "
            "in a lognormal coterminal swap market model...")

        vars = CommonVars()
        vars.setup()

        numberOfRates = len(vars.todaysForwards_)

        evolution = EvolutionDescription(vars.rateTimes_)

        fwdCorr = ExponentialForwardCorrelation(
            vars.rateTimes_,
            vars.longTermCorrelation_,
            vars.beta_)

        cs = LMMCurveState(vars.rateTimes_)
        cs.setOnForwardRates(vars.todaysForwards_)

        corr = CotSwapFromFwdCorrelation(fwdCorr, cs, vars.displacement_)

        swapVariances = PiecewiseConstantVarianceVector(numberOfRates)
        for i in range(numberOfRates):
            swapVariances[i] = PiecewiseConstantAbcdVariance(
                vars.a_, vars.b_, vars.c_, vars.d_,
                i, vars.rateTimes_)

        caplet0Swaption1Priority = 1.0

        calibrator = CTSMMCapletMaxHomogeneityCalibration(
            evolution,
            corr,
            swapVariances,
            vars.capletVols_,
            cs,
            vars.displacement_,
            caplet0Swaption1Priority)

        maxIterations = 10
        capletTolerance = 1e-4
        innerMaxIterations = 100
        innerTolerance = 1e-8

        result = calibrator.calibrate(
            vars.numberOfFactors_,
            maxIterations,
            capletTolerance,
            innerMaxIterations,
            innerTolerance)
        self.assertFalse(not result)

        swapPseudoRoots = calibrator.swapPseudoRoots()
        smm = PseudoRootFacade(
            swapPseudoRoots,
            vars.rateTimes_,
            cs.coterminalSwapRates(),
            DoubleVector(numberOfRates, vars.displacement_))
        flmm = CotSwapToFwdAdapter(smm)
        capletTotCovariance = flmm.totalCovariance(numberOfRates - 1)

        capletVols = DoubleVector(numberOfRates)
        for i in range(numberOfRates):
            capletVols[i] = sqrt(capletTotCovariance[i][i] / vars.rateTimes_[i])

        swapTolerance = 1e-14
        swapTerminalCovariance = Matrix(numberOfRates, numberOfRates, 0.0)
        for i in range(numberOfRates):
            expSwaptionVol = swapVariances[i].totalVolatility(i)
            swapTerminalCovariance += swapPseudoRoots[i] * transpose(swapPseudoRoots[i])
            swaptionVol = sqrt(swapTerminalCovariance[i][i] / vars.rateTimes_[i])
            error = abs(swaptionVol - expSwaptionVol)
            self.assertFalse(error > swapTolerance)

        for i in range(numberOfRates):
            error = abs(capletVols[i] - vars.capletVols_[i])
            self.assertFalse(error > capletTolerance)
        period = 2
        offset = 0
        adaptedDisplacements = DoubleVector()
        adapted = FwdPeriodAdapter(flmm, period, offset, adaptedDisplacements)

    def testPeriodFunction(self):

        TEST_MESSAGE(
            "Testing max homogeneity periodic caplet calibration "
            "in a lognormal coterminal swap market model...")

        vars = CommonVars()
        vars.setup()

        numberOfRates = len(vars.todaysForwards_)
        period = 2
        offset = numberOfRates % period
        numberBigRates = int(numberOfRates / period)

        evolution = EvolutionDescription(vars.rateTimes_)

        bigRateTimes = DoubleVector(numberBigRates + 1)

        for i in range(0, numberBigRates + 1):
            bigRateTimes[i] = vars.rateTimes_[i * period + offset]

        fwdCorr = ExponentialForwardCorrelation(
            vars.rateTimes_,
            vars.longTermCorrelation_,
            vars.beta_)

        cs = LMMCurveState(vars.rateTimes_)
        cs.setOnForwardRates(vars.todaysForwards_)

        corr = CotSwapFromFwdCorrelation(fwdCorr, cs, vars.displacement_)

        swapVariances = PiecewiseConstantAbcdVarianceVector()
        for i in range(numberBigRates):
            swapVariances.append(
                PiecewiseConstantAbcdVariance(
                    vars.a_, vars.b_, vars.c_, vars.d_, i, bigRateTimes))

        varianceInterpolator = VolatilityInterpolationSpecifierabcd(
            period, offset, swapVariances,
            vars.rateTimes_)

        caplet0Swaption1Priority = 1.0

        maxUnperiodicIterations = 10
        toleranceUnperiodic = 1e-5
        max1dIterations = 100
        tolerance1d = 1e-8
        maxPeriodIterations = 30
        periodTolerance = 1e-5

        swapPseudoRoots = MatrixVector()
        deformationSize = Value()
        totalSwaptionError = Value()
        finalScales = DoubleVector()
        iterationsDone = Value()
        errorImprovement = Value()
        modelSwaptionVolsMatrix = Matrix()

        capletSwaptionPeriodicCalibration(
            evolution,
            corr,
            varianceInterpolator,
            vars.capletVols_,
            cs,
            vars.displacement_,
            caplet0Swaption1Priority,
            vars.numberOfFactors_,
            period,
            max1dIterations,
            tolerance1d,
            maxUnperiodicIterations,
            toleranceUnperiodic,
            maxPeriodIterations,
            periodTolerance,
            deformationSize,
            totalSwaptionError,
            swapPseudoRoots,
            finalScales,
            iterationsDone,
            errorImprovement,
            modelSwaptionVolsMatrix)

        smm = PseudoRootFacade(
            swapPseudoRoots,
            vars.rateTimes_,
            cs.coterminalSwapRates(),
            DoubleVector(numberOfRates, vars.displacement_))
        flmm = CotSwapToFwdAdapter(smm)
        capletTotCovariance = flmm.totalCovariance(numberOfRates - 1)

        capletVols = DoubleVector(numberOfRates)
        for i in range(numberOfRates):
            capletVols[i] = sqrt(capletTotCovariance[i][i] / vars.rateTimes_[i])

        capletTolerance = 1e-4

        for i in range(numberOfRates):
            error = abs(capletVols[i] - vars.capletVols_[i])
            self.assertFalse(error > capletTolerance)

        adaptedDisplacements = DoubleVector(numberBigRates, vars.displacement_)
        adaptedFlmm = FwdPeriodAdapter(flmm, period, offset, adaptedDisplacements)

        adaptedsmm = FwdToCotSwapAdapter(adaptedFlmm)

        swapTolerance = 2e-5

        swapTerminalCovariance = Matrix(
            adaptedsmm.totalCovariance(adaptedsmm.numberOfSteps() - 1))

        for i in range(numberBigRates):
            expSwaptionVol = swapVariances[i].totalVolatility(i)

            time = adaptedsmm.evolution().rateTimes()[i]
            swaptionVol = sqrt(swapTerminalCovariance[i][i] / time)

            error = abs(swaptionVol - expSwaptionVol)
            self.assertFalse(error > swapTolerance)

    def testSphereCylinder(self):

        TEST_MESSAGE(
            "Testing sphere-cylinder optimization...")

        R = 1.0
        S = 0.5
        alpha = 1.5
        Z1 = 1.0 / sqrt(3.0)
        Z2 = 1.0 / sqrt(3.0)
        Z3 = 1.0 / sqrt(3.0)

        optimizer = SphereCylinderOptimizer(R, S, alpha, Z1, Z2, Z3)
        maxIterations = 100
        tolerance = 1e-8
        y1 = Value()
        y2 = Value()
        y3 = Value()

        optimizer.findClosest(maxIterations, tolerance, y1, y2, y3)

        errorTol = 1e-12
        self.assertFalse(abs(y1.value() - 1.0) > errorTol)
        self.assertFalse(abs(y2.value() - 0.0) > errorTol)
        self.assertFalse(abs(y3.value() - 0.0) > errorTol)

        optimizer.findByProjection(y1, y2, y3)

        self.assertFalse(abs(y1.value() - 1.0) > errorTol)
        self.assertFalse(abs(y2.value() - 0.0) > errorTol)
        self.assertFalse(abs(y3.value() - 0.0) > errorTol)

        R = 5.0
        S = 1.0
        alpha = 1.0
        Z1 = 1.0
        Z2 = 2.0
        Z3 = sqrt(20.0)

        optimizer = SphereCylinderOptimizer(R, S, alpha, Z1, Z2, Z3)
        maxIterations = 100
        tolerance = 1e-8
        y1 = Value()
        y2 = Value()
        y3 = Value()

        optimizer.findClosest(maxIterations, tolerance, y1, y2, y3)

        errorTol = 1e-4
        self.assertFalse(abs(y1.value() - 1.03306) > errorTol)
        self.assertFalse(abs(y2.value() - 0.999453) > errorTol)
        self.assertFalse(abs(y3.value() - 4.78893) > errorTol)

        optimizer.findByProjection(y1, y2, y3)

        self.assertFalse(abs(y1.value() - 1.0) > errorTol)
        self.assertFalse(abs(y2.value() - 1.0) > errorTol)
        self.assertFalse(abs(y3.value() - sqrt(23.0)) > errorTol)
