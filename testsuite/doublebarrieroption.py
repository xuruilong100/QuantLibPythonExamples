import unittest
from utilities import *
from QuantLib import *
from math import sqrt


class NewBarrierOptionData(object):
    def __init__(self,
                 barrierType,
                 barrierlo,
                 barrierhi,
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
        self.barrierlo = barrierlo
        self.barrierhi = barrierhi
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


class DoubleBarrierFxOptionData(object):
    def __init__(self,
                 barrierType,
                 barrier1,
                 barrier2,
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
        self.barrier1 = barrier1
        self.barrier2 = barrier2
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


class DoubleBarrierOptionTest(unittest.TestCase):
    def testEuropeanHaugValues(self):
        TEST_MESSAGE("Testing double barrier european options against Haug's values...")

        european = Exercise.European
        values = [
            # /* The data below are from
            # "The complete guide to option pricing formulas 2nd Ed",E.G. Haug, McGraw-Hill, p.156 and following.

            # Note:
            # The book uses b instead of q (q=r-b)
            # */
            # //           BarrierType, barr.lo,  barr.hi,         type, exercise,strk,     s,   q,   r,    t,    v,  result, tol
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 4.3515, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 6.1644, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 7.0373, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 6.9853, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 7.9336, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 6.5088, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 4.3505, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 5.8500, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 5.7726, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 6.8082, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 6.3383, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 4.3841, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 4.3139, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 4.8293, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 3.7765, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 5.9697, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 4.0004, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 2.2563, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 3.7516, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 2.6387, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 1.4903, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 3.5805, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 1.5098, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 0.5635, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 1.2055, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 0.3098, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 0.0477, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 0.5537, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 0.0441, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 0.0011, 1.0e-4),
            # //           BarrierType, barr.lo,  barr.hi,         type, exercise,strk,     s,   q,   r,    t,    v,  result, tol
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 1.8825, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 3.7855, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 5.7191, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 2.1374, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 4.7033, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 50.0, 150.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 7.1683, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 1.8825, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 3.7845, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 5.6060, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 2.1374, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 4.6236, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 60.0, 140.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 6.1062, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 1.8825, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 3.7014, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 4.6472, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 2.1325, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 3.8944, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 70.0, 130.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 3.5868, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 1.8600, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 2.6866, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 2.0719, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 1.8883, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 1.7851, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 80.0, 120.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 0.8244, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 0.9473, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 0.3449, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 0.0578, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 0.4555, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 0.0491, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockOut, 90.0, 110.0, Option.Put, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 0.0013, 1.0e-4),
            # //           BarrierType, barr.lo,  barr.hi,         type,  strk,     s,   q,   r,    t,    v,  result, tol
            NewBarrierOptionData(DoubleBarrier.KnockIn, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 0.0000, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 0.0900, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 1.1537, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 0.0292, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 1.6487, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 50.0, 150.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 5.7321, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 0.0010, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 0.4045, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 2.4184, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 0.2062, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 3.2439, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 60.0, 140.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 7.8569, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 0.0376, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 1.4252, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 4.4145, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 1.0447, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 5.5818, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 70.0, 130.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 9.9846, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 0.5999, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 3.6158, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 6.7007, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 3.4340, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 8.0724, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 80.0, 120.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 11.6774, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.15, 3.1460, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.25, 5.9447, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.25, 0.35, 8.1432, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.15, 6.4608, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.25, 9.5382, 1.0e-4),
            NewBarrierOptionData(DoubleBarrier.KnockIn, 90.0, 110.0, Option.Call, european, 100, 100.0, 0.0, 0.1, 0.50, 0.35, 12.2398, 1.0e-4),
        ]

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
            exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            payoff = PlainVanillaPayoff(value.type, value.strike)

            stochProcess = BlackScholesMertonProcess(QuoteHandle(spot),
                                                     YieldTermStructureHandle(qTS),
                                                     YieldTermStructureHandle(rTS),
                                                     BlackVolTermStructureHandle(volTS))

            opt = DoubleBarrierOption(
                value.barrierType, value.barrierlo, value.barrierhi,
                0,  # // no rebate
                payoff, exercise)

            # // Ikeda/Kunitomo engine
            engine = AnalyticDoubleBarrierEngine(stochProcess)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

            # // Wulin Suo/Yong Wang engine
            engine = WulinYongDoubleBarrierEngine(stochProcess)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

            engine = BinomialCRRDoubleBarrierEngine(stochProcess, 300)
            opt.setPricingEngine(engine)
            calculated = opt.NPV()
            expected = value.result
            error = abs(calculated - expected)
            tol = 0.28
            self.assertFalse(error > tol)

            engine = BinomialCRRDKDoubleBarrierEngine(stochProcess, 300)
            opt.setPricingEngine(engine)
            calculated = opt.NPV()
            expected = value.result
            error = abs(calculated - expected)
            tol = 0.033  # // error one order of magnitude lower than plain binomial
            self.assertFalse(error > tol)

            if value.barrierType == DoubleBarrier.KnockOut:
                engine = FdHestonDoubleBarrierEngine(
                    HestonModel(
                        HestonProcess(
                            YieldTermStructureHandle(rTS),
                            YieldTermStructureHandle(qTS),
                            QuoteHandle(spot),
                            (vol.value()) ** 2, 1.0,
                            (vol.value()) ** 2, 0.001, 0.0)),
                    251, 76, 3)

                opt.setPricingEngine(engine)
                calculated = opt.NPV()
                expected = value.result
                error = abs(calculated - expected)

                tol = 0.025  # // error one order of magnitude lower than plain binomial
                self.assertFalse(error > tol)

    def testVannaVolgaDoubleBarrierValues(self):
        TEST_MESSAGE(
            "Testing double-barrier FX options against Vanna/Volga values...")

        backup = SavedSettings()

        values = [

            # //            BarrierType, barr.1, barr.2, rebate,         type,    strike,          s,         q,         r,  t, vol25Put,    volAtm,vol25Call,      vol,    result,   tol
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Call, 1.13321, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.11638, 0.14413, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Call, 1.22687, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.10088, 0.07456, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Call, 1.31179, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.08925, 0.02710, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Call, 1.38843, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.08463, 0.00569, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Call, 1.46047, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.08412, 0.00013, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Put, 1.13321, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.11638, 0.00017, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Put, 1.22687, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.10088, 0.00353, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Put, 1.31179, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.08925, 0.02221, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Put, 1.38843, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.08463, 0.06049, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.1, 1.5, 0.0, Option.Put, 1.46047, 1.30265, 0.0003541, 0.0033871, 1.0, 0.10087, 0.08925, 0.08463, 0.08412, 0.11103, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Call, 1.06145, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.12511, 0.19981, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Call, 1.19545, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.10890, 0.10389, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Call, 1.32238, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.09444, 0.03555, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Call, 1.44298, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.09197, 0.00634, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Call, 1.56345, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.09261, 0.00000, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Put, 1.06145, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.12511, 0.00000, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Put, 1.19545, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.10890, 0.00436, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Put, 1.32238, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.09444, 0.03173, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Put, 1.44298, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.09197, 0.09346, 1.0e-4),
            DoubleBarrierFxOptionData(DoubleBarrier.KnockOut, 1.0, 1.6, 0.0, Option.Put, 1.56345, 1.30265, 0.0009418, 0.0039788, 2.0, 0.10891, 0.09525, 0.09197, 0.09261, 0.17704, 1.0e-4)
        ]

        dc = Actual360()
        today = Date(5, Mar, 2013)
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
            for j in range(1 + 1):

                barrierType = j  # static_cast<DoubleBarrier.Type>(j)

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
                        QuoteHandle(volAtm), DeltaVolQuote.Fwd, value.t,
                        DeltaVolQuote.AtmDeltaNeutral))

                # // always delta neutral atm
                vol25PutQuote = DeltaVolQuoteHandle(
                    DeltaVolQuote(
                        -0.25, QuoteHandle(vol25Put), value.t, DeltaVolQuote.Fwd))

                vol25CallQuote = DeltaVolQuoteHandle(
                    DeltaVolQuote(
                        0.25, QuoteHandle(vol25Call), value.t, DeltaVolQuote.Fwd))

                doubleBarrierOption = DoubleBarrierOption(
                    barrierType, value.barrier1, value.barrier2,
                    value.rebate, payoff, exercise)

                bsVanillaPrice = blackFormula(value.type, value.strike,
                                              spot.value() * qTS.discount(value.t) / rTS.discount(value.t),
                                              value.v * sqrt(value.t), rTS.discount(value.t))
                vannaVolgaEngine = VannaVolgaWYDoubleBarrierEngine(
                    volAtmQuote,
                    vol25PutQuote,
                    vol25CallQuote,
                    QuoteHandle(spot),
                    YieldTermStructureHandle(rTS),
                    YieldTermStructureHandle(qTS),
                    true,
                    bsVanillaPrice)
                doubleBarrierOption.setPricingEngine(vannaVolgaEngine)

                # // Expected result for KO is given in array, for KI is evaluated as vanilla - KO
                expected = 0
                if barrierType == DoubleBarrier.KnockOut:
                    expected = value.result
                elif barrierType == DoubleBarrier.KnockIn:
                    expected = (bsVanillaPrice - value.result)

                calculated = doubleBarrierOption.NPV()
                error = abs(calculated - expected)
                self.assertFalse(error > value.tol)

                vannaVolgaEngine = VannaVolgaIKDoubleBarrierEngine(
                    volAtmQuote,
                    vol25PutQuote,
                    vol25CallQuote,
                    QuoteHandle(spot),
                    YieldTermStructureHandle(rTS),
                    YieldTermStructureHandle(qTS),
                    true,
                    bsVanillaPrice)
                doubleBarrierOption.setPricingEngine(vannaVolgaEngine)

                calculated = doubleBarrierOption.NPV()
                error = abs(calculated - expected)
                maxtol = 5.0e-3  # // different engines have somewhat different results
                self.assertFalse(error > maxtol)

    def testMonteCarloDoubleBarrierWithAnalytical(self):
        TEST_MESSAGE("Testing MC double-barrier options against analytical values...")

        backup = SavedSettings()

        tolerance = 0.01  # //percentage difference between analytical and monte carlo values to be tolerated

        # // set up dates
        calendar = TARGET()
        todaysDate = Date(15, May, 1998)
        settlementDate = Date(17, May, 1998)
        Settings.instance().evaluationDate = todaysDate

        # // our options
        typeOpt = Option.Put
        underlying = 36
        strike = 40
        dividendYield = 0.00
        riskFreeRate = 0.06
        volatility = 0.20
        maturity = Date(17, May, 1999)
        dayCounter = Actual365Fixed()

        exerciseDates = DateVector()
        for i in range(1, 4 + 1):
            exerciseDates.push_back(settlementDate + 3 * i * Months)

        europeanExercise = EuropeanExercise(maturity)

        underlyingH = QuoteHandle(SimpleQuote(underlying))

        # // bootstrap the yield/dividend/vol curves
        flatTermStructure = YieldTermStructureHandle(
            FlatForward(settlementDate, riskFreeRate, dayCounter))
        flatDividendTS = YieldTermStructureHandle(
            FlatForward(settlementDate, dividendYield, dayCounter))
        flatVolTS = BlackVolTermStructureHandle(
            BlackConstantVol(
                settlementDate, calendar, volatility,
                dayCounter))
        payoff = PlainVanillaPayoff(typeOpt, strike)
        bsmProcess = BlackScholesMertonProcess(
            underlyingH, flatDividendTS,
            flatTermStructure, flatVolTS)

        barrierLow = underlying * 0.9
        barrierHigh = underlying * 1.1

        knockIndoubleBarrierOption = DoubleBarrierOption(
            DoubleBarrier.KnockIn,
            barrierLow,
            barrierHigh,
            0,
            payoff,
            europeanExercise)

        analyticdoublebarrierengine = AnalyticDoubleBarrierEngine(bsmProcess)
        knockIndoubleBarrierOption.setPricingEngine(analyticdoublebarrierengine)
        analytical = knockIndoubleBarrierOption.NPV()

        mcdoublebarrierengine = MakeMCPRDoubleBarrierEngine(bsmProcess)
        mcdoublebarrierengine.withSteps(5000)
        mcdoublebarrierengine.withAntitheticVariate()
        mcdoublebarrierengine.withAbsoluteTolerance(0.5)
        mcdoublebarrierengine.withSeed(1)
        mcdoublebarrierengine = mcdoublebarrierengine.makeEngine()

        knockIndoubleBarrierOption.setPricingEngine(mcdoublebarrierengine)
        monteCarlo = knockIndoubleBarrierOption.NPV()

        percentageDiff = abs(analytical - monteCarlo) / analytical

        self.assertFalse(percentageDiff > tolerance)

        knockOutDoubleBarrierOption = DoubleBarrierOption(
            DoubleBarrier.KnockOut,
            barrierLow,
            barrierHigh,
            0,
            payoff,
            europeanExercise)

        knockOutDoubleBarrierOption.setPricingEngine(analyticdoublebarrierengine)
        analytical = knockOutDoubleBarrierOption.NPV()

        tolerance = 0.01

        mcdoublebarrierengine = MakeMCPRDoubleBarrierEngine(bsmProcess)
        mcdoublebarrierengine.withSteps(5000)
        mcdoublebarrierengine.withAntitheticVariate()
        mcdoublebarrierengine.withAbsoluteTolerance(tolerance)
        mcdoublebarrierengine.withSeed(10)
        mcdoublebarrierengine = mcdoublebarrierengine.makeEngine()

        knockOutDoubleBarrierOption.setPricingEngine(mcdoublebarrierengine)
        monteCarlo = knockOutDoubleBarrierOption.NPV()

        diff = abs(analytical - monteCarlo)

        self.assertFalse(diff > tolerance)
