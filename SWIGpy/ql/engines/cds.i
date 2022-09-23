#ifndef ql_engines_cds_i
#define ql_engines_cds_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%define QL_TYPECHECK_BOOL                        7220    %enddef

%typemap(in) boost::optional<bool> {
	if($input == Py_None)
		$1 = boost::none;
	else if ($input == Py_True)
		$1 = true;
	else
		$1 = false;
}

%typecheck (QL_TYPECHECK_BOOL) boost::optional<bool> {
    if (PyBool_Check($input) || Py_None == $input)
    	$1 = 1;
    else
    	$1 = 0;
}

%{
using QuantLib::MidPointCdsEngine;
using QuantLib::IntegralCdsEngine;
using QuantLib::IsdaCdsEngine;
using QuantLib::BlackCdsOptionEngine;
%}

%shared_ptr(MidPointCdsEngine)
class MidPointCdsEngine : public PricingEngine {
  public:
    MidPointCdsEngine(
        Handle<DefaultProbabilityTermStructure> probability,
        Real recoveryRate,
        Handle<YieldTermStructure> discountCurve,
        boost::optional<bool> includeSettlementDateFlows = boost::none);
};

%shared_ptr(IntegralCdsEngine)
class IntegralCdsEngine : public PricingEngine {
  public:
    IntegralCdsEngine(
        const Period& integrationStep,
        Handle<DefaultProbabilityTermStructure>,
        Real recoveryRate,
        Handle<YieldTermStructure> discountCurve,
        boost::optional<bool> includeSettlementDateFlows = boost::none);
};

%shared_ptr(IsdaCdsEngine)
class IsdaCdsEngine : public PricingEngine {
    %rename(NoFix) None;
  public:
    enum NumericalFix {None, Taylor};
    enum AccrualBias {HalfDayBias, NoBias};
    enum ForwardsInCouponPeriod {Flat, Piecewise};
    IsdaCdsEngine(
        Handle<DefaultProbabilityTermStructure> probability,
        Real recoveryRate,
        Handle<YieldTermStructure> discountCurve,
        boost::optional<bool> includeSettlementDateFlows = boost::none,
        NumericalFix numericalFix = Taylor,
        AccrualBias accrualBias = HalfDayBias,
        ForwardsInCouponPeriod forwardsInCouponPeriod = Piecewise);
        Handle<YieldTermStructure> isdaRateCurve() const;
        Handle<DefaultProbabilityTermStructure> isdaCreditCurve() const;
};

%shared_ptr(BlackCdsOptionEngine)
class BlackCdsOptionEngine : public PricingEngine {
  public:
    BlackCdsOptionEngine(
        Handle<DefaultProbabilityTermStructure>,
        Real recoveryRate,
        Handle<YieldTermStructure> termStructure,
        Handle<Quote> vol);
    Handle<YieldTermStructure> termStructure();
    Handle<Quote> volatility();
};

#endif
