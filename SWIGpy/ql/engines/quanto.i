#ifndef ql_engines_quanto_i
#define ql_engines_quanto_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::QuantoEngine;
%}

%shared_ptr(QuantoEngine<VanillaOption, AnalyticEuropeanEngine>)
%shared_ptr(QuantoEngine<ForwardVanillaOption, ForwardVanillaEngine<AnalyticEuropeanEngine>>)
%shared_ptr(QuantoEngine<ForwardVanillaOption, ForwardPerformanceVanillaEngine<AnalyticEuropeanEngine>>)
%shared_ptr(QuantoEngine<BarrierOption, AnalyticBarrierEngine>)
%shared_ptr(QuantoEngine<DoubleBarrierOption, AnalyticDoubleBarrierEngine>)
template <class Instr, class Engine>
class QuantoEngine : public PricingEngine {
  public:
    QuantoEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess>,
        Handle<YieldTermStructure> foreignRiskFreeRate,
        Handle<BlackVolTermStructure> exchangeRateVolatility,
        Handle<Quote> correlation);
};

%template(QuantoVanillaEngine) QuantoEngine<VanillaOption, AnalyticEuropeanEngine>;
%template(QuantoForwardVanillaEngine) QuantoEngine<ForwardVanillaOption, ForwardVanillaEngine<AnalyticEuropeanEngine>>;
%template(QuantoForwardVanillaPerformanceEngine) QuantoEngine<ForwardVanillaOption, ForwardPerformanceVanillaEngine<AnalyticEuropeanEngine>>;
%template(QuantoBarrierEngine) QuantoEngine<BarrierOption, AnalyticBarrierEngine>;
%template(QuantoDoubleBarrierEngine) QuantoEngine<DoubleBarrierOption, AnalyticDoubleBarrierEngine>;

#endif
