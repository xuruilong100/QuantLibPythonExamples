import unittest

from QuantLib import *

from utilities import *


class CurrencyTest(unittest.TestCase):

    def testBespokeConstructor(self):
        TEST_MESSAGE(
            "Testing bespoke currency constructor...")

        name = "Some Currency"
        code = "CCY"
        symbol = "#"

        customCcy = Currency(
            name, code, 100, symbol, "", 100, Rounding(), "")

        self.assertFalse(customCcy.empty())
        self.assertFalse(customCcy.name() != name)
        self.assertFalse(customCcy.code() != code)
        self.assertFalse(customCcy.symbol() != symbol)
