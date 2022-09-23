#ifndef ql_cashflows_inflationcouponpricers_all_i
#define ql_cashflows_inflationcouponpricers_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::YoYInflationCouponPricer;
using QuantLib::CPICouponPricer;
using QuantLib::BachelierYoYInflationCouponPricer;
using QuantLib::BlackYoYInflationCouponPricer;
using QuantLib::UnitDisplacedBlackYoYInflationCouponPricer;
%}

%shared_ptr(CPICouponPricer)
class CPICouponPricer : public InflationCouponPricer {
  public:
    CPICouponPricer();
    CPICouponPricer(Handle<YieldTermStructure> nominalTermStructure);
    CPICouponPricer(
        Handle<CPIVolatilitySurface> capletVol,
        Handle<YieldTermStructure> nominalTermStructure);

    Handle<CPIVolatilitySurface> capletVolatility() const;
    Handle<YieldTermStructure> nominalTermStructure() const;
    void setCapletVolatility(
        const Handle<CPIVolatilitySurface>& capletVol);
};

%shared_ptr(YoYInflationCouponPricer)
class YoYInflationCouponPricer : public InflationCouponPricer {
  public:
    YoYInflationCouponPricer();
    YoYInflationCouponPricer(Handle<YieldTermStructure> nominalTermStructure);
    YoYInflationCouponPricer(
        Handle<YoYOptionletVolatilitySurface> capletVol,
        Handle<YieldTermStructure> nominalTermStructure);

    Handle<YoYOptionletVolatilitySurface> capletVolatility() const;
    Handle<YieldTermStructure> nominalTermStructure() const;
    void setCapletVolatility(
        const Handle<YoYOptionletVolatilitySurface>& capletVol);
};

%shared_ptr(BlackYoYInflationCouponPricer)
class BlackYoYInflationCouponPricer : public YoYInflationCouponPricer {
  public:
    BlackYoYInflationCouponPricer();
    BlackYoYInflationCouponPricer(
        const Handle<YieldTermStructure>& nominalTermStructure);
    BlackYoYInflationCouponPricer(
        const Handle<YoYOptionletVolatilitySurface>& capletVol,
        const Handle<YieldTermStructure>& nominalTermStructure);
};

%shared_ptr(UnitDisplacedBlackYoYInflationCouponPricer)
class UnitDisplacedBlackYoYInflationCouponPricer : public YoYInflationCouponPricer {
  public:
    UnitDisplacedBlackYoYInflationCouponPricer();
    UnitDisplacedBlackYoYInflationCouponPricer(
        const Handle<YieldTermStructure>& nominalTermStructure);
    UnitDisplacedBlackYoYInflationCouponPricer(
        const Handle<YoYOptionletVolatilitySurface>& capletVol,
        const Handle<YieldTermStructure>& nominalTermStructure);
};

%shared_ptr(BachelierYoYInflationCouponPricer)
class BachelierYoYInflationCouponPricer : public YoYInflationCouponPricer {
  public:
    BachelierYoYInflationCouponPricer();
    BachelierYoYInflationCouponPricer(
        const Handle<YieldTermStructure>& nominalTermStructure);
    BachelierYoYInflationCouponPricer(
        const Handle<YoYOptionletVolatilitySurface>& capletVol,
        const Handle<YieldTermStructure>& nominalTermStructure);
};

#endif
