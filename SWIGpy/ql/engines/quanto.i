#ifndef ql_engines_quanto_i
#define ql_engines_quanto_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::QuantoEngine;
typedef QuantoEngine<VanillaOption,AnalyticEuropeanEngine> QuantoEuropeanEngine;
typedef QuantoEngine<ForwardVanillaOption,AnalyticEuropeanEngine> QuantoForwardEuropeanEngine;
%}

%shared_ptr(QuantoEuropeanEngine)
class QuantoEuropeanEngine : public PricingEngine {
  public:
    QuantoEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        const Handle<YieldTermStructure>& foreignRiskFreeRate,
        const Handle<BlackVolTermStructure>& exchangeRateVolatility,
        const Handle<Quote>& correlation);
};

%shared_ptr(QuantoForwardEuropeanEngine)
class QuantoForwardEuropeanEngine : public PricingEngine {
  public:
    QuantoForwardEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        const Handle<YieldTermStructure>& foreignRiskFreeRate,
        const Handle<BlackVolTermStructure>& exchangeRateVolatility,
        const Handle<Quote>& correlation);
};

#endif
