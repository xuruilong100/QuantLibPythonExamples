import unittest
from testsuite.americanoption import AmericanOptionTest
from testsuite.amortizingbond import AmortizingBondTest
from testsuite.andreasenhugevolatilityinterpl import AndreasenHugeVolatilityInterplTest
from testsuite.array import ArrayTest
from testsuite.asianoptions import AsianOptionTest
from testsuite.autocovariances import AutocovariancesTest
from testsuite.barrieroption import BarrierOptionTest
from testsuite.basketoption import BasketOptionTest
from testsuite.batesmodel import BatesModelTest
from testsuite.binaryoption import BinaryOptionTest
from testsuite.blackdeltacalculator import BlackDeltaCalculatorTest
from testsuite.blackformula import BlackFormulaTest
from testsuite.brownianbridge import BrownianBridgeTest
from testsuite.businessdayconventions import BusinessDayConventionTest
from testsuite.calendars import CalendarTest
from testsuite.chooseroption import ChooserOptionTest
from testsuite.cliquetoption import CliquetOptionTest
from testsuite.commodityunitofmeasure import CommodityUnitOfMeasureTest
from testsuite.compoundoption import CompoundOptionTest
from testsuite.covariance import CovarianceTest
from testsuite.creditriskplus import CreditRiskPlusTest
from testsuite.currency import CurrencyTest
from testsuite.dates import DateTest
from testsuite.daycounters import DayCounterTest
from testsuite.digitaloption import DigitalOptionTest
from testsuite.distributions import DistributionTest
from testsuite.dividendoption import DividendOptionTest
from testsuite.doublebarrieroption import DoubleBarrierOptionTest
from testsuite.doublebinaryoption import DoubleBinaryOptionTest
from testsuite.europeanoption import EuropeanOptionTest
from testsuite.everestoption import EverestOptionTest
from testsuite.exchangerate import ExchangeRateTest
from testsuite.extendedtrees import ExtendedTreesTest
from testsuite.extensibleoptions import ExtensibleOptionsTest
from testsuite.fastfouriertransform import FastFourierTransformTest
from testsuite.fdcev import FdCevTest
from testsuite.fdheston import FdHestonTest
from testsuite.fdsabr import FdSabrTest
from testsuite.forwardoption import ForwardOptionTest
from testsuite.functions import FunctionsTest # warnings
from testsuite.garch import GARCHTest
from testsuite.gaussianquadratures import GaussianQuadraturesTest
from testsuite.gjrgarchmodel import GJRGARCHModelTest
from testsuite.hestonmodel import HestonModelTest
from testsuite.hestonslvmodel import HestonSLVModelTest
from testsuite.himalayaoption import HimalayaOptionTest
from testsuite.hybridhestonhullwhiteprocess import HybridHestonHullWhiteProcessTest
from testsuite.indexes import IndexTest
from testsuite.instruments import InstrumentTest
from testsuite.integrals import IntegralTest
from testsuite.interestrates import InterestRateTest
from testsuite.interpolations import InterpolationTest
from testsuite.jumpdiffusion import JumpDiffusionTest
from testsuite.lazyobject import LazyObjectTest
from testsuite.lookbackoption import LookbackOptionTest
from testsuite.lowdiscrepancysequences import LowDiscrepancyTest
from testsuite.margrabeoption import MargrabeOptionTest
from testsuite.matrices import MatricesTest
from testsuite.mclongstaffschwartzengine import MCLongstaffSchwartzEngineTest
from testsuite.mersennetwister import MersenneTwisterTest
from testsuite.money import MoneyTest
from testsuite.numericaldifferentiation import NumericalDifferentiationTest
from testsuite.pagodaoption import PagodaOptionTest
from testsuite.partialtimebarrieroption import PartialTimeBarrierOptionTest
from testsuite.pathgenerator import PathGeneratorTest
from testsuite.period import PeriodTest
from testsuite.quantooption import QuantoOptionTest
from testsuite.quotes import QuoteTest
from testsuite.riskneutraldensitycalculator import RiskNeutralDensityCalculatorTest
from testsuite.riskstats import RiskStatisticsTest
from testsuite.rngtraits import RngTraitsTest
from testsuite.rounding import RoundingTest
from testsuite.schedule import ScheduleTest
from testsuite.settings import SettingsTest
from testsuite.solvers import Solver1DTest
from testsuite.spreadoption import SpreadOptionTest
from testsuite.stats import StatisticsTest
from testsuite.swingoption import SwingOptionTest
from testsuite.termstructures import TermStructureTest
from testsuite.timegrid import TimeGridTest
from testsuite.timeseries import TimeSeriesTest
from testsuite.tqreigendecomposition import TqrEigenDecompositionTest
from testsuite.transformedgrid import TransformedGridTest
from testsuite.twoassetbarrieroption import TwoAssetBarrierOptionTest
from testsuite.twoassetcorrelationoption import TwoAssetCorrelationOptionTest
from testsuite.varianceoption import VarianceOptionTest
from testsuite.varianceswaps import VarianceSwapTest


if __name__ == '__main__':
    unittest.main()

'''
Ran 546 tests in 610.466s

OK (skipped=25)
'''
