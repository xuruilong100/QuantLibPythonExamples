import unittest
from utilities import *
from QuantLib import *


class MCVarianceSwapData(object):
    def __init__(self,
                 typeOpt,
                 varStrike,
                 nominal,
                 s,  # spot
                 q,  # dividend
                 r,  # risk-free rate
                 t1,  # intermediate time
                 t,  # time to maturity
                 v1,  # volatility at t1
                 v,  # volatility at t
                 result,  # result
                 tol, ):
        self.typeOpt = typeOpt
        self.varStrike = varStrike
        self.nominal = nominal
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t1 = t1  # intermediate time
        self.t = t  # time to maturity
        self.v1 = v1  # volatility at t1
        self.v = v  # volatility at t
        self.result = result  # result
        self.tol = tol  # tolerance


class ReplicatingVarianceSwapData(object):
    def __init__(self,
                 typeOpt,
                 varStrike,
                 nominal,
                 s,  # spot
                 q,  # dividend
                 r,  # risk-free rate
                 t,  # time to maturity
                 v,  # volatility at t
                 result,  # result
                 tol, ):
        self.typeOpt = typeOpt
        self.varStrike = varStrike
        self.nominal = nominal
        self.s = s  # spot
        self.q = q  # dividend
        self.r = r  # risk-free rate
        self.t = t  # time to maturity
        self.v = v  # volatility at t
        self.result = result  # result
        self.tol = tol  # tolerance


class Datum(object):
    def __init__(self,
                 typeOpt,
                 strike,
                 v):
        self.typeOpt = typeOpt
        self.strike = strike
        self.v = v


class VarianceSwapTest(unittest.TestCase):
    def testReplicatingVarianceSwap(self):
        TEST_MESSAGE("Testing variance swap with replicating cost engine...")

        values = [

            # data from "A Guide to and Variance Swaps",
            #   Derman, Kamal & Zou, 1999
            #   with maturity t corrected from 0.25 to 0.246575
            #   corresponding to Jan 1, 1999 to Apr 1, 1999

            # type, varStrike, nominal,     s,    q,    r,        t,    v,  result, tol
            ReplicatingVarianceSwapData(Position.Long, 0.04, 50000, 100.0, 0.00, 0.05, 0.246575, 0.20, 0.04189, 1.0e-4)]

        replicatingOptionData = [

            # data from "A Guide to and Variance Swaps",
            #   Derman, Kamal & Zou, 1999

            # Option.Type, strike, v
            Datum(Option.Put, 50, 0.30),
            Datum(Option.Put, 55, 0.29),
            Datum(Option.Put, 60, 0.28),
            Datum(Option.Put, 65, 0.27),
            Datum(Option.Put, 70, 0.26),
            Datum(Option.Put, 75, 0.25),
            Datum(Option.Put, 80, 0.24),
            Datum(Option.Put, 85, 0.23),
            Datum(Option.Put, 90, 0.22),
            Datum(Option.Put, 95, 0.21),
            Datum(Option.Put, 100, 0.20),
            Datum(Option.Call, 100, 0.20),
            Datum(Option.Call, 105, 0.19),
            Datum(Option.Call, 110, 0.18),
            Datum(Option.Call, 115, 0.17),
            Datum(Option.Call, 120, 0.16),
            Datum(Option.Call, 125, 0.15),
            Datum(Option.Call, 130, 0.14),
            Datum(Option.Call, 135, 0.13)]

        dc = Actual365Fixed()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)

        for value in values:
            exDate = today + timeToDays(value.t, 365)
            dates = DateVector(1)
            dates[0] = exDate

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)

            options = len(replicatingOptionData)
            callStrikes = DoubleVector()
            putStrikes = DoubleVector()
            callVols = DoubleVector()
            putVols = DoubleVector()

            # Assumes ascending strikes and same min call and max put strikes
            for j in range(options):
                if replicatingOptionData[j].typeOpt == Option.Call:
                    callStrikes.push_back(replicatingOptionData[j].strike)
                    callVols.push_back(replicatingOptionData[j].v)

                elif replicatingOptionData[j].typeOpt == Option.Put:
                    putStrikes.push_back(replicatingOptionData[j].strike)
                    putVols.push_back(replicatingOptionData[j].v)

            vols = Matrix(options - 1, 1)
            strikes = DoubleVector()
            for j in range(putVols.size()):
                vols[j][0] = putVols[j]
                strikes.push_back(putStrikes[j])

            for k in range(1, callVols.size()):
                j = putVols.size() - 1
                vols[j + k][0] = callVols[k]
                strikes.push_back(callStrikes[k])

            volTS = BlackVarianceSurface(
                today, NullCalendar(), dates, strikes, vols, dc)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = ReplicatingVarianceSwapEngine(
                stochProcess, 5.0,
                callStrikes, putStrikes)

            varianceSwap = VarianceSwap(
                value.typeOpt, value.varStrike, value.nominal, today, exDate)
            varianceSwap.setPricingEngine(engine)

            calculated = varianceSwap.variance()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)

    def testMCVarianceSwap(self):
        TEST_MESSAGE("Testing variance swap with Monte Carlo engine...")

        values = [

            # data from "A Guide to and Variance Swaps",
            #   Derman, Kamal & Zou, 1999
            #   with maturity t corrected from 0.25 to 0.246575
            #   corresponding to Jan 1, 1999 to Apr 1, 1999

            # exercising code using BlackVarianceCurve because BlackVarianceSurface is unreliable
            # Result should be v*v for arbitrary t1 and v1 (as long as 0<=t1<t and 0<=v1<v)

            # type, varStrike, nominal,     s,    q,    r,  t1,     t,     v1,    v, result, tol
            MCVarianceSwapData(Position.Long, 0.04, 50000, 100.0, 0.00, 0.05, 0.1, 0.246575, 0.1, 0.20, 0.04, 3.0e-4)]

        dc = Actual365Fixed()
        today = Date.todaysDate()

        spot = SimpleQuote(0.0)
        qRate = SimpleQuote(0.0)
        qTS = flatRate(today, qRate, dc)
        rRate = SimpleQuote(0.0)
        rTS = flatRate(today, rRate, dc)
        vols = DoubleVector(2)
        dates = DateVector(2)

        for value in values:
            exDate = today + timeToDays(value.t, 365)
            intermDate = today + timeToDays(value.t1, 365)
            exercise = EuropeanExercise(exDate)
            dates[0] = intermDate
            dates[1] = exDate

            spot.setValue(value.s)
            qRate.setValue(value.q)
            rRate.setValue(value.r)
            vols[0] = value.v1
            vols[1] = value.v

            volTS = BlackVarianceCurve(today, dates, vols, dc, true)

            stochProcess = BlackScholesMertonProcess(
                QuoteHandle(spot),
                YieldTermStructureHandle(qTS),
                YieldTermStructureHandle(rTS),
                BlackVolTermStructureHandle(volTS))

            engine = MakeMCPRVarianceSwapEngine(stochProcess)
            engine.withStepsPerYear(250)
            engine.withSamples(1023)
            engine.withSeed(42)
            engine = engine.makeEngine()

            varianceSwap = VarianceSwap(
                value.typeOpt, value.varStrike,
                value.nominal, today, exDate)
            varianceSwap.setPricingEngine(engine)

            calculated = varianceSwap.variance()
            expected = value.result
            error = abs(calculated - expected)
            self.assertFalse(error > value.tol)
