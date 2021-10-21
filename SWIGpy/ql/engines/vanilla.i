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
using QuantLib::AnalyticPDFHestonEngine;
using QuantLib::BaroneAdesiWhaleyApproximationEngine;
using QuantLib::BatesEngine;
using QuantLib::BatesDoubleExpEngine;
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
using QuantLib::HestonExpansionEngine;
using QuantLib::IntegralEngine;
using QuantLib::JuQuadraticApproximationEngine;
using QuantLib::MCAmericanEngine;
using QuantLib::MCEuropeanEngine;
using QuantLib::MakeMCEuropeanEngine;
using QuantLib::VarianceGammaEngine;
using QuantLib::BinomialVanillaEngine;
using QuantLib::MCEuropeanHestonEngine;
using QuantLib::MCEuropeanGJRGARCHEngine;
using QuantLib::MakeMCEuropeanHestonEngine;
using QuantLib::MakeFdHestonVanillaEngine;
using QuantLib::MakeFdBlackScholesVanillaEngine;
using QuantLib::MakeMCAmericanEngine;
using QuantLib::MakeMCEuropeanGJRGARCHEngine;
using QuantLib::AnalyticHestonHullWhiteEngine;
using QuantLib::AnalyticH1HWEngine;
using QuantLib::BatesDetJumpEngine;
using QuantLib::BatesDoubleExpDetJumpEngine;
using QuantLib::JumpDiffusionEngine;
%}

%{
using QuantLib::CrankNicolson;
using QuantLib::AdditiveEQPBinomialTree;
using QuantLib::CoxRossRubinstein;
using QuantLib::JarrowRudd;
using QuantLib::Joshi4;
using QuantLib::LeisenReimer;
using QuantLib::Tian;
using QuantLib::Trigeorgis;
using QuantLib::ExtendedAdditiveEQPBinomialTree;
using QuantLib::ExtendedCoxRossRubinstein;
using QuantLib::ExtendedJarrowRudd;
using QuantLib::ExtendedJoshi4;
using QuantLib::ExtendedLeisenReimer;
using QuantLib::ExtendedTian;
using QuantLib::ExtendedTrigeorgis;
%}

%shared_ptr(AnalyticCEVEngine)
class AnalyticCEVEngine : public PricingEngine {
  public:
    AnalyticCEVEngine(
        Real f0, Real alpha, Real beta,
        Handle<YieldTermStructure> rTS);
};

%shared_ptr(BinomialVanillaEngine<AdditiveEQPBinomialTree>)
%shared_ptr(BinomialVanillaEngine<CoxRossRubinstein>)
%shared_ptr(BinomialVanillaEngine<JarrowRudd>)
%shared_ptr(BinomialVanillaEngine<Joshi4>)
%shared_ptr(BinomialVanillaEngine<LeisenReimer>)
%shared_ptr(BinomialVanillaEngine<Tian>)
%shared_ptr(BinomialVanillaEngine<Trigeorgis>)
%shared_ptr(BinomialVanillaEngine<ExtendedAdditiveEQPBinomialTree>)
%shared_ptr(BinomialVanillaEngine<ExtendedCoxRossRubinstein>)
%shared_ptr(BinomialVanillaEngine<ExtendedJarrowRudd>)
%shared_ptr(BinomialVanillaEngine<ExtendedJoshi4>)
%shared_ptr(BinomialVanillaEngine<ExtendedLeisenReimer>)
%shared_ptr(BinomialVanillaEngine<ExtendedTian>)
%shared_ptr(BinomialVanillaEngine<ExtendedTrigeorgis>)
template <class T>
class BinomialVanillaEngine : public PricingEngine {
  public:
    BinomialVanillaEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps);
};

%template(BinomialCRRVanillaEngine) BinomialVanillaEngine<CoxRossRubinstein>;
%template(BinomialEQPVanillaEngine) BinomialVanillaEngine<AdditiveEQPBinomialTree>;
%template(BinomialJ4VanillaEngine) BinomialVanillaEngine<Joshi4>;
%template(BinomialJRVanillaEngine) BinomialVanillaEngine<JarrowRudd>;
%template(BinomialLRVanillaEngine) BinomialVanillaEngine<LeisenReimer>;
%template(BinomialTianVanillaEngine) BinomialVanillaEngine<Tian>;
%template(BinomialTrigeorgisVanillaEngine) BinomialVanillaEngine<Trigeorgis>;
%template(BinomialExCRRVanillaEngine) BinomialVanillaEngine<ExtendedCoxRossRubinstein>;
%template(BinomialExEQPVanillaEngine) BinomialVanillaEngine<ExtendedAdditiveEQPBinomialTree>;
%template(BinomialExJ4VanillaEngine) BinomialVanillaEngine<ExtendedJoshi4>;
%template(BinomialExJRVanillaEngine) BinomialVanillaEngine<ExtendedJarrowRudd>;
%template(BinomialExLRVanillaEngine) BinomialVanillaEngine<ExtendedLeisenReimer>;
%template(BinomialExTianVanillaEngine) BinomialVanillaEngine<ExtendedTian>;
%template(BinomialExTrigeorgisVanillaEngine) BinomialVanillaEngine<ExtendedTrigeorgis>;

%shared_ptr(AnalyticBSMHullWhiteEngine)
class AnalyticBSMHullWhiteEngine : public PricingEngine {
  public:
    AnalyticBSMHullWhiteEngine(
        Real equityShortRateCorrelation,
        ext::shared_ptr<GeneralizedBlackScholesProcess>,
        const ext::shared_ptr<HullWhite>&);
};

%shared_ptr(AnalyticDigitalAmericanEngine)
class AnalyticDigitalAmericanEngine : public PricingEngine {
  public:
    AnalyticDigitalAmericanEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
    bool knock_in() const;
};

%shared_ptr(AnalyticDigitalAmericanKOEngine)
class AnalyticDigitalAmericanKOEngine : public PricingEngine {
  public:
    AnalyticDigitalAmericanKOEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
    bool knock_in() const;
};

%shared_ptr(AnalyticEuropeanEngine)
class AnalyticEuropeanEngine : public PricingEngine {
  public:
    AnalyticEuropeanEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
    AnalyticEuropeanEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Handle<YieldTermStructure> discountCurve);
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
      private:
        Integration();
      public:
        static Integration gaussLaguerre(Size integrationOrder = 128);
        static Integration gaussLegendre(Size integrationOrder = 128);
        static Integration gaussChebyshev(Size integrationOrder = 128);
        static Integration gaussChebyshev2nd(Size integrationOrder = 128);
        static Integration gaussLobatto(
            Real relTolerance, Real absTolerance,
            Size maxEvaluations = 1000);
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

        %extend {
            Real calculate(
                Real c_inf,
                PyObject * func,
                Real maxBound) const {
                const ext::function<Real(Real)> f = UnaryFunction(func);
                return self->calculate(c_inf, f, maxBound);
            }
            Real calculate(
                Real c_inf,
                PyObject * func,
                PyObject * maxBound) const {
                    const ext::function<Real(Real)> f = UnaryFunction(func);
                    const ext::function<Real()> m = UnaryFunction(maxBound);
                    return self->calculate(c_inf, f, m);
            }
        }

        Size numberOfEvaluations() const;
        bool isAdaptiveIntegration() const;
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
        ComplexLogFormula cpxLog,
        const AnalyticHestonEngine::Integration& itg,
        Real andersenPiterbargEpsilon = 1e-8);

    Size numberOfEvaluations() const;
    static void doCalculation(
        Real riskFreeDiscount,
        Real dividendDiscount,
        Real spotPrice,
        Real strikePrice,
        Real term,
        Real kappa,
        Real theta,
        Real sigma,
        Real v0,
        Real rho,
        const TypePayoff& type,
        const Integration& integration,
        ComplexLogFormula cpxLog,
        const AnalyticHestonEngine* enginePtr,
        Real& value,
        Size& evaluations);
    static ComplexLogFormula optimalControlVariate(
        Time t, Real v0, Real kappa, Real theta, Real sigma, Real rho);

    %extend {
        std::pair<Real, Real> chF(
            Real real, Real imag, Time t) const {
            const std::complex<Real> tmp = self->chF(
                std::complex<Real>(real, imag), t);
            return std::pair<Real, Real>(
                tmp.real(), tmp.imag());
        }
        std::pair<Real, Real> lnChF(
            Real real, Real imag, Time t) const {
            const std::complex<Real> tmp = self->lnChF(
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
    AnalyticPTDHestonEngine(
        const ext::shared_ptr<PiecewiseTimeDependentHestonModel>& model,
        Size integrationOrder = 144);
    AnalyticPTDHestonEngine(
        const ext::shared_ptr<PiecewiseTimeDependentHestonModel>& model,
        ComplexLogFormula cpxLog,
        const Integration& itg,
        Real andersenPiterbargEpsilon = 1e-8);
    Size numberOfEvaluations() const;

    %extend {
        std::pair<Real, Real> chF(
            Real real, Real imag, Time t) const {
            const std::complex<Real> tmp = self->chF(
                std::complex<Real>(real, imag), t);
            return std::pair<Real, Real>(
                tmp.real(), tmp.imag());
        }
        std::pair<Real, Real> lnChF(
            Real real, Real imag, Time t) const {
            const std::complex<Real> tmp = self->lnChF(
                std::complex<Real>(real, imag), t);
            return std::pair<Real, Real>(
                tmp.real(), tmp.imag());
        }
    }
};

%shared_ptr(AnalyticPDFHestonEngine)
class AnalyticPDFHestonEngine : public PricingEngine {
  public:
    explicit AnalyticPDFHestonEngine(
        ext::shared_ptr<HestonModel> model,
        Real gaussLobattoEps = 1e-6,
        Size gaussLobattoIntegrationOrder = 10000UL);

    Real Pv(Real x_t, Time t) const;
    Real cdf(Real X, Time t) const;
};

%shared_ptr(BaroneAdesiWhaleyApproximationEngine)
class BaroneAdesiWhaleyApproximationEngine : public PricingEngine {
  public:
    BaroneAdesiWhaleyApproximationEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(BatesEngine)
class BatesEngine : public AnalyticHestonEngine {
  public:
    BatesEngine(
        const ext::shared_ptr<BatesModel>& model,
        Size integrationOrder = 144);
    BatesEngine(
        const ext::shared_ptr<BatesModel>& model,
        Real relTolerance,
        Size maxEvaluations);
};

%shared_ptr(BatesDoubleExpEngine)
class BatesDoubleExpEngine : public AnalyticHestonEngine {
  public:
    explicit BatesDoubleExpEngine(
        const ext::shared_ptr<BatesDoubleExpModel>& model,
        Size integrationOrder = 144);
    BatesDoubleExpEngine(
        const ext::shared_ptr<BatesDoubleExpModel>& model,
        Real relTolerance, Size maxEvaluations);
};

%shared_ptr(BjerksundStenslandApproximationEngine)
class BjerksundStenslandApproximationEngine : public PricingEngine {
  public:
    BjerksundStenslandApproximationEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(COSHestonEngine)
class COSHestonEngine : public PricingEngine {
  public:
    COSHestonEngine(
        const ext::shared_ptr<HestonModel>& model,
        Real L = 16, Size N = 200);

    %extend {
        std::pair<Real, Real> chF(
            Real u, Real t) const {
            const std::complex<Real> tmp = self->chF(u, t);
            return std::pair<Real, Real>(
                tmp.real(), tmp.imag());
        }
    }

    Real c1(Time t) const;
    Real c2(Time t) const;
    Real c3(Time t) const;
    Real c4(Time t) const;

    Real mu(Time t) const;
    Real var(Time t) const;
    Real skew(Time t) const;
    Real kurtosis(Time t) const;
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
        ControlVariate cv = OptimalCV,
        Real scaling = Null<Real>());
};

%shared_ptr(FdBlackScholesVanillaEngine)
class FdBlackScholesVanillaEngine : public PricingEngine {
  public:
    enum CashDividendModel {
        Spot,
        Escrowed
    };

    FdBlackScholesVanillaEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size tGrid = 100, Size xGrid = 100, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas(),
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>(),
        CashDividendModel cashDividendModel = Spot);

    FdBlackScholesVanillaEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess>,
        ext::shared_ptr<FdmQuantoHelper> quantoHelper,
        Size tGrid = 100, Size xGrid = 100, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas(),
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>(),
        CashDividendModel cashDividendModel = Spot);
};

class MakeFdBlackScholesVanillaEngine {
  public:
    explicit MakeFdBlackScholesVanillaEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);

    MakeFdBlackScholesVanillaEngine& withQuantoHelper(
        const ext::shared_ptr<FdmQuantoHelper>& quantoHelper);
    MakeFdBlackScholesVanillaEngine& withTGrid(Size tGrid);
    MakeFdBlackScholesVanillaEngine& withXGrid(Size xGrid);
    MakeFdBlackScholesVanillaEngine& withDampingSteps(
        Size dampingSteps);
    MakeFdBlackScholesVanillaEngine& withFdmSchemeDesc(
        const FdmSchemeDesc& schemeDesc);
    MakeFdBlackScholesVanillaEngine& withLocalVol(bool localVol);
    MakeFdBlackScholesVanillaEngine& withIllegalLocalVolOverwrite(
        Real illegalLocalVolOverwrite);
    MakeFdBlackScholesVanillaEngine& withCashDividendModel(
        FdBlackScholesVanillaEngine::CashDividendModel cashDividendModel);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
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

%shared_ptr(FdCEVVanillaEngine)
class FdCEVVanillaEngine : public PricingEngine {
  public:
    FdCEVVanillaEngine(
        Real f0, Real alpha, Real beta,
        Handle<YieldTermStructure> rTS,
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
        ext::shared_ptr<LocalVolTermStructure> leverageFct = ext::shared_ptr<LocalVolTermStructure>(),
        Real mixingFactor = 1.0);

    FdHestonVanillaEngine(
        const ext::shared_ptr<HestonModel>& model,
        ext::shared_ptr<FdmQuantoHelper> quantoHelper,
        Size tGrid = 100,
        Size xGrid = 100,
        Size vGrid = 50,
        Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
        ext::shared_ptr<LocalVolTermStructure> leverageFct = ext::shared_ptr<LocalVolTermStructure>(),
        Real mixingFactor = 1.0);

        void update();
        void enableMultipleStrikesCaching(
            const std::vector<Real>& strikes);

        FdmSolverDesc getSolverDesc(
            Real equityScaleFactor) const;
};

class MakeFdHestonVanillaEngine {
  public:
    explicit MakeFdHestonVanillaEngine(
        const ext::shared_ptr<HestonModel>& hestonModel);

    MakeFdHestonVanillaEngine& withQuantoHelper(
        const ext::shared_ptr<FdmQuantoHelper>& quantoHelper);
    MakeFdHestonVanillaEngine& withTGrid(Size tGrid);
    MakeFdHestonVanillaEngine& withXGrid(Size xGrid);
    MakeFdHestonVanillaEngine& withVGrid(Size vGrid);
    MakeFdHestonVanillaEngine& withDampingSteps(
        Size dampingSteps);
    MakeFdHestonVanillaEngine& withFdmSchemeDesc(
        const FdmSchemeDesc& schemeDesc);
    MakeFdHestonVanillaEngine& withLeverageFunction(
        ext::shared_ptr<LocalVolTermStructure>& leverageFct);


    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%shared_ptr(FdSabrVanillaEngine)
class FdSabrVanillaEngine : public PricingEngine {
  public:
    FdSabrVanillaEngine(
        Real f0, Real alpha, Real beta,
        Real nu, Real rho,
        Handle<YieldTermStructure> rTS,
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
        const std::vector<ext::shared_ptr<Instrument>>& optionList);
};

%shared_ptr(FFTVanillaEngine)
class FFTVanillaEngine : public PricingEngine {
  public:
    explicit FFTVanillaEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Real logStrikeSpacing = 0.001);
    void precalculate(
        const std::vector<ext::shared_ptr<Instrument>>& optionList);
};

%shared_ptr(HestonExpansionEngine)
class HestonExpansionEngine : public PricingEngine {
  public:
    enum HestonExpansionFormula {
        LPP2, LPP3, Forde
    };
    HestonExpansionEngine(
        const ext::shared_ptr<HestonModel>& model,
        HestonExpansionFormula formula);
};

%shared_ptr(IntegralEngine)
class IntegralEngine : public PricingEngine {
  public:
    IntegralEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess>);
};

%shared_ptr(JuQuadraticApproximationEngine)
class JuQuadraticApproximationEngine : public PricingEngine {
  public:
    JuQuadraticApproximationEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(MCEuropeanEngine<PseudoRandom>)
%shared_ptr(MCEuropeanEngine<LowDiscrepancy>)
template <class RNG>
class MCEuropeanEngine : public PricingEngine {
  public:
    MCEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPREuropeanEngine) MCEuropeanEngine<PseudoRandom>;
%template(MCLDEuropeanEngine) MCEuropeanEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCEuropeanEngine {
  public:
    MakeMCEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& p);

    MakeMCEuropeanEngine& withSteps(Size steps);
    MakeMCEuropeanEngine& withStepsPerYear(Size steps);
    MakeMCEuropeanEngine& withBrownianBridge(bool b = true);
    MakeMCEuropeanEngine& withSamples(Size samples);
    MakeMCEuropeanEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCEuropeanEngine& withMaxSamples(Size samples);
    MakeMCEuropeanEngine& withSeed(BigNatural seed);
    MakeMCEuropeanEngine& withAntitheticVariate(bool b = true);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPREuropeanEngine) MakeMCEuropeanEngine<PseudoRandom>;
%template(MakeMCLDEuropeanEngine) MakeMCEuropeanEngine<LowDiscrepancy>;

%shared_ptr(MCAmericanEngine<PseudoRandom>)
%shared_ptr(MCAmericanEngine<LowDiscrepancy>)
template <class RNG>
class MCAmericanEngine : public PricingEngine {
  public:
    MCAmericanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool antitheticVariate,
        bool controlVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed,
        Size polynomOrder,
        LsmBasisSystem::PolynomType polynomType,
        Size nCalibrationSamples=Null<Size>(),
        const boost::optional<bool>& antitheticVariateCalibration=boost::none,
        BigNatural seedCalibration=Null<Size>());
};

%template(MCPRAmericanEngine) MCAmericanEngine<PseudoRandom>;
%template(MCLDAmericanEngine) MCAmericanEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCAmericanEngine {
  public:
    MakeMCAmericanEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);

    MakeMCAmericanEngine& withSteps(Size steps);
    MakeMCAmericanEngine& withStepsPerYear(Size steps);
    MakeMCAmericanEngine& withSamples(Size samples);
    MakeMCAmericanEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCAmericanEngine& withMaxSamples(Size samples);
    MakeMCAmericanEngine& withSeed(BigNatural seed);
    MakeMCAmericanEngine& withAntitheticVariate(bool b = true);
    MakeMCAmericanEngine& withControlVariate(bool b = true);
    MakeMCAmericanEngine& withPolynomOrder(Size polynomOrer);
    MakeMCAmericanEngine& withBasisSystem(LsmBasisSystem::PolynomType);
    MakeMCAmericanEngine& withCalibrationSamples(Size calibrationSamples);
    MakeMCAmericanEngine& withAntitheticVariateCalibration(bool b = true);
    MakeMCAmericanEngine& withSeedCalibration(BigNatural seed);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPRAmericanEngine) MakeMCAmericanEngine<PseudoRandom>;
%template(MakeMCLDAmericanEngine) MakeMCAmericanEngine<LowDiscrepancy>;

%shared_ptr(VarianceGammaEngine)
class VarianceGammaEngine : public PricingEngine {
  public:
    VarianceGammaEngine(
        ext::shared_ptr<VarianceGammaProcess> process,
        Real absoluteError=1e-5);
};

%shared_ptr(MCEuropeanHestonEngine<PseudoRandom>)
%shared_ptr(MCEuropeanHestonEngine<LowDiscrepancy>)
template <class RNG>
class MCEuropeanHestonEngine : public PricingEngine {
  public:
    MCEuropeanHestonEngine(
        const ext::shared_ptr<HestonProcess>& ,
        Size timeSteps,
        Size timeStepsPerYear,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPREuropeanHestonEngine) MCEuropeanHestonEngine<PseudoRandom>;
%template(MCLDEuropeanHestonEngine) MCEuropeanHestonEngine<LowDiscrepancy>;

template<class RNG = PseudoRandom,
         class S = Statistics,
         class P = HestonProcess>
class MakeMCEuropeanHestonEngine {
  public:
    explicit MakeMCEuropeanHestonEngine(
        const ext::shared_ptr<P>& process);

    MakeMCEuropeanHestonEngine& withSteps(Size steps);
    MakeMCEuropeanHestonEngine& withStepsPerYear(Size steps);
    MakeMCEuropeanHestonEngine& withSamples(Size samples);
    MakeMCEuropeanHestonEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCEuropeanHestonEngine& withMaxSamples(Size samples);
    MakeMCEuropeanHestonEngine& withSeed(BigNatural seed);
    MakeMCEuropeanHestonEngine& withAntitheticVariate(bool b = true);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPREuropeanHestonEngine) MakeMCEuropeanHestonEngine<PseudoRandom>;
%template(MakeMCLDEuropeanHestonEngine) MakeMCEuropeanHestonEngine<LowDiscrepancy>;
%template(MakeMCPREuropeanHestonSLVEngine) MakeMCEuropeanHestonEngine<PseudoRandom, GeneralStatistics, HestonSLVProcess>;
%template(MakeMCLDEuropeanHestonSLVEngine) MakeMCEuropeanHestonEngine<LowDiscrepancy, GeneralStatistics, HestonSLVProcess>;

%shared_ptr(MCEuropeanGJRGARCHEngine<PseudoRandom>)
%shared_ptr(MCEuropeanGJRGARCHEngine<LowDiscrepancy>)
template <class RNG>
class MCEuropeanGJRGARCHEngine : public PricingEngine {
  public:
    MCEuropeanGJRGARCHEngine(
        const ext::shared_ptr<GJRGARCHProcess>& ,
        Size timeSteps,
        Size timeStepsPerYear,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPREuropeanGJRGARCHEngine) MCEuropeanGJRGARCHEngine<PseudoRandom>;
%template(MCLDEuropeanGJRGARCHEngine) MCEuropeanGJRGARCHEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCEuropeanGJRGARCHEngine {
  public:
    MakeMCEuropeanGJRGARCHEngine(ext::shared_ptr<GJRGARCHProcess>);

    MakeMCEuropeanGJRGARCHEngine& withSteps(Size steps);
    MakeMCEuropeanGJRGARCHEngine& withStepsPerYear(Size steps);
    MakeMCEuropeanGJRGARCHEngine& withSamples(Size samples);
    MakeMCEuropeanGJRGARCHEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCEuropeanGJRGARCHEngine& withMaxSamples(Size samples);
    MakeMCEuropeanGJRGARCHEngine& withSeed(BigNatural seed);
    MakeMCEuropeanGJRGARCHEngine& withAntitheticVariate(bool b = true);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(* $self);
        }
    }
};

%template(MakeMCPREuropeanGJRGARCHEngine) MakeMCEuropeanGJRGARCHEngine<PseudoRandom>;
%template(MakeMCLDEuropeanGJRGARCHEngine) MakeMCEuropeanGJRGARCHEngine<LowDiscrepancy>;

%shared_ptr(AnalyticHestonHullWhiteEngine)
class AnalyticHestonHullWhiteEngine : public AnalyticHestonEngine {
  public:
    AnalyticHestonHullWhiteEngine(
        const ext::shared_ptr<HestonModel>& hestonModel,
        ext::shared_ptr<HullWhite> hullWhiteModel,
        Size integrationOrder = 144);

    AnalyticHestonHullWhiteEngine(
        const ext::shared_ptr<HestonModel>& model,
        ext::shared_ptr<HullWhite> hullWhiteModel,
        Real relTolerance,
        Size maxEvaluations);
};

%shared_ptr(AnalyticH1HWEngine)
class AnalyticH1HWEngine : public AnalyticHestonHullWhiteEngine {
  public:
    AnalyticH1HWEngine(
        const ext::shared_ptr<HestonModel>& model,
        const ext::shared_ptr<HullWhite>& hullWhiteModel,
        Real rhoSr,
        Size integrationOrder = 144);

    AnalyticH1HWEngine(
        const ext::shared_ptr<HestonModel>& model,
        const ext::shared_ptr<HullWhite>& hullWhiteModel,
        Real rhoSr,
        Real relTolerance,
        Size maxEvaluations);
};

%shared_ptr(BatesDetJumpEngine)
class BatesDetJumpEngine : public BatesEngine {
  public:
    explicit BatesDetJumpEngine(
        const ext::shared_ptr<BatesDetJumpModel>& model,
        Size integrationOrder = 144);
    BatesDetJumpEngine(
        const ext::shared_ptr<BatesDetJumpModel>& model,
        Real relTolerance, Size maxEvaluations);
};

%shared_ptr(BatesDoubleExpDetJumpEngine)
class BatesDoubleExpDetJumpEngine : public BatesDoubleExpEngine {
  public:
    explicit BatesDoubleExpDetJumpEngine(
        const ext::shared_ptr<BatesDoubleExpDetJumpModel>& model,
        Size integrationOrder = 144);
    BatesDoubleExpDetJumpEngine(
        const ext::shared_ptr<BatesDoubleExpDetJumpModel>& model,
        Real relTolerance, Size maxEvaluations);
};

%shared_ptr(JumpDiffusionEngine)
class JumpDiffusionEngine : public PricingEngine {
  public:
    JumpDiffusionEngine(
        ext::shared_ptr<Merton76Process>,
        Real relativeAccuracy_ = 1e-4,
        Size maxIterations = 100);
};

#endif
