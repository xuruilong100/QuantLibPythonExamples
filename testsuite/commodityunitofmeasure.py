import unittest
from utilities import *
from QuantLib import *


class CommodityUnitOfMeasureTest(unittest.TestCase):

    def testDirect(self):
        TEST_MESSAGE("Testing direct commodity unit of measure conversions...")

        UOMManager = UnitOfMeasureConversionManager.instance()

        # MB to BBL
        actual = UnitOfMeasureConversion(
            NullCommodityType(), MBUnitOfMeasure(),
            BarrelUnitOfMeasure(), 1000).convert(
            Quantity(NullCommodityType(), MBUnitOfMeasure(), 1000))
        calc = UOMManager.lookup(
            NullCommodityType(), BarrelUnitOfMeasure(),
            MBUnitOfMeasure(), UnitOfMeasureConversion.Direct).convert(
            Quantity(NullCommodityType(), MBUnitOfMeasure(), 1000))

        self.assertFalse(not close(calc, actual))

        # BBL to Gallon
        actual = UnitOfMeasureConversion(
            NullCommodityType(), BarrelUnitOfMeasure(),
            GallonUnitOfMeasure(), 42).convert(
            Quantity(NullCommodityType(), GallonUnitOfMeasure(), 1000))
        calc = UOMManager.lookup(
            NullCommodityType(), BarrelUnitOfMeasure(),
            GallonUnitOfMeasure(),
            UnitOfMeasureConversion.Direct).convert(
            Quantity(NullCommodityType(), GallonUnitOfMeasure(), 1000))

        self.assertFalse(not close(calc, actual))

        # BBL to Litre
        actual = UnitOfMeasureConversion(
            NullCommodityType(), BarrelUnitOfMeasure(),
            LitreUnitOfMeasure(), 158.987).convert(
            Quantity(NullCommodityType(), LitreUnitOfMeasure(), 1000))
        calc = UOMManager.lookup(
            NullCommodityType(), BarrelUnitOfMeasure(),
            LitreUnitOfMeasure(),
            UnitOfMeasureConversion.Direct).convert(
            Quantity(NullCommodityType(), LitreUnitOfMeasure(), 1000))

        self.assertFalse(not close(calc, actual))

        # BBL to KL
        actual = UnitOfMeasureConversion(
            NullCommodityType(), KilolitreUnitOfMeasure(),
            BarrelUnitOfMeasure(), 6.28981).convert(
            Quantity(NullCommodityType(), KilolitreUnitOfMeasure(), 1000))
        calc = UOMManager.lookup(
            NullCommodityType(), BarrelUnitOfMeasure(),
            KilolitreUnitOfMeasure(),
            UnitOfMeasureConversion.Direct).convert(
            Quantity(NullCommodityType(), KilolitreUnitOfMeasure(), 1000))

        self.assertFalse(not close(calc, actual))

        # MB to Gallon
        actual = UnitOfMeasureConversion(
            NullCommodityType(), GallonUnitOfMeasure(),
            MBUnitOfMeasure(), 42000).convert(
            Quantity(NullCommodityType(), MBUnitOfMeasure(), 1000))
        calc = UOMManager.lookup(
            NullCommodityType(), GallonUnitOfMeasure(),
            MBUnitOfMeasure(), UnitOfMeasureConversion.Direct).convert(
            Quantity(NullCommodityType(), MBUnitOfMeasure(), 1000))

        self.assertFalse(not close(calc, actual))

        # Gallon to Litre
        actual = UnitOfMeasureConversion(
            NullCommodityType(), LitreUnitOfMeasure(),
            GallonUnitOfMeasure(), 3.78541).convert(
            Quantity(NullCommodityType(), LitreUnitOfMeasure(), 1000))
        calc = UOMManager.lookup(
            NullCommodityType(), GallonUnitOfMeasure(),
            LitreUnitOfMeasure(),
            UnitOfMeasureConversion.Direct).convert(
            Quantity(NullCommodityType(), LitreUnitOfMeasure(), 1000))

        self.assertFalse(not close(calc, actual))
