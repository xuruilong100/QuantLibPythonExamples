import unittest

from QuantLib import *

from utilities import *


class ExchangeRateTest(unittest.TestCase):

    def testDirect(self):
        TEST_MESSAGE(
            "Testing direct exchange rates...")

        EUR = EURCurrency()
        USD = USDCurrency()

        eur_usd = ExchangeRate(EUR, USD, 1.2042)

        m1 = 50000.0 * EUR
        m2 = 100000.0 * USD

        MoneySettings.instance().conversionType = Money.NoConversion

        calculated = eur_usd.exchange(m1)
        expected = Money(m1.value() * eur_usd.rate(), USD)

        self.assertFalse(not close(calculated, expected))

        calculated = eur_usd.exchange(m2)
        expected = Money(m2.value() / eur_usd.rate(), EUR)

        self.assertFalse(not close(calculated, expected))

    def testDerived(self):
        TEST_MESSAGE(
            "Testing derived exchange rates...")

        EUR = EURCurrency()
        USD = USDCurrency()
        GBP = GBPCurrency()

        eur_usd = ExchangeRate(EUR, USD, 1.2042)
        eur_gbp = ExchangeRate(EUR, GBP, 0.6612)

        derived = ExchangeRate.chain(eur_usd, eur_gbp)

        m1 = 50000.0 * GBP
        m2 = 100000.0 * USD

        MoneySettings.instance().conversionType = Money.NoConversion

        calculated = derived.exchange(m1)
        expected = Money(m1.value() * eur_usd.rate() / eur_gbp.rate(), USD)

        self.assertFalse(not close(calculated, expected))

        calculated = derived.exchange(m2)
        expected = Money(m2.value() * eur_gbp.rate() / eur_usd.rate(), GBP)

        self.assertFalse(not close(calculated, expected))

    def testDirectLookup(self):
        TEST_MESSAGE(
            "Testing lookup of direct exchange rates...")

        rateManager = ExchangeRateManager.instance()
        rateManager.clear()

        EUR = EURCurrency()
        USD = USDCurrency()

        eur_usd1 = ExchangeRate(EUR, USD, 1.1983)
        eur_usd2 = ExchangeRate(USD, EUR, 1.0 / 1.2042)
        rateManager.add(eur_usd1, Date(4, August, 2004))
        rateManager.add(eur_usd2, Date(5, August, 2004))

        m1 = 50000.0 * EUR
        m2 = 100000.0 * USD

        MoneySettings.instance().conversionType = Money.NoConversion

        eur_usd = rateManager.lookup(
            EUR, USD,
            Date(4, August, 2004),
            ExchangeRate.Direct)
        calculated = eur_usd.exchange(m1)
        expected = Money(m1.value() * eur_usd1.rate(), USD)

        self.assertFalse(not close(calculated, expected))

        eur_usd = rateManager.lookup(
            EUR, USD,
            Date(5, August, 2004),
            ExchangeRate.Direct)
        calculated = eur_usd.exchange(m1)
        expected = Money(m1.value() / eur_usd2.rate(), USD)

        self.assertFalse(not close(calculated, expected))

        usd_eur = rateManager.lookup(
            USD, EUR,
            Date(4, August, 2004),
            ExchangeRate.Direct)

        calculated = usd_eur.exchange(m2)
        expected = Money(m2.value() / eur_usd1.rate(), EUR)

        self.assertFalse(not close(calculated, expected))

        usd_eur = rateManager.lookup(
            USD, EUR,
            Date(5, August, 2004),
            ExchangeRate.Direct)

        calculated = usd_eur.exchange(m2)
        expected = Money(m2.value() * eur_usd2.rate(), EUR)

        self.assertFalse(not close(calculated, expected))

    def testTriangulatedLookup(self):
        TEST_MESSAGE(
            "Testing lookup of triangulated exchange rates...")

        rateManager = ExchangeRateManager.instance()
        rateManager.clear()

        EUR = EURCurrency()
        USD = USDCurrency()
        ITL = ITLCurrency()

        eur_usd1 = ExchangeRate(EUR, USD, 1.1983)
        eur_usd2 = ExchangeRate(EUR, USD, 1.2042)
        rateManager.add(eur_usd1, Date(4, August, 2004))
        rateManager.add(eur_usd2, Date(5, August, 2004))

        m1 = 50000000.0 * ITL
        m2 = 100000.0 * USD

        MoneySettings.instance().conversionType = Money.NoConversion

        itl_usd = rateManager.lookup(ITL, USD, Date(4, August, 2004))
        calculated = itl_usd.exchange(m1)
        expected = Money(m1.value() * eur_usd1.rate() / 1936.27, USD)

        self.assertFalse(not close(calculated, expected))

        itl_usd = rateManager.lookup(ITL, USD,
                                     Date(5, August, 2004))
        calculated = itl_usd.exchange(m1)
        expected = Money(m1.value() * eur_usd2.rate() / 1936.27, USD)

        self.assertFalse(not close(calculated, expected))

        usd_itl = rateManager.lookup(USD, ITL, Date(4, August, 2004))

        calculated = usd_itl.exchange(m2)
        expected = Money(m2.value() * 1936.27 / eur_usd1.rate(), ITL)

        self.assertFalse(not close(calculated, expected))

        usd_itl = rateManager.lookup(
            USD, ITL,
            Date(5, August, 2004))

        calculated = usd_itl.exchange(m2)
        expected = Money(m2.value() * 1936.27 / eur_usd2.rate(), ITL)

        self.assertFalse(not close(calculated, expected))

    def testSmartLookup(self):
        TEST_MESSAGE(
            "Testing lookup of derived exchange rates...")

        EUR = EURCurrency()
        USD = USDCurrency()
        GBP = GBPCurrency()
        CHF = CHFCurrency()
        SEK = SEKCurrency()
        JPY = JPYCurrency()

        rateManager = ExchangeRateManager.instance()
        rateManager.clear()

        eur_usd1 = ExchangeRate(EUR, USD, 1.1983)
        eur_usd2 = ExchangeRate(USD, EUR, 1.0 / 1.2042)
        rateManager.add(eur_usd1, Date(4, August, 2004))
        rateManager.add(eur_usd2, Date(5, August, 2004))

        eur_gbp1 = ExchangeRate(GBP, EUR, 1.0 / 0.6596)
        eur_gbp2 = ExchangeRate(EUR, GBP, 0.6612)
        rateManager.add(eur_gbp1, Date(4, August, 2004))
        rateManager.add(eur_gbp2, Date(5, August, 2004))

        usd_chf1 = ExchangeRate(USD, CHF, 1.2847)
        usd_chf2 = ExchangeRate(CHF, USD, 1.0 / 1.2774)
        rateManager.add(usd_chf1, Date(4, August, 2004))
        rateManager.add(usd_chf2, Date(5, August, 2004))

        chf_sek1 = ExchangeRate(SEK, CHF, 0.1674)
        chf_sek2 = ExchangeRate(CHF, SEK, 1.0 / 0.1677)
        rateManager.add(chf_sek1, Date(4, August, 2004))
        rateManager.add(chf_sek2, Date(5, August, 2004))

        jpy_sek1 = ExchangeRate(SEK, JPY, 14.5450)
        jpy_sek2 = ExchangeRate(JPY, SEK, 1.0 / 14.6110)
        rateManager.add(jpy_sek1, Date(4, August, 2004))
        rateManager.add(jpy_sek2, Date(5, August, 2004))

        m1 = 100000.0 * USD
        m2 = 100000.0 * EUR
        m3 = 100000.0 * GBP
        m4 = 100000.0 * CHF
        m5 = 100000.0 * SEK
        m6 = 100000.0 * JPY

        MoneySettings.instance().conversionType = Money.NoConversion

        usd_sek = rateManager.lookup(USD, SEK, Date(4, August, 2004))
        calculated = usd_sek.exchange(m1)
        expected = Money(m1.value() * usd_chf1.rate() / chf_sek1.rate(), SEK)

        self.assertFalse(not close(calculated, expected))

        usd_sek = rateManager.lookup(SEK, USD, Date(5, August, 2004))
        calculated = usd_sek.exchange(m5)
        expected = Money(m5.value() * usd_chf2.rate() / chf_sek2.rate(), USD)

        self.assertFalse(not close(calculated, expected))

        eur_sek = rateManager.lookup(EUR, SEK, Date(4, August, 2004))
        calculated = eur_sek.exchange(m2)
        expected = Money(
            m2.value() * eur_usd1.rate() * usd_chf1.rate() / chf_sek1.rate(),
            SEK)

        self.assertFalse(not close(calculated, expected))

        eur_sek = rateManager.lookup(SEK, EUR, Date(5, August, 2004))
        calculated = eur_sek.exchange(m5)
        expected = Money(
            m5.value() * eur_usd2.rate() * usd_chf2.rate() / chf_sek2.rate(),
            EUR)

        self.assertFalse(not close(calculated, expected))

        eur_jpy = rateManager.lookup(EUR, JPY, Date(4, August, 2004))
        calculated = eur_jpy.exchange(m2)
        expected = Money(m2.value() * eur_usd1.rate() * usd_chf1.rate() * jpy_sek1.rate() / chf_sek1.rate(), JPY)

        self.assertFalse(not close(calculated, expected))

        eur_jpy = rateManager.lookup(JPY, EUR, Date(5, August, 2004))
        calculated = eur_jpy.exchange(m6)
        expected = Money(
            m6.value() * jpy_sek2.rate() * eur_usd2.rate() * usd_chf2.rate() / chf_sek2.rate(),
            EUR)

        self.assertFalse(not close(calculated, expected))

        gbp_jpy = rateManager.lookup(GBP, JPY, Date(4, August, 2004))
        calculated = gbp_jpy.exchange(m3)
        expected = Money(
            m3.value() * eur_gbp1.rate() * eur_usd1.rate() * usd_chf1.rate() * jpy_sek1.rate() / chf_sek1.rate(),
            JPY)

        self.assertFalse(not close(calculated, expected))

        gbp_jpy = rateManager.lookup(JPY, GBP, Date(5, August, 2004))
        calculated = gbp_jpy.exchange(m6)
        expected = Money(
            m6.value() * jpy_sek2.rate() * eur_usd2.rate() * usd_chf2.rate() * eur_gbp2.rate() / chf_sek2.rate(),
            GBP)

        self.assertFalse(not close(calculated, expected))
