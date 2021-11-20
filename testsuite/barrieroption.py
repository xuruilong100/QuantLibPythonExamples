import unittest
from utilities import *
from QuantLib import *
from math import log, sqrt


class BarrierOptionData(object):
    def __init__(self,
                 typeOpt,
                 volatility,
                 strike,
                 barrier,
                 callValue,
                 putValue):
        self.type = typeOpt
        self.volatility = volatility
        self.strike = strike
        self.barrier = barrier
        self.callValue = callValue
        self.putValue = putValue


class NewBarrierOptionData(object):
    def __init__(self,
                 barrierType,
                 barrier,
                 rebate,
                 typeOpt,
                 exType,
                 strike,
                 s,
                 q,
                 r,
                 t,
                 v,
                 result,
                 tol):
        self.barrierType = barrierType
        self.barrier = barrier
        self.rebate = rebate
        self.type = typeOpt
        self.exType = exType
        self.strike = strike
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.result = result  # result
        self.tol = tol  # tolerance


class BarrierFxOptionData(object):
    def __init__(self,
                 barrierType,
                 barrier,
                 rebate,
                 typeOpt,
                 strike,
                 s,
                 q,
                 r,
                 t,
                 vol25Put,
                 volAtm,
                 vol25Call,
                 v,
                 result,
                 tol):
        self.barrierType = barrierType
        self.barrier = barrier
        self.rebate = rebate
        self.type = typeOpt
        self.strike = strike
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.vol25Put = vol25Put  # 25 delta put vol
        self.volAtm = volAtm  # atm vol
        self.vol25Call = vol25Call  # 25 delta call vol
        self.v = v  # volatility
        self.result = result  # result
        self.tol = tol  # tolerance


class BarrierOptionTest(unittest.TestCase):
    def testParity(self):
        TEST_MESSAGE(
            "Testing that knock-in plus knock-out barrier options "
            "replicate a European option...")
        today = Date(16, Sep, 2015)
        Settings.instance().evaluationDate = today

        dc = Actual360()

        spot = SimpleQuote(100.0)
        rTS = flatRate(today, 0.01, dc)
        volTS = flatVol(today, 0.20, dc)
        volHandle = RelinkableBlackVolTermStructureHandle(volTS)

        stochProcess = BlackScholesProcess(
            QuoteHandle(spot),
            YieldTermStructureHandle(rTS),
            volHandle)

        exerciseDate = today + Period(6, Months)

        payoff = PlainVanillaPayoff(Option.Call, 100.0)

        exercise = EuropeanExercise(exerciseDate)

        knockIn = BarrierOption(Barrier.DownIn, 90.0, 0.0, payoff, exercise)
        knockOut = BarrierOption(Barrier.DownOut, 90.0, 0.0, payoff, exercise)
        european = EuropeanOption(payoff, exercise)

        barrierEngine = AnalyticBarrierEngine(stochProcess)

        europeanEngine = AnalyticEuropeanEngine(stochProcess)

        knockIn.setPricingEngine(barrierEngine)
        knockOut.setPricingEngine(barrierEngine)
        european.setPricingEngine(europeanEngine)

        replicated = knockIn.NPV() + knockOut.NPV()
        expected = european.NPV()
        error = abs(replicated - expected)
        self.assertFalse(error > 1e-7)

        # try again with different day counters

        volHandle.linkTo(flatVol(today, 0.20, Business252(TARGET())))

        replicated = knockIn.NPV() + knockOut.NPV()
        expected = european.NPV()
        error = abs(replicated - expected)
        self.assertFalse(error > 1e-7)

    def testHaugValues(self):
        TEST_MESSAGE("Testing barrier options against Haug's values...")

        european = Exercise.European
        american = Exercise.American
        values = [
            # The data below are from
            # "Option pricing formulas", E.G. Haug, McGraw-Hill 1998 pag. 72
            #     barrierType, barrier, rebate,         type, exercise, strk,     s,    q,    r,    t,    v,  result, tol
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 9.0246, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 6.7924, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 4.8759, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 2.6789, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 2.3580, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 2.3453, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 7.7627, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 4.0109, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 2.0576, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 13.8333, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 7.8494, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 3.9795, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 14.1112, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 8.4482, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 4.5910, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 8.8334, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 7.0285, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 5.4137, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 2.6341, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 2.4389, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 2.4315, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 9.0093, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 5.1370, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 2.8517, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 14.8816, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 9.2045, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 5.3043, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 15.2098, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 9.7278, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 5.8350, 1.0e-4),
            #     barrierType, barrier, rebate,         type, exercise, strk,     s,    q,    r,    t,    v,  result, tol
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 2.2798, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 2.2947, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 2.6252, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 3.7760, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 5.4932, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 7.5187, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 2.9586, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 6.5677, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 11.9752, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 2.2845, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 5.9085, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 11.6465, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 1.4653, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 3.3721, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 7.0846, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 2.4170, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 2.4258, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 2.6246, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 4.2293, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 5.8032, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 7.5649, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 3.8769, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 7.7989, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 13.3078, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 3.3328, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 7.2636, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 12.9713, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, european, 90, 100.0, 0.04, 0.08, 0.50, 0.30, 2.0658, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, european, 100, 100.0, 0.04, 0.08, 0.50, 0.30, 4.4226, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Put, european, 110, 100.0, 0.04, 0.08, 0.50, 0.30, 8.3686, 1.0e-4),
            # Options with american exercise: values computed with 400 steps of Haug's VBA code (handles only out options)
            #     barrierType, barrier, rebate,         type, exercise, strk,     s,    q,    r,    t,    v,  result, tol
            NewBarrierOptionData(Barrier.DownOut, 95.0, 0.0, Option.Call, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 10.4655, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 0.0, Option.Call, american, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 4.5159, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 0.0, Option.Call, american, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 2.5971, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, american, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Call, american, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 0.0, Option.Call, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 11.8076, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 0.0, Option.Call, american, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 3.3993, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 3.0, Option.Call, american, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 2.3457, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 3.0, Option.Put, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 2.2795, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 0.0, Option.Put, american, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 3.3512, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 95.0, 0.0, Option.Put, american, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 11.5773, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, american, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.DownOut, 100.0, 3.0, Option.Put, american, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 3.0000, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 0.0, Option.Put, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 1.4763, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 0.0, Option.Put, american, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 3.3001, 1.0e-4),
            NewBarrierOptionData(Barrier.UpOut, 105.0, 0.0, Option.Put, american, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 10.0000, 1.0e-4),
            # some american in-options - results (roughly) verified with other numerical methods 
            #     barrierType, barrier, rebate,         type, exercise, strk,     s,    q,    r,    t,    v,  result, tol
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 7.7615, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, american, 100, 100.0, 0.04, 0.08, 0.50, 0.25, 4.0118, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 95.0, 3.0, Option.Call, american, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 2.0544, 1.0e-4),
            NewBarrierOptionData(Barrier.DownIn, 100.0, 3.0, Option.Call, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 13.8308, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, american, 90, 100.0, 0.04, 0.08, 0.50, 0.25, 14.1150, 1.0e-4),
            NewBarrierOptionData(Barrier.UpIn, 105.0, 3.0, Option.Call, american, 110, 100.0, 0.04, 0.08, 0.50, 0.25, 4.5900, 1.0e-4)]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.0)
        volTS = flatVol(today, vol, dc)

        for value in values:
            exDate = today + timeToDays(value.t)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            payoff = PlainVanillaPayoff(value.type, value.strike)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            exercise = EuropeanExercise(exDate) if value.exType == Exercise.European else AmericanExercise(exDate)
            # if (value.exType == Exercise.European)
            #     exercise = EuropeanExercise(exDate)
            # else
            #     exercise = AmericanExercise(exDate)

            barrierOption = BarrierOption(
                value.barrierType, value.barrier, value.rebate, payoff, exercise)

            if value.exType == Exercise.European:
                # these engines support only european options
                engine = AnalyticBarrierEngine(stochProcess)

                barrierOption.setPricingEngine(engine)

                calculated = barrierOption.NPV()
                expected = value.result
                error = abs(calculated - expected)
                self.assertFalse(error > value.tol)

                engine = FdBlackScholesBarrierEngine(stochProcess, 200, 400)
                barrierOption.setPricingEngine(engine)

                calculated = barrierOption.NPV()
                expected = value.result
                error = abs(calculated - expected)
                self.assertFalse(error > 5.0e-3)

            engine = BinomialCRRBarrierEngine(stochProcess, 400)
            barrierOption.setPricingEngine(engine)

            calculated = barrierOption.NPV()
            expected = value.result
            error = abs(calculated - expected)
            tol = 1.1e-2
            self.assertFalse(error > tol)

            # Note: here, to test Derman convergence, we force maxTimeSteps to 
            # timeSteps, effectively disabling Boyle-Lau barrier adjustment.
            # Production code should always enable Boyle-Lau. In most cases it
            # gives very good convergence with only a modest timeStep increment.
            engine = BinomialCRRDKBarrierEngine(stochProcess, 400)
            barrierOption.setPricingEngine(engine)
            calculated = barrierOption.NPV()
            expected = value.result
            error = abs(calculated - expected)
            tol = 4e-2
            self.assertFalse(error > tol)

    def testBabsiriValues(self):
        TEST_MESSAGE("Testing barrier options against Babsiri's values...")

        # Data from
        # "Simulating Path-Dependent Options: A New Approach"
        # - M. El Babsiri and G. Noel
        # Journal of Derivatives Winter 1998 6, 2

        values = [
            BarrierOptionData(Barrier.DownIn, 0.10, 100, 90, 0.07187, 0.0),
            BarrierOptionData(Barrier.DownIn, 0.15, 100, 90, 0.60638, 0.0),
            BarrierOptionData(Barrier.DownIn, 0.20, 100, 90, 1.64005, 0.0),
            BarrierOptionData(Barrier.DownIn, 0.25, 100, 90, 2.98495, 0.0),
            BarrierOptionData(Barrier.DownIn, 0.30, 100, 90, 4.50952, 0.0),
            BarrierOptionData(Barrier.UpIn, 0.10, 100, 110, 4.79148, 0.0),
            BarrierOptionData(Barrier.UpIn, 0.15, 100, 110, 7.08268, 0.0),
            BarrierOptionData(Barrier.UpIn, 0.20, 100, 110, 9.11008, 0.0),
            BarrierOptionData(Barrier.UpIn, 0.25, 100, 110, 11.06148, 0.0),
            BarrierOptionData(Barrier.UpIn, 0.30, 100, 110, 12.98351, 0.0)]

        underlyingPrice = 100.0
        rebate = 0.0
        r = 0.05
        q = 0.02

        dc = Actual360()
        today = Date.todaysDate()
        underlying = SimpleQuote(underlyingPrice)

        qH_SME = SimpleQuote(q)
        qTS = flatRate(today, qH_SME, dc)

        rH_SME = SimpleQuote(r)
        rTS = flatRate(today, rH_SME, dc)

        volatility = SimpleQuote(0.10)
        volTS = flatVol(today, volatility, dc)

        exDate = today + 360
        exercise = EuropeanExercise(exDate)

        for value in values:
            volatility.setValue(value.volatility)

            callPayoff = PlainVanillaPayoff(Option.Call, value.strike)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(underlying),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = AnalyticBarrierEngine(stochProcess)

            # analytic
            barrierCallOption = BarrierOption(
                value.type, value.barrier, rebate, callPayoff, exercise)
            barrierCallOption.setPricingEngine(engine)
            calculated = barrierCallOption.NPV()
            expected = value.callValue
            error = abs(calculated - expected)
            maxErrorAllowed = 1.0e-5
            self.assertFalse(error > maxErrorAllowed)

            maxMcRelativeErrorAllowed = 2.0e-2

            mcEngine = MakeMCLDBarrierEngine(stochProcess)
            mcEngine.withStepsPerYear(1)
            mcEngine.withBrownianBridge()
            mcEngine.withSamples(131071)  # 2^17-1
            mcEngine.withMaxSamples(1048575)  # 2^20-1
            mcEngine.withSeed(5)
            mcEngine = mcEngine.makeEngine()

            barrierCallOption.setPricingEngine(mcEngine)
            calculated = barrierCallOption.NPV()
            error = abs(calculated - expected) / expected
            self.assertFalse(error > maxMcRelativeErrorAllowed)

    def testBeagleholeValues(self):
        TEST_MESSAGE("Testing barrier options against Beaglehole's values...")

        # Data from
        # "Going to Extreme: Correcting Simulation Bias in Exotic
        # Option Valuation"
        # - D.R. Beaglehole, P.H. Dybvig and G. Zhou
        # Financial Analysts Journal Jan / Feb 1997 53, 1

        values = [
            BarrierOptionData(Barrier.DownOut, 0.50, 50, 45, 5.477, 0.0)]

        underlyingPrice = 50.0
        rebate = 0.0
        r = log(1.1)
        q = 0.00

        dc = Actual360()
        today = Date.todaysDate()

        underlying = SimpleQuote(underlyingPrice)

        qH_SME = SimpleQuote(q)
        qTS = flatRate(today, qH_SME, dc)

        rH_SME = SimpleQuote(r)
        rTS = flatRate(today, rH_SME, dc)

        volatility = SimpleQuote(0.10)
        volTS = flatVol(today, volatility, dc)

        exDate = today + 360
        exercise = EuropeanExercise(exDate)

        for value in values:
            volatility.setValue(value.volatility)

            callPayoff = PlainVanillaPayoff(Option.Call, value.strike)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(underlying),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = AnalyticBarrierEngine(stochProcess)

            barrierCallOption = BarrierOption(
                value.type, value.barrier, rebate, callPayoff, exercise)
            barrierCallOption.setPricingEngine(engine)
            calculated = barrierCallOption.NPV()
            expected = value.callValue
            maxErrorAllowed = 1.0e-3
            error = abs(calculated - expected)
            self.assertFalse(error > maxErrorAllowed)

            maxMcRelativeErrorAllowed = 0.01
            mcEngine = MakeMCLDBarrierEngine(stochProcess)
            mcEngine.withStepsPerYear(1)
            mcEngine.withBrownianBridge()
            mcEngine.withSamples(131071)  # 2^17-1
            mcEngine.withMaxSamples(1048575)  # 2^20-1
            mcEngine.withSeed(10)
            mcEngine = mcEngine.makeEngine()

            barrierCallOption.setPricingEngine(mcEngine)
            calculated = barrierCallOption.NPV()
            error = abs(calculated - expected) / expected
            self.assertFalse(error > maxMcRelativeErrorAllowed)

    def testPerturbative(self):
        TEST_MESSAGE("Testing perturbative engine for barrier options...")

        S = 100.0
        rebate = 0.0
        r = 0.03
        q = 0.02

        dc = Actual360()
        today = Date.todaysDate()

        underlying = SimpleQuote(S)
        qTS = flatRate(today, q, dc)
        rTS = flatRate(today, r, dc)

        dates = DateVector(2)
        vols = DoubleVector(2)

        dates[0] = today + 90
        vols[0] = 0.105
        dates[1] = today + 180
        vols[1] = 0.11

        volTS = BlackVarianceCurve(today, dates, vols, dc)

        stochProcess = BlackScholesMertonProcess(
            QuoteHandle(underlying),
            YieldTermStructureHandle(qTS),
            YieldTermStructureHandle(rTS),
            BlackVolTermStructureHandle(volTS))

        strike = 101.0
        barrier = 101.0
        exDate = today + 180

        exercise = EuropeanExercise(exDate)
        payoff = PlainVanillaPayoff(Option.Put, strike)

        option = BarrierOption(Barrier.UpOut, barrier, rebate, payoff, exercise)

        order = 0
        zeroGamma = false
        engine = PerturbativeBarrierOptionEngine(
            stochProcess, order, zeroGamma)

        option.setPricingEngine(engine)

        calculated = option.NPV()
        expected = 0.897365
        tolerance = 1.0e-6
        self.assertFalse(abs(calculated - expected) > tolerance)

        order = 1
        engine = PerturbativeBarrierOptionEngine(
            stochProcess, order, zeroGamma)

        option.setPricingEngine(engine)

        calculated = option.NPV()
        expected = 0.894374
        self.assertFalse(abs(calculated - expected) > tolerance)

    def testLocalVolAndHestonComparison(self):
        TEST_MESSAGE(
            "Testing local volatility and Heston FD engines "
            "for barrier options...")

        backup = SavedSettings()

        settlementDate = Date(5, July, 2002)
        Settings.instance().evaluationDate = settlementDate

        dayCounter = Actual365Fixed()
        calendar = TARGET()

        t = [13, 41, 75, 165, 256, 345, 524, 703]
        r = [0.0357, 0.0349, 0.0341, 0.0355, 0.0359, 0.0368, 0.0386, 0.0401]

        rates = DoubleVector(1, 0.0357)
        dates = DateVector(1, settlementDate)
        for i in range(8):
            dates.push_back(settlementDate + t[i])
            rates.push_back(r[i])

        rTS = YieldTermStructureHandle(
            ZeroCurve(dates, rates, dayCounter))
        qTS = YieldTermStructureHandle(
            flatRate(settlementDate, 0.0, dayCounter))

        s0 = QuoteHandle(SimpleQuote(4500.00))

        strikes = [
            100, 500, 2000, 3400, 3600, 3800, 4000, 4200, 4400, 4500,
            4600, 4800, 5000, 5200, 5400, 5600, 7500, 10000, 20000, 30000]

        v = [
            1.015873, 1.015873, 1.015873, 0.89729, 0.796493, 0.730914, 0.631335, 0.568895,
            0.711309, 0.711309, 0.711309, 0.641309, 0.635593, 0.583653, 0.508045, 0.463182,
            0.516034, 0.500534, 0.500534, 0.500534, 0.448706, 0.416661, 0.375470, 0.353442,
            0.516034, 0.482263, 0.447713, 0.387703, 0.355064, 0.337438, 0.316966, 0.306859,
            0.497587, 0.464373, 0.430764, 0.374052, 0.344336, 0.328607, 0.310619, 0.301865,
            0.479511, 0.446815, 0.414194, 0.361010, 0.334204, 0.320301, 0.304664, 0.297180,
            0.461866, 0.429645, 0.398092, 0.348638, 0.324680, 0.312512, 0.299082, 0.292785,
            0.444801, 0.413014, 0.382634, 0.337026, 0.315788, 0.305239, 0.293855, 0.288660,
            0.428604, 0.397219, 0.368109, 0.326282, 0.307555, 0.298483, 0.288972, 0.284791,
            0.420971, 0.389782, 0.361317, 0.321274, 0.303697, 0.295302, 0.286655, 0.282948,
            0.413749, 0.382754, 0.354917, 0.316532, 0.300016, 0.292251, 0.284420, 0.281164,
            0.400889, 0.370272, 0.343525, 0.307904, 0.293204, 0.286549, 0.280189, 0.277767,
            0.390685, 0.360399, 0.334344, 0.300507, 0.287149, 0.281380, 0.276271, 0.274588,
            0.383477, 0.353434, 0.327580, 0.294408, 0.281867, 0.276746, 0.272655, 0.271617,
            0.379106, 0.349214, 0.323160, 0.289618, 0.277362, 0.272641, 0.269332, 0.268846,
            0.377073, 0.347258, 0.320776, 0.286077, 0.273617, 0.269057, 0.266293, 0.266265,
            0.399925, 0.369232, 0.338895, 0.289042, 0.265509, 0.255589, 0.249308, 0.249665,
            0.423432, 0.406891, 0.373720, 0.314667, 0.281009, 0.263281, 0.246451, 0.242166,
            0.453704, 0.453704, 0.453704, 0.381255, 0.334578, 0.305527, 0.268909, 0.251367,
            0.517748, 0.517748, 0.517748, 0.416577, 0.364770, 0.331595, 0.287423, 0.264285]

        blackVolMatrix = Matrix(len(strikes), len(dates) - 1)
        for i in range(len(strikes)):
            for j in range(1, len(dates)):
                blackVolMatrix[i][j - 1] = v[i * (len(dates) - 1) + j - 1]

        volTS = BlackVarianceSurface(
            settlementDate,
            calendar,
            dates[1:],  # DateVector(dates.begin() + 1, dates.end()),
            strikes,
            blackVolMatrix,
            dayCounter)
        volTS.setInterpolationBicubic()
        localVolProcess = BlackScholesMertonProcess(
            s0, qTS, rTS,
            BlackVolTermStructureHandle(volTS))

        v0 = 0.195662
        kappa = 5.6628
        theta = 0.0745911
        sigma = 1.1619
        rho = -0.511493

        hestonProcess = HestonProcess(
            rTS, qTS, s0, v0,
            kappa, theta, sigma, rho)

        hestonModel = HestonModel(hestonProcess)

        fdHestonEngine = FdHestonBarrierEngine(
            hestonModel, 100, 400, 50)

        fdLocalVolEngine = FdBlackScholesBarrierEngine(
            localVolProcess,
            100, 400, 0,
            FdmSchemeDesc.Douglas(),
            true, 0.35)

        strike = s0.value()
        barrier = 3000
        rebate = 100
        exDate = settlementDate + Period(20, Months)

        payoff = PlainVanillaPayoff(Option.Put, strike)

        exercise = EuropeanExercise(exDate)

        barrierOption = BarrierOption(
            Barrier.DownOut, barrier, rebate, payoff, exercise)

        barrierOption.setPricingEngine(fdHestonEngine)
        expectedHestonNPV = 111.5
        calculatedHestonNPV = barrierOption.NPV()

        barrierOption.setPricingEngine(fdLocalVolEngine)
        expectedLocalVolNPV = 132.8
        calculatedLocalVolNPV = barrierOption.NPV()

        tol = 0.01

        self.assertFalse(
            abs(expectedHestonNPV - calculatedHestonNPV) > tol * expectedHestonNPV)
        self.assertFalse(
            abs(expectedLocalVolNPV - calculatedLocalVolNPV) > tol * expectedLocalVolNPV)

    def testVannaVolgaSimpleBarrierValues(self):
        TEST_MESSAGE("Testing barrier FX options against Vanna/Volga values...")

        backup = SavedSettings()

        values = [
            # barrierType,barrier,rebate,type,strike,s,q,r,t,vol25Put,volAtm,vol25Call,vol, result, tol
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Call, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.148127, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Call, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.075943, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Call, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.0274771, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Call, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.00573, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Call, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.00012, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Put, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.00697606, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Put, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.020078, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Put, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.0489395, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Put, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.0969877, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.5, 0, Option.Put, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.157, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Call, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.0322202, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Call, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.0241491, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Call, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.0164275, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Call, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.01, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Call, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.00489, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Put, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.000560713, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Put, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.000546804, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Put, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.000130649, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Put, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.000300828, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.5, 0, Option.Put, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.00135, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Call, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.17746, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Call, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.0994142, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Call, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.0439, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Call, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.01574, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Call, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.00501, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.00612, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.00426, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.00257, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.00122, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.00045, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Put, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.00022, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Put, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.00284, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Put, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.02032, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Put, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.058235, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.1, 0, Option.Put, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.109432, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.00017, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.00083, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Call, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.00289, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Call, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.00067784, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Call, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Call, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Call, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.17423, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.09584, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.04133, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.01452, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.00456, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Put, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.00732, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Put, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.01778, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Put, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.02875, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Put, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.0390535, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.1, 0, Option.Put, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.0489236, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.13321, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.11638, 0.00753, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.22687, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.10088, 0.02062, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.31179, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08925, 0.04907, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.38843, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08463, 0.09711, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.46047, 1.30265, 0.0003541, 0.0033871, 1, 0.10087, 0.08925, 0.08463, 0.08412, 0.15752, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Call, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.20493, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Call, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.105577, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Call, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.0358872, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Call, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.00634958, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Call, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Put, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.0108218, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Put, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.0313339, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Put, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.0751237, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Put, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.153407, 1.0e-4),
            BarrierFxOptionData(Barrier.UpOut, 1.6, 0, Option.Put, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.253767, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Call, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.05402, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Call, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.0410069, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Call, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.0279562, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Call, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.0173055, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Call, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.00764, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Put, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.000962737, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Put, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.00102637, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Put, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.000419834, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Put, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.00159277, 1.0e-4),
            BarrierFxOptionData(Barrier.UpIn, 1.6, 0, Option.Put, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.00473629, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Call, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.255098, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Call, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.145701, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Call, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.06384, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Call, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.02366, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Call, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.00764, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.00592, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.00421, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.00256, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.0012, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Call, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.0004, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Put, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Put, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.00280549, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Put, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.0279945, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Put, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.0896352, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1, 0, Option.Put, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.175182, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.00000, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.00000, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.00000, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.0002, 1.0e-4),
            BarrierFxOptionData(Barrier.DownOut, 1.3, 0, Option.Put, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.00096, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Call, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.00384783, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Call, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.000883232, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Call, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Call, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.00000, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Call, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.00000, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.25302, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.14238, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.06128, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.02245, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Call, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.00725, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Put, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.01178, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Put, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.0295548, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Put, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.047549, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Put, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.0653642, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1, 0, Option.Put, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.0833221, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.06145, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.12511, 0.01178, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.19545, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.1089, 0.03236, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.32238, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09444, 0.07554, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.44298, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09197, 0.15479, 1.0e-4),
            BarrierFxOptionData(Barrier.DownIn, 1.3, 0, Option.Put, 1.56345, 1.30265, 0.0009418, 0.0039788, 2, 0.10891, 0.09525, 0.09197, 0.09261, 0.25754, 1.0e-4)]

        dc = Actual365Fixed()
        today = Date(5, March, 2013)
        Settings.instance().evaluationDate = today

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vol25Put = SimpleQuote(0.0)
        volAtm = SimpleQuote(0.0)
        vol25Call = SimpleQuote(0.0)

        for value in values:
            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol25Put.setValue(value.vol25Put)
            volAtm.setValue(value.volAtm)
            vol25Call.setValue(value.vol25Call)

            payoff = PlainVanillaPayoff(value.type, value.strike)

            exDate = today + timeToDays(value.t, 365)
            exercise = EuropeanExercise(exDate)

            volAtmQuote = DeltaVolQuoteHandle(
                DeltaVolQuote(
                    QuoteHandle(volAtm), DeltaVolQuote.Fwd,
                    value.t, DeltaVolQuote.AtmDeltaNeutral))

            vol25PutQuote = DeltaVolQuoteHandle(
                DeltaVolQuote(
                    -0.25, QuoteHandle(vol25Put),
                    value.t, DeltaVolQuote.Fwd))

            vol25CallQuote = DeltaVolQuoteHandle(DeltaVolQuote(
                0.25, QuoteHandle(vol25Call), value.t, DeltaVolQuote.Fwd))

            barrierOption = BarrierOption(
                value.barrierType, value.barrier, value.rebate, payoff, exercise)

            bsVanillaPrice = blackFormula(
                value.type, value.strike,
                spot.value() * qTS.discount(value.t) / rTS.discount(value.t),
                value.v * sqrt(value.t), rTS.discount(value.t))
            vannaVolgaEngine = VannaVolgaBarrierEngine(
                volAtmQuote,
                vol25PutQuote,
                vol25CallQuote,
                QuoteHandle(spot),
                YieldTermStructureHandle(rTS),
                YieldTermStructureHandle(qTS),
                true,
                bsVanillaPrice)
            barrierOption.setPricingEngine(vannaVolgaEngine)

            calculated = barrierOption.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

    def testDividendBarrierOption(self):
        TEST_MESSAGE(
            "Testing barrier option pricing with discrete dividends...")

        backup = SavedSettings()

        dc = Actual365Fixed()

        today = Date(11, February, 2018)
        maturity = today + Period(1, Years)
        Settings.instance().evaluationDate = today

        spot = 100.0
        strike = 105.0
        rebate = 5.0

        barriers = [80.0, 120.0]
        barrierTypes = [Barrier.DownOut, Barrier.UpOut]

        r = 0.05
        q = 0.0
        v = 0.02

        s0 = QuoteHandle(SimpleQuote(spot))
        qTS = YieldTermStructureHandle(flatRate(today, q, dc))
        rTS = YieldTermStructureHandle(flatRate(today, r, dc))
        volTS = BlackVolTermStructureHandle(flatVol(today, v, dc))

        bsProcess = BlackScholesMertonProcess(s0, qTS, rTS, volTS)

        douglas = FdBlackScholesBarrierEngine(
            bsProcess, 100, 100, 0, FdmSchemeDesc.Douglas())

        crankNicolson = FdBlackScholesBarrierEngine(
            bsProcess, 100, 100, 0, FdmSchemeDesc.CrankNicolson())

        craigSnyed = FdBlackScholesBarrierEngine(
            bsProcess, 100, 100, 0, FdmSchemeDesc.CraigSneyd())

        hundsdorfer = FdBlackScholesBarrierEngine(
            bsProcess, 100, 100, 0, FdmSchemeDesc.Hundsdorfer())

        mol = FdBlackScholesBarrierEngine(
            bsProcess, 100, 100, 0, FdmSchemeDesc.MethodOfLines())

        trPDF2 = FdBlackScholesBarrierEngine(
            bsProcess, 100, 100, 0, FdmSchemeDesc.TrBDF2())

        hestonEngine = FdHestonBarrierEngine(
            HestonModel(
                HestonProcess(
                    rTS, qTS, s0, v * v, 1.0, v * v, 0.005, 0.0)),
            50, 101, 3)

        engines = [
            douglas, crankNicolson,
            trPDF2, craigSnyed, hundsdorfer, mol, hestonEngine]

        payoff = PlainVanillaPayoff(Option.Put, strike)

        exercise = EuropeanExercise(maturity)

        divAmount = 30
        divDate = today + Period(6, Months)

        expected = [
            rTS.discount(divDate) * rebate,
            payoff(
                (spot - divAmount * rTS.discount(divDate)) / rTS.discount(maturity)) * rTS.discount(maturity)]

        relTol = 1e-4
        for i in range(len(barriers)):
            for engine in engines:
                barrier = barriers[i]
                barrierType = barrierTypes[i]

                barrierOption = DividendBarrierOption(
                    barrierType, barrier, rebate, payoff, exercise,
                    DateVector(1, divDate),
                    DoubleVector(1, divAmount))

                barrierOption.setPricingEngine(engine)

                calculated = barrierOption.NPV()

                diff = abs(calculated - expected[i])
                self.assertFalse(diff > relTol * expected[i])
