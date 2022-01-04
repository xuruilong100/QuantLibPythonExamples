import unittest
from utilities import *
from QuantLib import *


class DateTest(unittest.TestCase):

    def testConsistency(self):
        TEST_MESSAGE("Testing dates...")

        minDate = Date.minDate().serialNumber() + 1
        maxDate = Date.maxDate().serialNumber()

        dyold = Date(minDate - 1).dayOfYear()
        dold = Date(minDate - 1).dayOfMonth()
        mold = Date(minDate - 1).month()
        yold = Date(minDate - 1).year()
        wdold = Date(minDate - 1).weekday()

        for i in range(minDate, maxDate + 1):
            t = Date(i)
            serial = t.serialNumber()

            # check serial number consistency
            self.assertFalse(serial != i)

            dy = t.dayOfYear()
            d = t.dayOfMonth()
            m = t.month()
            y = t.year()
            wd = t.weekday()

            # check if skipping any date
            self.assertFalse(
                not ((dy == dyold + 1) or
                     (dy == 1 and dyold == 365 and not Date.isLeap(yold)) or
                     (dy == 1 and dyold == 366 and Date.isLeap(yold))))

            dyold = dy

            self.assertFalse(
                not ((d == dold + 1 and m == mold and y == yold) or
                     (d == 1 and m == mold + 1 and y == yold) or
                     (d == 1 and m == 1 and y == yold + 1)))

            dold = d
            mold = m
            yold = y

            # check month definition
            self.assertFalse(m < 1 or m > 12)

            # check day definition
            self.assertFalse(d < 1)

            self.assertFalse(
                not ((m == 1 and d <= 31) or
                     (m == 2 and d <= 28) or
                     (m == 2 and d == 29 and Date.isLeap(y)) or
                     (m == 3 and d <= 31) or
                     (m == 4 and d <= 30) or
                     (m == 5 and d <= 31) or
                     (m == 6 and d <= 30) or
                     (m == 7 and d <= 31) or
                     (m == 8 and d <= 31) or
                     (m == 9 and d <= 30) or
                     (m == 10 and d <= 31) or
                     (m == 11 and d <= 30) or
                     (m == 12 and d <= 31)))

            # check weekday definition
            self.assertFalse(
                not ((wd == wdold + 1) or
                     (wd == 1 and wdold == 7)))

            wdold = wd

            # create the same date with a different constructor
            s = Date(d, m, y)
            # check serial number consistency
            serial = s.serialNumber()
            self.assertFalse(serial != i)

    def testEcbDates(self):
        TEST_MESSAGE("Testing ECB dates...")

        knownDates = ECB.knownDates()
        self.assertFalse(len(knownDates) == 0)

        n = len(ECB.nextDates(Date.minDate()))
        self.assertFalse(n != len(knownDates))

        previousEcbDate = Date.minDate()
        for i in knownDates:
            currentEcbDate = i
            self.assertFalse(not ECB.isECBdate(currentEcbDate))

            ecbDateMinusOne = currentEcbDate - 1
            self.assertFalse(ECB.isECBdate(ecbDateMinusOne))
            self.assertFalse(ECB.nextDate(ecbDateMinusOne) != currentEcbDate)
            self.assertFalse(ECB.nextDate(previousEcbDate) != currentEcbDate)

            previousEcbDate = currentEcbDate

        knownDate = knownDates[0]
        ECB.removeDate(knownDate)
        self.assertFalse(ECB.isECBdate(knownDate))
        ECB.addDate(knownDate)
        self.assertFalse(not ECB.isECBdate(knownDate))

    def testImmDates(self):
        TEST_MESSAGE("Testing IMM dates...")

        IMMcodes = [
            "F0", "G0", "H0", "J0", "K0", "M0", "N0", "Q0", "U0", "V0", "X0", "Z0",
            "F1", "G1", "H1", "J1", "K1", "M1", "N1", "Q1", "U1", "V1", "X1", "Z1",
            "F2", "G2", "H2", "J2", "K2", "M2", "N2", "Q2", "U2", "V2", "X2", "Z2",
            "F3", "G3", "H3", "J3", "K3", "M3", "N3", "Q3", "U3", "V3", "X3", "Z3",
            "F4", "G4", "H4", "J4", "K4", "M4", "N4", "Q4", "U4", "V4", "X4", "Z4",
            "F5", "G5", "H5", "J5", "K5", "M5", "N5", "Q5", "U5", "V5", "X5", "Z5",
            "F6", "G6", "H6", "J6", "K6", "M6", "N6", "Q6", "U6", "V6", "X6", "Z6",
            "F7", "G7", "H7", "J7", "K7", "M7", "N7", "Q7", "U7", "V7", "X7", "Z7",
            "F8", "G8", "H8", "J8", "K8", "M8", "N8", "Q8", "U8", "V8", "X8", "Z8",
            "F9", "G9", "H9", "J9", "K9", "M9", "N9", "Q9", "U9", "V9", "X9", "Z9"]

        counter = Date(1, January, 2000)
        last = Date(1, January, 2040)

        while counter <= last:
            imm = IMM.nextDate(counter, false)

            # check that imm is greater than counter
            self.assertFalse(imm <= counter)

            # check that imm is an IMM date
            self.assertFalse(not IMM.isIMMdate(imm, false))

            # check that imm is <= to the next IMM date in the main cycle
            self.assertFalse(imm > IMM.nextDate(counter, true))

            # check that for every date IMMdate is the inverse of IMMcode
            self.assertFalse(IMM.date(IMM.code(imm), counter) != imm)

            # check that for every date the 120 IMM codes refer to future dates
            for i in range(40):
                self.assertFalse(IMM.date(IMMcodes[i], counter) < counter)

            counter = counter + 1

    def testAsxDates(self):
        TEST_MESSAGE("Testing ASX dates...")

        ASXcodes = [
            "F0", "G0", "H0", "J0", "K0", "M0", "N0", "Q0", "U0", "V0", "X0", "Z0",
            "F1", "G1", "H1", "J1", "K1", "M1", "N1", "Q1", "U1", "V1", "X1", "Z1",
            "F2", "G2", "H2", "J2", "K2", "M2", "N2", "Q2", "U2", "V2", "X2", "Z2",
            "F3", "G3", "H3", "J3", "K3", "M3", "N3", "Q3", "U3", "V3", "X3", "Z3",
            "F4", "G4", "H4", "J4", "K4", "M4", "N4", "Q4", "U4", "V4", "X4", "Z4",
            "F5", "G5", "H5", "J5", "K5", "M5", "N5", "Q5", "U5", "V5", "X5", "Z5",
            "F6", "G6", "H6", "J6", "K6", "M6", "N6", "Q6", "U6", "V6", "X6", "Z6",
            "F7", "G7", "H7", "J7", "K7", "M7", "N7", "Q7", "U7", "V7", "X7", "Z7",
            "F8", "G8", "H8", "J8", "K8", "M8", "N8", "Q8", "U8", "V8", "X8", "Z8",
            "F9", "G9", "H9", "J9", "K9", "M9", "N9", "Q9", "U9", "V9", "X9", "Z9"]

        counter = Date(1, January, 2000)
        last = Date(1, January, 2040)

        while counter <= last:
            asx = ASX.nextDate(counter, false)

            # check that asx is greater than counter
            self.assertFalse(asx <= counter)

            # check that asx is an ASX date
            self.assertFalse(not ASX.isASXdate(asx, false))

            # check that asx is <= to the next ASX date in the main cycle
            self.assertFalse(asx > ASX.nextDate(counter, true))

            # check that for every date ASXdate is the inverse of ASXcode
            self.assertFalse(ASX.date(ASX.code(asx), counter) != asx)

            # check that for every date the 120 ASX codes refer to future dates
            for ASXcode in ASXcodes:
                self.assertFalse(ASX.date(ASXcode, counter) < counter)

            counter = counter + 1

    def testIsoDates(self):
        TEST_MESSAGE("Testing ISO dates...")
        input_date = "2006-01-15"
        d = DateParser.parseISO(input_date)
        self.assertFalse(
            d.dayOfMonth() != 15 or
            d.month() != January or
            d.year() != 2006)

    def testParseDates(self):
        TEST_MESSAGE("Testing parsing of dates...")

        input_date = "2006-01-15"
        d = DateParser.parseFormatted(input_date, "%Y-%m-%d")
        self.assertFalse(d != Date(15, January, 2006))

        input_date = "12/02/2012"
        d = DateParser.parseFormatted(input_date, "%m/%d/%Y")
        self.assertFalse(d != Date(2, December, 2012))

        d = DateParser.parseFormatted(input_date, "%d/%m/%Y")
        self.assertFalse(d != Date(12, February, 2012))

        input_date = "20011002"
        d = DateParser.parseFormatted(input_date, "%Y%m%d")
        self.assertFalse(d != Date(2, October, 2001))

    @unittest.skip('skip testIntraday')
    def testIntraday(self):
        TEST_MESSAGE("Testing intraday information of dates...")

        d1 = Date(12, February, 2015, 10, 45, 12, 1234, 76253)

        self.assertTrue(d1.year() == 2015, "failed to reproduce year")
        self.assertTrue(d1.month() == February, "failed to reproduce month")
        self.assertTrue(d1.dayOfMonth() == 12, "failed to reproduce day")
        self.assertTrue(d1.hours() == 10, "failed to reproduce hour of day")
        self.assertTrue(d1.minutes() == 45, "failed to reproduce minute of hour")
        self.assertTrue(d1.seconds() == 13, "failed to reproduce second of minute")

        if Date.ticksPerSecond() == 1000:
            self.assertTrue(
                d1.fractionOfSecond() == 0.234,
                "failed to reproduce fraction of second")
        elif Date.ticksPerSecond() >= 1000000:
            self.assertTrue(
                d1.fractionOfSecond() == (234000 + 76253) / 1000000.0,
                "failed to reproduce fraction of second")

        if Date.ticksPerSecond() >= 1000:
            self.assertTrue(
                d1.milliseconds() == 234 + 76,
                "failed to reproduce number of milliseconds")

        if Date.ticksPerSecond() >= 100000:
            self.assertTrue(
                d1.microseconds() == 253,
                "failed to reproduce number of microseconds")

        d2 = Date(28, February, 2015, 50, 165, 476, 1234, 253)
        self.assertTrue(d2.year() == 2015, "failed to reproduce year")
        self.assertTrue(d2.month() == March, "failed to reproduce month")
        self.assertTrue(d2.dayOfMonth() == 2, "failed to reproduce day")
        self.assertTrue(d2.hours() == 4, "failed to reproduce hour of day")
        self.assertTrue(d2.minutes() == 52, "failed to reproduce minute of hour")
        self.assertTrue(d2.seconds() == 57, "failed to reproduce second of minute")

        if Date.ticksPerSecond() >= 1000:
            self.assertTrue(
                d2.milliseconds() == 234,
                "failed to reproduce number of milliseconds")
        if Date.ticksPerSecond() >= 1000000:
            self.assertTrue(
                d2.microseconds() == 253,
                "failed to reproduce number of microseconds")

        # std.ostringstream s
        s = Date(7, February, 2015, 1, 4, 2, 3, 4).ISO()

        self.assertTrue(
            s == "2015-02-07T01:04:02,003004",
            "datetime to string failed to reproduce expected result")

    def testCanHash(self):
        TEST_MESSAGE("Testing hashing of dates...")

        start_date = Date(1, Jan, 2020)
        nb_tests = 500

        hasher = hash

        # Check hash values
        for i in range(nb_tests):
            for j in range(nb_tests):
                lhs = start_date + i
                rhs = start_date + j

                self.assertFalse(lhs == rhs and hasher(lhs) != hasher(rhs))
                self.assertFalse(lhs != rhs and hasher(lhs) == hasher(rhs))

                # Check if can be used as unordered_set key
        s = dict()
        s[start_date] = 1.0

        self.assertTrue(start_date in s.keys())
