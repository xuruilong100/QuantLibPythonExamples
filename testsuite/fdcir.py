import unittest
from utilities import *
from QuantLib import *


class FdCIRTest(unittest.TestCase):

    def testFdmCIRConvergence(self):
        TEST_MESSAGE("Testing FDM CIR convergence...")

        schemes = [
            FdmSchemeDesc.Hundsdorfer(),
            FdmSchemeDesc.ModifiedCraigSneyd(),
            FdmSchemeDesc.ModifiedHundsdorfer(),
            FdmSchemeDesc.CraigSneyd(),
            FdmSchemeDesc.TrBDF2(),
            FdmSchemeDesc.CrankNicolson()]

        # set up dates
        today = Date.todaysDate()

        # our options
        typeOpt = Option.Put
        underlying = 36
        strike = 40
        dividendYield = 0.00
        riskFreeRate = 0.06
        volatility = 0.20
        maturity = today + 365
        dayCounter = Actual365Fixed()

        europeanExercise = EuropeanExercise(maturity)

        underlyingH = QuoteHandle(
            SimpleQuote(underlying))

        flatTermStructure = YieldTermStructureHandle(
            (flatRate(today, riskFreeRate, dayCounter)))
        flatDividendTS = YieldTermStructureHandle(
            (flatRate(today, dividendYield, dayCounter)))
        flatVolTS = BlackVolTermStructureHandle(
            (flatVol(today, volatility, dayCounter)))
        payoff = PlainVanillaPayoff(typeOpt, strike)
        bsmProcess = BlackScholesMertonProcess(
            underlyingH, flatDividendTS,
            flatTermStructure, flatVolTS)

        europeanOption = VanillaOption(payoff, europeanExercise)

        speed = 1.2188
        cirSigma = 0.02438
        level = 0.0183
        initialRate = 0.06
        rho = 0.00789
        lmbd = -0.5726
        newSpeed = speed + (cirSigma * lmbd)  # 1.0792
        newLevel = (level * speed) / (speed + (cirSigma * lmbd))  ## 0.0240

        cirProcess = CoxIngersollRossProcess(
            newSpeed, cirSigma, initialRate, newLevel)

        expected = 4.275
        tolerance = 0.0003

        for scheme in schemes:
            fdcirengine = MakeFdCIRVanillaEngine(cirProcess, bsmProcess, rho)
            fdcirengine.withFdmSchemeDesc(scheme)
            fdcirengine = fdcirengine.makeEngine()
            europeanOption.setPricingEngine(fdcirengine)
            calculated = europeanOption.NPV()
            self.assertFalse(abs(expected - calculated) > tolerance)
