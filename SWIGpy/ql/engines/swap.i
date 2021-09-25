#ifndef ql_engines_swap_i
#define ql_engines_swap_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::DiscountingSwapEngine;
%}

%shared_ptr(DiscountingSwapEngine)
class DiscountingSwapEngine : public PricingEngine {
  public:
    DiscountingSwapEngine(
        Handle<YieldTermStructure> discountCurve = Handle<YieldTermStructure>(),
        const boost::optional<bool>& includeSettlementDateFlows = boost::none,
        Date settlementDate = Date(),
        Date npvDate = Date());
      Handle<YieldTermStructure> discountCurve() const;
};

#endif
