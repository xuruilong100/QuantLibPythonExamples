import unittest
from math import sqrt

from QuantLib import *

from utilities import *

length = 10


def makeIndex():
    dayCounter = Actual360()
    dates = [Date(4, September, 2005), Date(4, September, 2018)]
    rates = [0.01, 0.08]

    termStructure = RelinkableYieldTermStructureHandle(
        ZeroCurve(dates, rates, dayCounter))

    index = Euribor1Y(termStructure)

    todaysDate = index.fixingCalendar().adjust(Date(4, September, 2005))
    Settings.instance().evaluationDate = todaysDate

    dates[0] = index.fixingCalendar().advance(
        todaysDate, index.fixingDays(), Days)

    termStructure.linkTo(ZeroCurve(dates, rates, dayCounter))

    return index


def makeCapVolCurve(todaysDate):
    vols = [14.40, 17.15, 16.81, 16.64, 16.17,
            15.78, 15.40, 15.21, 14.86, 14.54]

    dates = []
    capletVols = []
    process = LiborForwardModelProcess(length + 1, makeIndex())

    for i in range(length):
        capletVols.append(vols[i] / 100)
        dates.append(process.fixingDates()[i + 1])

    return CapletVarianceCurve(
        todaysDate, dates, capletVols,
        ActualActual(ActualActual.ISDA))


def makeProcess(volaComp=Matrix()):
    factors = 1 if volaComp.empty() else volaComp.columns()

    index = makeIndex()
    process = LiborForwardModelProcess(length, index)

    fct = LfmHullWhiteParameterization(
        process,
        makeCapVolCurve(Settings.instance().evaluationDate),
        volaComp * transpose(volaComp), factors)

    process.setCovarParam(fct)

    return process


class LiborMarketModelProcessTest(unittest.TestCase):

    def testInitialisation(self):
        TEST_MESSAGE(
            "Testing caplet LMM process initialisation...")

        backup = SavedSettings()

        dayCounter = Actual360()
        termStructure = RelinkableYieldTermStructureHandle(
            flatRate(knownGoodDefault, 0.04, dayCounter))

        index = Euribor6M(termStructure)
        capletVol = ConstantOptionletVolatility(
            termStructure.referenceDate(),
            termStructure.calendar(),
            Following,
            0.2,
            termStructure.dayCounter())

        calendar = index.fixingCalendar()

        for daysOffset in range(1825, 8):
            todaysDate = calendar.adjust(knownGoodDefault + daysOffset)
            Settings.instance().evaluationDate = todaysDate
            settlementDate = calendar.advance(todaysDate, index.fixingDays(), Days)

            termStructure.linkTo(flatRate(settlementDate, 0.04, dayCounter))

            process = LiborForwardModelProcess(60, index)

            fixings = process.fixingTimes()
            for i in range(1, len(fixings) - 1):
                ileft = process.nextIndexReset(fixings[i] - 0.000001)
                iright = process.nextIndexReset(fixings[i] + 0.000001)
                ii = process.nextIndexReset(fixings[i])

                self.assertFalse((ileft != i) or (iright != i + 1) or (ii != i + 1))

    def testLambdaBootstrapping(self):
        TEST_MESSAGE(
            "Testing caplet LMM lambda bootstrapping...")

        backup = SavedSettings()

        tolerance = 1e-10
        lambdaExpected = [
            14.3010297550, 19.3821411939, 15.9816590141,
            15.9953118303, 14.0570815635, 13.5687599894,
            12.7477197786, 13.7056638165, 11.6191989567]

        process = makeProcess()

        covar = process.covariance(0.0, NullArray(), 1.0)

        for i in range(9):
            calculated = sqrt(covar[i + 1][i + 1])
            expected = lambdaExpected[i] / 100

            self.assertFalse(abs(calculated - expected) > tolerance)

        param = process.covarParam()

        tmp = process.fixingTimes()
        grid = TimeGrid(tmp, 14)

        for i in range(len(grid)):
            t = grid[i]
            diff = param.integratedCovariance(t) - param.integratedCovariance(t)

            for k in range(diff.rows()):
                for j in range(diff.columns()):
                    self.assertFalse(abs(diff[k][j]) > tolerance)

    def testMonteCarloCapletPricing(self):
        TEST_MESSAGE(
            "Testing caplet LMM Monte-Carlo caplet pricing...")

        backup = SavedSettings()

        compValues = [
            0.85549771, 0.46707264, 0.22353259,
            0.91915359, 0.37716089, 0.11360610,
            0.96438280, 0.26413316, -0.01412414,
            0.97939148, 0.13492952, -0.15028753,
            0.95970595, -0.00000000, -0.28100621,
            0.97939148, -0.13492952, -0.15028753,
            0.96438280, -0.26413316, -0.01412414,
            0.91915359, -0.37716089, 0.11360610,
            0.85549771, -0.46707264, 0.22353259]

        volaComp = Matrix(9, 3)

        for i in range(9):
            for j in range(3):
                volaComp[i][j] = compValues[i * 3 + j]

        process1 = makeProcess()
        process2 = makeProcess(volaComp)
        tmp = process1.fixingTimes()
        grid = TimeGrid(tmp, 12)

        location = []
        for i in range(len(tmp)):
            j = 0
            for g in grid:
                if g == tmp[i]:
                    break
                else:
                    j = j + 1

            location.append(j)

        seed = 42

        rsg1 = GaussianLowDiscrepancySequenceGenerator(
            UniformLowDiscrepancySequenceGenerator(
                process1.factors() * (len(grid) - 1), seed))

        rsg2 = GaussianLowDiscrepancySequenceGenerator(
            UniformLowDiscrepancySequenceGenerator(
                process2.factors() * (len(grid) - 1), seed))
        generator1 = GaussianSobolMultiPathGenerator(process1, grid, rsg1, false)
        generator2 = GaussianSobolMultiPathGenerator(process2, grid, rsg2, false)

        nrTrails = 250000

        stat1 = [GeneralStatistics() for i in range(process1.size())]
        stat2 = [GeneralStatistics() for i in range(process2.size())]
        stat3 = [GeneralStatistics() for i in range(process2.size() - 1)]
        for i in range(nrTrails):
            path1 = generator1.next()
            path2 = generator2.next()

            rates1 = DoubleVector(length)
            rates2 = DoubleVector(length)
            for j in range(process1.size()):
                rates1[j] = path1.value()[j][location[j]]
                rates2[j] = path2.value()[j][location[j]]

            dis1 = process1.discountBond(rates1)
            dis2 = process2.discountBond(rates2)

            for k in range(process1.size()):
                accrualPeriod = process1.accrualEndTimes()[k] - process1.accrualStartTimes()[k]

                payoff1 = max(rates1[k] - 0.04, 0.0) * accrualPeriod

                payoff2 = max(rates2[k] - 0.04, 0.0) * accrualPeriod
                stat1[k].add(dis1[k] * payoff1)
                stat2[k].add(dis2[k] * payoff2)

                if k != 0:
                    payoff3 = max(rates2[k] - (rates2[k - 1] + 0.0025), 0.0) * accrualPeriod
                    stat3[k - 1].add(dis2[k] * payoff3)

        capletNpv = [
            0.000000000000, 0.000002841629, 0.002533279333,
            0.009577143571, 0.017746502618, 0.025216116835,
            0.031608230268, 0.036645683881, 0.039792254012,
            0.041829864365]

        ratchetNpv = [
            0.0082644895, 0.0082754754, 0.0082159966,
            0.0082982822, 0.0083803357, 0.0084366961,
            0.0084173270, 0.0081803406, 0.0079533814]

        for k in range(process1.size()):

            calculated1 = stat1[k].mean()
            tolerance1 = stat1[k].errorEstimate()
            expected = capletNpv[k]

            self.assertFalse(abs(calculated1 - expected) > tolerance1)

            calculated2 = stat2[k].mean()
            tolerance2 = stat2[k].errorEstimate()

            self.assertFalse(abs(calculated2 - expected) > tolerance2)

            if k != 0:
                calculated3 = stat3[k - 1].mean()
                tolerance3 = stat3[k - 1].errorEstimate()
                expected = ratchetNpv[k - 1]

                refError = 1e-5

                self.assertFalse(abs(calculated3 - expected) > tolerance3 + refError)
