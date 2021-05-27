#ifndef ql_termstructures_inflationtermstructures_all_i
#define ql_termstructures_inflationtermstructures_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/InflationTermStructure.i

%{
using QuantLib::YoYInflationTermStructure;
using QuantLib::ZeroInflationTermStructure;
using QuantLib::YoYCapFloorTermPriceSurface;
using QuantLib::InterpolatedYoYCapFloorTermPriceSurface;
using QuantLib::PiecewiseZeroInflationCurve;
using QuantLib::PiecewiseYoYInflationCurve;
using QuantLib::InterpolatedZeroInflationCurve;
using QuantLib::InterpolatedYoYInflationCurve;
%}

%shared_ptr(YoYInflationTermStructure);
class YoYInflationTermStructure : public InflationTermStructure {
  private:
    YoYInflationTermStructure();
  public:
    Rate yoyRate(const Date &d, const Period& instObsLag = Period(-1,Days),
                 bool forceLinearInterpolation = false,
                 bool extrapolate = false) const;
    Rate yoyRate(Time t,
                 bool extrapolate = false) const;
};

%template(YoYInflationTermStructureHandle) Handle<YoYInflationTermStructure>;
%template(RelinkableYoYInflationTermStructureHandle) RelinkableHandle<YoYInflationTermStructure>;

%shared_ptr(ZeroInflationTermStructure);
class ZeroInflationTermStructure : public InflationTermStructure {
  private:
    ZeroInflationTermStructure();
  public:
    Rate zeroRate(const Date &d, const Period& instObsLag = Period(-1,Days),
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
    virtual std::pair<std::vector<Time>, std::vector<Rate> > atmYoYSwapTimeRates() const;
    virtual std::pair<std::vector<Date>, std::vector<Rate> > atmYoYSwapDateRates() const;
    virtual ext::shared_ptr<YoYInflationTermStructure> YoYTS() const;
    ext::shared_ptr<YoYInflationIndex> yoyIndex();
    virtual BusinessDayConvention businessDayConvention() const;
    virtual Natural fixingDays() const;
    virtual Real price(const Date& d, Rate k);
    virtual Real capPrice(const Date& d, Rate k);
    virtual Real floorPrice(const Date& d, Rate k);
    virtual Rate atmYoYSwapRate(const Date &d,
                                bool extrapolate = true);
    virtual Rate atmYoYRate(const Date &d,
                            const Period &obsLag = Period(-1,Days),
                            bool extrapolate = true);
    virtual Real price(const Period& d, Rate k) const;
    virtual Real capPrice(const Period& d, Rate k) const;
    virtual Real floorPrice(const Period& d, Rate k) const;
    virtual Rate atmYoYSwapRate(const Period &d,
                                bool extrapolate = true) const;
    virtual Rate atmYoYRate(const Period &d,
                            const Period &obsLag = Period(-1,Days),
                            bool extrapolate = true) const;

    virtual std::vector<Rate> strikes();
    virtual std::vector<Rate> capStrikes();
    virtual std::vector<Rate> floorStrikes();
    virtual std::vector<Period> maturities();
    virtual Rate minStrike() const;
    virtual Rate maxStrike() const;
    virtual Date minMaturity() const;
    virtual Date maxMaturity() const;

    virtual Date yoyOptionDateFromTenor(const Period& p) const;
};

%define export_yoy_capfloor_termpricesurface(Name,Interpolator2D, Interpolator1D)

%{
typedef InterpolatedYoYCapFloorTermPriceSurface<Interpolator2D, Interpolator1D> Name;
%}

%shared_ptr(Name);
class Name : public YoYCapFloorTermPriceSurface {
  public:
    %extend {
        Name(Natural fixingDays,
             const Period& yyLag,    // observation lag
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

%shared_ptr(PiecewiseZeroInflationCurve<Linear>);
template <class Interpolator>
class PiecewiseZeroInflationCurve : public ZeroInflationTermStructure {
    %feature("kwargs") PiecewiseZeroInflationCurve;

  public:
    PiecewiseZeroInflationCurve(
        const Date& referenceDate,
        const Calendar& calendar,
        const DayCounter& dayCounter,
        const Period& lag,
        Frequency frequency,
        bool indexIsInterpolated,
        Rate baseRate,
        const Handle<YieldTermStructure>& nominalTS,
        const std::vector<ext::shared_ptr<BootstrapHelper<ZeroInflationTermStructure>>>& instruments,
        Real accuracy = 1.0e-12,
        const Interpolator& i = Interpolator());
    const std::vector<Date>& dates() const;
    const std::vector<Time>& times() const;

    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(PiecewiseZeroInflation) PiecewiseZeroInflationCurve<Linear>;

%shared_ptr(PiecewiseYoYInflationCurve<Linear>);
template <class Interpolator>
class PiecewiseYoYInflationCurve : public YoYInflationTermStructure {
    %feature("kwargs") PiecewiseYoYInflationCurve;
  public:
    PiecewiseYoYInflationCurve(
        const Date& referenceDate,
        const Calendar& calendar,
        const DayCounter& dayCounter,
        const Period& lag,
        Frequency frequency,
        bool indexIsInterpolated,
        Rate baseRate,
        const Handle<YieldTermStructure>& nominalTS,
        const std::vector<ext::shared_ptr<BootstrapHelper<YoYInflationTermStructure> > >& instruments,
        Real accuracy = 1.0e-12,
        const Interpolator& i = Interpolator());
    const std::vector<Date>& dates() const;
    const std::vector<Time>& times() const;

    std::vector<std::pair<Date,Real> > nodes() const;
};

%template(PiecewiseYoYInflation) PiecewiseYoYInflationCurve<Linear>;

%shared_ptr(InterpolatedZeroInflationCurve<Linear>);
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
        bool indexIsInterpolated,
        const Handle<YieldTermStructure>& yTS,
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

%shared_ptr(InterpolatedYoYInflationCurve<Linear>);
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
        const Handle<YieldTermStructure>& yTS,
        const std::vector<Date>& dates,
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