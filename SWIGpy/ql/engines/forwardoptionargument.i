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
typedef ForwardVanillaEngine<AnalyticEuropeanEngine> ForwardEuropeanEngine;
%}

%shared_ptr(ForwardEuropeanEngine)
class ForwardEuropeanEngine : public PricingEngine {
  public:
    ForwardEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>&);
};

%shared_ptr(AnalyticHestonForwardEuropeanEngine)
class AnalyticHestonForwardEuropeanEngine : public PricingEngine {
  public:
    AnalyticHestonForwardEuropeanEngine(
        const ext::shared_ptr<HestonProcess>& process,
        Size integrationOrder = 144);
};

%shared_ptr(MCForwardEuropeanBSEngine<PseudoRandom>);
%shared_ptr(MCForwardEuropeanBSEngine<LowDiscrepancy>);
template <class RNG>
class MCForwardEuropeanBSEngine : public PricingEngine {
    %feature("kwargs") MCForwardEuropeanBSEngine;

  public:
    %extend {
        MCForwardEuropeanBSEngine(
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool brownianBridge = false,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            return new MCForwardEuropeanBSEngine<RNG>(
                process,
                timeSteps,
                timeStepsPerYear,
                brownianBridge,
                antitheticVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed);
        }
    }
};

%template(MCPRForwardEuropeanBSEngine) MCForwardEuropeanBSEngine<PseudoRandom>;
%template(MCLDForwardEuropeanBSEngine) MCForwardEuropeanBSEngine<LowDiscrepancy>;

%pythoncode %{
def MCForwardEuropeanBSEngine(
        process,
        traits,
        timeSteps=None,
        timeStepsPerYear=None,
        brownianBridge=False,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRForwardEuropeanBSEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDForwardEuropeanBSEngine
    else:
        raise RuntimeError("unknown MC traits: %s" % traits);
    return cls(
        process,
        timeSteps,
        timeStepsPerYear,
        brownianBridge,
        antitheticVariate,
        requiredSamples,
        requiredTolerance,
        maxSamples,
        seed)
%}

%shared_ptr(MCForwardEuropeanHestonEngine<PseudoRandom>);
%shared_ptr(MCForwardEuropeanHestonEngine<LowDiscrepancy>);
template <class RNG>
class MCForwardEuropeanHestonEngine : public PricingEngine {
    %feature("kwargs") MCForwardEuropeanHestonEngine;

  public:
    %extend {
        MCForwardEuropeanHestonEngine(
            const ext::shared_ptr<HestonProcess>& process,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0,
            bool controlVariate = false) {
            return new MCForwardEuropeanHestonEngine<RNG>(
                process,
                timeSteps,
                timeStepsPerYear,
                antitheticVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed,
                controlVariate);
        }
    }
};

%template(MCPRForwardEuropeanHestonEngine) MCForwardEuropeanHestonEngine<PseudoRandom>;
%template(MCLDForwardEuropeanHestonEngine) MCForwardEuropeanHestonEngine<LowDiscrepancy>;

%pythoncode %{
def MCForwardEuropeanHestonEngine(
        process,
        traits,
        timeSteps=None,
        timeStepsPerYear=None,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0,
        controlVariate=False):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRForwardEuropeanHestonEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDForwardEuropeanHestonEngine
    else:
        raise RuntimeError("unknown MC traits: %s" % traits);
    return cls(
        process,
        timeSteps,
        timeStepsPerYear,
        antitheticVariate,
        requiredSamples,
        requiredTolerance,
        maxSamples,
        seed,
        controlVariate)
%}

#endif
