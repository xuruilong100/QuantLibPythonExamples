import unittest
from utilities import *
from QuantLib import *


class EngineType(object):
    Analytic = 'Analytic'
    JR = 'JR'
    CRR = 'CRR'
    EQP = 'EQP'
    TGEO = 'TGEO'
    TIAN = 'TIAN'
    LR = 'LR'
    JOSHI = 'JOSHI'


def makeProcess(u,
                q,
                r,
                vol):
    return BlackScholesMertonProcess(
        QuoteHandle(u),
        YieldTermStructureHandle(q),
        YieldTermStructureHandle(r),
        BlackVolTermStructureHandle(vol))


def makeOption(payoff,
               exercise,
               u,
               q,
               r,
               vol,
               engineType,
               binomialSteps):
    stochProcess = makeProcess(u, q, r, vol)

    engine = None

    if engineType == 'Analytic':
        engine = AnalyticEuropeanEngine(stochProcess)
    elif engineType == 'JR':
        engine = BinomialExJRVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == 'CRR':
        engine = BinomialExCRRVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == 'EQP':
        engine = BinomialExEQPVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == 'TGEO':
        engine = BinomialExTrigeorgisVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == 'TIAN':
        engine = BinomialExTianVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == 'LR':
        engine = BinomialExLRVanillaEngine(
            stochProcess, binomialSteps)
    elif engineType == 'JOSHI':
        engine = BinomialExJ4VanillaEngine(
            stochProcess, binomialSteps)

    option = EuropeanOption(payoff, exercise)
    option.setPricingEngine(engine)

    return option


class ExtendedTreesTest(unittest.TestCase):
    def testJRBinomialEngines(self):
        TEST_MESSAGE("Testing time-dependent JR binomial European engines "
                     "against analytic results...")
        backup = SavedSettings()

        engine = EngineType.JR
        steps = 251
        relativeTol = dict()
        relativeTol["value"] = 0.002
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(engine, steps, relativeTol)

    def testCRRBinomialEngines(self):
        TEST_MESSAGE("Testing time-dependent CRR binomial European engines "
                     "against analytic results...")

        backup = SavedSettings()

        engine = EngineType.CRR
        steps = 501
        relativeTol = dict()
        relativeTol["value"] = 0.02
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(engine, steps, relativeTol)

    def testEQPBinomialEngines(self):
        TEST_MESSAGE("Testing time-dependent EQP binomial European engines "
                     "against analytic results...")

        backup = SavedSettings()

        engine = EngineType.EQP
        steps = 501
        relativeTol = dict()
        relativeTol["value"] = 0.02
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(engine, steps, relativeTol)

    def testTGEOBinomialEngines(self):
        TEST_MESSAGE("Testing time-dependent TGEO binomial European engines "
                     "against analytic results...")

        backup = SavedSettings()

        engine = EngineType.TGEO
        steps = 251
        relativeTol = dict()
        relativeTol["value"] = 0.002
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(engine, steps, relativeTol)

    def testTIANBinomialEngines(self):
        TEST_MESSAGE("Testing time-dependent TIAN binomial European engines "
                     "against analytic results...")

        backup = SavedSettings()

        engine = EngineType.TIAN
        steps = 251
        relativeTol = dict()
        relativeTol["value"] = 0.002
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(engine, steps, relativeTol)

    def testLRBinomialEngines(self):
        TEST_MESSAGE("Testing time-dependent LR binomial European engines "
                     "against analytic results...")

        backup = SavedSettings()

        engine = EngineType.LR
        steps = 251
        relativeTol = dict()
        relativeTol["value"] = 1.0e-6
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(engine, steps, relativeTol)

    def testJOSHIBinomialEngines(self):
        TEST_MESSAGE("Testing time-dependent Joshi binomial European engines "
                     "against analytic results...")

        backup = SavedSettings()

        engine = EngineType.JOSHI
        steps = 251
        relativeTol = dict()
        relativeTol["value"] = 1.0e-7
        relativeTol["delta"] = 1.0e-3
        relativeTol["gamma"] = 1.0e-4
        relativeTol["theta"] = 0.03
        self._testEngineConsistency(engine, steps, relativeTol)

    def _testEngineConsistency(self,
                               engine,
                               binomialSteps,
                               tolerance):

        calculated = dict()
        expected = dict()

        # test options
        types = [Option.Call, Option.Put]
        strikes = [75.0, 100.0, 125.0]
        lengths = [1]

        # test data
        underlyings = [100.0]
        qRates = [0.00, 0.05]
        rRates = [0.01, 0.05, 0.15]
        vols = [0.11, 0.50, 1.20]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)

        for optType in types:
            for strike in strikes:
                for length in lengths:
                    exDate = today + Period(length * 360, Days)
                    exercise = EuropeanExercise(exDate)
                    payoff = PlainVanillaPayoff(optType, strike)
                    # reference option
                    refOption = makeOption(
                        payoff, exercise, spot, qTS, rTS, volTS, 'Analytic', NullSize())
                    # option to check
                    option = makeOption(
                        payoff, exercise, spot, qTS, rTS, volTS, engine, binomialSteps)

                    for u in underlyings:
                        for m in qRates:
                            for n in rRates:
                                for v in vols:
                                    q = m
                                    r = n
                                    spot.setValue(u)
                                    qRate.setValue(q)
                                    rRate.setValue(r)
                                    vol.setValue(v)

                                    expected.clear()
                                    calculated.clear()

                                    # FLOATING_POINT_EXCEPTION
                                    expected["value"] = refOption.NPV()
                                    calculated["value"] = option.NPV()

                                    if option.NPV() > spot.value() * 1.0e-5:
                                        expected["delta"] = refOption.delta()
                                        expected["gamma"] = refOption.gamma()
                                        expected["theta"] = refOption.theta()
                                        calculated["delta"] = option.delta()
                                        calculated["gamma"] = option.gamma()
                                        calculated["theta"] = option.theta()

                                    for it in calculated.keys():
                                        greek = it
                                        expct = expected[greek]
                                        calcl = calculated[greek]
                                        tol = tolerance[greek]
                                        error = relativeError(expct, calcl, u)
                                        self.assertFalse(error > tol)
