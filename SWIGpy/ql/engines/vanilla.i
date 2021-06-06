#ifndef ql_engines_vanilla_i
#define ql_engines_vanilla_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticCEVEngine;
using QuantLib::AnalyticBSMHullWhiteEngine;
using QuantLib::AnalyticDigitalAmericanEngine;
using QuantLib::AnalyticDigitalAmericanKOEngine;
using QuantLib::AnalyticEuropeanEngine;
using QuantLib::AnalyticGJRGARCHEngine;
using QuantLib::AnalyticHestonEngine;
using QuantLib::AnalyticPTDHestonEngine;
using QuantLib::BaroneAdesiWhaleyApproximationEngine;
using QuantLib::BatesEngine;
using QuantLib::BjerksundStenslandApproximationEngine;
using QuantLib::COSHestonEngine;
using QuantLib::ExponentialFittingHestonEngine;
using QuantLib::FdBlackScholesVanillaEngine;
using QuantLib::FdBatesVanillaEngine;
using QuantLib::FdCEVVanillaEngine;
using QuantLib::FdHestonVanillaEngine;
using QuantLib::FdSabrVanillaEngine;
using QuantLib::FFTVarianceGammaEngine;
using QuantLib::FFTVanillaEngine;
using QuantLib::IntegralEngine;
using QuantLib::JuQuadraticApproximationEngine;
using QuantLib::MCAmericanEngine;
using QuantLib::MCEuropeanEngine;
using QuantLib::MakeMCEuropeanEngine;
using QuantLib::VarianceGammaEngine;
using QuantLib::CrankNicolson;
using QuantLib::FDBermudanEngine;
using QuantLib::FDEuropeanEngine;
using QuantLib::BinomialVanillaEngine;
using QuantLib::CoxRossRubinstein;
using QuantLib::JarrowRudd;
using QuantLib::AdditiveEQPBinomialTree;
using QuantLib::Trigeorgis;
using QuantLib::Tian;
using QuantLib::LeisenReimer;
using QuantLib::Joshi4;
using QuantLib::MCEuropeanHestonEngine;
using QuantLib::FDAmericanEngine;
using QuantLib::FDShoutEngine;
using QuantLib::MCEuropeanGJRGARCHEngine;
%}

%shared_ptr(AnalyticCEVEngine);
class AnalyticCEVEngine : public PricingEngine {
  public:
    AnalyticCEVEngine(
        Real f0, Real alpha, Real beta,
        const Handle<YieldTermStructure>& rTS);
};

%shared_ptr(BinomialVanillaEngine<CoxRossRubinstein>)
%shared_ptr(BinomialVanillaEngine<JarrowRudd>)
%shared_ptr(BinomialVanillaEngine<AdditiveEQPBinomialTree>)
%shared_ptr(BinomialVanillaEngine<Trigeorgis>)
%shared_ptr(BinomialVanillaEngine<Tian>)
%shared_ptr(BinomialVanillaEngine<LeisenReimer>)
%shared_ptr(BinomialVanillaEngine<Joshi4>)
template <class T>
class BinomialVanillaEngine : public PricingEngine {
  public:
    BinomialVanillaEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
        Size steps);
};

%template(BinomialCRRVanillaEngine) BinomialVanillaEngine<CoxRossRubinstein>;
%template(BinomialJRVanillaEngine) BinomialVanillaEngine<JarrowRudd>;
%template(BinomialEQPVanillaEngine) BinomialVanillaEngine<AdditiveEQPBinomialTree>;
%template(BinomialTrigeorgisVanillaEngine) BinomialVanillaEngine<Trigeorgis>;
%template(BinomialTianVanillaEngine) BinomialVanillaEngine<Tian>;
%template(BinomialLRVanillaEngine) BinomialVanillaEngine<LeisenReimer>;
%template(BinomialJ4VanillaEngine) BinomialVanillaEngine<Joshi4>;

%pythoncode %{
def BinomialVanillaEngine(
        process, type, steps):
    type = type.lower()
    if type == "crr" or type == "coxrossrubinstein":
        cls = BinomialCRRVanillaEngine
    elif type == "jr" or type == "jarrowrudd":
        cls = BinomialJRVanillaEngine
    elif type == "eqp":
        cls = BinomialEQPVanillaEngine
    elif type == "trigeorgis":
        cls = BinomialTrigeorgisVanillaEngine
    elif type == "tian":
        cls = BinomialTianVanillaEngine
    elif type == "lr" or type == "leisenreimer":
        cls = BinomialLRVanillaEngine
    elif type == "j4" or type == "joshi4":
        cls = BinomialJ4VanillaEngine
    else:
        raise RuntimeError("unknown binomial engine type: %s" % type);
    return cls(process, steps)
%}

%shared_ptr(AnalyticBSMHullWhiteEngine)
class AnalyticBSMHullWhiteEngine : public PricingEngine {
  public:
    AnalyticBSMHullWhiteEngine(
        Real equityShortRateCorrelation,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
        const ext::shared_ptr<HullWhite>&);
};

%shared_ptr(AnalyticDigitalAmericanEngine)
class AnalyticDigitalAmericanEngine : public PricingEngine {
  public:
    AnalyticDigitalAmericanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(AnalyticDigitalAmericanKOEngine)
class AnalyticDigitalAmericanKOEngine : public PricingEngine {
  public:
    AnalyticDigitalAmericanKOEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(AnalyticEuropeanEngine)
class AnalyticEuropeanEngine : public PricingEngine {
  public:
    AnalyticEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
    AnalyticEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        const Handle<YieldTermStructure>& discountCurve);
};

%shared_ptr(AnalyticGJRGARCHEngine)
class AnalyticGJRGARCHEngine : public PricingEngine {
  public:
    AnalyticGJRGARCHEngine(
        const ext::shared_ptr<GJRGARCHModel>& process);
};

%rename (AnalyticHestonEngineIntegration) AnalyticHestonEngine::Integration;
%feature ("flatnested") AnalyticHestonEngine::Integration;
%shared_ptr(AnalyticHestonEngine)
class AnalyticHestonEngine : public PricingEngine {
  public:
    class Integration {
      public:
        // non adaptive integration algorithms based on Gaussian quadrature
        static Integration gaussLaguerre(Size integrationOrder = 128);
        static Integration gaussLegendre(Size integrationOrder = 128);
        static Integration gaussChebyshev(Size integrationOrder = 128);
        static Integration gaussChebyshev2nd(Size integrationOrder = 128);

        // for an adaptive integration algorithm Gatheral's version has to
        // be used.Be aware: using a too large number for maxEvaluations might
        // result in a stack overflow as the these integrations are based on
        // recursive algorithms.
        static Integration gaussLobatto(
            Real relTolerance, Real absTolerance,
            Size maxEvaluations = 1000);

        // usually these routines have a poor convergence behavior.
        static Integration gaussKronrod(
            Real absTolerance,
            Size maxEvaluations = 1000);
        static Integration simpson(
            Real absTolerance,
            Size maxEvaluations = 1000);
        static Integration trapezoid(
            Real absTolerance,
            Size maxEvaluations = 1000);
        static Integration discreteSimpson(
            Size evaluation = 1000);
        static Integration discreteTrapezoid(
            Size evaluation = 1000);

        static Real andersenPiterbargIntegrationLimit(
            Real c_inf, Real epsilon, Real v0, Real t);

        Real calculate(
            Real c_inf,
            const ext::function<Real(Real)>& f,
            doubleOrNull maxBound = Null<Real>()) const;

        Size numberOfEvaluations() const;
        bool isAdaptiveIntegration() const;

      private:
        enum Algorithm {
            GaussLobatto,
            GaussKronrod,
            Simpson,
            Trapezoid,
            DiscreteTrapezoid,
            DiscreteSimpson,
            GaussLaguerre,
            GaussLegendre,
            GaussChebyshev,
            GaussChebyshev2nd
        };

        Integration(
            Algorithm intAlgo,
            const ext::shared_ptr<GaussianQuadrature>& quadrature);

        Integration(
            Algorithm intAlgo,
            const ext::shared_ptr<Integrator>& integrator);
    };
    enum ComplexLogFormula {
        Gatheral,
        BranchCorrection,
        AndersenPiterbarg,
        AndersenPiterbargOptCV,
        AsymptoticChF,
        OptimalCV
    };
    AnalyticHestonEngine(
        const ext::shared_ptr<HestonModel>& model,
        Size integrationOrder = 144);
    AnalyticHestonEngine(
        const ext::shared_ptr<HestonModel>& model,
        Real relTolerance,
        Size maxEvaluations);
    AnalyticHestonEngine(
        const ext::shared_ptr<HestonModel>& model,
        ComplexLogFormula cpxLog, const AnalyticHestonEngine::Integration& itg,
        Real andersenPiterbargEpsilon = 1e-8);

    %extend {
        std::pair<Real, Real> chF(
            Real real, Real imag, Time t) const {
            const std::complex<Real> tmp = self->chF(
                std::complex<Real>(real, imag), t);
            return std::pair<Real, Real>(
                tmp.real(), tmp.imag());
        }
    }
};

%shared_ptr(AnalyticPTDHestonEngine)
class AnalyticPTDHestonEngine : public PricingEngine {
  public:
    enum ComplexLogFormula {
        Gatheral,
        AndersenPiterbarg
    };
    typedef AnalyticHestonEngine::Integration Integration;

    AnalyticPTDHestonEngine(
        const ext::shared_ptr<PiecewiseTimeDependentHestonModel>& model,
        Real relTolerance, Size maxEvaluations);
    // Constructor using Laguerre integration
    // and Gatheral's version of complex log.
    AnalyticPTDHestonEngine(
        const ext::shared_ptr<PiecewiseTimeDependentHestonModel>& model,
        Size integrationOrder = 144);

    // Constructor giving full control over Fourier integration algorithm
    AnalyticPTDHestonEngine(
        const ext::shared_ptr<PiecewiseTimeDependentHestonModel>& model,
        ComplexLogFormula cpxLog,
        const Integration& itg,
        Real andersenPiterbargEpsilon = 1e-8);
};

%shared_ptr(BaroneAdesiWhaleyApproximationEngine);
class BaroneAdesiWhaleyApproximationEngine : public PricingEngine {
  public:
    BaroneAdesiWhaleyApproximationEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(BatesEngine)
class BatesEngine : public PricingEngine {
  public:
    BatesEngine(
        const ext::shared_ptr<BatesModel>& model,
        Size integrationOrder = 144);
    BatesEngine(
        const ext::shared_ptr<BatesModel>& model,
        Real relTolerance,
        Size maxEvaluations);
};

%shared_ptr(BjerksundStenslandApproximationEngine);
class BjerksundStenslandApproximationEngine : public PricingEngine {
  public:
    BjerksundStenslandApproximationEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(COSHestonEngine)
class COSHestonEngine : public PricingEngine {
  public:
    COSHestonEngine(
        const ext::shared_ptr<HestonModel>& model,
        Real L = 16, Size N = 200);
};

%shared_ptr(ExponentialFittingHestonEngine)
class ExponentialFittingHestonEngine : public PricingEngine {
  public:
    enum ControlVariate {
        AndersenPiterbarg,
        AndersenPiterbargOptCV,
        AsymptoticChF,
        OptimalCV
    };

    ExponentialFittingHestonEngine(
        const ext::shared_ptr<HestonModel>& model,
        ControlVariate cv = AndersenPiterbargOptCV,
        doubleOrNull scaling = Null<Real>());
};

%shared_ptr(FdBlackScholesVanillaEngine)
class FdBlackScholesVanillaEngine : public PricingEngine {
  public:
    enum CashDividendModel {
        Spot,
        Escrowed
    };

    FdBlackScholesVanillaEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size tGrid = 100, Size xGrid = 100, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas(),
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>(),
        CashDividendModel cashDividendModel = Spot);

    FdBlackScholesVanillaEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
        const ext::shared_ptr<FdmQuantoHelper>& quantoHelper,
        Size tGrid = 100, Size xGrid = 100, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas(),
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>(),
        CashDividendModel cashDividendModel = Spot);

    %feature("kwargs") make;
    %extend {
        static ext::shared_ptr<FdBlackScholesVanillaEngine> make(
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
            const ext::shared_ptr<FdmQuantoHelper>& quantoHelper = ext::shared_ptr<FdmQuantoHelper>(),
            Size tGrid = 100,
            Size xGrid = 100,
            Size dampingSteps = 0,
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas(),
            bool localVol = false,
            Real illegalLocalVolOverwrite = -Null<Real>(),
            CashDividendModel cashDividendModel = Spot) {
            return ext::shared_ptr<FdBlackScholesVanillaEngine>(
                new FdBlackScholesVanillaEngine(
                    process,
                    quantoHelper,
                    tGrid,
                    xGrid,
                    dampingSteps,
                    schemeDesc,
                    localVol,
                    illegalLocalVolOverwrite,
                    cashDividendModel));
        }
    }
};

%shared_ptr(FdBatesVanillaEngine)
class FdBatesVanillaEngine : public PricingEngine {
  public:
    FdBatesVanillaEngine(
        const ext::shared_ptr<BatesModel>& model,
        Size tGrid = 100, Size xGrid = 100,
        Size vGrid=50, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer());
};

%shared_ptr(FdCEVVanillaEngine);
class FdCEVVanillaEngine : public PricingEngine {
  public:
    FdCEVVanillaEngine(
        Real f0, Real alpha, Real beta,
        const Handle<YieldTermStructure>& rTS,
        Size tGrid = 50, Size xGrid = 400,
        Size dampingSteps = 0,
        Real scalingFactor = 1.0, Real eps = 1e-4,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas());
};

%shared_ptr(FdHestonVanillaEngine)
class FdHestonVanillaEngine : public PricingEngine {
  public:
    FdHestonVanillaEngine(
        const ext::shared_ptr<HestonModel>& model,
        Size tGrid = 100, Size xGrid = 100,
        Size vGrid = 50, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
        const ext::shared_ptr<LocalVolTermStructure>& leverageFct = ext::shared_ptr<LocalVolTermStructure>(),
        const Real mixingFactor = 1.0);

    FdHestonVanillaEngine(
        const ext::shared_ptr<HestonModel>& model,
        const ext::shared_ptr<FdmQuantoHelper>& quantoHelper,
        Size tGrid = 100,
        Size xGrid = 100,
        Size vGrid = 50,
        Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
        const ext::shared_ptr<LocalVolTermStructure>& leverageFct = ext::shared_ptr<LocalVolTermStructure>(),
        const Real mixingFactor = 1.0);

    %feature("kwargs") make;
    %extend {
        static ext::shared_ptr<FdHestonVanillaEngine> make(
            const ext::shared_ptr<HestonModel>& model,
            const ext::shared_ptr<FdmQuantoHelper>& quantoHelper = ext::shared_ptr<FdmQuantoHelper>(),
            Size tGrid = 100,
            Size xGrid = 100,
            Size vGrid = 50,
            Size dampingSteps = 0,
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
            const ext::shared_ptr<LocalVolTermStructure>& leverageFct = ext::shared_ptr<LocalVolTermStructure>(),
            const Real mixingFactor = 1.0) {
            return ext::shared_ptr<FdHestonVanillaEngine>(
                new FdHestonVanillaEngine(
                    model, quantoHelper,
                    tGrid, xGrid, vGrid,
                    dampingSteps, schemeDesc,
                    leverageFct, mixingFactor));
        }
    }
};

%shared_ptr(FdSabrVanillaEngine);
class FdSabrVanillaEngine : public PricingEngine {
  public:
    FdSabrVanillaEngine(
        Real f0, Real alpha, Real beta,
        Real nu, Real rho,
        const Handle<YieldTermStructure>& rTS,
        Size tGrid = 50, Size fGrid = 400, Size xGrid = 50,
        Size dampingSteps = 0,
        Real scalingFactor = 1.0,
        Real eps = 1e-4,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer());
};

%shared_ptr(FFTVarianceGammaEngine)
class FFTVarianceGammaEngine : public PricingEngine {
  public:
    FFTVarianceGammaEngine(
        const ext::shared_ptr<VarianceGammaProcess>& process,
        Real logStrikeSpacing = 0.001);
    void precalculate(
        const std::vector<ext::shared_ptr<Instrument> >& optionList);
};

%shared_ptr(FFTVanillaEngine)
class FFTVanillaEngine : public PricingEngine {
  public:
    explicit FFTVanillaEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Real logStrikeSpacing = 0.001);
    void precalculate(
        const std::vector<ext::shared_ptr<Instrument> >& optionList);
};

%shared_ptr(IntegralEngine)
class IntegralEngine : public PricingEngine {
  public:
    IntegralEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>&);
};

%shared_ptr(JuQuadraticApproximationEngine);
class JuQuadraticApproximationEngine : public PricingEngine {
  public:
    JuQuadraticApproximationEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(MCEuropeanEngine<PseudoRandom>);
%shared_ptr(MCEuropeanEngine<LowDiscrepancy>);
template <class RNG>
class MCEuropeanEngine : public PricingEngine {
    %feature("kwargs") MCEuropeanEngine;

  public:
    %extend {
        MCEuropeanEngine(
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool brownianBridge = false,
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            QL_REQUIRE(Size(timeSteps) != Null<Size>() || Size(timeStepsPerYear) != Null<Size>(),
                       "number of steps not specified");
            return new MCEuropeanEngine<RNG>(
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

%template(MCPREuropeanEngine) MCEuropeanEngine<PseudoRandom>;
%template(MCLDEuropeanEngine) MCEuropeanEngine<LowDiscrepancy>;

%pythoncode %{
def MCEuropeanEngine(
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
        cls = MCPREuropeanEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDEuropeanEngine
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

template <class RNG>
class MakeMCEuropeanEngine {
  public:
    MakeMCEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& p);
    // named parameters
    MakeMCEuropeanEngine& withSteps(Size steps);
    MakeMCEuropeanEngine& withStepsPerYear(Size steps);
    MakeMCEuropeanEngine& withBrownianBridge(bool b = true);
    MakeMCEuropeanEngine& withSamples(Size samples);
    MakeMCEuropeanEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCEuropeanEngine& withMaxSamples(Size samples);
    MakeMCEuropeanEngine& withSeed(BigNatural seed);
    MakeMCEuropeanEngine& withAntitheticVariate(bool b = true);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> toPricingEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPREuropeanEngine) MakeMCEuropeanEngine<PseudoRandom>;
%template(MakeMCLDEuropeanEngine) MakeMCEuropeanEngine<LowDiscrepancy>;

%shared_ptr(MCAmericanEngine<PseudoRandom>);
%shared_ptr(MCAmericanEngine<LowDiscrepancy>);
template <class RNG>
class MCAmericanEngine : public PricingEngine {
    %feature("kwargs") MCAmericanEngine;

  public:
    %extend {
        MCAmericanEngine(
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool antitheticVariate = false,
            bool controlVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0,
            intOrNull polynomOrder = 2,
            LsmBasisSystem::PolynomType polynomType = LsmBasisSystem::Monomial,
            int nCalibrationSamples = 2048,
            boost::optional<bool> antitheticVariateCalibration = boost::none,
            BigNatural seedCalibration = Null<Size>()) {
            return new MCAmericanEngine<RNG>(
                process,
                timeSteps,
                timeStepsPerYear,
                antitheticVariate,
                controlVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed,
                polynomOrder,
                polynomType,
                nCalibrationSamples,
                antitheticVariateCalibration,
                seedCalibration);
        }
    }
};

%template(MCPRAmericanEngine) MCAmericanEngine<PseudoRandom>;
%template(MCLDAmericanEngine) MCAmericanEngine<LowDiscrepancy>;

%pythoncode %{
def MCAmericanEngine(
        process,
        traits,
        timeSteps=None,
        timeStepsPerYear=None,
        antitheticVariate=False,
        controlVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0,
        polynomOrder=2,
        polynomType=LsmBasisSystem.Monomial,
        nCalibrationSamples=2048,
        antitheticVariateCalibration=None,
        seedCalibration=None):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPRAmericanEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDAmericanEngine
    else:
        raise RuntimeError("unknown MC traits: %s" % traits);
    return cls(process,
               timeSteps,
               timeStepsPerYear,
               antitheticVariate,
               controlVariate,
               requiredSamples,
               requiredTolerance,
               maxSamples,
               seed,
               polynomOrder,
               polynomType,
               nCalibrationSamples,
               antitheticVariateCalibration,
               seedCalibration if seedCalibration is not None else nullInt())
%}

%shared_ptr(VarianceGammaEngine)
class VarianceGammaEngine : public PricingEngine {
  public:
    VarianceGammaEngine(
        const ext::shared_ptr<VarianceGammaProcess>& process);
};

%shared_ptr(FDBermudanEngine<CrankNicolson>);
template <class S>
class FDBermudanEngine : public PricingEngine {
  public:
    FDBermudanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size timeSteps = 100,
        Size gridPoints = 100,
        bool timeDependent = false);
};

%template(FDCNBermudanEngine) FDBermudanEngine<CrankNicolson>;

%shared_ptr(FDEuropeanEngine<CrankNicolson>);
template <class S>
class FDEuropeanEngine : public PricingEngine {
  public:
    FDEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps = 100,
        Size gridPoints = 100,
        bool timeDependent = false);
};

%template(FDCNEuropeanEngine) FDEuropeanEngine<CrankNicolson>;

%shared_ptr(MCEuropeanHestonEngine<PseudoRandom>);
%shared_ptr(MCEuropeanHestonEngine<LowDiscrepancy>);
template <class RNG>
class MCEuropeanHestonEngine : public PricingEngine {
    %feature("kwargs") MCEuropeanHestonEngine;

  public:
    %extend {
        MCEuropeanHestonEngine(
            const ext::shared_ptr<HestonProcess>& process,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            QL_REQUIRE(
                Size(timeSteps) != Null<Size>() || Size(timeStepsPerYear) != Null<Size>(),
                "number of steps not specified");
            return new MCEuropeanHestonEngine<RNG>(
                process,
                timeSteps,
                timeStepsPerYear,
                antitheticVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed);
        }
    }
};

%template(MCPREuropeanHestonEngine) MCEuropeanHestonEngine<PseudoRandom>;
%template(MCLDEuropeanHestonEngine) MCEuropeanHestonEngine<LowDiscrepancy>;

%pythoncode %{
def MCEuropeanHestonEngine(
        process,
        traits,
        timeSteps=None,
        timeStepsPerYear=None,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPREuropeanHestonEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDEuropeanHestonEngine
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
        seed)
%}

%shared_ptr(FDAmericanEngine<CrankNicolson>);
template <class S>
class FDAmericanEngine : public PricingEngine {
  public:
    FDAmericanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size timeSteps = 100,
        Size gridPoints = 100,
        bool timeDependent = false);
};

%template(FDCNAmericanEngine) FDAmericanEngine<CrankNicolson>;

%shared_ptr(FDShoutEngine<CrankNicolson>);
template <class S>
class FDShoutEngine : public PricingEngine {
  public:
    FDShoutEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size timeSteps = 100,
        Size gridPoints = 100,
        bool timeDependent = false);
};

%template(FDCNShoutEngine) FDShoutEngine<CrankNicolson>;

%shared_ptr(MCEuropeanGJRGARCHEngine<PseudoRandom>);
%shared_ptr(MCEuropeanGJRGARCHEngine<LowDiscrepancy>);
template <class RNG>
class MCEuropeanGJRGARCHEngine : public PricingEngine {
    %feature("kwargs") MCEuropeanGJRGARCHEngine;

  public:
    %extend {
        MCEuropeanGJRGARCHEngine(
            const ext::shared_ptr<GJRGARCHProcess>& process,
            intOrNull timeSteps = Null<Size>(),
            intOrNull timeStepsPerYear = Null<Size>(),
            bool antitheticVariate = false,
            intOrNull requiredSamples = Null<Size>(),
            doubleOrNull requiredTolerance = Null<Real>(),
            intOrNull maxSamples = Null<Size>(),
            BigInteger seed = 0) {
            QL_REQUIRE(
                Size(timeSteps) != Null<Size>() || Size(timeStepsPerYear) != Null<Size>(),
                "number of steps not specified");
            return new MCEuropeanGJRGARCHEngine<RNG>(
                process,
                timeSteps,
                timeStepsPerYear,
                antitheticVariate,
                requiredSamples,
                requiredTolerance,
                maxSamples,
                seed);
        }
    }
};

%template(MCPREuropeanGJRGARCHEngine) MCEuropeanGJRGARCHEngine<PseudoRandom>;
%template(MCLDEuropeanGJRGARCHEngine) MCEuropeanGJRGARCHEngine<LowDiscrepancy>;

%pythoncode %{
def MCEuropeanGJRGARCHEngine(
        process,
        traits,
        timeSteps=None,
        timeStepsPerYear=None,
        antitheticVariate=False,
        requiredSamples=None,
        requiredTolerance=None,
        maxSamples=None,
        seed=0):
    traits = traits.lower()
    if traits == "pr" or traits == "pseudorandom":
        cls = MCPREuropeanGJRGARCHEngine
    elif traits == "ld" or traits == "lowdiscrepancy":
        cls = MCLDEuropeanGJRGARCHEngine
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
        seed)
%}

#endif
