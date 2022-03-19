import unittest
from utilities import *
from QuantLib import *


class Datum(object):
    def __init__(self,
                 n,
                 units,
                 rate):
        self.n = n
        self.units = units
        self.rate = rate


class CommonVars(object):

    # setup
    def __init__(self):
        self.calendar = TARGET()
        self.settlementDays = 2
        self.today = Date(9, June, 2009)
        self.compounding = Continuous
        self.dayCount = Actual360()
        self.settlementDate = self.calendar.advance(
            self.today, self.settlementDays, Days)
        Settings.instance().evaluationDate = self.today
        self.backup = SavedSettings()

        ts = [13, 41, 75, 165, 256, 345, 524, 703]
        r = [0.035, 0.033, 0.034, 0.034, 0.036, 0.037, 0.039, 0.040]
        rates = DoubleVector(1, 0.035)
        dates = DateVector(1, self.settlementDate)
        for i in range(8):
            dates.append(self.calendar.advance(self.today, ts[i], Days))
            rates.append(r[i])

        self.termStructure = ZeroCurve(dates, rates, self.dayCount)


class PiecewiseZeroSpreadedTermStructureTest(unittest.TestCase):

    def testFlatInterpolationLeft(self):
        TEST_MESSAGE("Testing flat interpolation before the first spreaded date...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.03)
        spreads = [QuoteHandle(spread1), QuoteHandle(spread2)]

        spreadDates = [
            vars.calendar.advance(vars.today, 8, Months),
            vars.calendar.advance(vars.today, 15, Months)]

        interpolationDate = vars.calendar.advance(vars.today, 6, Months)

        # spreadedTermStructure = PiecewiseZeroSpreadedTermStructure(
        spreadedTermStructure = SpreadedLinearZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)

        t = vars.dayCount.yearFraction(vars.today, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()

        tolerance = 1e-9
        expectedRate = spread1.value() + \
                       vars.termStructure.zeroRate(t, vars.compounding).rate()

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

    def testFlatInterpolationRight(self):
        TEST_MESSAGE("Testing flat interpolation after the last spreaded date...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.03)
        spreads = [QuoteHandle(spread1), QuoteHandle(spread2)]

        spreadDates = [
            vars.calendar.advance(vars.today, 8, Months),
            vars.calendar.advance(vars.today, 15, Months)]

        interpolationDate = vars.calendar.advance(vars.today, 20, Months)

        # spreadedTermStructure = PiecewiseZeroSpreadedTermStructure(
        spreadedTermStructure = SpreadedLinearZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)
        spreadedTermStructure.enableExtrapolation()

        t = vars.dayCount.yearFraction(vars.today, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()

        tolerance = 1e-9
        expectedRate = spread2.value() + \
                       vars.termStructure.zeroRate(t, vars.compounding).rate()

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

    def testLinearInterpolationMultipleSpreads(self):
        TEST_MESSAGE("Testing linear interpolation with more than two spreaded dates...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.02)
        spread3 = SimpleQuote(0.035)
        spread4 = SimpleQuote(0.04)
        spreads = [
            QuoteHandle(spread1), QuoteHandle(spread2),
            QuoteHandle(spread3), QuoteHandle(spread4)]

        spreadDates = [
            vars.calendar.advance(vars.today, 90, Days),
            vars.calendar.advance(vars.today, 150, Days),
            vars.calendar.advance(vars.today, 30, Months),
            vars.calendar.advance(vars.today, 40, Months)]

        interpolationDate = vars.calendar.advance(vars.today, 120, Days)

        # spreadedTermStructure = PiecewiseZeroSpreadedTermStructure(
        spreadedTermStructure = SpreadedLinearZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)

        t = vars.dayCount.yearFraction(vars.today, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()

        tolerance = 1e-9
        expectedRate = spread1.value() + \
                       vars.termStructure.zeroRate(t, vars.compounding).rate()

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

    def testLinearInterpolation(self):
        TEST_MESSAGE("Testing linear interpolation between two dates...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.03)
        spreads = [QuoteHandle(spread1), QuoteHandle(spread2)]

        spreadDates = [
            vars.calendar.advance(vars.today, 100, Days),
            vars.calendar.advance(vars.today, 150, Days)]

        interpolationDate = vars.calendar.advance(vars.today, 120, Days)

        # spreadedTermStructure = InterpolatedPiecewiseZeroSpreadedTermStructure<Linear>(
        spreadedTermStructure = SpreadedLinearZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)

        d0 = vars.calendar.advance(vars.today, 100, Days)
        d1 = vars.calendar.advance(vars.today, 150, Days)
        d2 = vars.calendar.advance(vars.today, 120, Days)

        m = (0.03 - 0.02) / vars.dayCount.yearFraction(d0, d1)
        expectedRate = m * vars.dayCount.yearFraction(d0, d2) + 0.054

        t = vars.dayCount.yearFraction(vars.settlementDate, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()

        tolerance = 1e-9

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

    def testForwardFlatInterpolation(self):
        TEST_MESSAGE("Testing forward flat interpolation between two dates...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.03)
        spreads = [QuoteHandle(spread1), QuoteHandle(spread2)]

        spreadDates = [
            vars.calendar.advance(vars.today, 75, Days),
            vars.calendar.advance(vars.today, 260, Days)]

        interpolationDate = vars.calendar.advance(vars.today, 100, Days)

        # spreadedTermStructure = InterpolatedPiecewiseZeroSpreadedTermStructure<ForwardFlat>(
        spreadedTermStructure = SpreadedForwardFlatZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)

        t = vars.dayCount.yearFraction(vars.today, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()

        tolerance = 1e-9
        expectedRate = vars.termStructure.zeroRate(t, vars.compounding).rate() + spread1.value()

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

    def testBackwardFlatInterpolation(self):
        TEST_MESSAGE("Testing backward flat interpolation between two dates...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.03)
        spread3 = SimpleQuote(0.04)
        spreads = [
            QuoteHandle(spread1), QuoteHandle(spread2), QuoteHandle(spread3)]

        spreadDates = [
            vars.calendar.advance(vars.today, 100, Days),
            vars.calendar.advance(vars.today, 200, Days),
            vars.calendar.advance(vars.today, 300, Days)]

        interpolationDate = vars.calendar.advance(vars.today, 110, Days)

        # spreadedTermStructure = InterpolatedPiecewiseZeroSpreadedTermStructure<BackwardFlat> >(
        spreadedTermStructure = SpreadedBackwardFlatZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)

        t = vars.dayCount.yearFraction(vars.today, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()

        tolerance = 1e-9
        expectedRate = vars.termStructure.zeroRate(t, vars.compounding).rate() + spread2.value()

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

    def testDefaultInterpolation(self):
        TEST_MESSAGE("Testing default interpolation between two dates...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.02)
        spreads = [QuoteHandle(spread1), QuoteHandle(spread2)]

        spreadDates = [
            vars.calendar.advance(vars.today, 75, Days),
            vars.calendar.advance(vars.today, 160, Days)]

        interpolationDate = vars.calendar.advance(vars.today, 100, Days)

        # spreadedTermStructure = PiecewiseZeroSpreadedTermStructure(
        spreadedTermStructure = SpreadedLinearZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)

        t = vars.dayCount.yearFraction(vars.today, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()

        tolerance = 1e-9
        expectedRate = vars.termStructure.zeroRate(t, vars.compounding).rate() + spread1.value()

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

    def testSetInterpolationFactory(self):
        TEST_MESSAGE("Testing factory constructor with additional parameters...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.03)
        spread3 = SimpleQuote(0.01)
        spreads = [
            QuoteHandle(spread1), QuoteHandle(spread2), QuoteHandle(spread3)]

        spreadDates = [
            vars.calendar.advance(vars.today, 8, Months),
            vars.calendar.advance(vars.today, 15, Months),
            vars.calendar.advance(vars.today, 25, Months)]

        interpolationDate = vars.calendar.advance(vars.today, 11, Months)

        # spreadedTermStructure

        freq = NoFrequency

        # Cubic factory
        factory = Cubic(CubicInterpolation.Spline, false)

        # spreadedTermStructure = InterpolatedPiecewiseZeroSpreadedTermStructure<Cubic>(
        spreadedTermStructure = SpreadedCubicZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure),
            spreads, spreadDates, vars.compounding, freq, vars.dayCount, factory)

        t = vars.dayCount.yearFraction(vars.today, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()

        tolerance = 1e-9
        expectedRate = vars.termStructure.zeroRate(t, vars.compounding).rate() + 0.026065770863

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

    def testMaxDate(self):
        TEST_MESSAGE("Testing term structure max date...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.03)
        spreads = [QuoteHandle(spread1), QuoteHandle(spread2)]

        spreadDates = [
            vars.calendar.advance(vars.today, 8, Months),
            vars.calendar.advance(vars.today, 15, Months)]

        # spreadedTermStructure = PiecewiseZeroSpreadedTermStructure(
        spreadedTermStructure = SpreadedLinearZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)

        maxDate = spreadedTermStructure.maxDate()

        expectedDate = min(vars.termStructure.maxDate(), spreadDates[-1])

        self.assertFalse(maxDate != expectedDate)

    def testQuoteChanging(self):
        TEST_MESSAGE("Testing quote update...")

        vars = CommonVars()

        spread1 = SimpleQuote(0.02)
        spread2 = SimpleQuote(0.03)
        spreads = [QuoteHandle(spread1), QuoteHandle(spread2)]

        spreadDates = [
            vars.calendar.advance(vars.today, 100, Days),
            vars.calendar.advance(vars.today, 150, Days)]

        interpolationDate = vars.calendar.advance(vars.today, 120, Days)

        # spreadedTermStructure = InterpolatedPiecewiseZeroSpreadedTermStructure<BackwardFlat>(
        spreadedTermStructure = SpreadedBackwardFlatZeroInterpolatedTermStructure(
            YieldTermStructureHandle(vars.termStructure), spreads, spreadDates)

        t = vars.dayCount.yearFraction(vars.settlementDate, interpolationDate)
        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()
        tolerance = 1e-9
        expectedRate = vars.termStructure.zeroRate(t, vars.compounding).rate() + 0.03

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)

        spread2.setValue(0.025)

        interpolatedZeroRate = spreadedTermStructure.zeroRate(t, vars.compounding).rate()
        expectedRate = vars.termStructure.zeroRate(t, vars.compounding).rate() + 0.025

        self.assertFalse(abs(interpolatedZeroRate - expectedRate) > tolerance)
