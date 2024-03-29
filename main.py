'''
Testing them one by one is recommended
'''
import unittest
# A
from testsuite.americanoption import AmericanOptionTest
from testsuite.amortizingbond import AmortizingBondTest
from testsuite.andreasenhugevolatilityinterpl import AndreasenHugeVolatilityInterplTest
from testsuite.arrays import ArrayTest
from testsuite.asianoptions import AsianOptionTest
from testsuite.assetswap import AssetSwapTest
from testsuite.autocovariances import AutocovariancesTest
# B
from testsuite.barrieroption import BarrierOptionTest
from testsuite.basismodels import BasismodelsTest
from testsuite.basisswapratehelpers import BasisSwapRateHelpersTest
from testsuite.basketoption import BasketOptionTest
from testsuite.batesmodel import BatesModelTest
from testsuite.bermudanswaption import BermudanSwaptionTest
from testsuite.binaryoption import BinaryOptionTest
from testsuite.blackdeltacalculator import BlackDeltaCalculatorTest
from testsuite.blackformula import BlackFormulaTest
from testsuite.bondforward import BondForwardTest
from testsuite.bonds import BondTest
from testsuite.brownianbridge import BrownianBridgeTest
from testsuite.businessdayconventions import BusinessDayConventionTest
# C
from testsuite.calendars import CalendarTest
from testsuite.callablebonds import CallableBondTest
from testsuite.capfloor import CapFloorTest
from testsuite.capflooredcoupon import CapFlooredCouponTest
from testsuite.cashflows import CashFlowsTest
from testsuite.catbonds import CatBondTest
from testsuite.cdsoption import CdsOptionTest
from testsuite.chooseroption import ChooserOptionTest
from testsuite.cliquetoption import CliquetOptionTest
from testsuite.cms import CmsTest
from testsuite.cmsspread import CmsSpreadTest
from testsuite.commodityunitofmeasure import CommodityUnitOfMeasureTest
from testsuite.compoundoption import CompoundOptionTest
from testsuite.convertiblebonds import ConvertibleBondTest
from testsuite.covariance import CovarianceTest
from testsuite.creditdefaultswap import CreditDefaultSwapTest
from testsuite.creditriskplus import CreditRiskPlusTest
from testsuite.crosscurrencyratehelpers import CrossCurrencyRateHelpersTest
from testsuite.currency import CurrencyTest
from testsuite.curvestates import CurveStatesTest
# D
from testsuite.dates import DateTest
from testsuite.daycounters import DayCounterTest
from testsuite.defaultprobabilitycurves import DefaultProbabilityCurveTest
from testsuite.digitalcoupon import DigitalCouponTest
from testsuite.digitaloption import DigitalOptionTest
from testsuite.distributions import DistributionTest
from testsuite.dividendoption import DividendOptionTest
from testsuite.doublebarrieroption import DoubleBarrierOptionTest
from testsuite.doublebinaryoption import DoubleBinaryOptionTest
# E
from testsuite.europeanoption import EuropeanOptionTest
from testsuite.everestoption import EverestOptionTest
from testsuite.exchangerate import ExchangeRateTest
from testsuite.extendedtrees import ExtendedTreesTest
from testsuite.extensibleoptions import ExtensibleOptionsTest
# F
from testsuite.fastfouriertransform import FastFourierTransformTest
from testsuite.fdcev import FdCevTest
from testsuite.fdcir import FdCIRTest
from testsuite.fdheston import FdHestonTest
from testsuite.fdsabr import FdSabrTest
from testsuite.fittedbonddiscountcurve import FittedBondDiscountCurveTest
from testsuite.forwardoption import ForwardOptionTest
from testsuite.functions import FunctionsTest  # warnings
# G
from testsuite.garch import GARCHTest
from testsuite.gaussianquadratures import GaussianQuadraturesTest
from testsuite.gjrgarchmodel import GJRGARCHModelTest
from testsuite.gsr import GsrTest
# H
from testsuite.hestonmodel import HestonModelTest
from testsuite.hestonslvmodel import HestonSLVModelTest
from testsuite.himalayaoption import HimalayaOptionTest
from testsuite.hybridhestonhullwhiteprocess import HybridHestonHullWhiteProcessTest
# I
from testsuite.indexes import IndexTest
from testsuite.inflation import InflationTest
from testsuite.inflationcapfloor import InflationCapFloorTest
from testsuite.inflationcapflooredcoupon import InflationCapFlooredCouponTest
from testsuite.inflationcpibond import InflationCPIBondTest
from testsuite.inflationcpicapfloor import InflationCPICapFloorTest
from testsuite.inflationcpiswap import CPISwapTest
from testsuite.inflationvolatility import InflationVolTest
from testsuite.inflationzciisinterpolation import InflationZCIISInterpolationTest
from testsuite.instruments import InstrumentTest
from testsuite.integrals import IntegralTest
from testsuite.interestrates import InterestRateTest
from testsuite.interpolations import InterpolationTest
# J
from testsuite.jumpdiffusion import JumpDiffusionTest
# L
from testsuite.lazyobject import LazyObjectTest
from testsuite.libormarketmodel import LiborMarketModelTest
from testsuite.libormarketmodelprocess import LiborMarketModelProcessTest
from testsuite.lookbackoption import LookbackOptionTest
from testsuite.lowdiscrepancysequences import LowDiscrepancyTest
# M
from testsuite.margrabeoption import MargrabeOptionTest
from testsuite.marketmodel import MarketModelTest
from testsuite.marketmodel_cms import MarketModelCmsTest
from testsuite.marketmodel_smm import MarketModelSmmTest
from testsuite.marketmodel_smmcapletalphacalibration import MarketModelSmmCapletAlphaCalibrationTest
from testsuite.marketmodel_smmcapletcalibration import MarketModelSmmCapletCalibrationTest
from testsuite.marketmodel_smmcaplethomocalibration import MarketModelSmmCapletHomoCalibrationTest
from testsuite.matrices import MatricesTest
from testsuite.mclongstaffschwartzengine import MCLongstaffSchwartzEngineTest
from testsuite.mersennetwister import MersenneTwisterTest
from testsuite.money import MoneyTest
# N
from testsuite.noarbsabr import NoArbSabrTest
from testsuite.normalclvmodel import NormalCLVModelTest
from testsuite.numericaldifferentiation import NumericalDifferentiationTest
# O
from testsuite.operators import OperatorTest
from testsuite.optimizers import OptimizersTest
from testsuite.optionletstripper import OptionletStripperTest
from testsuite.overnightindexedcoupon import OvernightIndexedCouponTest
from testsuite.overnightindexedswap import OvernightIndexedSwapTest
# P
from testsuite.pagodaoption import PagodaOptionTest
from testsuite.partialtimebarrieroption import PartialTimeBarrierOptionTest
from testsuite.pathgenerator import PathGeneratorTest
from testsuite.period import PeriodTest
from testsuite.piecewiseyieldcurve import PiecewiseYieldCurveTest
from testsuite.piecewisezerospreadedtermstructure import PiecewiseZeroSpreadedTermStructureTest
# Q
from testsuite.quantooption import QuantoOptionTest
from testsuite.quotes import QuoteTest
# R
from testsuite.rangeaccrual import RangeAccrualTest
from testsuite.riskneutraldensitycalculator import RiskNeutralDensityCalculatorTest
from testsuite.riskstats import RiskStatisticsTest
from testsuite.rngtraits import RngTraitsTest
from testsuite.rounding import RoundingTest
# S
from testsuite.sampledcurve import SampledCurveTest
from testsuite.schedule import ScheduleTest
from testsuite.settings import SettingsTest
from testsuite.shortratemodels import ShortRateModelTest
from testsuite.sofrfutures import SofrFuturesTest
from testsuite.solvers import Solver1DTest
from testsuite.spreadoption import SpreadOptionTest
from testsuite.squarerootclvmodel import SquareRootCLVModelTest
from testsuite.stats import StatisticsTest
from testsuite.subperiodcoupons import SubPeriodsCouponTest
from testsuite.svivolatility import SviVolatilityTest
from testsuite.swap import SwapTest
from testsuite.swapforwardmappings import SwapForwardMappingsTest
from testsuite.swaption import SwaptionTest
from testsuite.swaptionvolatilitycube import SwaptionVolatilityCubeTest
from testsuite.swaptionvolatilitymatrix import SwaptionVolatilityMatrixTest
from testsuite.swingoption import SwingOptionTest
# T
from testsuite.termstructures import TermStructureTest
from testsuite.timegrid import TimeGridTest
from testsuite.timeseries import TimeSeriesTest
from testsuite.tqreigendecomposition import TqrEigenDecompositionTest
from testsuite.transformedgrid import TransformedGridTest
from testsuite.twoassetbarrieroption import TwoAssetBarrierOptionTest
from testsuite.twoassetcorrelationoption import TwoAssetCorrelationOptionTest
# U
from testsuite.ultimateforwardtermstructure import UltimateForwardTermStructureTest
# V
from testsuite.variancegamma import VarianceGammaTest
from testsuite.varianceoption import VarianceOptionTest
from testsuite.varianceswaps import VarianceSwapTest
from testsuite.volatilitymodels import VolatilityModelsTest
from testsuite.vpp import VPPTest
# Z
from testsuite.zabr import ZabrTest
from testsuite.zerocouponswap import ZeroCouponSwapTest

if __name__ == '__main__':
    unittest.main()

'''
Ran 876 tests in 896.654s

OK (skipped=40)
'''
