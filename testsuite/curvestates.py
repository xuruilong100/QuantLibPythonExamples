import unittest

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):

        self.calendar = NullCalendar()
        self.todaysDate = Settings.instance().evaluationDate

        self.endDate = self.todaysDate + Period(10, Years)
        dates = Schedule(self.todaysDate, self.endDate, Period(Semiannual), self.calendar, Following, Following,
                         DateGeneration.Backward, false)
        self.rateTimes = DoubleVector(len(dates) - 1)
        self.paymentTimes = DoubleVector(len(self.rateTimes) - 1)
        self.accruals = DoubleVector(len(self.rateTimes) - 1)
        self.dayCounter = SimpleDayCounter()
        for i in range(1, len(dates)):
            self.rateTimes[i - 1] = self.dayCounter.yearFraction(self.todaysDate, dates[i])

        for i in range(1, len(self.rateTimes)):
            self.accruals[i - 1] = self.rateTimes[i] - self.rateTimes[i - 1]
            self.paymentTimes[i - 1] = self.rateTimes[i]

        self.todaysForwards = DoubleVector(len(self.paymentTimes))
        displacement = 0.0
        for i in range(1, len(self.todaysForwards)):
            self.todaysForwards[i] = 0.03 + 0.0010 * i

        todaysDiscounts = DoubleVector(len(self.rateTimes))
        todaysDiscounts[0] = 0.95
        for i in range(1, len(self.rateTimes)):
            todaysDiscounts[i] = todaysDiscounts[i - 1] / (1.0 + self.todaysForwards[i - 1] * self.accruals[i - 1])

        N = self.todaysForwards.size()
        todaysCoterminalSwapRates = DoubleVector(N)
        coterminalAnnuity = DoubleVector(N)
        floatingLeg = 0.0
        for i in range(1, N + 1):
            if i == 1:
                coterminalAnnuity[N - 1] = self.accruals[N - 1] * todaysDiscounts[N]
            else:
                coterminalAnnuity[N - i] = coterminalAnnuity[N - i + 1] + self.accruals[N - i] * todaysDiscounts[N - i + 1]

            floatingLeg = todaysDiscounts[N - i] - todaysDiscounts[N]
            todaysCoterminalSwapRates[N - i] = floatingLeg / coterminalAnnuity[N - i]

        evolutionTimes = DoubleVector(len(self.rateTimes) - 1)

        for i in range(len(self.rateTimes) - 1):
            evolutionTimes[i] = self.rateTimes[i]
        evolution = EvolutionDescription(self.rateTimes, evolutionTimes)
        evolution.rateTaus()
        evolution.firstAliveRate()


class CurveStatesTest(unittest.TestCase):

    @unittest.skip("testLMMCurveState")
    def testLMMCurveState(self):

        TEST_MESSAGE(
            "Testing Libor-market-model curve state...")

        vars = CommonVars()

    @unittest.skip("testCoterminalSwapCurveState")
    def testCoterminalSwapCurveState(self):

        TEST_MESSAGE(
            "Testing coterminal-swap-market-model curve state...")

        vars = CommonVars()

    def testCMSwapCurveState(self):

        TEST_MESSAGE(
            "Testing constant-maturity-swap-market-model curve state...")

        vars = CommonVars()

        nbRates = vars.todaysForwards.size()
        factors = nbRates
        pseudo = Matrix(nbRates, factors, 0.1)
        displacements = DoubleVector(nbRates, .0)
        rateTimes = DoubleVector(nbRates + 1)
        taus = DoubleVector(nbRates, .5)
        forwards = DoubleVector(nbRates, 0.0)

        for i in range(len(forwards)):
            forwards[i] = i * .001 + .04

        for i in range(len(rateTimes)):
            rateTimes[i] = (i + 1) * .5

        numeraire = nbRates
        alive = 0

        spanningFwds = 1

        cmsDriftcalculator = CMSMMDriftCalculator(
            pseudo, displacements, taus, numeraire,
            alive, spanningFwds)

        cmsCs = CMSwapCurveState(rateTimes, spanningFwds)
        cmsCs.setOnCMSwapRates(forwards)
        cmsDrifts = DoubleVector(nbRates)
        cmsDriftcalculator.compute(cmsCs, cmsDrifts)

        lmmDriftcalculator = LMMDriftCalculator(
            pseudo, displacements, taus, numeraire, alive)
        lmmCs = LMMCurveState(rateTimes)
        lmmCs.setOnForwardRates(forwards)
