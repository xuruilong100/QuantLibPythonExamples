#ifndef ql_engines_swaption_i
#define ql_engines_swaption_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::BlackSwaptionEngine;
using QuantLib::BachelierSwaptionEngine;
using QuantLib::JamshidianSwaptionEngine;
using QuantLib::TreeSwaptionEngine;
using QuantLib::G2SwaptionEngine;
using QuantLib::FdG2SwaptionEngine;
using QuantLib::FdHullWhiteSwaptionEngine;
using QuantLib::Gaussian1dSwaptionEngine;
using QuantLib::Gaussian1dJamshidianSwaptionEngine;
using QuantLib::Gaussian1dNonstandardSwaptionEngine;
using QuantLib::Gaussian1dFloatFloatSwaptionEngine;
%}

%shared_ptr(BlackSwaptionEngine)
class BlackSwaptionEngine : public PricingEngine {
  public:
    BlackSwaptionEngine(const Handle<YieldTermStructure> & discountCurve,
                        const Handle<Quote>& vol,
                        const DayCounter& dc = Actual365Fixed(),
                        Real displacement = 0.0);
    BlackSwaptionEngine(const Handle<YieldTermStructure> & discountCurve,
                        const Handle<SwaptionVolatilityStructure>& v);
};

%shared_ptr(BachelierSwaptionEngine)
class BachelierSwaptionEngine : public PricingEngine {
  public:
    BachelierSwaptionEngine(const Handle<YieldTermStructure> & discountCurve,
                            const Handle<Quote>& vol,
                            const DayCounter& dc = Actual365Fixed());
    BachelierSwaptionEngine(const Handle<YieldTermStructure> & discountCurve,
                            const Handle<SwaptionVolatilityStructure>& v);
};

%shared_ptr(JamshidianSwaptionEngine)
class JamshidianSwaptionEngine : public PricingEngine {
  public:
    JamshidianSwaptionEngine(
        const ext::shared_ptr<OneFactorAffineModel>& model,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
};

%shared_ptr(TreeSwaptionEngine)
class TreeSwaptionEngine : public PricingEngine {
  public:
    TreeSwaptionEngine(
        const ext::shared_ptr<ShortRateModel>& model,
        Size timeSteps,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
    TreeSwaptionEngine(
        const ext::shared_ptr<ShortRateModel>& model,
        const TimeGrid& grid,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
    TreeSwaptionEngine(
        const Handle<ShortRateModel>& model,
        Size timeSteps,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
};

%shared_ptr(G2SwaptionEngine)
class G2SwaptionEngine : public PricingEngine {
  public:
    G2SwaptionEngine(const ext::shared_ptr<G2>& model,
                     Real range, Size intervals);
};

%shared_ptr(FdG2SwaptionEngine)
class FdG2SwaptionEngine : public PricingEngine {
  public:
    FdG2SwaptionEngine(const ext::shared_ptr<G2>& model,
                       Size tGrid = 100, Size xGrid = 50, Size yGrid = 50,
                       Size dampingSteps = 0, Real invEps = 1e-5,
                       const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer());
};

%shared_ptr(FdHullWhiteSwaptionEngine)
class FdHullWhiteSwaptionEngine : public PricingEngine {
  public:
    FdHullWhiteSwaptionEngine(const ext::shared_ptr<HullWhite>& model,
                              Size tGrid = 100, Size xGrid = 100,
                              Size dampingSteps = 0, Real invEps = 1e-5,
                              const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas());
};

%shared_ptr(Gaussian1dSwaptionEngine)
class Gaussian1dSwaptionEngine : public PricingEngine {
    %rename(NoProb) None;

  public:
    enum Probabilities {
        None,
        Naive,
        Digital
    };
    Gaussian1dSwaptionEngine(
        const ext::shared_ptr<Gaussian1dModel>& model,
        const int integrationPoints = 64, const Real stddevs = 7.0,
        const bool extrapolatePayoff = true,
        const bool flatPayoffExtrapolation = false,
        const Handle<YieldTermStructure>& discountCurve = Handle<YieldTermStructure>(),
        const Gaussian1dSwaptionEngine::Probabilities probabilities = Gaussian1dSwaptionEngine::None);
    Gaussian1dSwaptionEngine(
        const Handle<Gaussian1dModel> &model,
        const int integrationPoints = 64, const Real stddevs = 7.0,
        const bool extrapolatePayoff = true,
        const bool flatPayoffExtrapolation = false,
        const Handle<YieldTermStructure>& discountCurve = Handle<YieldTermStructure>(),
        const Gaussian1dSwaptionEngine::Probabilities probabilities = Gaussian1dSwaptionEngine::None);
};

%shared_ptr(Gaussian1dJamshidianSwaptionEngine)
class Gaussian1dJamshidianSwaptionEngine : public PricingEngine {
  public:
    Gaussian1dJamshidianSwaptionEngine(
        const ext::shared_ptr<Gaussian1dModel>& model);
};

%shared_ptr(Gaussian1dNonstandardSwaptionEngine)
class Gaussian1dNonstandardSwaptionEngine : public PricingEngine {
    %rename(NoProb) None;

  public:
    enum Probabilities {
        None,
        Naive,
        Digital
    };
    Gaussian1dNonstandardSwaptionEngine(
        const ext::shared_ptr<Gaussian1dModel>& model,
        const int integrationPoints = 64, const Real stddevs = 7.0,
        const bool extrapolatePayoff = true,
        const bool flatPayoffExtrapolation = false,
        const Handle<Quote>& oas = Handle<Quote>(),
        const Handle<YieldTermStructure>& discountCurve = Handle<YieldTermStructure>(),
        const Gaussian1dNonstandardSwaptionEngine::Probabilities probabilities = Gaussian1dNonstandardSwaptionEngine::None);
    Gaussian1dNonstandardSwaptionEngine(
        const Handle<Gaussian1dModel> &model,
        const int integrationPoints = 64, const Real stddevs = 7.0,
        const bool extrapolatePayoff = true,
        const bool flatPayoffExtrapolation = false,
        const Handle<Quote>& oas = Handle<Quote>(),
        const Handle<YieldTermStructure>& discountCurve = Handle<YieldTermStructure>(),
        const Gaussian1dNonstandardSwaptionEngine::Probabilities probabilities = Gaussian1dNonstandardSwaptionEngine::None);
};

%shared_ptr(Gaussian1dFloatFloatSwaptionEngine)
class Gaussian1dFloatFloatSwaptionEngine : public PricingEngine {
    %rename(NoProb) None;

  public:
    enum Probabilities {
        None,
        Naive,
        Digital
    };
    Gaussian1dFloatFloatSwaptionEngine(
        const ext::shared_ptr<Gaussian1dModel>& model,
        const int integrationPoints = 64,
        const Real stddevs = 7.0,
        const bool extrapolatePayoff = true,
        const bool flatPayoffExtrapolation = false,
        const Handle<Quote>& oas = Handle<Quote>(),
        const Handle<YieldTermStructure>& discountCurve = Handle<YieldTermStructure>(),
        const bool includeTodaysExercise = false,
        const Gaussian1dFloatFloatSwaptionEngine::Probabilities probabilities =
        Gaussian1dFloatFloatSwaptionEngine::None);
    Gaussian1dFloatFloatSwaptionEngine(
        const Handle<Gaussian1dModel> &model,
        const int integrationPoints = 64,
        const Real stddevs = 7.0,
        const bool extrapolatePayoff = true,
        const bool flatPayoffExtrapolation = false,
        const Handle<Quote> &oas = Handle<Quote>(),
        const Handle<YieldTermStructure> &discountCurve = Handle<YieldTermStructure>(),
        const bool includeTodaysExercise = false,
        const Gaussian1dFloatFloatSwaptionEngine::Probabilities probabilities =
        Gaussian1dFloatFloatSwaptionEngine::None);
    Handle<YieldTermStructure> discountingCurve() const;
};

#endif
