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
using QuantLib::MCLookbackEngine;
using QuantLib::MakeMCLookbackEngine;
%}

%shared_ptr(AnalyticContinuousFloatingLookbackEngine)
class AnalyticContinuousFloatingLookbackEngine : public PricingEngine {
  public:
    AnalyticContinuousFloatingLookbackEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticContinuousFixedLookbackEngine)
class AnalyticContinuousFixedLookbackEngine : public PricingEngine {
  public:
    AnalyticContinuousFixedLookbackEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticContinuousPartialFloatingLookbackEngine)
class AnalyticContinuousPartialFloatingLookbackEngine : public PricingEngine {
  public:
    AnalyticContinuousPartialFloatingLookbackEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticContinuousPartialFixedLookbackEngine)
class AnalyticContinuousPartialFixedLookbackEngine : public PricingEngine {
  public:
    AnalyticContinuousPartialFixedLookbackEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(MCLookbackEngine<ContinuousFixedLookbackOption, PseudoRandom>)
%shared_ptr(MCLookbackEngine<ContinuousFloatingLookbackOption, PseudoRandom>)
%shared_ptr(MCLookbackEngine<ContinuousPartialFixedLookbackOption, PseudoRandom>)
%shared_ptr(MCLookbackEngine<ContinuousPartialFloatingLookbackOption, PseudoRandom>)
%shared_ptr(MCLookbackEngine<ContinuousFixedLookbackOption, LowDiscrepancy>)
%shared_ptr(MCLookbackEngine<ContinuousFloatingLookbackOption, LowDiscrepancy>)
%shared_ptr(MCLookbackEngine<ContinuousPartialFixedLookbackOption, LowDiscrepancy>)
%shared_ptr(MCLookbackEngine<ContinuousPartialFloatingLookbackOption, LowDiscrepancy>)
template <class I, class RNG>
class MCLookbackEngine : public PricingEngine {
  public:
    MCLookbackEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antithetic,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRFixedLookbackEngine) MCLookbackEngine<ContinuousFixedLookbackOption, PseudoRandom>;
%template(MCPRFloatingLookbackEngine) MCLookbackEngine<ContinuousFloatingLookbackOption, PseudoRandom>;
%template(MCPRPartialFixedLookbackEngine) MCLookbackEngine<ContinuousPartialFixedLookbackOption, PseudoRandom>;
%template(MCPRPartialFloatingLookbackEngine) MCLookbackEngine<ContinuousPartialFloatingLookbackOption, PseudoRandom>;
%template(MCLDFixedLookbackEngine) MCLookbackEngine<ContinuousFixedLookbackOption, LowDiscrepancy>;
%template(MCLDFloatingLookbackEngine) MCLookbackEngine<ContinuousFloatingLookbackOption, LowDiscrepancy>;
%template(MCLDPartialFixedLookbackEngine) MCLookbackEngine<ContinuousPartialFixedLookbackOption, LowDiscrepancy>;
%template(MCLDPartialFloatingLookbackEngine) MCLookbackEngine<ContinuousPartialFloatingLookbackOption, LowDiscrepancy>;

%shared_ptr(MakeMCLookbackEngine<ContinuousFixedLookbackOption, PseudoRandom>)
%shared_ptr(MakeMCLookbackEngine<ContinuousFloatingLookbackOption, PseudoRandom>)
%shared_ptr(MakeMCLookbackEngine<ContinuousPartialFixedLookbackOption, PseudoRandom>)
%shared_ptr(MakeMCLookbackEngine<ContinuousPartialFloatingLookbackOption, PseudoRandom>)
%shared_ptr(MakeMCLookbackEngine<ContinuousFixedLookbackOption, LowDiscrepancy>)
%shared_ptr(MakeMCLookbackEngine<ContinuousFloatingLookbackOption, LowDiscrepancy>)
%shared_ptr(MakeMCLookbackEngine<ContinuousPartialFixedLookbackOption, LowDiscrepancy>)
%shared_ptr(MakeMCLookbackEngine<ContinuousPartialFloatingLookbackOption, LowDiscrepancy>)
template <class I, class RNG>
class MakeMCLookbackEngine {
  public:
    explicit MakeMCLookbackEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);
    // named parameters
    MakeMCLookbackEngine& withSteps(Size steps);
    MakeMCLookbackEngine& withStepsPerYear(Size steps);
    MakeMCLookbackEngine& withBrownianBridge(bool b = true);
    MakeMCLookbackEngine& withAntitheticVariate(bool b = true);
    MakeMCLookbackEngine& withSamples(Size samples);
    MakeMCLookbackEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCLookbackEngine& withMaxSamples(Size samples);
    MakeMCLookbackEngine& withSeed(BigNatural seed);
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(*self);
        }
    }
};

%template(MakeMCPRFixedLookbackEngine) MakeMCLookbackEngine<ContinuousFixedLookbackOption, PseudoRandom>;
%template(MakeMCPRFloatingLookbackEngine) MakeMCLookbackEngine<ContinuousFloatingLookbackOption, PseudoRandom>;
%template(MakeMCPRPartialFixedLookbackEngine) MakeMCLookbackEngine<ContinuousPartialFixedLookbackOption, PseudoRandom>;
%template(MakeMCPRPartialFloatingLookbackEngine) MakeMCLookbackEngine<ContinuousPartialFloatingLookbackOption, PseudoRandom>;
%template(MakeMCLDFixedLookbackEngine) MakeMCLookbackEngine<ContinuousFixedLookbackOption, LowDiscrepancy>;
%template(MakeMCLDFloatingLookbackEngine) MakeMCLookbackEngine<ContinuousFloatingLookbackOption, LowDiscrepancy>;
%template(MakeMCLDPartialFixedLookbackEngine) MakeMCLookbackEngine<ContinuousPartialFixedLookbackOption, LowDiscrepancy>;
%template(MakeMCLDPartialFloatingLookbackEngine) MakeMCLookbackEngine<ContinuousPartialFloatingLookbackOption, LowDiscrepancy>;

#endif
