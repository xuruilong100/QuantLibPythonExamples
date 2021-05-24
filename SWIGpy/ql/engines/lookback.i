#ifndef ql_engines_lookback_i
#define ql_engines_lookback_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticContinuousFloatingLookbackEngine;
using QuantLib::AnalyticContinuousFixedLookbackEngine;
using QuantLib::AnalyticContinuousPartialFloatingLookbackEngine;
using QuantLib::AnalyticContinuousPartialFixedLookbackEngine;
%}

%shared_ptr(AnalyticContinuousFloatingLookbackEngine)
class AnalyticContinuousFloatingLookbackEngine : public PricingEngine {
  public:
    AnalyticContinuousFloatingLookbackEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(AnalyticContinuousFixedLookbackEngine)
class AnalyticContinuousFixedLookbackEngine : public PricingEngine {
  public:
    AnalyticContinuousFixedLookbackEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(AnalyticContinuousPartialFloatingLookbackEngine)
class AnalyticContinuousPartialFloatingLookbackEngine : public PricingEngine {
  public:
    AnalyticContinuousPartialFloatingLookbackEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(AnalyticContinuousPartialFixedLookbackEngine)
class AnalyticContinuousPartialFixedLookbackEngine : public PricingEngine {
  public:
    AnalyticContinuousPartialFixedLookbackEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

#endif
