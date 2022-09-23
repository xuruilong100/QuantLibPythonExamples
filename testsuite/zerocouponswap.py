import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.backup = SavedSettings()
        self.settlementDays = 2
        self.paymentDelay = 1
        self.calendar = TARGET()
        self.dayCount = Actual365Fixed()
        self.businessConvention = ModifiedFollowing
        self.baseNominal = 1.0e6
        self.finalPayment = 1.2e6
        self.euriborHandle = RelinkableYieldTermStructureHandle()
        self.euribor = Euribor6M(self.euriborHandle)
        self.euribor.addFixing(Date(10, February, 2021), 0.0085)
        self.today = self.calendar.adjust(Date(15, March, 2021))
        Settings.instance().evaluationDate = self.today
        self.settlement = self.calendar.advance(
            self.today, self.settlementDays, Days)
        self.euriborHandle.linkTo(
            flatRate(self.settlement, 0.007, self.dayCount))
        self.discountEngine = DiscountingSwapEngine(self.euriborHandle)

    def createSubPeriodsCoupon(self,
                               start,
                               end):
        paymentDate = self.calendar.advance(
            end, Period(self.paymentDelay, Days),
            self.businessConvention)
        cpn = SubPeriodsCoupon(
            paymentDate, self.baseNominal, start, end,
            self.settlementDays, self.euribor)
        cpn.setPricer(
            CompoundingRatePricer())
        return cpn

    def createZCSwap0(self,
                      type,
                      start,
                      end,
                      baseNominal,
                      finalPayment):
        swap = ZeroCouponSwap(
            type, baseNominal, start, end, finalPayment,
            self.euribor, self.calendar, self.businessConvention,
            self.paymentDelay)
        swap.setPricingEngine(
            self.discountEngine)
        return swap

    def createZCSwap1(self,
                      type,
                      start,
                      end,
                      finalPayment):
        return self.createZCSwap0(
            type, start, end, self.baseNominal, finalPayment)

    def createZCSwap2(self,
                      type,
                      start,
                      end):
        return self.createZCSwap1(
            type, start, end, self.finalPayment)

    def createZCSwap3(self,
                      start,
                      end,
                      fixedRate):
        swap = ZeroCouponSwap(
            Swap.Receiver, self.baseNominal,
            start, end, fixedRate, self.dayCount, self.euribor,
            self.calendar, self.businessConvention, self.paymentDelay)
        swap.setPricingEngine(
            self.discountEngine)
        return swap


class ZeroCouponSwapTest(unittest.TestCase):

    def testInstrumentValuation(self):
        TEST_MESSAGE(
            "Testing zero coupon swap valuation...")

        self.checkReplicationOfZeroCouponSwapNPV(
            Date(12, February, 2021), Date(12, February, 2041),
            Swap.Receiver)

        self.checkReplicationOfZeroCouponSwapNPV(
            Date(15, April, 2021), Date(12, February, 2041), Swap.Payer)

        self.checkReplicationOfZeroCouponSwapNPV(
            Date(12, February, 2000), Date(12, February, 2020))

    def testFairFixedPayment(self):
        TEST_MESSAGE(
            "Testing fair fixed payment...")

        self.checkFairFixedPayment(
            Date(12, February, 2021), Date(12, February, 2041), Swap.Receiver)

        self.checkFairFixedPayment(
            Date(17, March, 2021), Date(12, February, 2041), Swap.Payer)

    def testFairFixedRate(self):
        TEST_MESSAGE(
            "Testing fair fixed rate...")

        self.checkFairFixedRate(
            Date(12, February, 2021), Date(12, February, 2041), Swap.Receiver)

        self.checkFairFixedRate(
            Date(17, March, 2021), Date(12, February, 2041), Swap.Payer)

    def testFixedPaymentFromRate(self):
        TEST_MESSAGE(
            "Testing fixed payment calculation from rate...")

        vars = CommonVars()
        tolerance = 1.0e-8
        fixedRate = 0.01

        start = Date(12, February, 2021)
        end = Date(12, February, 2041)

        zcSwap = vars.createZCSwap3(start, end, fixedRate)
        actualFxdPmt = zcSwap.fixedPayment()

        T = vars.dayCount.yearFraction(start, end)
        expectedFxdPmt = zcSwap.baseNominal() * (pow(1.0 + fixedRate, T) - 1.0)

        self.assertFalse(
            abs(actualFxdPmt - expectedFxdPmt) > tolerance)

    def testArgumentsValidation(self):
        TEST_MESSAGE(
            "Testing arguments validation...")

        vars = CommonVars()

        start = Date(12, February, 2021)
        end = Date(12, February, 2041)

        self.assertRaises(
            RuntimeError, vars.createZCSwap0,
            Swap.Payer, start, end, -1.0e6, 1.0e6)

        self.assertRaises(
            RuntimeError,
            vars.createZCSwap3,
            end, start, 0.01)

    def testExpectedCashFlowsInLegs(self):
        TEST_MESSAGE(
            "Testing expected cash flows in legs...")

        vars = CommonVars()
        tolerance = 1.0e-8

        start = Date(12, February, 2021)
        end = Date(12, February, 2041)

        zcSwap = vars.createZCSwap3(start, end, 0.01)
        fixedCashFlow = zcSwap.fixedLeg()[0]
        floatingCashFlow = zcSwap.floatingLeg()[0]

        paymentDate = vars.calendar.advance(
            end, Period(vars.paymentDelay, Days), vars.businessConvention)
        subPeriodCpn = vars.createSubPeriodsCoupon(start, end)

        self.assertFalse(
            abs(fixedCashFlow.amount() - zcSwap.fixedPayment()) > tolerance or
            fixedCashFlow.date() != paymentDate)

        self.assertFalse(
            abs(floatingCashFlow.amount() - subPeriodCpn.amount()) > tolerance or
            floatingCashFlow.date() != paymentDate)

    def checkReplicationOfZeroCouponSwapNPV(self,
                                            start,
                                            end,
                                            type=Swap.Receiver):
        vars = CommonVars()
        tolerance = 1.0e-8

        zcSwap = vars.createZCSwap2(type, start, end)

        actualNPV = zcSwap.NPV()
        actualFixedLegNPV = zcSwap.fixedLegNPV()
        actualFloatLegNPV = zcSwap.floatingLegNPV()

        paymentDate = vars.calendar.advance(
            end, Period(vars.paymentDelay, Days), vars.businessConvention)
        discountAtPayment = 0.0 if paymentDate < vars.settlement else vars.euriborHandle.discount(paymentDate)
        expectedFixedLegNPV = -type * discountAtPayment * vars.finalPayment

        subPeriodCpn = vars.createSubPeriodsCoupon(start, end)
        expectedFloatLegNPV = 0.0 if paymentDate < vars.settlement else type * discountAtPayment * subPeriodCpn.amount()

        expectedNPV = expectedFloatLegNPV + expectedFixedLegNPV

        self.assertFalse(
            abs(actualNPV - expectedNPV) > tolerance or
            abs(actualFixedLegNPV - expectedFixedLegNPV) > tolerance or
            abs(actualFloatLegNPV - expectedFloatLegNPV) > tolerance)

    def checkFairFixedPayment(self,
                              start,
                              end,
                              type):
        vars = CommonVars()
        tolerance = 1.0e-8

        zcSwap = vars.createZCSwap2(type, start, end)
        fairFixedPayment = zcSwap.fairFixedPayment()
        parZCSwap = vars.createZCSwap1(
            type, start, end, fairFixedPayment)
        parZCSwapNPV = parZCSwap.NPV()

        self.assertFalse((abs(parZCSwapNPV) > tolerance))

    def checkFairFixedRate(self, start, end, type):
        vars = CommonVars()
        tolerance = 1.0e-8

        zcSwap = vars.createZCSwap2(type, start, end)
        fairFixedRate = zcSwap.fairFixedRate(vars.dayCount)
        parZCSwap = vars.createZCSwap3(start, end, fairFixedRate)
        parZCSwapNPV = parZCSwap.NPV()

        self.assertFalse((abs(parZCSwapNPV) > tolerance))
