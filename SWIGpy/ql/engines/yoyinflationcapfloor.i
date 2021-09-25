#ifndef ql_engines_yoyinflationcapfloor_i
#define ql_engines_yoyinflationcapfloor_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::YoYInflationCapFloorEngine;
using QuantLib::YoYInflationBlackCapFloorEngine;
using QuantLib::YoYInflationUnitDisplacedBlackCapFloorEngine;
using QuantLib::YoYInflationBachelierCapFloorEngine;
%}

%shared_ptr(YoYInflationCapFloorEngine)
class YoYInflationCapFloorEngine : public PricingEngine {
  private:
    YoYInflationCapFloorEngine();
  public:
    ext::shared_ptr<YoYInflationIndex> index() const;
    Handle<YoYOptionletVolatilitySurface> volatility() const;
    Handle<YieldTermStructure> nominalTermStructure() const;
    void setVolatility(const Handle<YoYOptionletVolatilitySurface>& vol);
};

%shared_ptr(YoYInflationBlackCapFloorEngine)
class YoYInflationBlackCapFloorEngine : public YoYInflationCapFloorEngine {
  public:
    YoYInflationBlackCapFloorEngine(
        const ext::shared_ptr<YoYInflationIndex>&,
        const Handle<YoYOptionletVolatilitySurface>& vol,
        const Handle<YieldTermStructure>& nominalTermStructure);
};

%shared_ptr(YoYInflationUnitDisplacedBlackCapFloorEngine)
class YoYInflationUnitDisplacedBlackCapFloorEngine : public YoYInflationCapFloorEngine {
  public:
    YoYInflationUnitDisplacedBlackCapFloorEngine(
        const ext::shared_ptr<YoYInflationIndex>&,
        const Handle<YoYOptionletVolatilitySurface>& vol,
        const Handle<YieldTermStructure>& nominalTermStructure);
};

%shared_ptr(YoYInflationBachelierCapFloorEngine)
class YoYInflationBachelierCapFloorEngine : public YoYInflationCapFloorEngine {
  public:
    YoYInflationBachelierCapFloorEngine(
        const ext::shared_ptr<YoYInflationIndex>&,
        const Handle<YoYOptionletVolatilitySurface>& vol,
        const Handle<YieldTermStructure>& nominalTermStructure);
};

#endif
