import unittest
from math import sqrt

from QuantLib import *

from utilities import *

SizeVector = BigNaturalVector


class MarketModelType(object):
    ExponentialCorrelationFlatVolatility = 1
    ExponentialCorrelationAbcdVolatility = 2

    def __init__(self):
        pass


class SubProductExpectedValues(object):
    def __init__(self, descr):
        self.description = descr
        self.testBias = false
        self.description = ""
        self.values = DoubleVector()
        self.testBias = None
        self.errorThreshold = None


def marketModelTypeToString(type):
    if type == MarketModelType.ExponentialCorrelationFlatVolatility:
        return "Exp. Corr. Flat Vol."
    if type == MarketModelType.ExponentialCorrelationAbcdVolatility:
        return "Exp. Corr. Abcd Vol."


class MeasureType(object):
    ProductSuggested = 1
    Terminal = 2
    MoneyMarket = 3
    MoneyMarketPlus = 4

    def __init__(self):
        pass


def measureTypeToString(type):
    if type == MeasureType.ProductSuggested:
        return "ProductSuggested measure"
    if type == MeasureType.Terminal:
        return "Terminal measure"
    if type == MeasureType.MoneyMarket:
        return "Money Market measure"
    if type == MeasureType.MoneyMarketPlus:
        return "Money Market Plus measure"


class EvolverType(object):
    Ipc, Balland, Pc, NormalPc = 1, 2, 3, 4

    def __init__(self):
        pass


def makeMarketModelEvolver(marketModel,
                           numeraires,
                           generatorFactory,
                           evolverType,
                           initialStep=0):
    if evolverType == EvolverType.Ipc:
        return LogNormalFwdRateIpc(
            marketModel, generatorFactory,
            numeraires, initialStep)
    if evolverType == EvolverType.Balland:
        return LogNormalFwdRateBalland(
            marketModel, generatorFactory,
            numeraires, initialStep)
    if evolverType == EvolverType.Pc:
        return LogNormalFwdRatePc(
            marketModel, generatorFactory,
            numeraires, initialStep)
    if evolverType == EvolverType.NormalPc:
        return NormalFwdRatePc(
            marketModel, generatorFactory,
            numeraires, initialStep)


class CommonVars(object):
    def __init__(self):
        self.todaysDate = Date()
        self.startDate = Date()
        self.endDate = Date()
        self.dates = Schedule()
        self.rateTimes = DoubleVector()
        self.paymentTimes = DoubleVector()
        self.accruals = DoubleVector()
        self.calendar = None
        self.dayCounter = None
        self.todaysForwards = DoubleVector()
        self.todaysCoterminalSwapRates = DoubleVector()
        self.meanForward = None
        self.coterminalAnnuity = DoubleVector()
        self.displacement = None
        self.todaysDiscounts = DoubleVector()
        self.volatilities = DoubleVector()
        self.blackVols = DoubleVector()
        self.normalVols = DoubleVector()
        self.swaptionsVolatilities = DoubleVector()
        self.swaptionsBlackVols = DoubleVector()
        self.a, self.b, self.c, self.d = None, None, None, None
        self.longTermCorrelation, self.beta = None, None
        self.measureOffset_ = None
        self.seed_ = None
        self.paths_, self.trainingPaths_ = None, None
        self.printReport_ = false

    def setup(self):

        self.calendar = NullCalendar()
        self.todaysDate = knownGoodDefault

        self.endDate = self.todaysDate + Period(5, Years)
        dates = Schedule(
            self.todaysDate, self.endDate, Period(Semiannual),
            self.calendar, Following, Following,
            DateGeneration.Backward, false)
        self.rateTimes = DoubleVector(len(dates) - 1)
        self.paymentTimes = DoubleVector(len(self.rateTimes) - 1)
        self.accruals = DoubleVector(len(self.rateTimes) - 1)
        self.dayCounter = SimpleDayCounter()
        for i in range(1, len(dates)):
            self.rateTimes[i - 1] = self.dayCounter.yearFraction(self.todaysDate, dates[i])

        for i in range(1, len(self.rateTimes)):
            self.paymentTimes[i - 1] = self.rateTimes[i]
        for i in range(1, len(self.rateTimes)):
            self.accruals[i - 1] = self.rateTimes[i] - self.rateTimes[i - 1]

        self.todaysForwards = DoubleVector(self.paymentTimes.size())
        self.displacement = 0.0
        self.meanForward = 0.0

        for i in range(len(self.todaysForwards)):
            self.todaysForwards[i] = 0.03 + 0.0010 * i
            self.meanForward += self.todaysForwards[i]

        self.meanForward /= len(self.todaysForwards)

        self.todaysDiscounts = DoubleVector(len(self.rateTimes))
        self.todaysDiscounts[0] = 0.95
        for i in range(1, len(self.rateTimes)):
            self.todaysDiscounts[i] = self.todaysDiscounts[i - 1] / (
                    1.0 + self.todaysForwards[i - 1] * self.accruals[i - 1])

        N = len(self.todaysForwards)
        self.todaysCoterminalSwapRates = DoubleVector(N)
        coterminalAnnuity = DoubleVector(N)
        floatingLeg = 0.0
        for i in range(1, N + 1):
            if i == 1:
                coterminalAnnuity[N - 1] = self.accruals[N - 1] * self.todaysDiscounts[N]
            else:
                coterminalAnnuity[N - i] = coterminalAnnuity[N - i + 1] + self.accruals[N - i] * self.todaysDiscounts[
                    N - i + 1]

            floatingLeg = self.todaysDiscounts[N - i] - self.todaysDiscounts[N]
            self.todaysCoterminalSwapRates[N - i] = floatingLeg / coterminalAnnuity[N - i]

        mktVols = [
            0.15541283, 0.18719678, 0.20890740, 0.22318179,
            0.23212717, 0.23731450, 0.23988649, 0.24066384,
            0.24023111, 0.23900189, 0.23726699, 0.23522952,
            0.23303022, 0.23076564, 0.22850101, 0.22627951,
            0.22412881, 0.22206569, 0.22009939]

        self.a = -0.0597
        self.b = 0.1677
        self.c = 0.5403
        self.d = 0.1710
        self.volatilities = DoubleVector(len(self.todaysForwards))
        self.blackVols = DoubleVector(len(self.todaysForwards))
        self.normalVols = DoubleVector(len(self.todaysForwards))
        for i in range(min(len(mktVols), len(self.todaysForwards))):
            self.volatilities[i] = self.todaysForwards[i] * mktVols[i] / (self.todaysForwards[i] + self.displacement)
            self.blackVols[i] = mktVols[i]
            self.normalVols[i] = mktVols[i] * self.todaysForwards[i]

        self.swaptionsVolatilities = self.volatilities

        self.longTermCorrelation = 0.5
        self.beta = 0.2
        self.measureOffset_ = 5

        self.seed_ = 42

        self.paths_ = 127
        self.trainingPaths_ = 31

        self.paths_ = 32767
        self.trainingPaths_ = 8191

    def simulate(self,
                 evolver,
                 product):
        initialNumeraire = evolver.numeraires()[0]
        initialNumeraireValue = self.todaysDiscounts[initialNumeraire]

        engine = AccountingEngine(evolver, product, initialNumeraireValue)
        stats = SequenceStatisticsInc(product.numberOfProducts())
        engine.multiplePathValues(stats, self.paths_)
        return stats

    def makeMarketModel(
            self,
            logNormal,
            evolution,
            numberOfFactors,
            marketModelType,
            forwardBump=0.0,
            volBump=0.0):
        fixingTimes = evolution.rateTimes()

        fixingTimes = fixingTimes[0:-1]
        volModel = LmExtLinearExponentialVolModel(fixingTimes, 0.5, 0.6, 0.1, 0.1)
        corrModel = LmLinearExponentialCorrelationModel(
            evolution.numberOfRates(),
            self.longTermCorrelation, self.beta)

        bumpedForwards = DoubleVector(len(self.todaysForwards))

        for i in range(len(self.todaysForwards)):
            bumpedForwards[i] = self.todaysForwards[i] + forwardBump

        bumpedVols = DoubleVector(self.volatilities.size())
        if logNormal:

            for i in range(len(self.volatilities)):
                bumpedVols[i] = self.volatilities[i] + volBump
        else:

            for i in range(len(self.normalVols)):
                bumpedVols[i] += self.normalVols[i]

        correlations = exponentialCorrelations(
            evolution.rateTimes(),
            self.longTermCorrelation,
            self.beta)
        corr = TimeHomogeneousForwardCorrelation(correlations,
                                                 evolution.rateTimes())
        if marketModelType == MarketModelType.ExponentialCorrelationFlatVolatility:
            return FlatVol(
                bumpedVols,
                corr,
                evolution,
                numberOfFactors,
                bumpedForwards,
                DoubleVector(bumpedForwards.size(), self.displacement))
        if marketModelType == MarketModelType.ExponentialCorrelationAbcdVolatility:
            return AbcdVol(
                0.0, 0.0, 1.0, 1.0,
                bumpedVols,
                corr,
                evolution,
                numberOfFactors,
                bumpedForwards,
                DoubleVector(bumpedForwards.size(), self.displacement))

    def addForwards(self,
                    product,
                    subProductExpectedValues):

        forwardStrikes = DoubleVector(len(self.todaysForwards))

        for i in range(len(self.todaysForwards)):
            forwardStrikes[i] = self.todaysForwards[i] + 0.01

        forwards = MultiStepForwards(self.rateTimes, self.accruals,
                                     self.paymentTimes, forwardStrikes)
        product.add(CloneMarketModelMultiProduct(forwards))

        subProductExpectedValues.append(SubProductExpectedValues("Forward"))
        subProductExpectedValues[-1].errorThreshold = 2.50
        for i in range(len(self.todaysForwards)):
            subProductExpectedValues[-1].values.append(
                (self.todaysForwards[i] - forwardStrikes[i]) * self.accruals[i] * self.todaysDiscounts[i + 1])

    def addOptionLets(self,
                      product,
                      subProductExpectedValues):

        optionletPayoffs = PayoffVector(len(self.todaysForwards))
        displacedPayoffs = StrikedTypePayoffVector(len(self.todaysForwards))

        for i in range(len(self.todaysForwards)):
            optionletPayoffs[i] = PlainVanillaPayoff(Option.Call, self.todaysForwards[i])

            displacedPayoffs[i] = PlainVanillaPayoff(Option.Call, self.todaysForwards[i] + self.displacement)

        optionlets = MultiStepOptionlets(self.rateTimes, self.accruals,
                                         self.paymentTimes, optionletPayoffs)
        product.add(CloneMarketModelMultiProduct(optionlets))

        subProductExpectedValues.append(SubProductExpectedValues("Caplet"))
        subProductExpectedValues[-1].errorThreshold = 2.50
        for i in range(len(self.todaysForwards)):
            subProductExpectedValues[-1].values.append(
                BlackCalculator(
                    displacedPayoffs[i],
                    self.todaysForwards[i] + self.displacement,
                    self.volatilities[i] * sqrt(self.rateTimes[i]),
                    self.todaysDiscounts[i + 1] * self.accruals[i]).value())

    def addCoinitialSwaps(self,
                          product,
                          subProductExpectedValues):

        fixedRate = 0.04
        multiStepCoinitialSwaps = MultiStepCoinitialSwaps(
            self.rateTimes, self.accruals, self.accruals,
            self.paymentTimes, fixedRate)
        product.add(
            CloneMarketModelMultiProduct(multiStepCoinitialSwaps))

        subProductExpectedValues.append(SubProductExpectedValues("coinitial swap"))
        subProductExpectedValues[-1].testBias = false
        subProductExpectedValues[-1].errorThreshold = 2.32
        coinitialSwapValue = 0
        for i in range(len(self.todaysForwards)):
            coinitialSwapValue += (self.todaysForwards[i] - fixedRate) * self.accruals[i] * self.todaysDiscounts[i + 1]
            subProductExpectedValues[-1].values.append(coinitialSwapValue)

    def addCoterminalSwapsAndSwaptions(self,
                                       product,
                                       subProductExpectedValues):
        fixedRate = 0.04
        swaps = MultiStepCoterminalSwaps(
            self.rateTimes, self.accruals, self.accruals,
            self.paymentTimes, fixedRate)

        payoffs = StrikedTypePayoffVector(len(self.todaysForwards))
        for i in range(len(payoffs)):
            payoffs[i] = PlainVanillaPayoff(Option.Call, self.todaysForwards[i])

        swaptions = MultiStepCoterminalSwaptions(self.rateTimes,
                                                 self.rateTimes, payoffs)
        product.add(CloneMarketModelMultiProduct(swaps))
        product.add(CloneMarketModelMultiProduct(swaptions))

        subProductExpectedValues.append(SubProductExpectedValues("coterminal swap"))
        subProductExpectedValues[-1].testBias = false
        subProductExpectedValues[-1].errorThreshold = 2.32
        curveState = LMMCurveState(self.rateTimes)
        curveState.setOnForwardRates(self.todaysForwards)
        atmRates = curveState.coterminalSwapRates()
        for i in range(len(self.todaysForwards)):
            expectedNPV = curveState.coterminalSwapAnnuity(0, i) * (atmRates[i] - fixedRate) * self.todaysDiscounts[0]
            subProductExpectedValues[-1].values.append(expectedNPV)

        productClone = MultiProductComposite()
        for i in range(product.size()):
            productClone.add(CloneMarketModelMultiProduct(product.item(i)))

        productClone.finalize()
        subProductExpectedValues.append(SubProductExpectedValues("coterminal swaption"))
        subProductExpectedValues[-1].testBias = false
        subProductExpectedValues[-1].errorThreshold = 2.32
        displacement = 0
        jacobian = SwapForwardMappings.coterminalSwapZedMatrix(
            curveState, displacement)
        logNormal = true

        evolution = productClone.evolution()
        factors = len(self.todaysForwards)
        marketModelType = MarketModelType.ExponentialCorrelationFlatVolatility
        marketModel = self.makeMarketModel(logNormal, evolution, factors, marketModelType)
        for i in range(len(self.todaysForwards)):
            forwardsCovariance = marketModel.totalCovariance(i)
            cotSwapsCovariance = jacobian * forwardsCovariance * transpose(jacobian)
            payoff = PlainVanillaPayoff(Option.Call, self.todaysForwards[i] + displacement)

            expectedSwaption = BlackCalculator(
                payoff,
                self.todaysCoterminalSwapRates[i] + displacement,
                sqrt(cotSwapsCovariance[i][i]),
                curveState.coterminalSwapAnnuity(0, i) *
                self.todaysDiscounts[0]).value()
            subProductExpectedValues[-1].values.append(expectedSwaption)


class MarketModelTest(unittest.TestCase):

    def testInverseFloater(self):

        TEST_MESSAGE(
            "Testing exact repricing of "
            "inverse floater "
            "in forward rate market model...")

        vars = CommonVars()
        vars.setup()

        fixedStrikes = DoubleVector(len(vars.accruals), 0.1)
        fixedMultipliers = DoubleVector(len(vars.accruals), 2.0)
        floatingSpreads = DoubleVector(len(vars.accruals), 0.002)
        fixedAccruals = DoubleVector(vars.accruals)
        floatingAccruals = DoubleVector(vars.accruals)

        payer = true

        product = CloneMarketModelMultiProduct(MultiStepInverseFloater(
            vars.rateTimes,
            fixedAccruals,
            floatingAccruals,
            fixedStrikes,
            fixedMultipliers,
            floatingSpreads,
            vars.paymentTimes,
            payer))

        productPathwise = MarketModelPathwiseInverseFloater(
            vars.rateTimes,
            fixedAccruals,
            floatingAccruals,
            fixedStrikes,
            fixedMultipliers,
            floatingSpreads,
            vars.paymentTimes,
            payer)

        productWrapped = CloneMarketModelMultiProduct(
            MultiProductPathwiseWrapper(productPathwise))

        productComposite = MultiProductComposite()
        productComposite.add(product)
        productComposite.add(productWrapped)
        productComposite.finalize()

        evolution = productComposite.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility,
            MarketModelType.ExponentialCorrelationAbcdVolatility]
        for j in marketModels:

            testedFactors = [min(len(vars.todaysForwards), 3)]
            for factors in testedFactors:
                measures = [MeasureType.MoneyMarket]
                for measure in measures:
                    numeraires = self.makeMeasure(product, measure, vars)

                    logNormal = false
                    marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                    evolvers = [EvolverType.Pc]
                    evolver = None

                    for i in evolvers:

                        generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                        evolver = makeMarketModelEvolver(
                            marketModel, numeraires, generatorFactory, i)

                        stats = vars.simulate(evolver, CloneMarketModelMultiProduct(productComposite))

                        modelVolatilities = DoubleVector(len(vars.accruals))
                        for i in range(len(vars.accruals)):
                            modelVolatilities[i] = sqrt(marketModel.totalCovariance(i)[i][i])

                        truePrice = 0.0

                        for i in range(len(vars.accruals)):
                            floatingCouponPV = floatingAccruals[i] * (vars.todaysForwards[i] + floatingSpreads[i]) * \
                                               vars.todaysDiscounts[i + 1]
                            inverseCouponPV = 2 * fixedAccruals[i] * vars.todaysDiscounts[i + 1] * \
                                              blackFormula(
                                                  Option.Put, fixedStrikes[i] / 2.0, vars.todaysForwards[i],
                                                  modelVolatilities[i])

                            truePrice += floatingCouponPV - inverseCouponPV

                        priceError = stats.mean()[0] - truePrice
                        priceSD = stats.errorEstimate()[0]

                        errorInSds = priceError / priceSD
                        self.assertFalse(abs(errorInSds) > 4.0)

                        numericalTolerance = 1E-12

                        self.assertFalse(abs(stats.mean()[0] - stats.mean()[1]) > numericalTolerance)

    def testPeriodAdapter(self):

        TEST_MESSAGE(
            "Testing period-adaptation routines in LIBOR market model...")
        vars = CommonVars()
        vars.setup()
        cs = LMMCurveState(vars.rateTimes)
        cs.setOnForwardRates(vars.todaysForwards)

        period = 2
        offset = 0

        bigRateCS = RestrictCurveState(
            cs, period, offset)

        swaptionPaymentTimes = DoubleVector(bigRateCS.rateTimes())
        swaptionPaymentTimes.pop_back()

        capletPaymentTimes = DoubleVector(swaptionPaymentTimes)

        numberBigRates = bigRateCS.numberOfRates()

        optionletPayoffs = StrikedTypePayoffVector(numberBigRates)
        swaptionPayoffs = StrikedTypePayoffVector(numberBigRates)
        displacedOptionletPayoffs = StrikedTypePayoffVector(numberBigRates)
        displacedSwaptionPayoffs = StrikedTypePayoffVector(numberBigRates)

        for i in range(numberBigRates):
            optionletPayoffs[i] = PlainVanillaPayoff(Option.Call, bigRateCS.forwardRate(i))
            swaptionPayoffs[i] = PlainVanillaPayoff(Option.Call, bigRateCS.coterminalSwapRate(i))
            displacedOptionletPayoffs[i] = PlainVanillaPayoff(Option.Call, bigRateCS.forwardRate(i) + vars.displacement)
            displacedSwaptionPayoffs[i] = PlainVanillaPayoff(
                Option.Call, bigRateCS.coterminalSwapRate(i) + vars.displacement)

        theProduct = MultiStepPeriodCapletSwaptions(
            vars.rateTimes,
            capletPaymentTimes,
            swaptionPaymentTimes,
            optionletPayoffs,
            swaptionPayoffs,
            period,
            offset)

        evolution = theProduct.evolution()

        logNormal = true
        factors = 5

        originalModel = vars.makeMarketModel(
            logNormal,
            evolution,
            factors,
            MarketModelType.ExponentialCorrelationAbcdVolatility)

        newDisplacements = DoubleVector()

        adaptedforwardModel = FwdPeriodAdapter(
            originalModel,
            period,
            offset,
            newDisplacements)

        adaptedSwapModel = FwdToCotSwapAdapter(adaptedforwardModel)

        finalForwardCovariances = adaptedforwardModel.totalCovariance(adaptedforwardModel.numberOfSteps() - 1)
        finalSwapCovariances = adaptedSwapModel.totalCovariance(adaptedSwapModel.numberOfSteps() - 1)

        adaptedForwardSds = DoubleVector(adaptedforwardModel.numberOfRates())
        adaptedSwapSds = DoubleVector(adaptedSwapModel.numberOfRates())
        approxCapletPrices = DoubleVector(adaptedforwardModel.numberOfRates())
        approxSwaptionPrices = DoubleVector(adaptedSwapModel.numberOfRates())

        for j in range(adaptedSwapModel.numberOfRates()):
            adaptedForwardSds[j] = sqrt(finalForwardCovariances[j][j])
            adaptedSwapSds[j] = sqrt(finalSwapCovariances[j][j])

            capletAnnuity = vars.todaysDiscounts[0] * bigRateCS.discountRatio(j + 1, 0) * bigRateCS.rateTaus()[j]

            approxCapletPrices[j] = BlackCalculator(
                displacedOptionletPayoffs[j],
                bigRateCS.forwardRate(j) + vars.displacement,
                adaptedForwardSds[j],
                capletAnnuity).value()

            swaptionAnnuity = vars.todaysDiscounts[0] * bigRateCS.coterminalSwapAnnuity(0, j)

            approxSwaptionPrices[j] = BlackCalculator(
                displacedSwaptionPayoffs[j],
                bigRateCS.coterminalSwapRate(j) + vars.displacement,
                adaptedSwapSds[j],
                swaptionAnnuity).value()

        generatorFactory = SobolBrownianGeneratorFactory(
            SobolBrownianGenerator.Diagonal, vars.seed_)

        evolver = makeMarketModelEvolver(
            originalModel,
            theProduct.suggestedNumeraires(),
            generatorFactory,
            EvolverType.Pc)

        stats = vars.simulate(evolver, CloneMarketModelMultiProduct(theProduct))

        results = stats.mean()
        errors = stats.errorEstimate()

        capletErrorsInSds = DoubleVector(numberBigRates)
        swaptionErrorsInSds = DoubleVector(numberBigRates)

        self.assertFalse(2 * numberBigRates != len(results))

        for i in range(numberBigRates):
            capletErrorsInSds[i] = (results[i] - approxCapletPrices[i]) / errors[i]
            swaptionErrorsInSds[i] = (results[i + numberBigRates] - approxSwaptionPrices[i]) / \
                                     errors[i + numberBigRates]

        capletTolerance = 4
        swaptionTolerance = 4

        for i in range(numberBigRates):
            self.assertFalse(abs(capletErrorsInSds[i]) > capletTolerance)

        for i in range(numberBigRates):
            self.assertFalse(abs(swaptionErrorsInSds[i]) > swaptionTolerance)

    def testAllMultiStepProducts(self):
        testDescription = "all multi-step products "

        vars = CommonVars()
        vars.setup()

        product = MultiProductComposite()
        subProductExpectedValues = []
        vars.addForwards(product, subProductExpectedValues)
        vars.addOptionLets(product, subProductExpectedValues)
        vars.addCoinitialSwaps(product, subProductExpectedValues)
        vars.addCoterminalSwapsAndSwaptions(product, subProductExpectedValues)
        product.finalize()
        self._testMultiProductComposite(
            product, subProductExpectedValues,
            testDescription, vars)

    def testOneStepForwardsAndOptionlets(self):

        TEST_MESSAGE(
            "Testing exact repricing of "
            "one-step forwards and optionlets "
            "in a lognormal forward rate market model...")

        vars = CommonVars()
        vars.setup()

        forwardStrikes = DoubleVector(len(vars.todaysForwards))
        optionletPayoffs = PayoffVector(len(vars.todaysForwards))
        displacedPayoffs = StrikedTypePayoffVector(len(vars.todaysForwards))
        for i in range(len(vars.todaysForwards)):
            forwardStrikes[i] = vars.todaysForwards[i] + 0.01
            optionletPayoffs[i] = PlainVanillaPayoff(Option.Call, vars.todaysForwards[i])
            displacedPayoffs[i] = PlainVanillaPayoff(Option.Call, vars.todaysForwards[i] + vars.displacement)

        forwards = OneStepForwards(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, forwardStrikes)
        optionlets = OneStepOptionlets(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, optionletPayoffs)

        product = MultiProductComposite()
        product.add(CloneMarketModelMultiProduct(forwards))
        product.add(CloneMarketModelMultiProduct(optionlets))
        product.finalize()

        evolution = product.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility,
            MarketModelType.ExponentialCorrelationAbcdVolatility]
        for j in marketModels:

            testedFactors = [len(vars.todaysForwards)]
            for factors in testedFactors:

                measures = [MeasureType.MoneyMarket, MeasureType.Terminal]
                for measure in measures:
                    numeraires = self.makeMeasure(product, measure, vars)

                    logNormal = true
                    marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                    evolvers = [EvolverType.Pc, EvolverType.Balland, EvolverType.Ipc]

                    stop = 0 if isInTerminalMeasure(evolution, numeraires) else 1
                    for i in range(len(evolvers) - stop):

                        for n in range(1):
                            generatorFactory = MTBrownianGeneratorFactory(vars.seed_)
                            evolver = makeMarketModelEvolver(
                                marketModel, numeraires, generatorFactory,
                                evolvers[i])

                            stats = vars.simulate(evolver, CloneMarketModelMultiProduct(product))
                            self.checkForwardsAndOptionlets(stats, forwardStrikes, displacedPayoffs, vars)

    def testOneStepNormalForwardsAndOptionlets(self):

        TEST_MESSAGE(
            "Testing exact repricing of "
            "one-step forwards and optionlets "
            "in a normal forward rate market model...")

        vars = CommonVars()
        vars.setup()

        forwardStrikes = DoubleVector(len(vars.todaysForwards))
        optionletPayoffs = PayoffVector(len(vars.todaysForwards))
        displacedPayoffs = PlainVanillaPayoffVector(len(vars.todaysForwards))
        for i in range(len(vars.todaysForwards)):
            forwardStrikes[i] = vars.todaysForwards[i] + 0.01
            optionletPayoffs[i] = PlainVanillaPayoff(Option.Call, vars.todaysForwards[i])
            displacedPayoffs[i] = PlainVanillaPayoff(Option.Call, vars.todaysForwards[i] + vars.displacement)

        forwards = OneStepForwards(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, forwardStrikes)
        optionlets = OneStepOptionlets(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, optionletPayoffs)

        product = MultiProductComposite()
        product.add(CloneMarketModelMultiProduct(forwards))
        product.add(CloneMarketModelMultiProduct(optionlets))
        product.finalize()

        evolution = product.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility,
            MarketModelType.ExponentialCorrelationAbcdVolatility]
        for j in marketModels:

            testedFactors = [len(vars.todaysForwards)]
            for factors in testedFactors:

                measures = [MeasureType.MoneyMarket, MeasureType.Terminal]
                for measure in measures:
                    numeraires = self.makeMeasure(product, measure, vars)

                    logNormal = false
                    marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                    evolvers = [EvolverType.NormalPc]

                    stop = 0 if isInTerminalMeasure(evolution, numeraires) else 1
                    for i in range(len(evolvers) - stop):

                        for n in range(1):
                            generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                            evolver = makeMarketModelEvolver(
                                marketModel, numeraires, generatorFactory,
                                evolvers[i])

                            stats = vars.simulate(evolver, CloneMarketModelMultiProduct(product))
                            self.checkNormalForwardsAndOptionlets(
                                stats, forwardStrikes, displacedPayoffs, vars)

    def testCallableSwapNaif(self):

        TEST_MESSAGE(
            "Pricing callable swap with naif exercise strategy in a LIBOR market model...")

        vars = CommonVars()
        vars.setup()

        fixedRate = 0.04

        payerSwap = MultiStepSwap(
            vars.rateTimes, vars.accruals, vars.accruals, vars.paymentTimes,
            fixedRate, true)

        receiverSwap = MultiStepSwap(
            vars.rateTimes, vars.accruals, vars.accruals, vars.paymentTimes,
            fixedRate, false)

        exerciseTimes = DoubleVector(vars.rateTimes)
        exerciseTimes.pop_back()

        swapTriggers = DoubleVector(exerciseTimes.size(), fixedRate)
        naifStrategy = SwapRateTrigger(vars.rateTimes, swapTriggers, exerciseTimes)

        collectedData = NodeDataVectorVector()
        basisCoefficients = DoubleVectorVector()
        control = NothingExerciseValue(vars.rateTimes)
        basisSystem = SwapBasisSystem(vars.rateTimes, exerciseTimes)
        nullRebate = NothingExerciseValue(vars.rateTimes)

        dummyProduct = CallSpecifiedMultiProduct(
            CloneMarketModelMultiProduct(receiverSwap),
            CloneCurveStateExerciseStrategy(naifStrategy),
            CloneMarketModelMultiProduct(ExerciseAdapter(
                CloneMarketModelExerciseValue(nullRebate))))

        evolution = dummyProduct.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility,
            MarketModelType.ExponentialCorrelationAbcdVolatility]
        for j in marketModels:

            testedFactors = [4, len(vars.todaysForwards)]
            for factors in testedFactors:

                measures = [MeasureType.MoneyMarketPlus]
                for measure in measures:
                    numeraires = self.makeMeasure(dummyProduct, measure, vars)

                    logNormal = true
                    marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                    evolvers = [EvolverType.Pc, EvolverType.Balland, EvolverType.Ipc]

                    stop = 0 if isInTerminalMeasure(evolution, numeraires) else 1
                    for i in range(len(evolvers) - stop):

                        for n in range(1):

                            generatorFactory = SobolBrownianGeneratorFactory(
                                SobolBrownianGenerator.Diagonal, vars.seed_)

                            evolver = makeMarketModelEvolver(
                                marketModel, numeraires, generatorFactory,
                                evolvers[i])

                            bermudanProduct = CallSpecifiedMultiProduct(
                                CloneMarketModelMultiProduct(MultiStepNothing(evolution)),
                                CloneCurveStateExerciseStrategy(naifStrategy),
                                CloneMarketModelMultiProduct(payerSwap))

                            callableProduct = CallSpecifiedMultiProduct(
                                CloneMarketModelMultiProduct(receiverSwap),
                                CloneCurveStateExerciseStrategy(naifStrategy),
                                CloneMarketModelMultiProduct(
                                    ExerciseAdapter(CloneMarketModelExerciseValue(nullRebate))))

                            allProducts = MultiProductComposite()
                            allProducts.add(CloneMarketModelMultiProduct(payerSwap))
                            allProducts.add(CloneMarketModelMultiProduct(receiverSwap))
                            allProducts.add(CloneMarketModelMultiProduct(bermudanProduct))
                            allProducts.add(CloneMarketModelMultiProduct(callableProduct))
                            allProducts.finalize()

                            stats = vars.simulate(evolver, CloneMarketModelMultiProduct(allProducts))
                            self.checkCallableSwap(stats)

                            uFactory = SobolBrownianGeneratorFactory(
                                SobolBrownianGenerator.Diagonal,
                                vars.seed_ + 142)
                            evolver = makeMarketModelEvolver(marketModel, numeraires, uFactory, evolvers[i])

                            innerEvolvers = MarketModelEvolverVector()

                            isExerciseTime = isInSubset(evolution.evolutionTimes(), naifStrategy.exerciseTimes())
                            for s in range(len(isExerciseTime)):
                                if isExerciseTime[s]:
                                    iFactory = MTBrownianGeneratorFactory(vars.seed_ + s)
                                    e = makeMarketModelEvolver(
                                        marketModel, numeraires, iFactory, evolvers[i], s)
                                    innerEvolvers.append(e)

                            initialNumeraire = evolver.numeraires()[0]
                            initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]

                            uEngine = UpperBoundEngine(
                                evolver, innerEvolvers, receiverSwap, nullRebate,
                                receiverSwap, nullRebate, naifStrategy,
                                initialNumeraireValue)
                            uStats = RiskStatistics()
                            uEngine.multiplePathValues(uStats, 255, 256)
                            delta = uStats.mean()
                            deltaError = uStats.errorEstimate()

    def testCallableSwapLS(self):

        TEST_MESSAGE(
            "Pricing callable swap with Longstaff-Schwartz exercise strategy in a LIBOR market model...")

        vars = CommonVars()
        vars.setup()

        fixedRate = 0.04

        payerSwap = MultiStepSwap(
            vars.rateTimes, vars.accruals, vars.accruals, vars.paymentTimes,
            fixedRate, true)

        receiverSwap = MultiStepSwap(
            vars.rateTimes, vars.accruals, vars.accruals, vars.paymentTimes,
            fixedRate, false)

        exerciseTimes = DoubleVector(vars.rateTimes)
        exerciseTimes.pop_back()

        swapTriggers = DoubleVector(exerciseTimes.size(), fixedRate)
        naifStrategy = SwapRateTrigger(vars.rateTimes, swapTriggers, exerciseTimes)

        collectedData = NodeDataVectorVector()
        basisCoefficients = DoubleVectorVector()
        control = NothingExerciseValue(vars.rateTimes)
        basisSystem = SwapBasisSystem(vars.rateTimes, exerciseTimes)
        nullRebate = NothingExerciseValue(vars.rateTimes)

        dummyProduct = CallSpecifiedMultiProduct(
            CloneMarketModelMultiProduct(receiverSwap),
            CloneCurveStateExerciseStrategy(naifStrategy),
            CloneMarketModelMultiProduct(
                ExerciseAdapter(CloneMarketModelExerciseValue(nullRebate))))

        evolution = dummyProduct.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility,
            MarketModelType.ExponentialCorrelationAbcdVolatility]
        for j in marketModels:

            testedFactors = [4, len(vars.todaysForwards)]
            for factors in testedFactors:

                measures = [MeasureType.MoneyMarket]
                for measure in measures:
                    numeraires = self.makeMeasure(dummyProduct, measure, vars)

                    logNormal = true
                    marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                    evolvers = [EvolverType.Pc, EvolverType.Balland, EvolverType.Ipc]

                    stop = 0 if isInTerminalMeasure(evolution, numeraires) else 1
                    for i in range(len(evolvers) - stop):

                        for n in range(1):

                            generatorFactory = SobolBrownianGeneratorFactory(
                                SobolBrownianGenerator.Diagonal, vars.seed_)

                            evolver = makeMarketModelEvolver(
                                marketModel, numeraires, generatorFactory,
                                evolvers[i])

                            collectNodeData(
                                evolver, receiverSwap, basisSystem, nullRebate, control,
                                vars.trainingPaths_, collectedData)
                            genericLongstaffSchwartzRegression(collectedData, basisCoefficients)
                            exerciseStrategy = LongstaffSchwartzExerciseStrategy(
                                CloneMarketModelBasisSystem(basisSystem),
                                basisCoefficients, evolution,
                                numeraires,
                                CloneMarketModelExerciseValue(nullRebate),
                                CloneMarketModelExerciseValue(control))

                            bermudanProduct = CallSpecifiedMultiProduct(
                                CloneMarketModelMultiProduct(MultiStepNothing(evolution)),
                                CloneCurveStateExerciseStrategy(exerciseStrategy),
                                CloneMarketModelMultiProduct(payerSwap))

                            callableProduct = CallSpecifiedMultiProduct(
                                CloneMarketModelMultiProduct(receiverSwap),
                                CloneCurveStateExerciseStrategy(exerciseStrategy),
                                CloneMarketModelMultiProduct(
                                    ExerciseAdapter(CloneMarketModelExerciseValue(nullRebate))))

                            allProducts = MultiProductComposite()
                            allProducts.add(CloneMarketModelMultiProduct(payerSwap))
                            allProducts.add(CloneMarketModelMultiProduct(receiverSwap))
                            allProducts.add(CloneMarketModelMultiProduct(bermudanProduct))
                            allProducts.add(CloneMarketModelMultiProduct(callableProduct))
                            allProducts.finalize()

                            stats = vars.simulate(evolver, CloneMarketModelMultiProduct(allProducts))
                            self.checkCallableSwap(stats)

                            uFactory = SobolBrownianGeneratorFactory(SobolBrownianGenerator.Diagonal,
                                                                     vars.seed_ + 142)
                            evolver = makeMarketModelEvolver(marketModel, numeraires, uFactory, evolvers[i])
                            innerEvolvers = MarketModelEvolverVector()
                            isExerciseTime = isInSubset(
                                evolution.evolutionTimes(), exerciseStrategy.exerciseTimes())
                            for s in range(len(isExerciseTime)):
                                if isExerciseTime[s]:
                                    iFactory = MTBrownianGeneratorFactory(vars.seed_ + s)
                                    e = makeMarketModelEvolver(
                                        marketModel, numeraires, iFactory, evolvers[i], s)
                                    innerEvolvers.append(e)

                            initialNumeraire = evolver.numeraires()[0]
                            initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]

                            uEngine = UpperBoundEngine(
                                evolver, innerEvolvers, receiverSwap, nullRebate,
                                receiverSwap, nullRebate, exerciseStrategy,
                                initialNumeraireValue)
                            uStats = RiskStatistics()
                            uEngine.multiplePathValues(uStats, 255, 256)
                            delta = uStats.mean()
                            deltaError = uStats.errorEstimate()

    def testGreeks(self):

        TEST_MESSAGE(
            "Testing caplet greeks in a lognormal forward rate market model using partial proxy simulation...")

        vars = CommonVars()
        vars.setup()

        payoffs = PayoffVector(len(vars.todaysForwards))
        displacedPayoffs = StrikedTypePayoffVector(len(vars.todaysForwards))
        for i in range(len(vars.todaysForwards)):
            payoffs[i] = CashOrNothingPayoff(Option.Call, vars.todaysForwards[i], 0.01)

            displacedPayoffs[i] = CashOrNothingPayoff(Option.Call, vars.todaysForwards[i] + vars.displacement, 0.01)

        product = MultiStepOptionlets(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, payoffs)

        evolution = product.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationAbcdVolatility]
        for j in marketModels:

            testedFactors = [4, 8, len(vars.todaysForwards)]
            for factors in testedFactors:
                measures = [MeasureType.MoneyMarket]
                for measure in measures:
                    numeraires = self.makeMeasure(product, measure, vars)

                    for n in range(1):

                        generatorFactory = SobolBrownianGeneratorFactory(
                            SobolBrownianGenerator.Diagonal,
                            vars.seed_)

                        logNormal = true
                        marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                        evolver = LogNormalFwdRateEuler(marketModel, generatorFactory, numeraires)
                        stats = SequenceStatisticsInc(product.numberOfProducts())

                        startIndexOfConstraint = SizeVector()
                        endIndexOfConstraint = SizeVector()

                        for i in range(len(evolution.evolutionTimes())):
                            startIndexOfConstraint.append(i)
                            endIndexOfConstraint.append(i + 1)

                        constrainedEvolvers = ConstrainedEvolverVectorVector()
                        diffWeights = DoubleVectorVectorVector()
                        greekStats = SequenceStatisticsIncVectorVector()

                        deltaGammaEvolvers = ConstrainedEvolverVector()
                        deltaGammaWeights = DoubleVectorVector(2, DoubleVector(3))
                        deltaGammaStats = SequenceStatisticsIncVector(2)
                        deltaGammaStats[0] = SequenceStatisticsInc(product.numberOfProducts())
                        deltaGammaStats[1] = SequenceStatisticsInc(product.numberOfProducts())

                        forwardBump = 1.0e-6
                        marketModel = vars.makeMarketModel(logNormal, evolution, factors, j, -forwardBump)
                        deltaGammaEvolvers.append(
                            LogNormalFwdRateEulerConstrained(
                                marketModel, generatorFactory, numeraires))
                        deltaGammaEvolvers[-1].setConstraintType(
                            startIndexOfConstraint,
                            endIndexOfConstraint)
                        marketModel = vars.makeMarketModel(logNormal, evolution, factors, j, forwardBump)
                        deltaGammaEvolvers.append(
                            LogNormalFwdRateEulerConstrained(
                                marketModel, generatorFactory, numeraires))
                        deltaGammaEvolvers[-1].setConstraintType(
                            startIndexOfConstraint,
                            endIndexOfConstraint)

                        deltaGammaWeights[0] = [0.0, -1.0 / (2.0 * forwardBump), 1.0 / (2.0 * forwardBump)]

                        deltaGammaWeights[1] = [-2.0 / (forwardBump * forwardBump), 1.0 / (forwardBump * forwardBump),
                                                1.0 / (forwardBump * forwardBump)]

                        vegaEvolvers = ConstrainedEvolverVector()
                        vegaWeights = DoubleVectorVector(1, DoubleVector(3))
                        vegaStats = SequenceStatisticsIncVector(1)
                        vegaStats[0] = SequenceStatisticsInc(product.numberOfProducts())

                        volBump = 1.0e-4
                        marketModel = vars.makeMarketModel(logNormal, evolution, factors, j, 0.0, -volBump)
                        vegaEvolvers.append(
                            LogNormalFwdRateEulerConstrained(
                                marketModel, generatorFactory, numeraires))
                        vegaEvolvers[-1].setConstraintType(startIndexOfConstraint,
                                                           endIndexOfConstraint)
                        marketModel = vars.makeMarketModel(logNormal, evolution, factors, j, 0.0, volBump)
                        vegaEvolvers.append(
                            LogNormalFwdRateEulerConstrained(
                                marketModel, generatorFactory, numeraires))
                        vegaEvolvers[-1].setConstraintType(
                            startIndexOfConstraint,
                            endIndexOfConstraint)

                        vegaWeights[0] = [0.0, -1.0 / (2.0 * volBump), 1.0 / (2.0 * volBump)]

                        constrainedEvolvers.append(deltaGammaEvolvers)
                        diffWeights.append(deltaGammaWeights)
                        greekStats.append(deltaGammaStats)

                        constrainedEvolvers.append(vegaEvolvers)
                        diffWeights.append(vegaWeights)
                        greekStats.append(vegaStats)

                        initialNumeraire = evolver.numeraires()[0]
                        initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]

                        engine = ProxyGreekEngine(
                            evolver, constrainedEvolvers, diffWeights,
                            startIndexOfConstraint, endIndexOfConstraint,
                            CloneMarketModelMultiProduct(product),
                            initialNumeraireValue)

                        engine.multiplePathValues(stats, greekStats, vars.paths_)

                        values = stats.mean()
                        errors = stats.errorEstimate()
                        deltas = greekStats[0][0].mean()
                        deltaErrors = greekStats[0][0].errorEstimate()
                        gammas = greekStats[0][1].mean()
                        gammaErrors = greekStats[0][1].errorEstimate()
                        vegas = greekStats[1][0].mean()
                        vegaErrors = greekStats[1][0].errorEstimate()

                        discPlus = DoubleVector(len(vars.todaysForwards) + 1,
                                                vars.todaysDiscounts[0])
                        discMinus = DoubleVector(len(vars.todaysForwards) + 1,
                                                 vars.todaysDiscounts[0])
                        fwdPlus = DoubleVector(len(vars.todaysForwards))
                        fwdMinus = DoubleVector(len(vars.todaysForwards))
                        pricePlus = DoubleVector(len(vars.todaysForwards))
                        price0 = DoubleVector(len(vars.todaysForwards))
                        priceMinus = DoubleVector(len(vars.todaysForwards))
                        for i in range(len(vars.todaysForwards)):
                            tau = vars.rateTimes[i + 1] - vars.rateTimes[i]
                            fwdPlus[i] = vars.todaysForwards[i] + forwardBump
                            fwdMinus[i] = vars.todaysForwards[i] - forwardBump
                            discPlus[i + 1] = discPlus[i] / (1.0 + fwdPlus[i] * tau)
                            discMinus[i + 1] = discMinus[i] / (1.0 + fwdMinus[i] * tau)
                            pricePlus[i] = BlackCalculator(
                                displacedPayoffs[i], fwdPlus[i],
                                vars.volatilities[i] * sqrt(vars.rateTimes[i]),
                                discPlus[i + 1] * tau).value()
                            price0[i] = BlackCalculator(
                                displacedPayoffs[i], vars.todaysForwards[i],
                                vars.volatilities[i] * sqrt(vars.rateTimes[i]),
                                vars.todaysDiscounts[i + 1] * tau).value()
                            priceMinus[i] = BlackCalculator(
                                displacedPayoffs[i], fwdMinus[i],
                                vars.volatilities[i] * sqrt(vars.rateTimes[i]),
                                discMinus[i + 1] * tau).value()

                        for i in range(product.numberOfProducts()):
                            numDelta = (pricePlus[i] - priceMinus[i]) / (2.0 * forwardBump)
                            numGamma = (pricePlus[i] - 2 * price0[i] + priceMinus[i]) / (forwardBump * forwardBump)

    def testPathwiseGreeks(self):

        TEST_MESSAGE(
            "Testing caplet deltas in a lognormal forward rate market model using pathwise method...")
        vars = CommonVars()
        vars.setup()

        payoffs = PayoffVector(len(vars.todaysForwards))
        displacedPayoffs = StrikedTypePayoffVector(len(vars.todaysForwards))
        for i in range(len(vars.todaysForwards)):
            payoffs[i] = PlainVanillaPayoff(Option.Call, vars.todaysForwards[i])

            displacedPayoffs[i] = PlainVanillaPayoff(Option.Call, vars.todaysForwards[i] + vars.displacement)

        for whichProduct in range(2):

            product1 = MarketModelPathwiseMultiDeflatedCaplet(
                vars.rateTimes, vars.accruals,
                vars.paymentTimes, vars.todaysForwards)

            product2 = MarketModelPathwiseMultiCaplet(
                vars.rateTimes, vars.accruals,
                vars.paymentTimes, vars.todaysForwards)

            if whichProduct == 0:
                product = product2
            else:
                product = product1

            productDummy = MultiStepOptionlets(
                vars.rateTimes, vars.accruals,
                vars.paymentTimes, payoffs)

            evolution = product.evolution()

            marketModels = [
                MarketModelType.ExponentialCorrelationAbcdVolatility]

            for j in marketModels:

                testedFactors = [2]

                for factors in testedFactors:
                    measures = [MeasureType.MoneyMarket]

                    for measure in measures:
                        numeraires = self.makeMeasure(productDummy, measure, vars)

                        for n in range(1):
                            generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                            logNormal = true
                            marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                            evolver = LogNormalFwdRateEuler(marketModel, generatorFactory, numeraires)
                            stats = SequenceStatisticsInc(
                                product.numberOfProducts() *
                                (len(vars.todaysForwards) + 1))

                            forwardBump = 1.0e-6

                            initialNumeraire = evolver.numeraires()[0]
                            initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]

                            accountingengine = PathwiseAccountingEngine(
                                evolver,
                                CloneMarketModelPathwiseMultiProduct(product),
                                marketModel,
                                initialNumeraireValue)

                            accountingengine.multiplePathValues(stats, vars.paths_)

                            valuesAndDeltas = stats.mean()
                            errors = stats.errorEstimate()

                            prices = DoubleVector(product.numberOfProducts())
                            priceErrors = DoubleVector(product.numberOfProducts())

                            deltas = Matrix(product.numberOfProducts(), len(vars.todaysForwards))
                            deltasErrors = Matrix(product.numberOfProducts(), len(vars.todaysForwards))
                            modelPrices = DoubleVector(product.numberOfProducts())

                            for i in range(product.numberOfProducts()):
                                prices[i] = valuesAndDeltas[i]

                                priceErrors[i] = errors[i]

                                modelPrices[i] = BlackCalculator(
                                    displacedPayoffs[i], vars.todaysForwards[i],
                                    vars.volatilities[i] * sqrt(vars.rateTimes[i]),
                                    vars.todaysDiscounts[i + 1] *
                                    (vars.rateTimes[i + 1] - vars.rateTimes[i])).value()

                                for j in range(len(vars.todaysForwards)):
                                    deltas[i][j] = valuesAndDeltas[(i + 1) * product.numberOfProducts() + j]
                                    deltasErrors[i][j] = errors[(i + 1) * product.numberOfProducts() + j]

                            modelDeltas = Matrix(product.numberOfProducts(), len(vars.todaysForwards))

                            discPlus = DoubleVector(
                                len(vars.todaysForwards) + 1,
                                vars.todaysDiscounts[0])
                            discMinus = DoubleVector(
                                len(vars.todaysForwards) + 1,
                                vars.todaysDiscounts[0])
                            fwdPlus = DoubleVector(len(vars.todaysForwards))
                            fwdMinus = DoubleVector(len(vars.todaysForwards))

                            for i in range(len(vars.todaysForwards)):
                                for j in range(len(vars.todaysForwards)):
                                    if i != j:
                                        fwdPlus[j] = vars.todaysForwards[j]
                                        fwdMinus[j] = vars.todaysForwards[j]
                                    else:
                                        fwdPlus[j] = vars.todaysForwards[j] + forwardBump
                                        fwdMinus[j] = vars.todaysForwards[j] - forwardBump

                                    tau = vars.rateTimes[j + 1] - vars.rateTimes[j]
                                    discPlus[j + 1] = discPlus[j] / (1.0 + fwdPlus[j] * tau)
                                    discMinus[j + 1] = discMinus[j] / (1.0 + fwdMinus[j] * tau)

                                for k in range(product.numberOfProducts()):
                                    tau = vars.rateTimes[k + 1] - vars.rateTimes[k]
                                    priceUp = BlackCalculator(
                                        displacedPayoffs[k], fwdPlus[k],
                                        vars.volatilities[k] * sqrt(vars.rateTimes[k]),
                                        discPlus[k + 1] * tau).value()
                                    priceDown = BlackCalculator(
                                        displacedPayoffs[k], fwdMinus[k],
                                        vars.volatilities[k] * sqrt(vars.rateTimes[k]),
                                        discMinus[k + 1] * tau).value()

                                    modelDeltas[k][i] = (priceUp - priceDown) / (2 * forwardBump)

                            numberErrors = 0

                            for i in range(product.numberOfProducts()):

                                thisPrice = prices[i]
                                thisModelPrice = modelPrices[i]
                                priceErrorInSds = ((thisPrice - thisModelPrice) / priceErrors[i])

                                errorTheshold = 3.5

                                self.assertFalse(abs(priceErrorInSds) > errorTheshold)

                                threshold = 1e-10

                                for j in range(len(vars.todaysForwards)):
                                    delta = deltas[i][j]
                                    modelDelta = modelDeltas[i][j]

                                    deltaErrorInSds = 100

                                    if deltasErrors[i][j] > 0.0:
                                        deltaErrorInSds = ((delta - modelDelta) / deltasErrors[i][j])
                                    elif abs(modelDelta - delta) < threshold:
                                        deltaErrorInSds = 0.0

                                    self.assertFalse(abs(deltaErrorInSds) > errorTheshold)

    @unittest.skip("testPathwiseVegas: crash")
    def testPathwiseVegas(self):

        TEST_MESSAGE(
            "Testing pathwise vegas in a lognormal forward rate market model...")
        vars = CommonVars()
        vars.setup()

        payoffs = PayoffVector(len(vars.todaysForwards))
        displacedPayoffs = StrikedTypePayoffVector(len(vars.todaysForwards))
        for i in range(len(vars.todaysForwards)):
            payoffs[i] = PlainVanillaPayoff(
                Option.Call, vars.todaysForwards[i])

            displacedPayoffs[i] = PlainVanillaPayoff(
                Option.Call, vars.todaysForwards[i] + vars.displacement)

        product = MultiStepOptionlets(
            vars.rateTimes, vars.accruals, vars.paymentTimes, payoffs)

        caplets = MarketModelPathwiseMultiCaplet(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, vars.todaysForwards)

        capletsDeflated = MarketModelPathwiseMultiDeflatedCaplet(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, vars.todaysForwards)

        cs = LMMCurveState(vars.rateTimes)
        cs.setOnForwardRates(vars.todaysForwards)

        evolution = product.evolution()
        steps = evolution.numberOfSteps()
        numberRates = evolution.numberOfRates()

        bumpSizeNumericalDifferentiation = 1E-6
        vegaBumpSize = 1e-2
        pathsToDo = 10
        pathsToDoSimulation = vars.paths_
        bumpIncrement = int(1 + evolution.numberOfSteps() / 3)
        numericalBumpSizeForSwaptionPseudo = 1E-7

        multiplier = 50

        maxError = 0.0
        numberSwaptionPseudoFailures = 0
        numberCapPseudoFailures = 0
        numberCapImpVolFailures = 0
        numberCapVolPseudoFailures = 0
        swaptionPseudoTolerance = 1e-8
        impVolTolerance = 1e-5
        capStrike = vars.meanForward
        initialNumeraireValue = 0.95

        marketModels = [
            MarketModelType.ExponentialCorrelationAbcdVolatility]

        for mmi in marketModels:

            testedFactors = [min(3, len(vars.todaysForwards))]

            for factors in testedFactors:
                logNormal = true

                marketModel = vars.makeMarketModel(
                    logNormal, evolution, factors, mmi)

                startIndex = min(1, evolution.numberOfRates() - 2)
                endIndex = evolution.numberOfRates() - 1

                derivative = SwaptionPseudoDerivative(
                    marketModel, startIndex, endIndex)

                pseudoRoots = MatrixVector()
                for k in range(marketModel.numberOfSteps()):
                    pseudoRoots.append(marketModel.pseudoRoot(k))

                for step in range(evolution.numberOfSteps()):
                    for l in range(evolution.numberOfRates()):
                        for f in range(factors):

                            pseudoRoots[step][l][f] += numericalBumpSizeForSwaptionPseudo

                            bumpedUp = PseudoRootFacade(
                                pseudoRoots, vars.rateTimes, marketModel.initialRates(),
                                marketModel.displacements())

                            upImpVol = SwapForwardMappings.swaptionImpliedVolatility(
                                bumpedUp, startIndex, endIndex)

                            pseudoRoots[step][l][f] -= numericalBumpSizeForSwaptionPseudo

                            pseudoRoots[step][l][f] -= numericalBumpSizeForSwaptionPseudo

                            bumpedDown = PseudoRootFacade(
                                pseudoRoots, vars.rateTimes, marketModel.initialRates(),
                                marketModel.displacements())

                            downImpVol = SwapForwardMappings.swaptionImpliedVolatility(
                                bumpedDown, startIndex, endIndex)

                            pseudoRoots[step][l][f] += numericalBumpSizeForSwaptionPseudo

                            volDeriv = (upImpVol - downImpVol) / (2.0 * numericalBumpSizeForSwaptionPseudo)

                            modelVal = derivative.volatilityDerivative(step)[l][f]

                            error = volDeriv - modelVal

                            if abs(error) > swaptionPseudoTolerance:
                                numberSwaptionPseudoFailures += 1

                self.assertFalse(numberSwaptionPseudoFailures > 0)

        for mmi in marketModels:

            testedFactors = [min(3, len(vars.todaysForwards))]

            for factors in testedFactors:
                logNormal = true

                marketModel = vars.makeMarketModel(logNormal, evolution, factors, mmi)

                for startIndex in range(1, evolution.numberOfRates() - 1):
                    for endIndex in range(startIndex + 1, evolution.numberOfRates()):

                        derivative = CapPseudoDerivative(
                            marketModel, capStrike, startIndex,
                            endIndex, initialNumeraireValue)

                        pseudoRoots = MatrixVector()
                        for k in range(marketModel.numberOfSteps()):
                            pseudoRoots.append(marketModel.pseudoRoot(k))

                        for step in range(evolution.numberOfSteps()):
                            for l in range(evolution.numberOfRates()):
                                for f in range(factors):

                                    pseudoRoots[step][l][f] += numericalBumpSizeForSwaptionPseudo

                                    bumpedUp = PseudoRootFacade(
                                        pseudoRoots, vars.rateTimes, marketModel.initialRates(),
                                        marketModel.displacements())

                                    totalCovUp = bumpedUp.totalCovariance(marketModel.numberOfSteps() - 1)

                                    pseudoRoots[step][l][f] -= numericalBumpSizeForSwaptionPseudo

                                    pseudoRoots[step][l][f] -= numericalBumpSizeForSwaptionPseudo

                                    bumpedDown = PseudoRootFacade(
                                        pseudoRoots, vars.rateTimes, marketModel.initialRates(),
                                        marketModel.displacements())

                                    totalCovDown = bumpedDown.totalCovariance(marketModel.numberOfSteps() - 1)

                                    pseudoRoots[step][l][f] += numericalBumpSizeForSwaptionPseudo

                                    priceDeriv = 0.0
                                    for k in range(startIndex, endIndex):
                                        upSd = sqrt(totalCovUp[k][k])
                                        downSd = sqrt(totalCovDown[k][k])

                                        annuity = vars.todaysDiscounts[k + 1] * marketModel.evolution().rateTaus()[k]
                                        forward = vars.todaysForwards[k]

                                        upPrice = blackFormula(
                                            Option.Call,
                                            capStrike,
                                            forward,
                                            upSd,
                                            annuity,
                                            marketModel.displacements()[k])

                                        downPrice = blackFormula(
                                            Option.Call,
                                            capStrike,
                                            forward,
                                            downSd,
                                            annuity,
                                            marketModel.displacements()[k])

                                        priceDeriv += (upPrice - downPrice) / (2.0 * numericalBumpSizeForSwaptionPseudo)

                                    modelVal = derivative.priceDerivative(step)[l][f]

                                    error = priceDeriv - modelVal

                                    if abs(error) > swaptionPseudoTolerance:
                                        numberCapPseudoFailures += 1

                        impVol = derivative.impliedVolatility()

                        totalCov = marketModel.totalCovariance(evolution.numberOfSteps() - 1)
                        priceConstVol = 0.0
                        priceVarVol = 0.0

                        for m in range(startIndex, endIndex):
                            annuity = vars.todaysDiscounts[m + 1] * marketModel.evolution().rateTaus()[m]
                            expiry = vars.rateTimes[m]
                            forward = vars.todaysForwards[m]

                            priceConstVol += blackFormula(
                                Option.Call,
                                capStrike,
                                forward,
                                impVol * sqrt(expiry),
                                annuity,
                                marketModel.displacements()[m])

                            priceVarVol += blackFormula(
                                Option.Call,
                                capStrike,
                                forward,
                                sqrt(totalCov[m][m]),
                                annuity,
                                marketModel.displacements()[m])

                        if abs(priceVarVol - priceConstVol) > impVolTolerance:
                            numberCapImpVolFailures += 1

                self.assertFalse(numberCapPseudoFailures > 0)
                self.assertFalse(numberCapImpVolFailures > 0)

            for factors in testedFactors:
                logNormal = true

                marketModel = vars.makeMarketModel(logNormal, evolution, factors, mmi)

                for startIndex in range(1, evolution.numberOfRates() - 1):
                    for endIndex in range(startIndex + 1, evolution.numberOfRates()):

                        derivative = CapPseudoDerivative(
                            marketModel,
                            capStrike,
                            startIndex,
                            endIndex, initialNumeraireValue)

                        pseudoRoots = MatrixVector()
                        for k in range(marketModel.numberOfSteps()):
                            pseudoRoots.append(marketModel.pseudoRoot(k))

                        for step in range(evolution.numberOfSteps()):
                            for l in range(evolution.numberOfRates()):
                                for f in range(factors):
                                    pseudoRoots[step][l][f] += numericalBumpSizeForSwaptionPseudo

                                    bumpedUp = PseudoRootFacade(
                                        pseudoRoots, vars.rateTimes, marketModel.initialRates(),
                                        marketModel.displacements())

                                    upDerivative = CapPseudoDerivative(
                                        bumpedUp,
                                        capStrike,
                                        startIndex,
                                        endIndex,
                                        initialNumeraireValue)

                                    volUp = upDerivative.impliedVolatility()

                                    pseudoRoots[step][l][f] -= numericalBumpSizeForSwaptionPseudo

                                    pseudoRoots[step][l][f] -= numericalBumpSizeForSwaptionPseudo

                                    bumpedDown = PseudoRootFacade(
                                        pseudoRoots, vars.rateTimes, marketModel.initialRates(),
                                        marketModel.displacements())

                                    downDerivative = CapPseudoDerivative(
                                        bumpedDown,
                                        capStrike,
                                        startIndex,
                                        endIndex, initialNumeraireValue)

                                    volDown = downDerivative.impliedVolatility()

                                    pseudoRoots[step][l][f] += numericalBumpSizeForSwaptionPseudo

                                    volDeriv = (volUp - volDown) / (2.0 * numericalBumpSizeForSwaptionPseudo)

                                    modelVal = derivative.volatilityDerivative(step)[l][f]

                                    error = volDeriv - modelVal

                                    if abs(error) > impVolTolerance * 10:
                                        numberCapVolPseudoFailures += 1

                self.assertFalse(numberCapVolPseudoFailures > 0)

        for mmi in range(len(marketModels)):
            testedFactors = [
                min(1, len(vars.todaysForwards))]

            for factors in testedFactors:
                factorsToTest = min(2, factors)

                measures = [
                    MeasureType.MoneyMarket]

                pseudoBumps = MatrixVector()
                pseudoBumpsDown = MatrixVector()

                for k in range(evolution.numberOfRates()):
                    for f in range(factors):
                        modelBump = Matrix(evolution.numberOfRates(), factors, 0.0)
                        modelBump[k][f] = bumpSizeNumericalDifferentiation
                        pseudoBumps.append(modelBump)
                        modelBump[k][f] = -bumpSizeNumericalDifferentiation
                        pseudoBumpsDown.append(modelBump)

                vegaBumps = MatrixVectorVector()

                modelBump = Matrix(evolution.numberOfRates(), factors, 0.0)

                for l in range(evolution.numberOfSteps()):
                    tmp = MatrixVector()

                    for k in range(evolution.numberOfRates(), bumpIncrement):
                        for f in range(factorsToTest):

                            for m in range(evolution.numberOfSteps()):
                                if l == m and k >= l:
                                    modelBump[k][f] = vegaBumpSize
                                tmp.append(modelBump)
                                modelBump[k][f] = 0.0

                    vegaBumps.append(tmp)

                for measure in measures:

                    numeraires = self.makeMeasure(product, measure, vars)

                    testees = []
                    testees2 = []
                    testers = []
                    testersDown = []

                    generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                    logNormal = true
                    marketModel = vars.makeMarketModel(
                        logNormal, evolution, factors,
                        marketModels[mmi])

                    for l in range(evolution.numberOfSteps()):
                        pseudoRoot = marketModel.pseudoRoot(l)
                        testees.append(RatePseudoRootJacobian(
                            pseudoRoot, evolution.firstAliveRate()[l],
                            numeraires[l],
                            evolution.rateTaus(), pseudoBumps,
                            marketModel.displacements()))

                        testees2.append(
                            RatePseudoRootJacobianAllElements(
                                pseudoRoot, evolution.firstAliveRate()[l], numeraires[l],
                                evolution.rateTaus(), marketModel.displacements()))

                        testers.append(
                            RatePseudoRootJacobianNumerical(
                                pseudoRoot, evolution.firstAliveRate()[l], numeraires[l],
                                evolution.rateTaus(), pseudoBumps, marketModel.displacements()))
                        testersDown.append(
                            RatePseudoRootJacobianNumerical(
                                pseudoRoot, evolution.firstAliveRate()[l], numeraires[l],
                                evolution.rateTaus(), pseudoBumpsDown, marketModel.displacements()))

                    generator = generatorFactory.create(factors, steps)
                    evolver = LogNormalFwdRateEuler(
                        marketModel, generatorFactory, numeraires)

                    oldRates = DoubleVector(evolution.numberOfRates())
                    newRates = DoubleVector(evolution.numberOfRates())
                    gaussians = DoubleVector(factors)

                    numberCashFlowsThisStep = SizeVector(product.numberOfProducts())

                    cashFlowsGenerated = MarketModelMultiProductCashFlowVectorVector(
                        product.numberOfProducts())

                    for i in range(product.numberOfProducts()):
                        tmp = MarketModelMultiProductCashFlowVector(
                            product.maxNumberOfCashFlowsPerProductPerStep())
                        cashFlowsGenerated[i] = tmp

                    B = Matrix(len(pseudoBumps), evolution.numberOfRates())
                    B2 = Matrix(len(pseudoBumps), evolution.numberOfRates())
                    B3 = Matrix(len(pseudoBumps), evolution.numberOfRates())
                    B4 = Matrix(len(pseudoBumps), evolution.numberOfRates())

                    globalB = MatrixVector()

                    modelB = Matrix(evolution.numberOfRates(), factors)
                    for i in range(steps):
                        globalB.append(modelB)

                    oneStepDFs = DoubleVector(evolution.numberOfRates() + 1)
                    oneStepDFs[0] = 1.0

                    numberFailures = 0
                    numberFailures2 = 0

                    for l in range(pathsToDo):

                        evolver.startNewPath()
                        product.reset()
                        generator.nextPath()

                        done = None
                        newRates = marketModel.initialRates()
                        currentStep = 0

                        while True:
                            oldRates = DoubleVector(newRates)

                            evolver.advanceStep()
                            done = product.nextTimeStep(
                                evolver.currentState(),
                                numberCashFlowsThisStep,
                                cashFlowsGenerated)

                            newRates = evolver.currentState().forwardRates()

                            for i in range(1, evolution.numberOfRates() + 1):
                                oneStepDFs[i] = 1.0 / (1 + oldRates[i - 1] * evolution.rateTaus()[i - 1])

                            generator.nextStep(gaussians)

                            testees[currentStep].getBumps(oldRates, oneStepDFs, newRates, gaussians, B)
                            testees2[currentStep].getBumps(oldRates, oneStepDFs, newRates, gaussians, globalB)
                            testers[currentStep].getBumps(oldRates, oneStepDFs, newRates, gaussians, B2)
                            testersDown[currentStep].getBumps(oldRates, oneStepDFs, newRates, gaussians, B3)

                            for i1 in range(len(pseudoBumps)):
                                jj = 0

                                for j1 in range(evolution.firstAliveRate()[i1]):
                                    B4[i1][j1] = 0.0
                                    jj += 1

                                for j1 in range(jj, numberRates):
                                    sum = 0.0

                                    for k1 in range(evolution.firstAliveRate()[i1], numberRates):
                                        for f1 in range(factors):
                                            sum += pseudoBumps[i1][k1][f1] * globalB[j1][k1][f1]

                                    B4[i1][j1] = sum

                            for j in range(B.rows()):
                                for k in range(B.columns()):
                                    analytic = B[j][k] / bumpSizeNumericalDifferentiation
                                    analytic2 = B4[j][k] / bumpSizeNumericalDifferentiation
                                    numerical = (B2[j][k] - B3[j][k]) / (2 * bumpSizeNumericalDifferentiation)
                                    errorSize = (analytic - numerical) / (
                                            bumpSizeNumericalDifferentiation * bumpSizeNumericalDifferentiation)
                                    errorSize2 = (analytic2 - numerical) / (
                                            bumpSizeNumericalDifferentiation * bumpSizeNumericalDifferentiation)

                                    maxError = max(maxError, abs(errorSize))

                                    if abs(errorSize) > multiplier:
                                        numberFailures += 1

                                    if abs(errorSize2) > multiplier:
                                        numberFailures2 += 1

                            currentStep += 1
                            if done == true:
                                break

                    self.assertFalse(numberFailures > 0)
                    self.assertFalse(numberFailures2 > 0)

                numberDeflatedErrors = 0
                numberUndeflatedErrors = 0
                biggestError = 0.0
                print(len(vegaBumps[1]))

                for deflate in range(2):

                    if deflate == 0:
                        productToUse = CloneMarketModelPathwiseMultiProduct(caplets)
                    else:
                        productToUse = CloneMarketModelPathwiseMultiProduct(capletsDeflated)

                    for measure in measures:

                        numeraires = self.makeMeasure(product, measure, vars)

                        generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                        logNormal = true

                        marketModel = vars.makeMarketModel(
                            logNormal, evolution, factors,
                            marketModels[mmi])

                        evolver = LogNormalFwdRateEuler(
                            marketModel,
                            generatorFactory,
                            numeraires)

                        initialNumeraire = evolver.numeraires()[0]
                        initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]

                        values = DoubleVector()
                        errors = DoubleVector()

                        accountingengine = PathwiseVegasAccountingEngine(
                            evolver,
                            productToUse,
                            marketModel,
                            vegaBumps,
                            initialNumeraireValue)

                        accountingengine.multiplePathValues(values, errors, pathsToDoSimulation)

                        vegasMatrix = Matrix(caplets.numberOfProducts(), len(vegaBumps[0]))
                        standardErrors = Matrix(vegasMatrix)
                        deltasMatrix = Matrix(caplets.numberOfProducts(), numberRates)
                        deltasErrors = Matrix(deltasMatrix)
                        prices = DoubleVector(caplets.numberOfProducts())
                        priceErrors = DoubleVector(caplets.numberOfProducts())

                        entriesPerProduct = 1 + numberRates + len(vegaBumps[0])

                        for i in range(caplets.numberOfProducts()):
                            prices[i] = values[i * entriesPerProduct]
                            priceErrors[i] = errors[i * entriesPerProduct]

                            for j0 in range(len(vegaBumps[0])):
                                vegasMatrix[i][j0] = values[i * entriesPerProduct + numberRates + 1 + j0]
                                standardErrors[i][j0] = errors[i * entriesPerProduct + numberRates + 1 + j0]

                            for j1 in range(numberRates):
                                deltasMatrix[i][j1] = values[i * entriesPerProduct + 1 + j1]
                                deltasErrors[i][j1] = errors[i * entriesPerProduct + 1 + j1]

                        totalCovariance = marketModel.totalCovariance(marketModel.numberOfSteps() - 1)

                        truePrices = DoubleVector(caplets.numberOfProducts())

                        for r in range(len(truePrices)):
                            truePrices[r] = BlackCalculator(
                                displacedPayoffs[r], vars.todaysForwards[r],
                                sqrt(totalCovariance[r][r]),
                                vars.todaysDiscounts[r + 1] * (
                                        vars.rateTimes[r + 1] - vars.rateTimes[r])).value()

                        for b in range(len(vegaBumps[0])):

                            bumpedPrices = DoubleVector(len(truePrices))
                            variances = DoubleVector(len(truePrices), 0.0)
                            vegas = DoubleVector(len(truePrices))

                            for step in range(marketModel.numberOfSteps()):
                                pseudoRoot = marketModel.pseudoRoot(step)
                                pseudoRoot += vegaBumps[step][b]

                                for rate in range(step, marketModel.numberOfRates()):
                                    variance = 0.0
                                    for f in range(marketModel.numberOfFactors()):
                                        variance += pseudoRoot[rate][f] * pseudoRoot[rate][f]

                                    variances[rate] += variance

                            for r in range(len(truePrices)):
                                bumpedPrices[r] = BlackCalculator(
                                    displacedPayoffs[r], vars.todaysForwards[r],
                                    sqrt(variances[r]),
                                    vars.todaysDiscounts[r + 1] * (
                                            vars.rateTimes[r + 1] - vars.rateTimes[
                                        r])).value()

                                vegas[r] = bumpedPrices[r] - truePrices[r]

                            for s in range(len(truePrices)):
                                mcVega = vegasMatrix[s][b]
                                analyticVega = vegas[s]
                                thisError = mcVega - analyticVega
                                thisSE = standardErrors[s][b]

                                if abs(thisError) > 0.0:
                                    errorInSEs = thisError / thisSE
                                    biggestError = max(abs(errorInSEs), biggestError)

                                    if abs(errorInSEs) > 4.5:
                                        if deflate == 0:
                                            numberUndeflatedErrors += 1
                                        else:
                                            numberDeflatedErrors += 1

                        productToUse2 = None

                        if deflate == 0:
                            productToUse2 = caplets
                        else:
                            productToUse2 = capletsDeflated

                        stats = SequenceStatisticsInc(productToUse2.numberOfProducts() * (len(vars.todaysForwards) + 1))

                        accountingengine = PathwiseAccountingEngine(
                            evolver,
                            productToUse2,
                            marketModel,
                            initialNumeraireValue)

                        accountingengine.multiplePathValues(stats, pathsToDoSimulation)

                        valuesAndDeltas2 = stats.mean()
                        errors2 = stats.errorEstimate()

                        prices2 = DoubleVector(productToUse2.numberOfProducts())
                        priceErrors2 = DoubleVector(productToUse2.numberOfProducts())

                        deltas2 = Matrix(productToUse2.numberOfProducts(), len(vars.todaysForwards))
                        deltasErrors2 = Matrix(productToUse2.numberOfProducts(), len(vars.todaysForwards))
                        modelPrices2 = DoubleVector(productToUse2.numberOfProducts())

                        for i in range(productToUse2.numberOfProducts()):
                            prices2[i] = valuesAndDeltas2[i]
                            priceErrors2[i] = errors2[i]

                            for j in range(len(vars.todaysForwards)):
                                deltas2[i][j] = valuesAndDeltas2[(i + 1) * productToUse2.numberOfProducts() + j]
                                deltasErrors2[i][j] = errors2[(i + 1) * productToUse2.numberOfProducts() + j]

                        for i in range(productToUse2.numberOfProducts()):

                            priceDiff = prices2[i] - prices[i]

                            self.assertFalse(abs(priceDiff) > 5 * priceErrors2[i])
                            for j in range(len(vars.todaysForwards)):
                                error = deltas2[i][j] - deltasMatrix[i][j]
                                self.assertFalse(abs(error) > 5 * deltasErrors2[i][j])

                self.assertFalse(numberDeflatedErrors + numberUndeflatedErrors > 0)

                caps = VolatilityBumpInstrumentJacobianCapVector()

                capStrike = vars.todaysForwards[0]

                for i in range(0, numberRates - 2, 3):
                    nextCap = VolatilityBumpInstrumentJacobianCap()

                    nextCap.startIndex_ = i + 2
                    nextCap.endIndex_ = i + 3
                    nextCap.strike_ = capStrike
                    caps.append(nextCap)

                startsAndEnds = SizeSizePairVector(len(caps))

                for r in range(len(caps)):
                    startsAndEnds[r].first = caps[r].startIndex_
                    startsAndEnds[r].second = caps[r].endIndex_

                capsDeflated = MarketModelPathwiseMultiDeflatedCap(
                    vars.rateTimes,
                    vars.accruals,
                    vars.paymentTimes,
                    capStrike,
                    startsAndEnds)

                for measure in measures:

                    numeraires = self.makeMeasure(product, measure, vars)

                    generatorFactory = MTBrownianGeneratorFactory(vars.seed_)
                    generatorFactory2 = MTBrownianGeneratorFactory(vars.seed_)

                    logNormal = true
                    marketModel = vars.makeMarketModel(
                        logNormal, evolution, factors,
                        marketModels[mmi])

                    evolver = LogNormalFwdRateEuler(
                        marketModel,
                        generatorFactory,
                        numeraires)

                    evolver2 = LogNormalFwdRateEuler(
                        marketModel,
                        generatorFactory2,
                        numeraires)

                    initialNumeraire = evolver.numeraires()[0]
                    initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]

                    values = DoubleVector()
                    errors = DoubleVector()

                    values2 = DoubleVector()
                    errors2 = DoubleVector()

                    accountingengine = PathwiseVegasOuterAccountingEngine(
                        evolver2,
                        capsDeflated,
                        marketModel,
                        vegaBumps,
                        initialNumeraireValue)

                    accountingengine.multiplePathValues(values2, errors2, pathsToDoSimulation)

                    accountingengine = PathwiseVegasAccountingEngine(
                        evolver,
                        capsDeflated,
                        marketModel,
                        vegaBumps,
                        initialNumeraireValue)

                    accountingengine.multiplePathValues(values, errors, pathsToDoSimulation)

                    tol = 1E-8

                    numberMeanFailures = 0

                    for i in range(values.size()):
                        if abs(values[i] - values2[i]) > tol:
                            numberMeanFailures += 1

                    self.assertFalse(numberMeanFailures > 0)

                    vegasMatrix = Matrix(capsDeflated.numberOfProducts(), len(vegaBumps[0]))
                    standardErrors = vegasMatrix
                    entriesPerProduct = 1 + numberRates + len(vegaBumps[0])

                    for i in range(capsDeflated.numberOfProducts()):
                        for j in range(len(vegaBumps[0])):
                            vegasMatrix[i][j] = values[i * entriesPerProduct + numberRates + 1 + j]
                            standardErrors[i][j] = errors[i * entriesPerProduct + numberRates + 1 + j]

                    totalCovariance = marketModel.totalCovariance(marketModel.numberOfSteps() - 1)

                    trueCapletPrices = DoubleVector(numberRates)
                    dispayoff = PlainVanillaPayoff(Option.Call, capStrike + vars.displacement)

                    for r in range(len(trueCapletPrices)):
                        trueCapletPrices[r] = BlackCalculator(
                            dispayoff, vars.todaysForwards[r],
                            sqrt(totalCovariance[r][r]),
                            vars.todaysDiscounts[r + 1] * (
                                    vars.rateTimes[r + 1] - vars.rateTimes[
                                r])).value()

                    trueCapPrices = DoubleVector(capsDeflated.numberOfProducts())
                    vegaCaps = DoubleVector(capsDeflated.numberOfProducts())

                    for s in range(capsDeflated.numberOfProducts()):
                        trueCapPrices[s] = 0.0

                        for t in range(caps[s].startIndex_, caps[s].endIndex_):
                            trueCapPrices[s] += trueCapletPrices[t]

                    numberErrors = 0

                    for b in range(len(vegaBumps[0])):

                        bumpedCapletPrices = DoubleVector(len(trueCapletPrices))

                        variances = DoubleVector(len(trueCapletPrices), 0.0)
                        vegasCaplets = DoubleVector(len(trueCapletPrices))

                        for step in range(marketModel.numberOfSteps()):
                            pseudoRoot = marketModel.pseudoRoot(step)
                            pseudoRoot += vegaBumps[step][b]

                            for rate in range(step, marketModel.numberOfRates()):
                                variance = 0.0
                                for f in range(marketModel.numberOfFactors()):
                                    variance += pseudoRoot[rate][f] * pseudoRoot[rate][f]

                                variances[rate] += variance

                        for r in range(len(trueCapletPrices)):
                            bumpedCapletPrices[r] = BlackCalculator(
                                dispayoff, vars.todaysForwards[r],
                                sqrt(variances[r]),
                                vars.todaysDiscounts[r + 1] * (
                                        vars.rateTimes[r + 1] - vars.rateTimes[r])).value()

                            vegasCaplets[r] = bumpedCapletPrices[r] - trueCapletPrices[r]

                        for s in range(capsDeflated.numberOfProducts()):
                            vegaCaps[s] = 0.0

                            for t in range(caps[s].startIndex_, caps[s].endIndex_):
                                vegaCaps[s] += vegasCaplets[t]

                        for s in range(capsDeflated.numberOfProducts()):
                            mcVega = vegasMatrix[s][b]
                            analyticVega = vegaCaps[s]
                            thisError = mcVega - analyticVega
                            thisSE = standardErrors[s][b]

                            if abs(thisError) > 0.0:
                                errorInSEs = abs(thisError / thisSE)

                                if errorInSEs > 4.0:
                                    numberErrors += 1

                    self.assertFalse(numberErrors > 0)

    @unittest.skip("testPathwiseMarketVegas")
    def testPathwiseMarketVegas(self):

        TEST_MESSAGE(
            "Testing pathwise market vegas in a lognormal forward rate market model...")

        vars = CommonVars()
        vars.setup()

        cs = LMMCurveState(vars.rateTimes)
        cs.setOnForwardRates(vars.todaysForwards)

        payoffs = PayoffVector(len(vars.todaysForwards))
        displacedPayoffs = StrikedTypePayoffVector(len(vars.todaysForwards))
        for i in range(len(vars.todaysForwards)):
            payoffs[i] = PlainVanillaPayoff(Option.Call, cs.coterminalSwapRate(i))
            displacedPayoffs[i] = PlainVanillaPayoff(
                Option.Call, cs.coterminalSwapRate(i) + vars.displacement)

        dummyProduct = MultiStepOptionlets(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, payoffs)

        bumpSizeNumericalDifferentiation = 1E-6

        swaptionsDeflated = MarketModelPathwiseCoterminalSwaptionsDeflated(
            vars.rateTimes, cs.coterminalSwapRates())
        swaptionsDeflated2 = MarketModelPathwiseCoterminalSwaptionsNumericalDeflated(
            vars.rateTimes, cs.coterminalSwapRates(), bumpSizeNumericalDifferentiation)

        evolution = dummyProduct.evolution()
        steps = evolution.numberOfSteps()
        numberRates = evolution.numberOfRates()

        pathsToDo = 10
        pathsToDoSimulation = vars.paths_

        multiplier = 50
        tolerance = 1E-6

        initialNumeraireValue = 0.95

        allowFactorwiseBumping = true
        caps = VolatilityBumpInstrumentJacobianCapVector()

        capStrike = vars.todaysForwards[0]

        for i in range(0, numberRates - 2, 3):
            nextCap = VolatilityBumpInstrumentJacobianCap()
            nextCap.startIndex_ = i
            nextCap.endIndex_ = i + 3
            nextCap.strike_ = capStrike
            caps.append(nextCap)

        startsAndEnds = SizeSizePairVector(len(caps))

        for j in range(len(caps)):
            tmp = SizeSizePair(caps[j].startIndex_, caps[j].endIndex_)
            startsAndEnds[j] = tmp

        capsDeflated = MarketModelPathwiseMultiDeflatedCap(
            vars.rateTimes,
            vars.accruals,
            vars.paymentTimes,
            capStrike,
            startsAndEnds)

        swaptions = VolatilityBumpInstrumentJacobianSwaptionVector(numberRates)

        for i in range(numberRates):
            swaptions[i].startIndex_ = i
            swaptions[i].endIndex_ = numberRates

        marketModels = [
            MarketModelType.ExponentialCorrelationAbcdVolatility]

        for j in marketModels:

            testedFactors = [min(1, len(vars.todaysForwards))]

            for factors in testedFactors:
                logNormal = true

                marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                possibleBumps = VegaBumpCollection(marketModel, allowFactorwiseBumping)

                bumpFinder = OrthogonalizedBumpFinder(
                    possibleBumps,
                    swaptions,
                    caps,
                    multiplier,
                    tolerance)

                theBumps = MatrixVectorVector()

                bumpFinder.GetVegaBumps(theBumps)

                swaptionVegasMatrix = Matrix(swaptionsDeflated.numberOfProducts(), len(theBumps[0]))

                for i in range(swaptionsDeflated.numberOfProducts()):
                    thisPseudoDerivative = SwaptionPseudoDerivative(
                        marketModel,
                        swaptions[i].startIndex_,
                        swaptions[i].endIndex_)

                    for j in range(len(theBumps[0])):
                        swaptionVegasMatrix[i][j] = 0

                        for k in range(steps):
                            for l in range(numberRates):
                                for m in range(factors):
                                    swaptionVegasMatrix[i][j] += theBumps[k][j][l][m] * \
                                                                 thisPseudoDerivative.volatilityDerivative(k)[l][m]

                numberDiagonalFailures = 0
                offDiagonalFailures = 0

                for i in range(len(swaptions)):
                    for j in range(len(theBumps[0])):
                        if i == j:
                            thisError = swaptionVegasMatrix[i][i] - 0.01

                            if abs(thisError) > 1e-8:
                                numberDiagonalFailures += 1

                        else:
                            thisError = swaptionVegasMatrix[i][j]
                            if abs(thisError) > 1e-8:
                                offDiagonalFailures += 1

                self.assertFalse(numberDiagonalFailures + offDiagonalFailures > 0)

                capsVegasMatrix = Matrix(len(caps), len(theBumps[0]))

                for i in range(len(caps)):
                    thisPseudoDerivative = CapPseudoDerivative(
                        marketModel,
                        caps[i].strike_,
                        caps[i].startIndex_,
                        caps[i].endIndex_, initialNumeraireValue)

                    for j in range(len(theBumps[0])):
                        capsVegasMatrix[i][j] = 0

                        for k in range(steps):
                            for l in range(numberRates):
                                for m in range(factors):
                                    capsVegasMatrix[i][j] += theBumps[k][j][l][m] * \
                                                             thisPseudoDerivative.volatilityDerivative(k)[l][m]

                numberDiagonalFailures = 0
                offDiagonalFailures = 0

                for i in range(len(caps)):
                    for j in range(len(theBumps[0])):
                        if i + len(swaptions) == j:
                            thisError = capsVegasMatrix[i][j] - 0.01

                            if abs(thisError) > 1e-8:
                                numberDiagonalFailures += 1

                        else:
                            thisError = capsVegasMatrix[i][j]
                            if abs(thisError) > 1e-8:
                                offDiagonalFailures += 1

                self.assertFalse(numberDiagonalFailures + offDiagonalFailures > 0)

        numberCashFlowsThisStep1 = SizeVector(swaptionsDeflated.numberOfProducts())

        cashFlowsGenerated1 = MarketModelPathwiseMultiProductCashFlowVectorVector(
            swaptionsDeflated.numberOfProducts())

        for i in range(swaptionsDeflated.numberOfProducts()):
            tmp = MarketModelPathwiseMultiProductCashFlowVector(
                swaptionsDeflated.maxNumberOfCashFlowsPerProductPerStep())

            for j in range(swaptionsDeflated.maxNumberOfCashFlowsPerProductPerStep()):
                tmp[j].amount(DoubleVector(numberRates + 1))

            cashFlowsGenerated1[i] = tmp

        numberCashFlowsThisStep2 = SizeVector(numberCashFlowsThisStep1)
        cashFlowsGenerated2 = MarketModelPathwiseMultiProductCashFlowVectorVector(cashFlowsGenerated1)

        for j in marketModels:

            testedFactors = [min(1, len(vars.todaysForwards))]

            for factors in testedFactors:
                generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                logNormal = true

                marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                evolver1 = LogNormalFwdRateEuler(
                    marketModel, generatorFactory, swaptionsDeflated.suggestedNumeraires())

                evolver2 = LogNormalFwdRateEuler(
                    marketModel, generatorFactory, swaptionsDeflated.suggestedNumeraires())

                for p in range(pathsToDo):
                    evolver1.startNewPath()
                    swaptionsDeflated.reset()
                    evolver2.startNewPath()
                    swaptionsDeflated2.reset()
                    step = 0

                    while true:

                        evolver1.advanceStep()
                        done = swaptionsDeflated.nextTimeStep(
                            evolver1.currentState(),
                            numberCashFlowsThisStep1,
                            cashFlowsGenerated1)

                        evolver2.advanceStep()
                        done2 = swaptionsDeflated2.nextTimeStep(
                            evolver2.currentState(),
                            numberCashFlowsThisStep2,
                            cashFlowsGenerated2)

                        self.assertFalse(done != done2)

                        for prod in range(swaptionsDeflated.numberOfProducts()):
                            self.assertFalse(numberCashFlowsThisStep1[prod] != numberCashFlowsThisStep2[prod])

                            for cf in range(numberCashFlowsThisStep1[prod]):
                                for rate in range(0, numberRates + 1):
                                    self.assertFalse(
                                        abs(cashFlowsGenerated1[prod][cf].amount()[rate] -
                                            cashFlowsGenerated2[prod][cf].amount()[rate]) > tolerance)

                        step += 1

                        if done:
                            break

        for j in marketModels:

            testedFactors = [min(1, len(vars.todaysForwards))]

            for factors in testedFactors:
                generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                logNormal = true

                marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                evolver = LogNormalFwdRateEuler(
                    marketModel,
                    generatorFactory, swaptionsDeflated.suggestedNumeraires())

                initialNumeraire = evolver.numeraires()[0]
                initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]

                possibleBumps = VegaBumpCollection(
                    marketModel,
                    allowFactorwiseBumping)

                bumpFinder = OrthogonalizedBumpFinder(
                    possibleBumps,
                    swaptions,
                    caps,
                    multiplier,
                    tolerance)

                theBumps = MatrixVectorVector()

                bumpFinder.GetVegaBumps(theBumps)

                values = DoubleVector()

                errors = DoubleVector()

                accountingEngine = PathwiseVegasAccountingEngine(
                    evolver,
                    CloneMarketModelPathwiseMultiProduct(swaptionsDeflated),
                    marketModel,
                    theBumps, initialNumeraireValue)

                accountingEngine.multiplePathValues(values, errors, pathsToDoSimulation)

                vegasMatrix = Matrix(swaptionsDeflated.numberOfProducts(), len(theBumps[0]))
                standardErrors = Matrix(swaptionsDeflated.numberOfProducts(), len(theBumps[0]))
                entriesPerProduct = 1 + numberRates + len(theBumps[0])

                for i in range(swaptionsDeflated.numberOfProducts()):
                    for j in range(len(theBumps[0])):
                        vegasMatrix[i][j] = values[i * entriesPerProduct + numberRates + 1 + j]
                        standardErrors[i][j] = errors[i * entriesPerProduct + numberRates + 1 + j]

                impliedVols_ = DoubleVector(len(swaptions))

                for i in range(len(swaptions)):
                    impliedVols_[i] = SwapForwardMappings.swaptionImpliedVolatility(
                        marketModel,
                        swaptions[i].startIndex_,
                        swaptions[i].endIndex_)

                analyticVegas = DoubleVector(len(swaptions))
                for i in range(len(swaptions)):
                    swapRate = cs.coterminalSwapRates()[i]
                    annuity = cs.coterminalSwapAnnuity(0, i) * initialNumeraireValue
                    expiry = vars.rateTimes[i]
                    sd = impliedVols_[i] * sqrt(expiry)
                    swapDisplacement = 0.0

                    vega = blackFormulaVolDerivative(
                        swapRate,
                        swapRate,
                        sd,
                        expiry,
                        annuity,
                        swapDisplacement)

                    analyticVegas[i] = vega * 0.01

                numberDiagonalFailures = 0
                offDiagonalFailures = 0

                av = [i for i in analyticVegas]

                for i in range(len(swaptions)):
                    thisError = vegasMatrix[i][i] - analyticVegas[i]
                    thisErrorInSds = thisError / (
                            standardErrors[i][i] + 1E-6)

                    if abs(thisErrorInSds) > 4:
                        numberDiagonalFailures += 1

                for i in range(len(swaptions)):
                    for j in range(len(theBumps[0])):
                        if i != j:
                            thisError = vegasMatrix[i][j]

                            thisErrorInSds = thisError / (standardErrors[i][j] + 1E-6)

                            if abs(thisErrorInSds) > 3.5:
                                offDiagonalFailures += 1

                self.assertFalse(offDiagonalFailures + numberDiagonalFailures > 0)

        for j in marketModels:

            testedFactors = [min(2, len(vars.todaysForwards))]

            for factors in testedFactors:
                generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                logNormal = true

                marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                evolver = LogNormalFwdRateEuler(
                    marketModel,
                    generatorFactory, capsDeflated.suggestedNumeraires())

                initialNumeraire = evolver.numeraires()[0]
                initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]

                possibleBumps = VegaBumpCollection(
                    marketModel,
                    allowFactorwiseBumping)

                bumpFinder = OrthogonalizedBumpFinder(
                    possibleBumps,
                    swaptions,
                    caps,
                    multiplier,
                    tolerance)

                theBumps = MatrixVectorVector()

                bumpFinder.GetVegaBumps(theBumps)

                values = DoubleVector()
                errors = DoubleVector()

                accountingEngine = PathwiseVegasAccountingEngine(
                    evolver,
                    CloneMarketModelPathwiseMultiProduct(capsDeflated),
                    marketModel,
                    theBumps, initialNumeraireValue)

                accountingEngine.multiplePathValues(values, errors, pathsToDoSimulation)

                vegasMatrix = Matrix(capsDeflated.numberOfProducts(), len(theBumps[0]))
                standardErrors = Matrix(capsDeflated.numberOfProducts(), len(theBumps[0]))
                entriesPerProduct = 1 + numberRates + len(theBumps[0])

                for i in range(capsDeflated.numberOfProducts()):
                    for j in range(len(theBumps[0])):
                        vegasMatrix[i][j] = values[i * entriesPerProduct + numberRates + j + 1]
                        standardErrors[i][j] = errors[i * entriesPerProduct + numberRates + j + 1]

                impliedVols_ = DoubleVector(len(caps))

                analyticVegas = DoubleVector(len(caps))
                for i in range(len(caps)):

                    capPseudo = CapPseudoDerivative(
                        marketModel,
                        caps[i].strike_,
                        caps[i].startIndex_,
                        caps[i].endIndex_, initialNumeraireValue)

                    impliedVols_[i] = capPseudo.impliedVolatility()

                    vega = 0.0

                    for j in range(caps[i].startIndex_, caps[i].endIndex_):
                        forward = cs.forwardRates()[j]
                        annuity = cs.discountRatio(j + 1, 0) * initialNumeraireValue * vars.accruals[j]
                        expiry = vars.rateTimes[j]
                        sd = impliedVols_[i] * sqrt(expiry)
                        displacement = 0.0

                        capletVega = blackFormulaVolDerivative(
                            caps[i].strike_, forward,
                            sd,
                            expiry,
                            annuity,
                            displacement)

                        vega += capletVega

                    analyticVegas[i] = vega * 0.01

                numberDiagonalFailures = 0
                offDiagonalFailures = 0

                for i in range(len(caps)):
                    thisError = vegasMatrix[i][i + len(swaptions)] - analyticVegas[i]
                    thisErrorInSds = thisError / (standardErrors[i][i + len(swaptions)] + 1E-6)

                    if abs(thisErrorInSds) > 4:
                        numberDiagonalFailures += 1

                for i in range(len(caps)):
                    for j in range(len(theBumps[0])):
                        if i + len(swaptions) != j:
                            thisError = vegasMatrix[i][j]

                            thisErrorInSds = thisError / (standardErrors[i][j] + 1E-6)

                            if abs(thisErrorInSds) > 3.5:
                                offDiagonalFailures += 1

                self.assertFalse(offDiagonalFailures + numberDiagonalFailures > 0)

    def testStochVolForwardsAndOptionlets(self):

        TEST_MESSAGE(
            "Testing exact repricing of "
            "forwards and optionlets "
            "in a stochastic vol displaced diffusion forward rate market model...")
        vars = CommonVars()
        vars.setup()

        forwardStrikes = DoubleVector(len(vars.todaysForwards))
        optionletPayoffs = PayoffVector(len(vars.todaysForwards))

        for i in range(len(vars.todaysForwards)):
            forwardStrikes[i] = vars.todaysForwards[i] + 0.01
            optionletPayoffs[i] = PlainVanillaPayoff(
                Option.Call, vars.todaysForwards[i])

        forwards = MultiStepForwards(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, forwardStrikes)
        optionlets = MultiStepOptionlets(
            vars.rateTimes, vars.accruals,
            vars.paymentTimes, optionletPayoffs)

        product = MultiProductComposite()
        product.add(CloneMarketModelMultiProduct(forwards))
        product.add(CloneMarketModelMultiProduct(optionlets))
        product.finalize()

        evolution = product.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility]

        firstVolatilityFactor = 2
        volatilityFactorStep = 2

        meanLevel = 1.0
        reversionSpeed = 1.0

        volVar = 1
        v0 = 1.0
        numberSubSteps = 8
        w1 = 0.5
        w2 = 0.5
        cutPoint = 1.5

        volProcess = SquareRootAndersen(
            meanLevel,
            reversionSpeed,
            volVar,
            v0,
            evolution.evolutionTimes(),
            numberSubSteps,
            w1,
            w2,
            cutPoint)

        for j in marketModels:

            testedFactors = [1, 2, len(vars.todaysForwards)]
            for factors in testedFactors:
                measures = [MeasureType.MoneyMarket, MeasureType.Terminal]

                for measure in measures:
                    numeraires = self.makeMeasure(product, measure, vars)

                    logNormal = true
                    marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                    for n in range(1):
                        generatorFactory = MTBrownianGeneratorFactory(vars.seed_)

                        evolver = SVDDFwdRatePc(
                            marketModel,
                            generatorFactory,
                            volProcess,
                            firstVolatilityFactor,
                            volatilityFactorStep,
                            numeraires)

                        stats = vars.simulate(
                            evolver, CloneMarketModelMultiProduct(product))

                        results = stats.mean()
                        errors = stats.errorEstimate()

                        for i in range(len(vars.accruals)):
                            trueValue = vars.todaysDiscounts[i] - vars.todaysDiscounts[i + 1] * (
                                    1 + forwardStrikes[i] * vars.accruals[i])
                            error = results[i] - trueValue
                            errorSds = error / errors[i]

                            self.assertFalse(abs(errorSds) > 3.5)

                        for i in range(len(vars.accruals)):
                            volCoeff = vars.volatilities[i]

                            theta = volCoeff * volCoeff * meanLevel
                            kappa = reversionSpeed
                            sigma = volCoeff * volVar
                            rho = 0.0
                            v1 = v0 * volCoeff * volCoeff

                            payoff = PlainVanillaPayoff(Option.Call, forwardStrikes[i])

                            nullEng = AnalyticHestonEngine(
                                HestonModel(
                                    HestonProcess(
                                        YieldTermStructureHandle(),
                                        YieldTermStructureHandle(),
                                        QuoteHandle(),
                                        1.0, 1.0, 1.0, 1.0, 1.0)))
                            trueValue = Value()
                            evaluations = Value()
                            AnalyticHestonEngine.doCalculation(
                                1.0,
                                1.0,
                                vars.todaysForwards[i] + vars.displacement,
                                vars.todaysForwards[i] + vars.displacement, vars.rateTimes[i], kappa, theta,
                                sigma, v1, rho, payoff,
                                AnalyticHestonEngineIntegration.gaussLaguerre(),
                                AnalyticHestonEngine.Gatheral,
                                nullEng, trueValue, evaluations)

                            trueValue = trueValue.value()
                            trueValue *= vars.accruals[i] * vars.todaysDiscounts[i + 1]

                            error = results[i + len(vars.accruals)] - trueValue
                            errorSds = error / errors[i]

                            self.assertFalse(abs(errorSds) > 4)

    def testAbcdVolatilityIntegration(self):

        TEST_MESSAGE(
            "Testing Abcd-volatility integration...")
        vars = CommonVars()
        vars.setup()

        a = -0.0597
        b = 0.1677
        c = 0.5403
        d = 0.1710

        N = 10
        precision = 1e-04

        instVol = AbcdFunction(a, b, c, d)
        SI = SegmentIntegral(20000)
        for i in range(N):
            T1 = 0.5 * (1 + i)
            for k in range(N - i):
                T2 = 0.5 * (1 + k)

                for j in range(N):
                    xMin = 0.5 * j
                    for l in range(N - j):
                        xMax = xMin + 0.5 * l
                        abcd2 = AbcdSquared(a, b, c, d, T1, T2)
                        numerical = SI(abcd2, xMin, xMax)
                        analytical = instVol.covariance(xMin, xMax, T1, T2)
                        self.assertFalse(abs(analytical - numerical) > precision)
                        if T1 == T2:
                            variance = instVol.variance(xMin, xMax, T1)
                            self.assertFalse(abs(analytical - variance) > 1e-14)

    def testAbcdVolatilityCompare(self):

        TEST_MESSAGE(
            "Testing different implementations of Abcd-volatility...")
        vars = CommonVars()
        vars.setup()

        a = 0.0597
        b = 0.1677
        c = 0.5403
        d = 0.1710

        lmAbcd = LmExtLinearExponentialVolModel(vars.rateTimes, b, c, d, a)
        abcd = AbcdFunction(a, b, c, d)
        for i1 in range(len(vars.rateTimes)):
            for i2 in range(len(vars.rateTimes)):
                T = 0.
                while T < min(vars.rateTimes[i1], vars.rateTimes[i2]):
                    lmCovariance = lmAbcd.integratedVariance(i1, i2, T)
                    abcdCovariance = abcd.covariance(0, T, vars.rateTimes[i1], vars.rateTimes[i2])
                    self.assertFalse(abs(lmCovariance - abcdCovariance) > 1e-10)
                    T += 0.5

    def testAbcdVolatilityFit(self):

        TEST_MESSAGE(
            "Testing Abcd-volatility fit...")
        vars = CommonVars()
        vars.setup()
        v = DoubleVector(len(vars.rateTimes) - 1)
        for i in range(len(v)):
            v[i] = vars.rateTimes[i]
        instVol = AbcdCalibration(
            v, vars.blackVols)

        a0 = instVol.a()
        b0 = instVol.b()
        c0 = instVol.c()
        d0 = instVol.d()
        error0 = instVol.error()

        instVol.compute()

        ec = instVol.endCriteria()
        a1 = instVol.a()
        b1 = instVol.b()
        c1 = instVol.c()
        d1 = instVol.d()
        error1 = instVol.error()

        self.assertFalse(error1 >= error0)

        abcd = AbcdFunction(a1, b1, c1, d1)
        v = DoubleVector(len(vars.rateTimes) - 1)
        for i in range(len(v)):
            v[i] = vars.rateTimes[i]
        k = instVol.k(
            v, vars.blackVols)
        tol = 3.0e-4
        for i in range(vars.blackVols.size()):
            self.assertFalse(abs(k[i] - 1.0) > tol)

    def testDriftCalculator(self):

        TEST_MESSAGE(
            "Testing drift calculation...")
        vars = CommonVars()
        vars.setup()

        tolerance = 1.0e-16
        factors = len(vars.todaysForwards)
        evolutionTimes = DoubleVector(len(vars.rateTimes) - 1)

        for i in range(len(vars.rateTimes) - 1):
            evolutionTimes[i] = vars.rateTimes[i]
        evolution = EvolutionDescription(vars.rateTimes, evolutionTimes)
        rateTaus = evolution.rateTaus()
        numeraires = moneyMarketPlusMeasure(evolution,
                                            vars.measureOffset_)
        alive = evolution.firstAliveRate()
        numberOfSteps = evolutionTimes.size()
        drifts = DoubleVector(numberOfSteps)
        driftsReduced = DoubleVector(numberOfSteps)
        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility,
            MarketModelType.ExponentialCorrelationAbcdVolatility]
        for k in marketModels:
            logNormal = true
            marketModel = vars.makeMarketModel(logNormal, evolution, factors, k)
            displacements = marketModel.displacements()
            for j in range(numberOfSteps):
                A = marketModel.pseudoRoot(j)

                inf = max(0, int(alive[j]))
                for h in range(inf, len(numeraires)):
                    driftcalculator = LMMDriftCalculator(
                        A, displacements, rateTaus,
                        numeraires[h], alive[j])
                    driftcalculator.computePlain(vars.todaysForwards, drifts)
                    driftcalculator.computeReduced(
                        vars.todaysForwards,
                        driftsReduced)
                    for i in range(drifts.size()):
                        error = abs(driftsReduced[i] - drifts[i])
                        self.assertFalse(error > tolerance)

    def testIsInSubset(self):

        TEST_MESSAGE(
            "Testing isInSubset function...")
        vars = CommonVars()
        vars.setup()

        dim = 100
        set = DoubleVector()
        subset = DoubleVector()
        for i in range(dim):
            set.append(i * 1.0)
        for i in range(dim):
            subset.append(dim + i * 1.0)
        result = isInSubset(set, subset)

    def testAbcdDegenerateCases(self):
        TEST_MESSAGE(
            "Testing abcd degenerate cases...")

        f1 = AbcdFunction(0.0, 0.0, 1.0E-15, 1.0)
        f2 = AbcdFunction(1.0, 0.0, 1.0E-50, 0.0)

        cov1 = f1.covariance(0.0, 1.0, 1.0, 1.0)
        self.assertFalse(abs(cov1 - 1.0) > 1E-14)

        cov2 = f2.covariance(0.0, 1.0, 1.0, 1.0)
        self.assertFalse(abs(cov2 - 1.0) > 1E-14)

    def testCovariance(self):
        TEST_MESSAGE(
            "Testing market models covariance...")

        n = 10

        rateTimes = DoubleVector()
        evolTimes1 = DoubleVector()
        evolTimes2 = DoubleVector()
        evolTimes3 = DoubleVector()
        evolTimes4 = DoubleVector()
        evolTimes = DoubleVectorVector()

        for i in range(1, n + 1):
            rateTimes.append(i)
        evolTimes1.append(n - 1)
        for i in range(1, n - 1 + 1):
            evolTimes2.append(i)
        for i in range(1, 2 * n - 2 + 1):
            evolTimes3.append(0.5 * i)
        evolTimes4.append(0.3)
        evolTimes4.append(1.3)
        evolTimes4.append(2.0)
        evolTimes4.append(4.5)
        evolTimes4.append(8.2)

        evolTimes.append(evolTimes1)
        evolTimes.append(evolTimes2)
        evolTimes.append(evolTimes3)
        evolTimes.append(evolTimes4)

        evolNames = []
        evolNames.append("one evolution time")
        evolNames.append("evolution times on rate fixings")
        evolNames.append("evolution times on rate fixings and midpoints between fixings")
        evolNames.append("irregular evolution times")

        ks = DoubleVector(n - 1, 1.0)
        displ = DoubleVector(n - 1, 0.0)
        rates = DoubleVector(n - 1, 0.0)
        vols = DoubleVector(n - 1, 1.0)

        c = exponentialCorrelations(rateTimes, 0.5, 0.2, 1.0, 0.0)
        corr = TimeHomogeneousForwardCorrelation(c, rateTimes)

        modelNames = []
        modelNames.append("FlatVol")
        modelNames.append("AbcdVol")

        for k in range(len(modelNames)):
            for l in range(len(evolNames)):
                evolution = EvolutionDescription(rateTimes, evolTimes[l])
                model = None
                if k == 0:
                    model = FlatVol(vols, corr, evolution, n - 1, rates, displ)

                if k == 1:
                    model = AbcdVol(
                        1.0, 0.0, 1.0E-50, 0.0, ks,
                        corr, evolution, n - 1, rates, displ)

                if model is not None:
                    for i in range(len(evolTimes[l])):
                        cov = model.covariance(i)
                        dt = evolTimes[l][i] - (evolTimes[l][i - 1] if i > 0 else 0.0)
                        for x in range(n - 1):
                            for y in range(n - 1):
                                self.assertFalse(
                                    min(rateTimes[x], rateTimes[y]) >= evolTimes[l][i]
                                    and abs(cov[x][y] - c[x][y] * dt) > 1.0E-14)

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
            self.assertFalse(
                not isInMoneyMarketPlusMeasure(evolution, result, vars.measureOffset_))

        return result

    def checkMultiProductCompositeResults(self,
                                          stats,
                                          subProductExpectedValues,
                                          vars):

        results = stats.mean()
        errors = stats.errorEstimate()

        nbOfResults = 0
        for subProductExpectedValue in subProductExpectedValues:
            for j in range(len(subProductExpectedValue.values)):
                nbOfResults += 1

        self.assertFalse(nbOfResults != len(results))

        currentResultIndex = 0

        stdDevs = []
        for subProductExpectedValue in subProductExpectedValues:
            minError = QL_MAX_REAL
            maxError = QL_MIN_REAL
            errorThreshold = subProductExpectedValue.errorThreshold
            for value in subProductExpectedValue.values:
                stdDev = (results[currentResultIndex] - value) / errors[currentResultIndex]
                stdDevs.append(stdDev)
                maxError = max(maxError, stdDev)
                minError = min(minError, stdDev)
                currentResultIndex += 1

            isBiased = minError > 0.0 or maxError < 0.0
            self.assertFalse(
                vars.printReport_
                or (subProductExpectedValue.testBias and isBiased)
                or max(-minError, maxError) > errorThreshold)

    def _testMultiProductComposite(self,
                                   product,
                                   subProductExpectedValues,
                                   testDescription,
                                   vars):

        TEST_MESSAGE(
            "Testing exact repricing of "
            + testDescription
            + "in a lognormal forward rate market model...")

        vars.setup()

        evolution = product.evolution()

        marketModels = [
            MarketModelType.ExponentialCorrelationFlatVolatility,
            MarketModelType.ExponentialCorrelationAbcdVolatility]
        for j in marketModels:

            testedFactors = [4, 8, len(vars.todaysForwards)]
            for factors in testedFactors:

                measures = [
                    MeasureType.Terminal, MeasureType.MoneyMarketPlus,
                    MeasureType.MoneyMarket]
                for measure in measures:
                    numeraires = self.makeMeasure(product, measure, vars)

                    logNormal = true
                    marketModel = vars.makeMarketModel(logNormal, evolution, factors, j)

                    evolvers = [EvolverType.Pc, EvolverType.Balland, EvolverType.Ipc]

                    stop = 0 if isInTerminalMeasure(evolution, numeraires) else 1
                    for i in range(len(evolvers) - stop):

                        for n in range(1):
                            generatorFactory = SobolBrownianGeneratorFactory(
                                SobolBrownianGenerator.Diagonal,
                                vars.seed_)

                            evolver = makeMarketModelEvolver(
                                marketModel, numeraires,
                                generatorFactory, evolvers[i])

                            stats = vars.simulate(evolver, CloneMarketModelMultiProduct(product))
                            self.checkMultiProductCompositeResults(
                                stats, subProductExpectedValues, vars)

    def checkForwardsAndOptionlets(self,
                                   stats,
                                   forwardStrikes,
                                   displacedPayoffs,
                                   *args):
        vars = args[0]
        results = stats.mean()
        errors = stats.errorEstimate()
        stdDevs = DoubleVector(len(vars.todaysForwards))

        N = len(vars.todaysForwards)
        expectedForwards = DoubleVector(N)
        expectedCaplets = DoubleVector(N)
        forwardStdDevs = DoubleVector(N)
        capletStdDev = DoubleVector(N)
        minError = QL_MAX_REAL
        maxError = QL_MIN_REAL

        for i in range(N):
            expectedForwards[i] = (vars.todaysForwards[i] - forwardStrikes[i]) * vars.accruals[i] * \
                                  vars.todaysDiscounts[i + 1]
            forwardStdDevs[i] = (results[i] - expectedForwards[i]) / errors[i]
            if forwardStdDevs[i] > maxError:
                maxError = forwardStdDevs[i]
            elif forwardStdDevs[i] < minError:
                minError = forwardStdDevs[i]
            expiry = vars.rateTimes[i]
            expectedCaplets[i] = BlackCalculator(
                displacedPayoffs[i],
                vars.todaysForwards[i] + vars.displacement,
                vars.volatilities[i] * sqrt(expiry),
                vars.todaysDiscounts[i + 1] * vars.accruals[i]).value()
            capletStdDev[i] = (results[i + N] - expectedCaplets[i]) / errors[i + N]
            if capletStdDev[i] > maxError:
                maxError = capletStdDev[i]
            elif capletStdDev[i] < minError:
                minError = capletStdDev[i]

        errorThreshold = 2.50
        self.assertFalse(
            vars.printReport_ or minError > 0.0 or maxError < 0.0 or
            minError < -errorThreshold or maxError > errorThreshold)

    def checkNormalForwardsAndOptionlets(self,
                                         stats,
                                         forwardStrikes,
                                         displacedPayoffs,
                                         *args):
        vars = args[0]
        results = stats.mean()
        errors = stats.errorEstimate()
        stdDevs = DoubleVector(len(vars.todaysForwards))

        N = len(vars.todaysForwards)
        expectedForwards = DoubleVector(N)
        expectedCaplets = DoubleVector(N)
        forwardStdDevs = DoubleVector(N)
        capletStdDev = DoubleVector(N)
        minError = QL_MAX_REAL
        maxError = QL_MIN_REAL

        for i in range(N):
            expectedForwards[i] = (vars.todaysForwards[i] - forwardStrikes[i]) * vars.accruals[i] * \
                                  vars.todaysDiscounts[i + 1]
            forwardStdDevs[i] = (results[i] - expectedForwards[i]) / errors[i]
            if forwardStdDevs[i] > maxError:
                maxError = forwardStdDevs[i]
            elif forwardStdDevs[i] < minError:
                minError = forwardStdDevs[i]
            expiry = vars.rateTimes[i]
            expectedCaplets[i] = bachelierBlackFormula(
                displacedPayoffs[i],
                vars.todaysForwards[i] + vars.displacement,
                vars.normalVols[i] * sqrt(expiry),
                vars.todaysDiscounts[i + 1] * vars.accruals[i])
            capletStdDev[i] = (results[i + N] - expectedCaplets[i]) / errors[i + N]
            if capletStdDev[i] > maxError:
                maxError = capletStdDev[i]
            elif capletStdDev[i] < minError:
                minError = capletStdDev[i]

        errorThreshold = 2.50
        self.assertFalse(
            minError > 0.0 or maxError < 0.0 or
            minError < -errorThreshold or maxError > errorThreshold)

    def checkCallableSwap(self, stats):
        payerNPV = stats.mean()[0]
        receiverNPV = stats.mean()[1]
        bermudanNPV = stats.mean()[2]
        callableNPV = stats.mean()[3]
        tolerance = 1.1e-15
        swapError = abs(receiverNPV + payerNPV)
        callableError = abs(receiverNPV + bermudanNPV - callableNPV)

        self.assertFalse(
            swapError > tolerance or bermudanNPV < 0.0 or
            callableNPV < receiverNPV or callableError > tolerance)

        self.assertFalse(swapError > tolerance)
        self.assertFalse(bermudanNPV < 0.0)
        self.assertFalse(callableNPV < receiverNPV)
        self.assertFalse(callableError > tolerance)

    def _testCallableSwapAnderson(self,
                                  marketModelType,
                                  testedFactor,
                                  vars):

        TEST_MESSAGE(
            "Pricing callable swap with Anderson exercise "
            "strategy in a LIBOR market model for test factor "
            + testedFactor + " and model type "
            + marketModelTypeToString(marketModelType)
            + "...")
        vars.setup()

        fixedRate = 0.04

        payerSwap = MultiStepSwap(
            vars.rateTimes, vars.accruals, vars.accruals, vars.paymentTimes,
            fixedRate, true)

        receiverSwap = MultiStepSwap(
            vars.rateTimes, vars.accruals, vars.accruals, vars.paymentTimes,
            fixedRate, false)

        exerciseTimes = DoubleVector(vars.rateTimes)
        exerciseTimes.pop_back()

        swapTriggers = DoubleVector(exerciseTimes.size(), fixedRate)
        naifStrategy = SwapRateTrigger(vars.rateTimes, swapTriggers, exerciseTimes)

        collectedData = NodeDataVectorVector()

        parameters = DoubleVectorVector()
        control = NothingExerciseValue(vars.rateTimes)
        nullRebate = NothingExerciseValue(vars.rateTimes)
        parametricForm = TriggeredSwapExercise(
            vars.rateTimes, exerciseTimes,
            DoubleVector(exerciseTimes.size(), fixedRate))

        dummyProduct = CallSpecifiedMultiProduct(
            receiverSwap, naifStrategy,
            ExerciseAdapter(nullRebate))

        evolution = dummyProduct.evolution()

        factors = testedFactor

        measures = [
            MeasureType.Terminal]
        for measure in measures:
            numeraires = self.makeMeasure(dummyProduct, measure, vars)
            logNormal = true
            marketModel = vars.makeMarketModel(logNormal, evolution, factors, marketModelType)
            evolvers = [EvolverType.Pc, EvolverType.Balland, EvolverType.Ipc]

            stop = 0 if isInTerminalMeasure(evolution, numeraires) else 1
            for i in range(len(evolvers) - stop):
                for n in range(1):

                    generatorFactory = SobolBrownianGeneratorFactory(
                        SobolBrownianGenerator.Diagonal, vars.seed_)
                    evolver = makeMarketModelEvolver(
                        marketModel,
                        numeraires,
                        generatorFactory,
                        evolvers[i])

                    collectNodeData(
                        evolver,
                        receiverSwap, parametricForm, nullRebate,
                        control, vars.trainingPaths_, collectedData)
                    om = Simplex(0.01)
                    ec = EndCriteria(1000, 100, 1e-8, 1e-16, 1e-8)
                    initialNumeraire = evolver.numeraires()[0]
                    initialNumeraireValue = vars.todaysDiscounts[initialNumeraire]
                    firstPassValue = genericEarlyExerciseOptimization(
                        collectedData, parametricForm, parameters, ec, om) * initialNumeraireValue

                    exerciseStrategy = ParametricExerciseAdapter(parametricForm, parameters)

                    bermudanProduct = CallSpecifiedMultiProduct(
                        MultiStepNothing(evolution),
                        exerciseStrategy, payerSwap)

                    callableProduct = CallSpecifiedMultiProduct(
                        receiverSwap, exerciseStrategy,
                        ExerciseAdapter(nullRebate))

                    allProducts = MultiProductComposite()
                    allProducts.add(payerSwap)
                    allProducts.add(receiverSwap)
                    allProducts.add(bermudanProduct)
                    allProducts.add(callableProduct)
                    allProducts.finalize()
                    stats = vars.simulate(evolver, allProducts)
                    self.checkCallableSwap(stats)

                    uFactory = SobolBrownianGeneratorFactory(
                        SobolBrownianGenerator.Diagonal, vars.seed_ + 142)
                    evolver = makeMarketModelEvolver(
                        marketModel,
                        numeraires,
                        uFactory,
                        evolvers[i])

                    innerEvolvers = MarketModelEvolverVector()
                    isExerciseTime = isInSubset(
                        evolution.evolutionTimes(),
                        exerciseStrategy.exerciseTimes())
                    for s in range(len(isExerciseTime)):
                        if isExerciseTime[s]:
                            iFactory = MTBrownianGeneratorFactory(vars.seed_ + s)
                            e = makeMarketModelEvolver(
                                marketModel,
                                numeraires,
                                iFactory,
                                evolvers[i],
                                s)
                            innerEvolvers.append(e)

                    uEngine = UpperBoundEngine(
                        evolver, innerEvolvers,
                        receiverSwap, nullRebate,
                        receiverSwap, nullRebate,
                        exerciseStrategy,
                        initialNumeraireValue)
                    uStats = RiskStatistics()
                    uEngine.multiplePathValues(uStats, 255, 256)
                    delta = uStats.mean()
                    deltaError = uStats.errorEstimate()
