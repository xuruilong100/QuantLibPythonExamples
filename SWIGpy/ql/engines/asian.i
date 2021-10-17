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
using QuantLib::MakeMCDiscreteArithmeticASEngine;
using QuantLib::MakeMCDiscreteGeometricAPEngine;
using QuantLib::MakeMCDiscreteGeometricAPHestonEngine;
using QuantLib::MakeMCDiscreteArithmeticAPEngine;
using QuantLib::MakeMCDiscreteArithmeticAPHestonEngine;
%}

%shared_ptr(AnalyticContinuousGeometricAveragePriceAsianEngine)
class AnalyticContinuousGeometricAveragePriceAsianEngine : public PricingEngine {
  public:
    AnalyticContinuousGeometricAveragePriceAsianEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticContinuousGeometricAveragePriceAsianHestonEngine)
class AnalyticContinuousGeometricAveragePriceAsianHestonEngine : public PricingEngine {
  public:
    AnalyticContinuousGeometricAveragePriceAsianHestonEngine(
        ext::shared_ptr<HestonProcess> process,
        Size summationCutoff = 50,
        Real xiRightLimit = 100.0);
    %extend {
        std::pair<Real, Real> Phi (
            Real sr, Real si,
            Real wr, Real wi,
            Real T, Real t = 0.0,
            Size cutoff = 50) const {
            std::complex<Real> s(sr, si), w(wr, wi);
            std::complex<Real> tmp = self->Phi(
                s, w, T, t, cutoff);
            return std::pair<Real, Real>(
                tmp.real(), tmp.imag());
        }
    }
};

%shared_ptr(ContinuousArithmeticAsianLevyEngine)
class ContinuousArithmeticAsianLevyEngine : public PricingEngine {
  public:
    ContinuousArithmeticAsianLevyEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Handle<Quote> runningAverage,
        Date startDate);
};

%shared_ptr(ContinuousArithmeticAsianVecerEngine)
class ContinuousArithmeticAsianVecerEngine : public PricingEngine {
    %feature("kwargs") ContinuousArithmeticAsianVecerEngine;
  public:
    ContinuousArithmeticAsianVecerEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Handle<Quote> currentAverage,
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
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticDiscreteGeometricAveragePriceAsianHestonEngine)
class AnalyticDiscreteGeometricAveragePriceAsianHestonEngine : public PricingEngine {
  public:
    AnalyticDiscreteGeometricAveragePriceAsianHestonEngine(
        ext::shared_ptr<HestonProcess> process,
        Real xiRightLimit = 100.0);
    %extend {
        std::pair<Real, Real> Phi (
            Real sr, Real si,
            Real wr, Real wi,
            Time t, Time T,
            Size kStar,
            const std::vector<Time>& t_n,
            const std::vector<Time>& tauK) const {
            std::complex<Real> s(sr, si), w(wr, wi);
            std::complex<Real> tmp = self->Phi(
                s, w, t, T, kStar, t_n, tauK);
            return std::pair<Real, Real>(
                tmp.real(), tmp.imag());
        }
    }
};

%shared_ptr(AnalyticDiscreteGeometricAverageStrikeAsianEngine)
class AnalyticDiscreteGeometricAverageStrikeAsianEngine : public PricingEngine {
  public:
    AnalyticDiscreteGeometricAverageStrikeAsianEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(MCDiscreteArithmeticAPEngine<PseudoRandom>);
%shared_ptr(MCDiscreteArithmeticAPEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteArithmeticAPEngine : public PricingEngine {
  public:
    MCDiscreteArithmeticAPEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        bool brownianBridge,
        bool antitheticVariate,
        bool controlVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRDiscreteArithmeticAPEngine) MCDiscreteArithmeticAPEngine<PseudoRandom>;
%template(MCLDDiscreteArithmeticAPEngine) MCDiscreteArithmeticAPEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCDiscreteArithmeticAPEngine {
  public:
    explicit MakeMCDiscreteArithmeticAPEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
    // named parameters
    MakeMCDiscreteArithmeticAPEngine& withBrownianBridge(bool b = true);
    MakeMCDiscreteArithmeticAPEngine& withSamples(Size samples);
    MakeMCDiscreteArithmeticAPEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCDiscreteArithmeticAPEngine& withMaxSamples(Size samples);
    MakeMCDiscreteArithmeticAPEngine& withSeed(BigNatural seed);
    MakeMCDiscreteArithmeticAPEngine& withAntitheticVariate(bool b = true);
    MakeMCDiscreteArithmeticAPEngine& withControlVariate(bool b = true);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRDiscreteArithmeticAPEngine) MakeMCDiscreteArithmeticAPEngine<PseudoRandom>;
%template(MakeMCLDDiscreteArithmeticAPEngine) MakeMCDiscreteArithmeticAPEngine<LowDiscrepancy>;

%shared_ptr(MCDiscreteArithmeticAPHestonEngine<PseudoRandom>);
%shared_ptr(MCDiscreteArithmeticAPHestonEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteArithmeticAPHestonEngine : public PricingEngine {
  public:
    MCDiscreteArithmeticAPHestonEngine(
        const ext::shared_ptr<HestonProcess>& process,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed,
        Size timeSteps=Null<Size>(),
        Size timeStepsPerYear=Null<Size>(),
        bool controlVariate=false);
};

%template(MCPRDiscreteArithmeticAPHestonEngine) MCDiscreteArithmeticAPHestonEngine<PseudoRandom>;
%template(MCLDDiscreteArithmeticAPHestonEngine) MCDiscreteArithmeticAPHestonEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCDiscreteArithmeticAPHestonEngine {
  public:
    explicit MakeMCDiscreteArithmeticAPHestonEngine(ext::shared_ptr<HestonProcess> process);
    // named parameters
    MakeMCDiscreteArithmeticAPHestonEngine& withSamples(Size samples);
    MakeMCDiscreteArithmeticAPHestonEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCDiscreteArithmeticAPHestonEngine& withMaxSamples(Size samples);
    MakeMCDiscreteArithmeticAPHestonEngine& withSeed(BigNatural seed);
    MakeMCDiscreteArithmeticAPHestonEngine& withAntitheticVariate(bool b = true);
    MakeMCDiscreteArithmeticAPHestonEngine& withSteps(Size steps);
    MakeMCDiscreteArithmeticAPHestonEngine& withStepsPerYear(Size steps);
    MakeMCDiscreteArithmeticAPHestonEngine& withControlVariate(bool b = false);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRDiscreteArithmeticAPHestonEngine) MakeMCDiscreteArithmeticAPHestonEngine<PseudoRandom>;
%template(MakeMCLDDiscreteArithmeticAPHestonEngine) MakeMCDiscreteArithmeticAPHestonEngine<LowDiscrepancy>;

%shared_ptr(MCDiscreteArithmeticASEngine<PseudoRandom>);
%shared_ptr(MCDiscreteArithmeticASEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteArithmeticASEngine : public PricingEngine {
  public:
    MCDiscreteArithmeticASEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRDiscreteArithmeticASEngine) MCDiscreteArithmeticASEngine<PseudoRandom>;
%template(MCLDDiscreteArithmeticASEngine) MCDiscreteArithmeticASEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCDiscreteArithmeticASEngine {
  public:
    explicit MakeMCDiscreteArithmeticASEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
    // named parameters
    MakeMCDiscreteArithmeticASEngine& withBrownianBridge(bool b = true);
    MakeMCDiscreteArithmeticASEngine& withSamples(Size samples);
    MakeMCDiscreteArithmeticASEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCDiscreteArithmeticASEngine& withMaxSamples(Size samples);
    MakeMCDiscreteArithmeticASEngine& withSeed(BigNatural seed);
    MakeMCDiscreteArithmeticASEngine& withAntitheticVariate(bool b = true);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRDiscreteArithmeticASEngine) MakeMCDiscreteArithmeticASEngine<PseudoRandom>;
%template(MakeMCLDDiscreteArithmeticASEngine) MakeMCDiscreteArithmeticASEngine<LowDiscrepancy>;

%shared_ptr(MCDiscreteGeometricAPEngine<PseudoRandom>);
%shared_ptr(MCDiscreteGeometricAPEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteGeometricAPEngine : public PricingEngine {
    %feature("kwargs") MCDiscreteGeometricAPEngine;
  public:
    MCDiscreteGeometricAPEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRDiscreteGeometricAPEngine) MCDiscreteGeometricAPEngine<PseudoRandom>;
%template(MCLDDiscreteGeometricAPEngine) MCDiscreteGeometricAPEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCDiscreteGeometricAPEngine {
  public:
    explicit MakeMCDiscreteGeometricAPEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
    // named parameters
    MakeMCDiscreteGeometricAPEngine& withBrownianBridge(bool b = true);
    MakeMCDiscreteGeometricAPEngine& withSamples(Size samples);
    MakeMCDiscreteGeometricAPEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCDiscreteGeometricAPEngine& withMaxSamples(Size samples);
    MakeMCDiscreteGeometricAPEngine& withSeed(BigNatural seed);
    MakeMCDiscreteGeometricAPEngine& withAntitheticVariate(bool b = true);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRDiscreteGeometricAPEngine) MakeMCDiscreteGeometricAPEngine<PseudoRandom>;
%template(MakeMCLDDiscreteGeometricAPEngine) MakeMCDiscreteGeometricAPEngine<LowDiscrepancy>;

%shared_ptr(MCDiscreteGeometricAPHestonEngine<PseudoRandom>);
%shared_ptr(MCDiscreteGeometricAPHestonEngine<LowDiscrepancy>);
template <class RNG>
class MCDiscreteGeometricAPHestonEngine : public PricingEngine {
  public:
    MCDiscreteGeometricAPHestonEngine(
        const ext::shared_ptr<HestonProcess>& process,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed,
        Size timeSteps = Null<Size>(),
        Size timeStepsPerYear = Null<Size>());
};

%template(MCPRDiscreteGeometricAPHestonEngine) MCDiscreteGeometricAPHestonEngine<PseudoRandom>;
%template(MCLDDiscreteGeometricAPHestonEngine) MCDiscreteGeometricAPHestonEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCDiscreteGeometricAPHestonEngine {
  public:
    explicit MakeMCDiscreteGeometricAPHestonEngine(
        ext::shared_ptr<HestonProcess> process);
    // named parameters
    MakeMCDiscreteGeometricAPHestonEngine& withSamples(Size samples);
    MakeMCDiscreteGeometricAPHestonEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCDiscreteGeometricAPHestonEngine& withMaxSamples(Size samples);
    MakeMCDiscreteGeometricAPHestonEngine& withSeed(BigNatural seed);
    MakeMCDiscreteGeometricAPHestonEngine& withAntitheticVariate(bool b = true);
    MakeMCDiscreteGeometricAPHestonEngine& withSteps(Size steps);
    MakeMCDiscreteGeometricAPHestonEngine& withStepsPerYear(Size steps);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRDiscreteGeometricAPHestonEngine) MakeMCDiscreteGeometricAPHestonEngine<PseudoRandom>;
%template(MakeMCLDDiscreteGeometricAPHestonEngine) MakeMCDiscreteGeometricAPHestonEngine<LowDiscrepancy>;

%shared_ptr(FdBlackScholesAsianEngine)
class FdBlackScholesAsianEngine : public PricingEngine {
  public:
    FdBlackScholesAsianEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size tGrid, Size xGrid, Size aGrid,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas());
};

#endif
