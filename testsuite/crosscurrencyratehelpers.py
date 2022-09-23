import unittest

from QuantLib import *

from utilities import *


class XccyTestDatum(object):
    def __init__(self,
                 n,
                 units,
                 basis):
        self.n = n
        self.units = units
        self.basis = basis


class CommonVars(object):

    def __init__(self):
        self.settlementDays = 2
        self.businessConvention = Following
        self.calendar = TARGET()
        self.dayCount = Actual365Fixed()
        self.endOfMonth = false
        self.basisPoint = 1.0e-4
        self.fxSpot = 1.25
        self.baseCcyIdxHandle = RelinkableYieldTermStructureHandle()
        self.quoteCcyIdxHandle = RelinkableYieldTermStructureHandle()
        self.baseCcyIdx = Euribor3M(self.baseCcyIdxHandle)
        self.quoteCcyIdx = USDLibor(
            Period(3, Months), self.quoteCcyIdxHandle)

        self.basisData = []
        self.basisData.append(XccyTestDatum(1, Years, -14.5))
        self.basisData.append(XccyTestDatum(18, Months, -18.5))
        self.basisData.append(XccyTestDatum(2, Years, -20.5))
        self.basisData.append(XccyTestDatum(3, Years, -23.75))
        self.basisData.append(XccyTestDatum(4, Years, -25.5))
        self.basisData.append(XccyTestDatum(5, Years, -26.5))
        self.basisData.append(XccyTestDatum(7, Years, -26.75))
        self.basisData.append(XccyTestDatum(10, Years, -26.25))
        self.basisData.append(XccyTestDatum(15, Years, -24.75))
        self.basisData.append(XccyTestDatum(20, Years, -23.25))
        self.basisData.append(XccyTestDatum(30, Years, -20.50))

        today = self.calendar.adjust(Date(6, September, 2013))
        Settings.instance().evaluationDate = today
        self.settlement = self.calendar.advance(today, self.settlementDays, Days)

        self.baseCcyIdxHandle.linkTo(flatRate(self.settlement, 0.007, self.dayCount))
        self.quoteCcyIdxHandle.linkTo(flatRate(self.settlement, 0.015, self.dayCount))
        self.backup = SavedSettings()

    def constantNotionalXccyRateHelper(self,
                                       q,
                                       collateralHandle,
                                       isFxBaseCurrencyCollateralCurrency,
                                       isBasisOnFxBaseCurrencyLeg):
        quoteHandle = QuoteHandle(SimpleQuote(q.basis * self.basisPoint))
        tenor = Period(q.n, q.units)
        return ConstNotionalCrossCurrencyBasisSwapRateHelper(
            quoteHandle, tenor, self.settlementDays, self.calendar,
            self.businessConvention, self.endOfMonth,
            self.baseCcyIdx, self.quoteCcyIdx,
            collateralHandle, isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg)

    def buildConstantNotionalXccyRateHelpers(self,
                                             xccyData,
                                             collateralHandle,
                                             isFxBaseCurrencyCollateralCurrency,
                                             isBasisOnFxBaseCurrencyLeg):
        instruments = RateHelperVector()

        for i in xccyData:
            instruments.append(self.constantNotionalXccyRateHelper(
                i, collateralHandle, isFxBaseCurrencyCollateralCurrency,
                isBasisOnFxBaseCurrencyLeg))

        return instruments

    def resettingXccyRateHelper(self,
                                q,
                                collateralHandle,
                                isFxBaseCurrencyCollateralCurrency,
                                isBasisOnFxBaseCurrencyLeg,
                                isFxBaseCurrencyLegResettable):
        quoteHandle = QuoteHandle(SimpleQuote(q.basis * self.basisPoint))
        tenor = Period(q.n, q.units)
        return MtMCrossCurrencyBasisSwapRateHelper(
            quoteHandle, tenor, self.settlementDays, self.calendar,
            self.businessConvention, self.endOfMonth,
            self.baseCcyIdx, self.quoteCcyIdx,
            collateralHandle, isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg, isFxBaseCurrencyLegResettable)

    def buildResettingXccyRateHelpers(self,
                                      xccyData,
                                      collateralHandle,
                                      isFxBaseCurrencyCollateralCurrency,
                                      isBasisOnFxBaseCurrencyLeg,
                                      isFxBaseCurrencyLegResettable):
        instruments = RateHelperVector()
        instruments.reserve(len(xccyData))
        for i in xccyData:
            instruments.append(
                self.resettingXccyRateHelper(
                    i, collateralHandle, isFxBaseCurrencyCollateralCurrency,
                    isBasisOnFxBaseCurrencyLeg, isFxBaseCurrencyLegResettable))

        return instruments

    def legSchedule(self,
                    tenor,
                    idx):
        sch = MakeSchedule()
        sch.fromDate(self.settlement)
        sch.to(self.settlement + tenor)
        sch.withTenor(idx.tenor())
        sch.withCalendar(self.calendar)
        sch.withConvention(self.businessConvention)
        sch.endOfMonth(self.endOfMonth)
        sch.backwards()
        sch = sch.makeSchedule()
        return sch

    def constantNotionalLeg(self,
                            schedule,
                            idx,
                            notional,
                            basis):
        leg = IborLeg(schedule, idx)
        leg.withNotionals(notional)
        leg.withSpreads(basis)
        leg = leg.makeLeg()
        lastPaymentDate = leg[-1].date()

        l = Leg()
        for i in leg:
            l.append(i)
        l.append(SimpleCashFlow(notional, lastPaymentDate))
        return l

    def buildXccyBasisSwap(self,
                           q,
                           fxSpot,
                           isFxBaseCurrencyCollateralCurrency,
                           isBasisOnFxBaseCurrencyLeg):
        baseCcyLegNotional = 1.0
        quoteCcyLegNotional = baseCcyLegNotional * fxSpot

        baseCcyLegBasis = q.basis * self.basisPoint if isBasisOnFxBaseCurrencyLeg else 0.0
        quoteCcyLegBasis = 0.0 if isBasisOnFxBaseCurrencyLeg else q.basis * self.basisPoint

        legs = []
        payer = true

        baseCcyLeg = self.constantNotionalLeg(
            self.legSchedule(Period(q.n, q.units), self.baseCcyIdx),
            self.baseCcyIdx, baseCcyLegNotional, baseCcyLegBasis)
        legs.append(
            Swap(LegVector(1, baseCcyLeg), BoolVector(1, not payer)))

        quoteCcyLeg = self.constantNotionalLeg(
            self.legSchedule(
                Period(q.n, q.units),
                self.quoteCcyIdx), self.quoteCcyIdx,
            quoteCcyLegNotional, quoteCcyLegBasis)
        legs.append(
            Swap(LegVector(1, quoteCcyLeg), BoolVector(1, payer)))
        return legs


class CrossCurrencyRateHelpersTest(unittest.TestCase):

    def testConstNotionalBasisSwapsWithCollateralInQuoteAndBasisInBaseCcy(self):
        TEST_MESSAGE(
            "Testing constant notional basis swaps with collateral in quote ccy and basis in base ccy...")

        isFxBaseCurrencyCollateralCurrency = false
        isBasisOnFxBaseCurrencyLeg = true

        self._testConstantNotionalCrossCurrencySwapsNPV(
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg)

    def testConstNotionalBasisSwapsWithCollateralInBaseAndBasisInQuoteCcy(self):
        TEST_MESSAGE(
            "Testing constant notional basis swaps with collateral in base ccy and basis in quote ccy...")

        isFxBaseCurrencyCollateralCurrency = true
        isBasisOnFxBaseCurrencyLeg = false

        self._testConstantNotionalCrossCurrencySwapsNPV(
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg)

    def testConstNotionalBasisSwapsWithCollateralAndBasisInBaseCcy(self):
        TEST_MESSAGE(
            "Testing constant notional basis swaps with collateral and basis in base ccy...")

        isFxBaseCurrencyCollateralCurrency = true
        isBasisOnFxBaseCurrencyLeg = true

        self._testConstantNotionalCrossCurrencySwapsNPV(
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg)

    def testConstNotionalBasisSwapsWithCollateralAndBasisInQuoteCcy(self):
        TEST_MESSAGE(
            "Testing constant notional basis swaps with collateral and basis in quote ccy...")

        isFxBaseCurrencyCollateralCurrency = false
        isBasisOnFxBaseCurrencyLeg = false

        self._testConstantNotionalCrossCurrencySwapsNPV(
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg)

    def testResettingBasisSwapsWithCollateralInQuoteAndBasisInBaseCcy(self):
        TEST_MESSAGE(
            "Testing resetting basis swaps with collateral in quote ccy and basis in base ccy...")

        isFxBaseCurrencyCollateralCurrency = false
        isFxBaseCurrencyLegResettable = false
        isBasisOnFxBaseCurrencyLeg = true

        self._testResettingCrossCurrencySwaps(
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg,
            isFxBaseCurrencyLegResettable)

    def testResettingBasisSwapsWithCollateralInBaseAndBasisInQuoteCcy(self):
        TEST_MESSAGE(
            "Testing resetting basis swaps with collateral in base ccy and basis in quote ccy...")

        isFxBaseCurrencyCollateralCurrency = true
        isFxBaseCurrencyLegResettable = true
        isBasisOnFxBaseCurrencyLeg = false

        self._testResettingCrossCurrencySwaps(
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg,
            isFxBaseCurrencyLegResettable)

    def testResettingBasisSwapsWithCollateralAndBasisInBaseCcy(self):
        TEST_MESSAGE(
            "Testing resetting basis swaps with collateral and basis in base ccy...")

        isFxBaseCurrencyCollateralCurrency = true
        isFxBaseCurrencyLegResettable = true
        isBasisOnFxBaseCurrencyLeg = true

        self._testResettingCrossCurrencySwaps(
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg,
            isFxBaseCurrencyLegResettable)

    def testResettingBasisSwapsWithCollateralAndBasisInQuoteCcy(self):
        TEST_MESSAGE(
            "Testing resetting basis swaps with collateral and basis in quote ccy...")

        isFxBaseCurrencyCollateralCurrency = false
        isFxBaseCurrencyLegResettable = false
        isBasisOnFxBaseCurrencyLeg = false

        self._testResettingCrossCurrencySwaps(
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg,
            isFxBaseCurrencyLegResettable)

    def testExceptionWhenInstrumentTenorShorterThanIndexFrequency(self):
        TEST_MESSAGE(
            "Testing exception when instrument tenor is shorter than index frequency...")

        vars = CommonVars()

        data = [XccyTestDatum(1, Months, 10.0)]
        collateralHandle = YieldTermStructureHandle()

        self.assertRaises(
            RuntimeError,
            vars.buildConstantNotionalXccyRateHelpers,
            data, collateralHandle, true, true)

    def _testConstantNotionalCrossCurrencySwapsNPV(self,
                                                   isFxBaseCurrencyCollateralCurrency,
                                                   isBasisOnFxBaseCurrencyLeg):
        vars = CommonVars()

        collateralHandle = vars.baseCcyIdxHandle if isFxBaseCurrencyCollateralCurrency else vars.quoteCcyIdxHandle

        collateralCcyLegEngine = DiscountingSwapEngine(collateralHandle)

        instruments = vars.buildConstantNotionalXccyRateHelpers(
            vars.basisData, collateralHandle,
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg)

        foreignCcyCurve = PiecewiseLogLinearDiscount(
            vars.settlement, instruments, vars.dayCount, LogLinear())
        foreignCcyCurve.enableExtrapolation()
        foreignCcyHandle = YieldTermStructureHandle(foreignCcyCurve)
        foreignCcyLegEngine = DiscountingSwapEngine(foreignCcyHandle)

        tolerance = 1.0e-12

        for i in range(len(vars.basisData)):

            quote = vars.basisData[i]
            xccySwapProxy = vars.buildXccyBasisSwap(
                quote, vars.fxSpot,
                isFxBaseCurrencyCollateralCurrency,
                isBasisOnFxBaseCurrencyLeg)

            if isFxBaseCurrencyCollateralCurrency:
                xccySwapProxy[0].setPricingEngine(collateralCcyLegEngine)
                xccySwapProxy[1].setPricingEngine(foreignCcyLegEngine)
            else:
                xccySwapProxy[0].setPricingEngine(foreignCcyLegEngine)
                xccySwapProxy[1].setPricingEngine(collateralCcyLegEngine)

            p = quote.n * quote.units

            baseCcyLegNpv = vars.fxSpot * xccySwapProxy[0].NPV()
            quoteCcyLegNpv = xccySwapProxy[1].NPV()
            npv = baseCcyLegNpv + quoteCcyLegNpv

            self.assertFalse(abs(npv) > tolerance)

    def _testResettingCrossCurrencySwaps(self,
                                         isFxBaseCurrencyCollateralCurrency,
                                         isBasisOnFxBaseCurrencyLeg,
                                         isFxBaseCurrencyLegResettable):
        vars = CommonVars()

        collateralHandle = vars.baseCcyIdxHandle if isFxBaseCurrencyCollateralCurrency else vars.quoteCcyIdxHandle

        resettingInstruments = vars.buildResettingXccyRateHelpers(
            vars.basisData, collateralHandle, isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg, isFxBaseCurrencyLegResettable)

        constNotionalInstruments = vars.buildConstantNotionalXccyRateHelpers(
            vars.basisData, collateralHandle,
            isFxBaseCurrencyCollateralCurrency,
            isBasisOnFxBaseCurrencyLeg)

        resettingCurve = PiecewiseLogLinearDiscount(
            vars.settlement, resettingInstruments, vars.dayCount, LogLinear())
        resettingCurve.enableExtrapolation()

        constNotionalCurve = PiecewiseLogLinearDiscount(
            vars.settlement, constNotionalInstruments, vars.dayCount, LogLinear())
        constNotionalCurve.enableExtrapolation()

        tolerance = 1.0e-4 * 5
        numberOfInstruments = len(vars.basisData)

        for i in range(numberOfInstruments):
            maturity = resettingInstruments[i].maturityDate()
            resettingZero = resettingCurve.zeroRate(
                maturity, vars.dayCount, Continuous)
            constNotionalZero = constNotionalCurve.zeroRate(
                maturity, vars.dayCount, Continuous)

            self.assertFalse(
                abs(resettingZero.rate() - constNotionalZero.rate()) > tolerance)
