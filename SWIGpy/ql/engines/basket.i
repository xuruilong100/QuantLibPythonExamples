#ifndef ql_engines_basket_i
#define ql_engines_basket_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::MCEuropeanBasketEngine;
using QuantLib::MCAmericanBasketEngine;
using QuantLib::StulzEngine;
using QuantLib::KirkEngine;
using QuantLib::Fd2dBlackScholesVanillaEngine;
using QuantLib::MCEverestEngine;
using QuantLib::MCHimalayaEngine;
%}

%shared_ptr(MCEuropeanBasketEngine<PseudoRandom>);
%shared_ptr(MCEuropeanBasketEngine<LowDiscrepancy>);
template <class RNG>
class MCEuropeanBasketEngine : public PricingEngine {
    %feature("kwargs") MCEuropeanBasketEngine;

  public:
    %extend {
        MCEuropeanBasketEngine(
            const ext::shared_ptr<StochasticProcessArray>& process,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool brownianBridge = false,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            return new MCEuropeanBasketEngine<RNG>(
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

%template(MCPREuropeanBasketEngine) MCEuropeanBasketEngine<PseudoRandom>;
%template(MCLDEuropeanBasketEngine) MCEuropeanBasketEngine<LowDiscrepancy>;

%pythoncode %{
def MCEuropeanBasketEngine(
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
        cls = MCPREuropeanBasketEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDEuropeanBasketEngine
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

%shared_ptr(MCAmericanBasketEngine<PseudoRandom>);
%shared_ptr(MCAmericanBasketEngine<LowDiscrepancy>);
template <class RNG>
class MCAmericanBasketEngine : public PricingEngine {
    %feature("kwargs") MCAmericanBasketEngine;

  public:
    %extend {
        MCAmericanBasketEngine(
            const ext::shared_ptr<StochasticProcessArray>& process,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool brownianBridge = false,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0,
            Size nCalibrationSamples = Null<Size>(),
            Size polynomOrder = 2,
            LsmBasisSystem::PolynomType polynomType = LsmBasisSystem::Monomial) {
            return new MCAmericanBasketEngine<RNG>(
                process,
                timeSteps,
                timeStepsPerYear,
                brownianBridge,
                antitheticVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed,
                nCalibrationSamples,
                polynomOrder,
                polynomType);
        }
    }
};

%template(MCPRAmericanBasketEngine) MCAmericanBasketEngine<PseudoRandom>;
%template(MCLDAmericanBasketEngine) MCAmericanBasketEngine<LowDiscrepancy>;

%pythoncode %{
def MCAmericanBasketEngine(
        process,
        traits,
        timeSteps=None,
        timeStepsPerYear=None,
        brownianBridge=False,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0,
        nCalibrationSamples=None,
        polynomOrder=2,
        polynomType=LsmBasisSystem.Monomial):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRAmericanBasketEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDAmericanBasketEngine
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
        seed,
        nCalibrationSamples,
        polynomOrder,
        polynomType)
%}

%shared_ptr(StulzEngine)
class StulzEngine : public PricingEngine {
  public:
    StulzEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process1,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process2,
        Real correlation);
};

%shared_ptr(KirkEngine)
class KirkEngine : public PricingEngine {
  public:
    KirkEngine(
        const ext::shared_ptr<BlackProcess>& process1,
        const ext::shared_ptr<BlackProcess>& process2,
        Real correlation);
};

%shared_ptr(Fd2dBlackScholesVanillaEngine)
class Fd2dBlackScholesVanillaEngine : public PricingEngine {
  public:
    Fd2dBlackScholesVanillaEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& p1,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& p2,
        Real correlation,
        Size xGrid = 100,
        Size yGrid = 100,
        Size tGrid = 50,
        Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>());
};

%shared_ptr(MCEverestEngine<PseudoRandom>);
%shared_ptr(MCEverestEngine<LowDiscrepancy>);
template <class RNG>
class MCEverestEngine : public PricingEngine {
    %feature("kwargs") MCEverestEngine;

  public:
    %extend {
        MCEverestEngine(
            const ext::shared_ptr<StochasticProcessArray>& process,
            Size timeSteps = Null<Size>(),
            Size timeStepsPerYear = Null<Size>(),
            bool brownianBridge = false,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            return new MCEverestEngine<RNG>(
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

%template(MCPREverestEngine) MCEverestEngine<PseudoRandom>;
%template(MCLDEverestEngine) MCEverestEngine<LowDiscrepancy>;

%pythoncode %{
def MCEverestEngine(
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
        cls = MCPREverestEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDEverestEngine
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

%shared_ptr(MCHimalayaEngine<PseudoRandom>);
%shared_ptr(MCHimalayaEngine<LowDiscrepancy>);
template <class RNG>
class MCHimalayaEngine : public PricingEngine {
    %feature("kwargs") MCHimalayaEngine;

  public:
    %extend {
        MCHimalayaEngine(
            const ext::shared_ptr<StochasticProcessArray>& process,
            bool brownianBridge = false,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            return new MCHimalayaEngine<RNG>(
                process,
                brownianBridge,
                antitheticVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed);
        }
    }
};

%template(MCPRHimalayaEngine) MCHimalayaEngine<PseudoRandom>;
%template(MCLDHimalayaEngine) MCHimalayaEngine<LowDiscrepancy>;

%pythoncode %{
def MCHimalayaEngine(
        process,
        traits,
        brownianBridge=False,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRHimalayaEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDHimalayaEngine
    else:
        raise RuntimeError("unknown MC traits: %s" % traits);
    return cls(
        process,
        brownianBridge,
        antitheticVariate,
        requiredSamples,
        requiredTolerance,
        maxSamples,
        seed)
%}

#endif
