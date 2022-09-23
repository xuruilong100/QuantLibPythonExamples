import unittest

from QuantLib import *

from utilities import *


class MoneyTest(unittest.TestCase):

    def testNone(self):
        TEST_MESSAGE(
            "Testing money arithmetic without conversions...")

        EUR = EURCurrency()

        m1 = Money(50000.0, EUR)
        m2 = Money(100000.0, EUR)
        m3 = Money(500000.0, EUR)

        MoneySettings.instance().conversionType = Money.NoConversion

        calculated = m1 * 3.0 + 2.5 * m2 - m3 / 5.0
        x = m1.value() * 3.0 + 2.5 * m2.value() - m3.value() / 5.0
        expected = Money(x, EUR)

        self.assertFalse(calculated != expected)

    def testBaseCurrency(self):
        TEST_MESSAGE(
            "Testing money arithmetic with conversion "
            "to base currency...")

        EUR = EURCurrency()
        GBP = GBPCurrency()
        USD = USDCurrency()

        m1 = Money(50000.0, GBP)
        m2 = Money(100000.0, EUR)
        m3 = Money(500000.0, USD)

        ExchangeRateManager.instance().clear()
        eur_usd = ExchangeRate(EUR, USD, 1.2042)
        eur_gbp = ExchangeRate(EUR, GBP, 0.6612)
        ExchangeRateManager.instance().add(eur_usd)
        ExchangeRateManager.instance().add(eur_gbp)

        MoneySettings.instance().conversionType = Money.BaseCurrencyConversion
        MoneySettings.instance().baseCurrency = EUR

        calculated = m1 * 3.0 + 2.5 * m2 - m3 / 5.0

        round = MoneySettings.instance().baseCurrency.rounding()
        x = round(m1.value() * 3.0 / eur_gbp.rate()) + \
            2.5 * m2.value() - \
            round(m3.value() / (5.0 * eur_usd.rate()))
        expected = Money(x, EUR)

        MoneySettings.instance().conversionType = Money.NoConversion

        self.assertFalse(calculated != expected)

    def testAutomated(self):
        TEST_MESSAGE(
            "Testing money arithmetic with automated conversion...")

        EUR = EURCurrency()
        GBP = GBPCurrency()
        USD = USDCurrency()

        m1 = Money(50000.0, GBP)
        m2 = Money(100000.0, EUR)
        m3 = Money(500000.0, USD)

        ExchangeRateManager.instance().clear()
        eur_usd = ExchangeRate(EUR, USD, 1.2042)
        eur_gbp = ExchangeRate(EUR, GBP, 0.6612)
        ExchangeRateManager.instance().add(eur_usd)
        ExchangeRateManager.instance().add(eur_gbp)

        money_settings = MoneySettings.instance()
        money_settings.conversionType = Money.AutomatedConversion

        calculated = (m1 * 3.0 + 2.5 * m2) - m3 / 5.0

        round = m1.currency().rounding()
        x = m1.value() * 3.0 + \
            round(2.5 * m2.value() * eur_gbp.rate()) - \
            round((m3.value() / 5.0) * eur_gbp.rate() / eur_usd.rate())
        expected = Money(x, GBP)

        money_settings.conversionType = Money.NoConversion

        self.assertFalse(calculated != expected)
