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
using QuantLib::AnalyticEuropeanMargrabeEngine;
using QuantLib::AnalyticAmericanMargrabeEngine;
using QuantLib::MCPagodaEngine;
using QuantLib::AnalyticTwoAssetCorrelationEngine;
using QuantLib::MakeMCEuropeanBasketEngine;
using QuantLib::MakeMCAmericanBasketEngine;
using QuantLib::MakeMCEverestEngine;
using QuantLib::MakeMCHimalayaEngine;
using QuantLib::MakeMCPagodaEngine;
%}

%shared_ptr(MCEuropeanBasketEngine<PseudoRandom>)
%shared_ptr(MCEuropeanBasketEngine<LowDiscrepancy>)
template <class RNG>
class MCEuropeanBasketEngine : public PricingEngine {
  public:
    MCEuropeanBasketEngine(
        ext::shared_ptr<StochasticProcessArray>,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPREuropeanBasketEngine) MCEuropeanBasketEngine<PseudoRandom>;
%template(MCLDEuropeanBasketEngine) MCEuropeanBasketEngine<LowDiscrepancy>;

template <class RNG = PseudoRandom, class S = Statistics>
class MakeMCEuropeanBasketEngine {
  public:
    MakeMCEuropeanBasketEngine(ext::shared_ptr<StochasticProcessArray>);

    MakeMCEuropeanBasketEngine& withSteps(Size steps);
    MakeMCEuropeanBasketEngine& withStepsPerYear(Size steps);
    MakeMCEuropeanBasketEngine& withBrownianBridge(bool b = true);
    MakeMCEuropeanBasketEngine& withAntitheticVariate(bool b = true);
    MakeMCEuropeanBasketEngine& withSamples(Size samples);
    MakeMCEuropeanBasketEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCEuropeanBasketEngine& withMaxSamples(Size samples);
    MakeMCEuropeanBasketEngine& withSeed(BigNatural seed);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPREuropeanBasketEngine) MakeMCEuropeanBasketEngine<PseudoRandom>;
%template(MakeMCLDEuropeanBasketEngine) MakeMCEuropeanBasketEngine<LowDiscrepancy>;

%shared_ptr(MCAmericanBasketEngine<PseudoRandom>)
%shared_ptr(MCAmericanBasketEngine<LowDiscrepancy>)
template <class RNG>
class MCAmericanBasketEngine : public PricingEngine {
    %feature("kwargs") MCAmericanBasketEngine;

  public:
    MCAmericanBasketEngine(
        const ext::shared_ptr<StochasticProcessArray>& ,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed,
        Size nCalibrationSamples=Null<Size>(),
        Size polynomOrder=2,
        LsmBasisSystem::PolynomType polynomType=LsmBasisSystem::Monomial);
};

%template(MCPRAmericanBasketEngine) MCAmericanBasketEngine<PseudoRandom>;
%template(MCLDAmericanBasketEngine) MCAmericanBasketEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCAmericanBasketEngine {
  public:
    MakeMCAmericanBasketEngine(ext::shared_ptr<StochasticProcessArray>);

    MakeMCAmericanBasketEngine& withSteps(Size steps);
    MakeMCAmericanBasketEngine& withStepsPerYear(Size steps);
    MakeMCAmericanBasketEngine& withBrownianBridge(bool b = true);
    MakeMCAmericanBasketEngine& withAntitheticVariate(bool b = true);
    MakeMCAmericanBasketEngine& withSamples(Size samples);
    MakeMCAmericanBasketEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCAmericanBasketEngine& withMaxSamples(Size samples);
    MakeMCAmericanBasketEngine& withSeed(BigNatural seed);
    MakeMCAmericanBasketEngine& withCalibrationSamples(Size samples);
    MakeMCAmericanBasketEngine& withPolynomialOrder(Size polynmOrder);
    MakeMCAmericanBasketEngine& withBasisSystem(LsmBasisSystem::PolynomType polynomType);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRAmericanBasketEngine) MakeMCAmericanBasketEngine<PseudoRandom>;
%template(MakeMCLDAmericanBasketEngine) MakeMCAmericanBasketEngine<LowDiscrepancy>;

%shared_ptr(StulzEngine)
class StulzEngine : public PricingEngine {
  public:
    StulzEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process1,
        ext::shared_ptr<GeneralizedBlackScholesProcess> process2,
        Real correlation);
};

%shared_ptr(KirkEngine)
class KirkEngine : public PricingEngine {
  public:
    KirkEngine(
        ext::shared_ptr<BlackProcess> process1,
        ext::shared_ptr<BlackProcess> process2,
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

%shared_ptr(MCEverestEngine<PseudoRandom>)
%shared_ptr(MCEverestEngine<LowDiscrepancy>)
template <class RNG>
class MCEverestEngine : public PricingEngine {
  public:
    MCEverestEngine(
        ext::shared_ptr<StochasticProcessArray>,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPREverestEngine) MCEverestEngine<PseudoRandom>;
%template(MCLDEverestEngine) MCEverestEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCEverestEngine {
  public:
    explicit MakeMCEverestEngine(ext::shared_ptr<StochasticProcessArray>);

    MakeMCEverestEngine& withSteps(Size steps);
    MakeMCEverestEngine& withStepsPerYear(Size steps);
    MakeMCEverestEngine& withBrownianBridge(bool b = true);
    MakeMCEverestEngine& withAntitheticVariate(bool b = true);
    MakeMCEverestEngine& withSamples(Size samples);
    MakeMCEverestEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCEverestEngine& withMaxSamples(Size samples);
    MakeMCEverestEngine& withSeed(BigNatural seed);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPREverestEngine) MakeMCEverestEngine<PseudoRandom>;
%template(MakeMCLDEverestEngine) MakeMCEverestEngine<LowDiscrepancy>;

%shared_ptr(MCHimalayaEngine<PseudoRandom>)
%shared_ptr(MCHimalayaEngine<LowDiscrepancy>)
template <class RNG>
class MCHimalayaEngine : public PricingEngine {
  public:
    MCHimalayaEngine(
        ext::shared_ptr<StochasticProcessArray>,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRHimalayaEngine) MCHimalayaEngine<PseudoRandom>;
%template(MCLDHimalayaEngine) MCHimalayaEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCHimalayaEngine {
  public:
    explicit MakeMCHimalayaEngine(ext::shared_ptr<StochasticProcessArray>);

    MakeMCHimalayaEngine& withBrownianBridge(bool b = true);
    MakeMCHimalayaEngine& withAntitheticVariate(bool b = true);
    MakeMCHimalayaEngine& withSamples(Size samples);
    MakeMCHimalayaEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCHimalayaEngine& withMaxSamples(Size samples);
    MakeMCHimalayaEngine& withSeed(BigNatural seed);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRHimalayaEngine) MakeMCHimalayaEngine<PseudoRandom>;
%template(MakeMCLDHimalayaEngine) MakeMCHimalayaEngine<LowDiscrepancy>;

%shared_ptr(AnalyticAmericanMargrabeEngine)
class AnalyticAmericanMargrabeEngine : public PricingEngine {
  public:
    AnalyticAmericanMargrabeEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process1,
        ext::shared_ptr<GeneralizedBlackScholesProcess> process2,
        Real correlation);
};

%shared_ptr(AnalyticEuropeanMargrabeEngine)
class AnalyticEuropeanMargrabeEngine : public PricingEngine {
  public:
    AnalyticEuropeanMargrabeEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process1,
        ext::shared_ptr<GeneralizedBlackScholesProcess> process2,
        Real correlation);
};


%shared_ptr(MCPagodaEngine<PseudoRandom>)
%shared_ptr(MCPagodaEngine<LowDiscrepancy>)
template <class RNG>
class MCPagodaEngine : public PricingEngine {
  public:
    MCPagodaEngine(
        ext::shared_ptr<StochasticProcessArray>,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRPagodaEngine) MCPagodaEngine<PseudoRandom>;
%template(MCLDPagodaEngine) MCPagodaEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCPagodaEngine {
  public:
    explicit MakeMCPagodaEngine(ext::shared_ptr<StochasticProcessArray>);

    MakeMCPagodaEngine& withBrownianBridge(bool b = true);
    MakeMCPagodaEngine& withAntitheticVariate(bool b = true);
    MakeMCPagodaEngine& withSamples(Size samples);
    MakeMCPagodaEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCPagodaEngine& withMaxSamples(Size samples);
    MakeMCPagodaEngine& withSeed(BigNatural seed);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRPagodaEngine) MakeMCPagodaEngine<PseudoRandom>;
%template(MakeMCLDPagodaEngine) MakeMCPagodaEngine<LowDiscrepancy>;

%shared_ptr(AnalyticTwoAssetCorrelationEngine)
class AnalyticTwoAssetCorrelationEngine : public PricingEngine {
  public:
    AnalyticTwoAssetCorrelationEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> p1,
        ext::shared_ptr<GeneralizedBlackScholesProcess> p2,
        Handle<Quote> correlation);
};

#endif
