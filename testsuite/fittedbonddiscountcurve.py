import unittest
from utilities import *
from QuantLib import *


class FittedBondDiscountCurveTest(unittest.TestCase):

    def testEvaluation(self):
        TEST_MESSAGE("Testing that fitted bond curves work as evaluators...")

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

        # BOOST_CHECK_NO_THROW(curve.discount(3.0))

        try:
            curve.discount(3.0)
        except Exception as e:
            NO_THROW = false
            self.assertTrue(NO_THROW)

    def testFlatExtrapolation(self):
        TEST_MESSAGE("Testing fitted bond curve with flat extrapolation...")

        savedSettings = SavedSettings()

        asof = Date(15, Jul, 2019)
        Settings.instance().evaluationDate = asof

        # market quotes for bonds below
        quotes = [101.2100, 100.6270, 99.9210, 101.6700]

        bonds = []

        # EJ5346956
        bonds.append(
            FixedRateBond(
                2, 100.0,
                Schedule(
                    Date(1, Feb, 2013), Date(3, Feb, 2020),
                    Period(6, Months), Canada(), Following, Following,
                    DateGeneration.Forward, false, Date(3, Aug, 2013)),
                DoubleVector(1, 0.046),
                ActualActual(ActualActual.ISDA)))

        # EK9689119
        bonds.append(
            FixedRateBond(
                2, 100.0,
                Schedule(
                    Date(12, Jun, 2015), Date(12, Jun, 2020),
                    Period(6, Months), Canada(), Following,
                    Following, DateGeneration.Forward, false, Date(12, Dec, 2015)),
                DoubleVector(1, 0.0295),
                ActualActual(ActualActual.ISDA)))

        # AQ1410069
        bonds.append(
            FixedRateBond(
                2, 100.0,
                Schedule(
                    Date(24, Nov, 2017), Date(24, Nov, 2020),
                    Period(6, Months), Canada(), Following,
                    Following, DateGeneration.Forward, false, Date(24, May, 2018)),
                DoubleVector(1, 0.02689),
                ActualActual(ActualActual.ISDA)))

        # AM5387676
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

        # method1 with the usual extrapolation
        method1 = NelsonSiegelFitting()

        # method2 extrapoates flat before the first and after the last bond maturity
        method2 = NelsonSiegelFitting(
            Array(),
            # OptimizationMethod(),
            Array(),
            Actual365Fixed().yearFraction(asof, helpers.front().bond().maturityDate()),
            Actual365Fixed().yearFraction(asof, helpers.back().bond().maturityDate()))

        # Set a guess that will provoke a "bad" calibration for method1, actually this result was
        # observed as a real calibration outcome given the default guess. The setup was more
        # elaborate though and we do not aim to replicate that here.

        guess = [0.0317, 5.0, -3.6796, 24.1703]

        # build the fitted bond curves

        curve1 = FittedBondDiscountCurve(
            asof, helpers, Actual365Fixed(), method1, 1E-10, 10000, guess)

        curve2 = FittedBondDiscountCurve(
            asof, helpers, Actual365Fixed(), method2, 1E-10, 10000, guess)

        curve1.enableExtrapolation()
        curve2.enableExtrapolation()

        # extract the model prices using the two curves

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

        # the resulting cost values are similar for both approaches
        # i.e. the fit has a similar quality, I get for example:
        # fitted curve cost1 = 0.0921232
        # fitted curve cost2 = 0.0919438

        # cost1 = sqrt(curve1.fitResults().minimumCostValue())
        # cost2 = sqrt(curve2.fitResults().minimumCostValue())

        # It turns out that the model yields are quite close for model1 and model2 while the curve
        # yields are hugely different: for model1 the yields are completely off (>> 100%) while for
        # model2 they are close to the bond model yields, as it should be.
        #
        # The reason why model1 produces reasonable bond yields is that the compounding from the
        # evaluation date to the settlement date of the bonds compensates for the discounting of
        # the bond flows in the "right way", although the level of the curve yields is completely
        # off. I get these results:
        #
        # helper  maturity  market yield model yield 1 model yield 2 curve yield 1 curve yield 2
        #  0      0.556164     0.0235711     0.0235647     0.0235709       8.69643     0.0235709
        #  1      0.912329     0.0222977     0.0231515     0.0231468       5.31326     0.0231466
        #  2       1.36438     0.0272363     0.0254977     0.0255014       3.56288      0.025524
        #  3       2.61096     0.0268932     0.0277398     0.0277418       1.87629     0.0278147

        for i in range(len(helpers)):
            t = curve1.timeFromReference(helpers[i].bond().maturityDate())
            # marketYield = bonds[i].yield(quotes[i], Actual365Fixed(), Continuous, NoFrequency)
            # modelYield1 = bonds[i].yield(modelPrices1[i], Actual365Fixed(), Continuous, NoFrequency)
            modelYield2 = bonds[i].bondYield(modelPrices2[i], Actual365Fixed(), Continuous, NoFrequency)
            # curveYield1 = curve1.zeroRate(t, Continuous).rate()
            curveYield2 = curve2.zeroRate(t, Continuous).rate()

            # BOOST_CHECK_CLOSE(modelYield2, curveYield2, 1.0) # 1.0 percent relative tolerance
            self.assertTrue(abs(modelYield2 - curveYield2) / modelYield2 < 0.01)
