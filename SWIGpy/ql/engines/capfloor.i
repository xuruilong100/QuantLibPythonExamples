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
%}

%shared_ptr(AnalyticCapFloorEngine)
class AnalyticCapFloorEngine : public PricingEngine {
  public:
    AnalyticCapFloorEngine(
        const ext::shared_ptr<OneFactorAffineModel>& model,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
};

%shared_ptr(BlackCapFloorEngine)
class BlackCapFloorEngine : public PricingEngine {
  public:
    BlackCapFloorEngine(
        const Handle<YieldTermStructure>& termStructure,
        const Handle<Quote>& vol,
        const DayCounter& dc = Actual365Fixed(),
        Real displacement = 0.0);
    BlackCapFloorEngine(
        const Handle<YieldTermStructure>& termStructure,
        const Handle<OptionletVolatilityStructure>& vol,
        Real displacement = Null<Real>());
};

%shared_ptr(BachelierCapFloorEngine)
class BachelierCapFloorEngine : public PricingEngine {
  public:
    BachelierCapFloorEngine(
        const Handle<YieldTermStructure>& termStructure,
        const Handle<Quote>& vol);
    BachelierCapFloorEngine(
        const Handle<YieldTermStructure>& termStructure,
        const Handle<OptionletVolatilityStructure>& vol);
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

#endif
