#ifndef ql_termstructures_inflationtermstructures_all_i
#define ql_termstructures_inflationtermstructures_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/InflationTermStructure.i
%include ../ql/indexes/all.i

%{
using QuantLib::CPICapFloorTermPriceSurface;
using QuantLib::InterpolatedCPICapFloorTermPriceSurface;
using QuantLib::YoYInflationTermStructure;
using QuantLib::ZeroInflationTermStructure;
using QuantLib::YoYCapFloorTermPriceSurface;
using QuantLib::InterpolatedYoYCapFloorTermPriceSurface;
using QuantLib::PiecewiseZeroInflationCurve;
using QuantLib::PiecewiseYoYInflationCurve;
using QuantLib::InterpolatedZeroInflationCurve;
using QuantLib::InterpolatedYoYInflationCurve;
%}

%shared_ptr(CPICapFloorTermPriceSurface)
class CPICapFloorTermPriceSurface : public InflationTermStructure {
  private:
    CPICapFloorTermPriceSurface();
  public:
    Handle<ZeroInflationIndex> zeroInflationIndex() const;
    Real nominal() const;
    BusinessDayConvention businessDayConvention() const;
    Real price(const Period& d, Rate k) const;
    Real capPrice(const Period& d, Rate k) const;
    Real floorPrice(const Period& d, Rate k) const;
    Real price(const Date& d, Rate k) const;
    Real capPrice(const Date& d, Rate k) const;
    Real floorPrice(const Date& d, Rate k) const;
    std::vector<Rate> strikes() const;
    std::vector<Rate> capStrikes() const;
    std::vector<Rate> floorStrikes() const;
    std::vector<Period> maturities() const;
    const Matrix& capPrices() const;
    const Matrix& floorPrices() const;
    Rate minStrike() const;
    Rate maxStrike() const;
    Date minDate() const;
    Date cpiOptionDateFromTenor(const Period& p) const;
};

%template(CPICapFloorTermPriceSurfaceHandle) Handle<CPICapFloorTermPriceSurface>;
%template(RelinkableCPICapFloorTermPriceSurfaceHandle) RelinkableHandle<CPICapFloorTermPriceSurface>;

%shared_ptr(InterpolatedCPICapFloorTermPriceSurface<Bilinear>)
template<class Interpolator2D>
class InterpolatedCPICapFloorTermPriceSurface : public CPICapFloorTermPriceSurface {
  public:
    InterpolatedCPICapFloorTermPriceSurface(
        Real nominal,
        Rate startRate,
        const Period& observationLag,
        const Calendar& cal,
        const BusinessDayConvention& bdc,
        const DayCounter& dc,
        const Handle<ZeroInflationIndex>& zii,
        const Handle<YieldTermStructure>& yts,
        const std::vector<Rate> &cStrikes,
        const std::vector<Rate> &fStrikes,
        const std::vector<Period> &cfMaturities,
        const Matrix& cPrice,
        const Matrix& fPrice,
        const Interpolator2D &interpolator2d = Interpolator2D());
        void performCalculations() const;
};

%template(CPICapFloorSurface) InterpolatedCPICapFloorTermPriceSurface<Bilinear>;

%shared_ptr(YoYInflationTermStructure)
class YoYInflationTermStructure : public InflationTermStructure {
  private:
    YoYInflationTermStructure();
  public:
    Rate yoyRate(const Date& d, const Period& instObsLag = Period(-1,Days),
                 bool forceLinearInterpolation = false,
                 bool extrapolate = false) const;
    Rate yoyRate(Time t,
                 bool extrapolate = false) const;
};

%template(YoYInflationTermStructureHandle) Handle<YoYInflationTermStructure>;
%template(RelinkableYoYInflationTermStructureHandle) RelinkableHandle<YoYInflationTermStructure>;

%shared_ptr(ZeroInflationTermStructure)
class ZeroInflationTermStructure : public InflationTermStructure {
  private:
    ZeroInflationTermStructure();
  public:
    Rate zeroRate(const Date& d, const Period& instObsLag = Period(-1,Days),
                  bool forceLinearInterpolation = false,
                  bool extrapolate = false) const;
    Rate zeroRate(Time t,
                  bool extrapolate = false) const;
};

%template(ZeroInflationTermStructureHandle) Handle<ZeroInflationTermStructure>;
%template(RelinkableZeroInflationTermStructureHandle) RelinkableHandle<ZeroInflationTermStructure>;

%shared_ptr(YoYCapFloorTermPriceSurface)
class YoYCapFloorTermPriceSurface : public InflationTermStructure {
  private:
    YoYCapFloorTermPriceSurface();
  public:
    std::pair<std::vector<Time>, std::vector<Rate>> atmYoYSwapTimeRates() const;
    std::pair<std::vector<Date>, std::vector<Rate>> atmYoYSwapDateRates() const;
    ext::shared_ptr<YoYInflationTermStructure> YoYTS() const;
    ext::shared_ptr<YoYInflationIndex> yoyIndex();
    BusinessDayConvention businessDayConvention() const;
    Natural fixingDays() const;
    Real price(const Date& d, Rate k);
    Real capPrice(const Date& d, Rate k);
    Real floorPrice(const Date& d, Rate k);
    Rate atmYoYSwapRate(
        const Date& d, bool extrapolate = true);
    Rate atmYoYRate(
        const Date& d,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = true);
    Real price(const Period& d, Rate k) const;
    Real capPrice(const Period& d, Rate k) const;
    Real floorPrice(const Period& d, Rate k) const;
    Rate atmYoYSwapRate(
        const Period& d,
        bool extrapolate = true) const;
    Rate atmYoYRate(
        const Period& d,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = true) const;
    std::vector<Rate> strikes();
    std::vector<Rate> capStrikes();
    std::vector<Rate> floorStrikes();
    std::vector<Period> maturities();
    Rate minStrike() const;
    Rate maxStrike() const;
    Date minMaturity() const;
    Date maxMaturity() const;
    Date yoyOptionDateFromTenor(const Period& p) const;
};

%define export_yoy_capfloor_termpricesurface(Name,Interpolator2D, Interpolator1D)

%{
typedef InterpolatedYoYCapFloorTermPriceSurface<Interpolator2D, Interpolator1D> Name;
%}

%shared_ptr(Name)
class Name : public YoYCapFloorTermPriceSurface {
  public:
    %extend {
        Name(Natural fixingDays,
             const Period& yyLag,
             const ext::shared_ptr<YoYInflationIndex>& yii,
             Rate baseRate,
             const Handle<YieldTermStructure>& nominal,
             const DayCounter& dc,
             const Calendar& cal,
             const BusinessDayConvention& bdc,
             const std::vector<Rate>& cStrikes,
             const std::vector<Rate>& fStrikes,
             const std::vector<Period>& cfMaturities,
             const Matrix& cPrice,
             const Matrix& fPrice,
             const Interpolator2D& interpolator2d = Interpolator2D(),
             const Interpolator1D& interpolator1d = Interpolator1D()) {
            return new Name(
                fixingDays, yyLag, yii,
                baseRate, nominal,
                dc, cal, bdc, cStrikes,
                fStrikes, cfMaturities,
                cPrice, fPrice);
        }
    }
};

%enddef

export_yoy_capfloor_termpricesurface(YoYInflationCapFloorTermPriceSurface,Bicubic,Cubic);

%shared_ptr(PiecewiseZeroInflationCurve<Linear>)
template <class Interpolator>
class PiecewiseZeroInflationCurve : public ZeroInflationTermStructure, public LazyObject {
    %feature("kwargs") PiecewiseZeroInflationCurve;
  public:
    PiecewiseZeroInflationCurve(
        const Date& referenceDate,
        const Calendar& calendar,
        const DayCounter& dayCounter,
        const Period& lag,
        Frequency frequency,
        Rate baseZeroRate,
        const std::vector<ext::shared_ptr<BootstrapHelper<ZeroInflationTermStructure>>>& instruments,
        Real accuracy = 1.0e-12,
        const Interpolator& i = Interpolator());
    const std::vector<Time>& times() const;
    const std::vector<Date>& dates() const;
    const std::vector<Real>& data() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(PiecewiseZeroInflation) PiecewiseZeroInflationCurve<Linear>;

%shared_ptr(PiecewiseYoYInflationCurve<Linear>)
template <class Interpolator>
class PiecewiseYoYInflationCurve : public YoYInflationTermStructure, public LazyObject {
    %feature("kwargs") PiecewiseYoYInflationCurve;
  public:
    PiecewiseYoYInflationCurve(
        const Date& referenceDate,
        const Calendar& calendar,
        const DayCounter& dayCounter,
        const Period& lag,
        Frequency frequency,
        bool indexIsInterpolated,
        Rate baseYoYRate,
        const std::vector<ext::shared_ptr<BootstrapHelper<YoYInflationTermStructure>>>& instruments,
        Real accuracy = 1.0e-12,
        const Interpolator& i = Interpolator());
    const std::vector<Time>& times() const;
    const std::vector<Date>& dates() const;
    const std::vector<Real>& data() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(PiecewiseYoYInflation) PiecewiseYoYInflationCurve<Linear>;

%shared_ptr(InterpolatedZeroInflationCurve<Linear>)
template <class Interpolator>
class InterpolatedZeroInflationCurve : public ZeroInflationTermStructure {
    %feature("kwargs") InterpolatedZeroInflationCurve;

  public:
    InterpolatedZeroInflationCurve(
        const Date& referenceDate,
        const Calendar& calendar,
        const DayCounter& dayCounter,
        const Period& lag,
        Frequency frequency,
        const std::vector<Date>& dates,
        const std::vector<Rate>& rates,
        const Interpolator& interpolator = Interpolator());

    const std::vector<Date>& dates() const;
    const std::vector<Time>& times() const;
    const std::vector<Real>& data() const;
    const std::vector<Rate>& rates() const;
    std::vector<std::pair<Date, Rate>> nodes() const;
};

%template(ZeroInflationCurve) InterpolatedZeroInflationCurve<Linear>;

%shared_ptr(InterpolatedYoYInflationCurve<Linear>)
template <class Interpolator>
class InterpolatedYoYInflationCurve : public YoYInflationTermStructure {
    %feature("kwargs") InterpolatedYoYInflationCurve;

  public:
    InterpolatedYoYInflationCurve(
        const Date& referenceDate,
        const Calendar& calendar,
        const DayCounter& dayCounter,
        const Period& lag,
        Frequency frequency,
        bool indexIsInterpolated,
        std::vector<Date> dates,
        const std::vector<Rate>& rates,
        const Interpolator& interpolator = Interpolator());
    const std::vector<Date>& dates() const;
    const std::vector<Time>& times() const;
    const std::vector<Real>& data() const;
    const std::vector<Rate>& rates() const;
    std::vector<std::pair<Date, Rate>> nodes() const;
};

%template(YoYInflationCurve) InterpolatedYoYInflationCurve<Linear>;

#endif
