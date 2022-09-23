import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):
    def __init__(self):
        self.today = Date(7, March, 2022)
        Settings.instance().evaluationDate = self.today
        self.backup = SavedSettings()
        self.curveHandle = RelinkableYieldTermStructureHandle()
        self.curveHandle.linkTo(flatRate(self.today, 0.0004977, Actual365Fixed()))


def buildBond(issue, maturity, cpn):
    sch = Schedule(issue, maturity, Period(Annual), TARGET(), Following, Following,
                   DateGeneration.Backward, false)

    return FixedRateBond(2, 1.e5, sch, DoubleVector(1, cpn),
                         ActualActual(ActualActual.ISDA))


def buildBondForward(underlying,
                     handle,
                     delivery,
                     typ):
    valueDt = handle.referenceDate()
    return BondForward(
        valueDt, delivery, typ, 0.0, 2,
        ActualActual(ActualActual.ISDA), TARGET(), Following,
        underlying, handle, handle)


class BondForwardTest(unittest.TestCase):

    def testFuturesPriceReplication(self):
        TEST_MESSAGE(
            "Testing futures price replication...")

        vars = CommonVars()

        tolerance = 1.0e-2

        issue = Date(15, August, 2015)
        maturity = Date(15, August, 2046)
        cpn = 0.025

        bnd = buildBond(issue, maturity, cpn)
        pricer = DiscountingBondEngine(vars.curveHandle)
        bnd.setPricingEngine(pricer)

        delivery = Date(10, March, 2022)
        conversionFactor = 0.76871
        bndFwd = buildBondForward(bnd, vars.curveHandle, delivery, Position.Long)

        futuresPrice = bndFwd.cleanForwardPrice() / conversionFactor
        expectedFuturesPrice = 207.47

        self.assertFalse(abs(futuresPrice - expectedFuturesPrice) > tolerance)

    def testCleanForwardPriceReplication(self):
        TEST_MESSAGE(
            "Testing clean forward price replication...")

        vars = CommonVars()

        tolerance = 1.0e-2

        issue = Date(15, August, 2015)
        maturity = Date(15, August, 2046)
        cpn = 0.025

        bnd = buildBond(issue, maturity, cpn)
        pricer = DiscountingBondEngine(vars.curveHandle)
        bnd.setPricingEngine(pricer)

        delivery = Date(10, March, 2022)
        bndFwd = buildBondForward(bnd, vars.curveHandle, delivery, Position.Long)

        fwdCleanPrice = bndFwd.cleanForwardPrice()
        expectedFwdCleanPrice = bndFwd.forwardValue() - bnd.accruedAmount(delivery)

        self.assertFalse(abs(fwdCleanPrice - expectedFwdCleanPrice) > tolerance)

    def testThatForwardValueIsEqualToSpotValueIfNoIncome(self):
        TEST_MESSAGE(
            "Testing that forward value is equal to spot value if no income...")

        vars = CommonVars()

        tolerance = 1.0e-2

        issue = Date(15, August, 2015)
        maturity = Date(15, August, 2046)
        cpn = 0.025

        bnd = buildBond(issue, maturity, cpn)
        pricer = DiscountingBondEngine(vars.curveHandle)
        bnd.setPricingEngine(pricer)

        delivery = Date(10, March, 2022)
        bndFwd = buildBondForward(bnd, vars.curveHandle, delivery, Position.Long)

        bndFwdValue = bndFwd.forwardValue()
        underlyingDirtyPrice = bnd.dirtyPrice()

        self.assertFalse(abs(bndFwdValue - underlyingDirtyPrice) > tolerance)
