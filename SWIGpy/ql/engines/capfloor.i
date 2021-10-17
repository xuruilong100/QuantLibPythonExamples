#ifndef ql_engines_capfloor_i
#define ql_engines_capfloor_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticCapFloorEngine;
using QuantLib::TreeCapFloorEngine;
using QuantLib::BlackCapFloorEngine;
using QuantLib::BachelierCapFloorEngine;
using QuantLib::Gaussian1dCapFloorEngine;
%}

%shared_ptr(AnalyticCapFloorEngine)
class AnalyticCapFloorEngine : public PricingEngine {
  public:
    AnalyticCapFloorEngine(
        const ext::shared_ptr<OneFactorAffineModel>& model,
        Handle<YieldTermStructure> termStructure = Handle<YieldTermStructure>());
};

%shared_ptr(BlackCapFloorEngine)
class BlackCapFloorEngine : public PricingEngine {
  public:
    BlackCapFloorEngine(
        Handle<YieldTermStructure> discountCurve,
        Volatility vol,
        const DayCounter& dc=Actual365Fixed(),
        Real displacement=0.0);
    BlackCapFloorEngine(
        Handle<YieldTermStructure> discountCurve,
        const Handle<Quote>& vol,
        const DayCounter& dc=Actual365Fixed(),
        Real displacement=0.0);
    BlackCapFloorEngine(
        Handle<YieldTermStructure> discountCurve,
        Handle<OptionletVolatilityStructure> vol,
        Real displacement=Null<Real>());
    Handle<YieldTermStructure> termStructure();
    Handle<OptionletVolatilityStructure> volatility();
    Real displacement() const;
};

%shared_ptr(BachelierCapFloorEngine)
class BachelierCapFloorEngine : public PricingEngine {
  public:
    BachelierCapFloorEngine(
        Handle<YieldTermStructure> discountCurve,
        Volatility vol,
        const DayCounter& dc=Actual365Fixed());
    BachelierCapFloorEngine(
        Handle<YieldTermStructure> discountCurve,
        const Handle<Quote>& vol,
        const DayCounter& dc=Actual365Fixed());
 	BachelierCapFloorEngine(
        Handle<YieldTermStructure> discountCurve,
        Handle<OptionletVolatilityStructure> vol);
    Handle<YieldTermStructure> termStructure();
    Handle<OptionletVolatilityStructure> volatility();
};

%shared_ptr(TreeCapFloorEngine)
class TreeCapFloorEngine : public PricingEngine {
  public:
    TreeCapFloorEngine(
        const ext::shared_ptr<ShortRateModel>& model,
        Size timeSteps,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
    TreeCapFloorEngine(
        const ext::shared_ptr<ShortRateModel>& model,
        const TimeGrid& grid,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
};

%shared_ptr(Gaussian1dCapFloorEngine)
class Gaussian1dCapFloorEngine : public PricingEngine {
  public:
    Gaussian1dCapFloorEngine(
        const ext::shared_ptr<Gaussian1dModel>& model,
        const int integrationPoints = 64,
        const Real stddevs = 7.0,
        const bool extrapolatePayoff = true,
        const bool flatPayoffExtrapolation = false,
        Handle<YieldTermStructure> discountCurve = Handle<YieldTermStructure>());
};

#endif
