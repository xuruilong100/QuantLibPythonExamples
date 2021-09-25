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
    MidPointCdsEngine(
        Handle<DefaultProbabilityTermStructure> probability,
        Real recoveryRate,
        Handle<YieldTermStructure> discountCurve,
        const boost::optional<bool>& includeSettlementDateFlows = boost::none);
};

%shared_ptr(IntegralCdsEngine)
class IntegralCdsEngine : public PricingEngine {
  public:
    IntegralCdsEngine(const Period& integrationStep,
                      Handle<DefaultProbabilityTermStructure>,
                      Real recoveryRate,
                      Handle<YieldTermStructure> discountCurve,
                      const boost::optional<bool>& includeSettlementDateFlows = boost::none);
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
        const boost::optional<bool> &includeSettlementDateFlows=boost::none,
        NumericalFix numericalFix=Taylor,
        AccrualBias accrualBias=HalfDayBias,
        ForwardsInCouponPeriod forwardsInCouponPeriod=Piecewise);
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
