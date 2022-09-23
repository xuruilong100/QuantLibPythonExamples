import unittest

from QuantLib import *

from utilities import *


class CdsOptionTest(unittest.TestCase):

    def testCached(self):
        TEST_MESSAGE(
            "Testing CDS-option value against cached values...")

        backup = SavedSettings()

        cachedToday = Date(10, December, 2007)
        Settings.instance().evaluationDate = cachedToday

        calendar = TARGET()

        riskFree = RelinkableYieldTermStructureHandle()
        riskFree.linkTo(
            FlatForward(cachedToday, 0.02, Actual360()))

        expiry = calendar.advance(cachedToday, 9, Months)
        startDate = calendar.advance(expiry, 1, Months)
        maturity = calendar.advance(startDate, 7, Years)

        dayCounter = Actual360()
        convention = ModifiedFollowing
        notional = 1000000.0

        hazardRate = QuoteHandle(SimpleQuote(0.001))

        schedule = Schedule(
            startDate, maturity, Period(Quarterly),
            calendar, convention, convention,
            DateGeneration.Forward, false)

        recoveryRate = 0.4
        defaultProbability = DefaultProbabilityTermStructureHandle(
            FlatHazardRate(0, calendar, hazardRate, dayCounter))

        swapEngine = MidPointCdsEngine(
            defaultProbability, recoveryRate, riskFree)

        swap = CreditDefaultSwap(
            Protection.Seller, notional, 0.001, schedule,
            convention, dayCounter)
        swap.setPricingEngine(swapEngine)
        strike = swap.fairSpread()

        cdsVol = QuoteHandle(SimpleQuote(0.20))

        underlying = CreditDefaultSwap(
            Protection.Seller, notional, strike, schedule,
            convention, dayCounter)
        underlying.setPricingEngine(swapEngine)

        exercise = EuropeanExercise(expiry)
        option1 = CdsOption(underlying, exercise)
        option1.setPricingEngine(
            BlackCdsOptionEngine(
                defaultProbability, recoveryRate,
                riskFree, cdsVol))

        cachedValue = 270.976348
        self.assertFalse(abs(option1.NPV() - cachedValue) > 1.0e-5)

        underlying = CreditDefaultSwap(
            Protection.Buyer, notional, strike, schedule,
            convention, dayCounter)
        underlying.setPricingEngine(swapEngine)

        option2 = CdsOption(underlying, exercise)
        option2.setPricingEngine(
            BlackCdsOptionEngine(
                defaultProbability, recoveryRate,
                riskFree, cdsVol))

        cachedValue = 270.976348
        self.assertFalse(abs(option2.NPV() - cachedValue) > 1.0e-5)
