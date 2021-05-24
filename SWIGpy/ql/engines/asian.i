#ifndef ql_engines_asian_i
#define ql_engines_asian_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticContinuousGeometricAveragePriceAsianEngine;
using QuantLib::AnalyticContinuousGeometricAveragePriceAsianHestonEngine;
using QuantLib::ContinuousArithmeticAsianLevyEngine;
using QuantLib::ContinuousArithmeticAsianVecerEngine;
using QuantLib::AnalyticDiscreteGeometricAveragePriceAsianEngine;
using QuantLib::AnalyticDiscreteGeometricAveragePriceAsianHestonEngine;
using QuantLib::AnalyticDiscreteGeometricAverageStrikeAsianEngine;
using QuantLib::MCDiscreteArithmeticAPEngine;
using QuantLib::MCDiscreteArithmeticAPHestonEngine;
using QuantLib::MCDiscreteArithmeticASEngine;
using QuantLib::MCDiscreteGeometricAPEngine;
using QuantLib::MCDiscreteGeometricAPHestonEngine;
using QuantLib::FdBlackScholesAsianEngine;
%}

%shared_ptr(AnalyticContinuousGeometricAveragePriceAsianEngine)
class AnalyticContinuousGeometricAveragePriceAsianEngine : public PricingEngine {
  public:
    AnalyticContinuousGeometricAveragePriceAsianEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(AnalyticContinuousGeometricAveragePriceAsianHestonEngine)
class AnalyticContinuousGeometricAveragePriceAsianHestonEngine : public PricingEngine {
  public:
    AnalyticContinuousGeometricAveragePriceAsianHestonEngine(
        const ext::shared_ptr<HestonProcess>& process,
        Size summationCutoff = 50,
        Real xiRightLimit = 100.0);
};

%shared_ptr(ContinuousArithmeticAsianLevyEngine)
class ContinuousArithmeticAsianLevyEngine : public PricingEngine {
  public:
    ContinuousArithmeticAsianLevyEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        const Handle<Quote>& runningAverage,
        const Date& startDate);
};

%shared_ptr(ContinuousArithmeticAsianVecerEngine)
class ContinuousArithmeticAsianVecerEngine : public PricingEngine {
    %feature("kwargs") ContinuousArithmeticAsianVecerEngine;
  public:
    ContinuousArithmeticAsianVecerEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        const Handle<Quote>& currentAverage,
        Date startDate,
        Size timeSteps = 100,
        Size assetSteps = 100,
        Real z_min = -1.0,
        Real z_max = 1.0);
};

%shared_ptr(AnalyticDiscreteGeometricAveragePriceAsianEngine)
class AnalyticDiscreteGeometricAveragePriceAsianEngine : public PricingEngine {
  public:
    AnalyticDiscreteGeometricAveragePriceAsianEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(AnalyticDiscreteGeometricAveragePriceAsianHestonEngine)
class AnalyticDiscreteGeometricAveragePriceAsianHestonEngine : public PricingEngine {
  public:
    AnalyticDiscreteGeometricAveragePriceAsianHestonEngine(
        const ext::shared_ptr<HestonProcess>& process,
        Real xiRightLimit = 100.0);
};

%shared_ptr(AnalyticDiscreteGeometricAverageStrikeAsianEngine)
class AnalyticDiscreteGeometricAverageStrikeAsianEngine : public PricingEngine {
  public:
    AnalyticDiscreteGeometricAverageStrikeAsianEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(MCDiscreteArithmeticAPEngine<PseudoRandom>);
%shared_ptr(MCDiscreteArithmeticAPEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteArithmeticAPEngine : public PricingEngine {
    %feature("kwargs") MCDiscreteArithmeticAPEngine;

  public:
    %extend {
        MCDiscreteArithmeticAPEngine(
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
            bool brownianBridge = false,
            bool antitheticVariate = false,
            bool controlVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            return new MCDiscreteArithmeticAPEngine<RNG>(
                process,
                brownianBridge,
                antitheticVariate,
                controlVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed);
        }
    }
};

%template(MCPRDiscreteArithmeticAPEngine) MCDiscreteArithmeticAPEngine<PseudoRandom>;
%template(MCLDDiscreteArithmeticAPEngine) MCDiscreteArithmeticAPEngine<LowDiscrepancy>;

%pythoncode %{
def MCDiscreteArithmeticAPEngine(
        process,
        traits,
        brownianBridge=True,
        antitheticVariate=False,
        controlVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRDiscreteArithmeticAPEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDDiscreteArithmeticAPEngine
    else:
        raise RuntimeError("unknown MC traits: %s" % traits);
    return cls(
        process,
        brownianBridge,
        antitheticVariate,
        controlVariate,
        requiredSamples,
        requiredTolerance,
        maxSamples,
        seed)
%}

%shared_ptr(MCDiscreteArithmeticAPHestonEngine<PseudoRandom>);
%shared_ptr(MCDiscreteArithmeticAPHestonEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteArithmeticAPHestonEngine : public PricingEngine {
    %feature("kwargs") MCDiscreteArithmeticAPHestonEngine;

  public:
    %extend {
        MCDiscreteArithmeticAPHestonEngine(
            const ext::shared_ptr<HestonProcess>& process,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool controlVariate = false) {
            return new MCDiscreteArithmeticAPHestonEngine<RNG>(
                process,
                antitheticVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed,
                timeSteps,
                timeStepsPerYear,
                controlVariate);
        }
    }
};

%template(MCPRDiscreteArithmeticAPHestonEngine) MCDiscreteArithmeticAPHestonEngine<PseudoRandom>;
%template(MCLDDiscreteArithmeticAPHestonEngine) MCDiscreteArithmeticAPHestonEngine<LowDiscrepancy>;

%pythoncode %{
def MCDiscreteArithmeticAPHestonEngine(
        process,
        traits,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0,
        timeSteps=None,
        timeStepsPerYear=None,
        controlVariate=False):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRDiscreteArithmeticAPHestonEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDDiscreteArithmeticAPHestonEngine
    else:
        raise RuntimeError("unknown MC traits: %s" % traits);
    return cls(
        process,
        antitheticVariate,
        requiredSamples,
        requiredTolerance,
        maxSamples,
        seed,
        timeSteps,
        timeStepsPerYear,
        controlVariate)
%}

%shared_ptr(MCDiscreteArithmeticASEngine<PseudoRandom>);
%shared_ptr(MCDiscreteArithmeticASEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteArithmeticASEngine : public PricingEngine {
    %feature("kwargs") MCDiscreteArithmeticASEngine;
  public:
    %extend {
        MCDiscreteArithmeticASEngine(
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
            bool brownianBridge = false,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            return new MCDiscreteArithmeticASEngine<RNG>(
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

%template(MCPRDiscreteArithmeticASEngine) MCDiscreteArithmeticASEngine<PseudoRandom>;
%template(MCLDDiscreteArithmeticASEngine) MCDiscreteArithmeticASEngine<LowDiscrepancy>;

%pythoncode %{
def MCDiscreteArithmeticASEngine(
        process,
        traits,
        brownianBridge=True,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRDiscreteArithmeticASEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDDiscreteArithmeticASEngine
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

%shared_ptr(MCDiscreteGeometricAPEngine<PseudoRandom>);
%shared_ptr(MCDiscreteGeometricAPEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteGeometricAPEngine : public PricingEngine {
    %feature("kwargs") MCDiscreteGeometricAPEngine;
  public:
    %extend {
        MCDiscreteGeometricAPEngine(
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
            bool brownianBridge = false,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            return new MCDiscreteGeometricAPEngine<RNG>(
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

%template(MCPRDiscreteGeometricAPEngine) MCDiscreteGeometricAPEngine<PseudoRandom>;
%template(MCLDDiscreteGeometricAPEngine) MCDiscreteGeometricAPEngine<LowDiscrepancy>;

%pythoncode %{
def MCDiscreteGeometricAPEngine(
        process,
        traits,
        brownianBridge=True,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRDiscreteGeometricAPEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDDiscreteGeometricAPEngine
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

%shared_ptr(MCDiscreteGeometricAPHestonEngine<PseudoRandom>);
%shared_ptr(MCDiscreteGeometricAPHestonEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteGeometricAPHestonEngine : public PricingEngine {
    %feature("kwargs") MCDiscreteGeometricAPHestonEngine;
  public:
    %extend {
        MCDiscreteGeometricAPHestonEngine(
            const ext::shared_ptr<HestonProcess>& process,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>()) {
            return new MCDiscreteGeometricAPHestonEngine<RNG>(
                process,
                antitheticVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed,
                timeSteps,
                timeStepsPerYear);
        }
    }
};

%template(MCPRDiscreteGeometricAPHestonEngine) MCDiscreteGeometricAPHestonEngine<PseudoRandom>;
%template(MCLDDiscreteGeometricAPHestonEngine) MCDiscreteGeometricAPHestonEngine<LowDiscrepancy>;

%pythoncode %{
def MCDiscreteGeometricAPHestonEngine(
        process,
        traits,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0,
        timeSteps=None,
        timeStepsPerYear=None):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRDiscreteGeometricAPHestonEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDDiscreteGeometricAPHestonEngine
    else:
        raise RuntimeError("unknown MC traits: %s" % traits);
    return cls(
        process,
        antitheticVariate,
        requiredSamples,
        requiredTolerance,
        maxSamples,
        seed,
        timeSteps,
        timeStepsPerYear)
%}

%shared_ptr(FdBlackScholesAsianEngine)
class FdBlackScholesAsianEngine : public PricingEngine {
  public:
    FdBlackScholesAsianEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size tGrid, Size xGrid, Size aGrid);
};

#endif
