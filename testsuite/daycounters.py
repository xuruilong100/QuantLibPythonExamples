import unittest

from QuantLib import *

from utilities import *


class SingleCaseI(object):
    def __init__(self,
                 convention,
                 start,
                 end,
                 refStart,
                 refEnd,
                 result):
        self.convention = convention
        self.start = start
        self.end = end
        self.refStart = refStart
        self.refEnd = refEnd
        self.result = result


class SingleCaseII(object):
    def __init__(self,
                 convention,
                 start,
                 end,
                 result):
        self.convention = convention
        self.start = start
        self.end = end
        self.refStart = Date()
        self.refEnd = Date()
        self.result = result


def ISMAYearFractionWithReferenceDates(dayCounter,
                                       start,
                                       end,
                                       refStart,
                                       refEnd):
    referenceDayCount = dayCounter.dayCount(refStart, refEnd)

    couponsPerYear = round(365.0 / referenceDayCount)

    return dayCounter.dayCount(start, end) / (referenceDayCount * couponsPerYear)


def actualActualDaycountComputation(schedule,
                                    start,
                                    end):
    daycounter = ActualActual(ActualActual.ISMA, schedule)
    yearFraction = 0.0

    for i in range(1, len(schedule) - 1):
        referenceStart = schedule.date(i)
        referenceEnd = schedule.date(i + 1)
        if start < referenceEnd and end > referenceStart:
            yearFraction += ISMAYearFractionWithReferenceDates(
                daycounter,
                start if start > referenceStart else referenceStart,
                end if end < referenceEnd else referenceEnd,
                referenceStart,
                referenceEnd)

    return yearFraction


class Thirty360Case(object):
    def __init__(self,
                 start,
                 end,
                 expected):
        self.start = start
        self.end = end
        self.expected = expected


class DayCounterTest(unittest.TestCase):

    def testActualActual(self):
        TEST_MESSAGE(
            "Testing actual/actual day counters...")

        testCases = [
            SingleCaseII(ActualActual.ISDA, Date(1, November, 2003), Date(1, May, 2004), 0.497724380567),
            SingleCaseI(ActualActual.ISMA, Date(1, November, 2003), Date(1, May, 2004), Date(1, November, 2003), Date(1, May, 2004), 0.500000000000),
            SingleCaseII(ActualActual.AFB, Date(1, November, 2003), Date(1, May, 2004), 0.497267759563),
            SingleCaseII(ActualActual.ISDA, Date(1, February, 1999), Date(1, July, 1999), 0.410958904110),
            SingleCaseI(ActualActual.ISMA, Date(1, February, 1999), Date(1, July, 1999), Date(1, July, 1998), Date(1, July, 1999), 0.410958904110),
            SingleCaseII(ActualActual.AFB, Date(1, February, 1999), Date(1, July, 1999), 0.410958904110),
            SingleCaseII(ActualActual.ISDA, Date(1, July, 1999), Date(1, July, 2000), 1.001377348600),
            SingleCaseI(ActualActual.ISMA, Date(1, July, 1999), Date(1, July, 2000), Date(1, July, 1999), Date(1, July, 2000), 1.000000000000),
            SingleCaseII(ActualActual.AFB, Date(1, July, 1999), Date(1, July, 2000), 1.000000000000),
            SingleCaseII(ActualActual.ISDA, Date(15, August, 2002), Date(15, July, 2003), 0.915068493151),
            SingleCaseI(ActualActual.ISMA, Date(15, August, 2002), Date(15, July, 2003), Date(15, January, 2003), Date(15, July, 2003), 0.915760869565),
            SingleCaseII(ActualActual.AFB, Date(15, August, 2002), Date(15, July, 2003), 0.915068493151),
            SingleCaseII(ActualActual.ISDA, Date(15, July, 2003), Date(15, January, 2004), 0.504004790778),
            SingleCaseI(ActualActual.ISMA, Date(15, July, 2003), Date(15, January, 2004), Date(15, July, 2003), Date(15, January, 2004), 0.500000000000),
            SingleCaseII(ActualActual.AFB, Date(15, July, 2003), Date(15, January, 2004), 0.504109589041),
            SingleCaseII(ActualActual.ISDA, Date(30, July, 1999), Date(30, January, 2000), 0.503892506924),
            SingleCaseI(ActualActual.ISMA, Date(30, July, 1999), Date(30, January, 2000), Date(30, July, 1999), Date(30, January, 2000), 0.500000000000),
            SingleCaseII(ActualActual.AFB, Date(30, July, 1999), Date(30, January, 2000), 0.504109589041),
            SingleCaseII(ActualActual.ISDA, Date(30, January, 2000), Date(30, June, 2000), 0.415300546448),
            SingleCaseI(ActualActual.ISMA, Date(30, January, 2000), Date(30, June, 2000), Date(30, January, 2000), Date(30, July, 2000), 0.417582417582),
            SingleCaseII(ActualActual.AFB, Date(30, January, 2000), Date(30, June, 2000), 0.41530054644)]

        n = len(testCases)
        for i in range(n):
            dayCounter = ActualActual(testCases[i].convention)
            d1 = testCases[i].start
            d2 = testCases[i].end
            rd1 = testCases[i].refStart
            rd2 = testCases[i].refEnd
            calculated = dayCounter.yearFraction(d1, d2, rd1, rd2)

            if abs(calculated - testCases[i].result) > 1.0e-10:
                self.assertFalse(testCases[i].convention == ActualActual.ISMA)

    def testActualActualIsma(self):
        TEST_MESSAGE(
            "Testing actual/actual (ISMA) with odd last period...")

        isEndOfMonth = false
        frequency = Semiannual
        interestAccrualDate = Date(30, Jan, 1999)
        maturityDate = Date(30, Jun, 2000)
        firstCouponDate = Date(30, Jul, 1999)
        penultimateCouponDate = Date(30, Jan, 2000)
        d1 = Date(30, Jan, 2000)
        d2 = Date(30, Jun, 2000)

        expected = 152. / (182. * 2)

        schedule = MakeSchedule()
        schedule.fromDate(interestAccrualDate)
        schedule.to(maturityDate)
        schedule.withFrequency(frequency)
        schedule.withFirstDate(firstCouponDate)
        schedule.withNextToLastDate(penultimateCouponDate)
        schedule.endOfMonth(isEndOfMonth)
        schedule = schedule.makeSchedule()

        dayCounter = ActualActual(ActualActual.ISMA, schedule)

        calculated = dayCounter.yearFraction(d1, d2)

        self.assertFalse(abs(calculated - expected) > 1.0e-10)

        isEndOfMonth = true
        frequency = Quarterly
        interestAccrualDate = Date(31, May, 1999)
        maturityDate = Date(30, Apr, 2000)
        firstCouponDate = Date(31, Aug, 1999)
        penultimateCouponDate = Date(30, Nov, 1999)
        d1 = Date(30, Nov, 1999)
        d2 = Date(30, Apr, 2000)

        expected = 91.0 / (91.0 * 4) + 61.0 / (92.0 * 4)

        schedule = MakeSchedule()
        schedule.fromDate(interestAccrualDate)
        schedule.to(maturityDate)
        schedule.withFrequency(frequency)
        schedule.withFirstDate(firstCouponDate)
        schedule.withNextToLastDate(penultimateCouponDate)
        schedule.endOfMonth(isEndOfMonth)
        schedule = schedule.makeSchedule()

        dayCounter = ActualActual(ActualActual.ISMA, schedule)

        calculated = dayCounter.yearFraction(d1, d2)

        self.assertFalse(abs(calculated - expected) > 1.0e-10)

        isEndOfMonth = false
        frequency = Quarterly
        interestAccrualDate = Date(31, May, 1999)
        maturityDate = Date(30, Apr, 2000)
        firstCouponDate = Date(31, Aug, 1999)
        penultimateCouponDate = Date(30, Nov, 1999)
        d1 = Date(30, Nov, 1999)
        d2 = Date(30, Apr, 2000)

        expected = 91.0 / (91.0 * 4) + 61.0 / (90.0 * 4)

        schedule = MakeSchedule()
        schedule.fromDate(interestAccrualDate)
        schedule.to(maturityDate)
        schedule.withFrequency(frequency)
        schedule.withFirstDate(firstCouponDate)
        schedule.withNextToLastDate(penultimateCouponDate)
        schedule.endOfMonth(isEndOfMonth)
        schedule = schedule.makeSchedule()

        dayCounter = ActualActual(ActualActual.ISMA, schedule)

        calculated = dayCounter.yearFraction(d1, d2)

        self.assertFalse(abs(calculated - expected) > 1.0e-10)

    def testActualActualWithSchedule(self):
        TEST_MESSAGE(
            "Testing actual/actual day counter with schedule...")

        issueDateExpected = Date(17, January, 2017)
        firstCouponDateExpected = Date(31, August, 2017)

        schedule = MakeSchedule()
        schedule.fromDate(issueDateExpected)
        schedule.withFirstDate(firstCouponDateExpected)
        schedule.to(Date(28, February, 2026))
        schedule.withFrequency(Semiannual)
        schedule.withCalendar(Canada())
        schedule.withConvention(Unadjusted)
        schedule.backwards()
        schedule.endOfMonth()
        schedule = schedule.makeSchedule()

        issueDate = schedule.date(0)
        self.assertTrue(issueDate == issueDateExpected)
        firstCouponDate = schedule.date(1)
        self.assertTrue(firstCouponDate == firstCouponDateExpected)

        quasiCouponDate2 = schedule.calendar().advance(
            firstCouponDate,
            -schedule.tenor(),
            schedule.businessDayConvention(),
            schedule.endOfMonth())
        quasiCouponDate1 = schedule.calendar().advance(
            quasiCouponDate2,
            -schedule.tenor(),
            schedule.businessDayConvention(),
            schedule.endOfMonth())

        quasiCouponDate1Expected = Date(31, August, 2016)
        quasiCouponDate2Expected = Date(28, February, 2017)

        self.assertTrue(quasiCouponDate2 == quasiCouponDate2Expected)
        self.assertTrue(quasiCouponDate1 == quasiCouponDate1Expected)

        dayCounter = ActualActual(ActualActual.ISMA, schedule)

        t_with_reference = dayCounter.yearFraction(
            issueDate, firstCouponDate,
            quasiCouponDate2, firstCouponDate)
        t_no_reference = dayCounter.yearFraction(
            issueDate, firstCouponDate)
        t_total = ISMAYearFractionWithReferenceDates(
            dayCounter,
            issueDate, quasiCouponDate2,
            quasiCouponDate1, quasiCouponDate2) + 0.5
        expected = 0.6160220994

        self.assertFalse(abs(t_total - expected) > 1.0e-10)
        self.assertFalse(abs(t_with_reference - expected) > 1.0e-10)
        self.assertFalse(abs(t_no_reference - t_with_reference) > 1.0e-10)

        settlementDate = Date(29, January, 2017)

        t_with_reference = ISMAYearFractionWithReferenceDates(
            dayCounter,
            issueDate, settlementDate,
            quasiCouponDate1, quasiCouponDate2)
        t_no_reference = dayCounter.yearFraction(issueDate, settlementDate)
        t_expected_first_qp = 0.03314917127071823
        self.assertFalse(abs(t_with_reference - t_expected_first_qp) > 1.0e-10)
        self.assertFalse(abs(t_no_reference - t_with_reference) > 1.0e-10)
        t2 = dayCounter.yearFraction(settlementDate, firstCouponDate)
        self.assertFalse(abs(t_expected_first_qp + t2 - expected) > 1.0e-10)

        settlementDate = Date(29, July, 2017)

        t_no_reference = dayCounter.yearFraction(issueDate, settlementDate)
        t_with_reference = ISMAYearFractionWithReferenceDates(
            dayCounter,
            issueDate, quasiCouponDate2,
            quasiCouponDate1, quasiCouponDate2) + \
                           ISMAYearFractionWithReferenceDates(
                               dayCounter,
                               quasiCouponDate2, settlementDate,
                               quasiCouponDate2, firstCouponDate)
        self.assertFalse(abs(t_no_reference - t_with_reference) > 1.0e-10)
        t2 = dayCounter.yearFraction(settlementDate, firstCouponDate)

        self.assertFalse(abs(t_total - (t_no_reference + t2)) > 1.0e-10)

    def testActualActualWithAnnualSchedule(self):
        TEST_MESSAGE(
            "Testing actual/actual with schedule for undefined annual reference periods...")

        calendar = UnitedStates(UnitedStates.GovernmentBond)
        schedule = MakeSchedule()
        schedule.fromDate(Date(10, January, 2017))
        schedule.withFirstDate(Date(31, August, 2017))
        schedule.to(Date(28, February, 2026))
        schedule.withFrequency(Annual)
        schedule.withCalendar(calendar)
        schedule.withConvention(Unadjusted)
        schedule.backwards().endOfMonth(false)
        schedule = schedule.makeSchedule()

        referencePeriodStart = schedule.date(1)
        referencePeriodEnd = schedule.date(2)

        testDate = schedule.date(1)
        dayCounter = ActualActual(ActualActual.ISMA, schedule)

        while testDate < referencePeriodEnd:
            difference = ISMAYearFractionWithReferenceDates(
                dayCounter,
                testDate, referencePeriodEnd,
                referencePeriodStart, referencePeriodEnd) - \
                         dayCounter.yearFraction(testDate, referencePeriodEnd)
            self.assertFalse(abs(difference) > 1.0e-10)

            testDate = calendar.advance(testDate, 1, Days)

    def testActualActualWithSemiannualSchedule(self):
        TEST_MESSAGE(
            "Testing actual/actual with schedule "
            "for undefined semiannual reference periods...")

        calendar = UnitedStates(UnitedStates.GovernmentBond)
        fromDate = Date(10, January, 2017)
        firstCoupon = Date(31, August, 2017)
        quasiCoupon = Date(28, February, 2017)
        quasiCoupon2 = Date(31, August, 2016)

        schedule = MakeSchedule()
        schedule.fromDate(fromDate)
        schedule.withFirstDate(firstCoupon)
        schedule.to(Date(28, February, 2026))
        schedule.withFrequency(Semiannual)
        schedule.withCalendar(calendar)
        schedule.withConvention(Unadjusted)
        schedule.backwards().endOfMonth(true)
        schedule = schedule.makeSchedule()

        testDate = schedule.date(1)
        dayCounter = ActualActual(ActualActual.ISMA, schedule)
        dayCounterNoSchedule = ActualActual(ActualActual.ISMA)

        referencePeriodStart = schedule.date(1)
        referencePeriodEnd = schedule.date(2)

        self.assertTrue(
            dayCounter.yearFraction(
                referencePeriodStart,
                referencePeriodStart) == 0.0,
            "This should be zero.")
        self.assertTrue(
            dayCounterNoSchedule.yearFraction(
                referencePeriodStart,
                referencePeriodStart) == 0.0,
            "This should be zero")
        self.assertTrue(
            dayCounterNoSchedule.yearFraction(
                referencePeriodStart,
                referencePeriodStart,
                referencePeriodStart,
                referencePeriodStart) == 0.0,
            "This should be zero")
        self.assertTrue(
            dayCounter.yearFraction(
                referencePeriodStart,
                referencePeriodEnd) == 0.5)
        self.assertTrue(
            dayCounterNoSchedule.yearFraction(
                referencePeriodStart,
                referencePeriodEnd,
                referencePeriodStart,
                referencePeriodEnd) == 0.5,
            "This should be exact for explicit reference "
            "periods with no schedule")

        while testDate < referencePeriodEnd:
            difference = dayCounter.yearFraction(
                testDate, referencePeriodEnd,
                referencePeriodStart, referencePeriodEnd) - dayCounter.yearFraction(testDate, referencePeriodEnd)
            self.assertFalse(abs(difference) > 1.0e-10)
            testDate = calendar.advance(testDate, 1, Days)

        calculatedYearFraction = dayCounter.yearFraction(fromDate, firstCoupon)
        expectedYearFraction = 0.5 + (dayCounter.dayCount(fromDate, quasiCoupon)) / \
                               (2 * dayCounter.dayCount(quasiCoupon2, quasiCoupon))

        self.assertTrue(
            abs(calculatedYearFraction - expectedYearFraction) < 1.0e-10)

        schedule = MakeSchedule()
        schedule.fromDate(Date(10, January, 2017))
        schedule.withFirstDate(Date(31, August, 2017))
        schedule.to(Date(28, February, 2026))
        schedule.withFrequency(Semiannual)
        schedule.withCalendar(calendar)
        schedule.withConvention(Unadjusted)
        schedule.backwards().endOfMonth(false)
        schedule = schedule.makeSchedule()

        periodStartDate = schedule.date(1)
        periodEndDate = schedule.date(2)

        dayCounter = ActualActual(ActualActual.ISMA, schedule)

        while periodEndDate < schedule.date(len(schedule) - 2):
            expected = actualActualDaycountComputation(
                schedule,
                periodStartDate,
                periodEndDate)
            calculated = dayCounter.yearFraction(periodStartDate, periodEndDate)

            self.assertFalse(abs(expected - calculated) > 1e-8)
            periodEndDate = calendar.advance(periodEndDate, 1, Days)

    def testSimple(self):
        TEST_MESSAGE(
            "Testing simple day counter...")

        p = [Period(3, Months), Period(6, Months), Period(1, Years)]
        expected = [0.25, 0.5, 1.0]
        n = len(p)

        first = Date(1, January, 2002)
        last = Date(31, December, 2005)
        dayCounter = SimpleDayCounter()

        start = first
        while start <= last:

            for i in range(n):
                end = start + p[i]
                calculated = dayCounter.yearFraction(start, end)
                self.assertFalse(abs(calculated - expected[i]) > 1.0e-12)
                start += Period(1, Days)

    def testOne(self):
        TEST_MESSAGE(
            "Testing 1/1 day counter...")

        p = [Period(3, Months), Period(6, Months), Period(1, Years)]
        expected = [1.0, 1.0, 1.0]
        n = len(p)

        first = Date(1, January, 2004)
        last = Date(31, December, 2004)
        dayCounter = OneDayCounter()

        start = first
        while start <= last:

            for i in range(n):
                end = start + p[i]
                calculated = dayCounter.yearFraction(start, end)
                self.assertFalse(abs(calculated - expected[i]) > 1.0e-12)
                start += Period(1, Days)

    def testBusiness252(self):
        TEST_MESSAGE(
            "Testing business/252 day counter...")

        testDates = [
            Date(1, February, 2002),
            Date(4, February, 2002),
            Date(16, May, 2003),
            Date(17, December, 2003),
            Date(17, December, 2004),
            Date(19, December, 2005),
            Date(2, January, 2006),
            Date(13, March, 2006),
            Date(15, May, 2006),
            Date(17, March, 2006),
            Date(15, May, 2006),
            Date(26, July, 2006),
            Date(28, June, 2007),
            Date(16, September, 2009),
            Date(26, July, 2016)]

        expected = [
            0.0039682539683,
            1.2738095238095,
            0.6031746031746,
            0.9960317460317,
            1.0000000000000,
            0.0396825396825,
            0.1904761904762,
            0.1666666666667,
            -0.1507936507937,
            0.1507936507937,
            0.2023809523810,
            0.912698412698,
            2.214285714286,
            6.84126984127]

        dayCounter1 = Business252(Brazil())

        for i in range(1, len(testDates)):
            calculated = dayCounter1.yearFraction(testDates[i - 1], testDates[i])
            self.assertFalse(abs(calculated - expected[i - 1]) > 1.0e-12)

        dayCounter2 = Business252()

        for i in range(1, len(testDates)):
            calculated = dayCounter2.yearFraction(testDates[i - 1], testDates[i])
            self.assertFalse(abs(calculated - expected[i - 1]) > 1.0e-12)

    def testThirty365(self):
        TEST_MESSAGE(
            "Testing 30/365 day counter...")

        d1 = Date(17, June, 2011)
        d2 = Date(30, December, 2012)
        dayCounter = Thirty365()

        days = dayCounter.dayCount(d1, d2)
        self.assertFalse(days != 553)

        t = dayCounter.yearFraction(d1, d2)
        expected = 553 / 365.0
        self.assertFalse(abs(t - expected) > 1.0e-12)

    def testThirty360_BondBasis(self):
        TEST_MESSAGE(
            "Testing 30/360 day counter (Bond Basis)...")

        dayCounter = Thirty360(Thirty360.BondBasis)

        data = [
            Thirty360Case(Date(20, August, 2006), Date(20, February, 2007), 180),
            Thirty360Case(Date(20, February, 2007), Date(20, August, 2007), 180),
            Thirty360Case(Date(20, August, 2007), Date(20, February, 2008), 180),
            Thirty360Case(Date(20, February, 2008), Date(20, August, 2008), 180),
            Thirty360Case(Date(20, August, 2008), Date(20, February, 2009), 180),
            Thirty360Case(Date(20, February, 2009), Date(20, August, 2009), 180),
            Thirty360Case(Date(31, August, 2006), Date(28, February, 2007), 178),
            Thirty360Case(Date(28, February, 2007), Date(31, August, 2007), 183),
            Thirty360Case(Date(31, August, 2007), Date(29, February, 2008), 179),
            Thirty360Case(Date(29, February, 2008), Date(31, August, 2008), 182),
            Thirty360Case(Date(31, August, 2008), Date(28, February, 2009), 178),
            Thirty360Case(Date(28, February, 2009), Date(31, August, 2009), 183),
            Thirty360Case(Date(31, January, 2006), Date(28, February, 2006), 28),
            Thirty360Case(Date(30, January, 2006), Date(28, February, 2006), 28),
            Thirty360Case(Date(28, February, 2006), Date(3, March, 2006), 5),
            Thirty360Case(Date(14, February, 2006), Date(28, February, 2006), 14),
            Thirty360Case(Date(30, September, 2006), Date(31, October, 2006), 30),
            Thirty360Case(Date(31, October, 2006), Date(28, November, 2006), 28),
            Thirty360Case(Date(31, August, 2007), Date(28, February, 2008), 178),
            Thirty360Case(Date(28, February, 2008), Date(28, August, 2008), 180),
            Thirty360Case(Date(28, February, 2008), Date(30, August, 2008), 182),
            Thirty360Case(Date(28, February, 2008), Date(31, August, 2008), 183),
            Thirty360Case(Date(26, February, 2007), Date(28, February, 2008), 362),
            Thirty360Case(Date(26, February, 2007), Date(29, February, 2008), 363),
            Thirty360Case(Date(29, February, 2008), Date(28, February, 2009), 359),
            Thirty360Case(Date(28, February, 2008), Date(30, March, 2008), 32),
            Thirty360Case(Date(28, February, 2008), Date(31, March, 2008), 33)]

        for x in data:
            calculated = dayCounter.dayCount(x.start, x.end)
            self.assertFalse(calculated != x.expected)

    def testThirty360_EurobondBasis(self):
        TEST_MESSAGE(
            "Testing 30/360 day counter (Eurobond Basis)...")

        dayCounter = Thirty360(Thirty360.EurobondBasis)

        data = [
            Thirty360Case(Date(20, August, 2006), Date(20, February, 2007), 180),
            Thirty360Case(Date(20, February, 2007), Date(20, August, 2007), 180),
            Thirty360Case(Date(20, August, 2007), Date(20, February, 2008), 180),
            Thirty360Case(Date(20, February, 2008), Date(20, August, 2008), 180),
            Thirty360Case(Date(20, August, 2008), Date(20, February, 2009), 180),
            Thirty360Case(Date(20, February, 2009), Date(20, August, 2009), 180),
            Thirty360Case(Date(28, February, 2006), Date(31, August, 2006), 182),
            Thirty360Case(Date(31, August, 2006), Date(28, February, 2007), 178),
            Thirty360Case(Date(28, February, 2007), Date(31, August, 2007), 182),
            Thirty360Case(Date(31, August, 2007), Date(29, February, 2008), 179),
            Thirty360Case(Date(29, February, 2008), Date(31, August, 2008), 181),
            Thirty360Case(Date(31, August, 2008), Date(28, Feb, 2009), 178),
            Thirty360Case(Date(28, February, 2009), Date(31, August, 2009), 182),
            Thirty360Case(Date(31, August, 2009), Date(28, Feb, 2010), 178),
            Thirty360Case(Date(28, February, 2010), Date(31, August, 2010), 182),
            Thirty360Case(Date(31, August, 2010), Date(28, Feb, 2011), 178),
            Thirty360Case(Date(28, February, 2011), Date(31, August, 2011), 182),
            Thirty360Case(Date(31, August, 2011), Date(29, Feb, 2012), 179),
            Thirty360Case(Date(31, January, 2006), Date(28, February, 2006), 28),
            Thirty360Case(Date(30, January, 2006), Date(28, February, 2006), 28),
            Thirty360Case(Date(28, February, 2006), Date(3, March, 2006), 5),
            Thirty360Case(Date(14, February, 2006), Date(28, February, 2006), 14),
            Thirty360Case(Date(30, September, 2006), Date(31, October, 2006), 30),
            Thirty360Case(Date(31, October, 2006), Date(28, November, 2006), 28),
            Thirty360Case(Date(31, August, 2007), Date(28, February, 2008), 178),
            Thirty360Case(Date(28, February, 2008), Date(28, August, 2008), 180),
            Thirty360Case(Date(28, February, 2008), Date(30, August, 2008), 182),
            Thirty360Case(Date(28, February, 2008), Date(31, August, 2008), 182),
            Thirty360Case(Date(26, February, 2007), Date(28, February, 2008), 362),
            Thirty360Case(Date(26, February, 2007), Date(29, February, 2008), 363),
            Thirty360Case(Date(29, February, 2008), Date(28, February, 2009), 359),
            Thirty360Case(Date(28, February, 2008), Date(30, March, 2008), 32),
            Thirty360Case(Date(28, February, 2008), Date(31, March, 2008), 32)]

        for x in data:
            calculated = dayCounter.dayCount(x.start, x.end)
            self.assertFalse(calculated != x.expected)

    def testThirty360_ISDA(self):
        TEST_MESSAGE(
            "Testing 30/360 day counter (ISDA)...")

        data1 = [
            Thirty360Case(Date(20, August, 2006), Date(20, February, 2007), 180),
            Thirty360Case(Date(20, February, 2007), Date(20, August, 2007), 180),
            Thirty360Case(Date(20, August, 2007), Date(20, February, 2008), 180),
            Thirty360Case(Date(20, February, 2008), Date(20, August, 2008), 180),
            Thirty360Case(Date(20, August, 2008), Date(20, February, 2009), 180),
            Thirty360Case(Date(20, February, 2009), Date(20, August, 2009), 180)]

        terminationDate = Date(20, August, 2009)
        dayCounter = Thirty360(Thirty360.ISDA, terminationDate)

        for x in data1:
            calculated = dayCounter.dayCount(x.start, x.end)
            self.assertFalse(calculated != x.expected)

        data2 = [
            Thirty360Case(Date(28, February, 2006), Date(31, August, 2006), 180),
            Thirty360Case(Date(31, August, 2006), Date(28, February, 2007), 180),
            Thirty360Case(Date(28, February, 2007), Date(31, August, 2007), 180),
            Thirty360Case(Date(31, August, 2007), Date(29, February, 2008), 180),
            Thirty360Case(Date(29, February, 2008), Date(31, August, 2008), 180),
            Thirty360Case(Date(31, August, 2008), Date(28, February, 2009), 180),
            Thirty360Case(Date(28, February, 2009), Date(31, August, 2009), 180),
            Thirty360Case(Date(31, August, 2009), Date(28, February, 2010), 180),
            Thirty360Case(Date(28, February, 2010), Date(31, August, 2010), 180),
            Thirty360Case(Date(31, August, 2010), Date(28, February, 2011), 180),
            Thirty360Case(Date(28, February, 2011), Date(31, August, 2011), 180),
            Thirty360Case(Date(31, August, 2011), Date(29, February, 2012), 179)]

        terminationDate = Date(29, February, 2012)
        dayCounter = Thirty360(Thirty360.ISDA, terminationDate)

        for x in data2:
            calculated = dayCounter.dayCount(x.start, x.end)
            self.assertFalse(calculated != x.expected)

        data3 = [
            Thirty360Case(Date(31, January, 2006), Date(28, February, 2006), 30),
            Thirty360Case(Date(30, January, 2006), Date(28, February, 2006), 30),
            Thirty360Case(Date(28, February, 2006), Date(3, March, 2006), 3),
            Thirty360Case(Date(14, February, 2006), Date(28, February, 2006), 16),
            Thirty360Case(Date(30, September, 2006), Date(31, October, 2006), 30),
            Thirty360Case(Date(31, October, 2006), Date(28, November, 2006), 28),
            Thirty360Case(Date(31, August, 2007), Date(28, February, 2008), 178),
            Thirty360Case(Date(28, February, 2008), Date(28, August, 2008), 180),
            Thirty360Case(Date(28, February, 2008), Date(30, August, 2008), 182),
            Thirty360Case(Date(28, February, 2008), Date(31, August, 2008), 182),
            Thirty360Case(Date(28, February, 2007), Date(28, February, 2008), 358),
            Thirty360Case(Date(28, February, 2007), Date(29, February, 2008), 359),
            Thirty360Case(Date(29, February, 2008), Date(28, February, 2009), 360),
            Thirty360Case(Date(29, February, 2008), Date(30, March, 2008), 30),
            Thirty360Case(Date(29, February, 2008), Date(31, March, 2008), 30)]

        terminationDate = Date(29, February, 2008)
        dayCounter = Thirty360(Thirty360.ISDA, terminationDate)

        for x in data3:
            calculated = dayCounter.dayCount(x.start, x.end)
            self.assertFalse(calculated != x.expected)

    def testActual365_Canadian(self):
        TEST_MESSAGE(
            "Testing that Actual/365 (Canadian) throws when needed...")

        dayCounter = Actual365Fixed(Actual365Fixed.Canadian)

        try:
            dayCounter.yearFraction(
                Date(10, September, 2018),
                Date(10, September, 2019))
        except Exception as e:
            print(e)

        try:
            dayCounter.yearFraction(
                Date(10, September, 2018),
                Date(12, September, 2018),
                Date(10, September, 2018),
                Date(15, September, 2018))
        except Exception as e:
            print(e)

    def testIntraday(self):
        TEST_MESSAGE(
            "Testing intraday behavior of day counter ...")

        d1 = Date(12, February, 2015)
        d2 = Date(14, February, 2015, 12, 34, 17, 1, 230298)

        tol = 100 * QL_EPSILON

        dayCounters = [
            ActualActual(ActualActual.ISDA), Actual365Fixed(), Actual360()]

        for dc in dayCounters:
            expected = ((12 * 60 + 34) * 60 + 17 + 0.231298) * dc.yearFraction(d1, d1 + 1) / 86400 + dc.yearFraction(d1, d1 + 2)

            self.assertTrue(
                abs(dc.yearFraction(d1, d2) - expected) < tol,
                "can not reproduce result for day counter " + dc.name())

            self.assertTrue(
                abs(dc.yearFraction(d2, d1) + expected) < tol,
                "can not reproduce result for day counter " + dc.name())

    def testActualActualOutOfScheduleRange(self):
        today = Date(10, November, 2020)
        temp = Settings.instance().evaluationDate
        Settings.instance().evaluationDate = today

        effectiveDate = Date(21, May, 2019)
        terminationDate = Date(21, May, 2029)
        tenor = Period(1, Years)
        calendar = China(China.IB)
        convention = Unadjusted
        terminationDateConvention = convention
        rule = DateGeneration.Backward
        endOfMonth = false

        schedule = Schedule(
            effectiveDate, terminationDate,
            tenor, calendar, convention,
            terminationDateConvention, rule, endOfMonth)
        dayCounter = ActualActual(
            ActualActual.Bond, schedule)
        raised = false

        try:
            dayCounter.yearFraction(today, today + Period(9, Years))
        except Exception as e:
            raised = true
            print(e)

        self.assertFalse(not raised)

        Settings.instance().evaluationDate = temp
