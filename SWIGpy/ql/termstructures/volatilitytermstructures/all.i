#ifndef ql_termstructures_volatilitytermstructures_all_i
#define ql_termstructures_volatilitytermstructures_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/VolatilityTermStructure.i

%{
using QuantLib::BlackVolTermStructure;
using QuantLib::LocalVolTermStructure;
using QuantLib::OptionletVolatilityStructure;
using QuantLib::YoYOptionletVolatilitySurface;
using QuantLib::SwaptionVolatilityStructure;
using QuantLib::CapFloorTermVolatilityStructure;
using QuantLib::CapFloorTermVolCurve;
using QuantLib::CapFloorTermVolSurface;
%}

%{
using QuantLib::BlackConstantVol;
using QuantLib::BlackVarianceCurve;
using QuantLib::BlackVarianceSurface;
using QuantLib::AndreasenHugeVolatilityAdapter;
using QuantLib::HestonBlackVolSurface;
%}

%{
using QuantLib::LocalConstantVol;
using QuantLib::LocalVolSurface;
using QuantLib::NoExceptLocalVolSurface;
using QuantLib::AndreasenHugeLocalVolAdapter;
%}

%{
using QuantLib::ConstantOptionletVolatility;
using QuantLib::StrippedOptionletAdapter;
using QuantLib::ConstantYoYOptionletVolatility;
using QuantLib::InterpolatedYoYOptionletVolatilityCurve;
using QuantLib::KInterpolatedYoYOptionletVolatilitySurface;
%}

%{
using QuantLib::ConstantSwaptionVolatility;
using QuantLib::SwaptionVolatilityMatrix;
using QuantLib::SwaptionVolatilityDiscrete;
using QuantLib::SwaptionVolatilityCube;
using QuantLib::SwaptionVolCube1;
using QuantLib::SwaptionVolCube2;
%}

%shared_ptr(BlackVolTermStructure);
class BlackVolTermStructure : public VolatilityTermStructure {
  private:
    BlackVolTermStructure();
  public:
    Volatility blackVol(const Date&, Real strike,
                        bool extrapolate = false) const;
    Volatility blackVol(Time, Real strike,
                        bool extrapolate = false) const;
    Real blackVariance(const Date&, Real strike,
                       bool extrapolate = false) const;
    Real blackVariance(Time, Real strike,
                       bool extrapolate = false) const;
    Volatility blackForwardVol(const Date&, const Date&,
                               Real strike, bool extrapolate = false) const;
    Volatility blackForwardVol(Time, Time, Real strike,
                               bool extrapolate = false) const;
    Real blackForwardVariance(const Date&, const Date&,
                              Real strike, bool extrapolate = false) const;
    Real blackForwardVariance(Time, Time, Real strike,
                              bool extrapolate = false) const;
};

%template(BlackVolTermStructureHandle) Handle<BlackVolTermStructure>;
%template(RelinkableBlackVolTermStructureHandle) RelinkableHandle<BlackVolTermStructure>;

%shared_ptr(LocalVolTermStructure);
class LocalVolTermStructure : public VolatilityTermStructure {
  private:
    LocalVolTermStructure();
  public:
    Volatility localVol(const Date&, Real u,
                        bool extrapolate = false) const;
    Volatility localVol(Time, Real u,
                        bool extrapolate = false) const;
};

%template(LocalVolTermStructureHandle) Handle<LocalVolTermStructure>;
%template(RelinkableLocalVolTermStructureHandle) RelinkableHandle<LocalVolTermStructure>;

%shared_ptr(OptionletVolatilityStructure);
class OptionletVolatilityStructure : public VolatilityTermStructure {
  private:
    OptionletVolatilityStructure();
  public:
    Volatility volatility(const Date&, Real strike,
                          bool extrapolate = false) const;
    Volatility volatility(Time, Real strike,
                          bool extrapolate = false) const;
    Real blackVariance(const Date&, Rate strike,
                       bool extrapolate = false) const ;
    Real blackVariance(Time, Rate strike,
                       bool extrapolate = false) const;
};

%template(OptionletVolatilityStructureHandle) Handle<OptionletVolatilityStructure>;
%template(RelinkableOptionletVolatilityStructureHandle) RelinkableHandle<OptionletVolatilityStructure>;

%shared_ptr(YoYOptionletVolatilitySurface)
class YoYOptionletVolatilitySurface : public VolatilityTermStructure {
  private:
    YoYOptionletVolatilitySurface();

  public:
    Period observationLag() const;
    Real frequency() const;
    bool indexIsInterpolated() const;
    Date baseDate() const;
    Time timeFromBase(
        const Date& date,
        const Period& obsLag = Period(-1, Days)) const;
    Real minStrike() const;
    Real maxStrike() const;
    Volatility baseLevel() const;
    Volatility volatility(
        const Date& maturityDate, Real strike,
        const Period& obsLag = Period(-1, Days),
        bool extrapolate = false) const;
    Volatility volatility(
        const Period& optionTenor, Real strike,
        const Period& obsLag = Period(-1, Days),
        bool extrapolate = false) const;
    Real totalVariance(
        const Date& exerciseDate, Rate strike,
        const Period& obsLag = Period(-1, Days),
        bool extrapolate = false) const;
    Real totalVariance(
        const Period& optionTenor, Rate strike,
        const Period& obsLag = Period(-1, Days),
        bool extrapolate = false) const;
};

%template(YoYOptionletVolatilitySurfaceHandle) Handle<YoYOptionletVolatilitySurface>;
%template(RelinkableYoYOptionletVolatilitySurface) RelinkableHandle<YoYOptionletVolatilitySurface>;

%shared_ptr(SwaptionVolatilityStructure);
class SwaptionVolatilityStructure : public VolatilityTermStructure {
  private:
    SwaptionVolatilityStructure();

  public:
    Volatility volatility(
        const Date& start, const Period& length,
        Rate strike, bool extrapolate = false) const;
    Volatility volatility(
        Time start, Time length,
        Rate strike, bool extrapolate = false) const;
    Real blackVariance(
        const Date& start, const Period& length,
        Rate strike, bool extrapolate = false) const;
    Real blackVariance(
        Time start, Time length,
        Rate strike, bool extrapolate = false) const;
    Date optionDateFromTenor(const Period& p) const;
    Real shift(
        const Period& optionTenor,
        const Period& swapTenor,
        bool extrapolate = false) const;
    Real shift(
        const Date& optionDate,
        const Period& swapTenor,
        bool extrapolate = false) const;
    Real shift(
        Time optionTime,
        const Period& swapTenor,
        bool extrapolate = false) const;
    Real shift(
        const Period& optionTenor,
        Time swapLength,
        bool extrapolate = false) const;
    Real shift(
        const Date& optionDate,
        Time swapLength,
        bool extrapolate = false) const;
    Real shift(
        Time optionTime,
        Time swapLength,
        bool extrapolate = false) const;
    ext::shared_ptr<SmileSection> smileSection(
        const Period& optionTenor,
        const Period& swapTenor,
        bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(
        const Date& optionDate,
        const Period& swapTenor,
        bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(
        Time optionTime,
        const Period& swapTenor,
        bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(
        const Period& optionTenor,
        Time swapLength,
        bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(
        const Date& optionDate,
        Time swapLength,
        bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(
        Time optionTime,
        Time swapLength,
        bool extr = false) const;
};

%template(SwaptionVolatilityStructureHandle) Handle<SwaptionVolatilityStructure>;
%template(RelinkableSwaptionVolatilityStructureHandle) RelinkableHandle<SwaptionVolatilityStructure>;

%shared_ptr(CapFloorTermVolatilityStructure);
class CapFloorTermVolatilityStructure : public VolatilityTermStructure {
  private:
    CapFloorTermVolatilityStructure();
  public:
    Volatility volatility(const Period& length, Rate strike,
                          bool extrapolate = false);
    Volatility volatility(const Date& end, Rate strike,
                          bool extrapolate = false);
    Volatility volatility(Time end, Rate strike,
                          bool extrapolate = false);
};

%template(CapFloorTermVolatilityStructureHandle) Handle<CapFloorTermVolatilityStructure>;
%template(RelinkableCapFloorTermVolatilityStructureHandle) RelinkableHandle<CapFloorTermVolatilityStructure>;

%shared_ptr(CapFloorTermVolCurve);
class CapFloorTermVolCurve : public CapFloorTermVolatilityStructure {
  public:
    CapFloorTermVolCurve(
        const Date& referenceDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& lengths,
        const std::vector<Volatility>& vols,
        const DayCounter& dc = QuantLib::Actual365Fixed());
    CapFloorTermVolCurve(
        Natural settlementDays,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& lengths,
        const std::vector<Volatility>& vols,
        const DayCounter& dc = QuantLib::Actual365Fixed());
};

%shared_ptr(CapFloorTermVolSurface);
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
    Date maxDate() const;
    Real minStrike() const;
    Real maxStrike() const;
    const std::vector<Period>& optionTenors() const;
    const std::vector<Date>& optionDates() const;
    const std::vector<Time>& optionTimes() const;
    const std::vector<Rate>& strikes() const;
};

%shared_ptr(BlackConstantVol);
class BlackConstantVol : public BlackVolTermStructure {
  public:
    BlackConstantVol(
        const Date& referenceDate,
        const Calendar& c,
        Volatility volatility,
        const DayCounter& dayCounter);
    BlackConstantVol(
        const Date& referenceDate,
        const Calendar& c,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter);
    BlackConstantVol(
        Natural settlementDays,
        const Calendar& calendar,
        Volatility volatility,
        const DayCounter& dayCounter);
    BlackConstantVol(
        Natural settlementDays,
        const Calendar& calendar,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter);
};

%shared_ptr(BlackVarianceCurve);
class BlackVarianceCurve : public BlackVolTermStructure {
  public:
    BlackVarianceCurve(
        const Date& referenceDate,
        const std::vector<Date>& dates,
        const std::vector<Real>& volatilities,
        const DayCounter& dayCounter,
        bool forceMonotoneVariance = true);
};

%shared_ptr(BlackVarianceSurface);
class BlackVarianceSurface : public BlackVolTermStructure {
    %feature("kwargs") BlackVarianceSurface;

  public:
    enum Extrapolation {
        ConstantExtrapolation,
        InterpolatorDefaultExtrapolation
    };
    %extend {
        BlackVarianceSurface(
            const Date& referenceDate,
            const Calendar& cal,
            const std::vector<Date>& dates,
            const std::vector<Real>& strikes,
            const Matrix& blackVols,
            const DayCounter& dayCounter,
            BlackVarianceSurface::Extrapolation lower =
                BlackVarianceSurface::InterpolatorDefaultExtrapolation,
            BlackVarianceSurface::Extrapolation upper =
                BlackVarianceSurface::InterpolatorDefaultExtrapolation,
            const std::string& interpolator = "") {
            BlackVarianceSurface* surface = new BlackVarianceSurface(
                referenceDate, cal,
                dates, strikes,
                blackVols, dayCounter,
                lower, upper);
            std::string s = boost::to_lower_copy(interpolator);
            if (s == "" || s == "bilinear") {
                surface->setInterpolation<QuantLib::Bilinear>();
            } else if (s == "bicubic") {
                surface->setInterpolation<QuantLib::Bicubic>();
            } else {
                QL_FAIL("Unknown interpolator: " << interpolator);
            }
            return surface;
        }
        void setInterpolation(
            const std::string& interpolator = "") {
            std::string s = boost::to_lower_copy(interpolator);
            if (s == "" || s == "bilinear") {
                self->setInterpolation<QuantLib::Bilinear>();
            } else if (s == "bicubic") {
                self->setInterpolation<QuantLib::Bicubic>();
            } else {
                QL_FAIL("Unknown interpolator: " << interpolator);
            }
        }
    }
};

%shared_ptr(AndreasenHugeVolatilityAdapter)
class AndreasenHugeVolatilityAdapter : public BlackVolTermStructure {
  public:
    AndreasenHugeVolatilityAdapter(
        const ext::shared_ptr<AndreasenHugeVolatilityInterpl>& volInterpl,
        Real eps = 1e-6);
};

%shared_ptr(HestonBlackVolSurface)
class HestonBlackVolSurface : public BlackVolTermStructure {
  public:
    HestonBlackVolSurface(
        const Handle<HestonModel>& hestonModel,
        const AnalyticHestonEngine::ComplexLogFormula cpxLogFormula = AnalyticHestonEngine::Gatheral,
        const AnalyticHestonEngine::Integration& integration = AnalyticHestonEngine::Integration::gaussLaguerre(164));
};

%shared_ptr(LocalConstantVol);
class LocalConstantVol : public LocalVolTermStructure {
  public:
    LocalConstantVol(
        const Date& referenceDate,
        Volatility volatility,
        const DayCounter& dayCounter);
    LocalConstantVol(
        const Date& referenceDate,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter);
    LocalConstantVol(
        Integer settlementDays,
        const Calendar& calendar,
        Volatility volatility,
        const DayCounter& dayCounter);
    LocalConstantVol(
        Integer settlementDays,
        const Calendar& calendar,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter);
};

%shared_ptr(LocalVolSurface);
class LocalVolSurface : public LocalVolTermStructure {
  public:
    LocalVolSurface(
        const Handle<BlackVolTermStructure>& blackTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<Quote>& underlying);
    LocalVolSurface(
        const Handle<BlackVolTermStructure>& blackTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        Real underlying);
};

%shared_ptr(NoExceptLocalVolSurface);
class NoExceptLocalVolSurface : public LocalVolSurface {
  public:
    NoExceptLocalVolSurface(
        const Handle<BlackVolTermStructure>& blackTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<Quote>& underlying,
        Real illegalLocalVolOverwrite);
    NoExceptLocalVolSurface(
        const Handle<BlackVolTermStructure>& blackTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        Real underlying,
        Real illegalLocalVolOverwrite);
};

%shared_ptr(AndreasenHugeLocalVolAdapter)
class AndreasenHugeLocalVolAdapter : public LocalVolTermStructure {
  public:
    explicit AndreasenHugeLocalVolAdapter(
        const ext::shared_ptr<AndreasenHugeVolatilityInterpl>& localVol);
};

%shared_ptr(ConstantOptionletVolatility);
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

%shared_ptr(StrippedOptionletAdapter);
class StrippedOptionletAdapter : public OptionletVolatilityStructure {
  public:
    StrippedOptionletAdapter(
        const ext::shared_ptr<StrippedOptionletBase>&);
};

%shared_ptr(ConstantYoYOptionletVolatility)
class ConstantYoYOptionletVolatility : public YoYOptionletVolatilitySurface {
  public:
    ConstantYoYOptionletVolatility(
        Volatility volatility,
        Natural settlementDays,
        const Calendar &cal,
        BusinessDayConvention bdc,
        const DayCounter& dc,
        const Period& observationLag,
        Frequency frequency,
        bool indexIsInterpolated,
        Real minStrike = -1.0,
        Real maxStrike = 100.0);
};

%shared_ptr(InterpolatedYoYOptionletVolatilityCurve<Linear>);
template <class Interpolator1D>
class InterpolatedYoYOptionletVolatilityCurve : public YoYOptionletVolatilitySurface {
  public:
    InterpolatedYoYOptionletVolatilityCurve(
        Natural settlementDays,
        const Calendar&,
        BusinessDayConvention bdc,
        const DayCounter& dc,
        const Period &lag,
        Frequency frequency,
        bool indexIsInterpolated,
        const std::vector<Date> &d,
        const std::vector<Volatility> &v,
        Rate minStrike,
        Rate maxStrike,
        const Interpolator1D &i = Interpolator1D());
};

%template(InterpolatedYoYInflationOptionletVolatilityCurve) InterpolatedYoYOptionletVolatilityCurve<Linear>;

%shared_ptr(KInterpolatedYoYOptionletVolatilitySurface<Linear>);
template <class Interpolator1D>
class KInterpolatedYoYOptionletVolatilitySurface : public YoYOptionletVolatilitySurface {
  public:
    %extend {
        KInterpolatedYoYOptionletVolatilitySurface(
            Natural settlementDays,
            const Calendar& calendar,
            BusinessDayConvention bdc,
            const DayCounter& dc,
            const Period& lag,
            const ext::shared_ptr<YoYCapFloorTermPriceSurface>& capFloorPrices,
            const ext::shared_ptr<PricingEngine>& pricer,
            const ext::shared_ptr<YoYOptionletStripper>& yoyOptionletStripper,
            Real slope,
            const Interpolator1D& interpolator = Interpolator1D()) {
            ext::shared_ptr<YoYInflationCapFloorEngine> engine = ext::dynamic_pointer_cast<YoYInflationCapFloorEngine>(pricer);
            return new KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>(
                settlementDays,
                calendar, bdc, dc,
                lag, capFloorPrices,
                engine, yoyOptionletStripper,
                slope, interpolator);
        }
    }
    std::pair<std::vector<Rate>, std::vector<Volatility>> Dslice(
        const Date& d) const;
};

%template(KInterpolatedYoYInflationOptionletVolatilitySurface) KInterpolatedYoYOptionletVolatilitySurface<Linear>;

%shared_ptr(ConstantSwaptionVolatility);
class ConstantSwaptionVolatility : public SwaptionVolatilityStructure {
  public:
    ConstantSwaptionVolatility(
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc,
        const Handle<Quote>& volatility,
        const DayCounter& dc,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantSwaptionVolatility(
        const Date& referenceDate,
        const Calendar& cal,
        BusinessDayConvention bdc,
        const Handle<Quote>& volatility,
        const DayCounter& dc,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantSwaptionVolatility(
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Volatility volatility,
        const DayCounter& dc,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantSwaptionVolatility(
        const Date& referenceDate,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Volatility volatility,
        const DayCounter& dc,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
};

%shared_ptr(SwaptionVolatilityDiscrete);
class SwaptionVolatilityDiscrete : public SwaptionVolatilityStructure {
    private:
        SwaptionVolatilityDiscrete();
    public:
        const std::vector<Period>& optionTenors() const;
        const std::vector<Date>& optionDates() const;
        const std::vector<Time>& optionTimes() const;
        const std::vector<Period>& swapTenors() const;
        const std::vector<Time>& swapLengths() const;
        const Date optionDateFromTime(Time optionTime) const;
};

%shared_ptr(SwaptionVolatilityMatrix);
class SwaptionVolatilityMatrix : public SwaptionVolatilityDiscrete {
  public:
    SwaptionVolatilityMatrix(
        const Date& referenceDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Date>& dates,
        const std::vector<Period>& lengths,
        const Matrix& vols,
        const DayCounter& dayCounter,
        const bool flatExtrapolation = false,
        const VolatilityType type = ShiftedLognormal,
        const Matrix& shifts = Matrix());
    SwaptionVolatilityMatrix(
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const std::vector<std::vector<Handle<Quote>>>& vols,
        const DayCounter& dayCounter,
        const bool flatExtrapolation = false,
        const VolatilityType type = ShiftedLognormal,
        const std::vector<std::vector<Real>>& shifts =
            std::vector<std::vector<Real>>());
    SwaptionVolatilityMatrix(
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const Matrix& vols,
        const DayCounter& dayCounter,
        const bool flatExtrapolation = false,
        const VolatilityType type = ShiftedLognormal,
        const Matrix& shifts = Matrix());
    %extend {
        SwaptionVolatilityMatrix(
            const Date& referenceDate,
            const std::vector<Date>& dates,
            const std::vector<Period>& lengths,
            const Matrix& vols,
            const DayCounter& dayCounter,
            const bool flatExtrapolation = false,
            const VolatilityType type = ShiftedLognormal,
            const Matrix& shifts = Matrix()) {
            return new SwaptionVolatilityMatrix(
                referenceDate, NullCalendar(), Following,
                dates, lengths, vols, dayCounter,
                flatExtrapolation, type, shifts);
        }
    }

    std::pair<Size, Size> locate(
        const Date& optionDate,
        const Period& swapTenor) const;
    std::pair<Size, Size> locate(
        Time optionTime,
        Time swapLength) const;
    VolatilityType volatilityType() const;
};

%shared_ptr(SwaptionVolatilityCube);
class SwaptionVolatilityCube : public SwaptionVolatilityDiscrete {
    private:
        SwaptionVolatilityCube();
    public:
        Rate atmStrike(
            const Date& optionDate,
            const Period& swapTenor) const;
};

%shared_ptr(SwaptionVolCube1);
class SwaptionVolCube1 : public SwaptionVolatilityCube {
  public:
    SwaptionVolCube1(
        const Handle<SwaptionVolatilityStructure>& atmVolStructure,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const std::vector<Spread>& strikeSpreads,
        const std::vector<std::vector<Handle<Quote>>>& volSpreads,
        const ext::shared_ptr<SwapIndex>& swapIndex,
        const ext::shared_ptr<SwapIndex>& shortSwapIndex,
        bool vegaWeightedSmileFit,
        const std::vector<std::vector<Handle<Quote>>>& parametersGuess,
        const std::vector<bool>& isParameterFixed,
        bool isAtmCalibrated,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        Real maxErrorTolerance = Null<Real>(),
        const ext::shared_ptr<OptimizationMethod>& optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = Null<Real>(),
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const bool backwardFlat = false,
        const Real cutoffStrike = 0.0001);
    Matrix sparseSabrParameters() const;
    Matrix denseSabrParameters() const;
    Matrix marketVolCube() const;
    Matrix volCubeAtmCalibrated() const;
    %extend {
        ext::shared_ptr<SabrSmileSection> smileSection(
            Time optionTime,
            Time swapLength,
            bool extr = false) {
            SwaptionVolatilityStructure* base = dynamic_cast<SwaptionVolatilityStructure*>($self);
            return ext::dynamic_pointer_cast<SabrSmileSection>(
                base->smileSection(optionTime, swapLength, extr));
        }
        ext::shared_ptr<SabrSmileSection> smileSection(
            const Period& optionTenor,
            const Period& swapTenor,
            bool extr = false) {
            SwaptionVolatilityStructure* base = dynamic_cast<SwaptionVolatilityStructure*>($self);
            return ext::dynamic_pointer_cast<SabrSmileSection>(
                base->smileSection(optionTenor, swapTenor, extr));
        }
    }
};

%shared_ptr(SwaptionVolCube2);
class SwaptionVolCube2 : public SwaptionVolatilityCube {
  public:
    SwaptionVolCube2(
        const Handle<SwaptionVolatilityStructure>& atmVolStructure,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const std::vector<Spread>& strikeSpreads,
        const std::vector<std::vector<Handle<Quote> > >& volSpreads,
        const ext::shared_ptr<SwapIndex>& swapIndex,
        const ext::shared_ptr<SwapIndex>& shortSwapIndex,
        bool vegaWeightedSmileFit);
};

#endif
