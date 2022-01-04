import unittest
from utilities import *
from QuantLib import *


class InterestRateData(object):
    def __init__(self,
                 r,
                 comp,
                 freq,
                 t,
                 comp2,
                 freq2,
                 expected,
                 precision):
        self.r = r
        self.comp = comp
        self.freq = freq
        self.t = t
        self.comp2 = comp2
        self.freq2 = freq2
        self.expected = expected
        self.precision = precision


class InterestRateTest(unittest.TestCase):

    def testConversions(self):
        TEST_MESSAGE("Testing interest-rate conversions...")

        cases = [
            # data from "Option Pricing Formulas", Haug, pag.181-182
            # Rate,Compounding,        Frequency,   Time, Compounding2,      Frequency2,  Rate2, precision
            InterestRateData(0.0800, Compounded, Quarterly, 1.00, Continuous, Annual, 0.0792, 4),
            InterestRateData(0.1200, Continuous, Annual, 1.00, Compounded, Annual, 0.1275, 4),
            InterestRateData(0.0800, Compounded, Quarterly, 1.00, Compounded, Annual, 0.0824, 4),
            InterestRateData(0.0700, Compounded, Quarterly, 1.00, Compounded, Semiannual, 0.0706, 4),
            # undocumented, but reasonable :)
            InterestRateData(0.0100, Compounded, Annual, 1.00, Simple, Annual, 0.0100, 4),
            InterestRateData(0.0200, Simple, Annual, 1.00, Compounded, Annual, 0.0200, 4),
            InterestRateData(0.0300, Compounded, Semiannual, 0.50, Simple, Annual, 0.0300, 4),
            InterestRateData(0.0400, Simple, Annual, 0.50, Compounded, Semiannual, 0.0400, 4),
            InterestRateData(0.0500, Compounded, EveryFourthMonth, 1.0 / 3, Simple, Annual, 0.0500, 4),
            InterestRateData(0.0600, Simple, Annual, 1.0 / 3, Compounded, EveryFourthMonth, 0.0600, 4),
            InterestRateData(0.0500, Compounded, Quarterly, 0.25, Simple, Annual, 0.0500, 4),
            InterestRateData(0.0600, Simple, Annual, 0.25, Compounded, Quarterly, 0.0600, 4),
            InterestRateData(0.0700, Compounded, Bimonthly, 1.0 / 6, Simple, Annual, 0.0700, 4),
            InterestRateData(0.0800, Simple, Annual, 1.0 / 6, Compounded, Bimonthly, 0.0800, 4),
            InterestRateData(0.0900, Compounded, Monthly, 1.0 / 12, Simple, Annual, 0.0900, 4),
            InterestRateData(0.1000, Simple, Annual, 1.0 / 12, Compounded, Monthly, 0.1000, 4),
            InterestRateData(0.0300, SimpleThenCompounded, Semiannual, 0.25, Simple, Annual, 0.0300, 4),
            InterestRateData(0.0300, SimpleThenCompounded, Semiannual, 0.25, Simple, Semiannual, 0.0300, 4),
            InterestRateData(0.0300, SimpleThenCompounded, Semiannual, 0.25, Simple, Quarterly, 0.0300, 4),
            InterestRateData(0.0300, SimpleThenCompounded, Semiannual, 0.50, Simple, Annual, 0.0300, 4),
            InterestRateData(0.0300, SimpleThenCompounded, Semiannual, 0.50, Simple, Semiannual, 0.0300, 4),
            InterestRateData(0.0300, SimpleThenCompounded, Semiannual, 0.75, Compounded, Semiannual, 0.0300, 4),
            InterestRateData(0.0400, Simple, Semiannual, 0.25, SimpleThenCompounded, Quarterly, 0.0400, 4),
            InterestRateData(0.0400, Simple, Semiannual, 0.25, SimpleThenCompounded, Semiannual, 0.0400, 4),
            InterestRateData(0.0400, Simple, Semiannual, 0.25, SimpleThenCompounded, Annual, 0.0400, 4),
            InterestRateData(0.0400, Compounded, Quarterly, 0.50, SimpleThenCompounded, Quarterly, 0.0400, 4),
            InterestRateData(0.0400, Simple, Semiannual, 0.50, SimpleThenCompounded, Semiannual, 0.0400, 4),
            InterestRateData(0.0400, Simple, Semiannual, 0.50, SimpleThenCompounded, Annual, 0.0400, 4),
            InterestRateData(0.0400, Compounded, Quarterly, 0.75, SimpleThenCompounded, Quarterly, 0.0400, 4),
            InterestRateData(0.0400, Compounded, Semiannual, 0.75, SimpleThenCompounded, Semiannual, 0.0400, 4),
            InterestRateData(0.0400, Simple, Semiannual, 0.75, SimpleThenCompounded, Annual, 0.0400, 4)]

        d1 = Date.todaysDate()

        for i in cases:
            ir = InterestRate(i.r, Actual360(), i.comp, i.freq)
            d2 = d1 + timeToDays(i.t)
            roundingPrecision = Rounding(i.precision)

            # check that the compound factor is the inverse of the discount factor
            compoundf = ir.compoundFactor(d1, d2)
            disc = ir.discountFactor(d1, d2)
            error = abs(disc - 1.0 / compoundf)
            self.assertFalse(error > 1e-15)

            # check that the equivalent InterestRate with *same* daycounter,
            # compounding, and frequency is the *same* InterestRate
            ir2 = ir.equivalentRate(
                ir.dayCounter(),
                ir.compounding(),
                ir.frequency(),
                d1, d2)
            error = abs(ir.rate() - ir2.rate())
            self.assertFalse(error > 1e-15)
            self.assertFalse(ir.dayCounter() != ir2.dayCounter())
            self.assertFalse(ir.compounding() != ir2.compounding())
            self.assertFalse(ir.frequency() != ir2.frequency())

            # check that the equivalent rate with *same* daycounter,
            # compounding, and frequency is the *same* rate
            r2 = ir.equivalentRate(
                ir.dayCounter(),
                ir.compounding(),
                ir.frequency(),
                d1, d2)
            error = abs(ir.rate() - r2.rate())
            self.assertFalse(error > 1e-15)

            # check that the equivalent InterestRate with *different*
            # compounding, and frequency is the *expected* InterestRate
            ir3 = ir.equivalentRate(ir.dayCounter(), i.comp2, i.freq2, d1, d2)
            expectedIR = InterestRate(i.expected, ir.dayCounter(), i.comp2, i.freq2)
            r3 = roundingPrecision(ir3.rate())
            error = abs(r3 - expectedIR.rate())
            self.assertFalse(error > 1.0e-17)
            self.assertFalse(ir3.dayCounter() != expectedIR.dayCounter())
            self.assertFalse(ir3.compounding() != expectedIR.compounding())
            self.assertFalse(ir3.frequency() != expectedIR.frequency())

            # check that the equivalent rate with *different*
            # compounding, and frequency is the *expected* rate
            r3 = ir.equivalentRate(ir.dayCounter(), i.comp2, i.freq2, d1, d2)
            r3 = roundingPrecision(r3.rate())
            error = abs(r3 - i.expected)
            self.assertFalse(error > 1.0e-17)
