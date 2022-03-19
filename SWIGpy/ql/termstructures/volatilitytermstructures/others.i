#ifndef ql_termstructures_volatilitytermstructures_others_i
#define ql_termstructures_volatilitytermstructures_others_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/VolatilityTermStructure.i

%{
using QuantLib::YoYOptionletVolatilitySurface;
using QuantLib::CPIVolatilitySurface;
using QuantLib::CapFloorTermVolatilityStructure;
using QuantLib::OptionletVolatilityStructure;
%}

%{
using QuantLib::ConstantYoYOptionletVolatility;
using QuantLib::InterpolatedYoYOptionletVolatilityCurve;
using QuantLib::KInterpolatedYoYOptionletVolatilitySurface;
using QuantLib::ConstantCPIVolatility;
using QuantLib::CapFloorTermVolCurve;
using QuantLib::CapFloorTermVolSurface;
using QuantLib::ConstantOptionletVolatility;
using QuantLib::StrippedOptionletAdapter;
using QuantLib::ConstantCapFloorTermVolatility;
using QuantLib::CapletVarianceCurve;
using QuantLib::SpreadedOptionletVolatility;
using QuantLib::TenorOptionletVTS;
typedef QuantLib::TenorOptionletVTS::CorrelationStructure TenorOptionletVTSCorrelationStructure;
typedef QuantLib::TenorOptionletVTS::TwoParameterCorrelation TwoParameterCorrelation;
%}

%shared_ptr(OptionletVolatilityStructure)
class OptionletVolatilityStructure : public VolatilityTermStructure {
  private:
    OptionletVolatilityStructure();
  public:
    Volatility volatility(const Period& optionTenor,
                          Rate strike, bool extrapolate = false) const;
    Volatility volatility(const Date&, Real strike,
                          bool extrapolate = false) const;
    Volatility volatility(Time, Real strike,
                          bool extrapolate = false) const;
    Real blackVariance(const Period& optionTenor,
                       Rate strike, bool extrapolate=false) const;
    Real blackVariance(const Date&, Rate strike,
                       bool extrapolate = false) const ;
    Real blackVariance(Time, Rate strike,
                       bool extrapolate = false) const;
    ext::shared_ptr<SmileSection> smileSection(const Period& optionTenor,
                                               bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(const Date& optionDate,
                                               bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(Time optionTime,
                                               bool extr = false) const;
    VolatilityType volatilityType() const;
    Real displacement() const;
};

%template(OptionletVolatilityStructureHandle) Handle<OptionletVolatilityStructure>;
%template(RelinkableOptionletVolatilityStructureHandle) RelinkableHandle<OptionletVolatilityStructure>;

%shared_ptr(YoYOptionletVolatilitySurface)
class YoYOptionletVolatilitySurface : public VolatilityTermStructure {
  private:
    YoYOptionletVolatilitySurface();
  public:
    Volatility volatility(
        const Date& maturityDate,
        Rate strike,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = false) const;
    Volatility volatility(
        const Period& optionTenor,
        Rate strike,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = false) const;
    Volatility volatility(Time time, Rate strike) const;
    VolatilityType volatilityType() const;
    Real displacement() const;
    Volatility totalVariance(
        const Date& exerciseDate,
        Rate strike,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = false) const;
    Volatility totalVariance(
        const Period& optionTenor,
        Rate strike,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = false) const;
    Period observationLag() const;
    Frequency frequency() const;
    bool indexIsInterpolated() const;
    Date baseDate() const;
    Time timeFromBase(
        const Date& date,
        const Period& obsLag = Period(-1,Days)) const;
    Volatility baseLevel() const;
};

%template(YoYOptionletVolatilitySurfaceHandle) Handle<YoYOptionletVolatilitySurface>;
%template(RelinkableYoYOptionletVolatilitySurfaceHandle) RelinkableHandle<YoYOptionletVolatilitySurface>;


%shared_ptr(CapFloorTermVolatilityStructure)
class CapFloorTermVolatilityStructure : public VolatilityTermStructure {
  private:
    CapFloorTermVolatilityStructure();
  public:
    Volatility volatility(const Period& length, Rate strike,
                          bool extrapolate = false) const;
    Volatility volatility(const Date& end, Rate strike,
                          bool extrapolate = false) const;
    Volatility volatility(Time end, Rate strike,
                          bool extrapolate = false) const;
};

%template(CapFloorTermVolatilityStructureHandle) Handle<CapFloorTermVolatilityStructure>;
%template(RelinkableCapFloorTermVolatilityStructureHandle) RelinkableHandle<CapFloorTermVolatilityStructure>;

%shared_ptr(CapFloorTermVolCurve)
class CapFloorTermVolCurve : public CapFloorTermVolatilityStructure {
  public:
    CapFloorTermVolCurve(
        Natural settlementDays,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Handle<Quote>>& vols,
        const DayCounter& dc = Actual365Fixed());
    CapFloorTermVolCurve(
        const Date& settlementDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Handle<Quote>>& vols,
        const DayCounter& dc = Actual365Fixed());
    CapFloorTermVolCurve(
        const Date& settlementDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Volatility>& vols,
        const DayCounter& dc = Actual365Fixed());
    CapFloorTermVolCurve(
        Natural settlementDays,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Volatility>& vols,
        const DayCounter& dc = Actual365Fixed());
    const std::vector<Period>& optionTenors() const;
    const std::vector<Date>& optionDates() const;
    const std::vector<Time>& optionTimes() const;
};

%template(CapFloorTermVolCurveHandle) Handle<CapFloorTermVolCurve>;

%shared_ptr(CapFloorTermVolSurface)
class CapFloorTermVolSurface : public CapFloorTermVolatilityStructure {
  public:
    CapFloorTermVolSurface(
        Natural settlementDays,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Rate>& strikes,
        const std::vector<std::vector<Handle<Quote>>>& quotes,
        const DayCounter& dc = QuantLib::Actual365Fixed());
    CapFloorTermVolSurface(
        const Date& settlementDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Rate>& strikes,
        const std::vector<std::vector<Handle<Quote>>>& quotes,
        const DayCounter& dc = QuantLib::Actual365Fixed());
    CapFloorTermVolSurface(
        const Date& settlementDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Rate>& strikes,
        const Matrix& volatilities,
        const DayCounter& dc = QuantLib::Actual365Fixed());
    CapFloorTermVolSurface(
        Natural settlementDays,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Rate>& strikes,
        const Matrix& volatilities,
        const DayCounter& dc = QuantLib::Actual365Fixed());
    const std::vector<Period>& optionTenors() const;
    const std::vector<Date>& optionDates() const;
    const std::vector<Time>& optionTimes() const;
    const std::vector<Rate>& strikes() const;
};

%shared_ptr(ConstantOptionletVolatility)
class ConstantOptionletVolatility : public OptionletVolatilityStructure {
  public:
    ConstantOptionletVolatility(
        const Date& referenceDate,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Volatility volatility,
        const DayCounter& dayCounter,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantOptionletVolatility(
        const Date& referenceDate,
        const Calendar& cal,
        BusinessDayConvention bdc,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantOptionletVolatility(
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Volatility volatility,
        const DayCounter& dayCounter,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantOptionletVolatility(
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
};

%shared_ptr(StrippedOptionletAdapter)
class StrippedOptionletAdapter : public OptionletVolatilityStructure {
  public:
    StrippedOptionletAdapter(
        const ext::shared_ptr<StrippedOptionletBase>&);
};

%shared_ptr(ConstantYoYOptionletVolatility)
class ConstantYoYOptionletVolatility : public YoYOptionletVolatilitySurface {
  public:
    ConstantYoYOptionletVolatility(
        Volatility v,
        Natural settlementDays,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const DayCounter& dc,
        const Period& observationLag,
        Frequency frequency,
        bool indexIsInterpolated,
        Rate minStrike = -1.0,
        Rate maxStrike = 100.0,
        VolatilityType volType = ShiftedLognormal,
        Real displacement = 0.0);
    ConstantYoYOptionletVolatility(
        Handle<Quote> v,
        Natural settlementDays,
        const Calendar& ,
        BusinessDayConvention bdc,
        const DayCounter& dc,
        const Period& observationLag,
        Frequency frequency,
        bool indexIsInterpolated,
        Rate minStrike=-1.0,
        Rate maxStrike=100.0,
        VolatilityType volType=ShiftedLognormal,
        Real displacement=0.0);
};

%shared_ptr(InterpolatedYoYOptionletVolatilityCurve<Linear>)
template <class Interpolator1D>
class InterpolatedYoYOptionletVolatilityCurve : public YoYOptionletVolatilitySurface {
  public:
    InterpolatedYoYOptionletVolatilityCurve(
        Natural settlementDays,
        const Calendar&,
        BusinessDayConvention bdc,
        const DayCounter& dc,
        const Period& lag,
        Frequency frequency,
        bool indexIsInterpolated,
        const std::vector<Date>& d,
        const std::vector<Volatility>& v,
        Rate minStrike,
        Rate maxStrike,
        const Interpolator1D& i = Interpolator1D());
    const std::vector<Time>& times() const;
    const std::vector<Date>& dates() const;
    const std::vector<Real>& data() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(InterpolatedYoYInflationOptionletVolatilityCurve) InterpolatedYoYOptionletVolatilityCurve<Linear>;

%shared_ptr(KInterpolatedYoYOptionletVolatilitySurface<Linear>)
template <class Interpolator1D>
class KInterpolatedYoYOptionletVolatilitySurface : public YoYOptionletVolatilitySurface {
  public:
    KInterpolatedYoYOptionletVolatilitySurface(
        Natural settlementDays,
        const Calendar& ,
        BusinessDayConvention bdc,
        const DayCounter& dc,
        const Period& lag,
        const ext::shared_ptr<YoYCapFloorTermPriceSurface>& capFloorPrices,
        ext::shared_ptr<YoYInflationCapFloorEngine> pricer,
        ext::shared_ptr<YoYOptionletStripper> yoyOptionletStripper,
        Real slope,
        const Interpolator1D& interpolator=Interpolator1D(),
        VolatilityType volType=ShiftedLognormal,
        Real displacement=0.0);

    std::pair<std::vector<Rate>, std::vector<Volatility>> Dslice(
        const Date& d) const;
};

%template(KInterpolatedYoYInflationOptionletVolatilitySurface) KInterpolatedYoYOptionletVolatilitySurface<Linear>;

%shared_ptr(CPIVolatilitySurface)
class CPIVolatilitySurface : public VolatilityTermStructure {
  private:
    CPIVolatilitySurface();
  public:
    Volatility volatility(
        const Date& maturityDate,
        Rate strike,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = false) const;
    Volatility volatility(
        const Period& optionTenor,
        Rate strike,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = false) const;
    Volatility volatility(Time time, Rate strike) const;
    Volatility totalVariance(
        const Date& exerciseDate,
        Rate strike,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = false) const;
    Volatility totalVariance(
        const Period& optionTenor,
        Rate strike,
        const Period& obsLag = Period(-1,Days),
        bool extrapolate = false) const;
    Period observationLag() const;
    Frequency frequency() const;
    bool indexIsInterpolated() const;
    Date baseDate() const;
    Time timeFromBase(
        const Date& date,
        const Period& obsLag = Period(-1,Days)) const;
    Volatility baseLevel() const;
};

%shared_ptr(ConstantCPIVolatility)
class ConstantCPIVolatility : public CPIVolatilitySurface {
  public:
    ConstantCPIVolatility(
        Volatility v,
        Natural settlementDays,
        const Calendar&,
        BusinessDayConvention bdc,
        const DayCounter& dc,
        const Period& observationLag,
        Frequency frequency,
        bool indexIsInterpolated);
};

%shared_ptr(ConstantCapFloorTermVolatility)
class ConstantCapFloorTermVolatility : public CapFloorTermVolatilityStructure {
  public:
    ConstantCapFloorTermVolatility(
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Handle<Quote> volatility,
        const DayCounter& dc);
    ConstantCapFloorTermVolatility(
        const Date& referenceDate,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Handle<Quote> volatility,
        const DayCounter& dc);
    ConstantCapFloorTermVolatility(
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Volatility volatility,
        const DayCounter& dc);
    ConstantCapFloorTermVolatility(
        const Date& referenceDate,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Volatility volatility,
        const DayCounter& dc);
};

%shared_ptr(CapletVarianceCurve)
class CapletVarianceCurve : public OptionletVolatilityStructure {
  public:
    CapletVarianceCurve(
        const Date& referenceDate,
        const std::vector<Date>& dates,
        const std::vector<Volatility>& capletVolCurve,
        const DayCounter& dayCounter,
        VolatilityType type = ShiftedLognormal,
        Real displacement = 0.0);
};

%shared_ptr(SpreadedOptionletVolatility)
class SpreadedOptionletVolatility : public OptionletVolatilityStructure {
  public:
    SpreadedOptionletVolatility(
        const Handle<OptionletVolatilityStructure>&,
        Handle<Quote> spread);

};

%shared_ptr(TenorOptionletVTSCorrelationStructure)
class TenorOptionletVTSCorrelationStructure {
  private:
    TenorOptionletVTSCorrelationStructure();
  public:
    Real operator()(
        const Time& start1, const Time& start2) const;
};

%shared_ptr(TwoParameterCorrelation)
class TwoParameterCorrelation : public TenorOptionletVTSCorrelationStructure {
  public:
    TwoParameterCorrelation(
        ext::shared_ptr<Interpolation> rhoInf,
        ext::shared_ptr<Interpolation> beta);
};

%shared_ptr(TenorOptionletVTS)
class TenorOptionletVTS : public OptionletVolatilityStructure {
  public:
    TenorOptionletVTS(
        const Handle<OptionletVolatilityStructure>& baseVTS,
        ext::shared_ptr<IborIndex> baseIndex,
        ext::shared_ptr<IborIndex> targIndex,
        ext::shared_ptr<TenorOptionletVTSCorrelationStructure> correlation);
};

#endif
