import unittest

from QuantLib import *

from utilities import *


def makeCdsSchedule(fromDate,
                    to,
                    rule):
    schedule = MakeSchedule()
    schedule.fromDate(fromDate)
    schedule.to(to)
    schedule.withCalendar(WeekendsOnly())
    schedule.withTenor(Period(3, Months))
    schedule.withConvention(Following)
    schedule.withTerminationDateConvention(Unadjusted)
    schedule.withRule(rule)
    schedule = schedule.makeSchedule()
    return schedule


class ScheduleTest(unittest.TestCase):

    def testDailySchedule(self):
        TEST_MESSAGE(
            "Testing schedule with daily frequency...")

        startDate = Date(17, January, 2012)

        s = MakeSchedule()
        s.fromDate(startDate)
        s.to(startDate + 7)
        s.withCalendar(TARGET())
        s.withFrequency(Daily)
        s.withConvention(Preceding)
        s = s.makeSchedule()

        expected = DateVector(6)
        expected[0] = Date(17, January, 2012)
        expected[1] = Date(18, January, 2012)
        expected[2] = Date(19, January, 2012)
        expected[3] = Date(20, January, 2012)
        expected[4] = Date(23, January, 2012)
        expected[5] = Date(24, January, 2012)

        self.check_dates(s, expected)

    def testEndDateWithEomAdjustment(self):
        TEST_MESSAGE(
            "Testing end date for schedule with end-of-month adjustment...")

        s = MakeSchedule()
        s.fromDate(Date(30, September, 2009))
        s.to(Date(15, June, 2012))
        s.withCalendar(Japan())
        s.withTenor(Period(6, Months))
        s.withConvention(Following)
        s.withTerminationDateConvention(Following)
        s.forwards()
        s.endOfMonth()
        s = s.makeSchedule()

        expected = DateVector(7)
        expected[0] = Date(30, September, 2009)
        expected[1] = Date(31, March, 2010)
        expected[2] = Date(30, September, 2010)
        expected[3] = Date(31, March, 2011)
        expected[4] = Date(30, September, 2011)
        expected[5] = Date(30, March, 2012)
        expected[6] = Date(29, June, 2012)

        self.check_dates(s, expected)

        s = MakeSchedule()
        s.fromDate(Date(30, September, 2009))
        s.to(Date(15, June, 2012))
        s.withCalendar(Japan())
        s.withTenor(Period(6, Months))
        s.withConvention(Following)
        s.withTerminationDateConvention(Unadjusted)
        s.forwards()
        s.endOfMonth()
        s = s.makeSchedule()
        expected[6] = Date(15, June, 2012)

        self.check_dates(s, expected)

    def testDatesPastEndDateWithEomAdjustment(self):
        TEST_MESSAGE(
            "Testing that no dates are past the end date with EOM adjustment...")

        s = MakeSchedule()
        s.fromDate(Date(28, March, 2013))
        s.to(Date(30, March, 2015))
        s.withCalendar(TARGET())
        s.withTenor(Period(1, Years))
        s.withConvention(Unadjusted)
        s.withTerminationDateConvention(Unadjusted)
        s.forwards()
        s.endOfMonth()
        s = s.makeSchedule()

        expected = DateVector(3)
        expected[0] = Date(31, March, 2013)
        expected[1] = Date(31, March, 2014)
        expected[2] = Date(30, March, 2015)

        self.check_dates(s, expected)
        self.assertFalse(s.isRegular(2))

    def testDatesSameAsEndDateWithEomAdjustment(self):
        TEST_MESSAGE(
            "Testing that next-to-last date same as end date is removed...")

        s = MakeSchedule()
        s.fromDate(Date(28, March, 2013))
        s.to(Date(31, March, 2015))
        s.withCalendar(TARGET())
        s.withTenor(Period(1, Years))
        s.withConvention(Unadjusted)
        s.withTerminationDateConvention(Unadjusted)
        s.forwards()
        s.endOfMonth()
        s = s.makeSchedule()

        expected = DateVector(3)
        expected[0] = Date(31, March, 2013)
        expected[1] = Date(31, March, 2014)
        expected[2] = Date(31, March, 2015)

        self.check_dates(s, expected)

        self.assertFalse(not s.isRegular(2))

    def testForwardDatesWithEomAdjustment(self):
        TEST_MESSAGE(
            "Testing that the last date is not adjusted for EOM when "
            "termination date convention is unadjusted...")

        s = MakeSchedule()
        s.fromDate(Date(31, August, 1996))
        s.to(Date(15, September, 1997))
        s.withCalendar(UnitedStates(UnitedStates.GovernmentBond))
        s.withTenor(Period(6, Months))
        s.withConvention(Unadjusted)
        s.withTerminationDateConvention(Unadjusted)
        s.forwards()
        s.endOfMonth()
        s = s.makeSchedule()

        expected = DateVector(4)
        expected[0] = Date(31, August, 1996)
        expected[1] = Date(28, February, 1997)
        expected[2] = Date(31, August, 1997)
        expected[3] = Date(15, September, 1997)

        self.check_dates(s, expected)

    def testBackwardDatesWithEomAdjustment(self):
        TEST_MESSAGE(
            "Testing that the first date is not adjusted for EOM "
            "going backward when termination date convention is unadjusted...")

        s = MakeSchedule()
        s.fromDate(Date(22, August, 1996))
        s.to(Date(31, August, 1997))
        s.withCalendar(UnitedStates(UnitedStates.GovernmentBond))
        s.withTenor(Period(6, Months))
        s.withConvention(Unadjusted)
        s.withTerminationDateConvention(Unadjusted)
        s.backwards()
        s.endOfMonth()
        s = s.makeSchedule()

        expected = DateVector(4)
        expected[0] = Date(22, August, 1996)
        expected[1] = Date(31, August, 1996)
        expected[2] = Date(28, February, 1997)
        expected[3] = Date(31, August, 1997)

        self.check_dates(s, expected)

    def testDoubleFirstDateWithEomAdjustment(self):
        TEST_MESSAGE(
            "Testing that the first date is not duplicated due to "
            "EOM convention when going backwards...")

        s = MakeSchedule()
        s.fromDate(Date(22, August, 1996))
        s.to(Date(31, August, 1997))
        s.withCalendar(UnitedStates(UnitedStates.GovernmentBond))
        s.withTenor(Period(6, Months))
        s.withConvention(Following)
        s.withTerminationDateConvention(Following)
        s.backwards()
        s.endOfMonth()
        s = s.makeSchedule()

        expected = DateVector(3)
        expected[0] = Date(30, August, 1996)
        expected[1] = Date(28, February, 1997)
        expected[2] = Date(29, August, 1997)

        self.check_dates(s, expected)

    def testCDS2015Convention(self):

        TEST_MESSAGE(
            "Testing CDS2015 semi-annual rolling convention...")

        rule = DateGeneration.CDS2015
        tenor = Period(5, Years)

        tradeDate = Date(12, Dec, 2016)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        expStart = Date(20, Sep, 2016)
        expMaturity = Date(20, Dec, 2021)
        self.assertTrue(maturity, expMaturity)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        self.assertTrue(s.startDate(), expStart)
        self.assertTrue(s.endDate(), expMaturity)

        maturity = tradeDate + tenor
        s = makeCdsSchedule(tradeDate, maturity, rule)
        self.assertTrue(s.startDate(), expStart)
        self.assertTrue(s.endDate(), expMaturity)

        tradeDate = Date(1, Mar, 2017)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        self.assertTrue(maturity, expMaturity)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expStart = Date(20, Dec, 2016)
        self.assertTrue(s.startDate(), expStart)
        self.assertTrue(s.endDate(), expMaturity)

        maturity = tradeDate + tenor
        s = makeCdsSchedule(tradeDate, maturity, rule)
        self.assertTrue(s.startDate(), expStart)
        expMaturity = Date(20, Mar, 2022)
        self.assertTrue(s.endDate(), expMaturity)

        tradeDate = Date(20, Mar, 2017)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        expStart = Date(20, Mar, 2017)
        expMaturity = Date(20, Jun, 2022)
        self.assertTrue(maturity, expMaturity)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        self.assertTrue(s.startDate(), expStart)
        self.assertTrue(s.endDate(), expMaturity)

    def testCDS2015ConventionGrid(self):

        TEST_MESSAGE(
            "Testing CDS2015 convention against ISDA doc...")

        inputs = [
            ((Date(19, Mar, 2016), Period(3, Months)), (Date(21, Dec, 2015), Date(20, Mar, 2016))),
            ((Date(20, Mar, 2016), Period(3, Months)), (Date(21, Dec, 2015), Date(20, Sep, 2016))),
            ((Date(21, Mar, 2016), Period(3, Months)), (Date(21, Mar, 2016), Date(20, Sep, 2016))),
            ((Date(19, Jun, 2016), Period(3, Months)), (Date(21, Mar, 2016), Date(20, Sep, 2016))),
            ((Date(20, Jun, 2016), Period(3, Months)), (Date(20, Jun, 2016), Date(20, Sep, 2016))),
            ((Date(21, Jun, 2016), Period(3, Months)), (Date(20, Jun, 2016), Date(20, Sep, 2016))),
            ((Date(19, Sep, 2016), Period(3, Months)), (Date(20, Jun, 2016), Date(20, Sep, 2016))),
            ((Date(20, Sep, 2016), Period(3, Months)), (Date(20, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(21, Sep, 2016), Period(3, Months)), (Date(20, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(19, Dec, 2016), Period(3, Months)), (Date(20, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(20, Dec, 2016), Period(3, Months)), (Date(20, Dec, 2016), Date(20, Mar, 2017))),
            ((Date(21, Dec, 2016), Period(3, Months)), (Date(20, Dec, 2016), Date(20, Mar, 2017))),
            ((Date(19, Mar, 2016), Period(6, Months)), (Date(21, Dec, 2015), Date(20, Jun, 2016))),
            ((Date(20, Mar, 2016), Period(6, Months)), (Date(21, Dec, 2015), Date(20, Dec, 2016))),
            ((Date(21, Mar, 2016), Period(6, Months)), (Date(21, Mar, 2016), Date(20, Dec, 2016))),
            ((Date(19, Jun, 2016), Period(6, Months)), (Date(21, Mar, 2016), Date(20, Dec, 2016))),
            ((Date(20, Jun, 2016), Period(6, Months)), (Date(20, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(21, Jun, 2016), Period(6, Months)), (Date(20, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(19, Sep, 2016), Period(6, Months)), (Date(20, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(20, Sep, 2016), Period(6, Months)), (Date(20, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(21, Sep, 2016), Period(6, Months)), (Date(20, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(19, Dec, 2016), Period(6, Months)), (Date(20, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(20, Dec, 2016), Period(6, Months)), (Date(20, Dec, 2016), Date(20, Jun, 2017))),
            ((Date(21, Dec, 2016), Period(6, Months)), (Date(20, Dec, 2016), Date(20, Jun, 2017))),
            ((Date(19, Mar, 2016), Period(9, Months)), (Date(21, Dec, 2015), Date(20, Sep, 2016))),
            ((Date(20, Mar, 2016), Period(9, Months)), (Date(21, Dec, 2015), Date(20, Mar, 2017))),
            ((Date(21, Mar, 2016), Period(9, Months)), (Date(21, Mar, 2016), Date(20, Mar, 2017))),
            ((Date(19, Jun, 2016), Period(9, Months)), (Date(21, Mar, 2016), Date(20, Mar, 2017))),
            ((Date(20, Jun, 2016), Period(9, Months)), (Date(20, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(21, Jun, 2016), Period(9, Months)), (Date(20, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(19, Sep, 2016), Period(9, Months)), (Date(20, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(20, Sep, 2016), Period(9, Months)), (Date(20, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(21, Sep, 2016), Period(9, Months)), (Date(20, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(19, Dec, 2016), Period(9, Months)), (Date(20, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(20, Dec, 2016), Period(9, Months)), (Date(20, Dec, 2016), Date(20, Sep, 2017))),
            ((Date(21, Dec, 2016), Period(9, Months)), (Date(20, Dec, 2016), Date(20, Sep, 2017))),
            ((Date(19, Mar, 2016), Period(1, Years)), (Date(21, Dec, 2015), Date(20, Dec, 2016))),
            ((Date(20, Mar, 2016), Period(1, Years)), (Date(21, Dec, 2015), Date(20, Jun, 2017))),
            ((Date(21, Mar, 2016), Period(1, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2017))),
            ((Date(19, Jun, 2016), Period(1, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2017))),
            ((Date(20, Jun, 2016), Period(1, Years)), (Date(20, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(21, Jun, 2016), Period(1, Years)), (Date(20, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(19, Sep, 2016), Period(1, Years)), (Date(20, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(20, Sep, 2016), Period(1, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2017))),
            ((Date(21, Sep, 2016), Period(1, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2017))),
            ((Date(19, Dec, 2016), Period(1, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2017))),
            ((Date(20, Dec, 2016), Period(1, Years)), (Date(20, Dec, 2016), Date(20, Dec, 2017))),
            ((Date(21, Dec, 2016), Period(1, Years)), (Date(20, Dec, 2016), Date(20, Dec, 2017))),
            ((Date(19, Mar, 2016), Period(5, Years)), (Date(21, Dec, 2015), Date(20, Dec, 2020))),
            ((Date(20, Mar, 2016), Period(5, Years)), (Date(21, Dec, 2015), Date(20, Jun, 2021))),
            ((Date(21, Mar, 2016), Period(5, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2021))),
            ((Date(19, Jun, 2016), Period(5, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2021))),
            ((Date(20, Jun, 2016), Period(5, Years)), (Date(20, Jun, 2016), Date(20, Jun, 2021))),
            ((Date(21, Jun, 2016), Period(5, Years)), (Date(20, Jun, 2016), Date(20, Jun, 2021))),
            ((Date(19, Sep, 2016), Period(5, Years)), (Date(20, Jun, 2016), Date(20, Jun, 2021))),
            ((Date(20, Sep, 2016), Period(5, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2021))),
            ((Date(21, Sep, 2016), Period(5, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2021))),
            ((Date(19, Dec, 2016), Period(5, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2021))),
            ((Date(20, Dec, 2016), Period(5, Years)), (Date(20, Dec, 2016), Date(20, Dec, 2021))),
            ((Date(21, Dec, 2016), Period(5, Years)), (Date(20, Dec, 2016), Date(20, Dec, 2021))),
            ((Date(20, Mar, 2016), Period(0, Months)), (Date(21, Dec, 2015), Date(20, Jun, 2016))),
            ((Date(21, Mar, 2016), Period(0, Months)), (Date(21, Mar, 2016), Date(20, Jun, 2016))),
            ((Date(19, Jun, 2016), Period(0, Months)), (Date(21, Mar, 2016), Date(20, Jun, 2016))),
            ((Date(20, Sep, 2016), Period(0, Months)), (Date(20, Sep, 2016), Date(20, Dec, 2016))),
            ((Date(21, Sep, 2016), Period(0, Months)), (Date(20, Sep, 2016), Date(20, Dec, 2016))),
            ((Date(19, Dec, 2016), Period(0, Months)), (Date(20, Sep, 2016), Date(20, Dec, 2016)))]

        self._testCDSConventions(inputs, DateGeneration.CDS2015)

    def testCDSConventionGrid(self):
        TEST_MESSAGE(
            "Testing CDS convention against ISDA doc...")

        inputs = [
            ((Date(19, Mar, 2016), Period(3, Months)), (Date(21, Dec, 2015), Date(20, Jun, 2016))),
            ((Date(20, Mar, 2016), Period(3, Months)), (Date(21, Dec, 2015), Date(20, Sep, 2016))),
            ((Date(21, Mar, 2016), Period(3, Months)), (Date(21, Mar, 2016), Date(20, Sep, 2016))),
            ((Date(19, Jun, 2016), Period(3, Months)), (Date(21, Mar, 2016), Date(20, Sep, 2016))),
            ((Date(20, Jun, 2016), Period(3, Months)), (Date(20, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(21, Jun, 2016), Period(3, Months)), (Date(20, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(19, Sep, 2016), Period(3, Months)), (Date(20, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(20, Sep, 2016), Period(3, Months)), (Date(20, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(21, Sep, 2016), Period(3, Months)), (Date(20, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(19, Dec, 2016), Period(3, Months)), (Date(20, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(20, Dec, 2016), Period(3, Months)), (Date(20, Dec, 2016), Date(20, Jun, 2017))),
            ((Date(21, Dec, 2016), Period(3, Months)), (Date(20, Dec, 2016), Date(20, Jun, 2017))),
            ((Date(19, Mar, 2016), Period(6, Months)), (Date(21, Dec, 2015), Date(20, Sep, 2016))),
            ((Date(20, Mar, 2016), Period(6, Months)), (Date(21, Dec, 2015), Date(20, Dec, 2016))),
            ((Date(21, Mar, 2016), Period(6, Months)), (Date(21, Mar, 2016), Date(20, Dec, 2016))),
            ((Date(19, Jun, 2016), Period(6, Months)), (Date(21, Mar, 2016), Date(20, Dec, 2016))),
            ((Date(20, Jun, 2016), Period(6, Months)), (Date(20, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(21, Jun, 2016), Period(6, Months)), (Date(20, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(19, Sep, 2016), Period(6, Months)), (Date(20, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(20, Sep, 2016), Period(6, Months)), (Date(20, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(21, Sep, 2016), Period(6, Months)), (Date(20, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(19, Dec, 2016), Period(6, Months)), (Date(20, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(20, Dec, 2016), Period(6, Months)), (Date(20, Dec, 2016), Date(20, Sep, 2017))),
            ((Date(21, Dec, 2016), Period(6, Months)), (Date(20, Dec, 2016), Date(20, Sep, 2017))),
            ((Date(19, Mar, 2016), Period(9, Months)), (Date(21, Dec, 2015), Date(20, Dec, 2016))),
            ((Date(20, Mar, 2016), Period(9, Months)), (Date(21, Dec, 2015), Date(20, Mar, 2017))),
            ((Date(21, Mar, 2016), Period(9, Months)), (Date(21, Mar, 2016), Date(20, Mar, 2017))),
            ((Date(19, Jun, 2016), Period(9, Months)), (Date(21, Mar, 2016), Date(20, Mar, 2017))),
            ((Date(20, Jun, 2016), Period(9, Months)), (Date(20, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(21, Jun, 2016), Period(9, Months)), (Date(20, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(19, Sep, 2016), Period(9, Months)), (Date(20, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(20, Sep, 2016), Period(9, Months)), (Date(20, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(21, Sep, 2016), Period(9, Months)), (Date(20, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(19, Dec, 2016), Period(9, Months)), (Date(20, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(20, Dec, 2016), Period(9, Months)), (Date(20, Dec, 2016), Date(20, Dec, 2017))),
            ((Date(21, Dec, 2016), Period(9, Months)), (Date(20, Dec, 2016), Date(20, Dec, 2017))),
            ((Date(19, Mar, 2016), Period(1, Years)), (Date(21, Dec, 2015), Date(20, Mar, 2017))),
            ((Date(20, Mar, 2016), Period(1, Years)), (Date(21, Dec, 2015), Date(20, Jun, 2017))),
            ((Date(21, Mar, 2016), Period(1, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2017))),
            ((Date(19, Jun, 2016), Period(1, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2017))),
            ((Date(20, Jun, 2016), Period(1, Years)), (Date(20, Jun, 2016), Date(20, Sep, 2017))),
            ((Date(21, Jun, 2016), Period(1, Years)), (Date(20, Jun, 2016), Date(20, Sep, 2017))),
            ((Date(19, Sep, 2016), Period(1, Years)), (Date(20, Jun, 2016), Date(20, Sep, 2017))),
            ((Date(20, Sep, 2016), Period(1, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2017))),
            ((Date(21, Sep, 2016), Period(1, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2017))),
            ((Date(19, Dec, 2016), Period(1, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2017))),
            ((Date(20, Dec, 2016), Period(1, Years)), (Date(20, Dec, 2016), Date(20, Mar, 2018))),
            ((Date(21, Dec, 2016), Period(1, Years)), (Date(20, Dec, 2016), Date(20, Mar, 2018))),
            ((Date(19, Mar, 2016), Period(5, Years)), (Date(21, Dec, 2015), Date(20, Mar, 2021))),
            ((Date(20, Mar, 2016), Period(5, Years)), (Date(21, Dec, 2015), Date(20, Jun, 2021))),
            ((Date(21, Mar, 2016), Period(5, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2021))),
            ((Date(19, Jun, 2016), Period(5, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2021))),
            ((Date(20, Jun, 2016), Period(5, Years)), (Date(20, Jun, 2016), Date(20, Sep, 2021))),
            ((Date(21, Jun, 2016), Period(5, Years)), (Date(20, Jun, 2016), Date(20, Sep, 2021))),
            ((Date(19, Sep, 2016), Period(5, Years)), (Date(20, Jun, 2016), Date(20, Sep, 2021))),
            ((Date(20, Sep, 2016), Period(5, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2021))),
            ((Date(21, Sep, 2016), Period(5, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2021))),
            ((Date(19, Dec, 2016), Period(5, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2021))),
            ((Date(20, Dec, 2016), Period(5, Years)), (Date(20, Dec, 2016), Date(20, Mar, 2022))),
            ((Date(21, Dec, 2016), Period(5, Years)), (Date(20, Dec, 2016), Date(20, Mar, 2022))),
            ((Date(19, Mar, 2016), Period(0, Months)), (Date(21, Dec, 2015), Date(20, Mar, 2016))),
            ((Date(20, Mar, 2016), Period(0, Months)), (Date(21, Dec, 2015), Date(20, Jun, 2016))),
            ((Date(21, Mar, 2016), Period(0, Months)), (Date(21, Mar, 2016), Date(20, Jun, 2016))),
            ((Date(19, Jun, 2016), Period(0, Months)), (Date(21, Mar, 2016), Date(20, Jun, 2016))),
            ((Date(20, Jun, 2016), Period(0, Months)), (Date(20, Jun, 2016), Date(20, Sep, 2016))),
            ((Date(21, Jun, 2016), Period(0, Months)), (Date(20, Jun, 2016), Date(20, Sep, 2016))),
            ((Date(19, Sep, 2016), Period(0, Months)), (Date(20, Jun, 2016), Date(20, Sep, 2016))),
            ((Date(20, Sep, 2016), Period(0, Months)), (Date(20, Sep, 2016), Date(20, Dec, 2016))),
            ((Date(21, Sep, 2016), Period(0, Months)), (Date(20, Sep, 2016), Date(20, Dec, 2016))),
            ((Date(19, Dec, 2016), Period(0, Months)), (Date(20, Sep, 2016), Date(20, Dec, 2016))),
            ((Date(20, Dec, 2016), Period(0, Months)), (Date(20, Dec, 2016), Date(20, Mar, 2017))),
            ((Date(21, Dec, 2016), Period(0, Months)), (Date(20, Dec, 2016), Date(20, Mar, 2017)))]

        self._testCDSConventions(inputs, DateGeneration.CDS)

    def testOldCDSConventionGrid(self):
        TEST_MESSAGE(
            "Testing old CDS convention...")

        inputs = [
            ((Date(19, Mar, 2016), Period(3, Months)), (Date(19, Mar, 2016), Date(20, Jun, 2016))),
            ((Date(20, Mar, 2016), Period(3, Months)), (Date(20, Mar, 2016), Date(20, Sep, 2016))),
            ((Date(21, Mar, 2016), Period(3, Months)), (Date(21, Mar, 2016), Date(20, Sep, 2016))),
            ((Date(19, Jun, 2016), Period(3, Months)), (Date(19, Jun, 2016), Date(20, Sep, 2016))),
            ((Date(20, Jun, 2016), Period(3, Months)), (Date(20, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(21, Jun, 2016), Period(3, Months)), (Date(21, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(19, Sep, 2016), Period(3, Months)), (Date(19, Sep, 2016), Date(20, Dec, 2016))),
            ((Date(20, Sep, 2016), Period(3, Months)), (Date(20, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(21, Sep, 2016), Period(3, Months)), (Date(21, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(19, Dec, 2016), Period(3, Months)), (Date(19, Dec, 2016), Date(20, Mar, 2017))),
            ((Date(20, Dec, 2016), Period(3, Months)), (Date(20, Dec, 2016), Date(20, Jun, 2017))),
            ((Date(21, Dec, 2016), Period(3, Months)), (Date(21, Dec, 2016), Date(20, Jun, 2017))),
            ((Date(19, Mar, 2016), Period(6, Months)), (Date(19, Mar, 2016), Date(20, Sep, 2016))),
            ((Date(20, Mar, 2016), Period(6, Months)), (Date(20, Mar, 2016), Date(20, Dec, 2016))),
            ((Date(21, Mar, 2016), Period(6, Months)), (Date(21, Mar, 2016), Date(20, Dec, 2016))),
            ((Date(19, Jun, 2016), Period(6, Months)), (Date(19, Jun, 2016), Date(20, Dec, 2016))),
            ((Date(20, Jun, 2016), Period(6, Months)), (Date(20, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(21, Jun, 2016), Period(6, Months)), (Date(21, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(19, Sep, 2016), Period(6, Months)), (Date(19, Sep, 2016), Date(20, Mar, 2017))),
            ((Date(20, Sep, 2016), Period(6, Months)), (Date(20, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(21, Sep, 2016), Period(6, Months)), (Date(21, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(19, Dec, 2016), Period(6, Months)), (Date(19, Dec, 2016), Date(20, Jun, 2017))),
            ((Date(20, Dec, 2016), Period(6, Months)), (Date(20, Dec, 2016), Date(20, Sep, 2017))),
            ((Date(21, Dec, 2016), Period(6, Months)), (Date(21, Dec, 2016), Date(20, Sep, 2017))),
            ((Date(19, Mar, 2016), Period(9, Months)), (Date(19, Mar, 2016), Date(20, Dec, 2016))),
            ((Date(20, Mar, 2016), Period(9, Months)), (Date(20, Mar, 2016), Date(20, Mar, 2017))),
            ((Date(21, Mar, 2016), Period(9, Months)), (Date(21, Mar, 2016), Date(20, Mar, 2017))),
            ((Date(19, Jun, 2016), Period(9, Months)), (Date(19, Jun, 2016), Date(20, Mar, 2017))),
            ((Date(20, Jun, 2016), Period(9, Months)), (Date(20, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(21, Jun, 2016), Period(9, Months)), (Date(21, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(19, Sep, 2016), Period(9, Months)), (Date(19, Sep, 2016), Date(20, Jun, 2017))),
            ((Date(20, Sep, 2016), Period(9, Months)), (Date(20, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(21, Sep, 2016), Period(9, Months)), (Date(21, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(19, Dec, 2016), Period(9, Months)), (Date(19, Dec, 2016), Date(20, Sep, 2017))),
            ((Date(20, Dec, 2016), Period(9, Months)), (Date(20, Dec, 2016), Date(20, Dec, 2017))),
            ((Date(21, Dec, 2016), Period(9, Months)), (Date(21, Dec, 2016), Date(20, Dec, 2017))),
            ((Date(19, Mar, 2016), Period(1, Years)), (Date(19, Mar, 2016), Date(20, Mar, 2017))),
            ((Date(20, Mar, 2016), Period(1, Years)), (Date(20, Mar, 2016), Date(20, Jun, 2017))),
            ((Date(21, Mar, 2016), Period(1, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2017))),
            ((Date(19, Jun, 2016), Period(1, Years)), (Date(19, Jun, 2016), Date(20, Jun, 2017))),
            ((Date(20, Jun, 2016), Period(1, Years)), (Date(20, Jun, 2016), Date(20, Sep, 2017))),
            ((Date(21, Jun, 2016), Period(1, Years)), (Date(21, Jun, 2016), Date(20, Sep, 2017))),
            ((Date(19, Sep, 2016), Period(1, Years)), (Date(19, Sep, 2016), Date(20, Sep, 2017))),
            ((Date(20, Sep, 2016), Period(1, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2017))),
            ((Date(21, Sep, 2016), Period(1, Years)), (Date(21, Sep, 2016), Date(20, Dec, 2017))),
            ((Date(19, Dec, 2016), Period(1, Years)), (Date(19, Dec, 2016), Date(20, Dec, 2017))),
            ((Date(20, Dec, 2016), Period(1, Years)), (Date(20, Dec, 2016), Date(20, Mar, 2018))),
            ((Date(21, Dec, 2016), Period(1, Years)), (Date(21, Dec, 2016), Date(20, Mar, 2018))),
            ((Date(19, Mar, 2016), Period(5, Years)), (Date(19, Mar, 2016), Date(20, Mar, 2021))),
            ((Date(20, Mar, 2016), Period(5, Years)), (Date(20, Mar, 2016), Date(20, Jun, 2021))),
            ((Date(21, Mar, 2016), Period(5, Years)), (Date(21, Mar, 2016), Date(20, Jun, 2021))),
            ((Date(19, Jun, 2016), Period(5, Years)), (Date(19, Jun, 2016), Date(20, Jun, 2021))),
            ((Date(20, Jun, 2016), Period(5, Years)), (Date(20, Jun, 2016), Date(20, Sep, 2021))),
            ((Date(21, Jun, 2016), Period(5, Years)), (Date(21, Jun, 2016), Date(20, Sep, 2021))),
            ((Date(19, Sep, 2016), Period(5, Years)), (Date(19, Sep, 2016), Date(20, Sep, 2021))),
            ((Date(20, Sep, 2016), Period(5, Years)), (Date(20, Sep, 2016), Date(20, Dec, 2021))),
            ((Date(21, Sep, 2016), Period(5, Years)), (Date(21, Sep, 2016), Date(20, Dec, 2021))),
            ((Date(19, Dec, 2016), Period(5, Years)), (Date(19, Dec, 2016), Date(20, Dec, 2021))),
            ((Date(20, Dec, 2016), Period(5, Years)), (Date(20, Dec, 2016), Date(20, Mar, 2022))),
            ((Date(21, Dec, 2016), Period(5, Years)), (Date(21, Dec, 2016), Date(20, Mar, 2022)))]

        self._testCDSConventions(inputs, DateGeneration.OldCDS)

    def testCDS2015ConventionSampleDates(self):
        TEST_MESSAGE(
            "Testing all dates in sample CDS schedule(s) for rule CDS2015...")

        rule = DateGeneration.CDS2015
        tenor = Period(1, Years)

        tradeDate = Date(18, Sep, 2015)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expDates = [
            Date(22, Jun, 2015), Date(21, Sep, 2015), Date(21, Dec, 2015),
            Date(21, Mar, 2016), Date(20, Jun, 2016)]
        self.check_dates(s, expDates)

        tradeDate = Date(19, Sep, 2015)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        self.check_dates(s, expDates)

        tradeDate = Date(20, Sep, 2015)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expDates.append(Date(20, Sep, 2016))
        expDates.append(Date(20, Dec, 2016))
        self.check_dates(s, expDates)

        tradeDate = Date(21, Sep, 2015)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expDates = expDates[1:]
        self.check_dates(s, expDates)

        tradeDate = Date(20, Jun, 2009)
        maturity = Date(20, Dec, 2009)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        tmp = [
            Date(20, Mar, 2009), Date(22, Jun, 2009),
            Date(21, Sep, 2009), Date(20, Dec, 2009)]
        expDates = tmp
        self.check_dates(s, expDates)

        tradeDate = Date(21, Jun, 2009)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        self.check_dates(s, expDates)

        tradeDate = Date(22, Jun, 2009)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expDates = expDates[1:]
        self.check_dates(s, expDates)

    def testCDSConventionSampleDates(self):
        TEST_MESSAGE(
            "Testing all dates in sample CDS schedule(s) for rule CDS...")

        rule = DateGeneration.CDS
        tenor = Period(1, Years)

        tradeDate = Date(18, Sep, 2015)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expDates = [
            Date(22, Jun, 2015), Date(21, Sep, 2015), Date(21, Dec, 2015),
            Date(21, Mar, 2016), Date(20, Jun, 2016), Date(20, Sep, 2016)]
        self.check_dates(s, expDates)

        tradeDate = Date(19, Sep, 2015)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        self.check_dates(s, expDates)

        tradeDate = Date(20, Sep, 2015)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expDates.append(Date(20, Dec, 2016))
        self.check_dates(s, expDates)

        tradeDate = Date(21, Sep, 2015)
        maturity = cdsMaturity(tradeDate, tenor, rule)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expDates = expDates[1:]
        self.check_dates(s, expDates)

        tradeDate = Date(20, Jun, 2009)
        maturity = Date(20, Dec, 2009)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        tmp = [
            Date(20, Mar, 2009), Date(22, Jun, 2009),
            Date(21, Sep, 2009), Date(20, Dec, 2009)]
        expDates = tmp
        self.check_dates(s, expDates)

        tradeDate = Date(21, Jun, 2009)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        self.check_dates(s, expDates)

        tradeDate = Date(22, Jun, 2009)
        s = makeCdsSchedule(tradeDate, maturity, rule)
        expDates = expDates[1:]
        self.check_dates(s, expDates)

    def testOldCDSConventionSampleDates(self):
        TEST_MESSAGE(
            "Testing all dates in sample CDS schedule(s) for rule OldCDS...")

        rule = DateGeneration.OldCDS
        tenor = Period(1, Years)

        tradeDatePlusOne = Date(18, Sep, 2015)
        maturity = cdsMaturity(tradeDatePlusOne, tenor, rule)
        s = makeCdsSchedule(tradeDatePlusOne, maturity, rule)
        expDates = [
            Date(18, Sep, 2015), Date(21, Dec, 2015),
            Date(21, Mar, 2016), Date(20, Jun, 2016),
            Date(20, Sep, 2016)]
        self.check_dates(s, expDates)

        expDates[0] = tradeDatePlusOne = Date(19, Sep, 2015)
        maturity = cdsMaturity(tradeDatePlusOne, tenor, rule)
        s = makeCdsSchedule(tradeDatePlusOne, maturity, rule)
        self.check_dates(s, expDates)

        expDates[0] = tradeDatePlusOne = Date(20, Sep, 2015)
        maturity = cdsMaturity(tradeDatePlusOne, tenor, rule)
        s = makeCdsSchedule(tradeDatePlusOne, maturity, rule)
        expDates.append(Date(20, Dec, 2016))
        self.check_dates(s, expDates)

        expDates[0] = tradeDatePlusOne = Date(21, Sep, 2015)
        maturity = cdsMaturity(tradeDatePlusOne, tenor, rule)
        s = makeCdsSchedule(tradeDatePlusOne, maturity, rule)
        self.check_dates(s, expDates)

        expDates[0] = tradeDatePlusOne = Date(19, Nov, 2015)
        s = makeCdsSchedule(tradeDatePlusOne, maturity, rule)
        self.check_dates(s, expDates)

        expDates[0] = tradeDatePlusOne = Date(20, Nov, 2015)
        s = makeCdsSchedule(tradeDatePlusOne, maturity, rule)
        self.check_dates(s, expDates)

        expDates[0] = tradeDatePlusOne = Date(21, Nov, 2015)
        s = makeCdsSchedule(tradeDatePlusOne, maturity, rule)
        expDates = [expDates[0]] + expDates[2:]
        self.check_dates(s, expDates)

    def testCDS2015ZeroMonthsMatured(self):
        TEST_MESSAGE(
            "Testing 0M tenor for CDS2015 where matured...")

        rule = DateGeneration.CDS2015
        tenor = Period(0, Months)

        inputs = [
            Date(20, Dec, 2015),
            Date(15, Feb, 2016),
            Date(19, Mar, 2016),
            Date(20, Jun, 2016),
            Date(15, Aug, 2016),
            Date(19, Sep, 2016),
            Date(20, Dec, 2016)]

        for input in inputs:
            self.assertTrue(cdsMaturity(input, tenor, rule) == NullDate())

    def testDateConstructor(self):
        TEST_MESSAGE(
            "Testing the constructor taking a vector of dates and "
            "possibly additional meta information...")

        dates = [
            Date(16, May, 2015),
            Date(18, May, 2015),
            Date(18, May, 2016),
            Date(31, December, 2017)]

        schedule1 = Schedule(dates)
        self.assertFalse(len(schedule1) != len(dates))
        for i in range(len(dates)):
            self.assertFalse(schedule1[i] != dates[i])
        self.assertFalse(schedule1.calendar() != NullCalendar())
        self.assertFalse(schedule1.businessDayConvention() != Unadjusted)

        regular = BoolVector(3)
        regular[0] = false
        regular[1] = true
        regular[2] = false
        schedule2 = Schedule(
            dates,
            TARGET(),
            Following,
            ModifiedPreceding,
            Period(1, Years),
            DateGeneration.Backward,
            true,
            regular)
        for i in range(1, len(dates)):
            self.assertFalse(schedule2.isRegular(i) != regular[i - 1])
        self.assertFalse(schedule2.calendar() != TARGET())
        self.assertFalse(schedule2.businessDayConvention() != Following)
        self.assertFalse(schedule2.terminationDateBusinessDayConvention() != ModifiedPreceding)
        self.assertFalse(schedule2.tenor() != Period(1, Years))
        self.assertFalse(schedule2.rule() != DateGeneration.Backward)
        self.assertFalse(not schedule2.endOfMonth())

    def testFourWeeksTenor(self):
        TEST_MESSAGE(
            "Testing that a four-weeks tenor works...")

        try:
            s = MakeSchedule()
            s.fromDate(Date(13, January, 2016))
            s.to(Date(4, May, 2016))
            s.withCalendar(TARGET())
            s.withTenor(Period(4, Weeks))
            s.withConvention(Following)
            s.forwards()
            s = s.makeSchedule()
        except Exception as e:
            print(e)

    def testScheduleAlwaysHasAStartDate(self):
        TEST_MESSAGE(
            "Testing that variations of MakeSchedule "
            "always produce a schedule with a start date...")
        calendar = UnitedStates(UnitedStates.GovernmentBond)
        schedule = MakeSchedule()
        schedule.fromDate(Date(10, January, 2017))
        schedule.withFirstDate(Date(31, August, 2017))
        schedule.to(Date(28, February, 2026))
        schedule.withFrequency(Semiannual)
        schedule.withCalendar(calendar)
        schedule.withConvention(Unadjusted)
        schedule.backwards()
        schedule.endOfMonth(false)
        schedule = schedule.makeSchedule()
        self.assertTrue(
            schedule.date(0) == Date(10, January, 2017),
            "The first element should always be the start date")
        schedule = MakeSchedule()
        schedule.fromDate(Date(10, January, 2017))
        schedule.to(Date(28, February, 2026))
        schedule.withFrequency(Semiannual)
        schedule.withCalendar(calendar)
        schedule.withConvention(Unadjusted)
        schedule.backwards()
        schedule.endOfMonth(false)
        schedule = schedule.makeSchedule()
        self.assertTrue(
            schedule.date(0) == Date(10, January, 2017),
            "The first element should always be the start date")
        schedule = MakeSchedule()
        schedule.fromDate(Date(31, August, 2017))
        schedule.to(Date(28, February, 2026))
        schedule.withFrequency(Semiannual)
        schedule.withCalendar(calendar)
        schedule.withConvention(Unadjusted)
        schedule.backwards()
        schedule.endOfMonth(false)
        schedule = schedule.makeSchedule()
        self.assertTrue(
            schedule.date(0) == Date(31, August, 2017),
            "The first element should always be the start date")

    def testShortEomSchedule(self):
        TEST_MESSAGE(
            "Testing short end-of-month schedule...")

        s = None

        try:
            s = MakeSchedule()
            s.fromDate(Date(21, Feb, 2019))
            s.to(Date(28, Feb, 2019))
            s.withCalendar(TARGET())
            s.withTenor(Period(1, Years))
            s.withConvention(ModifiedFollowing)
            s.withTerminationDateConvention(ModifiedFollowing)
            s.backwards()
            s.endOfMonth(true)
            s = s.makeSchedule()
        except Exception as e:
            print(e)

        self.assertTrue(len(s) == 2)
        self.assertTrue(s[0] == Date(21, Feb, 2019))
        self.assertTrue(s[1] == Date(28, Feb, 2019))

    def testFirstDateOnMaturity(self):
        TEST_MESSAGE(
            "Testing schedule with first date on maturity...")
        schedule = MakeSchedule()
        schedule.fromDate(Date(20, September, 2016))
        schedule.to(Date(20, December, 2016))
        schedule.withFirstDate(Date(20, December, 2016))
        schedule.withFrequency(Quarterly)
        schedule.withCalendar(UnitedStates(UnitedStates.GovernmentBond))
        schedule.withConvention(Unadjusted)
        schedule.backwards()
        schedule = schedule.makeSchedule()

        expected = DateVector(2)
        expected[0] = Date(20, September, 2016)
        expected[1] = Date(20, December, 2016)

        self.check_dates(schedule, expected)

        schedule = MakeSchedule()
        schedule.fromDate(Date(20, September, 2016))
        schedule.to(Date(20, December, 2016))
        schedule.withFirstDate(Date(20, December, 2016))
        schedule.withFrequency(Quarterly)
        schedule.withCalendar(UnitedStates(UnitedStates.GovernmentBond))
        schedule.withConvention(Unadjusted)
        schedule.forwards()
        schedule = schedule.makeSchedule()

        self.check_dates(schedule, expected)

    def testNextToLastDateOnStart(self):
        TEST_MESSAGE(
            "Testing schedule with next-to-last date on start date...")
        schedule = MakeSchedule()
        schedule.fromDate(Date(20, September, 2016))
        schedule.to(Date(20, December, 2016))
        schedule.withNextToLastDate(Date(20, September, 2016))
        schedule.withFrequency(Quarterly)
        schedule.withCalendar(UnitedStates(UnitedStates.GovernmentBond))
        schedule.withConvention(Unadjusted)
        schedule.backwards()
        schedule = schedule.makeSchedule()

        expected = DateVector(2)
        expected[0] = Date(20, September, 2016)
        expected[1] = Date(20, December, 2016)

        self.check_dates(schedule, expected)

        schedule = MakeSchedule()
        schedule.fromDate(Date(20, September, 2016))
        schedule.to(Date(20, December, 2016))
        schedule.withNextToLastDate(Date(20, September, 2016))
        schedule.withFrequency(Quarterly)
        schedule.withCalendar(UnitedStates(UnitedStates.GovernmentBond))
        schedule.withConvention(Unadjusted)
        schedule.backwards()
        schedule = schedule.makeSchedule()

        self.check_dates(schedule, expected)

    def testTruncation(self):
        TEST_MESSAGE(
            "Testing schedule truncation...")
        s = MakeSchedule()
        s.fromDate(Date(30, September, 2009))
        s.to(Date(15, June, 2020))
        s.withCalendar(Japan())
        s.withTenor(Period(6, Months))
        s.withConvention(Following)
        s.withTerminationDateConvention(Following)
        s.forwards()
        s.endOfMonth()
        s = s.makeSchedule()

        t = s.until(Date(1, Jan, 2014))
        expected = DateVector(10)
        expected[0] = Date(30, September, 2009)
        expected[1] = Date(31, March, 2010)
        expected[2] = Date(30, September, 2010)
        expected[3] = Date(31, March, 2011)
        expected[4] = Date(30, September, 2011)
        expected[5] = Date(30, March, 2012)
        expected[6] = Date(28, September, 2012)
        expected[7] = Date(29, March, 2013)
        expected[8] = Date(30, September, 2013)
        expected[9] = Date(1, January, 2014)
        self.check_dates(t, expected)
        self.assertTrue(t.isRegular()[-1] == false)

        t = s.until(Date(30, September, 2013))
        expected = DateVector(9)
        expected[0] = Date(30, September, 2009)
        expected[1] = Date(31, March, 2010)
        expected[2] = Date(30, September, 2010)
        expected[3] = Date(31, March, 2011)
        expected[4] = Date(30, September, 2011)
        expected[5] = Date(30, March, 2012)
        expected[6] = Date(28, September, 2012)
        expected[7] = Date(29, March, 2013)
        expected[8] = Date(30, September, 2013)
        self.check_dates(t, expected)
        self.assertTrue(t.isRegular()[-1] == true)

        t = s.after(Date(1, Jan, 2014))
        expected = DateVector(15)
        expected[0] = Date(1, January, 2014)
        expected[1] = Date(31, March, 2014)
        expected[2] = Date(30, September, 2014)
        expected[3] = Date(31, March, 2015)
        expected[4] = Date(30, September, 2015)
        expected[5] = Date(31, March, 2016)
        expected[6] = Date(30, September, 2016)
        expected[7] = Date(31, March, 2017)
        expected[8] = Date(29, September, 2017)
        expected[9] = Date(30, March, 2018)
        expected[10] = Date(28, September, 2018)
        expected[11] = Date(29, March, 2019)
        expected[12] = Date(30, September, 2019)
        expected[13] = Date(31, March, 2020)
        expected[14] = Date(30, June, 2020)
        self.check_dates(t, expected)
        self.assertTrue(t.isRegular()[0] == false)

        t = s.after(Date(28, September, 2018))
        expected = DateVector(5)
        expected[0] = Date(28, September, 2018)
        expected[1] = Date(29, March, 2019)
        expected[2] = Date(30, September, 2019)
        expected[3] = Date(31, March, 2020)
        expected[4] = Date(30, June, 2020)
        self.check_dates(t, expected)
        self.assertTrue(t.isRegular()[0] == true)

    def check_dates(self,
                    s,
                    expected):
        self.assertFalse(len(s) != len(expected))

        for i in range(len(expected)):
            self.assertFalse(s[i] != expected[i])

    def _testCDSConventions(self,
                            inputs,
                            rule):
        for input in inputs:
            fromDate = input[0][0]
            tenor = input[0][1]

            maturity = cdsMaturity(fromDate, tenor, rule)
            expEnd = input[1][1]
            self.assertTrue(maturity, expEnd)

            s = makeCdsSchedule(fromDate, maturity, rule)

            expStart = input[1][0]
            start = s.startDate()
            end = s.endDate()
            self.assertTrue(start, expStart)
            self.assertTrue(end, expEnd)
