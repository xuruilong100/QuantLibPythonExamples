#ifndef ql_engines_swap_i
#define ql_engines_swap_i

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
using QuantLib::DiscountingSwapEngine;
using QuantLib::TreeVanillaSwapEngine;
%}

%shared_ptr(DiscountingSwapEngine)
class DiscountingSwapEngine : public PricingEngine {
  public:
    DiscountingSwapEngine(
        Handle<YieldTermStructure> discountCurve = Handle<YieldTermStructure>(),
        boost::optional<bool> includeSettlementDateFlows = boost::none,
        Date settlementDate = Date(),
        Date npvDate = Date());
      Handle<YieldTermStructure> discountCurve() const;
};

%shared_ptr(TreeVanillaSwapEngine)
class TreeVanillaSwapEngine : public PricingEngine {
  public:
    TreeVanillaSwapEngine(
        const ext::shared_ptr<ShortRateModel>&,
        Size timeSteps,
        Handle<YieldTermStructure> termStructure = Handle<YieldTermStructure>());
    TreeVanillaSwapEngine(
        const ext::shared_ptr<ShortRateModel>&,
        const TimeGrid& timeGrid,
        Handle<YieldTermStructure> termStructure = Handle<YieldTermStructure>());
};

#endif
