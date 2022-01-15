import unittest
from utilities import *
from QuantLib import *
from math import sqrt


class DeltaData(object):
    def __init__(self,
                 ot,
                 dt,
                 spot,
                 dDf,
                 fDf,
                 stdDev,
                 strike,
                 value):
        self.ot = ot
        self.dt = dt
        self.spot = spot
        self.dDf = dDf  # domestic discount
        self.fDf = fDf  # foreign  discount
        self.stdDev = stdDev
        self.strike = strike
        self.value = value


class EuropeanOptionData(object):
    def __init__(self,
                 typeOpt,
                 strike,
                 s,
                 q,
                 r,
                 t,
                 v,
                 result,
                 tol):
        self.typeOpt = typeOpt
        self.strike = strike
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.result = result  # expected result
        self.tol = tol  # tolerance


class BlackDeltaCalculatorTest(unittest.TestCase):

    def testDeltaValues(self):
        TEST_MESSAGE("Testing delta calculator values...")

        values = [
            # Values taken from parallel implementation in R
            DeltaData(Option.Call, DeltaVolQuote.Spot, 1.421, 0.997306, 0.992266, 0.1180654, 1.608080, 0.15),
            DeltaData(Option.Call, DeltaVolQuote.PaSpot, 1.421, 0.997306, 0.992266, 0.1180654, 1.600545, 0.15),
            DeltaData(Option.Call, DeltaVolQuote.Fwd, 1.421, 0.997306, 0.992266, 0.1180654, 1.609029, 0.15),
            DeltaData(Option.Call, DeltaVolQuote.PaFwd, 1.421, 0.997306, 0.992266, 0.1180654, 1.601550, 0.15),
            DeltaData(Option.Call, DeltaVolQuote.Spot, 122.121, 0.9695434, 0.9872347, 0.0887676, 119.8031, 0.67),
            DeltaData(Option.Call, DeltaVolQuote.PaSpot, 122.121, 0.9695434, 0.9872347, 0.0887676, 117.7096, 0.67),
            DeltaData(Option.Call, DeltaVolQuote.Fwd, 122.121, 0.9695434, 0.9872347, 0.0887676, 120.0592, 0.67),
            DeltaData(Option.Call, DeltaVolQuote.PaFwd, 122.121, 0.9695434, 0.9872347, 0.0887676, 118.0532, 0.67),
            DeltaData(Option.Put, DeltaVolQuote.Spot, 3.4582, 0.99979, 0.9250616, 0.3199034, 4.964924, -0.821),
            DeltaData(Option.Put, DeltaVolQuote.PaSpot, 3.4582, 0.99979, 0.9250616, 0.3199034, 3.778327, -0.821),
            DeltaData(Option.Put, DeltaVolQuote.Fwd, 3.4582, 0.99979, 0.9250616, 0.3199034, 4.51896, -0.821),
            DeltaData(Option.Put, DeltaVolQuote.PaFwd, 3.4582, 0.99979, 0.9250616, 0.3199034, 3.65728, -0.821),
            # JPYUSD Data taken from Castagnas "FX Options and Smile Risk" (Wiley 2009)
            DeltaData(Option.Put, DeltaVolQuote.Spot, 103.00, 0.99482, 0.98508, 0.07247845, 97.47, -0.25),
            DeltaData(Option.Put, DeltaVolQuote.PaSpot, 103.00, 0.99482, 0.98508, 0.07247845, 97.22, -0.25)]

        for i in range(len(values)):
            currOt = values[i].ot
            currDt = values[i].dt
            currSpot = values[i].spot
            currdDf = values[i].dDf
            currfDf = values[i].fDf
            currStdDev = values[i].stdDev
            currStrike = values[i].strike
            currDelta = values[i].value

            myCalc = BlackDeltaCalculator(currOt, currDt, currSpot,
                                          currdDf, currfDf, currStdDev)

            tolerance = 1.0e-3

            expected = currDelta
            calculated = myCalc.deltaFromStrike(currStrike)
            error = abs(calculated - expected)

            self.assertFalse(error > tolerance)

            tolerance = 1.0e-2
            # tolerance not that small, but sufficient for strikes in
            # particular since they might be results of a numerical
            # procedure

            expected = currStrike
            calculated = myCalc.strikeFromDelta(currDelta)
            error = abs(calculated - expected)

            self.assertFalse(error > tolerance)

    def testDeltaPriceConsistency(self):
        TEST_MESSAGE("Testing premium-adjusted delta price consistency...")

        # This function tests for price consistencies with the standard
        # Black Scholes calculator, since premium adjusted deltas can be calculated
        # from spot deltas by adding/subtracting the premium.

        backup = SavedSettings()

        # actually, value and tol won't be needed for testing
        values = [
            #        type, strike,   spot,    rd,    rf,    t,  vol,   value,    tol
            EuropeanOptionData(Option.Call, 0.9123, 1.2212, 0.0231, 0.0000, 0.25, 0.301, 0.0, 0.0),
            EuropeanOptionData(Option.Call, 0.9234, 1.2212, 0.0231, 0.0000, 0.35, 0.111, 0.0, 0.0),
            EuropeanOptionData(Option.Call, 0.9783, 1.2212, 0.0231, 0.0000, 0.45, 0.071, 0.0, 0.0),
            EuropeanOptionData(Option.Call, 1.0000, 1.2212, 0.0231, 0.0000, 0.55, 0.082, 0.0, 0.0),
            EuropeanOptionData(Option.Call, 1.1230, 1.2212, 0.0231, 0.0000, 0.65, 0.012, 0.0, 0.0),
            EuropeanOptionData(Option.Call, 1.2212, 1.2212, 0.0231, 0.0000, 0.75, 0.129, 0.0, 0.0),
            EuropeanOptionData(Option.Call, 1.3212, 1.2212, 0.0231, 0.0000, 0.85, 0.034, 0.0, 0.0),
            EuropeanOptionData(Option.Call, 1.3923, 1.2212, 0.0131, 0.2344, 0.95, 0.001, 0.0, 0.0),
            EuropeanOptionData(Option.Call, 1.3455, 1.2212, 0.0000, 0.0000, 1.00, 0.127, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 0.9123, 1.2212, 0.0231, 0.0000, 0.25, 0.301, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 0.9234, 1.2212, 0.0231, 0.0000, 0.35, 0.111, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 0.9783, 1.2212, 0.0231, 0.0000, 0.45, 0.071, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 1.0000, 1.2212, 0.0231, 0.0000, 0.55, 0.082, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 1.1230, 1.2212, 0.0231, 0.0000, 0.65, 0.012, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 1.2212, 1.2212, 0.0231, 0.0000, 0.75, 0.129, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 1.3212, 1.2212, 0.0231, 0.0000, 0.85, 0.034, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 1.3923, 1.2212, 0.0131, 0.2344, 0.95, 0.001, 0.0, 0.0),
            EuropeanOptionData(Option.Put, 1.3455, 1.2212, 0.0000, 0.0000, 1.00, 0.127, 0.0, 0.0),
            # extreme case: zero vol
            EuropeanOptionData(Option.Put, 1.3455, 1.2212, 0.0000, 0.0000, 0.50, 0.000, 0.0, 0.0),
            # extreme case: zero strike
            EuropeanOptionData(Option.Put, 0.0000, 1.2212, 0.0000, 0.0000, 1.50, 0.133, 0.0, 0.0),
            # extreme case: zero strike+zero vol
            EuropeanOptionData(Option.Put, 0.0000, 1.2212, 0.0000, 0.0000, 1.00, 0.133, 0.0, 0.0)]

        dc = Actual360()
        calendar = TARGET()
        today = Date.todaysDate()

        # Start setup of market data

        discFor = 0.0
        discDom = 0.0
        implVol = 0.0
        expectedVal = 0.0
        calculatedVal = 0.0
        error = 0.0

        spotQuote = SimpleQuote(0.0)
        spotHandle = QuoteHandle(spotQuote)

        qQuote = SimpleQuote(0.0)
        qHandle = QuoteHandle(qQuote)
        qTS = FlatForward(today, qHandle, dc)

        rQuote = SimpleQuote(0.0)
        rHandle = QuoteHandle(qQuote)
        rTS = FlatForward(today, rHandle, dc)

        volQuote = SimpleQuote(0.0)
        volHandle = QuoteHandle(volQuote)
        volTS = BlackConstantVol(today, calendar, volHandle, dc)

        # Setup of market data finished

        tolerance = 1.0e-10

        for value in values:

            payoff = PlainVanillaPayoff(value.typeOpt, value.strike)
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spotQuote.setValue(value.s)
            volQuote.setValue(value.v)
            rQuote.setValue(value.r)
            qQuote.setValue(value.q)

            discDom = rTS.discount(exDate)
            discFor = qTS.discount(exDate)
            implVol = sqrt(volTS.blackVariance(exDate, 0.0))

            myCalc = BlackDeltaCalculator(
                value.typeOpt, DeltaVolQuote.PaSpot,
                spotQuote.value(), discDom, discFor, implVol)

            stochProcess = BlackScholesMertonProcess(
                spotHandle,
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = AnalyticEuropeanEngine(stochProcess)

            option = EuropeanOption(payoff, exercise)
            option.setPricingEngine(engine)

            calculatedVal = myCalc.deltaFromStrike(value.strike)

            delta = 0.0
            if implVol > 0.0:
                delta = option.delta()
            else:
                fwd = spotQuote.value() * discFor / discDom
                if payoff.optionType() == Option.Call and fwd > payoff.strike():
                    delta = 1.0
                elif payoff.optionType() == Option.Put and fwd < payoff.strike():
                    delta = -1.0

            expectedVal = delta - option.NPV() / spotQuote.value()

            error = abs(expectedVal - calculatedVal)

            self.assertFalse(error > tolerance)

            myCalc.setDeltaType(DeltaVolQuote.PaFwd)

            calculatedVal = myCalc.deltaFromStrike(value.strike)
            expectedVal = expectedVal / discFor  # Premium adjusted Fwd Delta is PA spot without discount
            error = abs(expectedVal - calculatedVal)

            self.assertFalse(error > tolerance)

            # Test consistency with BlackScholes Calculator for Spot Delta
            myCalc.setDeltaType(DeltaVolQuote.Spot)

            calculatedVal = myCalc.deltaFromStrike(value.strike)
            expectedVal = delta
            error = abs(calculatedVal - expectedVal)

            self.assertFalse(error > tolerance)

    def testPutCallParity(self):
        TEST_MESSAGE("Testing put-call parity for deltas...")

        # Test for put call parity between put and call deltas.

        backup = SavedSettings()

        # The data below are from
        # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998
        # pag 11-16

        values = [
            # pag 2-8
            #        type, strike,   spot,    q,    r,    t,  vol,   value,    tol
            EuropeanOptionData(Option.Call, 65.00, 60.00, 0.00, 0.08, 0.25, 0.30, 2.1334, 1.0e-4),
            EuropeanOptionData(Option.Put, 95.00, 100.00, 0.05, 0.10, 0.50, 0.20, 2.4648, 1.0e-4),
            EuropeanOptionData(Option.Put, 19.00, 19.00, 0.10, 0.10, 0.75, 0.28, 1.7011, 1.0e-4),
            EuropeanOptionData(Option.Call, 19.00, 19.00, 0.10, 0.10, 0.75, 0.28, 1.7011, 1.0e-4),
            EuropeanOptionData(Option.Call, 1.60, 1.56, 0.08, 0.06, 0.50, 0.12, 0.0291, 1.0e-4),
            EuropeanOptionData(Option.Put, 70.00, 75.00, 0.05, 0.10, 0.50, 0.35, 4.0870, 1.0e-4),
            # pag 24
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.15, 0.0205, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.15, 1.8734, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.15, 9.9413, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.25, 0.3150, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.25, 3.1217, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.25, 10.3556, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.10, 0.35, 0.9474, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.10, 0.35, 4.3693, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.10, 0.35, 11.1381, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.15, 0.8069, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.15, 4.0232, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.15, 10.5769, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.25, 2.7026, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.25, 6.6997, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.25, 12.7857, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 90.00, 0.10, 0.10, 0.50, 0.35, 4.9329, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 100.00, 0.10, 0.10, 0.50, 0.35, 9.3679, 1.0e-4),
            EuropeanOptionData(Option.Call, 100.00, 110.00, 0.10, 0.10, 0.50, 0.35, 15.3086, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.15, 9.9210, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.15, 1.8734, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.15, 0.0408, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.25, 10.2155, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.25, 3.1217, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.25, 0.4551, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.10, 0.35, 10.8479, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.10, 0.35, 4.3693, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.10, 0.35, 1.2376, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.15, 10.3192, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.15, 4.0232, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.15, 1.0646, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.25, 12.2149, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.25, 6.6997, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.25, 3.2734, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 90.00, 0.10, 0.10, 0.50, 0.35, 14.4452, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 100.00, 0.10, 0.10, 0.50, 0.35, 9.3679, 1.0e-4),
            EuropeanOptionData(Option.Put, 100.00, 110.00, 0.10, 0.10, 0.50, 0.35, 5.7963, 1.0e-4),
            # pag 27
            EuropeanOptionData(Option.Call, 40.00, 42.00, 0.08, 0.04, 0.75, 0.35, 5.0975, 1.0e-4)]

        dc = Actual360()
        calendar = TARGET()
        today = Date.todaysDate()

        spotQuote = SimpleQuote(0.0)

        qQuote = SimpleQuote(0.0)
        qHandle = QuoteHandle(qQuote)
        qTS = FlatForward(today, qHandle, dc)

        rQuote = SimpleQuote(0.0)
        rHandle = QuoteHandle(qQuote)
        rTS = FlatForward(today, rHandle, dc)

        volQuote = SimpleQuote(0.0)
        volHandle = QuoteHandle(volQuote)
        volTS = BlackConstantVol(today, calendar, volHandle, dc)

        tolerance = 1.0e-10

        for value in values:
            payoff = PlainVanillaPayoff(Option.Call, value.strike)
            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spotQuote.setValue(value.s)
            volQuote.setValue(value.v)
            rQuote.setValue(value.r)
            qQuote.setValue(value.q)
            discDom = rTS.discount(exDate)
            discFor = qTS.discount(exDate)
            implVol = sqrt(volTS.blackVariance(exDate, 0.0))
            forward = spotQuote.value() * discFor / discDom

            myCalc = BlackDeltaCalculator(
                Option.Call, DeltaVolQuote.Spot,
                spotQuote.value(),
                discDom, discFor, implVol)

            deltaCall = myCalc.deltaFromStrike(value.strike)

            myCalc.setOptionType(Option.Put)
            deltaPut = myCalc.deltaFromStrike(value.strike)

            myCalc.setOptionType(Option.Call)

            expectedDiff = discFor
            calculatedDiff = deltaCall - deltaPut
            error = abs(expectedDiff - calculatedDiff)

            self.assertFalse(error > tolerance)
            myCalc.setDeltaType(DeltaVolQuote.Fwd)

            deltaCall = myCalc.deltaFromStrike(value.strike)

            myCalc.setOptionType(Option.Put)
            deltaPut = myCalc.deltaFromStrike(value.strike)

            myCalc.setOptionType(Option.Call)

            expectedDiff = 1.0
            calculatedDiff = deltaCall - deltaPut
            error = abs(expectedDiff - calculatedDiff)

            self.assertFalse(error > tolerance)

            myCalc.setDeltaType(DeltaVolQuote.PaSpot)

            deltaCall = myCalc.deltaFromStrike(value.strike)

            myCalc.setOptionType(Option.Put)
            deltaPut = myCalc.deltaFromStrike(value.strike)

            myCalc.setOptionType(Option.Call)

            expectedDiff = discFor * value.strike / forward
            calculatedDiff = deltaCall - deltaPut
            error = abs(expectedDiff - calculatedDiff)

            self.assertFalse(error > tolerance)

            myCalc.setDeltaType(DeltaVolQuote.PaFwd)

            deltaCall = myCalc.deltaFromStrike(value.strike)

            myCalc.setOptionType(Option.Put)
            deltaPut = myCalc.deltaFromStrike(value.strike)

            myCalc.setOptionType(Option.Call)

            expectedDiff = value.strike / forward
            calculatedDiff = deltaCall - deltaPut
            error = abs(expectedDiff - calculatedDiff)

            self.assertFalse(error > tolerance)

    def testAtmCalcs(self):
        TEST_MESSAGE("Testing delta-neutral ATM quotations...")

        backup = SavedSettings()

        values = [
            DeltaData(Option.Call, DeltaVolQuote.Spot, 1.421, 0.997306, 0.992266, 0.1180654, 1.608080, 0.15),
            DeltaData(Option.Call, DeltaVolQuote.PaSpot, 1.421, 0.997306, 0.992266, 0.1180654, 1.600545, 0.15),
            DeltaData(Option.Call, DeltaVolQuote.Fwd, 1.421, 0.997306, 0.992266, 0.1180654, 1.609029, 0.15),
            DeltaData(Option.Call, DeltaVolQuote.PaFwd, 1.421, 0.997306, 0.992266, 0.1180654, 1.601550, 0.15),
            DeltaData(Option.Call, DeltaVolQuote.Spot, 122.121, 0.9695434, 0.9872347, 0.0887676, 119.8031, 0.67),
            DeltaData(Option.Call, DeltaVolQuote.PaSpot, 122.121, 0.9695434, 0.9872347, 0.0887676, 117.7096, 0.67),
            DeltaData(Option.Call, DeltaVolQuote.Fwd, 122.121, 0.9695434, 0.9872347, 0.0887676, 120.0592, 0.67),
            DeltaData(Option.Call, DeltaVolQuote.PaFwd, 122.121, 0.9695434, 0.9872347, 0.0887676, 118.0532, 0.67),
            DeltaData(Option.Put, DeltaVolQuote.Spot, 3.4582, 0.99979, 0.9250616, 0.3199034, 4.964924, -0.821),
            DeltaData(Option.Put, DeltaVolQuote.PaSpot, 3.4582, 0.99979, 0.9250616, 0.3199034, 3.778327, -0.821),
            DeltaData(Option.Put, DeltaVolQuote.Fwd, 3.4582, 0.99979, 0.9250616, 0.3199034, 4.51896, -0.821),
            DeltaData(Option.Put, DeltaVolQuote.PaFwd, 3.4582, 0.99979, 0.9250616, 0.3199034, 3.65728, -0.821),
            # Data taken from Castagnas "FX Options and Smile Risk" (Wiley 2009)
            DeltaData(Option.Put, DeltaVolQuote.Spot, 103.00, 0.99482, 0.98508, 0.07247845, 97.47, -0.25),
            DeltaData(Option.Put, DeltaVolQuote.PaSpot, 103.00, 0.99482, 0.98508, 0.07247845, 97.22, -0.25),
            # Extreme case: zero vol, ATM Fwd strike
            DeltaData(Option.Call, DeltaVolQuote.Fwd, 103.00, 0.99482, 0.98508, 0.0, 101.0013, 0.5),
            DeltaData(Option.Call, DeltaVolQuote.Spot, 103.00, 0.99482, 0.98508, 0.0, 101.0013, 0.99482 * 0.5)]

        tolerance = 1.0e-2  # not that small, but sufficient for strikes

        for i in range(len(values)):
            currDt = values[i].dt
            currSpot = values[i].spot
            currdDf = values[i].dDf
            currfDf = values[i].fDf
            currStdDev = values[i].stdDev
            currFwd = currSpot * currfDf / currdDf

            myCalc = BlackDeltaCalculator(
                Option.Call, currDt, currSpot, currdDf,
                currfDf, currStdDev)

            currAtmStrike = myCalc.atmStrike(DeltaVolQuote.AtmDeltaNeutral)
            currCallDelta = myCalc.deltaFromStrike(currAtmStrike)
            myCalc.setOptionType(Option.Put)
            currPutDelta = myCalc.deltaFromStrike(currAtmStrike)
            myCalc.setOptionType(Option.Call)

            expected = 0.0
            calculated = currCallDelta + currPutDelta
            error = abs(calculated - expected)

            self.assertFalse(error > tolerance)

            myCalc.setDeltaType(DeltaVolQuote.Fwd)
            currAtmStrike = myCalc.atmStrike(DeltaVolQuote.AtmDeltaNeutral)
            currCallDelta = myCalc.deltaFromStrike(currAtmStrike)
            myCalc.setOptionType(Option.Put)
            currPutDelta = myCalc.deltaFromStrike(currAtmStrike)
            myCalc.setOptionType(Option.Call)

            expected = 0.0
            calculated = currCallDelta + currPutDelta
            error = abs(calculated - expected)

            self.assertFalse(error > tolerance)

            myCalc.setDeltaType(DeltaVolQuote.PaSpot)
            currAtmStrike = myCalc.atmStrike(DeltaVolQuote.AtmDeltaNeutral)
            currCallDelta = myCalc.deltaFromStrike(currAtmStrike)
            myCalc.setOptionType(Option.Put)
            currPutDelta = myCalc.deltaFromStrike(currAtmStrike)
            myCalc.setOptionType(Option.Call)

            expected = 0.0
            calculated = currCallDelta + currPutDelta
            error = abs(calculated - expected)

            self.assertFalse(error > tolerance)

            myCalc.setDeltaType(DeltaVolQuote.PaFwd)
            currAtmStrike = myCalc.atmStrike(DeltaVolQuote.AtmDeltaNeutral)
            currCallDelta = myCalc.deltaFromStrike(currAtmStrike)
            myCalc.setOptionType(Option.Put)
            currPutDelta = myCalc.deltaFromStrike(currAtmStrike)
            myCalc.setOptionType(Option.Call)

            expected = 0.0
            calculated = currCallDelta + currPutDelta
            error = abs(calculated - expected)

            self.assertFalse(error > tolerance)

            # Test ATM forward Calculations
            calculated = myCalc.atmStrike(DeltaVolQuote.AtmFwd)
            expected = currFwd
            error = abs(expected - calculated)

            self.assertFalse(error > tolerance)

            # Test ATM 0.50 delta calculations
            myCalc.setDeltaType(DeltaVolQuote.Fwd)
            atmFiftyStrike = myCalc.atmStrike(DeltaVolQuote.AtmPutCall50)
            calculated = abs(myCalc.deltaFromStrike(atmFiftyStrike))
            expected = 0.50
            error = abs(expected - calculated)

            self.assertFalse(error > tolerance)
