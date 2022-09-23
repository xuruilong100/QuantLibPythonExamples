import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.backup = SavedSettings()
        self.swapSettlementDays = 2
        self.faceAmount = 100.0
        self.fixedConvention = Unadjusted
        self.compounding = Continuous
        self.fixedFrequency = Annual
        self.floatingFrequency = Semiannual
        self.today = Date(24, April, 2007)
        Settings.instance().evaluationDate = self.today
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.termStructure.linkTo(flatRate(self.today, 0.05, Actual365Fixed()))
        self.iborIndex = Euribor(Period(self.floatingFrequency), self.termStructure)
        self.calendar = self.iborIndex.fixingCalendar()
        self.swapIndex = SwapIndex(
            "EuriborSwapIsdaFixA", Period(10, Years), self.swapSettlementDays,
            self.iborIndex.currency(), self.calendar,
            Period(self.fixedFrequency), self.fixedConvention,
            self.iborIndex.dayCounter(), self.iborIndex)
        self.spread = 0.0
        self.nonnullspread = 0.003

        self.pricer = BlackIborCouponPricer()
        self.swaptionVolatilityStructure = SwaptionVolatilityStructureHandle(
            ConstantSwaptionVolatility(
                self.today, NullCalendar(), Following,
                0.2, Actual365Fixed()))
        self.meanReversionQuote = QuoteHandle(SimpleQuote(0.01))
        self.cmspricer = AnalyticHaganPricer(
            self.swaptionVolatilityStructure,
            GFunctionFactory.Standard,
            self.meanReversionQuote)

    def cleanUp(self):
        IndexManager.instance().clearHistories()


class AssetSwapTest(unittest.TestCase):

    def testConsistency(self):
        TEST_MESSAGE(
            "Testing consistency between fair price and fair spread...")

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3

        bondSchedule = Schedule(
            Date(4, January, 2005),
            Date(4, January, 2037),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        bond = FixedRateBond(
            settlementDays, vars.faceAmount,
            bondSchedule,
            DoubleVector(1, 0.04),
            ActualActual(ActualActual.ISDA),
            Following,
            100.0, Date(4, January, 2005))

        payFixedRate = true
        bondPrice = 95.0

        isPar = true
        parAssetSwap = AssetSwap(
            payFixedRate,
            bond, bondPrice,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)

        swapEngine = DiscountingSwapEngine(
            vars.termStructure,
            true,
            bond.settlementDate(),
            Settings.instance().evaluationDate)

        parAssetSwap.setPricingEngine(swapEngine)
        fairCleanPrice = parAssetSwap.fairCleanPrice()
        fairSpread = parAssetSwap.fairSpread()

        tolerance = 1.0e-13

        assetSwap2 = AssetSwap(
            payFixedRate,
            bond, fairCleanPrice,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)
        assetSwap2.setPricingEngine(swapEngine)
        self.assertFalse(abs(assetSwap2.NPV()) > tolerance)
        self.assertFalse(abs(assetSwap2.fairCleanPrice() - fairCleanPrice) > tolerance)
        self.assertFalse(abs(assetSwap2.fairSpread() - vars.spread) > tolerance)

        assetSwap3 = AssetSwap(
            payFixedRate,
            bond, bondPrice,
            vars.iborIndex, fairSpread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)
        assetSwap3.setPricingEngine(swapEngine)
        self.assertFalse(abs(assetSwap3.NPV()) > tolerance)
        self.assertFalse(abs(assetSwap3.fairCleanPrice() - bondPrice) > tolerance)
        self.assertFalse(abs(assetSwap3.fairSpread() - fairSpread) > tolerance)

        swapEngine = DiscountingSwapEngine(
            vars.termStructure,
            true,
            bond.settlementDate(),
            bond.settlementDate())

        parAssetSwap.setPricingEngine(swapEngine)
        self.assertFalse(abs(parAssetSwap.fairCleanPrice() - fairCleanPrice) > tolerance)
        self.assertFalse(abs(parAssetSwap.fairSpread() - fairSpread) > tolerance)

        assetSwap2 = AssetSwap(
            payFixedRate,
            bond, fairCleanPrice,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)
        assetSwap2.setPricingEngine(swapEngine)
        self.assertFalse(abs(assetSwap2.NPV()) > tolerance)
        self.assertFalse(abs(assetSwap2.fairCleanPrice() - fairCleanPrice) > tolerance)
        self.assertFalse(abs(assetSwap2.fairSpread() - vars.spread) > tolerance)

        assetSwap3 = AssetSwap(
            payFixedRate,
            bond, bondPrice,
            vars.iborIndex, fairSpread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)
        assetSwap3.setPricingEngine(swapEngine)
        self.assertFalse(abs(assetSwap3.NPV()) > tolerance)
        self.assertFalse(abs(assetSwap3.fairCleanPrice() - bondPrice) > tolerance)
        self.assertFalse(abs(assetSwap3.fairSpread() - fairSpread) > tolerance)

        isPar = false
        mktAssetSwap = AssetSwap(
            payFixedRate,
            bond, bondPrice,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)

        swapEngine = DiscountingSwapEngine(
            vars.termStructure,
            true,
            bond.settlementDate(),
            Settings.instance().evaluationDate)

        mktAssetSwap.setPricingEngine(swapEngine)
        fairCleanPrice = mktAssetSwap.fairCleanPrice()
        fairSpread = mktAssetSwap.fairSpread()

        assetSwap4 = AssetSwap(
            payFixedRate,
            bond, fairCleanPrice,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)
        assetSwap4.setPricingEngine(swapEngine)
        self.assertFalse(abs(assetSwap4.NPV()) > tolerance)
        self.assertFalse(abs(assetSwap4.fairCleanPrice() - fairCleanPrice) > tolerance)
        self.assertFalse(abs(assetSwap4.fairSpread() - vars.spread) > tolerance)

        assetSwap5 = AssetSwap(
            payFixedRate,
            bond, bondPrice,
            vars.iborIndex, fairSpread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)
        assetSwap5.setPricingEngine(swapEngine)
        self.assertFalse(abs(assetSwap5.NPV()) > tolerance)
        self.assertFalse(abs(assetSwap5.fairCleanPrice() - bondPrice) > tolerance)
        self.assertFalse(abs(assetSwap5.fairSpread() - fairSpread) > tolerance)

        swapEngine = DiscountingSwapEngine(
            vars.termStructure,
            true,
            bond.settlementDate(),
            bond.settlementDate())

        mktAssetSwap.setPricingEngine(swapEngine)
        self.assertFalse(abs(mktAssetSwap.fairCleanPrice() - fairCleanPrice) > tolerance)
        self.assertFalse(abs(mktAssetSwap.fairSpread() - fairSpread) > tolerance)

        assetSwap4 = AssetSwap(
            payFixedRate,
            bond, fairCleanPrice,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)
        assetSwap4.setPricingEngine(swapEngine)
        self.assertFalse(abs(assetSwap4.NPV()) > tolerance)
        self.assertFalse(abs(assetSwap4.fairCleanPrice() - fairCleanPrice) > tolerance)
        self.assertFalse(abs(assetSwap4.fairSpread() - vars.spread) > tolerance)

        assetSwap5 = AssetSwap(
            payFixedRate,
            bond, bondPrice,
            vars.iborIndex, fairSpread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            isPar)
        assetSwap5.setPricingEngine(swapEngine)
        self.assertFalse(abs(assetSwap5.NPV()) > tolerance)
        self.assertFalse(abs(assetSwap5.fairCleanPrice() - bondPrice) > tolerance)
        self.assertFalse(abs(assetSwap5.fairSpread() - fairSpread) > tolerance)

        vars.cleanUp()

    def testImpliedValue(self):
        TEST_MESSAGE(
            "Testing implied bond value against asset-swap fair"
            " price with null spread...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3
        fixingDays = 2
        payFixedRate = true
        parAssetSwap = true
        inArrears = false

        fixedBondSchedule1 = Schedule(
            Date(4, January, 2005),
            Date(4, January, 2037),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBond1 = FixedRateBond(
            settlementDays, vars.faceAmount,
            fixedBondSchedule1,
            DoubleVector(1, 0.04),
            ActualActual(ActualActual.ISDA),
            Following,
            100.0, Date(4, January, 2005))

        bondEngine = DiscountingBondEngine(vars.termStructure)
        swapEngine = DiscountingSwapEngine(vars.termStructure)
        fixedBond1.setPricingEngine(bondEngine)

        fixedBondPrice1 = fixedBond1.cleanPrice()
        fixedBondAssetSwap1 = AssetSwap(
            payFixedRate,
            fixedBond1, fixedBondPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondAssetSwap1.setPricingEngine(swapEngine)
        fixedBondAssetSwapPrice1 = fixedBondAssetSwap1.fairCleanPrice()
        tolerance = 1.0e-13

        tolerance2 = 1.0e-13 if usingAtParCoupons else 1.0e-2

        error1 = abs(fixedBondAssetSwapPrice1 - fixedBondPrice1)

        self.assertFalse(error1 > tolerance2)

        fixedBondSchedule2 = Schedule(
            Date(5, February, 2005),
            Date(5, February, 2019),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBond2 = FixedRateBond(
            settlementDays, vars.faceAmount,
            fixedBondSchedule2,
            DoubleVector(1, 0.05),
            Thirty360(Thirty360.BondBasis),
            Following,
            100.0, Date(5, February, 2005))

        fixedBond2.setPricingEngine(bondEngine)

        fixedBondPrice2 = fixedBond2.cleanPrice()
        fixedBondAssetSwap2 = AssetSwap(
            payFixedRate,
            fixedBond2, fixedBondPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondAssetSwap2.setPricingEngine(swapEngine)
        fixedBondAssetSwapPrice2 = fixedBondAssetSwap2.fairCleanPrice()
        error2 = abs(fixedBondAssetSwapPrice2 - fixedBondPrice2)

        self.assertFalse(error2 > tolerance2)

        floatingBondSchedule1 = Schedule(
            Date(29, September, 2003),
            Date(29, September, 2013),
            Period(Semiannual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)

        floatingBond1 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule1,
            vars.iborIndex, Actual360(),
            Following, fixingDays,
            DoubleVector(1, 1),
            DoubleVector(1, 0.0056),
            DoubleVector(),
            DoubleVector(),
            inArrears,
            100.0, Date(29, September, 2003))

        floatingBond1.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond1.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(27, March, 2007), 0.0402)
        floatingBondPrice1 = floatingBond1.cleanPrice()
        floatingBondAssetSwap1 = AssetSwap(
            payFixedRate,
            floatingBond1, floatingBondPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondAssetSwap1.setPricingEngine(swapEngine)
        floatingBondAssetSwapPrice1 = floatingBondAssetSwap1.fairCleanPrice()
        error3 = abs(floatingBondAssetSwapPrice1 - floatingBondPrice1)

        self.assertFalse(error3 > tolerance2)

        floatingBondSchedule2 = Schedule(
            Date(24, September, 2004),
            Date(24, September, 2018),
            Period(Semiannual), bondCalendar,
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)
        floatingBond2 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule2,
            vars.iborIndex, Actual360(),
            ModifiedFollowing, fixingDays,
            DoubleVector(1, 1),
            DoubleVector(1, 0.0025),
            DoubleVector(),
            DoubleVector(),
            inArrears,
            100.0, Date(24, September, 2004))

        floatingBond2.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond2.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(22, March, 2007), 0.04013)
        currentCoupon = 0.04013 + 0.0025
        floatingCurrentCoupon = floatingBond2.nextCouponRate()
        error4 = abs(floatingCurrentCoupon - currentCoupon)
        self.assertFalse(error4 > tolerance)

        floatingBondPrice2 = floatingBond2.cleanPrice()
        floatingBondAssetSwap2 = AssetSwap(
            payFixedRate,
            floatingBond2, floatingBondPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondAssetSwap2.setPricingEngine(swapEngine)
        floatingBondAssetSwapPrice2 = floatingBondAssetSwap2.fairCleanPrice()
        error5 = abs(floatingBondAssetSwapPrice2 - floatingBondPrice2)

        self.assertFalse(error5 > tolerance2)

        cmsBondSchedule1 = Schedule(
            Date(22, August, 2005),
            Date(22, August, 2020),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBond1 = CmsRateBond(
            settlementDays, vars.faceAmount,
            cmsBondSchedule1,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 1.0),
            DoubleVector(1, 0.0),
            DoubleVector(1, 0.055),
            DoubleVector(1, 0.025),
            inArrears,
            100.0, Date(22, August, 2005))

        cmsBond1.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond1.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(18, August, 2006), 0.04158)
        cmsBondPrice1 = cmsBond1.cleanPrice()
        cmsBondAssetSwap1 = AssetSwap(
            payFixedRate,
            cmsBond1, cmsBondPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondAssetSwap1.setPricingEngine(swapEngine)
        cmsBondAssetSwapPrice1 = cmsBondAssetSwap1.fairCleanPrice()
        error6 = abs(cmsBondAssetSwapPrice1 - cmsBondPrice1)

        self.assertFalse(error6 > tolerance2)

        cmsBondSchedule2 = Schedule(
            Date(6, May, 2005),
            Date(6, May, 2015),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBond2 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule2,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 0.84), DoubleVector(1, 0.0),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(6, May, 2005))

        cmsBond2.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond2.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(4, May, 2006), 0.04217)
        cmsBondPrice2 = cmsBond2.cleanPrice()
        cmsBondAssetSwap2 = AssetSwap(
            payFixedRate,
            cmsBond2, cmsBondPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondAssetSwap2.setPricingEngine(swapEngine)
        cmsBondAssetSwapPrice2 = cmsBondAssetSwap2.fairCleanPrice()
        error7 = abs(cmsBondAssetSwapPrice2 - cmsBondPrice2)

        self.assertFalse(error7 > tolerance2)

        zeroCpnBond1 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(20, December, 2015),
            Following,
            100.0, Date(19, December, 1985))

        zeroCpnBond1.setPricingEngine(bondEngine)

        zeroCpnBondPrice1 = zeroCpnBond1.cleanPrice()
        zeroCpnAssetSwap1 = AssetSwap(
            payFixedRate,
            zeroCpnBond1, zeroCpnBondPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnAssetSwap1.setPricingEngine(swapEngine)
        zeroCpnBondAssetSwapPrice1 = zeroCpnAssetSwap1.fairCleanPrice()
        error8 = abs(cmsBondAssetSwapPrice1 - cmsBondPrice1)

        self.assertFalse(error8 > tolerance2)

        zeroCpnBond2 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(17, February, 2028),
            Following,
            100.0, Date(17, February, 1998))

        zeroCpnBond2.setPricingEngine(bondEngine)

        zeroCpnBondPrice2 = zeroCpnBond2.cleanPrice()
        zeroCpnAssetSwap2 = AssetSwap(
            payFixedRate,
            zeroCpnBond2, zeroCpnBondPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnAssetSwap2.setPricingEngine(swapEngine)
        zeroCpnBondAssetSwapPrice2 = zeroCpnAssetSwap2.fairCleanPrice()
        error9 = abs(cmsBondAssetSwapPrice2 - cmsBondPrice2)

        self.assertFalse(error9 > tolerance2)

        vars.cleanUp()

    def testMarketASWSpread(self):
        TEST_MESSAGE(
            "Testing relationship between market asset swap"
            " and par asset swap...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3
        fixingDays = 2
        payFixedRate = true
        parAssetSwap = true
        mktAssetSwap = false
        inArrears = false

        fixedBondSchedule1 = Schedule(
            Date(4, January, 2005),
            Date(4, January, 2037),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBond1 = FixedRateBond(
            settlementDays, vars.faceAmount, fixedBondSchedule1,
            DoubleVector(1, 0.04),
            ActualActual(ActualActual.ISDA), Following,
            100.0, Date(4, January, 2005))

        bondEngine = DiscountingBondEngine(vars.termStructure)
        swapEngine = DiscountingSwapEngine(vars.termStructure)
        fixedBond1.setPricingEngine(bondEngine)

        fixedBondMktPrice1 = 89.22
        fixedBondMktFullPrice1 = fixedBondMktPrice1 + fixedBond1.accruedAmount()
        fixedBondParAssetSwap1 = AssetSwap(
            payFixedRate,
            fixedBond1, fixedBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondParAssetSwap1.setPricingEngine(swapEngine)
        fixedBondParAssetSwapSpread1 = fixedBondParAssetSwap1.fairSpread()
        fixedBondMktAssetSwap1 = AssetSwap(
            payFixedRate,
            fixedBond1, fixedBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        fixedBondMktAssetSwap1.setPricingEngine(swapEngine)
        fixedBondMktAssetSwapSpread1 = fixedBondMktAssetSwap1.fairSpread()

        tolerance2 = 1.0e-13 if usingAtParCoupons else 1.0e-4

        error1 = abs(fixedBondMktAssetSwapSpread1 - 100 * fixedBondParAssetSwapSpread1 / fixedBondMktFullPrice1)

        self.assertFalse(error1 > tolerance2)

        fixedBondSchedule2 = Schedule(
            Date(5, February, 2005),
            Date(5, February, 2019),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBond2 = FixedRateBond(
            settlementDays, vars.faceAmount, fixedBondSchedule2,
            DoubleVector(1, 0.05),
            Thirty360(Thirty360.BondBasis), Following,
            100.0, Date(5, February, 2005))

        fixedBond2.setPricingEngine(bondEngine)

        fixedBondMktPrice2 = 99.98
        fixedBondMktFullPrice2 = fixedBondMktPrice2 + fixedBond2.accruedAmount()
        fixedBondParAssetSwap2 = AssetSwap(
            payFixedRate,
            fixedBond2, fixedBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondParAssetSwap2.setPricingEngine(swapEngine)
        fixedBondParAssetSwapSpread2 = fixedBondParAssetSwap2.fairSpread()
        fixedBondMktAssetSwap2 = AssetSwap(
            payFixedRate,
            fixedBond2, fixedBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        fixedBondMktAssetSwap2.setPricingEngine(swapEngine)
        fixedBondMktAssetSwapSpread2 = fixedBondMktAssetSwap2.fairSpread()
        error2 = abs(fixedBondMktAssetSwapSpread2 - 100 * fixedBondParAssetSwapSpread2 / fixedBondMktFullPrice2)

        self.assertFalse(error2 > tolerance2)

        floatingBondSchedule1 = Schedule(
            Date(29, September, 2003),
            Date(29, September, 2013),
            Period(Semiannual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)

        floatingBond1 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule1,
            vars.iborIndex, Actual360(),
            Following, fixingDays,
            DoubleVector(1, 1), DoubleVector(1, 0.0056),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(29, September, 2003))

        floatingBond1.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond1.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(27, March, 2007), 0.0402)
        floatingBondMktPrice1 = 101.64
        floatingBondMktFullPrice1 = floatingBondMktPrice1 + floatingBond1.accruedAmount()
        floatingBondParAssetSwap1 = AssetSwap(
            payFixedRate,
            floatingBond1, floatingBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondParAssetSwap1.setPricingEngine(swapEngine)
        floatingBondParAssetSwapSpread1 = floatingBondParAssetSwap1.fairSpread()
        floatingBondMktAssetSwap1 = AssetSwap(
            payFixedRate,
            floatingBond1, floatingBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        floatingBondMktAssetSwap1.setPricingEngine(swapEngine)
        floatingBondMktAssetSwapSpread1 = floatingBondMktAssetSwap1.fairSpread()
        error3 = abs(floatingBondMktAssetSwapSpread1 - 100 * floatingBondParAssetSwapSpread1 / floatingBondMktFullPrice1)

        self.assertFalse(error3 > tolerance2)

        floatingBondSchedule2 = Schedule(
            Date(24, September, 2004),
            Date(24, September, 2018),
            Period(Semiannual), bondCalendar,
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)
        floatingBond2 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule2,
            vars.iborIndex, Actual360(),
            ModifiedFollowing, fixingDays,
            DoubleVector(1, 1), DoubleVector(1, 0.0025),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(24, September, 2004))

        floatingBond2.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond2.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(22, March, 2007), 0.04013)

        floatingBondMktPrice2 = 101.248
        floatingBondMktFullPrice2 = floatingBondMktPrice2 + floatingBond2.accruedAmount()
        floatingBondParAssetSwap2 = AssetSwap(
            payFixedRate,
            floatingBond2, floatingBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondParAssetSwap2.setPricingEngine(swapEngine)
        floatingBondParAssetSwapSpread2 = floatingBondParAssetSwap2.fairSpread()
        floatingBondMktAssetSwap2 = AssetSwap(
            payFixedRate,
            floatingBond2, floatingBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        floatingBondMktAssetSwap2.setPricingEngine(swapEngine)
        floatingBondMktAssetSwapSpread2 = floatingBondMktAssetSwap2.fairSpread()
        error4 = abs(floatingBondMktAssetSwapSpread2 - 100 * floatingBondParAssetSwapSpread2 / floatingBondMktFullPrice2)

        self.assertFalse(error4 > tolerance2)

        cmsBondSchedule1 = Schedule(
            Date(22, August, 2005),
            Date(22, August, 2020),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBond1 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule1,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 1.0), DoubleVector(1, 0.0),
            DoubleVector(1, 0.055), DoubleVector(1, 0.025),
            inArrears,
            100.0, Date(22, August, 2005))

        cmsBond1.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond1.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(18, August, 2006), 0.04158)
        cmsBondMktPrice1 = 88.45
        cmsBondMktFullPrice1 = cmsBondMktPrice1 + cmsBond1.accruedAmount()
        cmsBondParAssetSwap1 = AssetSwap(
            payFixedRate,
            cmsBond1, cmsBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondParAssetSwap1.setPricingEngine(swapEngine)
        cmsBondParAssetSwapSpread1 = cmsBondParAssetSwap1.fairSpread()
        cmsBondMktAssetSwap1 = AssetSwap(
            payFixedRate,
            cmsBond1, cmsBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        cmsBondMktAssetSwap1.setPricingEngine(swapEngine)
        cmsBondMktAssetSwapSpread1 = cmsBondMktAssetSwap1.fairSpread()
        error5 = abs(cmsBondMktAssetSwapSpread1 - 100 * cmsBondParAssetSwapSpread1 / cmsBondMktFullPrice1)

        self.assertFalse(error5 > tolerance2)

        cmsBondSchedule2 = Schedule(
            Date(6, May, 2005),
            Date(6, May, 2015),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBond2 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule2,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 0.84), DoubleVector(1, 0.0),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(6, May, 2005))

        cmsBond2.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond2.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(4, May, 2006), 0.04217)
        cmsBondMktPrice2 = 94.08
        cmsBondMktFullPrice2 = cmsBondMktPrice2 + cmsBond2.accruedAmount()
        cmsBondParAssetSwap2 = AssetSwap(
            payFixedRate,
            cmsBond2, cmsBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondParAssetSwap2.setPricingEngine(swapEngine)
        cmsBondParAssetSwapSpread2 = cmsBondParAssetSwap2.fairSpread()
        cmsBondMktAssetSwap2 = AssetSwap(
            payFixedRate,
            cmsBond2, cmsBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        cmsBondMktAssetSwap2.setPricingEngine(swapEngine)
        cmsBondMktAssetSwapSpread2 = cmsBondMktAssetSwap2.fairSpread()
        error6 = abs(cmsBondMktAssetSwapSpread2 - 100 * cmsBondParAssetSwapSpread2 / cmsBondMktFullPrice2)

        self.assertFalse(error6 > tolerance2)

        zeroCpnBond1 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(20, December, 2015),
            Following,
            100.0, Date(19, December, 1985))

        zeroCpnBond1.setPricingEngine(bondEngine)

        zeroCpnBondMktPrice1 = 70.436
        zeroCpnBondMktFullPrice1 = zeroCpnBondMktPrice1 + zeroCpnBond1.accruedAmount()
        zeroCpnBondParAssetSwap1 = AssetSwap(
            payFixedRate, zeroCpnBond1,
            zeroCpnBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnBondParAssetSwap1.setPricingEngine(swapEngine)
        zeroCpnBondParAssetSwapSpread1 = zeroCpnBondParAssetSwap1.fairSpread()
        zeroCpnBondMktAssetSwap1 = AssetSwap(
            payFixedRate, zeroCpnBond1,
            zeroCpnBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        zeroCpnBondMktAssetSwap1.setPricingEngine(swapEngine)
        zeroCpnBondMktAssetSwapSpread1 = zeroCpnBondMktAssetSwap1.fairSpread()
        error7 = abs(zeroCpnBondMktAssetSwapSpread1 - 100 * zeroCpnBondParAssetSwapSpread1 / zeroCpnBondMktFullPrice1)

        self.assertFalse(error7 > tolerance2)

        zeroCpnBond2 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(17, February, 2028),
            Following,
            100.0, Date(17, February, 1998))

        zeroCpnBond2.setPricingEngine(bondEngine)

        zeroCpnBondMktPrice2 = 35.160
        zeroCpnBondMktFullPrice2 = zeroCpnBondMktPrice2 + zeroCpnBond2.accruedAmount()
        zeroCpnBondParAssetSwap2 = AssetSwap(
            payFixedRate, zeroCpnBond2,
            zeroCpnBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnBondParAssetSwap2.setPricingEngine(swapEngine)
        zeroCpnBondParAssetSwapSpread2 = zeroCpnBondParAssetSwap2.fairSpread()
        zeroCpnBondMktAssetSwap2 = AssetSwap(
            payFixedRate, zeroCpnBond2,
            zeroCpnBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        zeroCpnBondMktAssetSwap2.setPricingEngine(swapEngine)
        zeroCpnBondMktAssetSwapSpread2 = zeroCpnBondMktAssetSwap2.fairSpread()
        error8 = abs(zeroCpnBondMktAssetSwapSpread2 - 100 * zeroCpnBondParAssetSwapSpread2 / zeroCpnBondMktFullPrice2)

        self.assertFalse(error8 > tolerance2)

        vars.cleanUp()

    def testZSpread(self):
        TEST_MESSAGE(
            "Testing clean and dirty price with null Z-spread "
            "against theoretical prices...")

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3
        fixingDays = 2
        inArrears = false

        fixedBondSchedule1 = Schedule(
            Date(4, January, 2005),
            Date(4, January, 2037),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBond1 = FixedRateBond(
            settlementDays, vars.faceAmount, fixedBondSchedule1,
            DoubleVector(1, 0.04),
            ActualActual(ActualActual.ISDA), Following,
            100.0, Date(4, January, 2005))

        bondEngine = DiscountingBondEngine(vars.termStructure)
        fixedBond1.setPricingEngine(bondEngine)

        fixedBondImpliedValue1 = fixedBond1.cleanPrice()
        fixedBondSettlementDate1 = fixedBond1.settlementDate()

        fixedBondCleanPrice1 = BondFunctions.cleanPrice(
            fixedBond1, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Annual,
            fixedBondSettlementDate1)
        tolerance = 1.0e-13
        error1 = abs(fixedBondImpliedValue1 - fixedBondCleanPrice1)
        self.assertFalse(error1 > tolerance)

        fixedBondSchedule2 = Schedule(
            Date(5, February, 2005),
            Date(5, February, 2019),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBond2 = FixedRateBond(
            settlementDays, vars.faceAmount, fixedBondSchedule2,
            DoubleVector(1, 0.05),
            Thirty360(Thirty360.BondBasis), Following,
            100.0, Date(5, February, 2005))

        fixedBond2.setPricingEngine(bondEngine)

        fixedBondImpliedValue2 = fixedBond2.cleanPrice()
        fixedBondSettlementDate2 = fixedBond2.settlementDate()

        fixedBondCleanPrice2 = BondFunctions.cleanPrice(
            fixedBond2, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Annual,
            fixedBondSettlementDate2)
        error3 = abs(fixedBondImpliedValue2 - fixedBondCleanPrice2)
        self.assertFalse(error3 > tolerance)

        floatingBondSchedule1 = Schedule(
            Date(29, September, 2003),
            Date(29, September, 2013),
            Period(Semiannual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)

        floatingBond1 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule1,
            vars.iborIndex, Actual360(),
            Following, fixingDays,
            DoubleVector(1, 1), DoubleVector(1, 0.0056),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(29, September, 2003))

        floatingBond1.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond1.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(27, March, 2007), 0.0402)
        floatingBondImpliedValue1 = floatingBond1.cleanPrice()

        floatingBondCleanPrice1 = BondFunctions.cleanPrice(
            floatingBond1, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Semiannual,
            fixedBondSettlementDate1)
        error5 = abs(floatingBondImpliedValue1 - floatingBondCleanPrice1)
        self.assertFalse(error5 > tolerance)

        floatingBondSchedule2 = Schedule(
            Date(24, September, 2004),
            Date(24, September, 2018),
            Period(Semiannual), bondCalendar,
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)
        floatingBond2 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule2,
            vars.iborIndex, Actual360(),
            ModifiedFollowing, fixingDays,
            DoubleVector(1, 1), DoubleVector(1, 0.0025),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(24, September, 2004))

        floatingBond2.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond2.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(22, March, 2007), 0.04013)
        floatingBondImpliedValue2 = floatingBond2.cleanPrice()

        floatingBondCleanPrice2 = BondFunctions.cleanPrice(
            floatingBond2, vars.termStructure.currentLink(),
            vars.spread, Actual365Fixed(), vars.compounding, Semiannual,
            fixedBondSettlementDate1)
        error7 = abs(floatingBondImpliedValue2 - floatingBondCleanPrice2)
        self.assertFalse(error7 > tolerance)

        cmsBondSchedule1 = Schedule(
            Date(22, August, 2005),
            Date(22, August, 2020),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBond1 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule1,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 1.0), DoubleVector(1, 0.0),
            DoubleVector(1, 0.055), DoubleVector(1, 0.025),
            inArrears,
            100.0, Date(22, August, 2005))

        cmsBond1.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond1.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(18, August, 2006), 0.04158)
        cmsBondImpliedValue1 = cmsBond1.cleanPrice()
        cmsBondSettlementDate1 = cmsBond1.settlementDate()

        cmsBondCleanPrice1 = BondFunctions.cleanPrice(
            cmsBond1, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Annual,
            cmsBondSettlementDate1)
        error9 = abs(cmsBondImpliedValue1 - cmsBondCleanPrice1)
        self.assertFalse(error9 > tolerance)

        cmsBondSchedule2 = Schedule(
            Date(6, May, 2005),
            Date(6, May, 2015),
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBond2 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule2,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 0.84), DoubleVector(1, 0.0),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(6, May, 2005))

        cmsBond2.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond2.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(4, May, 2006), 0.04217)
        cmsBondImpliedValue2 = cmsBond2.cleanPrice()
        cmsBondSettlementDate2 = cmsBond2.settlementDate()

        cmsBondCleanPrice2 = BondFunctions.cleanPrice(
            cmsBond2, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Annual,
            cmsBondSettlementDate2)
        error11 = abs(cmsBondImpliedValue2 - cmsBondCleanPrice2)
        self.assertFalse(error11 > tolerance)

        zeroCpnBond1 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(20, December, 2015),
            Following,
            100.0, Date(19, December, 1985))

        zeroCpnBond1.setPricingEngine(bondEngine)

        zeroCpnBondImpliedValue1 = zeroCpnBond1.cleanPrice()
        zeroCpnBondSettlementDate1 = zeroCpnBond1.settlementDate()

        zeroCpnBondCleanPrice1 = BondFunctions.cleanPrice(
            zeroCpnBond1,
            vars.termStructure.currentLink(),
            vars.spread,
            Actual365Fixed(),
            vars.compounding, Annual,
            zeroCpnBondSettlementDate1)
        error13 = abs(zeroCpnBondImpliedValue1 - zeroCpnBondCleanPrice1)
        self.assertFalse(error13 > tolerance)

        zeroCpnBond2 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(17, February, 2028),
            Following,
            100.0, Date(17, February, 1998))

        zeroCpnBond2.setPricingEngine(bondEngine)

        zeroCpnBondImpliedValue2 = zeroCpnBond2.cleanPrice()
        zeroCpnBondSettlementDate2 = zeroCpnBond2.settlementDate()

        zeroCpnBondCleanPrice2 = BondFunctions.cleanPrice(
            zeroCpnBond2,
            vars.termStructure.currentLink(),
            vars.spread,
            Actual365Fixed(),
            vars.compounding, Annual,
            zeroCpnBondSettlementDate2)
        error15 = abs(zeroCpnBondImpliedValue2 - zeroCpnBondCleanPrice2)
        self.assertFalse(error15 > tolerance)
        vars.cleanUp()

    def testGenericBondImplied(self):
        TEST_MESSAGE(
            "Testing implied generic-bond value against"
            " asset-swap fair price with null spread...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3
        fixingDays = 2
        payFixedRate = true
        parAssetSwap = true
        inArrears = false

        fixedBondStartDate1 = Date(4, January, 2005)
        fixedBondMaturityDate1 = Date(4, January, 2037)
        fixedBondSchedule1 = Schedule(
            fixedBondStartDate1,
            fixedBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg1 = FixedRateLeg(fixedBondSchedule1)
        fixedBondLeg1.withNotionals(vars.faceAmount)
        fixedBondLeg1.withCouponRates(0.04, ActualActual(ActualActual.ISDA))
        fixedBondLeg1 = fixedBondLeg1.makeLeg()
        fixedbondRedemption1 = bondCalendar.adjust(fixedBondMaturityDate1, Following)
        fixedBondLeg1 = [l for l in fixedBondLeg1]
        fixedBondLeg1.append(
            SimpleCashFlow(100.0, fixedbondRedemption1))
        fixedBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate1, fixedBondStartDate1,
            fixedBondLeg1)
        bondEngine = DiscountingBondEngine(vars.termStructure)
        swapEngine = DiscountingSwapEngine(vars.termStructure)
        fixedBond1.setPricingEngine(bondEngine)

        fixedBondPrice1 = fixedBond1.cleanPrice()
        fixedBondAssetSwap1 = AssetSwap(
            payFixedRate,
            fixedBond1, fixedBondPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondAssetSwap1.setPricingEngine(swapEngine)
        fixedBondAssetSwapPrice1 = fixedBondAssetSwap1.fairCleanPrice()
        tolerance = 1.0e-13

        tolerance2 = 1.0e-13 if usingAtParCoupons else 1.0e-2

        error1 = abs(fixedBondAssetSwapPrice1 - fixedBondPrice1)

        self.assertFalse(error1 > tolerance2)

        fixedBondStartDate2 = Date(5, February, 2005)
        fixedBondMaturityDate2 = Date(5, February, 2019)
        fixedBondSchedule2 = Schedule(
            fixedBondStartDate2,
            fixedBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg2 = FixedRateLeg(fixedBondSchedule2)
        fixedBondLeg2.withNotionals(vars.faceAmount)
        fixedBondLeg2.withCouponRates(0.05, Thirty360(Thirty360.BondBasis))
        fixedBondLeg2 = fixedBondLeg2.makeLeg()
        fixedbondRedemption2 = bondCalendar.adjust(
            fixedBondMaturityDate2,
            Following)
        fixedBondLeg2 = [l for l in fixedBondLeg2]
        fixedBondLeg2.append(
            SimpleCashFlow(100.0, fixedbondRedemption2))
        fixedBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate2, fixedBondStartDate2, fixedBondLeg2)
        fixedBond2.setPricingEngine(bondEngine)

        fixedBondPrice2 = fixedBond2.cleanPrice()
        fixedBondAssetSwap2 = AssetSwap(
            payFixedRate,
            fixedBond2, fixedBondPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondAssetSwap2.setPricingEngine(swapEngine)
        fixedBondAssetSwapPrice2 = fixedBondAssetSwap2.fairCleanPrice()
        error2 = abs(fixedBondAssetSwapPrice2 - fixedBondPrice2)

        self.assertFalse(error2 > tolerance2)

        floatingBondStartDate1 = Date(29, September, 2003)
        floatingBondMaturityDate1 = Date(29, September, 2013)
        floatingBondSchedule1 = Schedule(
            floatingBondStartDate1,
            floatingBondMaturityDate1,
            Period(Semiannual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        floatingBondLeg1 = IborLeg(floatingBondSchedule1, vars.iborIndex)
        floatingBondLeg1.withNotionals(vars.faceAmount)
        floatingBondLeg1.withPaymentDayCounter(Actual360())
        floatingBondLeg1.withFixingDays(fixingDays)
        floatingBondLeg1.withSpreads(0.0056)
        floatingBondLeg1.inArrears(inArrears)
        floatingBondLeg1 = floatingBondLeg1.makeLeg()

        floatingbondRedemption1 = bondCalendar.adjust(
            floatingBondMaturityDate1, Following)
        floatingBondLeg1 = [l for l in floatingBondLeg1]
        floatingBondLeg1.append(
            SimpleCashFlow(100.0, floatingbondRedemption1))
        floatingBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate1, floatingBondStartDate1,
            floatingBondLeg1)
        floatingBond1.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond1.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(27, March, 2007), 0.0402)
        floatingBondPrice1 = floatingBond1.cleanPrice()
        floatingBondAssetSwap1 = AssetSwap(
            payFixedRate,
            floatingBond1, floatingBondPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondAssetSwap1.setPricingEngine(swapEngine)
        floatingBondAssetSwapPrice1 = floatingBondAssetSwap1.fairCleanPrice()
        error3 = abs(floatingBondAssetSwapPrice1 - floatingBondPrice1)

        self.assertFalse(error3 > tolerance2)

        floatingBondStartDate2 = Date(24, September, 2004)
        floatingBondMaturityDate2 = Date(24, September, 2018)
        floatingBondSchedule2 = Schedule(
            floatingBondStartDate2,
            floatingBondMaturityDate2,
            Period(Semiannual), bondCalendar,
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)
        floatingBondLeg2 = IborLeg(floatingBondSchedule2, vars.iborIndex)
        floatingBondLeg2.withNotionals(vars.faceAmount)
        floatingBondLeg2.withPaymentDayCounter(Actual360())
        floatingBondLeg2.withPaymentAdjustment(ModifiedFollowing)
        floatingBondLeg2.withFixingDays(fixingDays)
        floatingBondLeg2.withSpreads(0.0025)
        floatingBondLeg2.inArrears(inArrears)
        floatingBondLeg2 = floatingBondLeg2.makeLeg()
        floatingbondRedemption2 = bondCalendar.adjust(
            floatingBondMaturityDate2, ModifiedFollowing)
        floatingBondLeg2 = [l for l in floatingBondLeg2]
        floatingBondLeg2.append(
            SimpleCashFlow(100.0, floatingbondRedemption2))
        floatingBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate2, floatingBondStartDate2,
            floatingBondLeg2)
        floatingBond2.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond2.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(22, March, 2007), 0.04013)
        currentCoupon = 0.04013 + 0.0025
        floatingCurrentCoupon = floatingBond2.nextCouponRate()
        error4 = abs(floatingCurrentCoupon - currentCoupon)
        self.assertFalse(error4 > tolerance)
        floatingBondPrice2 = floatingBond2.cleanPrice()
        floatingBondAssetSwap2 = AssetSwap(
            payFixedRate,
            floatingBond2, floatingBondPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondAssetSwap2.setPricingEngine(swapEngine)
        floatingBondAssetSwapPrice2 = floatingBondAssetSwap2.fairCleanPrice()
        error5 = abs(floatingBondAssetSwapPrice2 - floatingBondPrice2)

        self.assertFalse(error5 > tolerance2)

        cmsBondStartDate1 = Date(22, August, 2005)
        cmsBondMaturityDate1 = Date(22, August, 2020)
        cmsBondSchedule1 = Schedule(
            cmsBondStartDate1,
            cmsBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg1 = CmsLeg(cmsBondSchedule1, vars.swapIndex)
        cmsBondLeg1.withNotionals(vars.faceAmount)
        cmsBondLeg1.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg1.withFixingDays(fixingDays)
        cmsBondLeg1.withCaps(0.055)
        cmsBondLeg1.withFloors(0.025)
        cmsBondLeg1.inArrears(inArrears)
        cmsBondLeg1 = cmsBondLeg1.makeLeg()
        cmsbondRedemption1 = bondCalendar.adjust(
            cmsBondMaturityDate1, Following)
        cmsBondLeg1 = [l for l in cmsBondLeg1]
        cmsBondLeg1.append(
            SimpleCashFlow(100.0, cmsbondRedemption1))
        cmsBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate1, cmsBondStartDate1, cmsBondLeg1)
        cmsBond1.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond1.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(18, August, 2006), 0.04158)
        cmsBondPrice1 = cmsBond1.cleanPrice()
        cmsBondAssetSwap1 = AssetSwap(
            payFixedRate,
            cmsBond1, cmsBondPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondAssetSwap1.setPricingEngine(swapEngine)
        cmsBondAssetSwapPrice1 = cmsBondAssetSwap1.fairCleanPrice()
        error6 = abs(cmsBondAssetSwapPrice1 - cmsBondPrice1)

        self.assertFalse(error6 > tolerance2)

        cmsBondStartDate2 = Date(6, May, 2005)
        cmsBondMaturityDate2 = Date(6, May, 2015)
        cmsBondSchedule2 = Schedule(
            cmsBondStartDate2,
            cmsBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg2 = CmsLeg(cmsBondSchedule2, vars.swapIndex)
        cmsBondLeg2.withNotionals(vars.faceAmount)
        cmsBondLeg2.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg2.withFixingDays(fixingDays)
        cmsBondLeg2.withGearings(0.84)
        cmsBondLeg2.inArrears(inArrears)
        cmsBondLeg2 = cmsBondLeg2.makeLeg()
        cmsbondRedemption2 = bondCalendar.adjust(
            cmsBondMaturityDate2, Following)
        cmsBondLeg2 = [l for l in cmsBondLeg2]
        cmsBondLeg2.append(
            SimpleCashFlow(100.0, cmsbondRedemption2))
        cmsBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate2, cmsBondStartDate2, cmsBondLeg2)
        cmsBond2.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond2.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(4, May, 2006), 0.04217)
        cmsBondPrice2 = cmsBond2.cleanPrice()
        cmsBondAssetSwap2 = AssetSwap(
            payFixedRate,
            cmsBond2, cmsBondPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondAssetSwap2.setPricingEngine(swapEngine)
        cmsBondAssetSwapPrice2 = cmsBondAssetSwap2.fairCleanPrice()
        error7 = abs(cmsBondAssetSwapPrice2 - cmsBondPrice2)

        self.assertFalse(error7 > tolerance2)

        zeroCpnBondStartDate1 = Date(19, December, 1985)
        zeroCpnBondMaturityDate1 = Date(20, December, 2015)
        zeroCpnBondRedemption1 = bondCalendar.adjust(
            zeroCpnBondMaturityDate1,
            Following)
        zeroCpnBondLeg1 = Leg(1, SimpleCashFlow(100.0, zeroCpnBondRedemption1))
        zeroCpnBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate1, zeroCpnBondStartDate1, zeroCpnBondLeg1)
        zeroCpnBond1.setPricingEngine(bondEngine)

        zeroCpnBondPrice1 = zeroCpnBond1.cleanPrice()
        zeroCpnAssetSwap1 = AssetSwap(
            payFixedRate,
            zeroCpnBond1, zeroCpnBondPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnAssetSwap1.setPricingEngine(swapEngine)
        zeroCpnBondAssetSwapPrice1 = zeroCpnAssetSwap1.fairCleanPrice()
        error8 = abs(zeroCpnBondAssetSwapPrice1 - zeroCpnBondPrice1)

        self.assertFalse(error8 > tolerance2)

        zeroCpnBondStartDate2 = Date(17, February, 1998)
        zeroCpnBondMaturityDate2 = Date(17, February, 2028)
        zerocpbondRedemption2 = bondCalendar.adjust(
            zeroCpnBondMaturityDate2,
            Following)
        zeroCpnBondLeg2 = Leg(1, SimpleCashFlow(100.0, zerocpbondRedemption2))
        zeroCpnBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate2, zeroCpnBondStartDate2, zeroCpnBondLeg2)
        zeroCpnBond2.setPricingEngine(bondEngine)

        zeroCpnBondPrice2 = zeroCpnBond2.cleanPrice()
        zeroCpnAssetSwap2 = AssetSwap(
            payFixedRate,
            zeroCpnBond2, zeroCpnBondPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnAssetSwap2.setPricingEngine(swapEngine)
        zeroCpnBondAssetSwapPrice2 = zeroCpnAssetSwap2.fairCleanPrice()
        error9 = abs(zeroCpnBondAssetSwapPrice2 - zeroCpnBondPrice2)

        self.assertFalse(error9 > tolerance2)
        vars.cleanUp()

    def testMASWWithGenericBond(self):
        TEST_MESSAGE(
            "Testing market asset swap against par asset swap "
            "with generic bond...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3
        fixingDays = 2
        payFixedRate = true
        parAssetSwap = true
        mktAssetSwap = false
        inArrears = false

        fixedBondStartDate1 = Date(4, January, 2005)
        fixedBondMaturityDate1 = Date(4, January, 2037)
        fixedBondSchedule1 = Schedule(
            fixedBondStartDate1,
            fixedBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg1 = FixedRateLeg(fixedBondSchedule1)
        fixedBondLeg1.withNotionals(vars.faceAmount)
        fixedBondLeg1.withCouponRates(0.04, ActualActual(ActualActual.ISDA))
        fixedBondLeg1 = fixedBondLeg1.makeLeg()
        fixedbondRedemption1 = bondCalendar.adjust(
            fixedBondMaturityDate1,
            Following)
        fixedBondLeg1 = [l for l in fixedBondLeg1]
        fixedBondLeg1.append(
            SimpleCashFlow(100.0, fixedbondRedemption1))
        fixedBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate1, fixedBondStartDate1,
            fixedBondLeg1)
        bondEngine = DiscountingBondEngine(vars.termStructure)
        swapEngine = DiscountingSwapEngine(vars.termStructure)
        fixedBond1.setPricingEngine(bondEngine)

        fixedBondMktPrice1 = 89.22
        fixedBondMktFullPrice1 = fixedBondMktPrice1 + fixedBond1.accruedAmount()
        fixedBondParAssetSwap1 = AssetSwap(
            payFixedRate,
            fixedBond1, fixedBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondParAssetSwap1.setPricingEngine(swapEngine)
        fixedBondParAssetSwapSpread1 = fixedBondParAssetSwap1.fairSpread()
        fixedBondMktAssetSwap1 = AssetSwap(
            payFixedRate,
            fixedBond1, fixedBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        fixedBondMktAssetSwap1.setPricingEngine(swapEngine)
        fixedBondMktAssetSwapSpread1 = fixedBondMktAssetSwap1.fairSpread()

        tolerance2 = 1.0e-13 if usingAtParCoupons else 1.0e-4

        error1 = abs(fixedBondMktAssetSwapSpread1 - 100 * fixedBondParAssetSwapSpread1 / fixedBondMktFullPrice1)

        self.assertFalse(error1 > tolerance2)

        fixedBondStartDate2 = Date(5, February, 2005)
        fixedBondMaturityDate2 = Date(5, February, 2019)
        fixedBondSchedule2 = Schedule(
            fixedBondStartDate2,
            fixedBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg2 = FixedRateLeg(fixedBondSchedule2)
        fixedBondLeg2.withNotionals(vars.faceAmount)
        fixedBondLeg2.withCouponRates(0.05, Thirty360(Thirty360.BondBasis))
        fixedBondLeg2 = fixedBondLeg2.makeLeg()
        fixedbondRedemption2 = bondCalendar.adjust(
            fixedBondMaturityDate2,
            Following)
        fixedBondLeg2 = [l for l in fixedBondLeg2]
        fixedBondLeg2.append(
            SimpleCashFlow(100.0, fixedbondRedemption2))
        fixedBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate2, fixedBondStartDate2, fixedBondLeg2)
        fixedBond2.setPricingEngine(bondEngine)

        fixedBondMktPrice2 = 99.98
        fixedBondMktFullPrice2 = fixedBondMktPrice2 + fixedBond2.accruedAmount()
        fixedBondParAssetSwap2 = AssetSwap(
            payFixedRate,
            fixedBond2, fixedBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondParAssetSwap2.setPricingEngine(swapEngine)
        fixedBondParAssetSwapSpread2 = fixedBondParAssetSwap2.fairSpread()
        fixedBondMktAssetSwap2 = AssetSwap(
            payFixedRate,
            fixedBond2, fixedBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        fixedBondMktAssetSwap2.setPricingEngine(swapEngine)
        fixedBondMktAssetSwapSpread2 = fixedBondMktAssetSwap2.fairSpread()
        error2 = abs(fixedBondMktAssetSwapSpread2 -
                     100 * fixedBondParAssetSwapSpread2 / fixedBondMktFullPrice2)

        self.assertFalse(error2 > tolerance2)

        floatingBondStartDate1 = Date(29, September, 2003)
        floatingBondMaturityDate1 = Date(29, September, 2013)
        floatingBondSchedule1 = Schedule(
            floatingBondStartDate1,
            floatingBondMaturityDate1,
            Period(Semiannual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        floatingBondLeg1 = IborLeg(floatingBondSchedule1, vars.iborIndex)
        floatingBondLeg1.withNotionals(vars.faceAmount)
        floatingBondLeg1.withPaymentDayCounter(Actual360())
        floatingBondLeg1.withFixingDays(fixingDays)
        floatingBondLeg1.withSpreads(0.0056)
        floatingBondLeg1.inArrears(inArrears)
        floatingBondLeg1 = floatingBondLeg1.makeLeg()
        floatingbondRedemption1 = bondCalendar.adjust(floatingBondMaturityDate1, Following)
        floatingBondLeg1 = [l for l in floatingBondLeg1]
        floatingBondLeg1.append(
            SimpleCashFlow(100.0, floatingbondRedemption1))
        floatingBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate1, floatingBondStartDate1,
            floatingBondLeg1)
        floatingBond1.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond1.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(27, March, 2007), 0.0402)

        floatingBondMktPrice1 = 101.64
        floatingBondMktFullPrice1 = floatingBondMktPrice1 + floatingBond1.accruedAmount()
        floatingBondParAssetSwap1 = AssetSwap(
            payFixedRate,
            floatingBond1, floatingBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondParAssetSwap1.setPricingEngine(swapEngine)
        floatingBondParAssetSwapSpread1 = floatingBondParAssetSwap1.fairSpread()
        floatingBondMktAssetSwap1 = AssetSwap(
            payFixedRate,
            floatingBond1, floatingBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        floatingBondMktAssetSwap1.setPricingEngine(swapEngine)
        floatingBondMktAssetSwapSpread1 = floatingBondMktAssetSwap1.fairSpread()
        error3 = abs(floatingBondMktAssetSwapSpread1 -
                     100 * floatingBondParAssetSwapSpread1 / floatingBondMktFullPrice1)

        self.assertFalse(error3 > tolerance2)

        floatingBondStartDate2 = Date(24, September, 2004)
        floatingBondMaturityDate2 = Date(24, September, 2018)
        floatingBondSchedule2 = Schedule(
            floatingBondStartDate2,
            floatingBondMaturityDate2,
            Period(Semiannual), bondCalendar,
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)
        floatingBondLeg2 = IborLeg(floatingBondSchedule2, vars.iborIndex)
        floatingBondLeg2.withNotionals(vars.faceAmount)
        floatingBondLeg2.withPaymentDayCounter(Actual360())
        floatingBondLeg2.withPaymentAdjustment(ModifiedFollowing)
        floatingBondLeg2.withFixingDays(fixingDays)
        floatingBondLeg2.withSpreads(0.0025)
        floatingBondLeg2.inArrears(inArrears)
        floatingBondLeg2 = floatingBondLeg2.makeLeg()
        floatingbondRedemption2 = bondCalendar.adjust(floatingBondMaturityDate2, ModifiedFollowing)
        floatingBondLeg2 = [l for l in floatingBondLeg2]
        floatingBondLeg2.append(
            SimpleCashFlow(100.0, floatingbondRedemption2))
        floatingBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate2, floatingBondStartDate2,
            floatingBondLeg2)
        floatingBond2.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond2.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(22, March, 2007), 0.04013)

        floatingBondMktPrice2 = 101.248
        floatingBondMktFullPrice2 = floatingBondMktPrice2 + floatingBond2.accruedAmount()
        floatingBondParAssetSwap2 = AssetSwap(
            payFixedRate,
            floatingBond2, floatingBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondParAssetSwap2.setPricingEngine(swapEngine)
        floatingBondParAssetSwapSpread2 = floatingBondParAssetSwap2.fairSpread()
        floatingBondMktAssetSwap2 = AssetSwap(
            payFixedRate,
            floatingBond2, floatingBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        floatingBondMktAssetSwap2.setPricingEngine(swapEngine)
        floatingBondMktAssetSwapSpread2 = floatingBondMktAssetSwap2.fairSpread()
        error4 = abs(floatingBondMktAssetSwapSpread2 -
                     100 * floatingBondParAssetSwapSpread2 / floatingBondMktFullPrice2)

        self.assertFalse(error4 > tolerance2)

        cmsBondStartDate1 = Date(22, August, 2005)
        cmsBondMaturityDate1 = Date(22, August, 2020)
        cmsBondSchedule1 = Schedule(
            cmsBondStartDate1,
            cmsBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg1 = CmsLeg(cmsBondSchedule1, vars.swapIndex)
        cmsBondLeg1.withNotionals(vars.faceAmount)
        cmsBondLeg1.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg1.withFixingDays(fixingDays)
        cmsBondLeg1.withCaps(0.055)
        cmsBondLeg1.withFloors(0.025)
        cmsBondLeg1.inArrears(inArrears)
        cmsBondLeg1 = cmsBondLeg1.makeLeg()
        cmsbondRedemption1 = bondCalendar.adjust(
            cmsBondMaturityDate1,
            Following)
        cmsBondLeg1 = [l for l in cmsBondLeg1]
        cmsBondLeg1.append(
            SimpleCashFlow(100.0, cmsbondRedemption1))
        cmsBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate1, cmsBondStartDate1, cmsBondLeg1)
        cmsBond1.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond1.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(18, August, 2006), 0.04158)
        cmsBondMktPrice1 = 88.45
        cmsBondMktFullPrice1 = cmsBondMktPrice1 + cmsBond1.accruedAmount()
        cmsBondParAssetSwap1 = AssetSwap(
            payFixedRate,
            cmsBond1, cmsBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondParAssetSwap1.setPricingEngine(swapEngine)
        cmsBondParAssetSwapSpread1 = cmsBondParAssetSwap1.fairSpread()
        cmsBondMktAssetSwap1 = AssetSwap(
            payFixedRate,
            cmsBond1, cmsBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        cmsBondMktAssetSwap1.setPricingEngine(swapEngine)
        cmsBondMktAssetSwapSpread1 = cmsBondMktAssetSwap1.fairSpread()
        error5 = abs(cmsBondMktAssetSwapSpread1 -
                     100 * cmsBondParAssetSwapSpread1 / cmsBondMktFullPrice1)

        self.assertFalse(error5 > tolerance2)

        cmsBondStartDate2 = Date(6, May, 2005)
        cmsBondMaturityDate2 = Date(6, May, 2015)
        cmsBondSchedule2 = Schedule(
            cmsBondStartDate2,
            cmsBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg2 = CmsLeg(cmsBondSchedule2, vars.swapIndex)
        cmsBondLeg2.withNotionals(vars.faceAmount)
        cmsBondLeg2.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg2.withFixingDays(fixingDays)
        cmsBondLeg2.withGearings(0.84)
        cmsBondLeg2.inArrears(inArrears)
        cmsBondLeg2 = cmsBondLeg2.makeLeg()
        cmsbondRedemption2 = bondCalendar.adjust(cmsBondMaturityDate2, Following)
        cmsBondLeg2 = [l for l in cmsBondLeg2]
        cmsBondLeg2.append(
            SimpleCashFlow(100.0, cmsbondRedemption2))
        cmsBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate2, cmsBondStartDate2, cmsBondLeg2)
        cmsBond2.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond2.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(4, May, 2006), 0.04217)
        cmsBondMktPrice2 = 94.08
        cmsBondMktFullPrice2 = cmsBondMktPrice2 + cmsBond2.accruedAmount()
        cmsBondParAssetSwap2 = AssetSwap(
            payFixedRate,
            cmsBond2, cmsBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondParAssetSwap2.setPricingEngine(swapEngine)
        cmsBondParAssetSwapSpread2 = cmsBondParAssetSwap2.fairSpread()
        cmsBondMktAssetSwap2 = AssetSwap(
            payFixedRate,
            cmsBond2, cmsBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        cmsBondMktAssetSwap2.setPricingEngine(swapEngine)
        cmsBondMktAssetSwapSpread2 = cmsBondMktAssetSwap2.fairSpread()
        error6 = abs(cmsBondMktAssetSwapSpread2 -
                     100 * cmsBondParAssetSwapSpread2 / cmsBondMktFullPrice2)

        self.assertFalse(error6 > tolerance2)

        zeroCpnBondStartDate1 = Date(19, December, 1985)
        zeroCpnBondMaturityDate1 = Date(20, December, 2015)
        zeroCpnBondRedemption1 = bondCalendar.adjust(zeroCpnBondMaturityDate1, Following)
        zeroCpnBondLeg1 = Leg(1, SimpleCashFlow(100.0, zeroCpnBondRedemption1))
        zeroCpnBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate1, zeroCpnBondStartDate1, zeroCpnBondLeg1)
        zeroCpnBond1.setPricingEngine(bondEngine)

        zeroCpnBondMktPrice1 = 70.436
        zeroCpnBondMktFullPrice1 = zeroCpnBondMktPrice1 + zeroCpnBond1.accruedAmount()
        zeroCpnBondParAssetSwap1 = AssetSwap(
            payFixedRate, zeroCpnBond1,
            zeroCpnBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnBondParAssetSwap1.setPricingEngine(swapEngine)
        zeroCpnBondParAssetSwapSpread1 = zeroCpnBondParAssetSwap1.fairSpread()
        zeroCpnBondMktAssetSwap1 = AssetSwap(
            payFixedRate, zeroCpnBond1,
            zeroCpnBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        zeroCpnBondMktAssetSwap1.setPricingEngine(swapEngine)
        zeroCpnBondMktAssetSwapSpread1 = zeroCpnBondMktAssetSwap1.fairSpread()
        error7 = abs(zeroCpnBondMktAssetSwapSpread1 -
                     100 * zeroCpnBondParAssetSwapSpread1 / zeroCpnBondMktFullPrice1)

        self.assertFalse(error7 > tolerance2)

        zeroCpnBondStartDate2 = Date(17, February, 1998)
        zeroCpnBondMaturityDate2 = Date(17, February, 2028)
        zerocpbondRedemption2 = bondCalendar.adjust(zeroCpnBondMaturityDate2, Following)
        zeroCpnBondLeg2 = Leg(1, SimpleCashFlow(100.0, zerocpbondRedemption2))
        zeroCpnBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate2, zeroCpnBondStartDate2, zeroCpnBondLeg2)
        zeroCpnBond2.setPricingEngine(bondEngine)

        zeroCpnBondMktPrice2 = 35.160
        zeroCpnBondMktFullPrice2 = zeroCpnBondMktPrice2 + zeroCpnBond2.accruedAmount()
        zeroCpnBondParAssetSwap2 = AssetSwap(
            payFixedRate, zeroCpnBond2,
            zeroCpnBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnBondParAssetSwap2.setPricingEngine(swapEngine)
        zeroCpnBondParAssetSwapSpread2 = zeroCpnBondParAssetSwap2.fairSpread()
        zeroCpnBondMktAssetSwap2 = AssetSwap(
            payFixedRate, zeroCpnBond2,
            zeroCpnBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            mktAssetSwap)
        zeroCpnBondMktAssetSwap2.setPricingEngine(swapEngine)
        zeroCpnBondMktAssetSwapSpread2 = zeroCpnBondMktAssetSwap2.fairSpread()
        error8 = abs(zeroCpnBondMktAssetSwapSpread2 -
                     100 * zeroCpnBondParAssetSwapSpread2 / zeroCpnBondMktFullPrice2)

        self.assertFalse(error8 > tolerance2)
        vars.cleanUp()

    def testZSpreadWithGenericBond(self):
        TEST_MESSAGE(
            "Testing clean and dirty price with null Z-spread "
            "against theoretical prices...")

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3
        fixingDays = 2
        inArrears = false

        fixedBondStartDate1 = Date(4, January, 2005)
        fixedBondMaturityDate1 = Date(4, January, 2037)
        fixedBondSchedule1 = Schedule(
            fixedBondStartDate1,
            fixedBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg1 = FixedRateLeg(fixedBondSchedule1)
        fixedBondLeg1.withNotionals(vars.faceAmount)
        fixedBondLeg1.withCouponRates(0.04, ActualActual(ActualActual.ISDA))
        fixedBondLeg1 = fixedBondLeg1.makeLeg()
        fixedbondRedemption1 = bondCalendar.adjust(
            fixedBondMaturityDate1,
            Following)
        fixedBondLeg1 = [l for l in fixedBondLeg1]
        fixedBondLeg1.append(
            SimpleCashFlow(100.0, fixedbondRedemption1))
        fixedBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate1, fixedBondStartDate1,
            fixedBondLeg1)
        bondEngine = DiscountingBondEngine(vars.termStructure)
        fixedBond1.setPricingEngine(bondEngine)

        fixedBondImpliedValue1 = fixedBond1.cleanPrice()
        fixedBondSettlementDate1 = fixedBond1.settlementDate()

        fixedBondCleanPrice1 = BondFunctions.cleanPrice(
            fixedBond1, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Annual,
            fixedBondSettlementDate1)
        tolerance = 1.0e-13
        error1 = abs(fixedBondImpliedValue1 - fixedBondCleanPrice1)
        self.assertFalse(error1 > tolerance)

        fixedBondStartDate2 = Date(5, February, 2005)
        fixedBondMaturityDate2 = Date(5, February, 2019)
        fixedBondSchedule2 = Schedule(
            fixedBondStartDate2,
            fixedBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg2 = FixedRateLeg(fixedBondSchedule2)
        fixedBondLeg2.withNotionals(vars.faceAmount)
        fixedBondLeg2.withCouponRates(0.05, Thirty360(Thirty360.BondBasis))
        fixedBondLeg2 = fixedBondLeg2.makeLeg()
        fixedbondRedemption2 = bondCalendar.adjust(
            fixedBondMaturityDate2,
            Following)
        fixedBondLeg2 = [l for l in fixedBondLeg2]
        fixedBondLeg2.append(
            SimpleCashFlow(100.0, fixedbondRedemption2))
        fixedBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate2, fixedBondStartDate2, fixedBondLeg2)
        fixedBond2.setPricingEngine(bondEngine)

        fixedBondImpliedValue2 = fixedBond2.cleanPrice()
        fixedBondSettlementDate2 = fixedBond2.settlementDate()

        fixedBondCleanPrice2 = BondFunctions.cleanPrice(
            fixedBond2, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Annual,
            fixedBondSettlementDate2)
        error3 = abs(fixedBondImpliedValue2 - fixedBondCleanPrice2)
        self.assertFalse(error3 > tolerance)

        floatingBondStartDate1 = Date(29, September, 2003)
        floatingBondMaturityDate1 = Date(29, September, 2013)
        floatingBondSchedule1 = Schedule(
            floatingBondStartDate1,
            floatingBondMaturityDate1,
            Period(Semiannual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        floatingBondLeg1 = IborLeg(floatingBondSchedule1, vars.iborIndex)
        floatingBondLeg1.withNotionals(vars.faceAmount)
        floatingBondLeg1.withPaymentDayCounter(Actual360())
        floatingBondLeg1.withFixingDays(fixingDays)
        floatingBondLeg1.withSpreads(0.0056)
        floatingBondLeg1.inArrears(inArrears)
        floatingBondLeg1 = floatingBondLeg1.makeLeg()
        floatingbondRedemption1 = bondCalendar.adjust(floatingBondMaturityDate1, Following)
        floatingBondLeg1 = [l for l in floatingBondLeg1]
        floatingBondLeg1.append(
            SimpleCashFlow(100.0, floatingbondRedemption1))
        floatingBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate1, floatingBondStartDate1,
            floatingBondLeg1)
        floatingBond1.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond1.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(27, March, 2007), 0.0402)
        floatingBondImpliedValue1 = floatingBond1.cleanPrice()

        floatingBondCleanPrice1 = BondFunctions.cleanPrice(
            floatingBond1, vars.termStructure.currentLink(),
            vars.spread, Actual365Fixed(), vars.compounding, Semiannual,
            fixedBondSettlementDate1)
        error5 = abs(floatingBondImpliedValue1 - floatingBondCleanPrice1)
        self.assertFalse(error5 > tolerance)

        floatingBondStartDate2 = Date(24, September, 2004)
        floatingBondMaturityDate2 = Date(24, September, 2018)
        floatingBondSchedule2 = Schedule(
            floatingBondStartDate2,
            floatingBondMaturityDate2,
            Period(Semiannual), bondCalendar,
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)
        floatingBondLeg2 = IborLeg(floatingBondSchedule2, vars.iborIndex)
        floatingBondLeg2.withNotionals(vars.faceAmount)
        floatingBondLeg2.withPaymentDayCounter(Actual360())
        floatingBondLeg2.withPaymentAdjustment(ModifiedFollowing)
        floatingBondLeg2.withFixingDays(fixingDays)
        floatingBondLeg2.withSpreads(0.0025)
        floatingBondLeg2.inArrears(inArrears)
        floatingBondLeg2 = floatingBondLeg2.makeLeg()
        floatingbondRedemption2 = bondCalendar.adjust(
            floatingBondMaturityDate2, ModifiedFollowing)
        floatingBondLeg2 = [l for l in floatingBondLeg2]
        floatingBondLeg2.append(
            SimpleCashFlow(100.0, floatingbondRedemption2))
        floatingBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate2, floatingBondStartDate2,
            floatingBondLeg2)
        floatingBond2.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond2.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(22, March, 2007), 0.04013)
        floatingBondImpliedValue2 = floatingBond2.cleanPrice()

        floatingBondCleanPrice2 = BondFunctions.cleanPrice(
            floatingBond2, vars.termStructure.currentLink(),
            vars.spread, Actual365Fixed(), vars.compounding, Semiannual,
            fixedBondSettlementDate1)
        error7 = abs(floatingBondImpliedValue2 - floatingBondCleanPrice2)
        self.assertFalse(error7 > tolerance)

        cmsBondStartDate1 = Date(22, August, 2005)
        cmsBondMaturityDate1 = Date(22, August, 2020)
        cmsBondSchedule1 = Schedule(
            cmsBondStartDate1,
            cmsBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg1 = CmsLeg(cmsBondSchedule1, vars.swapIndex)
        cmsBondLeg1.withNotionals(vars.faceAmount)
        cmsBondLeg1.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg1.withFixingDays(fixingDays)
        cmsBondLeg1.withCaps(0.055)
        cmsBondLeg1.withFloors(0.025)
        cmsBondLeg1.inArrears(inArrears)
        cmsBondLeg1 = cmsBondLeg1.makeLeg()
        cmsbondRedemption1 = bondCalendar.adjust(cmsBondMaturityDate1, Following)
        cmsBondLeg1 = [l for l in cmsBondLeg1]
        cmsBondLeg1.append(
            SimpleCashFlow(100.0, cmsbondRedemption1))
        cmsBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate1, cmsBondStartDate1, cmsBondLeg1)
        cmsBond1.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond1.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(18, August, 2006), 0.04158)
        cmsBondImpliedValue1 = cmsBond1.cleanPrice()
        cmsBondSettlementDate1 = cmsBond1.settlementDate()

        cmsBondCleanPrice1 = BondFunctions.cleanPrice(
            cmsBond1, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Annual,
            cmsBondSettlementDate1)
        error9 = abs(cmsBondImpliedValue1 - cmsBondCleanPrice1)
        self.assertFalse(error9 > tolerance)

        cmsBondStartDate2 = Date(6, May, 2005)
        cmsBondMaturityDate2 = Date(6, May, 2015)
        cmsBondSchedule2 = Schedule(
            cmsBondStartDate2,
            cmsBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg2 = CmsLeg(cmsBondSchedule2, vars.swapIndex)
        cmsBondLeg2.withNotionals(vars.faceAmount)
        cmsBondLeg2.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg2.withFixingDays(fixingDays)
        cmsBondLeg2.withGearings(0.84)
        cmsBondLeg2.inArrears(inArrears)
        cmsBondLeg2 = cmsBondLeg2.makeLeg()
        cmsbondRedemption2 = bondCalendar.adjust(cmsBondMaturityDate2, Following)
        cmsBondLeg2 = [l for l in cmsBondLeg2]
        cmsBondLeg2.append(
            SimpleCashFlow(100.0, cmsbondRedemption2))
        cmsBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate2, cmsBondStartDate2, cmsBondLeg2)
        cmsBond2.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond2.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(4, May, 2006), 0.04217)
        cmsBondImpliedValue2 = cmsBond2.cleanPrice()
        cmsBondSettlementDate2 = cmsBond2.settlementDate()

        cmsBondCleanPrice2 = BondFunctions.cleanPrice(
            cmsBond2, vars.termStructure.currentLink(), vars.spread,
            Actual365Fixed(), vars.compounding, Annual,
            cmsBondSettlementDate2)
        error11 = abs(cmsBondImpliedValue2 - cmsBondCleanPrice2)
        self.assertFalse(error11 > tolerance)

        zeroCpnBondStartDate1 = Date(19, December, 1985)
        zeroCpnBondMaturityDate1 = Date(20, December, 2015)
        zeroCpnBondRedemption1 = bondCalendar.adjust(zeroCpnBondMaturityDate1, Following)
        zeroCpnBondLeg1 = Leg(1, SimpleCashFlow(100.0, zeroCpnBondRedemption1))
        zeroCpnBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate1, zeroCpnBondStartDate1, zeroCpnBondLeg1)
        zeroCpnBond1.setPricingEngine(bondEngine)

        zeroCpnBondImpliedValue1 = zeroCpnBond1.cleanPrice()
        zeroCpnBondSettlementDate1 = zeroCpnBond1.settlementDate()

        zeroCpnBondCleanPrice1 = BondFunctions.cleanPrice(
            zeroCpnBond1,
            vars.termStructure.currentLink(),
            vars.spread,
            Actual365Fixed(),
            vars.compounding, Annual,
            zeroCpnBondSettlementDate1)
        error13 = abs(zeroCpnBondImpliedValue1 - zeroCpnBondCleanPrice1)
        self.assertFalse(error13 > tolerance)

        zeroCpnBondStartDate2 = Date(17, February, 1998)
        zeroCpnBondMaturityDate2 = Date(17, February, 2028)
        zerocpbondRedemption2 = bondCalendar.adjust(zeroCpnBondMaturityDate2, Following)
        zeroCpnBondLeg2 = Leg(1, SimpleCashFlow(100.0, zerocpbondRedemption2))
        zeroCpnBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate2, zeroCpnBondStartDate2, zeroCpnBondLeg2)
        zeroCpnBond2.setPricingEngine(bondEngine)

        zeroCpnBondImpliedValue2 = zeroCpnBond2.cleanPrice()
        zeroCpnBondSettlementDate2 = zeroCpnBond2.settlementDate()

        zeroCpnBondCleanPrice2 = BondFunctions.cleanPrice(
            zeroCpnBond2,
            vars.termStructure.currentLink(),
            vars.spread,
            Actual365Fixed(),
            vars.compounding, Annual,
            zeroCpnBondSettlementDate2)
        error15 = abs(zeroCpnBondImpliedValue2 - zeroCpnBondCleanPrice2)
        self.assertFalse(error15 > tolerance)
        vars.cleanUp()

    def testSpecializedBondVsGenericBond(self):
        TEST_MESSAGE(
            "Testing clean and dirty prices for specialized bond"
            " against equivalent generic bond...")

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3
        fixingDays = 2
        inArrears = false

        fixedBondStartDate1 = Date(4, January, 2005)
        fixedBondMaturityDate1 = Date(4, January, 2037)
        fixedBondSchedule1 = Schedule(
            fixedBondStartDate1,
            fixedBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg1 = FixedRateLeg(fixedBondSchedule1)
        fixedBondLeg1.withNotionals(vars.faceAmount)
        fixedBondLeg1.withCouponRates(0.04, ActualActual(ActualActual.ISDA))
        fixedBondLeg1 = fixedBondLeg1.makeLeg()
        fixedbondRedemption1 = bondCalendar.adjust(fixedBondMaturityDate1, Following)
        fixedBondLeg1 = [l for l in fixedBondLeg1]
        fixedBondLeg1.append(
            SimpleCashFlow(100.0, fixedbondRedemption1))

        fixedBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate1, fixedBondStartDate1,
            fixedBondLeg1)
        bondEngine = DiscountingBondEngine(vars.termStructure)
        fixedBond1.setPricingEngine(bondEngine)

        fixedSpecializedBond1 = FixedRateBond(
            settlementDays, vars.faceAmount, fixedBondSchedule1,
            DoubleVector(1, 0.04),
            ActualActual(ActualActual.ISDA), Following,
            100.0, Date(4, January, 2005))
        fixedSpecializedBond1.setPricingEngine(bondEngine)

        fixedBondTheoValue1 = fixedBond1.cleanPrice()
        fixedSpecializedBondTheoValue1 = fixedSpecializedBond1.cleanPrice()
        tolerance = 1.0e-13
        error1 = abs(fixedBondTheoValue1 - fixedSpecializedBondTheoValue1)
        self.assertFalse(error1 > tolerance)

        fixedBondTheoDirty1 = fixedBondTheoValue1 + fixedBond1.accruedAmount()
        fixedSpecializedTheoDirty1 = fixedSpecializedBondTheoValue1 + fixedSpecializedBond1.accruedAmount()
        error2 = abs(fixedBondTheoDirty1 - fixedSpecializedTheoDirty1)
        self.assertFalse(error2 > tolerance)

        fixedBondStartDate2 = Date(5, February, 2005)
        fixedBondMaturityDate2 = Date(5, February, 2019)
        fixedBondSchedule2 = Schedule(
            fixedBondStartDate2,
            fixedBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg2 = FixedRateLeg(fixedBondSchedule2)
        fixedBondLeg2.withNotionals(vars.faceAmount)
        fixedBondLeg2.withCouponRates(0.05, Thirty360(Thirty360.BondBasis))
        fixedBondLeg2 = fixedBondLeg2.makeLeg()
        fixedbondRedemption2 = bondCalendar.adjust(fixedBondMaturityDate2, Following)
        fixedBondLeg2 = [l for l in fixedBondLeg2]
        fixedBondLeg2.append(
            SimpleCashFlow(100.0, fixedbondRedemption2))

        fixedBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate2, fixedBondStartDate2, fixedBondLeg2)
        fixedBond2.setPricingEngine(bondEngine)

        fixedSpecializedBond2 = FixedRateBond(
            settlementDays, vars.faceAmount, fixedBondSchedule2,
            DoubleVector(1, 0.05),
            Thirty360(Thirty360.BondBasis), Following,
            100.0, Date(5, February, 2005))
        fixedSpecializedBond2.setPricingEngine(bondEngine)

        fixedBondTheoValue2 = fixedBond2.cleanPrice()
        fixedSpecializedBondTheoValue2 = fixedSpecializedBond2.cleanPrice()

        error3 = abs(fixedBondTheoValue2 - fixedSpecializedBondTheoValue2)
        self.assertFalse(error3 > tolerance)

        fixedBondTheoDirty2 = fixedBondTheoValue2 + fixedBond2.accruedAmount()
        fixedSpecializedBondTheoDirty2 = fixedSpecializedBondTheoValue2 + fixedSpecializedBond2.accruedAmount()

        error4 = abs(fixedBondTheoDirty2 - fixedSpecializedBondTheoDirty2)
        self.assertFalse(error4 > tolerance)

        floatingBondStartDate1 = Date(29, September, 2003)
        floatingBondMaturityDate1 = Date(29, September, 2013)
        floatingBondSchedule1 = Schedule(
            floatingBondStartDate1,
            floatingBondMaturityDate1,
            Period(Semiannual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        floatingBondLeg1 = IborLeg(floatingBondSchedule1, vars.iborIndex)
        floatingBondLeg1.withNotionals(vars.faceAmount)
        floatingBondLeg1.withPaymentDayCounter(Actual360())
        floatingBondLeg1.withFixingDays(fixingDays)
        floatingBondLeg1.withSpreads(0.0056)
        floatingBondLeg1.inArrears(inArrears)
        floatingBondLeg1 = floatingBondLeg1.makeLeg()
        floatingbondRedemption1 = bondCalendar.adjust(floatingBondMaturityDate1, Following)
        floatingBondLeg1 = [l for l in floatingBondLeg1]
        floatingBondLeg1.append(
            SimpleCashFlow(100.0, floatingbondRedemption1))

        floatingBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate1, floatingBondStartDate1,
            floatingBondLeg1)
        floatingBond1.setPricingEngine(bondEngine)

        floatingSpecializedBond1 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule1,
            vars.iborIndex, Actual360(),
            Following, fixingDays,
            DoubleVector(1, 1),
            DoubleVector(1, 0.0056),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(29, September, 2003))
        floatingSpecializedBond1.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond1.cashflows(), vars.pricer)
        setCouponPricer(floatingSpecializedBond1.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(27, March, 2007), 0.0402)
        floatingBondTheoValue1 = floatingBond1.cleanPrice()
        floatingSpecializedBondTheoValue1 = floatingSpecializedBond1.cleanPrice()

        error5 = abs(floatingBondTheoValue1 - floatingSpecializedBondTheoValue1)
        self.assertFalse(error5 > tolerance)
        floatingBondTheoDirty1 = floatingBondTheoValue1 + floatingBond1.accruedAmount()
        floatingSpecializedBondTheoDirty1 = floatingSpecializedBondTheoValue1 + floatingSpecializedBond1.accruedAmount()
        error6 = abs(floatingBondTheoDirty1 - floatingSpecializedBondTheoDirty1)
        self.assertFalse(error6 > tolerance)

        floatingBondStartDate2 = Date(24, September, 2004)
        floatingBondMaturityDate2 = Date(24, September, 2018)
        floatingBondSchedule2 = Schedule(floatingBondStartDate2,
                                         floatingBondMaturityDate2,
                                         Period(Semiannual), bondCalendar,
                                         ModifiedFollowing, ModifiedFollowing,
                                         DateGeneration.Backward, false)
        floatingBondLeg2 = IborLeg(floatingBondSchedule2, vars.iborIndex)
        floatingBondLeg2.withNotionals(vars.faceAmount)
        floatingBondLeg2.withPaymentDayCounter(Actual360())
        floatingBondLeg2.withPaymentAdjustment(ModifiedFollowing)
        floatingBondLeg2.withFixingDays(fixingDays)
        floatingBondLeg2.withSpreads(0.0025)
        floatingBondLeg2.inArrears(inArrears)
        floatingBondLeg2 = floatingBondLeg2.makeLeg()
        floatingbondRedemption2 = bondCalendar.adjust(floatingBondMaturityDate2, ModifiedFollowing)
        floatingBondLeg2 = [l for l in floatingBondLeg2]
        floatingBondLeg2.append(
            SimpleCashFlow(100.0, floatingbondRedemption2))

        floatingBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate2, floatingBondStartDate2,
            floatingBondLeg2)
        floatingBond2.setPricingEngine(bondEngine)

        floatingSpecializedBond2 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule2,
            vars.iborIndex, Actual360(),
            ModifiedFollowing, fixingDays,
            DoubleVector(1, 1),
            DoubleVector(1, 0.0025),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(24, September, 2004))
        floatingSpecializedBond2.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond2.cashflows(), vars.pricer)
        setCouponPricer(floatingSpecializedBond2.cashflows(), vars.pricer)

        vars.iborIndex.addFixing(Date(22, March, 2007), 0.04013)

        floatingBondTheoValue2 = floatingBond2.cleanPrice()
        floatingSpecializedBondTheoValue2 = floatingSpecializedBond2.cleanPrice()

        error7 = abs(floatingBondTheoValue2 - floatingSpecializedBondTheoValue2)
        self.assertFalse(error7 > tolerance)

        floatingBondTheoDirty2 = floatingBondTheoValue2 + floatingBond2.accruedAmount()
        floatingSpecializedTheoDirty2 = floatingSpecializedBondTheoValue2 + floatingSpecializedBond2.accruedAmount()

        error8 = abs(floatingBondTheoDirty2 - floatingSpecializedTheoDirty2)
        self.assertFalse(error8 > tolerance)

        cmsBondStartDate1 = Date(22, August, 2005)
        cmsBondMaturityDate1 = Date(22, August, 2020)
        cmsBondSchedule1 = Schedule(
            cmsBondStartDate1,
            cmsBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg1 = CmsLeg(cmsBondSchedule1, vars.swapIndex)
        cmsBondLeg1.withNotionals(vars.faceAmount)
        cmsBondLeg1.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg1.withFixingDays(fixingDays)
        cmsBondLeg1.withCaps(0.055)
        cmsBondLeg1.withFloors(0.025)
        cmsBondLeg1.inArrears(inArrears)
        cmsBondLeg1 = cmsBondLeg1.makeLeg()
        cmsbondRedemption1 = bondCalendar.adjust(cmsBondMaturityDate1, Following)
        cmsBondLeg1 = [l for l in cmsBondLeg1]
        cmsBondLeg1.append(
            SimpleCashFlow(100.0, cmsbondRedemption1))

        cmsBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate1, cmsBondStartDate1, cmsBondLeg1)
        cmsBond1.setPricingEngine(bondEngine)

        cmsSpecializedBond1 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule1,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 1.0), DoubleVector(1, 0.0),
            DoubleVector(1, 0.055), DoubleVector(1, 0.025),
            inArrears,
            100.0, Date(22, August, 2005))
        cmsSpecializedBond1.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond1.cashflows(), vars.cmspricer)
        setCouponPricer(cmsSpecializedBond1.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(18, August, 2006), 0.04158)
        cmsBondTheoValue1 = cmsBond1.cleanPrice()
        cmsSpecializedBondTheoValue1 = cmsSpecializedBond1.cleanPrice()
        error9 = abs(cmsBondTheoValue1 - cmsSpecializedBondTheoValue1)
        self.assertFalse(error9 > tolerance)

        cmsBondTheoDirty1 = cmsBondTheoValue1 + cmsBond1.accruedAmount()
        cmsSpecializedBondTheoDirty1 = cmsSpecializedBondTheoValue1 + cmsSpecializedBond1.accruedAmount()
        error10 = abs(cmsBondTheoDirty1 - cmsSpecializedBondTheoDirty1)
        self.assertFalse(error10 > tolerance)

        cmsBondStartDate2 = Date(6, May, 2005)
        cmsBondMaturityDate2 = Date(6, May, 2015)
        cmsBondSchedule2 = Schedule(
            cmsBondStartDate2,
            cmsBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg2 = CmsLeg(cmsBondSchedule2, vars.swapIndex)
        cmsBondLeg2.withNotionals(vars.faceAmount)
        cmsBondLeg2.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg2.withFixingDays(fixingDays)
        cmsBondLeg2.withGearings(0.84)
        cmsBondLeg2.inArrears(inArrears)
        cmsBondLeg2 = cmsBondLeg2.makeLeg()
        cmsbondRedemption2 = bondCalendar.adjust(cmsBondMaturityDate2, Following)
        cmsBondLeg2 = [l for l in cmsBondLeg2]
        cmsBondLeg2.append(
            SimpleCashFlow(100.0, cmsbondRedemption2))

        cmsBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate2, cmsBondStartDate2, cmsBondLeg2)
        cmsBond2.setPricingEngine(bondEngine)

        cmsSpecializedBond2 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule2,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 0.84), DoubleVector(1, 0.0),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(6, May, 2005))
        cmsSpecializedBond2.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond2.cashflows(), vars.cmspricer)
        setCouponPricer(cmsSpecializedBond2.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(4, May, 2006), 0.04217)
        cmsBondTheoValue2 = cmsBond2.cleanPrice()
        cmsSpecializedBondTheoValue2 = cmsSpecializedBond2.cleanPrice()

        error11 = abs(cmsBondTheoValue2 - cmsSpecializedBondTheoValue2)
        self.assertFalse(error11 > tolerance)
        cmsBondTheoDirty2 = cmsBondTheoValue2 + cmsBond2.accruedAmount()
        cmsSpecializedBondTheoDirty2 = cmsSpecializedBondTheoValue2 + cmsSpecializedBond2.accruedAmount()
        error12 = abs(cmsBondTheoDirty2 - cmsSpecializedBondTheoDirty2)
        self.assertFalse(error12 > tolerance)

        zeroCpnBondStartDate1 = Date(19, December, 1985)
        zeroCpnBondMaturityDate1 = Date(20, December, 2015)
        zeroCpnBondRedemption1 = bondCalendar.adjust(zeroCpnBondMaturityDate1, Following)
        zeroCpnBondLeg1 = Leg(1, SimpleCashFlow(100.0, zeroCpnBondRedemption1))

        zeroCpnBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate1, zeroCpnBondStartDate1, zeroCpnBondLeg1)
        zeroCpnBond1.setPricingEngine(bondEngine)

        zeroCpnSpecializedBond1 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(20, December, 2015),
            Following,
            100.0, Date(19, December, 1985))
        zeroCpnSpecializedBond1.setPricingEngine(bondEngine)

        zeroCpnBondTheoValue1 = zeroCpnBond1.cleanPrice()
        zeroCpnSpecializedBondTheoValue1 = zeroCpnSpecializedBond1.cleanPrice()

        error13 = abs(zeroCpnBondTheoValue1 - zeroCpnSpecializedBondTheoValue1)
        self.assertFalse(error13 > tolerance)
        zeroCpnBondTheoDirty1 = zeroCpnBondTheoValue1 + zeroCpnBond1.accruedAmount()
        zeroCpnSpecializedBondTheoDirty1 = zeroCpnSpecializedBondTheoValue1 + zeroCpnSpecializedBond1.accruedAmount()
        error14 = abs(zeroCpnBondTheoDirty1 - zeroCpnSpecializedBondTheoDirty1)
        self.assertFalse(error14 > tolerance)

        zeroCpnBondStartDate2 = Date(17, February, 1998)
        zeroCpnBondMaturityDate2 = Date(17, February, 2028)
        zerocpbondRedemption2 = bondCalendar.adjust(zeroCpnBondMaturityDate2, Following)
        zeroCpnBondLeg2 = Leg(1, SimpleCashFlow(100.0, zerocpbondRedemption2))

        zeroCpnBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate2, zeroCpnBondStartDate2, zeroCpnBondLeg2)
        zeroCpnBond2.setPricingEngine(bondEngine)

        zeroCpnSpecializedBond2 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(17, February, 2028),
            Following,
            100.0, Date(17, February, 1998))
        zeroCpnSpecializedBond2.setPricingEngine(bondEngine)

        zeroCpnBondTheoValue2 = zeroCpnBond2.cleanPrice()
        zeroCpnSpecializedBondTheoValue2 = zeroCpnSpecializedBond2.cleanPrice()

        error15 = abs(zeroCpnBondTheoValue2 - zeroCpnSpecializedBondTheoValue2)
        self.assertFalse(error15 > tolerance)

        zeroCpnBondTheoDirty2 = zeroCpnBondTheoValue2 + zeroCpnBond2.accruedAmount()

        zeroCpnSpecializedBondTheoDirty2 = zeroCpnSpecializedBondTheoValue2 + zeroCpnSpecializedBond2.accruedAmount()

        error16 = abs(zeroCpnBondTheoDirty2 - zeroCpnSpecializedBondTheoDirty2)
        self.assertFalse(error16 > tolerance)
        vars.cleanUp()

    def testSpecializedBondVsGenericBondUsingAsw(self):
        TEST_MESSAGE(
            "Testing asset-swap prices and spreads for specialized"
            " bond against equivalent generic bond...")

        vars = CommonVars()

        bondCalendar = TARGET()
        settlementDays = 3
        fixingDays = 2
        payFixedRate = true
        parAssetSwap = true
        inArrears = false

        fixedBondStartDate1 = Date(4, January, 2005)
        fixedBondMaturityDate1 = Date(4, January, 2037)
        fixedBondSchedule1 = Schedule(
            fixedBondStartDate1,
            fixedBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg1 = FixedRateLeg(fixedBondSchedule1)
        fixedBondLeg1.withNotionals(vars.faceAmount)
        fixedBondLeg1.withCouponRates(0.04, ActualActual(ActualActual.ISDA))
        fixedBondLeg1 = fixedBondLeg1.makeLeg()
        fixedbondRedemption1 = bondCalendar.adjust(fixedBondMaturityDate1, Following)
        fixedBondLeg1 = [l for l in fixedBondLeg1]
        fixedBondLeg1.append(
            SimpleCashFlow(100.0, fixedbondRedemption1))

        fixedBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate1, fixedBondStartDate1,
            fixedBondLeg1)
        bondEngine = DiscountingBondEngine(vars.termStructure)
        swapEngine = DiscountingSwapEngine(vars.termStructure)
        fixedBond1.setPricingEngine(bondEngine)

        fixedSpecializedBond1 = FixedRateBond(
            settlementDays, vars.faceAmount, fixedBondSchedule1,
            DoubleVector(1, 0.04),
            ActualActual(ActualActual.ISDA), Following,
            100.0, Date(4, January, 2005))
        fixedSpecializedBond1.setPricingEngine(bondEngine)

        fixedBondPrice1 = fixedBond1.cleanPrice()
        fixedSpecializedBondPrice1 = fixedSpecializedBond1.cleanPrice()
        fixedBondAssetSwap1 = AssetSwap(
            payFixedRate,
            fixedBond1, fixedBondPrice1,
            vars.iborIndex, vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondAssetSwap1.setPricingEngine(swapEngine)
        fixedSpecializedBondAssetSwap1 = AssetSwap(
            payFixedRate,
            fixedSpecializedBond1,
            fixedSpecializedBondPrice1,
            vars.iborIndex,
            vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedSpecializedBondAssetSwap1.setPricingEngine(swapEngine)
        fixedBondAssetSwapPrice1 = fixedBondAssetSwap1.fairCleanPrice()
        fixedSpecializedBondAssetSwapPrice1 = fixedSpecializedBondAssetSwap1.fairCleanPrice()
        tolerance = 1.0e-13
        error1 = abs(fixedBondAssetSwapPrice1 - fixedSpecializedBondAssetSwapPrice1)
        self.assertFalse(error1 > tolerance)

        fixedBondMktPrice1 = 91.832
        fixedBondASW1 = AssetSwap(
            payFixedRate,
            fixedBond1, fixedBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondASW1.setPricingEngine(swapEngine)
        fixedSpecializedBondASW1 = AssetSwap(
            payFixedRate,
            fixedSpecializedBond1,
            fixedBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedSpecializedBondASW1.setPricingEngine(swapEngine)
        fixedBondASWSpread1 = fixedBondASW1.fairSpread()
        fixedSpecializedBondASWSpread1 = fixedSpecializedBondASW1.fairSpread()
        error2 = abs(fixedBondASWSpread1 - fixedSpecializedBondASWSpread1)
        self.assertFalse(error2 > tolerance)

        fixedBondStartDate2 = Date(5, February, 2005)
        fixedBondMaturityDate2 = Date(5, February, 2019)
        fixedBondSchedule2 = Schedule(
            fixedBondStartDate2,
            fixedBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        fixedBondLeg2 = FixedRateLeg(fixedBondSchedule2)
        fixedBondLeg2.withNotionals(vars.faceAmount)
        fixedBondLeg2.withCouponRates(0.05, Thirty360(Thirty360.BondBasis))
        fixedBondLeg2 = fixedBondLeg2.makeLeg()
        fixedbondRedemption2 = bondCalendar.adjust(fixedBondMaturityDate2, Following)
        fixedBondLeg2 = [l for l in fixedBondLeg2]
        fixedBondLeg2.append(
            SimpleCashFlow(100.0, fixedbondRedemption2))

        fixedBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            fixedBondMaturityDate2, fixedBondStartDate2, fixedBondLeg2)
        fixedBond2.setPricingEngine(bondEngine)

        fixedSpecializedBond2 = FixedRateBond(
            settlementDays, vars.faceAmount, fixedBondSchedule2,
            DoubleVector(1, 0.05),
            Thirty360(Thirty360.BondBasis), Following,
            100.0, Date(5, February, 2005))
        fixedSpecializedBond2.setPricingEngine(bondEngine)

        fixedBondPrice2 = fixedBond2.cleanPrice()
        fixedSpecializedBondPrice2 = fixedSpecializedBond2.cleanPrice()
        fixedBondAssetSwap2 = AssetSwap(
            payFixedRate,
            fixedBond2, fixedBondPrice2,
            vars.iborIndex, vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondAssetSwap2.setPricingEngine(swapEngine)
        fixedSpecializedBondAssetSwap2 = AssetSwap(
            payFixedRate,
            fixedSpecializedBond2,
            fixedSpecializedBondPrice2,
            vars.iborIndex,
            vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedSpecializedBondAssetSwap2.setPricingEngine(swapEngine)
        fixedBondAssetSwapPrice2 = fixedBondAssetSwap2.fairCleanPrice()
        fixedSpecializedBondAssetSwapPrice2 = fixedSpecializedBondAssetSwap2.fairCleanPrice()

        error3 = abs(fixedBondAssetSwapPrice2 - fixedSpecializedBondAssetSwapPrice2)
        self.assertFalse(error3 > tolerance)

        fixedBondMktPrice2 = 102.178
        fixedBondASW2 = AssetSwap(
            payFixedRate,
            fixedBond2, fixedBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedBondASW2.setPricingEngine(swapEngine)
        fixedSpecializedBondASW2 = AssetSwap(
            payFixedRate,
            fixedSpecializedBond2,
            fixedBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        fixedSpecializedBondASW2.setPricingEngine(swapEngine)
        fixedBondASWSpread2 = fixedBondASW2.fairSpread()
        fixedSpecializedBondASWSpread2 = fixedSpecializedBondASW2.fairSpread()
        error4 = abs(fixedBondASWSpread2 - fixedSpecializedBondASWSpread2)
        self.assertFalse(error4 > tolerance)

        floatingBondStartDate1 = Date(29, September, 2003)
        floatingBondMaturityDate1 = Date(29, September, 2013)
        floatingBondSchedule1 = Schedule(
            floatingBondStartDate1,
            floatingBondMaturityDate1,
            Period(Semiannual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        floatingBondLeg1 = IborLeg(floatingBondSchedule1, vars.iborIndex)
        floatingBondLeg1.withNotionals(vars.faceAmount)
        floatingBondLeg1.withPaymentDayCounter(Actual360())
        floatingBondLeg1.withFixingDays(fixingDays)
        floatingBondLeg1.withSpreads(0.0056)
        floatingBondLeg1.inArrears(inArrears)
        floatingBondLeg1 = floatingBondLeg1.makeLeg()
        floatingbondRedemption1 = bondCalendar.adjust(floatingBondMaturityDate1, Following)
        floatingBondLeg1 = [l for l in floatingBondLeg1]
        floatingBondLeg1.append(
            SimpleCashFlow(100.0, floatingbondRedemption1))

        floatingBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate1, floatingBondStartDate1,
            floatingBondLeg1)
        floatingBond1.setPricingEngine(bondEngine)

        floatingSpecializedBond1 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule1,
            vars.iborIndex, Actual360(),
            Following, fixingDays,
            DoubleVector(1, 1),
            DoubleVector(1, 0.0056),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(29, September, 2003))
        floatingSpecializedBond1.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond1.cashflows(), vars.pricer)
        setCouponPricer(floatingSpecializedBond1.cashflows(), vars.pricer)
        vars.iborIndex.addFixing(Date(27, March, 2007), 0.0402)
        floatingBondPrice1 = floatingBond1.cleanPrice()
        floatingSpecializedBondPrice1 = floatingSpecializedBond1.cleanPrice()
        floatingBondAssetSwap1 = AssetSwap(
            payFixedRate,
            floatingBond1, floatingBondPrice1,
            vars.iborIndex, vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondAssetSwap1.setPricingEngine(swapEngine)
        floatingSpecializedBondAssetSwap1 = AssetSwap(
            payFixedRate,
            floatingSpecializedBond1,
            floatingSpecializedBondPrice1,
            vars.iborIndex,
            vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingSpecializedBondAssetSwap1.setPricingEngine(swapEngine)
        floatingBondAssetSwapPrice1 = floatingBondAssetSwap1.fairCleanPrice()
        floatingSpecializedBondAssetSwapPrice1 = floatingSpecializedBondAssetSwap1.fairCleanPrice()

        error5 = abs(floatingBondAssetSwapPrice1 - floatingSpecializedBondAssetSwapPrice1)
        self.assertFalse(error5 > tolerance)

        floatingBondMktPrice1 = 101.33
        floatingBondASW1 = AssetSwap(
            payFixedRate,
            floatingBond1, floatingBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondASW1.setPricingEngine(swapEngine)
        floatingSpecializedBondASW1 = AssetSwap(
            payFixedRate,
            floatingSpecializedBond1,
            floatingBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingSpecializedBondASW1.setPricingEngine(swapEngine)
        floatingBondASWSpread1 = floatingBondASW1.fairSpread()
        floatingSpecializedBondASWSpread1 = floatingSpecializedBondASW1.fairSpread()
        error6 = abs(floatingBondASWSpread1 - floatingSpecializedBondASWSpread1)
        self.assertFalse(error6 > tolerance)

        floatingBondStartDate2 = Date(24, September, 2004)
        floatingBondMaturityDate2 = Date(24, September, 2018)
        floatingBondSchedule2 = Schedule(
            floatingBondStartDate2,
            floatingBondMaturityDate2,
            Period(Semiannual), bondCalendar,
            ModifiedFollowing, ModifiedFollowing,
            DateGeneration.Backward, false)
        floatingBondLeg2 = IborLeg(floatingBondSchedule2, vars.iborIndex)
        floatingBondLeg2.withNotionals(vars.faceAmount)
        floatingBondLeg2.withPaymentDayCounter(Actual360())
        floatingBondLeg2.withPaymentAdjustment(ModifiedFollowing)
        floatingBondLeg2.withFixingDays(fixingDays)
        floatingBondLeg2.withSpreads(0.0025)
        floatingBondLeg2.inArrears(inArrears)
        floatingBondLeg2 = floatingBondLeg2.makeLeg()
        floatingbondRedemption2 = bondCalendar.adjust(floatingBondMaturityDate2, ModifiedFollowing)
        floatingBondLeg2 = [l for l in floatingBondLeg2]
        floatingBondLeg2.append(
            SimpleCashFlow(100.0, floatingbondRedemption2))

        floatingBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            floatingBondMaturityDate2, floatingBondStartDate2,
            floatingBondLeg2)
        floatingBond2.setPricingEngine(bondEngine)

        floatingSpecializedBond2 = FloatingRateBond(
            settlementDays, vars.faceAmount,
            floatingBondSchedule2,
            vars.iborIndex, Actual360(),
            ModifiedFollowing, fixingDays,
            DoubleVector(1, 1),
            DoubleVector(1, 0.0025),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(24, September, 2004))
        floatingSpecializedBond2.setPricingEngine(bondEngine)

        setCouponPricer(floatingBond2.cashflows(), vars.pricer)
        setCouponPricer(floatingSpecializedBond2.cashflows(), vars.pricer)

        vars.iborIndex.addFixing(Date(22, March, 2007), 0.04013)

        floatingBondPrice2 = floatingBond2.cleanPrice()
        floatingSpecializedBondPrice2 = floatingSpecializedBond2.cleanPrice()
        floatingBondAssetSwap2 = AssetSwap(
            payFixedRate,
            floatingBond2, floatingBondPrice2,
            vars.iborIndex, vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondAssetSwap2.setPricingEngine(swapEngine)
        floatingSpecializedBondAssetSwap2 = AssetSwap(
            payFixedRate,
            floatingSpecializedBond2,
            floatingSpecializedBondPrice2,
            vars.iborIndex,
            vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingSpecializedBondAssetSwap2.setPricingEngine(swapEngine)
        floatingBondAssetSwapPrice2 = floatingBondAssetSwap2.fairCleanPrice()
        floatingSpecializedBondAssetSwapPrice2 = floatingSpecializedBondAssetSwap2.fairCleanPrice()
        error7 = abs(floatingBondAssetSwapPrice2 - floatingSpecializedBondAssetSwapPrice2)
        self.assertFalse(error7 > tolerance)

        floatingBondMktPrice2 = 101.26
        floatingBondASW2 = AssetSwap(
            payFixedRate,
            floatingBond2, floatingBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingBondASW2.setPricingEngine(swapEngine)
        floatingSpecializedBondASW2 = AssetSwap(
            payFixedRate,
            floatingSpecializedBond2,
            floatingBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        floatingSpecializedBondASW2.setPricingEngine(swapEngine)
        floatingBondASWSpread2 = floatingBondASW2.fairSpread()
        floatingSpecializedBondASWSpread2 = floatingSpecializedBondASW2.fairSpread()
        error8 = abs(floatingBondASWSpread2 - floatingSpecializedBondASWSpread2)
        self.assertFalse(error8 > tolerance)

        cmsBondStartDate1 = Date(22, August, 2005)
        cmsBondMaturityDate1 = Date(22, August, 2020)
        cmsBondSchedule1 = Schedule(
            cmsBondStartDate1,
            cmsBondMaturityDate1,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg1 = CmsLeg(cmsBondSchedule1, vars.swapIndex)
        cmsBondLeg1.withNotionals(vars.faceAmount)
        cmsBondLeg1.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg1.withFixingDays(fixingDays)
        cmsBondLeg1.withCaps(0.055)
        cmsBondLeg1.withFloors(0.025)
        cmsBondLeg1.inArrears(inArrears)
        cmsBondLeg1 = cmsBondLeg1.makeLeg()
        cmsbondRedemption1 = bondCalendar.adjust(cmsBondMaturityDate1, Following)
        cmsBondLeg1 = [l for l in cmsBondLeg1]
        cmsBondLeg1.append(
            SimpleCashFlow(100.0, cmsbondRedemption1))

        cmsBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate1, cmsBondStartDate1, cmsBondLeg1)
        cmsBond1.setPricingEngine(bondEngine)

        cmsSpecializedBond1 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule1,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 1.0), DoubleVector(1, 0.0),
            DoubleVector(1, 0.055), DoubleVector(1, 0.025),
            inArrears,
            100.0, Date(22, August, 2005))
        cmsSpecializedBond1.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond1.cashflows(), vars.cmspricer)
        setCouponPricer(cmsSpecializedBond1.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(18, August, 2006), 0.04158)
        cmsBondPrice1 = cmsBond1.cleanPrice()
        cmsSpecializedBondPrice1 = cmsSpecializedBond1.cleanPrice()
        cmsBondAssetSwap1 = AssetSwap(
            payFixedRate, cmsBond1, cmsBondPrice1,
            vars.iborIndex, vars.nonnullspread,
            Schedule(), vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondAssetSwap1.setPricingEngine(swapEngine)
        cmsSpecializedBondAssetSwap1 = AssetSwap(
            payFixedRate, cmsSpecializedBond1,
            cmsSpecializedBondPrice1,
            vars.iborIndex,
            vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsSpecializedBondAssetSwap1.setPricingEngine(swapEngine)
        cmsBondAssetSwapPrice1 = cmsBondAssetSwap1.fairCleanPrice()
        cmsSpecializedBondAssetSwapPrice1 = cmsSpecializedBondAssetSwap1.fairCleanPrice()
        error9 = abs(cmsBondAssetSwapPrice1 - cmsSpecializedBondAssetSwapPrice1)
        self.assertFalse(error9 > tolerance)

        cmsBondMktPrice1 = 87.02
        cmsBondASW1 = AssetSwap(
            payFixedRate,
            cmsBond1, cmsBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondASW1.setPricingEngine(swapEngine)
        cmsSpecializedBondASW1 = AssetSwap(
            payFixedRate,
            cmsSpecializedBond1,
            cmsBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsSpecializedBondASW1.setPricingEngine(swapEngine)
        cmsBondASWSpread1 = cmsBondASW1.fairSpread()
        cmsSpecializedBondASWSpread1 = cmsSpecializedBondASW1.fairSpread()
        error10 = abs(cmsBondASWSpread1 - cmsSpecializedBondASWSpread1)
        self.assertFalse(error10 > tolerance)

        cmsBondStartDate2 = Date(6, May, 2005)
        cmsBondMaturityDate2 = Date(6, May, 2015)
        cmsBondSchedule2 = Schedule(
            cmsBondStartDate2,
            cmsBondMaturityDate2,
            Period(Annual), bondCalendar,
            Unadjusted, Unadjusted,
            DateGeneration.Backward, false)
        cmsBondLeg2 = CmsLeg(cmsBondSchedule2, vars.swapIndex)
        cmsBondLeg2.withNotionals(vars.faceAmount)
        cmsBondLeg2.withPaymentDayCounter(Thirty360(Thirty360.BondBasis))
        cmsBondLeg2.withFixingDays(fixingDays)
        cmsBondLeg2.withGearings(0.84)
        cmsBondLeg2.inArrears(inArrears)
        cmsBondLeg2 = cmsBondLeg2.makeLeg()
        cmsbondRedemption2 = bondCalendar.adjust(cmsBondMaturityDate2, Following)
        cmsBondLeg2 = [l for l in cmsBondLeg2]
        cmsBondLeg2.append(
            SimpleCashFlow(100.0, cmsbondRedemption2))

        cmsBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            cmsBondMaturityDate2, cmsBondStartDate2, cmsBondLeg2)
        cmsBond2.setPricingEngine(bondEngine)

        cmsSpecializedBond2 = CmsRateBond(
            settlementDays, vars.faceAmount, cmsBondSchedule2,
            vars.swapIndex, Thirty360(Thirty360.BondBasis),
            Following, fixingDays,
            DoubleVector(1, 0.84), DoubleVector(1, 0.0),
            DoubleVector(), DoubleVector(),
            inArrears,
            100.0, Date(6, May, 2005))
        cmsSpecializedBond2.setPricingEngine(bondEngine)

        setCouponPricer(cmsBond2.cashflows(), vars.cmspricer)
        setCouponPricer(cmsSpecializedBond2.cashflows(), vars.cmspricer)
        vars.swapIndex.addFixing(Date(4, May, 2006), 0.04217)
        cmsBondPrice2 = cmsBond2.cleanPrice()
        cmsSpecializedBondPrice2 = cmsSpecializedBond2.cleanPrice()
        cmsBondAssetSwap2 = AssetSwap(
            payFixedRate, cmsBond2, cmsBondPrice2,
            vars.iborIndex, vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondAssetSwap2.setPricingEngine(swapEngine)
        cmsSpecializedBondAssetSwap2 = AssetSwap(
            payFixedRate, cmsSpecializedBond2,
            cmsSpecializedBondPrice2,
            vars.iborIndex,
            vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsSpecializedBondAssetSwap2.setPricingEngine(swapEngine)
        cmsBondAssetSwapPrice2 = cmsBondAssetSwap2.fairCleanPrice()
        cmsSpecializedBondAssetSwapPrice2 = cmsSpecializedBondAssetSwap2.fairCleanPrice()
        error11 = abs(cmsBondAssetSwapPrice2 - cmsSpecializedBondAssetSwapPrice2)
        self.assertFalse(error11 > tolerance)

        cmsBondMktPrice2 = 94.35
        cmsBondASW2 = AssetSwap(
            payFixedRate,
            cmsBond2, cmsBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsBondASW2.setPricingEngine(swapEngine)
        cmsSpecializedBondASW2 = AssetSwap(
            payFixedRate,
            cmsSpecializedBond2,
            cmsBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        cmsSpecializedBondASW2.setPricingEngine(swapEngine)
        cmsBondASWSpread2 = cmsBondASW2.fairSpread()
        cmsSpecializedBondASWSpread2 = cmsSpecializedBondASW2.fairSpread()
        error12 = abs(cmsBondASWSpread2 - cmsSpecializedBondASWSpread2)
        self.assertFalse(error12 > tolerance)

        zeroCpnBondStartDate1 = Date(19, December, 1985)
        zeroCpnBondMaturityDate1 = Date(20, December, 2015)
        zeroCpnBondRedemption1 = bondCalendar.adjust(zeroCpnBondMaturityDate1, Following)
        zeroCpnBondLeg1 = Leg(1, SimpleCashFlow(100.0, zeroCpnBondRedemption1))

        zeroCpnBond1 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate1, zeroCpnBondStartDate1, zeroCpnBondLeg1)
        zeroCpnBond1.setPricingEngine(bondEngine)

        zeroCpnSpecializedBond1 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(20, December, 2015),
            Following,
            100.0, Date(19, December, 1985))
        zeroCpnSpecializedBond1.setPricingEngine(bondEngine)

        zeroCpnBondPrice1 = zeroCpnBond1.cleanPrice()
        zeroCpnSpecializedBondPrice1 = zeroCpnSpecializedBond1.cleanPrice()
        zeroCpnBondAssetSwap1 = AssetSwap(
            payFixedRate, zeroCpnBond1,
            zeroCpnBondPrice1,
            vars.iborIndex, vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnBondAssetSwap1.setPricingEngine(swapEngine)
        zeroCpnSpecializedBondAssetSwap1 = AssetSwap(
            payFixedRate,
            zeroCpnSpecializedBond1,
            zeroCpnSpecializedBondPrice1,
            vars.iborIndex,
            vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnSpecializedBondAssetSwap1.setPricingEngine(swapEngine)
        zeroCpnBondAssetSwapPrice1 = zeroCpnBondAssetSwap1.fairCleanPrice()
        zeroCpnSpecializedBondAssetSwapPrice1 = zeroCpnSpecializedBondAssetSwap1.fairCleanPrice()
        error13 = abs(zeroCpnBondAssetSwapPrice1 - zeroCpnSpecializedBondAssetSwapPrice1)
        self.assertFalse(error13 > tolerance)

        zeroCpnBondMktPrice1 = 72.277
        zeroCpnBondASW1 = AssetSwap(
            payFixedRate,
            zeroCpnBond1, zeroCpnBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnBondASW1.setPricingEngine(swapEngine)
        zeroCpnSpecializedBondASW1 = AssetSwap(
            payFixedRate,
            zeroCpnSpecializedBond1,
            zeroCpnBondMktPrice1,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnSpecializedBondASW1.setPricingEngine(swapEngine)
        zeroCpnBondASWSpread1 = zeroCpnBondASW1.fairSpread()
        zeroCpnSpecializedBondASWSpread1 = zeroCpnSpecializedBondASW1.fairSpread()
        error14 = abs(zeroCpnBondASWSpread1 - zeroCpnSpecializedBondASWSpread1)
        self.assertFalse(error14 > tolerance)

        zeroCpnBondStartDate2 = Date(17, February, 1998)
        zeroCpnBondMaturityDate2 = Date(17, February, 2028)
        zerocpbondRedemption2 = bondCalendar.adjust(zeroCpnBondMaturityDate2, Following)
        zeroCpnBondLeg2 = Leg(1, SimpleCashFlow(100.0, zerocpbondRedemption2))

        zeroCpnBond2 = Bond(
            settlementDays, bondCalendar, vars.faceAmount,
            zeroCpnBondMaturityDate2, zeroCpnBondStartDate2, zeroCpnBondLeg2)
        zeroCpnBond2.setPricingEngine(bondEngine)

        zeroCpnSpecializedBond2 = ZeroCouponBond(
            settlementDays, bondCalendar, vars.faceAmount,
            Date(17, February, 2028),
            Following,
            100.0, Date(17, February, 1998))
        zeroCpnSpecializedBond2.setPricingEngine(bondEngine)

        zeroCpnBondPrice2 = zeroCpnBond2.cleanPrice()
        zeroCpnSpecializedBondPrice2 = zeroCpnSpecializedBond2.cleanPrice()

        zeroCpnBondAssetSwap2 = AssetSwap(
            payFixedRate, zeroCpnBond2,
            zeroCpnBondPrice2,
            vars.iborIndex, vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnBondAssetSwap2.setPricingEngine(swapEngine)
        zeroCpnSpecializedBondAssetSwap2 = AssetSwap(
            payFixedRate,
            zeroCpnSpecializedBond2,
            zeroCpnSpecializedBondPrice2,
            vars.iborIndex,
            vars.nonnullspread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnSpecializedBondAssetSwap2.setPricingEngine(swapEngine)
        zeroCpnBondAssetSwapPrice2 = zeroCpnBondAssetSwap2.fairCleanPrice()
        zeroCpnSpecializedBondAssetSwapPrice2 = zeroCpnSpecializedBondAssetSwap2.fairCleanPrice()
        error15 = abs(zeroCpnBondAssetSwapPrice2 - zeroCpnSpecializedBondAssetSwapPrice2)
        self.assertFalse(error15 > tolerance)

        zeroCpnBondMktPrice2 = 72.277
        zeroCpnBondASW2 = AssetSwap(
            payFixedRate,
            zeroCpnBond2, zeroCpnBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnBondASW2.setPricingEngine(swapEngine)
        zeroCpnSpecializedBondASW2 = AssetSwap(
            payFixedRate,
            zeroCpnSpecializedBond2,
            zeroCpnBondMktPrice2,
            vars.iborIndex, vars.spread,
            Schedule(),
            vars.iborIndex.dayCounter(),
            parAssetSwap)
        zeroCpnSpecializedBondASW2.setPricingEngine(swapEngine)
        zeroCpnBondASWSpread2 = zeroCpnBondASW2.fairSpread()
        zeroCpnSpecializedBondASWSpread2 = zeroCpnSpecializedBondASW2.fairSpread()
        error16 = abs(zeroCpnBondASWSpread2 - zeroCpnSpecializedBondASWSpread2)
        self.assertFalse(error16 > tolerance)
        vars.cleanUp()
