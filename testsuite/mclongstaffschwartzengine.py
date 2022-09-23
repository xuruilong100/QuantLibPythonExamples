import unittest

from QuantLib import *

from utilities import *


class MCLongstaffSchwartzEngineTest(unittest.TestCase):

    def testAmericanOption(self):
        TEST_MESSAGE(
            "Testing Monte-Carlo pricing of American options...")

        backup = SavedSettings()

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

        flatTermStructure = YieldTermStructureHandle(
            FlatForward(settlementDate, riskFreeRate, dayCounter))
        flatDividendTS = YieldTermStructureHandle(
            FlatForward(settlementDate, dividendYield, dayCounter))

        expectedExProb = Matrix(2, 3)
        expectedExProb[0][0] = 0.48013
        expectedExProb[0][1] = 0.51678
        expectedExProb[0][2] = 0.54598
        expectedExProb[1][0] = 0.75549
        expectedExProb[1][1] = 0.67569
        expectedExProb[1][2] = 0.65562

        polynomialTypes = [
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
                mcengine.withPolynomialOrder(3)
                mcengine.withBasisSystem(
                    polynomialTypes[0 * (i * 3 + j) % len(polynomialTypes)])
                mcengine = mcengine.makeEngine()

                americanOption.setPricingEngine(mcengine)
                calculated = americanOption.NPV()
                errorEstimate = americanOption.errorEstimate()
                exerciseProbability = americanOption.resultScalar("exerciseProbability")

                americanOption.setPricingEngine(
                    FdBlackScholesVanillaEngine(stochasticProcess, 401, 200))
                expected = americanOption.NPV()

                self.assertFalse(abs(calculated - expected) > 2.34 * errorEstimate)

                self.assertFalse(abs(exerciseProbability - expectedExProb[i][j]) > 0.015)

    @unittest.skip("testAmericanMaxOption")
    def testAmericanMaxOption(self):

        TEST_MESSAGE(
            "Testing Monte-Carlo pricing of American max options...")
