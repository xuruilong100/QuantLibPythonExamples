#ifndef ql_engines_cliquet_i
#define ql_engines_cliquet_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticCliquetEngine;
using QuantLib::AnalyticPerformanceEngine;
using QuantLib::MCPerformanceEngine;
using QuantLib::MakeMCPerformanceEngine;
%}

%shared_ptr(AnalyticCliquetEngine)
class AnalyticCliquetEngine : public PricingEngine {
  public:
    AnalyticCliquetEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticPerformanceEngine)
class AnalyticPerformanceEngine : public PricingEngine {
  public:
    AnalyticPerformanceEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(MCPerformanceEngine<PseudoRandom>)
%shared_ptr(MCPerformanceEngine<LowDiscrepancy>)
template<class RNG>
class MCPerformanceEngine : public PricingEngine {
  public:
    MCPerformanceEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRPerformanceEngine) MCPerformanceEngine<PseudoRandom>;
%template(MCLDPerformanceEngine) MCPerformanceEngine<LowDiscrepancy>;

%shared_ptr(MakeMCPerformanceEngine<PseudoRandom>)
%shared_ptr(MakeMCPerformanceEngine<LowDiscrepancy>)
template <class RNG>
class MakeMCPerformanceEngine {
  public:
    MakeMCPerformanceEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);

    MakeMCPerformanceEngine& withBrownianBridge(bool b = true);
    MakeMCPerformanceEngine& withAntitheticVariate(bool b = true);
    MakeMCPerformanceEngine& withSamples(Size samples);
    MakeMCPerformanceEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCPerformanceEngine& withMaxSamples(Size samples);
    MakeMCPerformanceEngine& withSeed(BigNatural seed);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(*self);
        }
    }
};

%template(MakeMCPRPerformanceEngine) MakeMCPerformanceEngine<PseudoRandom>;
%template(MakeMCLDPerformanceEngine) MakeMCPerformanceEngine<LowDiscrepancy>;

#endif
