#ifndef ql_engines_others_i
#define ql_engines_others_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticSimpleChooserEngine;
using QuantLib::AnalyticComplexChooserEngine;
using QuantLib::AnalyticCompoundOptionEngine;
using QuantLib::AnalyticHolderExtensibleOptionEngine;
using QuantLib::AnalyticWriterExtensibleOptionEngine;
using QuantLib::IntegralHestonVarianceOptionEngine;
using QuantLib::ReplicatingVarianceSwapEngine;
using QuantLib::MCVarianceSwapEngine;
using QuantLib::MakeMCVarianceSwapEngine;
%}

%shared_ptr(AnalyticSimpleChooserEngine)
class AnalyticSimpleChooserEngine : public PricingEngine {
  public:
    explicit AnalyticSimpleChooserEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticComplexChooserEngine)
class AnalyticComplexChooserEngine : public PricingEngine {
  public:
    explicit AnalyticComplexChooserEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticCompoundOptionEngine)
class AnalyticCompoundOptionEngine : public PricingEngine {
  public:
    explicit AnalyticCompoundOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticHolderExtensibleOptionEngine)
class AnalyticHolderExtensibleOptionEngine : public PricingEngine {
  public:
    explicit AnalyticHolderExtensibleOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticWriterExtensibleOptionEngine)
class AnalyticWriterExtensibleOptionEngine : public PricingEngine {
  public:
    explicit AnalyticWriterExtensibleOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(IntegralHestonVarianceOptionEngine)
class IntegralHestonVarianceOptionEngine : public PricingEngine {
  public:
    explicit IntegralHestonVarianceOptionEngine(
        ext::shared_ptr<HestonProcess>);
};

%shared_ptr(ReplicatingVarianceSwapEngine)
class ReplicatingVarianceSwapEngine : public PricingEngine {
  public:
    ReplicatingVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Real dk = 5.0,
        const std::vector<Real>& callStrikes = std::vector<Real>(),
        const std::vector<Real>& putStrikes = std::vector<Real>());
};

%shared_ptr(MCVarianceSwapEngine<PseudoRandom>)
%shared_ptr(MCVarianceSwapEngine<LowDiscrepancy>)
template <class RNG>
class MCVarianceSwapEngine : public PricingEngine {
  public:
    MCVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRVarianceSwapEngine) MCVarianceSwapEngine<PseudoRandom>;
%template(MCLDVarianceSwapEngine) MCVarianceSwapEngine<LowDiscrepancy>;

%shared_ptr(MakeMCVarianceSwapEngine<PseudoRandom>)
%shared_ptr(MakeMCVarianceSwapEngine<LowDiscrepancy>)
template <class RNG>
class MakeMCVarianceSwapEngine {
  public:
    MakeMCVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
    // named parameters
    MakeMCVarianceSwapEngine& withSteps(Size steps);
    MakeMCVarianceSwapEngine& withStepsPerYear(Size steps);
    MakeMCVarianceSwapEngine& withBrownianBridge(bool b = true);
    MakeMCVarianceSwapEngine& withSamples(Size samples);
    MakeMCVarianceSwapEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCVarianceSwapEngine& withMaxSamples(Size samples);
    MakeMCVarianceSwapEngine& withSeed(BigNatural seed);
    MakeMCVarianceSwapEngine& withAntitheticVariate(bool b = true);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(*self);
        }
    }
};

%template(MakeMCPRVarianceSwapEngine) MakeMCVarianceSwapEngine<PseudoRandom>;
%template(MakeMCLDVarianceSwapEngine) MakeMCVarianceSwapEngine<LowDiscrepancy>;

#endif
