#ifndef ql_engines_forwardoptionargument_i
#define ql_engines_forwardoptionargument_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i


%{
using QuantLib::ForwardVanillaEngine;
using QuantLib::AnalyticHestonForwardEuropeanEngine;
using QuantLib::MCForwardEuropeanBSEngine;
using QuantLib::MCForwardEuropeanHestonEngine;
using QuantLib::MakeMCForwardEuropeanBSEngine;
using QuantLib::MakeMCForwardEuropeanHestonEngine;
typedef ForwardVanillaEngine<AnalyticEuropeanEngine> ForwardEuropeanEngine;
%}

%shared_ptr(ForwardEuropeanEngine)
class ForwardEuropeanEngine : public PricingEngine {
  public:
    ForwardEuropeanEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess>);
};

%shared_ptr(AnalyticHestonForwardEuropeanEngine)
class AnalyticHestonForwardEuropeanEngine : public PricingEngine {
  public:
    AnalyticHestonForwardEuropeanEngine(
        ext::shared_ptr<HestonProcess> process,
        Size integrationOrder = 144);
    Real propagator(
        Time resetTime, Real varReset) const;
    ext::shared_ptr<AnalyticHestonEngine> forwardChF(
        Handle<Quote> &spotReset, Real varReset) const;
};

%shared_ptr(MCForwardEuropeanBSEngine<PseudoRandom>);
%shared_ptr(MCForwardEuropeanBSEngine<LowDiscrepancy>);
template <class RNG>
class MCForwardEuropeanBSEngine : public PricingEngine {
  public:
    MCForwardEuropeanBSEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess> &process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples, BigNatural seed);
};

%template(MCPRForwardEuropeanBSEngine) MCForwardEuropeanBSEngine<PseudoRandom>;
%template(MCLDForwardEuropeanBSEngine) MCForwardEuropeanBSEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCForwardEuropeanBSEngine {
  public:
    explicit MakeMCForwardEuropeanBSEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
    // named parameters
    MakeMCForwardEuropeanBSEngine& withSteps(Size steps);
    MakeMCForwardEuropeanBSEngine& withStepsPerYear(Size steps);
    MakeMCForwardEuropeanBSEngine& withBrownianBridge(bool b = false);
    MakeMCForwardEuropeanBSEngine& withSamples(Size samples);
    MakeMCForwardEuropeanBSEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCForwardEuropeanBSEngine& withMaxSamples(Size samples);
    MakeMCForwardEuropeanBSEngine& withSeed(BigNatural seed);
    MakeMCForwardEuropeanBSEngine& withAntitheticVariate(bool b = true);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRForwardEuropeanBSEngine) MakeMCForwardEuropeanBSEngine<PseudoRandom>;
%template(MakeMCLDForwardEuropeanBSEngine) MakeMCForwardEuropeanBSEngine<LowDiscrepancy>;

%shared_ptr(MCForwardEuropeanHestonEngine<PseudoRandom>);
%shared_ptr(MCForwardEuropeanHestonEngine<LowDiscrepancy>);
template <class RNG>
class MCForwardEuropeanHestonEngine : public PricingEngine {
  public:
    MCForwardEuropeanHestonEngine(
        const ext::shared_ptr<HestonProcess> &process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed,
        bool controlVariate=false);
};

%template(MCPRForwardEuropeanHestonEngine) MCForwardEuropeanHestonEngine<PseudoRandom>;
%template(MCLDForwardEuropeanHestonEngine) MCForwardEuropeanHestonEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCForwardEuropeanHestonEngine {
  public:
    explicit MakeMCForwardEuropeanHestonEngine(ext::shared_ptr<HestonProcess> process);
    // named parameters
    MakeMCForwardEuropeanHestonEngine& withSteps(Size steps);
    MakeMCForwardEuropeanHestonEngine& withStepsPerYear(Size steps);
    MakeMCForwardEuropeanHestonEngine& withSamples(Size samples);
    MakeMCForwardEuropeanHestonEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCForwardEuropeanHestonEngine& withMaxSamples(Size samples);
    MakeMCForwardEuropeanHestonEngine& withSeed(BigNatural seed);
    MakeMCForwardEuropeanHestonEngine& withAntitheticVariate(bool b = true);
    MakeMCForwardEuropeanHestonEngine& withControlVariate(bool b = false);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRForwardEuropeanHestonEngine) MakeMCForwardEuropeanHestonEngine<PseudoRandom>;
%template(MakeMCLDForwardEuropeanHestonEngine) MakeMCForwardEuropeanHestonEngine<LowDiscrepancy>;

#endif
