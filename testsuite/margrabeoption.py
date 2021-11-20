import unittest
from utilities import *
from QuantLib import *


class MargrabeAmericanOptionTwoData(object):
    def __init__(self,
                 s1,
                 s2,
                 Q1,
                 Q2,
                 q1,
                 q2,
                 r,
                 t,  # years
                 v1,
                 v2,
                 rho,
                 result,
                 tol):
        self.s1 = s1
        self.s2 = s2
        self.Q1 = Q1
        self.Q2 = Q2
        self.q1 = q1
        self.q2 = q2
        self.r = r
        self.t = t  # years
        self.v1 = v1
        self.v2 = v2
        self.rho = rho
        self.result = result
        self.tol = tol


class MargrabeOptionTwoData(object):
    def __init__(self,
                 s1,
                 s2,
                 Q1,
                 Q2,
                 q1,
                 q2,
                 r,
                 t,  # years
                 v1,
                 v2,
                 rho,
                 result,
                 delta1,
                 delta2,
                 gamma1,
                 gamma2,
                 theta,
                 rho_greek,
                 tol):
        self.s1 = s1
        self.s2 = s2
        self.Q1 = Q1
        self.Q2 = Q2
        self.q1 = q1
        self.q2 = q2
        self.r = r
        self.t = t  # years
        self.v1 = v1
        self.v2 = v2
        self.rho = rho
        self.result = result
        self.delta1 = delta1
        self.delta2 = delta2
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        self.theta = theta
        self.rho_greek = rho_greek
        self.tol = tol


class MargrabeOptionTest(unittest.TestCase):
    def testEuroExchangeTwoAssets(self):
        TEST_MESSAGE("Testing European one-asset-for-another option...")

        # Exchange-One-Asset-for-Another European Options
        values = [
            # Simplification in we assume that the option always exchanges S2 for S1
            # s1,  s2,  Q1,  Q2,  q1,  q2,  r,  t,  v1,  v2,  rho,  result,
            # delta1,  delta2,  gamma1,  gamma2,  theta, rho, tol
            # data from "given article p.52"
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.15, -0.50, 2.125, 0.841, -0.818, 0.112, 0.135, -2.043, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.20, -0.50, 2.199, 0.813, -0.784, 0.109, 0.132, -2.723, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.25, -0.50, 2.283, 0.788, -0.753, 0.105, 0.126, -3.419, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.15, 0.00, 2.045, 0.883, -0.870, 0.108, 0.131, -1.168, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.20, 0.00, 2.091, 0.857, -0.838, 0.112, 0.135, -1.698, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.25, 0.00, 2.152, 0.830, -0.805, 0.111, 0.134, -2.302, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.15, 0.50, 1.974, 0.946, -0.942, 0.079, 0.096, -0.126, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.20, 0.50, 1.989, 0.929, -0.922, 0.092, 0.111, -0.398, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.25, 0.50, 2.019, 0.902, -0.891, 0.104, 0.125, -0.838, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.15, -0.50, 2.762, 0.672, -0.602, 0.072, 0.087, -1.207, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.20, -0.50, 2.989, 0.661, -0.578, 0.064, 0.078, -1.457, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.25, -0.50, 3.228, 0.653, -0.557, 0.058, 0.070, -1.712, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.15, 0.00, 2.479, 0.695, -0.640, 0.085, 0.102, -0.874, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.20, 0.00, 2.650, 0.680, -0.616, 0.077, 0.093, -1.078, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.25, 0.00, 2.847, 0.668, -0.592, 0.069, 0.083, -1.302, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.15, 0.50, 2.138, 0.746, -0.713, 0.106, 0.128, -0.416, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.20, 0.50, 2.231, 0.728, -0.689, 0.099, 0.120, -0.550, 0.0, 1.0e-3),
            MargrabeOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.25, 0.50, 2.374, 0.707, -0.659, 0.090, 0.109, -0.741, 0.0, 1.0e-3),
            # Quantity tests from Excel calcuations
            MargrabeOptionTwoData(22.0, 10.0, 1, 2, 0.06, 0.04, 0.10, 0.50, 0.20, 0.15, 0.50, 2.138, 0.746, -1.426, 0.106, 0.255, -0.987, 0.0, 1.0e-3),
            MargrabeOptionTwoData(11.0, 20.0, 2, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.20, 0.50, 2.231, 1.455, -0.689, 0.198, 0.120, 0.410, 0.0, 1.0e-3),
            MargrabeOptionTwoData(11.0, 10.0, 2, 2, 0.06, 0.04, 0.10, 0.50, 0.20, 0.25, 0.50, 2.374, 1.413, -1.317, 0.181, 0.219, -0.336, 0.0, 1.0e-3)
        ]

        dc = Actual360()
        today = Settings.instance().evaluationDate

        spot1 = SimpleQuote(0.0)
        spot2 = SimpleQuote(0.0)
        qRate1 = SimpleQuote(0.0)
        qTS1 = flatRate(today, qRate1, dc)
        qRate2 = SimpleQuote(0.0)
        qTS2 = flatRate(today, qRate2, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol1 = SimpleQuote(0.0)
        volTS1 = flatVol(today, vol1, dc)
        vol2 = SimpleQuote(0.0)
        volTS2 = flatVol(today, vol2, dc)

        for value in values:

            exDate = today + timeToDays(value.t)
            exercise = EuropeanExercise(exDate)

            spot1.setValue(value.s1)
            spot2.setValue(value.s2)
            qRate1.setValue(value.q1)
            qRate2.setValue(value.q2)
            rRate.setValue(value.r)
            vol1.setValue(value.v1)
            vol2.setValue(value.v2)

            stochProcess1 = BlackScholesMertonProcess(
                QuoteHandle(spot1),
                YieldTermStructureHandle(qTS1),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS1))

            stochProcess2 = BlackScholesMertonProcess(
                QuoteHandle(spot2),
                YieldTermStructureHandle(qTS2),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS2))

            procs = [stochProcess1, stochProcess2]

            correlationMatrix = Matrix(2, 2, value.rho)
            for j in range(2):
                correlationMatrix[j][j] = 1.0

            engine = AnalyticEuropeanMargrabeEngine(stochProcess1, stochProcess2, value.rho)

            margrabeOption = MargrabeOption(value.Q1, value.Q2, exercise)

            # analytic engine
            margrabeOption.setPricingEngine(engine)

            calculated = margrabeOption.NPV()
            expected = value.result
            error = abs(calculated - expected)
            tolerance = value.tol
            self.assertFalse(error > tolerance)

            calculated = margrabeOption.delta1()
            expected = value.delta1
            error = abs(calculated - expected)
            self.assertFalse(error > tolerance)

            calculated = margrabeOption.delta2()
            expected = value.delta2
            error = abs(calculated - expected)
            self.assertFalse(error > tolerance)

            calculated = margrabeOption.gamma1()
            expected = value.gamma1
            error = abs(calculated - expected)
            self.assertFalse(error > tolerance)

            calculated = margrabeOption.gamma2()
            expected = value.gamma2
            error = abs(calculated - expected)
            self.assertFalse(error > tolerance)

            calculated = margrabeOption.theta()
            expected = value.theta
            error = abs(calculated - expected)
            self.assertFalse(error > tolerance)

            calculated = margrabeOption.rho()
            expected = value.rho_greek
            error = abs(calculated - expected)
            self.assertFalse(error > tolerance)

    def testAmericanExchangeTwoAssets(self):
        TEST_MESSAGE("Testing American one-asset-for-another option...")

        values = [
            # Simplification in we assume that the option always exchanges S2 for S1
            # s1, s2, Q1, Q2, q1, q2, r, t, v1, v2, rho, result, tol
            # data from Haug

            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.15, -0.50, 2.1357, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.20, -0.50, 2.2074, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.25, -0.50, 2.2902, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.15, 0.00, 2.0592, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.20, 0.00, 2.1032, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.25, 0.00, 2.1618, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.15, 0.50, 2.0001, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.20, 0.50, 2.0110, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.10, 0.20, 0.25, 0.50, 2.0359, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.15, -0.50, 2.8051, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.20, -0.50, 3.0288, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.25, -0.50, 3.2664, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.15, 0.00, 2.5282, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.20, 0.00, 2.6945, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.25, 0.00, 2.8893, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.15, 0.50, 2.2053, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.20, 0.50, 2.2906, 1.0e-3),
            MargrabeAmericanOptionTwoData(22.0, 20.0, 1, 1, 0.06, 0.04, 0.10, 0.50, 0.20, 0.25, 0.50, 2.4261, 1.0e-3)
        ]

        today = Settings.instance().evaluationDate
        dc = Actual360()
        spot1 = SimpleQuote(0.0)
        spot2 = SimpleQuote(0.0)

        qRate1 = SimpleQuote(0.0)
        qTS1 = flatRate(today, qRate1, dc)
        qRate2 = SimpleQuote(0.0)
        qTS2 = flatRate(today, qRate2, dc)

        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)

        vol1 = SimpleQuote(0.0)
        volTS1 = flatVol(today, vol1, dc)
        vol2 = SimpleQuote(0.0)
        volTS2 = flatVol(today, vol2, dc)

        for value in values:

            exDate = today + timeToDays(value.t)
            exercise = AmericanExercise(today, exDate)

            spot1.setValue(value.s1)
            spot2.setValue(value.s2)
            qRate1.setValue(value.q1)
            qRate2.setValue(value.q2)
            rRate.setValue(value.r)
            vol1.setValue(value.v1)
            vol2.setValue(value.v2)

            stochProcess1 = BlackScholesMertonProcess(
                QuoteHandle(spot1),
                YieldTermStructureHandle(qTS1),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS1))

            stochProcess2 = BlackScholesMertonProcess(
                QuoteHandle(spot2),
                YieldTermStructureHandle(qTS2),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS2))

            procs = [stochProcess1, stochProcess2]

            correlationMatrix = Matrix(2, 2, value.rho)
            for j in range(2):
                correlationMatrix[j][j] = 1.0

            engine = AnalyticAmericanMargrabeEngine(stochProcess1, stochProcess2, value.rho)

            margrabeOption = MargrabeOption(value.Q1, value.Q2, exercise)

            # analytic engine
            margrabeOption.setPricingEngine(engine)

            calculated = margrabeOption.NPV()
            expected = value.result
            error = abs(calculated - expected)
            tolerance = value.tol
            self.assertFalse(error > tolerance)

    def testGreeks(self):
        TEST_MESSAGE("Testing analytic European exchange option greeks...")

        backup = SavedSettings()

        calculated = dict()
        expected = dict()
        tolerance = dict()
        tolerance["delta1"] = 1.0e-5
        tolerance["delta2"] = 1.0e-5
        tolerance["gamma1"] = 1.0e-5
        tolerance["gamma2"] = 1.0e-5
        tolerance["theta"] = 1.0e-5
        tolerance["rho"] = 1.0e-5

        underlyings1 = [22.0]
        underlyings2 = [20.0]
        qRates1 = [0.06, 0.16, 0.04]
        qRates2 = [0.04, 0.14, 0.02]
        rRates = [0.1, 0.2, 0.08]
        residualTimes = [0.1, 0.5]
        vols1 = [0.20]
        vols2 = [0.15, 0.20, 0.25]

        dc = Actual360()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = today

        spot1 = SimpleQuote(0.0)
        spot2 = SimpleQuote(0.0)

        qRate1 = SimpleQuote(0.0)
        qTS1 = flatRate(qRate1, dc)
        qRate2 = SimpleQuote(0.0)
        qTS2 = flatRate(qRate2, dc)

        rRate = SimpleQuote(0.0)
        rTS = flatRate(rRate, dc)

        vol1 = SimpleQuote(0.0)
        volTS1 = flatVol(vol1, dc)
        vol2 = SimpleQuote(0.0)
        volTS2 = flatVol(vol2, dc)

        for residualTime in residualTimes:
            exDate = today + timeToDays(residualTime)
            exercise = EuropeanExercise(exDate)

            # option to check
            stochProcess1 = BlackScholesMertonProcess(
                QuoteHandle(spot1), YieldTermStructureHandle(qTS1), YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS1))

            stochProcess2 = BlackScholesMertonProcess(
                QuoteHandle(spot2), YieldTermStructureHandle(qTS2), YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS2))

            procs = [stochProcess1, stochProcess2]

            # The correlation -0.5 can be different real between -1 and 1 for more tests
            correlation = -0.5
            correlationMatrix = Matrix(2, 2, correlation)
            for j in range(2):
                correlationMatrix[j][j] = 1.0

                engine = AnalyticEuropeanMargrabeEngine(stochProcess1, stochProcess2, correlation)

                # The quantities of S1 and S2 can be different from 1 & 1 for more tests
                margrabeOption = MargrabeOption(1, 1, exercise)

                # analytic engine
                margrabeOption.setPricingEngine(engine)

                for i in range(len(underlyings1)):
                    for m in range(len(qRates1)):
                        for n in rRates:
                            for p in range(len(vols1)):
                                u1 = underlyings1[i]
                                u2 = underlyings2[i]

                                q1 = qRates1[m]
                                q2 = qRates2[m]
                                r = n
                                v1 = vols1[p]
                                v2 = vols2[p]

                                spot1.setValue(u1)
                                spot2.setValue(u2)
                                qRate1.setValue(q1)
                                qRate2.setValue(q2)
                                rRate.setValue(r)
                                vol1.setValue(v1)
                                vol2.setValue(v2)

                                value = margrabeOption.NPV()

                                calculated["delta1"] = margrabeOption.delta1()
                                calculated["delta2"] = margrabeOption.delta2()
                                calculated["gamma1"] = margrabeOption.gamma1()
                                calculated["gamma2"] = margrabeOption.gamma2()
                                calculated["theta"] = margrabeOption.theta()
                                calculated["rho"] = margrabeOption.rho()

                                if value > spot1.value() * 1.0e-5:
                                    # perturb spot and get delta1 and gamma
                                    u = u1
                                    du = u * 1.0e-4
                                    spot1.setValue(u + du)
                                    value_p = margrabeOption.NPV()
                                    delta_p = margrabeOption.delta1()
                                    spot1.setValue(u - du)
                                    value_m = margrabeOption.NPV()
                                    delta_m = margrabeOption.delta1()
                                    spot1.setValue(u)
                                    expected["delta1"] = (value_p - value_m) / (2 * du)
                                    expected["gamma1"] = (delta_p - delta_m) / (2 * du)

                                    u = u2
                                    spot2.setValue(u + du)
                                    value_p = margrabeOption.NPV()
                                    delta_p = margrabeOption.delta2()
                                    spot2.setValue(u - du)
                                    value_m = margrabeOption.NPV()
                                    delta_m = margrabeOption.delta2()
                                    spot2.setValue(u)
                                    expected["delta2"] = (value_p - value_m) / (2 * du)
                                    expected["gamma2"] = (delta_p - delta_m) / (2 * du)

                                    # perturb rates and get rho
                                    dr = r * 1.0e-4
                                    rRate.setValue(r + dr)
                                    value_p = margrabeOption.NPV()
                                    rRate.setValue(r - dr)
                                    value_m = margrabeOption.NPV()
                                    rRate.setValue(r)
                                    expected["rho"] = (value_p - value_m) / (2 * dr)

                                    # perturb date and get theta
                                    dT = dc.yearFraction(today - 1, today + 1)
                                    Settings.instance().evaluationDate = today - 1
                                    value_m = margrabeOption.NPV()
                                    Settings.instance().evaluationDate = today + 1
                                    value_p = margrabeOption.NPV()
                                    Settings.instance().evaluationDate = today
                                    expected["theta"] = (value_p - value_m) / dT

                                    # compare

                                    for it in calculated.keys():
                                        greek = it
                                        expct = expected[greek]
                                        calcl = calculated[greek]
                                        tol = tolerance[greek]
                                        error = relativeError(expct, calcl, u1)
                                        self.assertFalse(error > tol)
