import unittest
from utilities import *
from QuantLib import *


class MCLongstaffSchwartzEngineTest(unittest.TestCase):
    def testAmericanOption(self):
        TEST_MESSAGE("Testing Monte-Carlo pricing of American options...")

        backup = SavedSettings()

        #  most of the example taken from the EquityOption.cpp
        optType = Option.Put
        underlying = 36
        dividendYield = 0.00
        riskFreeRate = 0.06
        volatility = 0.20

        todaysDate = Date(15, May, 1998)
        settlementDate = Date(17, May, 1998)
        Settings.instance().evaluationDate = todaysDate

        maturity = Date(17, May, 1999)
        dayCounter = Actual365Fixed()

        americanExercise = AmericanExercise(settlementDate, maturity)

        #  bootstrap the yield/dividend/vol curves
        flatTermStructure = YieldTermStructureHandle(
            FlatForward(settlementDate, riskFreeRate, dayCounter))
        flatDividendTS = YieldTermStructureHandle(
            FlatForward(settlementDate, dividendYield, dayCounter))

        #  expected results for exercise probability, evaluated with third-party
        #  product (using Cox-Rubinstein binomial tree)
        expectedExProb = Matrix(2, 3)
        expectedExProb[0][0] = 0.48013  # (price: 2.105)
        expectedExProb[0][1] = 0.51678  # (price: 3.451)
        expectedExProb[0][2] = 0.54598  # (price: 4.807)
        expectedExProb[1][0] = 0.75549  # (price: 4.505)
        expectedExProb[1][1] = 0.67569  # (price: 5.764)
        expectedExProb[1][2] = 0.65562  # (price: 7.138)

        polynomTypes = [
            LsmBasisSystem.Monomial, LsmBasisSystem.Laguerre,
            LsmBasisSystem.Hermite, LsmBasisSystem.Hyperbolic,
            LsmBasisSystem.Chebyshev2nd]

        for i in range(2):
            for j in range(3):
                flatVolTS = BlackVolTermStructureHandle(
                    BlackConstantVol(
                        settlementDate, NullCalendar(),
                        volatility + 0.1 * j, dayCounter))

                payoff = PlainVanillaPayoff(optType, underlying + 4 * i)

                underlyingH = QuoteHandle(SimpleQuote(underlying))

                stochasticProcess = GeneralizedBlackScholesProcess(
                    underlyingH, flatDividendTS,
                    flatTermStructure, flatVolTS)

                americanOption = VanillaOption(payoff, americanExercise)

                mcengine = MakeMCPRAmericanEngine(stochasticProcess)
                mcengine.withSteps(75)
                mcengine.withAntitheticVariate()
                mcengine.withAbsoluteTolerance(0.02)
                mcengine.withSeed(42)
                mcengine.withPolynomOrder(3)
                mcengine.withBasisSystem(
                    polynomTypes[0 * (i * 3 + j) % len(polynomTypes)])
                mcengine = mcengine.makeEngine()

                americanOption.setPricingEngine(mcengine)
                #  FLOATING_POINT_EXCEPTION
                calculated = americanOption.NPV()
                errorEstimate = americanOption.errorEstimate()
                exerciseProbability = americanOption.resultScalar("exerciseProbability")

                americanOption.setPricingEngine(
                    FdBlackScholesVanillaEngine(stochasticProcess, 401, 200))
                expected = americanOption.NPV()

                #  Check price
                self.assertFalse(abs(calculated - expected) > 2.34 * errorEstimate)
                #  Check exercise probability (tolerance 1.5%)
                self.assertFalse(abs(exerciseProbability - expectedExProb[i][j]) > 0.015)

    @unittest.skip("not implemented")
    def testAmericanMaxOption(self):
        #  reference values taken from
        #  "Monte Carlo Methods in Financial Engineering",
        #  by Paul Glasserman, 2004 Springer Verlag, p. 462

        TEST_MESSAGE(
            "Testing Monte-Carlo pricing of American max options...")
