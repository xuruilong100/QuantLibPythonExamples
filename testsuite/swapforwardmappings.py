import unittest
from math import sqrt

from QuantLib import *

from utilities import *

SizeVector = BigNaturalVector


class MarketModelData(object):

    def __init__(self):
        calendar = NullCalendar()
        todaysDate = knownGoodDefault
        endDate = todaysDate + Period(9, Years)
        dates = Schedule(
            todaysDate, endDate, Period(Semiannual),
            calendar, Following, Following, DateGeneration.Backward, false)
        self.nbRates_ = len(dates) - 2
        self.rateTimes_ = DoubleVector(self.nbRates_ + 1)

        self.accruals_ = DoubleVector(self.nbRates_)
        self.dayCounter = SimpleDayCounter()
        for i in range(1, self.nbRates_ + 2):
            self.rateTimes_[i - 1] = self.dayCounter.yearFraction(todaysDate, dates[i])

        self.displacements_ = DoubleVector(self.nbRates_, .0)

        self.forwards_ = DoubleVector(self.nbRates_)
        self.discountFactors_ = DoubleVector(self.nbRates_ + 1)
        self.discountFactors_[0] = 1.0
        for i in range(self.nbRates_):
            self.forwards_[i] = 0.03 + 0.0010 * i
            self.accruals_[i] = self.rateTimes_[i + 1] - self.rateTimes_[i]
            self.discountFactors_[i + 1] = self.discountFactors_[i] / (1 + self.forwards_[i] * self.accruals_[i])

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
        self.volatilities_ = DoubleVector(self.nbRates_)
        for i in range(len(self.volatilities_)):
            self.volatilities_[i] = mktVols[i]

    def rateTimes(self):
        return self.rateTimes_

    def forwards(self):
        return self.forwards_

    def volatilities(self):
        return self.volatilities_

    def displacements(self):
        return self.displacements_

    def discountFactors(self):
        return self.discountFactors_

    def nbRates(self):
        return self.nbRates_


def simulate(todaysDiscounts,
             evolver,
             product):
    paths_ = 32767

    initialNumeraire = evolver.numeraires()[0]
    initialNumeraireValue = todaysDiscounts[initialNumeraire]

    engine = AccountingEngine(evolver, product, initialNumeraireValue)
    stats = SequenceStatisticsInc(product.numberOfProducts())
    engine.multiplePathValues(stats, paths_)
    return stats


def makeMultiStepCoterminalSwaptions(
        rateTimes, strike):
    paymentTimes = DoubleVector(len(rateTimes) - 1)
    for i in range(len(rateTimes) - 1):
        paymentTimes[i] = rateTimes[i]
    payoffs = StrikedTypePayoffVector(len(paymentTimes))
    for i in range(len(paymentTimes)):
        payoffs[i] = PlainVanillaPayoff(Option.Call, strike)

    return MultiStepCoterminalSwaptions(
        rateTimes, paymentTimes, payoffs)


class SwapForwardMappingsTest(unittest.TestCase):

    def testForwardSwapJacobians(self):

        TEST_MESSAGE(
            "Testing forward-rate coinitial-swap Jacobian...")
        marketData = MarketModelData()
        rateTimes = marketData.rateTimes()
        forwards = marketData.forwards()
        nbRates = marketData.nbRates()
        lmmCurveState = LMMCurveState(rateTimes)
        lmmCurveState.setOnForwardRates(forwards)

        bumpSize = 1e-8

        bumpedForwards = forwards

        coinitialJacobian = Matrix(nbRates, nbRates)

        for i in range(nbRates):
            for j in range(nbRates):
                bumpedForwards = forwards
                bumpedForwards[j] += bumpSize
                lmmCurveState.setOnForwardRates(bumpedForwards)
                upRate = lmmCurveState.cmSwapRate(0, i + 1)
                bumpedForwards[j] -= 2.0 * bumpSize
                lmmCurveState.setOnForwardRates(bumpedForwards)
                downRate = lmmCurveState.cmSwapRate(0, i + 1)
                deriv = (upRate - downRate) / (2.0 * bumpSize)
                coinitialJacobian[i][j] = deriv

        modelJacobian = SwapForwardMappings.coinitialSwapForwardJacobian(lmmCurveState)

        errorTolerance = 1e-5

        for i in range(nbRates):
            for j in range(nbRates):
                self.assertFalse(
                    abs(modelJacobian[i][j] - coinitialJacobian[i][j]) > errorTolerance)

        TEST_MESSAGE(
            "Testing forward-rate constant-maturity swap Jacobian...")
        marketData = MarketModelData()
        rateTimes = marketData.rateTimes()
        forwards = marketData.forwards()
        nbRates = marketData.nbRates()
        lmmCurveState = LMMCurveState(rateTimes)
        lmmCurveState.setOnForwardRates(forwards)

        bumpSize = 1e-8

        for spanningForwards in range(1, nbRates):

            bumpedForwards = forwards

            cmsJacobian = Matrix(nbRates, nbRates)

            for i in range(nbRates):
                for j in range(nbRates):
                    bumpedForwards = forwards
                    bumpedForwards[j] += bumpSize
                    lmmCurveState.setOnForwardRates(bumpedForwards)
                    upRate = lmmCurveState.cmSwapRate(i, spanningForwards)
                    bumpedForwards[j] -= 2.0 * bumpSize
                    lmmCurveState.setOnForwardRates(bumpedForwards)
                    downRate = lmmCurveState.cmSwapRate(i, spanningForwards)
                    deriv = (upRate - downRate) / (2.0 * bumpSize)
                    cmsJacobian[i][j] = deriv

            modelJacobian = SwapForwardMappings.cmSwapForwardJacobian(
                lmmCurveState, spanningForwards)

            errorTolerance = 1e-5

            for i in range(nbRates):
                for j in range(nbRates):
                    self.assertFalse(abs(modelJacobian[i][j] - cmsJacobian[i][j]) > errorTolerance)

    def testForwardCoterminalMappings(self):

        TEST_MESSAGE(
            "Testing forward-rate coterminal-swap mappings...")
        marketData = MarketModelData()
        rateTimes = marketData.rateTimes()
        forwards = marketData.forwards()
        nbRates = marketData.nbRates()
        lmmCurveState = LMMCurveState(rateTimes)
        lmmCurveState.setOnForwardRates(forwards)

        longTermCorr = 0.5
        beta = .2
        strike = .03
        product = makeMultiStepCoterminalSwaptions(rateTimes, strike)

        evolution = product.evolution()
        numberOfFactors = nbRates
        displacement = marketData.displacements()[0]
        jacobian = SwapForwardMappings.coterminalSwapZedMatrix(
            lmmCurveState, displacement)

        correlations = exponentialCorrelations(
            evolution.rateTimes(),
            longTermCorr,
            beta)
        corr = TimeHomogeneousForwardCorrelation(correlations,
                                                 rateTimes)
        smmMarketModel = FlatVol(
            marketData.volatilities(),
            corr,
            evolution,
            numberOfFactors,
            lmmCurveState.coterminalSwapRates(),
            marketData.displacements())

        lmmMarketModel = CotSwapToFwdAdapter(smmMarketModel)

        generatorFactory = SobolBrownianGeneratorFactory(SobolBrownianGenerator.Diagonal)
        numeraires = SizeVector(nbRates, nbRates)
        evolver = LogNormalFwdRatePc(lmmMarketModel, generatorFactory, numeraires)

        stats = simulate(marketData.discountFactors(), evolver,
                         CloneMarketModelMultiProduct(product))
        results = stats.mean()
        errors = stats.errorEstimate()

        todaysDiscounts = marketData.discountFactors()
        todaysCoterminalSwapRates = lmmCurveState.coterminalSwapRates()
        for i in range(nbRates):
            cotSwapsCovariance = smmMarketModel.totalCovariance(i)

            payoff = PlainVanillaPayoff(Option.Call, strike + displacement)

            expectedSwaption = BlackCalculator(
                payoff,
                todaysCoterminalSwapRates[i] + displacement,
                sqrt(cotSwapsCovariance[i][i]),
                lmmCurveState.coterminalSwapAnnuity(i, i) *
                todaysDiscounts[i]).value()

            self.assertFalse(abs(expectedSwaption - results[i]) > 0.01)

    def testSwaptionImpliedVolatility(self):

        TEST_MESSAGE(
            "Testing implied swaption vol in LMM using HW approximation...")
        marketData = MarketModelData()
        rateTimes = marketData.rateTimes()
        forwards = marketData.forwards()
        nbRates = marketData.nbRates()
        lmmCurveState = LMMCurveState(rateTimes)
        lmmCurveState.setOnForwardRates(forwards)

        longTermCorr = 0.5
        beta = .2
        strike = .03

        for startIndex in range(1, nbRates - 2, + 5):
            endIndex = nbRates - 2

            payoff = PlainVanillaPayoff(Option.Call, strike)
            product = MultiStepSwaption(rateTimes, startIndex, endIndex, payoff)

            evolution = product.evolution()
            numberOfFactors = nbRates
            displacement = marketData.displacements()[0]
            jacobian = SwapForwardMappings.coterminalSwapZedMatrix(
                lmmCurveState, displacement)

            correlations = exponentialCorrelations(
                evolution.rateTimes(),
                longTermCorr,
                beta)
            corr = TimeHomogeneousForwardCorrelation(correlations,
                                                     rateTimes)
            lmmMarketModel = FlatVol(
                marketData.volatilities(),
                corr,
                evolution,
                numberOfFactors,
                lmmCurveState.forwardRates(),
                marketData.displacements())

            generatorFactory = SobolBrownianGeneratorFactory(
                SobolBrownianGenerator.Diagonal)
            numeraires = SizeVector(nbRates, nbRates)
            evolver = LogNormalFwdRatePc(
                lmmMarketModel, generatorFactory, numeraires)

            stats = simulate(marketData.discountFactors(), evolver,
                             CloneMarketModelMultiProduct(product))
            results = stats.mean()
            errors = stats.errorEstimate()

            estimatedImpliedVol = SwapForwardMappings.swaptionImpliedVolatility(
                lmmMarketModel, startIndex, endIndex)

            swapRate = lmmCurveState.cmSwapRate(startIndex, endIndex - startIndex)
            swapAnnuity = lmmCurveState.cmSwapAnnuity(startIndex, startIndex, endIndex - startIndex) * \
                          marketData.discountFactors()[startIndex]

            payoffDis = PlainVanillaPayoff(Option.Call, strike + displacement)

            expectedSwaption = BlackCalculator(
                payoffDis,
                swapRate + displacement,
                estimatedImpliedVol * sqrt(rateTimes[startIndex]),
                swapAnnuity).value()

            error = expectedSwaption - results[0]
            errorInSds = error / errors[0]
            self.assertFalse(abs(errorInSds) > 3.5)
