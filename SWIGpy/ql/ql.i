// Undefine symbols that are also used in quantlib

%{
#ifdef barrier
#undef barrier
#endif
%}

%{
#include <ql/quantlib.hpp>

#if QL_HEX_VERSION < 0x01210000
    #error using an old version of QuantLib, please update
#endif

#ifdef BOOST_MSVC
#ifdef QL_ENABLE_THREAD_SAFE_OBSERVER_PATTERN
#define BOOST_LIB_NAME boost_thread
#include <boost/config/auto_link.hpp>
#undef BOOST_LIB_NAME
#define BOOST_LIB_NAME boost_system
#include <boost/config/auto_link.hpp>
#undef BOOST_LIB_NAME
#endif
#endif

// add here SWIG version check

#if defined(_MSC_VER)         // Microsoft Visual C++ 6.0
// disable Swig-dependent warnings

// 'identifier1' has C-linkage specified,
// but returns UDT 'identifier2' which is incompatible with C
#pragma warning(disable: 4190)

// 'int' : forcing value to bool 'true' or 'false' (performance warning)
#pragma warning(disable: 4800)

// debug info too long etc etc
#pragma warning(disable: 4786)
#endif
%}

#ifdef SWIGPYTHON
%{
#if PY_VERSION_HEX < 0x02010000
    #error Python version 2.1.0 or later is required
#endif
%}
#endif


%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/common.i
%include ../ql/types.i

%include ../ql/blackformula.i
%include ../ql/bondfunctions.i
%include ../ql/bootstraphelpers/all.i
%include ../ql/calendars.i
%include ../ql/calibratedmodels/HestonModel.i
%include ../ql/calibratedmodels/ShortRateModel.i
%include ../ql/calibratedmodels/hestonmodels/all.i
%include ../ql/calibratedmodels/others/all.i
%include ../ql/calibratedmodels/shortratemodels/all.i
%include ../ql/calibrationhelpers.i
%include ../ql/callability.i
%include ../ql/cashflows/CashFlows.i
%include ../ql/cashflows/Coupon.i
%include ../ql/cashflows/Dividend.i
%include ../ql/cashflows/FloatingRateCouponPricer.i
%include ../ql/cashflows/Leg.i
%include ../ql/cashflows/coupons/all.i
%include ../ql/cashflows/dividends/all.i
%include ../ql/cashflows/floatingratecouponpricers/all.i
%include ../ql/cashflows/others/all.i
%include ../ql/currencies.i
%include ../ql/date.i
%include ../ql/daycounters.i
%include ../ql/defaultprobabilityhelpers/all.i
%include ../ql/distributions.i
%include ../ql/engines/asian.i
%include ../ql/engines/barrier.i
%include ../ql/engines/basket.i
%include ../ql/engines/bond.i
%include ../ql/engines/capfloor.i
%include ../ql/engines/cds.i
%include ../ql/engines/dividend.i
%include ../ql/engines/forwardoptionargument.i
%include ../ql/engines/lookback.i
%include ../ql/engines/quanto.i
%include ../ql/engines/spread.i
%include ../ql/engines/swap.i
%include ../ql/engines/swaption.i
%include ../ql/engines/swing.i
%include ../ql/engines/vanilla.i
%include ../ql/engines/yoyinflationcapfloor.i
%include ../ql/exchangerates.i
%include ../ql/exercise.i
%include ../ql/fdms/Fdm1dMesher.i
%include ../ql/fdms/FdmBoundaryCondition.i
%include ../ql/fdms/FdmInnerValueCalculator.i
%include ../ql/fdms/FdmLinearOp.i
%include ../ql/fdms/FdmMesher.i
%include ../ql/fdms/FdmSolver.i
%include ../ql/fdms/Scheme.i
%include ../ql/fdms/StepCondition.i
%include ../ql/fdms/boundaryconditions/all.i
%include ../ql/fdms/fdm1dmeshers/all.i
%include ../ql/fdms/fdminnervaluecalculators/all.i
%include ../ql/fdms/fdmlinearops/all.i
%include ../ql/fdms/others/all.i
%include ../ql/fdms/stepconditions/all.i
%include ../ql/grid.i
%include ../ql/indexes/all.i
%include ../ql/inflation.i
%include ../ql/instruments/Bond.i
%include ../ql/instruments/CapFloor.i
%include ../ql/instruments/Forward.i
%include ../ql/instruments/Option.i
%include ../ql/instruments/Swap.i
%include ../ql/instruments/YoYInflationCapFloor.i
%include ../ql/instruments/bonds/all.i
%include ../ql/instruments/capfloors/all.i
%include ../ql/instruments/forwards/all.i
%include ../ql/instruments/options/MultiAssetOption.i
%include ../ql/instruments/options/OneAssetOption.i
%include ../ql/instruments/options/multiassetoptions/all.i
%include ../ql/instruments/options/oneassetoptions/all.i
%include ../ql/instruments/options/others/all.i
%include ../ql/instruments/others/all.i
%include ../ql/instruments/swaps/all.i
%include ../ql/instruments/yoyinflationcapfloors/all.i
%include ../ql/integrals.i
%include ../ql/interestrate.i
%include ../ql/interpolation.i
%include ../ql/linearalgebra.i
%include ../ql/money.i
%include ../ql/montecarlo.i
%include ../ql/ode.i
%include ../ql/operators.i
%include ../ql/optimizers.i
%include ../ql/parameter.i
%include ../ql/payoffs.i
%include ../ql/quotes/all.i
%include ../ql/randomnumbers.i
%include ../ql/ratehelpers/all.i
%include ../ql/riskneutraldensitycalculator.i
%include ../ql/rounding.i
%include ../ql/sampledcurve.i
%include ../ql/scheduler.i
%include ../ql/settings.i
%include ../ql/slv.i
%include ../ql/smilesections/all.i
%include ../ql/solvers.i
%include ../ql/statistics.i
%include ../ql/stochasticprocesses/all.i
%include ../ql/termstructureconsistentmodels/all.i
%include ../ql/termstructures/DefaultProbabilityTermStructure.i
%include ../ql/termstructures/InflationTermStructure.i
%include ../ql/termstructures/VolatilityTermStructure.i
%include ../ql/termstructures/YieldTermStructure.i
%include ../ql/termstructures/defaultprobabilitytermstructures/all.i
%include ../ql/termstructures/inflationtermstructures/all.i
%include ../ql/termstructures/volatilitytermstructures/all.i
%include ../ql/termstructures/yieldtermstructures/all.i
%include ../ql/termstructures/yieldtermstructures/fittingmethods.i
%include ../ql/testsuite.i
%include ../ql/timebasket.i
%include ../ql/timeseries.i
%include ../ql/vectors.i
%include ../ql/volatilities.i
%include ../ql/volatilitymodels.i
