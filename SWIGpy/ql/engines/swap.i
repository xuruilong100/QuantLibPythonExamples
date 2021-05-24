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
        const Handle<YieldTermStructure>& discountCurve,
        bool includeSettlementDateFlows,
        const Date& settlementDate = Date(),
        const Date& npvDate = Date());
    %extend {
        DiscountingSwapEngine(
            const Handle<YieldTermStructure>& discountCurve,
            const Date& settlementDate = Date(),
            const Date& npvDate = Date()) {
            return new DiscountingSwapEngine(
                discountCurve,
                boost::none,
                settlementDate,
                npvDate);
        }
    }
};

#endif
