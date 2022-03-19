import unittest
from utilities import *
from QuantLib import *


class GsrTest(unittest.TestCase):

    def testGsrProcess(self):
        TEST_MESSAGE("Testing GSR process...")

        refDate = Settings.instance().evaluationDate

        # constant reversion, constant volatility, test conditional expectation and
        # variance against
        # existing HullWhiteForwardProcess
        # technically we test two representations of the same constant reversion
        # and volatility structure,
        # namely with and without step dates

        tol = 1E-8

        reversion = 0.01
        modelvol = 0.01

        yts0 = YieldTermStructureHandle(
            FlatForward(0, TARGET(), 0.00, Actual365Fixed()))

        stepDates0 = DateVector()
        vols0 = DoubleVector(1, modelvol)
        reversions0 = DoubleVector(1, reversion)

        stepDates1 = DateVector()
        for i in range(1, 60):
            stepDates1.append(refDate + (i * Period(6, Months)))
        vols1 = DoubleVector(stepDates1.size() + 1, modelvol)
        reversions1 = DoubleVector(stepDates1.size() + 1, reversion)

        T = 10.0
        while True:
            model = Gsr(yts0, stepDates0, vols0, reversions0, T)
            gsrProcess = model.stateProcess()
            model2 = Gsr(yts0, stepDates1, vols1, reversions1, T)
            gsrProcess2 = model2.stateProcess()

            hwProcess = HullWhiteForwardProcess(yts0, reversion, modelvol)
            hwProcess.setForwardMeasureTime(T)

            t = 0.5
            while True:
                w = 0.0
                while True:
                    xw = -0.1
                    while True:
                        hwVal = hwProcess.expectation(w, xw, t - w)
                        gsrVal = gsrProcess.expectation(w, xw, t - w)
                        gsr2Val = gsrProcess2.expectation(w, xw, t - w)
                        self.assertFalse(abs(hwVal - gsrVal) > tol)
                        self.assertFalse(abs(hwVal - gsr2Val) > tol)

                        hwVal = hwProcess.variance(w, xw, t - w)
                        gsrVal = gsrProcess.variance(w, xw, t - w)
                        gsr2Val = gsrProcess2.variance(w, xw, t - w)
                        self.assertFalse(abs(hwVal - gsrVal) > tol)
                        self.assertFalse(abs(hwVal - gsr2Val) > tol)
                        xw += 0.01
                        if xw > 0.1:
                            break
                    w += t / 5.0
                    if w > t - 0.1:
                        break
                t += T / 20.0
                if t > T - 0.1:
                    break
            T += 10.0
            if T > 30.0:
                break

        # time dependent reversion and volatility (test cases to be added)

        times = Array(2)
        vols = Array(3)
        reversions = Array(3)

        times[0] = 1.0
        times[1] = 2.0
        vols[0] = 0.2
        vols[1] = 0.3
        vols[2] = 0.4
        reversions[0] = 0.50
        reversions[1] = 0.80
        reversions[2] = 1.30

        p = GsrProcess(times, vols, reversions)
        p.setForwardMeasureTime(10.0)

        # add more test cases here ...

    def testGsrModel(self):
        TEST_MESSAGE("Testing GSR model...")

        refDate = Settings.instance().evaluationDate

        modelvol = 0.01
        reversion = 0.01

        stepDates = DateVector()  # no step dates
        vols = DoubleVector(1, modelvol)
        reversions = DoubleVector(1, reversion)

        stepDates1 = DateVector()  # artificial step dates (should yield the
        # same result)
        for i in range(1, 60):
            stepDates1.append(refDate + (i * Period(6, Months)))
        vols1 = DoubleVector(stepDates1.size() + 1, modelvol)
        reversions1 = DoubleVector(stepDates1.size() + 1, reversion)

        yts = YieldTermStructureHandle(
            FlatForward(0, TARGET(), 0.03, Actual365Fixed()))
        model = Gsr(yts, stepDates, vols, reversions, 50.0)
        model2 = Gsr(yts, stepDates1, vols1, reversions1, 50.0)
        hw = HullWhite(yts, reversion, modelvol)

        # test zerobond prices against existing HullWhite model
        # technically we test two representations of the same constant reversion
        # and volatility structure,
        # namely with and without step dates

        tol0 = 1E-8

        w = 0.1
        while True:
            t = w + 0.1
            while True:
                xw = -0.10
                while True:
                    yw = (xw - model.stateProcess().expectation(0.0, 0.0, w)) / \
                         model.stateProcess().stdDeviation(0.0, 0.0, w)
                    rw = xw + 0.03  # instantaneous forward is 0.03
                    gsrVal = model.zerobond(t, w, yw)
                    gsr2Val = model2.zerobond(t, w, yw)
                    hwVal = hw.discountBond(w, t, rw)
                    self.assertFalse(abs(gsrVal - hwVal) > tol0)
                    self.assertFalse(abs(gsr2Val - hwVal) > tol0)
                    xw += 0.01
                    if xw > 0.10:
                        break
                t += 2.5
                if t > 50.0:
                    break
            w += 5.0
            if w > 50.0:
                break

        # test standard, nonstandard and jamshidian engine against existing Hull
        # White Jamshidian engine

        expiry = TARGET().advance(refDate, Period(5, Years))
        tenor = Period(10, Years)
        swpIdx = EuriborSwapIsdaFixA(tenor, yts)
        forward = swpIdx.fixing(expiry)

        underlying = swpIdx.underlyingSwap(expiry)
        underlyingFixed = MakeVanillaSwap(
            Period(10, Years), swpIdx.iborIndex(), forward, Period(0, Days))
        underlyingFixed.withEffectiveDate(swpIdx.valueDate(expiry))
        underlyingFixed.withFixedLegCalendar(swpIdx.fixingCalendar())
        underlyingFixed.withFixedLegDayCount(swpIdx.dayCounter())
        underlyingFixed.withFixedLegTenor(swpIdx.fixedLegTenor())
        underlyingFixed.withFixedLegConvention(swpIdx.fixedLegConvention())
        underlyingFixed.withFixedLegTerminationDateConvention(
            swpIdx.fixedLegConvention())
        underlyingFixed = underlyingFixed.makeVanillaSwap()
        exercise = EuropeanExercise(expiry)
        stdswaption = Swaption(underlyingFixed, exercise)
        nonstdswaption = NonstandardSwaption(stdswaption)

        stdswaption.setPricingEngine(
            JamshidianSwaptionEngine(hw, yts))
        HwJamNpv = stdswaption.NPV()

        nonstdswaption.setPricingEngine(
            Gaussian1dNonstandardSwaptionEngine(
                model, 64, 7.0, true, false))
        stdswaption.setPricingEngine(
            Gaussian1dSwaptionEngine(model, 64, 7.0, true, false))
        GsrNonStdNpv = nonstdswaption.NPV()
        GsrStdNpv = stdswaption.NPV()
        stdswaption.setPricingEngine(
            Gaussian1dJamshidianSwaptionEngine(model))
        GsrJamNpv = stdswaption.NPV()

        self.assertFalse(abs(HwJamNpv - GsrNonStdNpv) > 0.00005)
        self.assertFalse(abs(HwJamNpv - GsrStdNpv) > 0.00005)
        self.assertFalse(abs(HwJamNpv - GsrJamNpv) > 0.00005)
