#ifndef ql_termstructures_yieldtermstructures_all_i
#define ql_termstructures_yieldtermstructures_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/YieldTermStructure.i

%{
using QuantLib::Discount;
using QuantLib::ZeroYield;
using QuantLib::ForwardRate;
%}

struct Discount {};
struct ZeroYield {};
struct ForwardRate {};

%{
using QuantLib::ImpliedTermStructure;
using QuantLib::ForwardSpreadedTermStructure;
using QuantLib::ZeroSpreadedTermStructure;
using QuantLib::InterpolatedPiecewiseZeroSpreadedTermStructure;
using QuantLib::FlatForward;
using QuantLib::UltimateForwardTermStructure;
using QuantLib::CompositeZeroYieldStructure;
using QuantLib::PiecewiseYieldCurve;
using QuantLib::SimpleZeroYield;
using QuantLib::InterpolatedDiscountCurve;
using QuantLib::FittedBondDiscountCurve;
using QuantLib::InterpolatedZeroCurve;
using QuantLib::InterpolatedForwardCurve;
typedef PiecewiseYieldCurve<SimpleZeroYield, Linear, QuantLib::GlobalBootstrap> GlobalLinearSimpleZeroCurve;
//typedef ext::shared_ptr<YieldTermStructure> FittedBondDiscountCurvePtr;
%}

%shared_ptr(ImpliedTermStructure)
class ImpliedTermStructure : public YieldTermStructure {
  public:
    ImpliedTermStructure(
        Handle<YieldTermStructure> curveHandle,
        const Date& referenceDate);
};

%shared_ptr(ZeroSpreadedTermStructure)
class ZeroSpreadedTermStructure : public YieldTermStructure {
  public:
    ZeroSpreadedTermStructure(
        Handle<YieldTermStructure> curveHandle,
        Handle<Quote> spreadHandle,
        Compounding comp = QuantLib::Continuous,
        Frequency freq = QuantLib::NoFrequency,
        DayCounter dc = DayCounter());
};

%shared_ptr(ForwardSpreadedTermStructure)
class ForwardSpreadedTermStructure : public YieldTermStructure {
  public:
    ForwardSpreadedTermStructure(
        Handle<YieldTermStructure> curveHandle,
        Handle<Quote> spreadHandle);
};

%shared_ptr(InterpolatedPiecewiseZeroSpreadedTermStructure<Linear>);
%shared_ptr(InterpolatedPiecewiseZeroSpreadedTermStructure<BackwardFlat>);
template <class Interpolator>
class InterpolatedPiecewiseZeroSpreadedTermStructure : public YieldTermStructure {
  public:
    InterpolatedPiecewiseZeroSpreadedTermStructure(
        Handle<YieldTermStructure> curveHandle,
        std::vector<Handle<Quote>> spreadHandles,
        const std::vector<Date>& dates,
        Compounding comp = QuantLib::Continuous,
        Frequency freq = QuantLib::NoFrequency,
        const DayCounter& dc = DayCounter(),
        const Interpolator& factory = Interpolator());
};

%template(SpreadedLinearZeroInterpolatedTermStructure) InterpolatedPiecewiseZeroSpreadedTermStructure<Linear>;
%template(SpreadedBackwardFlatZeroInterpolatedTermStructure) InterpolatedPiecewiseZeroSpreadedTermStructure<BackwardFlat>;

%shared_ptr(FlatForward)
class FlatForward : public YieldTermStructure {
  public:
    FlatForward(
        const Date& referenceDate,
        Handle<Quote> forward,
        const DayCounter& dayCounter,
        Compounding compounding = QuantLib::Continuous,
        Frequency frequency = QuantLib::Annual);
    FlatForward(
        const Date& referenceDate,
        Rate forward,
        const DayCounter& dayCounter,
        Compounding compounding = QuantLib::Continuous,
        Frequency frequency = QuantLib::Annual);
    FlatForward(
        Integer settlementDays,
        const Calendar& calendar,
        Handle<Quote> forward,
        const DayCounter& dayCounter,
        Compounding compounding = QuantLib::Continuous,
        Frequency frequency = QuantLib::Annual);
    FlatForward(
        Integer settlementDays,
        const Calendar& calendar,
        Rate forward,
        const DayCounter& dayCounter,
        Compounding compounding = QuantLib::Continuous,
        Frequency frequency = QuantLib::Annual);
    Compounding compounding() const;
    Frequency compoundingFrequency() const;
};

%shared_ptr(UltimateForwardTermStructure)
class UltimateForwardTermStructure : public YieldTermStructure {
  public:
    UltimateForwardTermStructure(
        Handle<YieldTermStructure> curveHandle,
        Handle<Quote> lastLiquidForwardRate,
        Handle<Quote> ultimateForwardRate,
        const Period& firstSmoothingPoint,
        Real alpha);
};

%shared_ptr(CompositeZeroYieldStructure<BinaryFunction>);
template <class F>
class CompositeZeroYieldStructure : public YieldTermStructure {
  public:
    %extend {
        CompositeZeroYieldStructure(
            const Handle<YieldTermStructure>& h1,
            const Handle<YieldTermStructure>& h2,
            PyObject* function,
            Compounding comp = QuantLib::Continuous,
            Frequency freq = QuantLib::NoFrequency) {
            return new CompositeZeroYieldStructure<F>(
                h1, h2, F(function), comp, freq);
        }
    }
};

%template(CompositeBFZeroYieldStructure) CompositeZeroYieldStructure<BinaryFunction>;

%define export_piecewise_curve(Name,Traits,Interpolator)
%{
typedef PiecewiseYieldCurve<Traits, Interpolator> Name;
%}

%shared_ptr(Name)
class Name : public YieldTermStructure {
  public:
    %extend {
        Name(
            const Date& referenceDate,
            const std::vector<ext::shared_ptr<RateHelper>>& instruments,
            const DayCounter& dayCounter,
            const std::vector<Handle<Quote>>& jumps=std::vector<Handle<Quote>>(),
            const std::vector<Date>& jumpDates=std::vector<Date>(),
            const Interpolator& i=Interpolator(),
            const IterativeBootstrap& b = IterativeBootstrap()) {
                return new Name(
                    referenceDate,
                    instruments,
                    dayCounter,
                    jumps,
                    jumpDates,
                    i,
                    Name::bootstrap_type(
                        b.accuracy, b.minValue, b.maxValue,
                        b.maxAttempts, b.maxFactor, b.minFactor,
                        b.dontThrow, b.dontThrowSteps));
            }
     	Name(
            const Date& referenceDate,
            const std::vector<ext::shared_ptr<RateHelper>>& instruments,
            const DayCounter& dayCounter,
            const Interpolator& i,
            const IterativeBootstrap& b = IterativeBootstrap()) {
                return new Name(
                    referenceDate,
                    instruments,
                    dayCounter,
                    i,
                    Name::bootstrap_type(
                        b.accuracy, b.minValue, b.maxValue,
                        b.maxAttempts, b.maxFactor, b.minFactor,
                        b.dontThrow, b.dontThrowSteps));
            }
     	Name(
            const Date& referenceDate,
            const std::vector<ext::shared_ptr<RateHelper>>& instruments,
            const DayCounter& dayCounter,
            const IterativeBootstrap& b) {
                return new Name(
                    referenceDate,
                    instruments,
                    dayCounter,
                    Name::bootstrap_type(
                        b.accuracy, b.minValue, b.maxValue,
                        b.maxAttempts, b.maxFactor, b.minFactor,
                        b.dontThrow, b.dontThrowSteps));
            }
     	Name(
            Natural settlementDays,
            const Calendar& calendar,
            const std::vector<ext::shared_ptr<RateHelper>>& instruments,
            const DayCounter& dayCounter,
            const std::vector<Handle<Quote>>& jumps=std::vector<Handle<Quote>>(),
            const std::vector<Date>& jumpDates=std::vector<Date>(),
            const Interpolator& i=Interpolator(),
            const IterativeBootstrap& b = IterativeBootstrap()) {
                return new Name(
                    settlementDays,
                    calendar,
                    instruments,
                    dayCounter,
                    jumps,
                    jumpDates,
                    i,
                    Name::bootstrap_type(
                        b.accuracy, b.minValue, b.maxValue,
                        b.maxAttempts, b.maxFactor, b.minFactor,
                        b.dontThrow, b.dontThrowSteps));
            }
     	Name(
            Natural settlementDays,
            const Calendar& calendar,
            const std::vector<ext::shared_ptr<RateHelper>>& instruments,
            const DayCounter& dayCounter,
            const Interpolator& i,
            const IterativeBootstrap& b = IterativeBootstrap()) {
                return new Name(
                    settlementDays,
                    calendar,
                    instruments,
                    dayCounter,
                    i,
                    Name::bootstrap_type(
                        b.accuracy, b.minValue, b.maxValue,
                        b.maxAttempts, b.maxFactor, b.minFactor,
                        b.dontThrow, b.dontThrowSteps));
            }
     	Name(
            Natural settlementDays,
            const Calendar& calendar,
            const std::vector<ext::shared_ptr<RateHelper>>& instruments,
            const DayCounter& dayCounter,
            const IterativeBootstrap& b) {
                return new Name(
                    settlementDays,
                    calendar,
                    instruments,
                    dayCounter,
                    Name::bootstrap_type(
                        b.accuracy, b.minValue, b.maxValue,
                        b.maxAttempts, b.maxFactor, b.minFactor,
                        b.dontThrow, b.dontThrowSteps));
            }
    }
    const std::vector<Date>& dates() const;
    const std::vector<Time>& times() const;
    const std::vector<Real>& data() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%enddef

// ForwardRate
export_piecewise_curve(PiecewiseLinearFlatForward,          ForwardRate,    LinearFlat);
export_piecewise_curve(PiecewiseBackwardFlatForward,        ForwardRate,    BackwardFlat);
export_piecewise_curve(PiecewiseConvexMonotoneForward,      ForwardRate,    ConvexMonotone);
export_piecewise_curve(PiecewiseCubicForward,               ForwardRate,    Cubic);
export_piecewise_curve(PiecewiseForwardFlatForward,         ForwardRate,    ForwardFlat);
export_piecewise_curve(PiecewiseLinearForward,              ForwardRate,    Linear);
export_piecewise_curve(PiecewiseLogLinearForward,           ForwardRate,    LogLinear);
//export_piecewise_curve(PiecewiseLogCubicForward,            ForwardRate,    LogCubic);
//export_piecewise_curve(PiecewiseLogMixedLinearCubicForward, ForwardRate,    LogMixedLinearCubic);
//export_piecewise_curve(PiecewiseMixedLinearCubicForward,    ForwardRate,    MixedLinearCubic);
export_piecewise_curve(PiecewiseDefaultLogCubicForward,     ForwardRate,    DefaultLogCubic);
export_piecewise_curve(PiecewiseMonotonicLogCubicForward,   ForwardRate,    MonotonicLogCubic);
export_piecewise_curve(PiecewiseKrugerLogForward,           ForwardRate,    KrugerLog);

// Discount
export_piecewise_curve(PiecewiseLinearFlatDiscount,          Discount,    LinearFlat);
export_piecewise_curve(PiecewiseBackwardFlatDiscount,        Discount,    BackwardFlat);
export_piecewise_curve(PiecewiseConvexMonotoneDiscount,      Discount,    ConvexMonotone);
export_piecewise_curve(PiecewiseCubicDiscount,               Discount,    Cubic);
export_piecewise_curve(PiecewiseForwardFlatDiscount,         Discount,    ForwardFlat);
export_piecewise_curve(PiecewiseLinearDiscount,              Discount,    Linear);
export_piecewise_curve(PiecewiseLogLinearDiscount,           Discount,    LogLinear);
//export_piecewise_curve(PiecewiseLogCubicDiscount,            Discount,    LogCubic);
//export_piecewise_curve(PiecewiseLogMixedLinearCubicDiscount, Discount,    LogMixedLinearCubic);
//export_piecewise_curve(PiecewiseMixedLinearCubicDiscount,    Discount,    MixedLinearCubic);
export_piecewise_curve(PiecewiseDefaultLogCubicDiscount,     Discount,    DefaultLogCubic);
export_piecewise_curve(PiecewiseMonotonicLogCubicDiscount,   Discount,    MonotonicLogCubic);
export_piecewise_curve(PiecewiseKrugerLogDiscount,           Discount,    KrugerLog);

// ZeroYield
export_piecewise_curve(PiecewiseLinearFlatZeroYield,          ZeroYield,    LinearFlat);
export_piecewise_curve(PiecewiseBackwardFlatZeroYield,        ZeroYield,    BackwardFlat);
export_piecewise_curve(PiecewiseConvexMonotoneZeroYield,      ZeroYield,    ConvexMonotone);
export_piecewise_curve(PiecewiseCubicZeroYield,               ZeroYield,    Cubic);
export_piecewise_curve(PiecewiseForwardFlatZeroYield,         ZeroYield,    ForwardFlat);
export_piecewise_curve(PiecewiseLinearZeroYield,              ZeroYield,    Linear);
export_piecewise_curve(PiecewiseLogLinearZeroYield,           ZeroYield,    LogLinear);
//export_piecewise_curve(PiecewiseLogCubicZeroYield,            ZeroYield,    LogCubic);
//export_piecewise_curve(PiecewiseLogMixedLinearCubicZeroYield, ZeroYield,    LogMixedLinearCubic);
//export_piecewise_curve(PiecewiseMixedLinearCubicZeroYield,    ZeroYield,    MixedLinearCubic);
export_piecewise_curve(PiecewiseDefaultLogCubicZeroYield,     ZeroYield,    DefaultLogCubic);
export_piecewise_curve(PiecewiseMonotonicLogCubicZeroYield,   ZeroYield,    MonotonicLogCubic);
export_piecewise_curve(PiecewiseKrugerLogZeroYield,           ZeroYield,    KrugerLog);

%{
class AdditionalErrors {
  private:
    std::vector<ext::shared_ptr<RateHelper>> additionalHelpers_;

  public:
    explicit AdditionalErrors(
        const std::vector<ext::shared_ptr<RateHelper>>& additionalHelpers)
        : additionalHelpers_(additionalHelpers) {}
    Array operator()() const {
        Array errors(additionalHelpers_.size() - 2);
        Real a = additionalHelpers_.front()->impliedQuote();
        Real b = additionalHelpers_.back()->impliedQuote();
        for (Size k = 0; k < errors.size(); ++k) {
            errors[k] = (static_cast<Real>(errors.size() - k) * a
                         + static_cast<Real>(1 + k) * b)
                            / static_cast<Real>(errors.size() + 1)
                        - additionalHelpers_.at(1 + k)->impliedQuote();
        }
        return errors;
    }
};

class AdditionalDates {
    std::vector<Date> additionalDates_;

  public:
    explicit AdditionalDates(const std::vector<Date>& additionalDates)
        : additionalDates_(additionalDates) {}
    std::vector<Date> operator()() const {
        return additionalDates_;
    }
};
%}

%shared_ptr(GlobalLinearSimpleZeroCurve)
class GlobalLinearSimpleZeroCurve : public YieldTermStructure {
  public:
    %extend {
        GlobalLinearSimpleZeroCurve(
            const Date& referenceDate,
            const std::vector<ext::shared_ptr<RateHelper>>& instruments,
            const DayCounter& dayCounter,
            const GlobalBootstrap& b) {
            if (b.additionalHelpers.empty()) {
                return new GlobalLinearSimpleZeroCurve(
                    referenceDate, instruments,
                    dayCounter, Linear(),
                    GlobalLinearSimpleZeroCurve::bootstrap_type(
                        b.accuracy));
            } else {
                return new GlobalLinearSimpleZeroCurve(
                    referenceDate, instruments, dayCounter, Linear(),
                    GlobalLinearSimpleZeroCurve::bootstrap_type(
                        b.additionalHelpers,
                        AdditionalDates(b.additionalDates),
                        AdditionalErrors(b.additionalHelpers),
                        b.accuracy));
            }
        }
    }
    const std::vector<Date>& dates() const;
    const std::vector<Time>& times() const;

    std::vector<std::pair<Date, Real>> nodes() const;
};

%shared_ptr(InterpolatedDiscountCurve<LogLinear>);
%shared_ptr(InterpolatedDiscountCurve<MonotonicLogCubic>);
%shared_ptr(InterpolatedDiscountCurve<SplineCubic>);
template <class Interpolator>
class InterpolatedDiscountCurve : public YieldTermStructure {
  public:
    InterpolatedDiscountCurve(
        const std::vector<Date>& dates,
        const std::vector<DiscountFactor>& discounts,
        const DayCounter& dayCounter,
        const Calendar& calendar = Calendar(),
        const Interpolator& i = Interpolator());
    const std::vector<Time>& times() const;
    const std::vector<Real>& data() const;
    const std::vector<Date>& dates() const;
    const std::vector<DiscountFactor>& discounts() const;
    std::vector<std::pair<Date,DiscountFactor>> nodes() const;
};

%template(DiscountCurve) InterpolatedDiscountCurve<LogLinear>;
%template(MonotonicLogCubicDiscountCurve) InterpolatedDiscountCurve<MonotonicLogCubic>;
%template(NaturalCubicDiscountCurve) InterpolatedDiscountCurve<SplineCubic>;

%shared_ptr(FittedBondDiscountCurve)
class FittedBondDiscountCurve : public YieldTermStructure {
  public:
    FittedBondDiscountCurve(
        Natural settlementDays,
        const Calendar& calendar,
        std::vector<ext::shared_ptr<BondHelper>> helpers,
        const DayCounter& dayCounter,
        const FittingMethod& fittingMethod,
        Real accuracy = 1.0e-10,
        Size maxEvaluations = 10000,
        const Array& guess = Array(),
        Real simplexLambda = 1.0);
    FittedBondDiscountCurve(
        const Date& referenceDate,
        std::vector<ext::shared_ptr<BondHelper>> helpers,
        const DayCounter& dayCounter,
        const FittingMethod& fittingMethod,
        Real accuracy = 1.0e-10,
        Size maxEvaluations = 10000,
        const Array& guess = Array(),
        Real simplexLambda = 1.0);
    Size numberOfBonds() const;
    const FittingMethod& fitResults() const;
};

%shared_ptr(InterpolatedZeroCurve<Linear>);
%shared_ptr(InterpolatedZeroCurve<LogLinear>);
%shared_ptr(InterpolatedZeroCurve<Cubic>);
%shared_ptr(InterpolatedZeroCurve<SplineCubic>);
%shared_ptr(InterpolatedZeroCurve<DefaultLogCubic>);
%shared_ptr(InterpolatedZeroCurve<MonotonicCubic>);
template <class Interpolator>
class InterpolatedZeroCurve : public YieldTermStructure {
  public:
    InterpolatedZeroCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& yields,
        const DayCounter& dayCounter,
        const Calendar& calendar = Calendar(),
        const std::vector<Handle<Quote>>& jumps = std::vector<Handle<Quote>>(),
        const std::vector<Date>& jumpDates = std::vector<Date>(),
        const Interpolator& interpolator = Interpolator(),
        Compounding compounding = Continuous,
        Frequency frequency = Annual);
    InterpolatedZeroCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& yields,
        const DayCounter& dayCounter,
        const Calendar& calendar,
        const Interpolator& interpolator,
        Compounding compounding = Continuous,
        Frequency frequency = Annual);
    InterpolatedZeroCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& yields,
        const DayCounter& dayCounter,
        const Interpolator& interpolator,
        Compounding compounding = Continuous,
        Frequency frequency = Annual);

    const std::vector<Time>& times() const;
    const std::vector<Real>& data() const;
    const std::vector<Date>& dates() const;
    const std::vector<Rate>& zeroRates() const;
    std::vector<std::pair<Date,Rate>> nodes() const;
};

%template(ZeroCurve) InterpolatedZeroCurve<Linear>;
%template(LogLinearZeroCurve) InterpolatedZeroCurve<LogLinear>;
%template(CubicZeroCurve) InterpolatedZeroCurve<Cubic>;
%template(NaturalCubicZeroCurve) InterpolatedZeroCurve<SplineCubic>;
%template(LogCubicZeroCurve) InterpolatedZeroCurve<DefaultLogCubic>;
%template(MonotonicCubicZeroCurve) InterpolatedZeroCurve<MonotonicCubic>;

%shared_ptr(InterpolatedForwardCurve<BackwardFlat>);
template <class Interpolator>
class InterpolatedForwardCurve : public YieldTermStructure {
  public:
    InterpolatedForwardCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& forwards,
        const DayCounter& dayCounter,
        const Calendar& cal = Calendar(),
        const std::vector<Handle<Quote>>& jumps = std::vector<Handle<Quote>>(),
        const std::vector<Date>& jumpDates = std::vector<Date>(),
        const Interpolator& interpolator = Interpolator());
    InterpolatedForwardCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& forwards,
        const DayCounter& dayCounter,
        const Calendar& calendar,
        const Interpolator& interpolator);
    InterpolatedForwardCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& forwards,
        const DayCounter& dayCounter,
        const Interpolator& interpolator);

    const std::vector<Time>& times() const;
    const std::vector<Real>& data() const;
    const std::vector<Date>& dates() const;
    const std::vector<Rate>& forwards() const;
    std::vector<std::pair<Date,Rate>> nodes() const;
};

%template(ForwardCurve) InterpolatedForwardCurve<BackwardFlat>;

#endif
