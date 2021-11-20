#ifndef ql_engines_barrier_i
#define ql_engines_barrier_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticBarrierEngine;
using QuantLib::AnalyticBinaryBarrierEngine;
using QuantLib::AnalyticDoubleBarrierEngine;
using QuantLib::MCBarrierEngine;
using QuantLib::FdBlackScholesBarrierEngine;
using QuantLib::FdBlackScholesRebateEngine;
using QuantLib::FdHestonBarrierEngine;
using QuantLib::FdHestonRebateEngine;
using QuantLib::BinomialBarrierEngine;
using QuantLib::VannaVolgaBarrierEngine;
using QuantLib::FdHestonDoubleBarrierEngine;
using QuantLib::WulinYongDoubleBarrierEngine;
using QuantLib::VannaVolgaDoubleBarrierEngine;
using QuantLib::AnalyticDoubleBarrierBinaryEngine;
using QuantLib::BinomialDoubleBarrierEngine;
using QuantLib::MakeMCBarrierEngine;
using QuantLib::PerturbativeBarrierOptionEngine;
using QuantLib::MCDoubleBarrierEngine;
using QuantLib::MakeMCDoubleBarrierEngine;
using QuantLib::AnalyticPartialTimeBarrierOptionEngine;
using QuantLib::AnalyticTwoAssetBarrierEngine;
%}

%{
using QuantLib::DiscretizedBarrierOption;
using QuantLib::DiscretizedDoubleBarrierOption;
using QuantLib::DiscretizedDermanKaniBarrierOption;
using QuantLib::DiscretizedDermanKaniDoubleBarrierOption;
%}

%shared_ptr(AnalyticBarrierEngine)
class AnalyticBarrierEngine : public PricingEngine {
  public:
    AnalyticBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticBinaryBarrierEngine)
class AnalyticBinaryBarrierEngine : public PricingEngine {
  public:
    AnalyticBinaryBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(MCBarrierEngine<PseudoRandom>)
%shared_ptr(MCBarrierEngine<LowDiscrepancy>)
template <class RNG>
class MCBarrierEngine : public PricingEngine {
  public:
    MCBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        bool isBiased,
        BigNatural seed);
};

%template(MCPRBarrierEngine) MCBarrierEngine<PseudoRandom>;
%template(MCLDBarrierEngine) MCBarrierEngine<LowDiscrepancy>;

template <class RNG>
class MakeMCBarrierEngine {
  public:
    MakeMCBarrierEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);

    MakeMCBarrierEngine& withSteps(Size steps);
    MakeMCBarrierEngine& withStepsPerYear(Size steps);
    MakeMCBarrierEngine& withBrownianBridge(bool b = true);
    MakeMCBarrierEngine& withAntitheticVariate(bool b = true);
    MakeMCBarrierEngine& withSamples(Size samples);
    MakeMCBarrierEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCBarrierEngine& withMaxSamples(Size samples);
    MakeMCBarrierEngine& withBias(bool b = true);
    MakeMCBarrierEngine& withSeed(BigNatural seed);

    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(*self);
        }
    }
};

%template(MakeMCPRBarrierEngine) MakeMCBarrierEngine<PseudoRandom>;
%template(MakeMCLDBarrierEngine) MakeMCBarrierEngine<LowDiscrepancy>;

%shared_ptr(FdBlackScholesBarrierEngine)
class FdBlackScholesBarrierEngine : public PricingEngine {
  public:
    FdBlackScholesBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size tGrid = 100,
        Size xGrid = 100,
        Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas(),
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>());
};

%shared_ptr(FdBlackScholesRebateEngine)
class FdBlackScholesRebateEngine : public PricingEngine {
  public:
    FdBlackScholesRebateEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size tGrid = 100, Size xGrid = 100, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas(),
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>());
};

%shared_ptr(FdHestonBarrierEngine)
class FdHestonBarrierEngine : public PricingEngine {
  public:
    FdHestonBarrierEngine(
        const ext::shared_ptr<HestonModel>& model,
        Size tGrid = 100, Size xGrid = 100, Size vGrid = 50, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
        const ext::shared_ptr<LocalVolTermStructure>& leverageFct = ext::shared_ptr<LocalVolTermStructure>(),
        const Real mixingFactor = 1.0);
};

%shared_ptr(FdHestonRebateEngine)
class FdHestonRebateEngine : public PricingEngine {
  public:
    FdHestonRebateEngine(
        const ext::shared_ptr<HestonModel>& model,
        Size tGrid = 100, Size xGrid = 100, Size vGrid = 50, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
        const ext::shared_ptr<LocalVolTermStructure>& leverageFct = ext::shared_ptr<LocalVolTermStructure>(),
        const Real mixingFactor = 1.0);
};

%feature("docstring") BinomialBarrierEngine "Binomial Engine for barrier options.
Features different binomial models, selected by the type parameters.
Uses Boyle-Lau adjustment for optimize steps and Derman-Kani optimization to speed
up convergence.
Type values:
    crr or coxrossrubinstein:        Cox-Ross-Rubinstein model
    jr  or jarrowrudd:               Jarrow-Rudd model
    eqp or additiveeqpbinomialtree:  Additive EQP model
    trigeorgis:                      Trigeorgis model
    tian:                            Tian model
    lr  or leisenreimer              Leisen-Reimer model
    j4  or joshi4:                   Joshi 4th (smoothed) model

Boyle-Lau adjustment is controlled by parameter max_steps.
If max_steps is equal to steps Boyle-Lau is disabled.
Il max_steps is 0 (default value), max_steps is calculated by capping it to
5*steps when Boyle-Lau would need more than 1000 steps.
If max_steps is specified, it would limit binomial steps to this value.
"

%shared_ptr(BinomialBarrierEngine<CoxRossRubinstein, DiscretizedBarrierOption>)
%shared_ptr(BinomialBarrierEngine<JarrowRudd, DiscretizedBarrierOption>)
%shared_ptr(BinomialBarrierEngine<AdditiveEQPBinomialTree, DiscretizedBarrierOption>)
%shared_ptr(BinomialBarrierEngine<Trigeorgis, DiscretizedBarrierOption>)
%shared_ptr(BinomialBarrierEngine<Tian, DiscretizedBarrierOption>)
%shared_ptr(BinomialBarrierEngine<LeisenReimer, DiscretizedBarrierOption>)
%shared_ptr(BinomialBarrierEngine<Joshi4, DiscretizedBarrierOption>)
%shared_ptr(BinomialBarrierEngine<CoxRossRubinstein, DiscretizedDermanKaniBarrierOption>)
%shared_ptr(BinomialBarrierEngine<JarrowRudd, DiscretizedDermanKaniBarrierOption>)
%shared_ptr(BinomialBarrierEngine<AdditiveEQPBinomialTree, DiscretizedDermanKaniBarrierOption>)
%shared_ptr(BinomialBarrierEngine<Trigeorgis, DiscretizedDermanKaniBarrierOption>)
%shared_ptr(BinomialBarrierEngine<Tian, DiscretizedDermanKaniBarrierOption>)
%shared_ptr(BinomialBarrierEngine<LeisenReimer, DiscretizedDermanKaniBarrierOption>)
%shared_ptr(BinomialBarrierEngine<Joshi4, DiscretizedDermanKaniBarrierOption>)
template <class T, class U>
class BinomialBarrierEngine : public PricingEngine {
  public:
    BinomialBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size steps,
        Size max_steps = 0);
};

%template(BinomialCRRBarrierEngine) BinomialBarrierEngine<CoxRossRubinstein, DiscretizedBarrierOption>;
%template(BinomialJRBarrierEngine) BinomialBarrierEngine<JarrowRudd, DiscretizedBarrierOption>;
%template(BinomialEQPBarrierEngine) BinomialBarrierEngine<AdditiveEQPBinomialTree, DiscretizedBarrierOption>;
%template(BinomialTrigeorgisBarrierEngine) BinomialBarrierEngine<Trigeorgis, DiscretizedBarrierOption>;
%template(BinomialTianBarrierEngine) BinomialBarrierEngine<Tian, DiscretizedBarrierOption>;
%template(BinomialLRBarrierEngine) BinomialBarrierEngine<LeisenReimer, DiscretizedBarrierOption>;
%template(BinomialJ4BarrierEngine) BinomialBarrierEngine<Joshi4, DiscretizedBarrierOption>;
%template(BinomialCRRDKBarrierEngine) BinomialBarrierEngine<CoxRossRubinstein, DiscretizedDermanKaniBarrierOption>;
%template(BinomialJRDKBarrierEngine) BinomialBarrierEngine<JarrowRudd, DiscretizedDermanKaniBarrierOption>;
%template(BinomialEQPDKBarrierEngine) BinomialBarrierEngine<AdditiveEQPBinomialTree, DiscretizedDermanKaniBarrierOption>;
%template(BinomialTrigeorgisDKBarrierEngine) BinomialBarrierEngine<Trigeorgis, DiscretizedDermanKaniBarrierOption>;
%template(BinomialTianDKBarrierEngine) BinomialBarrierEngine<Tian, DiscretizedDermanKaniBarrierOption>;
%template(BinomialLRDKBarrierEngine) BinomialBarrierEngine<LeisenReimer, DiscretizedDermanKaniBarrierOption>;
%template(BinomialJ4DKBarrierEngine) BinomialBarrierEngine<Joshi4, DiscretizedDermanKaniBarrierOption>;

%shared_ptr(VannaVolgaBarrierEngine)
class VannaVolgaBarrierEngine : public PricingEngine {
  public:
    VannaVolgaBarrierEngine(
        Handle<DeltaVolQuote> atmVol,
        Handle<DeltaVolQuote> vol25Put,
        Handle<DeltaVolQuote> vol25Call,
        Handle<Quote> spotFX,
        Handle<YieldTermStructure> domesticTS,
        Handle<YieldTermStructure> foreignTS,
        bool adaptVanDelta = false,
        Real bsPriceWithSmile = 0.0);
};

%feature("docstring") AnalyticDoubleBarrierEngine "
Double barrier engine implementing Ikeda-Kunitomo series."

%shared_ptr(AnalyticDoubleBarrierEngine)
class AnalyticDoubleBarrierEngine : public PricingEngine {
  public:
    AnalyticDoubleBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        int series = 5);
};

%shared_ptr(FdHestonDoubleBarrierEngine)
class FdHestonDoubleBarrierEngine : public PricingEngine {
  public:
    FdHestonDoubleBarrierEngine(
        const ext::shared_ptr<HestonModel>& model,
        Size tGrid = 100, Size xGrid = 100,
        Size vGrid = 50, Size dampingSteps = 0,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
        ext::shared_ptr<LocalVolTermStructure> leverageFct = ext::shared_ptr<LocalVolTermStructure>(),
        Real mixingFactor = 1.0);
};

%shared_ptr(WulinYongDoubleBarrierEngine)
class WulinYongDoubleBarrierEngine : public PricingEngine {
  public:
    WulinYongDoubleBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        int series = 5);
};

%feature("docstring") VannaVolgaDoubleBarrierEngine "
Vanna-Volga engine for double barrier options.
Supports different double barrier engines, selected by the type parameters.
Type values:
    ik or analytic:  Ikeda-Kunitomo standard engine (default)
    wo:              Wulin-Yong engine
"

%shared_ptr(VannaVolgaDoubleBarrierEngine<AnalyticDoubleBarrierEngine>)
%shared_ptr(VannaVolgaDoubleBarrierEngine<WulinYongDoubleBarrierEngine>)
template <class E>
class VannaVolgaDoubleBarrierEngine : public PricingEngine {
  public:
    VannaVolgaDoubleBarrierEngine(
        Handle<DeltaVolQuote> atmVol,
        Handle<DeltaVolQuote> vol25Put,
        Handle<DeltaVolQuote> vol25Call,
        Handle<Quote> spotFX,
        Handle<YieldTermStructure> domesticTS,
        Handle<YieldTermStructure> foreignTS,
        const bool adaptVanDelta = false,
        const Real bsPriceWithSmile = 0.0,
        int series = 5);
};

%template(VannaVolgaIKDoubleBarrierEngine) VannaVolgaDoubleBarrierEngine<AnalyticDoubleBarrierEngine>;
%template(VannaVolgaWYDoubleBarrierEngine) VannaVolgaDoubleBarrierEngine<WulinYongDoubleBarrierEngine>;

%shared_ptr(AnalyticDoubleBarrierBinaryEngine)
class AnalyticDoubleBarrierBinaryEngine : public PricingEngine {
  public:
    AnalyticDoubleBarrierBinaryEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%feature("docstring") BinomialDoubleBarrierEngine "Binomial Engine for double barrier options.
Features different binomial models, selected by the type parameters.
Uses Derman-Kani optimization to speed up convergence.
Type values:
    crr or coxrossrubinstein:        Cox-Ross-Rubinstein model
    jr  or jarrowrudd:               Jarrow-Rudd model
    eqp or additiveeqpbinomialtree:  Additive EQP model
    trigeorgis:                      Trigeorgis model
    tian:                            Tian model
    lr  or leisenreimer              Leisen-Reimer model
    j4  or joshi4:                   Joshi 4th (smoothed) model
"
%shared_ptr(BinomialDoubleBarrierEngine<CoxRossRubinstein, DiscretizedDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<JarrowRudd, DiscretizedDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<AdditiveEQPBinomialTree, DiscretizedDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<Trigeorgis, DiscretizedDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<Tian, DiscretizedDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<LeisenReimer, DiscretizedDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<Joshi4, DiscretizedDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<CoxRossRubinstein, DiscretizedDermanKaniDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<JarrowRudd, DiscretizedDermanKaniDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<AdditiveEQPBinomialTree, DiscretizedDermanKaniDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<Trigeorgis, DiscretizedDermanKaniDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<Tian, DiscretizedDermanKaniDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<LeisenReimer, DiscretizedDermanKaniDoubleBarrierOption>)
%shared_ptr(BinomialDoubleBarrierEngine<Joshi4, DiscretizedDermanKaniDoubleBarrierOption>)
template <class T, class U>
class BinomialDoubleBarrierEngine : public PricingEngine {
  public:
    BinomialDoubleBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size steps);
};

%template(BinomialCRRDoubleBarrierEngine) BinomialDoubleBarrierEngine<CoxRossRubinstein, DiscretizedDoubleBarrierOption>;
%template(BinomialJRDoubleBarrierEngine) BinomialDoubleBarrierEngine<JarrowRudd, DiscretizedDoubleBarrierOption>;
%template(BinomialEQPDoubleBarrierEngine) BinomialDoubleBarrierEngine<AdditiveEQPBinomialTree, DiscretizedDoubleBarrierOption>;
%template(BinomialTrigeorgisDoubleBarrierEngine) BinomialDoubleBarrierEngine<Trigeorgis, DiscretizedDoubleBarrierOption>;
%template(BinomialTianDoubleBarrierEngine) BinomialDoubleBarrierEngine<Tian, DiscretizedDoubleBarrierOption>;
%template(BinomialLRDoubleBarrierEngine) BinomialDoubleBarrierEngine<LeisenReimer, DiscretizedDoubleBarrierOption>;
%template(BinomialJ4DoubleBarrierEngine) BinomialDoubleBarrierEngine<Joshi4, DiscretizedDoubleBarrierOption>;
%template(BinomialCRRDKDoubleBarrierEngine) BinomialDoubleBarrierEngine<CoxRossRubinstein, DiscretizedDermanKaniDoubleBarrierOption>;
%template(BinomialJRDKDoubleBarrierEngine) BinomialDoubleBarrierEngine<JarrowRudd, DiscretizedDermanKaniDoubleBarrierOption>;
%template(BinomialEQPDKDoubleBarrierEngine) BinomialDoubleBarrierEngine<AdditiveEQPBinomialTree, DiscretizedDermanKaniDoubleBarrierOption>;
%template(BinomialTrigeorgisDKDoubleBarrierEngine) BinomialDoubleBarrierEngine<Trigeorgis, DiscretizedDermanKaniDoubleBarrierOption>;
%template(BinomialTianDKDoubleBarrierEngine) BinomialDoubleBarrierEngine<Tian, DiscretizedDermanKaniDoubleBarrierOption>;
%template(BinomialLRDKDoubleBarrierEngine) BinomialDoubleBarrierEngine<LeisenReimer, DiscretizedDermanKaniDoubleBarrierOption>;
%template(BinomialJ4DKDoubleBarrierEngine) BinomialDoubleBarrierEngine<Joshi4, DiscretizedDermanKaniDoubleBarrierOption>;

%shared_ptr(PerturbativeBarrierOptionEngine)
class PerturbativeBarrierOptionEngine : public PricingEngine {
  public:
    explicit PerturbativeBarrierOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Natural order = 1,
        bool zeroGamma = false);
};

%shared_ptr(MCDoubleBarrierEngine<PseudoRandom>)
%shared_ptr(MCDoubleBarrierEngine<LowDiscrepancy>)
template <class RNG>
class MCDoubleBarrierEngine : public PricingEngine {
  public:
    MCDoubleBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antithetic,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRDoubleBarrierEngine) MCDoubleBarrierEngine<PseudoRandom>;
%template(MCLDDoubleBarrierEngine) MCDoubleBarrierEngine<LowDiscrepancy>;

%shared_ptr(MakeMCDoubleBarrierEngine<PseudoRandom>)
%shared_ptr(MakeMCDoubleBarrierEngine<LowDiscrepancy>)
template <class RNG>
class MakeMCDoubleBarrierEngine {
  public:
    explicit MakeMCDoubleBarrierEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);
    // named parameters
    MakeMCDoubleBarrierEngine& withSteps(Size steps);
    MakeMCDoubleBarrierEngine& withStepsPerYear(Size steps);
    MakeMCDoubleBarrierEngine& withBrownianBridge(bool b = true);
    MakeMCDoubleBarrierEngine& withAntitheticVariate(bool b = true);
    MakeMCDoubleBarrierEngine& withSamples(Size samples);
    MakeMCDoubleBarrierEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCDoubleBarrierEngine& withMaxSamples(Size samples);
    MakeMCDoubleBarrierEngine& withSeed(BigNatural seed);
    // conversion to pricing engine
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(*self);
        }
    }
};

%template(MakeMCPRDoubleBarrierEngine) MakeMCDoubleBarrierEngine<PseudoRandom>;
%template(MakeMCLDDoubleBarrierEngine) MakeMCDoubleBarrierEngine<LowDiscrepancy>;

%shared_ptr(AnalyticPartialTimeBarrierOptionEngine)
class AnalyticPartialTimeBarrierOptionEngine : public PricingEngine {
  public:
    explicit AnalyticPartialTimeBarrierOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticTwoAssetBarrierEngine)
class AnalyticTwoAssetBarrierEngine : public PricingEngine {
  public:
    AnalyticTwoAssetBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process1,
        ext::shared_ptr<GeneralizedBlackScholesProcess> process2,
        Handle<Quote> rho);
};

#endif
