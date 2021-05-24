#ifndef ql_volatilities_i
#define ql_volatilities_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::CmsMarket;
using QuantLib::CmsMarketCalibration;
using QuantLib::StrippedOptionletBase;
using QuantLib::OptionletStripper1;
%}

%shared_ptr(CmsMarket)
class CmsMarket {
  public:
    CmsMarket(
        const std::vector<Period>& swapLengths,
        const std::vector<ext::shared_ptr<SwapIndex>>& swapIndexes,
        const ext::shared_ptr<IborIndex>& iborIndex,
        const std::vector<std::vector<Handle<Quote>>>& bidAskSpreads,
        const std::vector<ext::shared_ptr<CmsCouponPricer>>& pricers,
        const Handle<YieldTermStructure>& discountingTS);

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
    Disposable<Array> weightedSpreadErrors(const Matrix& weights);
    Disposable<Array> weightedSpotNpvErrors(const Matrix& weights);
    Disposable<Array> weightedFwdNpvErrors(const Matrix& weights);
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
};

%shared_ptr(StrippedOptionletBase);
class StrippedOptionletBase {
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
};

%shared_ptr(OptionletStripper1);
class OptionletStripper1 : public StrippedOptionletBase {
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
    const Matrix& capFloorVolatilities() const;
    const Matrix& optionletPrices() const;
    Rate switchStrike() const;
};

#endif
