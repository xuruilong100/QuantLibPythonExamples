import unittest
from utilities import *
from QuantLib import *


class HimalayaOptionTest(unittest.TestCase):
    def testCached(self):
        TEST_MESSAGE("Testing Himalaya option against cached values...")

        today = Settings.instance().evaluationDate

        dc = Actual360()
        fixingDates = DateVector()
        for i in range(5):
            fixingDates.push_back(today + i * 90)

        strike = 101.0
        option = HimalayaOption(fixingDates, strike)

        riskFreeRate = YieldTermStructureHandle(flatRate(today, 0.05, dc))

        processes = StochasticProcess1DVector(4)
        processes[0] = BlackScholesMertonProcess(
            QuoteHandle(SimpleQuote(100.0)),
            YieldTermStructureHandle(flatRate(today, 0.01, dc)),
            riskFreeRate,
            BlackVolTermStructureHandle(flatVol(today, 0.30, dc)))
        processes[1] = BlackScholesMertonProcess(
            QuoteHandle(SimpleQuote(110.0)),
            YieldTermStructureHandle(flatRate(today, 0.05, dc)),
            riskFreeRate,
            BlackVolTermStructureHandle(flatVol(today, 0.35, dc)))
        processes[2] = BlackScholesMertonProcess(
            QuoteHandle(SimpleQuote(90.0)),
            YieldTermStructureHandle(flatRate(today, 0.04, dc)),
            riskFreeRate,
            BlackVolTermStructureHandle(flatVol(today, 0.25, dc)))
        processes[3] = BlackScholesMertonProcess(
            QuoteHandle(SimpleQuote(105.0)),
            YieldTermStructureHandle(flatRate(today, 0.03, dc)),
            riskFreeRate,
            BlackVolTermStructureHandle(flatVol(today, 0.20, dc)))

        correlation = Matrix(4, 4)
        correlation[0][0] = 1.00
        correlation[0][1] = 0.50
        correlation[0][2] = 0.30
        correlation[0][3] = 0.10
        correlation[1][0] = 0.50
        correlation[1][1] = 1.00
        correlation[1][2] = 0.20
        correlation[1][3] = 0.40
        correlation[2][0] = 0.30
        correlation[2][1] = 0.20
        correlation[2][2] = 1.00
        correlation[2][3] = 0.60
        correlation[3][0] = 0.10
        correlation[3][1] = 0.40
        correlation[3][2] = 0.60
        correlation[3][3] = 1.00

        seed = 86421
        fixedSamples = 1023

        process = StochasticProcessArray(processes, correlation)
        mcEngine = MakeMCPRHimalayaEngine(process)
        mcEngine.withSamples(fixedSamples)
        mcEngine.withSeed(seed)
        mcEngine = mcEngine.makeEngine()

        option.setPricingEngine(mcEngine)

        value = option.NPV()
        storedValue = 5.93632056
        tolerance = 1.0e-8

        self.assertFalse(abs(value - storedValue) > tolerance)

        minimumTol = 1.0e-2
        tolerance = option.errorEstimate()
        tolerance = min(tolerance / 2.0, minimumTol * value)

        mcEngine = MakeMCPRHimalayaEngine(process)
        mcEngine.withAbsoluteTolerance(tolerance)
        mcEngine.withSeed(seed)
        mcEngine = mcEngine.makeEngine()

        option.setPricingEngine(mcEngine)

        option.NPV()
        accuracy = option.errorEstimate()
        self.assertFalse(accuracy > tolerance)
