#ifndef ql_cashflows_floatingratecouponpricers_all_i
#define ql_cashflows_floatingratecouponpricers_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/cashflows/FloatingRateCouponPricer.i

%{
using QuantLib::GFunctionFactory;
using QuantLib::CmsCouponPricer;
using QuantLib::CmsSpreadCouponPricer;
using QuantLib::IborCouponPricer;
using QuantLib::AnalyticHaganPricer;
using QuantLib::NumericHaganPricer;
using QuantLib::LinearTsrPricer;
using QuantLib::LognormalCmsSpreadPricer;
using QuantLib::BlackIborCouponPricer;
%}

class GFunctionFactory {
  private:
    GFunctionFactory();

  public:
    enum YieldCurveModel {
        Standard,
        ExactYield,
        ParallelShifts,
        NonParallelShifts
    };
};

%shared_ptr(CmsCouponPricer)
class CmsCouponPricer : public FloatingRateCouponPricer {
  private:
    CmsCouponPricer();

  public:
    Handle<SwaptionVolatilityStructure> swaptionVolatility() const;
    void setSwaptionVolatility(
        const Handle<SwaptionVolatilityStructure>& v = Handle<SwaptionVolatilityStructure>());
};

%template(CmsCouponPricerVector) std::vector<ext::shared_ptr<CmsCouponPricer> >;

%shared_ptr(CmsSpreadCouponPricer)
class CmsSpreadCouponPricer : public FloatingRateCouponPricer {
  private:
    CmsSpreadCouponPricer();
  public:
    Handle<Quote> correlation() const;
    void setCorrelation(
        const Handle<Quote> &correlation = Handle<Quote>());
};

%shared_ptr(IborCouponPricer)
class IborCouponPricer : public FloatingRateCouponPricer {
  private:
    IborCouponPricer();
  public:
    Handle<OptionletVolatilityStructure> capletVolatility() const;
    void setCapletVolatility(
        const Handle<OptionletVolatilityStructure>& v = Handle<OptionletVolatilityStructure>());
};

%shared_ptr(AnalyticHaganPricer)
class AnalyticHaganPricer : public CmsCouponPricer {
  public:
    AnalyticHaganPricer(const Handle<SwaptionVolatilityStructure>& v,
                        GFunctionFactory::YieldCurveModel model,
                        const Handle<Quote>& meanReversion);
};

%shared_ptr(NumericHaganPricer)
class NumericHaganPricer : public CmsCouponPricer {
  public:
    NumericHaganPricer(const Handle<SwaptionVolatilityStructure>& v,
                       GFunctionFactory::YieldCurveModel model,
                       const Handle<Quote>& meanReversion,
                       Rate lowerLimit = 0.0,
                       Rate upperLimit = 1.0,
                       Real precision = 1.0e-6);
};

%rename (LinearTsrPricerSettings) LinearTsrPricer::Settings;
%feature ("flatnested") Settings;
%shared_ptr(LinearTsrPricer)
class LinearTsrPricer : public CmsCouponPricer {
  public:
    struct Settings {

        Settings();
        Settings &withRateBound(const Real lowerRateBound = 0.0001,
                                const Real upperRateBound = 2.0000);
        Settings &withVegaRatio(const Real vegaRatio = 0.01);
        Settings &withVegaRatio(const Real vegaRatio,
                                const Real lowerRateBound,
                                const Real upperRateBound);
        Settings &withPriceThreshold(const Real priceThreshold = 1.0E-8);
        Settings &withPriceThreshold(const Real priceThreshold,
                                     const Real lowerRateBound,
                                     const Real upperRateBound);
        Settings &withBSStdDevs(const Real stdDevs = 3.0);
        Settings &withBSStdDevs(const Real stdDevs,
                                const Real lowerRateBound,
                                const Real upperRateBound);
        enum Strategy {
            RateBound,
            VegaRatio,
            PriceThreshold,
            BSStdDevs
        };
    };

    LinearTsrPricer(
        const Handle<SwaptionVolatilityStructure> &swaptionVol,
        const Handle<Quote> &meanReversion,
        const Handle<YieldTermStructure> &couponDiscountCurve = Handle<YieldTermStructure>(),
        const LinearTsrPricer::Settings &settings = LinearTsrPricer::Settings());
};

%shared_ptr(LognormalCmsSpreadPricer)
class LognormalCmsSpreadPricer : public CmsSpreadCouponPricer {
  public:
    LognormalCmsSpreadPricer(
        const ext::shared_ptr<CmsCouponPricer>& cmsPricer,
        const Handle<Quote> &correlation,
        const Handle<YieldTermStructure> &couponDiscountCurve = Handle<YieldTermStructure>(),
        const Size IntegrationPoints = 16,
        const boost::optional<VolatilityType> volatilityType = boost::none,
        const Real shift1 = Null<Real>(), const Real shift2 = Null<Real>());
    Real swapletPrice() const;
    Rate swapletRate() const;
    Real capletPrice(Rate effectiveCap) const;
    Rate capletRate(Rate effectiveCap) const;
    Real floorletPrice(Rate effectiveFloor) const;
    Rate floorletRate(Rate effectiveFloor) const;
};

%shared_ptr(BlackIborCouponPricer)
class BlackIborCouponPricer : public IborCouponPricer {
  public:
    enum TimingAdjustment {
        Black76, BivariateLognormal };
    BlackIborCouponPricer(
        const Handle<OptionletVolatilityStructure>& v =
        Handle<OptionletVolatilityStructure>(),
        const TimingAdjustment timingAdjustment = Black76,
        const Handle<Quote> correlation =
        Handle<Quote>(ext::shared_ptr<Quote>(new SimpleQuote(1.0))));
};

#endif
