#ifndef ql_volatilities_i
#define ql_volatilities_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CmsMarket;
using QuantLib::CmsMarketCalibration;
using QuantLib::StrippedOptionletBase;
using QuantLib::OptionletStripper;
using QuantLib::StrippedOptionlet;
using QuantLib::OptionletStripper1;
using QuantLib::OptionletStripper2;
%}

%shared_ptr(CmsMarket)
class CmsMarket : public LazyObject {
  public:
    CmsMarket(
        std::vector<Period> swapLengths,
        std::vector<ext::shared_ptr<SwapIndex>> swapIndexes,
        ext::shared_ptr<IborIndex> iborIndex,
        const std::vector<std::vector<Handle<Quote>>>& bidAskSpreads,
        const std::vector<ext::shared_ptr<CmsCouponPricer>>& pricers,
        Handle<YieldTermStructure> discountingTS);

    void reprice(
        const Handle<SwaptionVolatilityStructure>& volStructure,
        Real meanReversion);
    const std::vector<Period>& swapTenors() const;
    const std::vector<Period>& swapLengths() const;
    const Matrix& impliedCmsSpreads();
    const Matrix& spreadErrors();
    Matrix browse() const;
    Real weightedSpreadError(const Matrix& weights);
    Real weightedSpotNpvError(const Matrix& weights);
    Real weightedFwdNpvError(const Matrix& weights);
    Array weightedSpreadErrors(const Matrix& weights);
    Array weightedSpotNpvErrors(const Matrix& weights);
    Array weightedFwdNpvErrors(const Matrix& weights);
};

class CmsMarketCalibration {
  public:
    enum CalibrationType {
        OnSpread,
        OnPrice,
        OnForwardCmsPrice
    };

    CmsMarketCalibration(
        Handle<SwaptionVolatilityStructure>& volCube,
        ext::shared_ptr<CmsMarket>& cmsMarket,
        const Matrix& weights,
        CalibrationType calibrationType);

    Array compute(
        const ext::shared_ptr<EndCriteria>& endCriteria,
        const ext::shared_ptr<OptimizationMethod>& method,
        const Array& guess,
        bool isMeanReversionFixed);
    Matrix compute(
        const ext::shared_ptr<EndCriteria>& endCriteria,
        const ext::shared_ptr<OptimizationMethod>& method,
        const Matrix& guess,
        bool isMeanReversionFixed,
        const Real meanReversionGuess = Null<Real>());
    Matrix computeParametric(
        const ext::shared_ptr<EndCriteria>& endCriteria,
        const ext::shared_ptr<OptimizationMethod>& method,
        const Matrix& guess, bool isMeanReversionFixed,
        const Real meanReversionGuess = Null<Real>());
    Real error();
    EndCriteria::Type endCriteria();
    static Real betaTransformInverse(Real beta);
    static Real betaTransformDirect(Real y);
    static Real reversionTransformInverse(Real reversion);
    static Real reversionTransformDirect(Real y);
};

%shared_ptr(StrippedOptionletBase);
class StrippedOptionletBase : public LazyObject {
  private:
    StrippedOptionletBase();
  public:
    const std::vector<Rate>& optionletStrikes(Size i);
    const std::vector<Volatility>& optionletVolatilities(Size i);
    const std::vector<Date>& optionletFixingDates();
    const std::vector<Time>& optionletFixingTimes();
    Size optionletMaturities();
    const std::vector<Rate>& atmOptionletRates();
    DayCounter dayCounter();
    Calendar calendar();
    Natural settlementDays();
    BusinessDayConvention businessDayConvention();
    VolatilityType volatilityType() const;
    Real displacement() const;
};

%shared_ptr(OptionletStripper);
class OptionletStripper : public StrippedOptionletBase {
  private:
    OptionletStripper();
  public:
    const std::vector<Period>& optionletFixingTenors() const;
    const std::vector<Date>& optionletPaymentDates() const;
    const std::vector<Time>& optionletAccrualPeriods() const;
    ext::shared_ptr<CapFloorTermVolSurface> termVolSurface() const;
    ext::shared_ptr<IborIndex> iborIndex() const;
};

%shared_ptr(StrippedOptionlet);
class StrippedOptionlet : public StrippedOptionletBase {
  public:
    StrippedOptionlet(Natural settlementDays,
                      const Calendar& calendar,
                      BusinessDayConvention bdc,
                      ext::shared_ptr<IborIndex> iborIndex,
                      const std::vector<Date>& optionletDates,
                      const std::vector<Rate>& strikes,
                      std::vector<std::vector<Handle<Quote>>>,
                      DayCounter dc,
                      VolatilityType type = ShiftedLognormal,
                      Real displacement = 0.0);
};

%shared_ptr(OptionletStripper1);
class OptionletStripper1 : public OptionletStripper {
    %feature("kwargs") OptionletStripper1;
  public:
    OptionletStripper1(
        const ext::shared_ptr<CapFloorTermVolSurface>& parVolSurface,
        const ext::shared_ptr<IborIndex>& index,
        Rate switchStrikes = Null<Rate>(),
        Real accuracy = 1.0e-6, Natural maxIter = 100,
        const Handle<YieldTermStructure>& discount = Handle<YieldTermStructure>(),
        VolatilityType type = ShiftedLognormal,
        Real displacement = 0.0,
        bool dontThrow = false);
    const Matrix& capFloorPrices() const;
    const Matrix& capletVols() const;
    const Matrix& capFloorVolatilities() const;
    const Matrix& optionletPrices() const;
    Rate switchStrike() const;
};

%shared_ptr(OptionletStripper2);
class OptionletStripper2 : public OptionletStripper {
  public:
    OptionletStripper2(
        const ext::shared_ptr<OptionletStripper1>& optionletStripper1,
        const Handle<CapFloorTermVolCurve>& atmCapFloorTermVolCurve);
    std::vector<Rate> atmCapFloorStrikes() const;
    std::vector<Real> atmCapFloorPrices() const;
    std::vector<Volatility> spreadsVol() const;
};

#endif
