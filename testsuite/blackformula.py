import unittest
from math import sqrt, exp

import numpy as np
from QuantLib import *

from utilities import *


class BlackFormulaTest(unittest.TestCase):

    def testBachelierImpliedVol(self):
        TEST_MESSAGE(
            "Testing Bachelier implied vol...")

        forward = 1.0
        bpvol = 0.01
        tte = 10.0
        stdDev = bpvol * sqrt(tte)
        optionType = Option.Call
        discount = 0.95

        d = [-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0]
        for i in d:
            strike = forward - i * bpvol * sqrt(tte)
            callPrem = bachelierBlackFormula(
                optionType, strike, forward, stdDev, discount)
            impliedBpVol = bachelierBlackFormulaImpliedVol(
                optionType, strike, forward, tte, callPrem, discount)

            self.assertFalse(abs(bpvol - impliedBpVol) > 1.0e-12)

    def testChambersImpliedVol(self):
        TEST_MESSAGE(
            "Testing Chambers-Nawalkha implied vol approximation...")

        types = [Option.Call, Option.Put]
        displacements = [0.0000, 0.0010, 0.0050, 0.0100, 0.0200]
        forwards = [
            -0.0010, 0.0000, 0.0050, 0.0100, 0.0200, 0.0500]
        strikes = [
            -0.0100, -0.0050, -0.0010, 0.0000, 0.0010, 0.0050,
            0.0100, 0.0200, 0.0500, 0.1000]
        stdDevs = [
            0.10, 0.15, 0.20, 0.30, 0.50, 0.60, 0.70,
            0.80, 1.00, 1.50, 2.00]
        discounts = [1.00, 0.95, 0.80, 1.10]

        tol = 5.0E-4

        for optType in types:
            for displacement in displacements:
                for forward in forwards:
                    for strike in strikes:
                        for stdDev in stdDevs:
                            for discount in discounts:
                                if forward + displacement > 0.0 and strike + displacement > 0.0:
                                    premium = blackFormula(
                                        optType, strike, forward, stdDev, discount, displacement)
                                    atmPremium = blackFormula(
                                        optType, forward, forward, stdDev, discount, displacement)
                                    iStdDev = blackFormulaImpliedStdDevChambers(
                                        optType, strike, forward, premium, atmPremium, discount, displacement)
                                    moneyness = (strike + displacement) / (forward + displacement)
                                    if moneyness > 1.0:
                                        moneyness = 1.0 / moneyness
                                    error = (iStdDev - stdDev) / stdDev * moneyness
                                    self.assertFalse(error > tol)

    def testRadoicicStefanicaImpliedVol(self):
        TEST_MESSAGE(
            "Testing Radoicic-Stefanica implied vol approximation...")

        T = 1.7
        r = 0.1
        df = exp(-r * T)

        forward = 100

        vol = 0.3
        stdDev = vol * sqrt(T)

        types = [Option.Call, Option.Put]
        strikes = [
            50, 60, 70, 80, 90, 100, 110, 125, 150, 200, 300]

        tol = 0.02

        for strike in strikes:
            for optType in types:
                payoff = PlainVanillaPayoff(optType, strike)

                marketValue = blackFormula(payoff, forward, stdDev, df)

                estVol = blackFormulaImpliedStdDevApproximationRS(
                    payoff, forward, marketValue, df) / sqrt(T)

                error = abs(estVol - vol)
                self.assertFalse(error > tol)

    def testRadoicicStefanicaLowerBound(self):
        TEST_MESSAGE(
            "Testing Radoicic-Stefanica lower bound...")

        forward = 1.0
        k = 1.2

        for s in np.arange(0.17, 2.9, 0.01):
            strike = exp(k) * forward
            c = blackFormula(Option.Call, strike, forward, s)
            estimate = blackFormulaImpliedStdDevApproximationRS(
                Option.Call, strike, forward, c)

            error = s - estimate
            self.assertFalse(np.isnan(estimate) or abs(error) > 0.05)
            self.assertFalse(c > 1e-6 and error < 0.0)

    def testImpliedVolAdaptiveSuccessiveOverRelaxation(self):
        TEST_MESSAGE(
            "Testing implied volatility calculation via "
            "adaptive successive over-relaxation...")

        backup = SavedSettings()

        dc = Actual365Fixed()
        today = Date(12, July, 2017)
        Settings.instance().evaluationDate = today

        exerciseDate = today + Period(15, Months)
        exerciseTime = dc.yearFraction(today, exerciseDate)

        rTS = flatRate(0.10, dc)
        qTS = flatRate(0.06, dc)

        df = rTS.discount(exerciseDate)

        vol = 0.20
        stdDev = vol * sqrt(exerciseTime)

        s0 = 100
        forward = s0 * qTS.discount(exerciseDate) / df

        types = [Option.Call, Option.Put]
        strikes = [50, 60, 70, 80, 90, 100, 110, 125, 150, 200]
        displacements = [0, 25, 50, 100]

        tol = 1e-8

        for strike in strikes:
            for optType in types:
                payoff = PlainVanillaPayoff(optType, strike)

                for displacement in displacements:
                    marketValue = blackFormula(
                        payoff, forward, stdDev, df, displacement)

                    impliedStdDev = blackFormulaImpliedStdDevLiRS(
                        payoff, forward, marketValue, df, displacement,
                        NullReal(), 1.0, tol, 100)

                    error = abs(impliedStdDev - stdDev)
                    self.assertFalse(error > 10 * tol)

    def testBlackFormulaForwardDerivative(self):
        TEST_MESSAGE(
            "Testing forward derivative of the Black formula...")

        strikes = [0.1, 0.5, 1.0, 2.0, 3.0]
        vol = 0.1
        self._assertBlackFormulaForwardDerivative(Option.Call, strikes, vol)
        self._assertBlackFormulaForwardDerivative(Option.Put, strikes, vol)

    def testBlackFormulaForwardDerivativeWithZeroStrike(self):
        TEST_MESSAGE(
            "Testing forward derivative of the Black formula "
            "with zero strike...")

        strikes = [0.0]
        vol = 0.1
        self._assertBlackFormulaForwardDerivative(Option.Call, strikes, vol)
        self._assertBlackFormulaForwardDerivative(Option.Put, strikes, vol)

    def testBlackFormulaForwardDerivativeWithZeroVolatility(self):
        TEST_MESSAGE(
            "Testing forward derivative of the Black formula "
            "with zero volatility...")

        strikes = [0.1, 0.5, 1.0, 2.0, 3.0]
        vol = 0.0
        self._assertBlackFormulaForwardDerivative(Option.Call, strikes, vol)
        self._assertBlackFormulaForwardDerivative(Option.Put, strikes, vol)

    def testBachelierBlackFormulaForwardDerivative(self):
        TEST_MESSAGE(
            "Testing forward derivative of the "
            "Bachelier Black formula...")

        strikes = [-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0]
        vol = 0.001
        self._assertBachelierBlackFormulaForwardDerivative(Option.Call, strikes, vol)
        self._assertBachelierBlackFormulaForwardDerivative(Option.Put, strikes, vol)

    def testBachelierBlackFormulaForwardDerivativeWithZeroVolatility(self):
        TEST_MESSAGE(
            "Testing forward derivative of the Bachelier Black formula "
            "with zero volatility...")

        strikes = [-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0]
        vol = 0.0
        self._assertBachelierBlackFormulaForwardDerivative(Option.Call, strikes, vol)
        self._assertBachelierBlackFormulaForwardDerivative(Option.Put, strikes, vol)

    def _assertBlackFormulaForwardDerivative(self,
                                             optionType,
                                             strikes,
                                             bpvol):
        forward = 1.0
        tte = 10.0
        stdDev = bpvol * sqrt(tte)
        discount = 0.95
        displacement = 0.01
        bump = 0.0001
        epsilon = 1.e-10
        optType = "Call" if optionType == Option.Call else "Put"

        for strike in strikes:
            delta = blackFormulaForwardDerivative(
                optionType, strike, forward, stdDev, discount, displacement)
            bumpedDelta = blackFormulaForwardDerivative(
                optionType, strike, forward + bump, stdDev, discount, displacement)

            basePremium = blackFormula(
                optionType, strike, forward, stdDev, discount, displacement)
            bumpedPremium = blackFormula(
                optionType, strike, forward + bump, stdDev, discount, displacement)
            deltaApprox = (bumpedPremium - basePremium) / bump

            success = (max(delta, bumpedDelta) + epsilon > deltaApprox) and \
                      (deltaApprox > min(delta, bumpedDelta) - epsilon)

            self.assertFalse(not success)

    def _assertBachelierBlackFormulaForwardDerivative(self,
                                                      optionType,
                                                      strikes,
                                                      bpvol):
        forward = 1.0
        tte = 10.0
        stdDev = bpvol * sqrt(tte)
        discount = 0.95
        bump = 0.0001
        epsilon = 1.e-10
        optType = "Call" if optionType == Option.Call else "Put"

        for strike in strikes:
            delta = bachelierBlackFormulaForwardDerivative(
                optionType, strike, forward, stdDev, discount)
            bumpedDelta = bachelierBlackFormulaForwardDerivative(
                optionType, strike, forward + bump, stdDev, discount)

            basePremium = bachelierBlackFormula(
                optionType, strike, forward, stdDev, discount)
            bumpedPremium = bachelierBlackFormula(
                optionType, strike, forward + bump, stdDev, discount)
            deltaApprox = (bumpedPremium - basePremium) / bump

            success = (max(delta, bumpedDelta) + epsilon > deltaApprox) and \
                      (deltaApprox > min(delta, bumpedDelta) - epsilon)

            self.assertFalse(not success)
