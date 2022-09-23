import unittest

from QuantLib import *

from utilities import *


class LazyObjectTest(unittest.TestCase):

    def testDiscardingNotifications(self):
        TEST_MESSAGE(
            "Testing that lazy objects discard notifications after the first...")

        q = SimpleQuote(0.0)
        s = Stock(QuoteHandle(q))

        f = Flag()
        f.registerWith(s)

        s.NPV()
        q.setValue(1.0)
        self.assertFalse(not f.isUp())

        f.lower()
        q.setValue(2.0)
        self.assertFalse(f.isUp())

        f.lower()
        s.NPV()
        q.setValue(3.0)
        self.assertFalse(not f.isUp())

    def testForwardingNotifications(self):
        TEST_MESSAGE(
            "Testing that lazy objects forward all notifications when told...")

        q = SimpleQuote(0.0)
        s = Stock(QuoteHandle(q))

        s.alwaysForwardNotifications()

        f = Flag()
        f.registerWith(s)

        s.NPV()
        q.setValue(1.0)
        self.assertFalse(not f.isUp())

        f.lower()
        q.setValue(2.0)
        self.assertFalse(not f.isUp())
