import unittest
from utilities import *
from QuantLib import *


class DoubleBinaryOptionData(object):
    def __init__(self,
                 barrierType,
                 barrier_lo,
                 barrier_hi,
                 cash,
                 s,
                 q,
                 r,
                 t,
                 v,
                 result,
                 tol):
        self.barrierType = barrierType
        self.barrier_lo = barrier_lo
        self.barrier_hi = barrier_hi
        self.cash = cash  # cash payoff for cash-or-nothing        
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.result = result  # expected result
        self.tol = tol  # tolerance


class DoubleBinaryOptionTest(unittest.TestCase):
    def testHaugValues(self):
        TEST_MESSAGE("Testing cash-or-nothing double barrier options against Haug's values...")

        values = [
            # /* The data below are from
            # "Option pricing formulas 2nd Ed.", E.G. Haug, McGraw-Hill 2007 pag. 181
            # Note: book uses cost of carry b, instead of dividend rate q
            # */
            #    barrierType,          bar_lo, bar_hi,  cash,   spot,    q,    r,    t,  vol,   value, tol
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 9.8716, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 8.9307, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 6.3272, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 1.9094, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 9.7961, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 7.2300, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 3.7100, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 0.4271, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 8.9054, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 3.6752, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 0.7960, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 0.0059, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 3.6323, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 0.0911, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 0.0002, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 0.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 0.2402, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 1.4076, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 3.8160, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.0075, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 0.9910, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 2.8098, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 4.6612, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.2656, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 2.7954, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 4.4024, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 4.9266, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 2.6285, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 4.7523, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 4.9096, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 4.9675, 1e-4),
            # following values calculated with haug's VBA code
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.0042, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 0.9450, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 3.5486, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 7.9663, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.0797, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 2.6458, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 6.1658, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 9.4486, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.9704, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 6.2006, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 9.0798, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 9.8699, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 6.2434, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 9.7847, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 9.8756, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 9.8758, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.0041, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 0.7080, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 2.1581, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 80.00, 120.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 4.2061, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.0723, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 1.6663, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 3.3930, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 85.00, 115.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 4.8679, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 0.7080, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 3.4424, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 4.7496, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 90.00, 110.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 5.0475, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.10, 3.6524, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.20, 5.1256, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.30, 5.0763, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 95.00, 105.00, 10.00, 100.00, 0.02, 0.05, 0.25, 0.50, 5.0275, 1e-4),
            # degenerate cases
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 95.00, 105.00, 10.00, 80.00, 0.02, 0.05, 0.25, 0.10, 0.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockOut, 95.00, 105.00, 10.00, 110.00, 0.02, 0.05, 0.25, 0.10, 0.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 95.00, 105.00, 10.00, 80.00, 0.02, 0.05, 0.25, 0.10, 10.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KnockIn, 95.00, 105.00, 10.00, 110.00, 0.02, 0.05, 0.25, 0.10, 10.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 95.00, 105.00, 10.00, 80.00, 0.02, 0.05, 0.25, 0.10, 10.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KIKO, 95.00, 105.00, 10.00, 110.00, 0.02, 0.05, 0.25, 0.10, 0.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 95.00, 105.00, 10.00, 80.00, 0.02, 0.05, 0.25, 0.10, 0.0000, 1e-4),
            DoubleBinaryOptionData(DoubleBarrier.KOKI, 95.00, 105.00, 10.00, 110.00, 0.02, 0.05, 0.25, 0.10, 10.0000, 1e-4),
        ]

        dc = Actual360()
        today = Date.todaysDate()

        spot = SimpleQuote(100.0)
        qRate = SimpleQuote(0.04)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.01)
        rTS = flatRate(today, rRate, dc)
        vol = SimpleQuote(0.25)
        volTS = flatVol(today, vol, dc)

        for value in values:

            payoff = CashOrNothingPayoff(Option.Call, 0, value.cash)

            exDate = today + timeToDays(value.t)
            exercise = None
            if value.barrierType == DoubleBarrier.KIKO or \
                    value.barrierType == DoubleBarrier.KOKI:
                exercise = AmericanExercise(today, exDate)
            else:
                exercise = EuropeanExercise(exDate)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            # checking with analytic engine
            engine = AnalyticDoubleBarrierBinaryEngine(stochProcess)
            opt = DoubleBarrierOption(
                value.barrierType, value.barrier_lo,
                value.barrier_hi, 0, payoff, exercise)
            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

            steps = 500
            # checking with binomial engine
            engine = BinomialCRRDoubleBarrierEngine(stochProcess, steps)
            opt.setPricingEngine(engine)
            calculated = opt.NPV()
            expected = value.result
            error = abs(calculated - expected)
            tol = 0.22
            self.assertFalse(error > tol)
