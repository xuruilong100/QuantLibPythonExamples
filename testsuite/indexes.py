import unittest

from QuantLib import *

from utilities import *


class IndexTest(unittest.TestCase):

    def testFixingObservability(self):
        TEST_MESSAGE(
            "Testing observability of index fixings...")

        i1 = Euribor6M()
        i2 = BMAIndex()

        f1 = Flag()
        f1.registerWith(i1)
        f1.lower()

        f2 = Flag()
        f2.registerWith(i2)
        f2.lower()

        today = knownGoodDefault

        euribor = Euribor6M()

        d1 = today
        while not euribor.isValidFixingDate(d1):
            d1 += Period(1, Days)

        euribor.addFixing(d1, -0.003)
        self.assertFalse(not f1.isUp())

        bma = BMAIndex()

        d2 = today
        while not bma.isValidFixingDate(d2):
            d2 += Period(1, Days)

        bma.addFixing(d2, 0.01)
        self.assertFalse(not f2.isUp())

    def testFixingHasHistoricalFixing(self):
        TEST_MESSAGE(
            "Testing if index has historical fixings...")

        def testCase(indexName,
                     expected,
                     testResult):
            self.assertFalse(expected != testResult)

        fixingFound = true
        fixingNotFound = false

        euribor3M = Euribor3M()
        euribor6M = Euribor6M()
        euribor6M_a = Euribor6M()

        today = Settings.instance().evaluationDate
        while (not euribor6M.isValidFixingDate(today)):
            today -= 1

        IndexManager.instance().clearHistories()

        euribor6M.addFixing(today, 0.01)

        name = euribor3M.name()
        testCase(name, fixingNotFound, euribor3M.hasHistoricalFixing(today))
        testCase(name, fixingNotFound, IndexManager.instance().hasHistoricalFixing(name, today))

        name = euribor6M.name()
        testCase(name, fixingFound, euribor6M.hasHistoricalFixing(today))
        testCase(name, fixingFound, euribor6M_a.hasHistoricalFixing(today))
        testCase(name, fixingFound, IndexManager.instance().hasHistoricalFixing(name, today))

        IndexManager.instance().clearHistories()

        name = euribor3M.name()
        testCase(name, fixingNotFound, euribor3M.hasHistoricalFixing(today))
        testCase(name, fixingNotFound, IndexManager.instance().hasHistoricalFixing(name, today))

        name = euribor6M.name()
        testCase(name, fixingNotFound, euribor6M.hasHistoricalFixing(today))
        testCase(name, fixingNotFound, euribor6M_a.hasHistoricalFixing(today))
        testCase(name, fixingNotFound, IndexManager.instance().hasHistoricalFixing(name, today))
