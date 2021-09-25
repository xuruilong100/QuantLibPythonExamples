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
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Handle<YieldTermStructure> foreignRiskFreeRate,
        Handle<BlackVolTermStructure> exchangeRateVolatility,
        Handle<Quote> correlation);
};

%shared_ptr(QuantoForwardEuropeanEngine)
class QuantoForwardEuropeanEngine : public PricingEngine {
  public:
    QuantoForwardEuropeanEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Handle<YieldTermStructure> foreignRiskFreeRate,
        Handle<BlackVolTermStructure> exchangeRateVolatility,
        Handle<Quote> correlation);
};

#endif
