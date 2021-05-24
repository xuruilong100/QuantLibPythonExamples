#ifndef ql_engines_cds_i
#define ql_engines_cds_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::MidPointCdsEngine;
using QuantLib::IntegralCdsEngine;
using QuantLib::IsdaCdsEngine;
using QuantLib::BlackCdsOptionEngine;
%}

%shared_ptr(MidPointCdsEngine)
class MidPointCdsEngine : public PricingEngine {
  public:
    MidPointCdsEngine(const Handle<DefaultProbabilityTermStructure>& probability,
                      Real recoveryRate,
                      const Handle<YieldTermStructure>& discountCurve);
};

%shared_ptr(IntegralCdsEngine)
class IntegralCdsEngine : public PricingEngine {
  public:
    IntegralCdsEngine(const Period &integrationStep,
                      const Handle<DefaultProbabilityTermStructure>& probability,
                      Real recoveryRate,
                      const Handle<YieldTermStructure>& discountCurve,
                      bool includeSettlementDateFlows = false);
};

%shared_ptr(IsdaCdsEngine)
class IsdaCdsEngine : public PricingEngine {
    %rename(NoFix) None;
  public:
    enum NumericalFix {None, Taylor};
    enum AccrualBias {HalfDayBias, NoBias};
    enum ForwardsInCouponPeriod {Flat, Piecewise};
    IsdaCdsEngine(
        const Handle<DefaultProbabilityTermStructure> &probability,
        Real recoveryRate,
        const Handle<YieldTermStructure> &discountCurve,
        bool includeSettlementDateFlows = false,
        const IsdaCdsEngine::NumericalFix numericalFix = IsdaCdsEngine::Taylor,
        const IsdaCdsEngine::AccrualBias accrualBias = IsdaCdsEngine::HalfDayBias,
        const IsdaCdsEngine::ForwardsInCouponPeriod forwardsInCouponPeriod = IsdaCdsEngine::Piecewise);
};

%shared_ptr(BlackCdsOptionEngine)
class BlackCdsOptionEngine : public PricingEngine {
  public:
    BlackCdsOptionEngine(
        const Handle<DefaultProbabilityTermStructure>&,
        Real recoveryRate,
        const Handle<YieldTermStructure>& termStructure,
        const Handle<Quote>& vol);
    Handle<YieldTermStructure> termStructure();
    Handle<Quote> volatility();
};

#endif
