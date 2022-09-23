import unittest

from QuantLib import *

from utilities import *


class FittedBondDiscountCurveTest(unittest.TestCase):

    def testEvaluation(self):
        TEST_MESSAGE(
            "Testing that fitted bond curves work as evaluators...")

        today = Settings.instance().evaluationDate
        bond = ZeroCouponBond(
            3, TARGET(), 100.0, today + Period(10, Years))
        q = QuoteHandle(SimpleQuote(100.0))

        helpers = BondHelperVector(1)
        helpers[0] = BondHelper(q, bond)

        fittingMethod = ExponentialSplinesFitting()

        maxIterations = 0
        guess = Array(9)
        guess[0] = -51293.44
        guess[1] = -212240.36
        guess[2] = 168668.51
        guess[3] = 88792.74
        guess[4] = 120712.13
        guess[5] = -34332.83
        guess[6] = -66479.66
        guess[7] = 13605.17
        guess[8] = 0.0

        curve = FittedBondDiscountCurve(
            0, TARGET(), helpers, Actual365Fixed(),
            fittingMethod, 1e-10, maxIterations, guess)

        try:
            curve.discount(3.0)
        except Exception as e:
            NO_THROW = false
            self.assertTrue(NO_THROW)

    def testFlatExtrapolation(self):
        TEST_MESSAGE(
            "Testing fitted bond curve with flat extrapolation...")

        savedSettings = SavedSettings()

        asof = Date(15, Jul, 2019)
        Settings.instance().evaluationDate = asof

        quotes = [101.2100, 100.6270, 99.9210, 101.6700]

        bonds = []

        bonds.append(
            FixedRateBond(
                2, 100.0,
                Schedule(
                    Date(1, Feb, 2013), Date(3, Feb, 2020),
                    Period(6, Months), Canada(), Following, Following,
                    DateGeneration.Forward, false, Date(3, Aug, 2013)),
                DoubleVector(1, 0.046),
                ActualActual(ActualActual.ISDA)))

        bonds.append(
            FixedRateBond(
                2, 100.0,
                Schedule(
                    Date(12, Jun, 2015), Date(12, Jun, 2020),
                    Period(6, Months), Canada(), Following,
                    Following, DateGeneration.Forward, false, Date(12, Dec, 2015)),
                DoubleVector(1, 0.0295),
                ActualActual(ActualActual.ISDA)))

        bonds.append(
            FixedRateBond(
                2, 100.0,
                Schedule(
                    Date(24, Nov, 2017), Date(24, Nov, 2020),
                    Period(6, Months), Canada(), Following,
                    Following, DateGeneration.Forward, false, Date(24, May, 2018)),
                DoubleVector(1, 0.02689),
                ActualActual(ActualActual.ISDA)))

        bonds.append(FixedRateBond(
            2, 100.0,
            Schedule(
                Date(21, Feb, 2017), Date(21, Feb, 2022),
                Period(6, Months), Canada(), Following,
                Following, DateGeneration.Forward, false, Date(21, Aug, 2017)),
            DoubleVector(1, 0.0338),
            ActualActual(ActualActual.ISDA)))

        helpers = BondHelperVector()

        for i in range(len(bonds)):
            helpers.append(
                BondHelper(
                    QuoteHandle(SimpleQuote(quotes[i])), bonds[i]))

        method1 = NelsonSiegelFitting()

        method2 = NelsonSiegelFitting(
            Array(),
            Array(),
            Actual365Fixed().yearFraction(asof, helpers.front().bond().maturityDate()),
            Actual365Fixed().yearFraction(asof, helpers.back().bond().maturityDate()))

        guess = [0.0317, 5.0, -3.6796, 24.1703]

        curve1 = FittedBondDiscountCurve(
            asof, helpers, Actual365Fixed(), method1, 1E-10, 10000, guess)

        curve2 = FittedBondDiscountCurve(
            asof, helpers, Actual365Fixed(), method2, 1E-10, 10000, guess)

        curve1.enableExtrapolation()
        curve2.enableExtrapolation()

        modelPrices1 = DoubleVector()
        modelPrices2 = DoubleVector()

        engine1 = DiscountingBondEngine(YieldTermStructureHandle(curve1))
        engine2 = DiscountingBondEngine(YieldTermStructureHandle(curve2))

        for bond in bonds:
            bond.setPricingEngine(engine1)
            modelPrices1.append(bond.cleanPrice())
            bond.setPricingEngine(engine2)
            modelPrices2.append(bond.cleanPrice())

        self.assertEqual(curve1.fitResults().errorCode(), EndCriteria.MaxIterations)
        self.assertEqual(curve2.fitResults().errorCode(), EndCriteria.MaxIterations)

        for i in range(len(helpers)):
            t = curve1.timeFromReference(helpers[i].bond().maturityDate())

            modelYield2 = bonds[i].bondYield(modelPrices2[i], Actual365Fixed(), Continuous, NoFrequency)

            curveYield2 = curve2.zeroRate(t, Continuous).rate()

            self.assertTrue(abs(modelYield2 - curveYield2) / modelYield2 < 0.01)
