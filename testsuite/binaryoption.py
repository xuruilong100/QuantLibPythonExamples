import unittest
from utilities import *
from QuantLib import *


class BinaryOptionData(object):
    def __init__(self,
                 barrierType,
                 barrier,
                 cash,
                 typeOpt,
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
        self.cash = cash  # cash payoff for cash-or-nothing
        self.typeOpt = typeOpt
        self.strike = strike
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility
        self.result = result  # expected result
        self.tol = tol  # tolerance


class BinaryOptionTest(unittest.TestCase):
    def testCashOrNothingHaugValues(self):
        TEST_MESSAGE("Testing cash-or-nothing barrier options against Haug's values...")

        values = [
            # The data below are from
            # "Option pricing formulas 2nd Ed.", E.G. Haug, McGraw-Hill 2007 pag. 180 - cases 13,14,17,18,21,22,25,26
            # Note:
            #     q is the dividend rate, while the book gives b, the cost of carry (q=r-b)
            #    barrierType, barrier,  cash,         type, strike,   spot,    q,    r,   t,  vol,   value, tol
            BinaryOptionData(Barrier.DownIn, 100.00, 15.00, Option.Call, 102.00, 105.00, 0.00, 0.10, 0.5, 0.20, 4.9289, 1e-4),
            BinaryOptionData(Barrier.DownIn, 100.00, 15.00, Option.Call, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 6.2150, 1e-4),
            # following value is wrong in book.
            BinaryOptionData(Barrier.UpIn, 100.00, 15.00, Option.Call, 102.00, 95.00, 0.00, 0.10, 0.5, 0.20, 5.8926, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 15.00, Option.Call, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 7.4519, 1e-4),
            # 17,18
            BinaryOptionData(Barrier.DownIn, 100.00, 15.00, Option.Put, 102.00, 105.00, 0.00, 0.10, 0.5, 0.20, 4.4314, 1e-4),
            BinaryOptionData(Barrier.DownIn, 100.00, 15.00, Option.Put, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 3.1454, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 15.00, Option.Put, 102.00, 95.00, 0.00, 0.10, 0.5, 0.20, 5.3297, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 15.00, Option.Put, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 3.7704, 1e-4),
            # 21,22
            BinaryOptionData(Barrier.DownOut, 100.00, 15.00, Option.Call, 102.00, 105.00, 0.00, 0.10, 0.5, 0.20, 4.8758, 1e-4),
            BinaryOptionData(Barrier.DownOut, 100.00, 15.00, Option.Call, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 4.9081, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 15.00, Option.Call, 102.00, 95.00, 0.00, 0.10, 0.5, 0.20, 0.0000, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 15.00, Option.Call, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 0.0407, 1e-4),
            # 25,26
            BinaryOptionData(Barrier.DownOut, 100.00, 15.00, Option.Put, 102.00, 105.00, 0.00, 0.10, 0.5, 0.20, 0.0323, 1e-4),
            BinaryOptionData(Barrier.DownOut, 100.00, 15.00, Option.Put, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 0.0000, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 15.00, Option.Put, 102.00, 95.00, 0.00, 0.10, 0.5, 0.20, 3.0461, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 15.00, Option.Put, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 3.0054, 1e-4),
            # other values calculated with book vba
            BinaryOptionData(Barrier.UpIn, 100.00, 15.00, Option.Call, 102.00, 95.00, -0.14, 0.10, 0.5, 0.20, 8.6806, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 15.00, Option.Call, 102.00, 95.00, 0.03, 0.10, 0.5, 0.20, 5.3112, 1e-4),
            # degenerate conditions (barrier touched)
            BinaryOptionData(Barrier.DownIn, 100.00, 15.00, Option.Call, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 7.4926, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 15.00, Option.Call, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 11.1231, 1e-4),
            # 17,18
            BinaryOptionData(Barrier.DownIn, 100.00, 15.00, Option.Put, 102.00, 98.00, 0.00, 0.10, 0.5, 0.20, 7.1344, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 15.00, Option.Put, 102.00, 101.00, 0.00, 0.10, 0.5, 0.20, 5.9299, 1e-4),
            # 21,22
            BinaryOptionData(Barrier.DownOut, 100.00, 15.00, Option.Call, 98.00, 99.00, 0.00, 0.10, 0.5, 0.20, 0.0000, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 15.00, Option.Call, 98.00, 101.00, 0.00, 0.10, 0.5, 0.20, 0.0000, 1e-4),
            # 25,26
            BinaryOptionData(Barrier.DownOut, 100.00, 15.00, Option.Put, 98.00, 99.00, 0.00, 0.10, 0.5, 0.20, 0.0000, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 15.00, Option.Put, 98.00, 101.00, 0.00, 0.10, 0.5, 0.20, 0.0000, 1e-4)
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
            payoff = CashOrNothingPayoff(value.typeOpt, value.strike, value.cash)

            exDate = today + timeToDays(value.t)
            amExercise = AmericanExercise(today, exDate, true)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))
            engine = AnalyticBinaryBarrierEngine(stochProcess)

            opt = BarrierOption(
                value.barrierType, value.barrier, 0, payoff, amExercise)

            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)

    def testAssetOrNothingHaugValues(self):
        TEST_MESSAGE("Testing asset-or-nothing barrier options against Haug's values...")

        values = [
            # The data below are from
            # "Option pricing formulas 2nd Ed.", E.G. Haug, McGraw-Hill 2007 pag. 180 - cases 15,16,19,20,23,24,27,28
            # Note:
            #     q is the dividend rate, while the book gives b, the cost of carry (q=r-b)
            #    barrierType, barrier,  cash,         type, strike,   spot,    q,    r,   t,  vol,   value, tol
            BinaryOptionData(Barrier.DownIn, 100.00, 0.00, Option.Call, 102.00, 105.00, 0.00, 0.10, 0.5, 0.20, 37.2782, 1e-4),
            BinaryOptionData(Barrier.DownIn, 100.00, 0.00, Option.Call, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 45.8530, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 0.00, Option.Call, 102.00, 95.00, 0.00, 0.10, 0.5, 0.20, 44.5294, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 0.00, Option.Call, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 54.9262, 1e-4),
            # 19,20
            BinaryOptionData(Barrier.DownIn, 100.00, 0.00, Option.Put, 102.00, 105.00, 0.00, 0.10, 0.5, 0.20, 27.5644, 1e-4),
            BinaryOptionData(Barrier.DownIn, 100.00, 0.00, Option.Put, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 18.9896, 1e-4),
            # following value is wrong in book.
            BinaryOptionData(Barrier.UpIn, 100.00, 0.00, Option.Put, 102.00, 95.00, 0.00, 0.10, 0.5, 0.20, 33.1723, 1e-4),
            BinaryOptionData(Barrier.UpIn, 100.00, 0.00, Option.Put, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 22.7755, 1e-4),
            # 23,24
            BinaryOptionData(Barrier.DownOut, 100.00, 0.00, Option.Call, 102.00, 105.00, 0.00, 0.10, 0.5, 0.20, 39.9391, 1e-4),
            BinaryOptionData(Barrier.DownOut, 100.00, 0.00, Option.Call, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 40.1574, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 0.00, Option.Call, 102.00, 95.00, 0.00, 0.10, 0.5, 0.20, 0.0000, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 0.00, Option.Call, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 0.2676, 1e-4),
            # 27,28
            BinaryOptionData(Barrier.DownOut, 100.00, 0.00, Option.Put, 102.00, 105.00, 0.00, 0.10, 0.5, 0.20, 0.2183, 1e-4),
            BinaryOptionData(Barrier.DownOut, 100.00, 0.00, Option.Put, 98.00, 105.00, 0.00, 0.10, 0.5, 0.20, 0.0000, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 0.00, Option.Put, 102.00, 95.00, 0.00, 0.10, 0.5, 0.20, 17.2983, 1e-4),
            BinaryOptionData(Barrier.UpOut, 100.00, 0.00, Option.Put, 98.00, 95.00, 0.00, 0.10, 0.5, 0.20, 17.0306, 1e-4)
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
            payoff = AssetOrNothingPayoff(value.typeOpt, value.strike)

            exDate = today + timeToDays(value.t)
            amExercise = AmericanExercise(today, exDate, true)

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vol.setValue(value.v)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))
            engine = AnalyticBinaryBarrierEngine(stochProcess)

            opt = BarrierOption(
                value.barrierType, value.barrier, 0, payoff, amExercise)

            opt.setPricingEngine(engine)

            calculated = opt.NPV()
            error = abs(calculated - value.result)
            self.assertFalse(error > value.tol)
