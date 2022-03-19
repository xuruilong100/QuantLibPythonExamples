import unittest
from utilities import *
from QuantLib import *

# auxiliary data
termsData = [
    Period(0, Days), Period(1, Years), Period(2, Years), Period(3, Years),
    Period(5, Years), Period(7, Years), Period(10, Years), Period(15, Years),
    Period(20, Years), Period(61, Years)  # avoid extrapolation issues with 30y caplets
]
terms = termsData

discRatesData = [
    -0.00147407, -0.001761684, -0.001736745, -0.00119244, 0.000896055,
    0.003537077, 0.007213824, 0.011391278, 0.013334611, 0.013982809]
discRates = discRatesData

proj3mRatesData = [
    -0.000483439, -0.000578569, -0.000383832, 0.000272656, 0.002478699,
    0.005100113, 0.008750643, 0.012788095, 0.014534052, 0.014942896]
proj3mRates = proj3mRatesData

proj6mRatesData = [
    0.000233608, 0.000218862, 0.000504018, 0.001240556, 0.003554415,
    0.006153921, 0.009688264, 0.013521628, 0.015136391, 0.015377704]
proj6mRates = proj6mRatesData


def getYTS(terms,
           rates,
           spread=0.0):
    today = Settings.instance().evaluationDate
    dates = DateVector()
    # dates.reserve(terms.size())
    for term in terms:
        dates.append(
            NullCalendar().advance(today, term, Unadjusted))
    ratesPlusSpread = DoubleVector(rates)
    # for k in ratesPlusSpread:
    #     k += spread
    for i in range(len(ratesPlusSpread)):
        ratesPlusSpread[i] += spread
    ts = CubicZeroCurve(
        dates, ratesPlusSpread, Actual365Fixed(), NullCalendar())
    return RelinkableYieldTermStructureHandle(ts)


capletTermsData = [
    Period(1, Years), Period(2, Years), Period(3, Years),
    Period(5, Years), Period(7, Years), Period(10, Years),
    Period(15, Years), Period(20, Years), Period(25, Years),
    Period(30, Years)]
capletTerms = capletTermsData

capletStrikesData = [
    -0.0050, 0.0000, 0.0050, 0.0100, 0.0150, 0.0200, 0.0300, 0.0500]
capletStrikes = capletStrikesData


def getOptionletTS():
    today = Settings.instance().evaluationDate
    dates = DateVector()
    dates.reserve(len(capletTerms))
    for capletTerm in capletTerms:
        dates.append(
            TARGET().advance(today, capletTerm, Following))
    # set up vol data manually
    capletVols = [
        [0.003010094, 0.002628065, 0.00456118, 0.006731268, 0.008678572, 0.010570881, 0.014149552, 0.021000638],
        [0.004173715, 0.003727039, 0.004180263, 0.005726083, 0.006905876, 0.008263514, 0.010555395, 0.014976523],
        [0.005870143, 0.005334526, 0.005599775, 0.006633987, 0.007773317, 0.009036581, 0.011474391, 0.016277549],
        [0.007458597, 0.007207522, 0.007263995, 0.007308727, 0.007813586, 0.008274858, 0.009743988, 0.012555171],
        [0.007711531, 0.007608826, 0.007572816, 0.007684107, 0.007971932, 0.008283118, 0.009268828, 0.011574083],
        [0.007619605, 0.007639059, 0.007719825, 0.007823373, 0.00800813, 0.008113384, 0.008616374, 0.009785436],
        [0.007312199, 0.007352993, 0.007369116, 0.007468333, 0.007515657, 0.00767695, 0.008020447, 0.009072769],
        [0.006905851, 0.006966315, 0.007056413, 0.007116494, 0.007259661, 0.00733308, 0.007667563, 0.008419696],
        [0.006529553, 0.006630731, 0.006749022, 0.006858027, 0.007001959, 0.007139097, 0.007390404, 0.008036255],
        [0.006225482, 0.006404012, 0.00651594, 0.006642273, 0.006640887, 0.006885713, 0.007093024, 0.00767373]]
    # create quotes
    capletVolQuotes = QuoteHandleVectorVector()
    for capletVol in capletVols:
        row = QuoteHandleVector()
        row.reserve(len(capletVol))
        for j in capletVol:
            row.append(RelinkableQuoteHandle(SimpleQuote(j)))
        capletVolQuotes.append(row)

    curve3m = getYTS(terms, proj3mRates)
    index = Euribor3M(curve3m)
    tmp1 = StrippedOptionlet(
        2, TARGET(), Following, index, dates, capletStrikes,
        capletVolQuotes, Actual365Fixed(), Normal, 0.0)
    tmp2 = StrippedOptionletAdapter(tmp1)
    return RelinkableOptionletVolatilityStructureHandle(tmp2)


swaptionVTSTermsData = [
    Period(1, Years), Period(5, Years),
    Period(10, Years), Period(20, Years), Period(30, Years)]
swaptionVTSTerms = swaptionVTSTermsData


def getSwaptionVTS():
    swaptionVols = [
        [0.002616, 0.00468, 0.0056, 0.005852, 0.005823],
        [0.006213, 0.00643, 0.006622, 0.006124, 0.005958],
        [0.006658, 0.006723, 0.006602, 0.005802, 0.005464],
        [0.005728, 0.005814, 0.005663, 0.004689, 0.004276],
        [0.005041, 0.005059, 0.004746, 0.003927, 0.003608]]
    swaptionVolQuotes = QuoteHandleVectorVector()
    for swaptionVol in swaptionVols:
        row = QuoteHandleVector()
        row.reserve(len(swaptionVol))
        for j in swaptionVol:
            row.append(RelinkableQuoteHandle(SimpleQuote(j)))
        swaptionVolQuotes.append(row)

    tmp = SwaptionVolatilityMatrix(
        TARGET(), Following, swaptionVTSTerms, swaptionVTSTerms,
        swaptionVolQuotes, Actual365Fixed(), true, Normal)
    return RelinkableSwaptionVolatilityStructureHandle(tmp)


class BasismodelsTest(unittest.TestCase):

    def testSwaptioncfsContCompSpread(self):
        TEST_MESSAGE(
            "Testing deterministic tenor basis model with continuous compounded spreads...")
        self._testSwaptioncfs(true)

    def testSwaptioncfsSimpleCompSpread(self):
        TEST_MESSAGE(
            "Testing deterministic tenor basis model with simple compounded spreads...")
        self._testSwaptioncfs(false)

    def testTenoroptionletvts(self):
        TEST_MESSAGE(
            "Testing volatility transformation for caplets/floorlets...")
        # market data and floating rate index
        today = Date(16, Sep, 2015)
        Settings.instance().evaluationDate = today
        spread = 0.01
        discYTS = getYTS(terms, discRates)
        proj3mYTS = getYTS(terms, proj3mRates)
        proj6mYTS = getYTS(terms, proj3mRates, spread)
        euribor3m = Euribor6M(proj3mYTS)
        euribor6m = Euribor6M(proj6mYTS)
        # 3m optionlet VTS
        optionletVTS3m = getOptionletTS()

        # we need a correlation structure
        corrTimesRaw = [0.0, 50.0]
        rhoInfDataRaw = [0.3, 0.3]
        betaDataRaw = [0.9, 0.9]
        corrTimes = corrTimesRaw
        rhoInfData = rhoInfDataRaw
        betaData = betaDataRaw
        rho = SafeLinearInterpolation(corrTimes, rhoInfData)
        beta = SafeLinearInterpolation(corrTimes, betaData)
        corr = TwoParameterCorrelation(rho, beta)
        # now we can set up the = volTS and calculate volatilities
        optionletVTS6m = TenorOptionletVTS(
            optionletVTS3m, euribor3m, euribor6m, corr)
        for capletTerm in capletTerms:
            for capletStrike in capletStrikes:
                vol3m = optionletVTS3m.volatility(capletTerm, capletStrike, true)
                vol6m = optionletVTS6m.volatility(capletTerm, capletStrike, true)
                vol6mShifted = optionletVTS6m.volatility(capletTerm, capletStrike + spread, true)
                # De-correlation yields that larger tenor shifted vols are smaller then shorter
                # tenor vols
                self.assertFalse(
                    vol6mShifted - vol3m > 0.0001)  # we leave 1bp tolerance due to simplified spread calculation

        # we need a correlation structure
        corrTimesRaw = [0.0, 50.0]
        rhoInfDataRaw = [0.0, 0.0]
        betaDataRaw = [0.0, 0.0]
        corrTimes = corrTimesRaw
        rhoInfData = rhoInfDataRaw
        betaData = betaDataRaw
        rho = SafeLinearInterpolation(corrTimes, rhoInfData)
        beta = SafeLinearInterpolation(corrTimes, betaData)
        corr = TwoParameterCorrelation(rho, beta)
        # now we can set up the = volTS and calculate volatilities
        optionletVTS6m = TenorOptionletVTS(optionletVTS3m, euribor3m, euribor6m, corr)
        for i in range(len(capletTerms)):
            for capletStrike in capletStrikes:
                vol3m = optionletVTS3m.volatility(capletTerms[i], capletStrike, true)
                vol6m = optionletVTS6m.volatility(capletTerms[i], capletStrike, true)
                vol6mShifted = optionletVTS6m.volatility(capletTerms[i], capletStrike + spread, true)
                # for perfect correlation shifted 6m vols should coincide with 3m vols
                tol = 0.001 if i < 3 else 0.0001  # 10bp tol for smaller tenors and 1bp tol for larger tenors
                self.assertFalse(abs(vol6mShifted - vol3m) > tol)

    def testTenorswaptionvts(self):
        TEST_MESSAGE("Testing volatility transformation for swaptions...")
        # market data and floating rate index
        spread = 0.01
        discYTS = getYTS(terms, discRates)
        proj3mYTS = getYTS(terms, proj3mRates)
        proj6mYTS = getYTS(terms, proj3mRates, spread)
        euribor3m = Euribor6M(proj3mYTS)
        euribor6m = Euribor6M(proj6mYTS)
        # Euribor6m ATM vols
        euribor6mSwVTS = getSwaptionVTS()
        # ----------
        euribor3mSwVTS = TenorSwaptionVTS(
            euribor6mSwVTS, discYTS, euribor6m, euribor3m,
            Period(1, Years), Period(1, Years),
            Thirty360(Thirty360.BondBasis),
            Thirty360(Thirty360.BondBasis))
        # 6m vols should be slightly larger then 3m vols due to basis
        for i in range(len(swaptionVTSTerms)):
            for j in range(len(swaptionVTSTerms)):
                vol6m = euribor6mSwVTS.volatility(
                    swaptionVTSTerms[i], swaptionVTSTerms[j], 0.01, true)
                vol3m = euribor3mSwVTS.volatility(
                    swaptionVTSTerms[i], swaptionVTSTerms[j], 0.01, true)
                self.assertFalse(vol3m > vol6m)

        # ----------
        euribor6mSwVTS2 = TenorSwaptionVTS(
            euribor6mSwVTS, discYTS, euribor6m, euribor6m,
            Period(1, Years), Period(1, Years),
            Thirty360(Thirty360.BondBasis), Thirty360(Thirty360.BondBasis))
        # 6m vols to 6m vols should yield initiial vols
        for i in range(len(swaptionVTSTerms)):
            for j in range(len(swaptionVTSTerms)):
                vol6m = euribor6mSwVTS.volatility(
                    swaptionVTSTerms[i], swaptionVTSTerms[j], 0.01, true)
                vol6m2 = euribor6mSwVTS2.volatility(
                    swaptionVTSTerms[i], swaptionVTSTerms[j], 0.01, true)
                tol = 1.0e-8
                self.assertFalse(abs(vol6m2 - vol6m) > tol)

        # ---------

        euribor3mSwVTS = TenorSwaptionVTS(
            euribor6mSwVTS, discYTS, euribor6m, euribor3m,
            Period(1, Years), Period(1, Years),
            Thirty360(Thirty360.BondBasis), Thirty360(Thirty360.BondBasis))
        euribor6mSwVTS2 = TenorSwaptionVTS(
            RelinkableSwaptionVolatilityStructureHandle(euribor3mSwVTS),
            discYTS, euribor3m, euribor6m, Period(1, Years), Period(1, Years),
            Thirty360(Thirty360.BondBasis), Thirty360(Thirty360.BondBasis))
        # 6m vols to 6m vols should yield initiial vols
        for i in range(len(swaptionVTSTerms)):
            for j in range(len(swaptionVTSTerms)):
                vol6m = euribor6mSwVTS.volatility(
                    swaptionVTSTerms[i], swaptionVTSTerms[j], 0.01, true)
                vol6m2 = euribor6mSwVTS2.volatility(
                    swaptionVTSTerms[i], swaptionVTSTerms[j], 0.01, true)
                tol = 1.0e-8
                self.assertFalse(abs(vol6m2 - vol6m) > tol)

    def _testSwaptioncfs(self, contTenorSpread):
        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()
        # market data and floating rate index
        discYTS = getYTS(terms, discRates)
        proj6mYTS = getYTS(terms, proj6mRates)
        euribor6m = Euribor6M(proj6mYTS)
        # Vanilla swap details
        today = Settings.instance().evaluationDate
        swapStart = TARGET().advance(today, Period(5, Years), Following)
        swapEnd = TARGET().advance(swapStart, Period(10, Years), Following)
        exerciseDate = TARGET().advance(swapStart, Period(-2, Days), Preceding)
        fixedSchedule = Schedule(
            swapStart, swapEnd, Period(1, Years), TARGET(), ModifiedFollowing,
            ModifiedFollowing, DateGeneration.Backward, false)
        floatSchedule = Schedule(
            swapStart, swapEnd, Period(6, Months), TARGET(), ModifiedFollowing,
            ModifiedFollowing, DateGeneration.Backward, false)
        swap = VanillaSwap(
            Swap.Payer, 10000.0, fixedSchedule, 0.03, Thirty360(Thirty360.BondBasis),
            floatSchedule, euribor6m, 0.0, euribor6m.dayCounter())
        swap.setPricingEngine(DiscountingSwapEngine(discYTS))
        # European exercise and swaption
        europeanExercise = EuropeanExercise(exerciseDate)
        swaption = Swaption(swap, europeanExercise, Settlement.Physical)
        # calculate basis model swaption cash flows, discount and conmpare with swap
        cashFlows = SwaptionCashFlows(swaption, discYTS, contTenorSpread)
        # model time is always Act365Fixed
        exerciseTime = Actual365Fixed().yearFraction(
            discYTS.referenceDate(), swaption.exercise().dates()[0])
        self.assertFalse(exerciseTime != cashFlows.exerciseTimes()[0])
        # there might be rounding errors
        tol = 1.0e-8
        # (discounted) fixed leg coupons must match swap fixed leg NPV
        fixedLeg = 0.0
        for k in range(len(cashFlows.fixedTimes())):
            fixedLeg += cashFlows.fixedWeights()[k] * discYTS.discount(cashFlows.fixedTimes()[k])
        self.assertFalse(abs(fixedLeg - (-swap.fixedLegNPV())) > tol)  # note, '-1' because payer swap
        # (discounted) floating leg coupons must match swap floating leg NPV
        floatLeg = 0.0
        for k in range(len(cashFlows.floatTimes())):
            floatLeg += cashFlows.floatWeights()[k] * discYTS.discount(cashFlows.floatTimes()[k])
        self.assertFalse(abs(floatLeg - swap.floatingLegNPV()) > tol)

        # There should not be spread coupons in a single-curve setting.
        # However, if indexed coupons are used the floating leg is not at par,
        # so we need to relax the tolerance to a level at which it will only
        # catch large errors.
        tol2 = tol if usingAtParCoupons else 0.02

        singleCurveCashFlows = SwaptionCashFlows(
            swaption, proj6mYTS, contTenorSpread)
        for k in range(1, len(singleCurveCashFlows.floatWeights()) - 1):
            self.assertFalse(
                abs(singleCurveCashFlows.floatWeights()[k]) > tol2)
