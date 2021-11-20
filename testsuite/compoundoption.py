import unittest
from utilities import *
from QuantLib import *


class CompoundOptionData(object):
    def __init__(self,
                 typeMother,
                 typeDaughter,
                 strikeMother,
                 strikeDaughter,
                 s,  # spot
                 q,  # dividend
                 r,  # risk-free rate
                 tMother,  # time to maturity
                 tDaughter,  # time to maturity
                 v,  # volatility
                 npv=None,  # expected result
                 tol=None,  # tolerance
                 delta=None,
                 gamma=None,
                 vega=None,
                 theta=None):
        self.typeMother = typeMother
        self.typeDaughter = typeDaughter
        self.strikeMother = strikeMother
        self.strikeDaughter = strikeDaughter
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.tMother = tMother  # time to maturity
        self.tDaughter = tDaughter  # time to maturity
        self.v = v  # volatility
        self.npv = npv  # expected result
        self.tol = tol  # tolerance
        self.delta = delta
        self.gamma = gamma
        self.vega = vega
        self.theta = theta


class CompoundOptionTest(unittest.TestCase):
    def testValues(self):
        TEST_MESSAGE("Testing compound-option values and greeks...")

        values = [
            # type Mother, typeDaughter, strike Mother, strike Daughter,  spot,    q,    r,    t Mother, t Daughter,  vol,   value,    tol, delta, gamma, vega, theta
            # Tolerance is taken to be pretty high with 1.0e-3, since the price/theta is very sensitive with respect to
            # the implementation of the bivariate normal - which differs in the various implementations.
            # Option Value Taken from Haug 2007, Greeks from www.sitmo.com
            CompoundOptionData(Option.Put, Option.Call, 50.0, 520.0, 500.0, 0.03, 0.08, 0.25, 0.5, 0.35, 21.1965, 1.0e-3, -0.1966, 0.0007, -32.1241, -3.3837),
            # *********************************************************
            # Option Values and Greeks taken from www.sitmo.com
            CompoundOptionData(Option.Call, Option.Call, 50.0, 520.0, 500.0, 0.03, 0.08, 0.25, 0.5, 0.35, 17.5945, 1.0e-3, 0.3219, 0.0038, 106.5185, -65.1614),
            CompoundOptionData(Option.Call, Option.Put, 50.0, 520.0, 500.0, 0.03, 0.08, 0.25, 0.5, 0.35, 18.7128, 1.0e-3, -0.2906, 0.0036, 103.3856, -46.6982),
            CompoundOptionData(Option.Put, Option.Put, 50.0, 520.0, 500.0, 0.03, 0.08, 0.25, 0.5, 0.35, 15.2601, 1.0e-3, 0.1760, 0.0005, -35.2570, -10.1126),
            # type Mother, typeDaughter, strike Mother, strike Daughter,  spot,    q,    r,    t Mother, t Daughter,  vol,   value,    tol, delta, gamma, vega, theta
            CompoundOptionData(Option.Call, Option.Call, 0.05, 1.14, 1.20, 0.0, 0.01, 0.5, 2.0, 0.11, 0.0729, 1.0e-3, 0.6614, 2.5762, 0.5812, -0.0297),
            CompoundOptionData(Option.Call, Option.Put, 0.05, 1.14, 1.20, 0.0, 0.01, 0.5, 2.0, 0.11, 0.0074, 1.0e-3, -0.1334, 1.9681, 0.2933, -0.0155),
            CompoundOptionData(Option.Put, Option.Call, 0.05, 1.14, 1.20, 0.0, 0.01, 0.5, 2.0, 0.11, 0.0021, 1.0e-3, -0.0426, 0.7252, -0.0052, -0.0058),
            CompoundOptionData(Option.Put, Option.Put, 0.05, 1.14, 1.20, 0.0, 0.01, 0.5, 2.0, 0.11, 0.0192, 1.0e-3, 0.1626, 0.1171, -0.2931, -0.0028),
            # type Mother, typeDaughter, strike Mother, strike Daughter,  spot,    q,    r,    t Mother, t Daughter,  vol,   value,    tol, delta, gamma, vega, theta
            CompoundOptionData(Option.Call, Option.Call, 10.0, 122.0, 120.0, 0.06, 0.02, 0.1, 0.7, 0.22, 0.4419, 1.0e-3, 0.1049, 0.0195, 11.3368, -6.2871),
            CompoundOptionData(Option.Call, Option.Put, 10.0, 122.0, 120.0, 0.06, 0.02, 0.1, 0.7, 0.22, 2.6112, 1.0e-3, -0.3618, 0.0337, 28.4843, -13.4124),
            CompoundOptionData(Option.Put, Option.Call, 10.0, 122.0, 120.0, 0.06, 0.02, 0.1, 0.7, 0.22, 4.1616, 1.0e-3, -0.3174, 0.0024, -26.6403, -2.2720),
            CompoundOptionData(Option.Put, Option.Put, 10.0, 122.0, 120.0, 0.06, 0.02, 0.1, 0.7, 0.22, 1.0914, 1.0e-3, 0.1748, 0.0165, -9.4928, -4.8995),
            # *********************************************************
            # *********************************************************
            # Option Values and Greeks taken from mathfinance VBA implementation
            # type Mother, typeDaughter, strike Mother, strike Daughter,  spot,    q,    r,    t Mother, t Daughter,  vol,   value,    tol, delta, gamma, vega, theta
            CompoundOptionData(Option.Call, Option.Call, 0.4, 8.2, 8.0, 0.05, 0.00, 2.0, 3.0, 0.08, 0.0099, 1.0e-3, 0.0285, 0.0688, 0.7764, -0.0027),
            CompoundOptionData(Option.Call, Option.Put, 0.4, 8.2, 8.0, 0.05, 0.00, 2.0, 3.0, 0.08, 0.9826, 1.0e-3, -0.7224, 0.2158, 2.7279, -0.3332),
            CompoundOptionData(Option.Put, Option.Call, 0.4, 8.2, 8.0, 0.05, 0.00, 2.0, 3.0, 0.08, 0.3585, 1.0e-3, -0.0720, -0.0835, -1.5633, -0.0117),
            CompoundOptionData(Option.Put, Option.Put, 0.4, 8.2, 8.0, 0.05, 0.00, 2.0, 3.0, 0.08, 0.0168, 1.0e-3, 0.0378, 0.0635, 0.3882, 0.0021),
            # type Mother, typeDaughter, strike Mother, strike Daughter,  spot,    q,    r,    t Mother, t Daughter,  vol,   value,    tol, delta, gamma, vega, theta
            CompoundOptionData(Option.Call, Option.Call, 0.02, 1.6, 1.6, 0.013, 0.022, 0.45, 0.5, 0.17, 0.0680, 1.0e-3, 0.4937, 2.1271, 0.4418, -0.0843),
            CompoundOptionData(Option.Call, Option.Put, 0.02, 1.6, 1.6, 0.013, 0.022, 0.45, 0.5, 0.17, 0.0605, 1.0e-3, -0.4169, 2.0836, 0.4330, -0.0697),
            CompoundOptionData(Option.Put, Option.Call, 0.02, 1.6, 1.6, 0.013, 0.022, 0.45, 0.5, 0.17, 0.0081, 1.0e-3, -0.0417, 0.0761, -0.0045, -0.0020),
            CompoundOptionData(Option.Put, Option.Put, 0.02, 1.6, 1.6, 0.013, 0.022, 0.45, 0.5, 0.17, 0.0078, 1.0e-3, 0.0413, 0.0326, -0.0133, -0.0016)
        ]

        backup = SavedSettings()

        calendar = TARGET()

        dc = Actual360()
        todaysDate = Settings.instance().evaluationDate

        spot = SimpleQuote(0.0)
        rRate = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        vol = SimpleQuote(0.0)

        rTS = FlatForward(0, NullCalendar(), QuoteHandle(rRate), dc)
        qTS = FlatForward(0, NullCalendar(), QuoteHandle(qRate), dc)
        volTS = BlackConstantVol(todaysDate, NullCalendar(),
                                 QuoteHandle(vol), dc)

        for value in values:
            payoffMother = PlainVanillaPayoff(value.typeMother, value.strikeMother)
            payoffDaughter = PlainVanillaPayoff(value.typeDaughter, value.strikeDaughter)

            matDateMom = todaysDate + timeToDays(value.tMother)
            matDateDaughter = todaysDate + timeToDays(value.tDaughter)

            exerciseMother = EuropeanExercise(matDateMom)
            exerciseDaughter = EuropeanExercise(matDateDaughter)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            compoundOption = CompoundOption(payoffMother, exerciseMother,
                                            payoffDaughter, exerciseDaughter)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engineCompound = AnalyticCompoundOptionEngine(stochProcess)

            compoundOption.setPricingEngine(engineCompound)

            calculated = compoundOption.NPV()
            error = abs(calculated - value.npv)  # -values[i].npv
            tolerance = value.tol

            self.assertFalse(error > tolerance)

            calculated = compoundOption.delta()
            error = abs(calculated - value.delta)
            tolerance = value.tol

            self.assertFalse(error > tolerance)

            calculated = compoundOption.gamma()
            error = abs(calculated - value.gamma)
            tolerance = value.tol

            self.assertFalse(error > tolerance)

            calculated = compoundOption.vega()
            error = abs(calculated - value.vega)
            tolerance = value.tol

            self.assertFalse(error > tolerance)

            calculated = compoundOption.theta()
            error = abs(calculated - value.theta)
            tolerance = value.tol

            self.assertFalse(error > tolerance)

    def testPutCallParity(self):
        TEST_MESSAGE("Testing compound-option put-call parity...")

        # Test Put Call Parity for compound options.
        # Formula taken from: "Foreign Exchange Risk", Wystup, Risk 2002
        # Page 81, Equation 9.5

        values = [
            # type Mother, typeDaughter, strike Mother, strike Daughter,  spot,    q,    r,    t Mother, t Daughter,  vol
            CompoundOptionData(Option.Put, Option.Call, 50.0, 520.0, 500.0, 0.03, 0.08, 0.25, 0.5, 0.35),
            CompoundOptionData(Option.Call, Option.Call, 50.0, 520.0, 500.0, 0.03, 0.08, 0.25, 0.5, 0.35),
            CompoundOptionData(Option.Call, Option.Put, 50.0, 520.0, 500.0, 0.03, 0.08, 0.25, 0.5, 0.35),
            CompoundOptionData(Option.Call, Option.Call, 0.05, 1.14, 1.20, 0.0, 0.01, 0.5, 2.0, 0.11),
            CompoundOptionData(Option.Call, Option.Put, 0.05, 1.14, 1.20, 0.0, 0.01, 0.5, 2.0, 0.11),
            CompoundOptionData(Option.Call, Option.Call, 10.0, 122.0, 120.0, 0.06, 0.02, 0.1, 0.7, 0.22),
            CompoundOptionData(Option.Call, Option.Put, 10.0, 122.0, 120.0, 0.06, 0.02, 0.1, 0.7, 0.22),
            CompoundOptionData(Option.Call, Option.Call, 0.4, 8.2, 8.0, 0.05, 0.00, 2.0, 3.0, 0.08),
            CompoundOptionData(Option.Call, Option.Put, 0.4, 8.2, 8.0, 0.05, 0.00, 2.0, 3.0, 0.08),
            CompoundOptionData(Option.Call, Option.Call, 0.02, 1.6, 1.6, 0.013, 0.022, 0.45, 0.5, 0.17),
            CompoundOptionData(Option.Call, Option.Put, 0.02, 1.6, 1.6, 0.013, 0.022, 0.45, 0.5, 0.17),
        ]

        backup = SavedSettings()

        calendar = TARGET()

        dc = Actual360()
        todaysDate = Settings.instance().evaluationDate

        spot = SimpleQuote(0.0)
        rRate = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        vol = SimpleQuote(0.0)

        rTS = FlatForward(0, NullCalendar(), QuoteHandle(rRate), dc)
        qTS = FlatForward(0, NullCalendar(), QuoteHandle(qRate), dc)
        volTS = BlackConstantVol(
            todaysDate, NullCalendar(),
            QuoteHandle(vol), dc)

        for value in values:
            payoffMotherCall = PlainVanillaPayoff(Option.Call, value.strikeMother)
            payoffMotherPut = PlainVanillaPayoff(Option.Put, value.strikeMother)
            payoffDaughter = PlainVanillaPayoff(value.typeDaughter, value.strikeDaughter)

            matDateMom = todaysDate + timeToDays(value.tMother)
            matDateDaughter = todaysDate + timeToDays(value.tDaughter)

            exerciseCompound = EuropeanExercise(matDateMom)
            exerciseDaughter = EuropeanExercise(matDateDaughter)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            compoundOptionCall = CompoundOption(payoffMotherCall, exerciseCompound,
                                                payoffDaughter, exerciseDaughter)

            compoundOptionPut = CompoundOption(payoffMotherPut, exerciseCompound,
                                               payoffDaughter, exerciseDaughter)

            vanillaOption = EuropeanOption(
                payoffDaughter, exerciseDaughter)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engineCompound = AnalyticCompoundOptionEngine(stochProcess)

            engineEuropean = AnalyticEuropeanEngine(stochProcess)

            compoundOptionCall.setPricingEngine(engineCompound)
            compoundOptionPut.setPricingEngine(engineCompound)
            vanillaOption.setPricingEngine(engineEuropean)

            discFact = rTS.discount(matDateMom)
            discStrike = value.strikeMother * discFact

            calculated = compoundOptionCall.NPV() + discStrike - compoundOptionPut.NPV() - vanillaOption.NPV()

            expected = 0.0
            error = abs(calculated - expected)
            tolerance = 1.0e-8

            self.assertFalse(error > tolerance)
