import unittest
from math import sqrt

from QuantLib import *

from utilities import *


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


class CommonVars(object):
    def __init__(self):

        self.todaysDate_, self.startDate_, self.endDate_ = None, None, None
        self.rateTimes_ = DoubleVector()
        self.accruals_ = DoubleVector()
        self.calendar_ = None
        self.dayCounter_ = None
        self.todaysForwards_ = DoubleVector()
        self.todaysCMSwapRates_ = DoubleVector()
        self.cMSwapAnnuity_ = DoubleVector()
        self.displacement_ = None
        self.todaysDiscounts_ = DoubleVector()
        self.volatilities_ = DoubleVector()
        self.blackVols_ = DoubleVector()
        self.a_, self.b_, self.c_, self.d_ = None, None, None, None
        self.longTermCorrelation_, self.beta_ = None, None
        self.measureOffset_ = None
        self.seed_ = None
        self.paths_, self.trainingPaths_ = None, None
        self.printReport_ = false
        self.spanningForwards_ = None

    def setup(self):

        self.calendar_ = NullCalendar()
        self.todaysDate_ = Settings.instance().evaluationDate

        self.endDate_ = self.todaysDate_ + Period(10, Years)
        dates = Schedule(
            self.todaysDate_, self.endDate_, Period(Semiannual),
            self.calendar_, Following, Following,
            DateGeneration.Backward, false)
        self.rateTimes_ = DoubleVector(len(dates) - 1)

        self.accruals_ = DoubleVector(len(self.rateTimes_) - 1)
        self.dayCounter_ = SimpleDayCounter()
        for i in range(1, len(dates)):
            self.rateTimes_[i - 1] = self.dayCounter_.yearFraction(self.todaysDate_, dates[i])

        for i in range(1, len(self.rateTimes_)):
            self.accruals_[i - 1] = self.rateTimes_[i] - self.rateTimes_[i - 1]

        self.todaysForwards_ = DoubleVector(len(self.accruals_))
        self.displacement_ = 0.02
        for i in range(len(self.todaysForwards_)):
            self.todaysForwards_[i] = 0.03 + 0.0010 * i
        curveState_lmm = LMMCurveState(self.rateTimes_)
        curveState_lmm.setOnForwardRates(self.todaysForwards_)

        self.spanningForwards_ = len(self.todaysForwards_)
        self.todaysCMSwapRates_ = curveState_lmm.cmSwapRates(self.spanningForwards_)

        self.todaysDiscounts_ = DoubleVector(len(self.rateTimes_))
        self.todaysDiscounts_[0] = 0.95
        for i in range(1, len(self.rateTimes_)):
            self.todaysDiscounts_[i] = self.todaysDiscounts_[i - 1] / (1.0 + self.todaysForwards_[i - 1] * self.accruals_[i - 1])

        mktVols = [
            0.15541283,
            0.18719678,
            0.20890740,
            0.22318179,
            0.23212717,
            0.23731450,
            0.23988649,
            0.24066384,
            0.24023111,
            0.23900189,
            0.23726699,
            0.23522952,
            0.23303022,
            0.23076564,
            0.22850101,
            0.22627951,
            0.22412881,
            0.22206569,
            0.22009939]
        self.a_ = -0.0597
        self.b_ = 0.1677
        self.c_ = 0.5403
        self.d_ = 0.1710
        self.volatilities_ = DoubleVector(len(self.todaysCMSwapRates_))
        self.blackVols_ = DoubleVector(len(self.todaysCMSwapRates_))
        for i in range(len(self.todaysCMSwapRates_)):
            self.volatilities_[i] = self.todaysCMSwapRates_[i] * mktVols[i] / (self.todaysCMSwapRates_[i] + self.displacement_)
            self.blackVols_[i] = mktVols[i]

        self.longTermCorrelation_ = 0.5
        self.beta_ = 0.2
        self.measureOffset_ = 5

        self.seed_ = 42

        self.paths_ = 32767
        self.trainingPaths_ = 8191

    def simulate(self,
                 evolver,
                 product):
        initialNumeraire = evolver.numeraires()[0]
        initialNumeraireValue = self.todaysDiscounts_[initialNumeraire]

        engine = AccountingEngine(evolver, product, initialNumeraireValue)
        stats = SequenceStatisticsInc(product.numberOfProducts())
        engine.multiplePathValues(stats, self.paths_)
        return stats

    def makeMarketModel(self,
                        evolution,
                        numberOfFactors,
                        marketModelType,
                        rateBump=0.0,
                        volBump=0.0):
        fixingTimes = evolution.rateTimes()

        ft = DoubleVector(len(fixingTimes) - 1)
        for i in range(len(ft)):
            ft[i] = fixingTimes[i]
        fixingTimes = ft
        volModel = LmExtLinearExponentialVolModel(fixingTimes, 0.5, 0.6, 0.1, 0.1)
        corrModel = LmLinearExponentialCorrelationModel(
            evolution.numberOfRates(),
            self.longTermCorrelation_, self.beta_)
        bumpedRates = DoubleVector(len(self.todaysCMSwapRates_))
        curveState_lmm = LMMCurveState(self.rateTimes_)
        curveState_lmm.setOnForwardRates(self.todaysForwards_)
        usedRates = curveState_lmm.cmSwapRates(self.spanningForwards_)

        for i in range(len(usedRates)):
            bumpedRates[i] += usedRates[i] + rateBump

        bumpedVols = DoubleVector(len(self.volatilities_))

        for i in range(len(self.volatilities_)):
            bumpedVols[i] += self.volatilities_[i] + volBump
        correlations = exponentialCorrelations(
            evolution.rateTimes(),
            self.longTermCorrelation_,
            self.beta_)
        corr = TimeHomogeneousForwardCorrelation(
            correlations,
            evolution.rateTimes())
        if marketModelType == MarketModelType.ExponentialCorrelationFlatVolatility:
            return FlatVol(
                bumpedVols,
                corr,
                evolution,
                numberOfFactors,
                bumpedRates,
                DoubleVector(bumpedRates.size(),
                             self.displacement_))
        if marketModelType == MarketModelType.ExponentialCorrelationAbcdVolatility:
            return AbcdVol(
                0.0, 0.0, 1.0, 1.0,
                bumpedVols,
                corr,
                evolution,
                numberOfFactors,
                bumpedRates,
                DoubleVector(bumpedRates.size(), self.displacement_))

    def makeMarketModelEvolver(
            self,
            marketModel,
            numeraires,
            generatorFactory,
            evolverType,
            initialStep=0):
        if evolverType == EvolverType.Pc:
            return LogNormalCmSwapRatePc(
                self.spanningForwards_,
                marketModel, generatorFactory,
                numeraires,
                initialStep)


class MarketModelCmsTest(unittest.TestCase):

    def testMultiStepCmSwapsAndSwaptions(self):

        TEST_MESSAGE(
            "Testing exact repricing of "
            "multi-step constant maturity swaps and swaptions "
            "in a lognormal constant maturity swap market model...")
        vars = CommonVars()
        vars.setup()

        fixedRate = 0.04

        swapPaymentTimes = DoubleVector(len(vars.rateTimes_) - 1)
        for i in range(len(swapPaymentTimes)):
            swapPaymentTimes[i] = vars.rateTimes_[i + 1]

        swaps = MultiStepCoterminalSwaps(
            vars.rateTimes_, vars.accruals_, vars.accruals_,
            swapPaymentTimes,
            fixedRate)

        swaptionPaymentTimes = DoubleVector(len(vars.rateTimes_) - 1)
        for i in range(len(swaptionPaymentTimes)):
            swaptionPaymentTimes[i] = vars.rateTimes_[i]

        displacedPayoff = StrikedTypePayoffVector(len(vars.todaysForwards_))
        undisplacedPayoff = StrikedTypePayoffVector(len(vars.todaysForwards_))
        for i in range(len(undisplacedPayoff)):
            displacedPayoff[i] = PlainVanillaPayoff(
                Option.Call, fixedRate + vars.displacement_)

            undisplacedPayoff[i] = PlainVanillaPayoff(Option.Call, fixedRate)

        swaptions = MultiStepCoterminalSwaptions(
            vars.rateTimes_,
            swaptionPaymentTimes,
            undisplacedPayoff)
        product = MultiProductComposite()
        product.add(CloneMarketModelMultiProduct(swaps))
        product.add(CloneMarketModelMultiProduct(swaptions))
        product.finalize()

        evolution = product.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility,
            MarketModelType.ExponentialCorrelationAbcdVolatility]

        for j in marketModels:

            testedFactors = [
                len(vars.todaysForwards_)]
            for factors in testedFactors:

                measures = [
                    MeasureType.Terminal,
                    MeasureType.MoneyMarket]
                for measure in measures:
                    numeraires = self.makeMeasure(product, measure, vars)

                    marketModel = vars.makeMarketModel(evolution, factors, j)

                    evolvers = [EvolverType.Pc]

                    evolver = None
                    stop = 0 if isInTerminalMeasure(evolution, numeraires) else 1
                    for i in range(len(evolvers) - stop):
                        for n in range(1):
                            generatorFactory = SobolBrownianGeneratorFactory(
                                SobolBrownianGenerator.Diagonal, vars.seed_)
                            evolver = vars.makeMarketModelEvolver(
                                marketModel,
                                numeraires,
                                generatorFactory,
                                evolvers[i])

                            stats = vars.simulate(
                                evolver,
                                CloneMarketModelMultiProduct(product))
                            self.checkCMSAndSwaptions(
                                stats, fixedRate, displacedPayoff, marketModel, vars)

    def makeMeasure(self,
                    product,
                    measureType,
                    vars):
        result = None
        evolution = product.evolution()
        if measureType == MeasureType.ProductSuggested:
            result = product.suggestedNumeraires()

        if measureType == MeasureType.Terminal:
            result = terminalMeasure(evolution)
            self.assertFalse(not isInTerminalMeasure(evolution, result))

        if measureType == MeasureType.MoneyMarket:
            result = moneyMarketMeasure(evolution)
            self.assertFalse(not isInMoneyMarketMeasure(evolution, result))

        if measureType == MeasureType.MoneyMarketPlus:
            result = moneyMarketPlusMeasure(evolution, vars.measureOffset_)
            self.assertFalse(not isInMoneyMarketPlusMeasure(
                evolution, result, vars.measureOffset_))

        return result

    def checkCMSAndSwaptions(self,
                             stats,
                             fixedRate,
                             displacedPayoff,
                             marketModel,
                             vars):
        results = stats.mean()
        errors = stats.errorEstimate()
        discrepancies = DoubleVector(len(vars.todaysForwards_))

        N = len(vars.todaysForwards_)

        maxError = QL_MIN_REAL
        curveState_lmm = LMMCurveState(vars.rateTimes_)
        curveState_lmm.setOnForwardRates(vars.todaysForwards_)

        expectedNPVs = DoubleVector(len(vars.todaysCMSwapRates_))
        errorThreshold = 0.5
        for i in range(N):
            expectedNPV = curveState_lmm.cmSwapAnnuity(i, i, vars.spanningForwards_) * (vars.todaysCMSwapRates_[i] - fixedRate) * vars.todaysDiscounts_[i]
            expectedNPVs[i] = expectedNPV
            discrepancies[i] = (results[i] - expectedNPVs[i]) / errors[i]
            maxError = max(abs(discrepancies[i]), maxError)

        self.assertFalse(maxError > errorThreshold)

        maxError = 0

        expectedSwaptions = DoubleVector(N)
        for i in range(N):
            expectedSwaption = BlackCalculator(
                displacedPayoff[i],
                vars.todaysCMSwapRates_[i] + vars.displacement_,
                vars.volatilities_[i] * sqrt(vars.rateTimes_[i]),
                curveState_lmm.cmSwapAnnuity(i, i, vars.spanningForwards_)
                * vars.todaysDiscounts_[i]).value()
            expectedSwaptions[i] = expectedSwaption
            discrepancies[i] = (results[N + i] - expectedSwaptions[i]) / errors[N + i]
            maxError = max(abs(discrepancies[i]), maxError)

        errorThreshold = 2.0

        self.assertFalse(maxError > errorThreshold)
