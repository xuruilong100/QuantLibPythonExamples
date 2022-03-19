#ifndef ql_termstructures_defaultprobabilitytermstructures_all_i
#define ql_termstructures_defaultprobabilitytermstructures_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/termstructures/DefaultProbabilityTermStructure.i

%{
using QuantLib::HazardRate;
using QuantLib::DefaultDensity;
using QuantLib::SurvivalProbability;
%}

struct HazardRate {};
struct DefaultDensity {};
struct SurvivalProbability {};

%{
using QuantLib::FlatHazardRate;
using QuantLib::InterpolatedHazardRateCurve;
using QuantLib::InterpolatedDefaultDensityCurve;
using QuantLib::InterpolatedSurvivalProbabilityCurve;
using QuantLib::PiecewiseDefaultCurve;
%}

%shared_ptr(FlatHazardRate)
class FlatHazardRate : public DefaultProbabilityTermStructure {
  public:
    FlatHazardRate(
        const Date& todaysDate,
        const Handle<Quote>& hazardRate,
        const DayCounter& dayCounter);
    FlatHazardRate(
        const Date& referenceDate,
        Rate hazardRate,
        const DayCounter&);
    FlatHazardRate(
        Natural settlementDays,
        const Calendar& calendar,
        const Handle<Quote>& hazardRate,
        const DayCounter& dayCounter);
    FlatHazardRate(
        Natural settlementDays,
        const Calendar& calendar,
        Rate hazardRate,
        const DayCounter&);
};

%shared_ptr(InterpolatedHazardRateCurve<BackwardFlat>)
template <class Interpolator>
class InterpolatedHazardRateCurve : public DefaultProbabilityTermStructure {
  public:
    InterpolatedHazardRateCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& hazardRates,
        const DayCounter& dayCounter,
        const Calendar& cal = Calendar(),
        const std::vector<Handle<Quote>>& jumps = std::vector<Handle<Quote>>(),
        const std::vector<Date>& jumpDates = std::vector<Date>(),
        const Interpolator& interpolator = Interpolator());
    InterpolatedHazardRateCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& hazardRates,
        const DayCounter& dayCounter,
        const Calendar& calendar,
        const Interpolator& interpolator);
    InterpolatedHazardRateCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& hazardRates,
        const DayCounter& dayCounter,
        const Interpolator& interpolator);
    const std::vector<Time>& times() const;
    const std::vector<Date>& dates() const;
    const std::vector<Real>& data() const;
    const std::vector<Real>& hazardRates() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(HazardRateCurve) InterpolatedHazardRateCurve<BackwardFlat>;

%shared_ptr(InterpolatedDefaultDensityCurve<Linear>)
template <class Interpolator>
class InterpolatedDefaultDensityCurve : public DefaultProbabilityTermStructure {
  public:
    InterpolatedDefaultDensityCurve(
        const std::vector<Date>& dates,
        const std::vector<Real>& densities,
        const DayCounter& dayCounter,
        const Calendar& calendar = Calendar(),
        const std::vector<Handle<Quote>>& jumps = std::vector<Handle<Quote>>(),
        const std::vector<Date>& jumpDates = std::vector<Date>(),
        const Interpolator& interpolator = Interpolator());
    InterpolatedDefaultDensityCurve(
        const std::vector<Date>& dates,
        const std::vector<Real>& densities,
        const DayCounter& dayCounter,
        const Calendar& calendar,
        const Interpolator& interpolator);
    InterpolatedDefaultDensityCurve(
        const std::vector<Date>& dates,
        const std::vector<Real>& densities,
        const DayCounter& dayCounter,
        const Interpolator& interpolator);
    const std::vector<Time>& times() const;
    const std::vector<Date>& dates() const;
    const std::vector<Real>& data() const;
    const std::vector<Real>& defaultDensities() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(DefaultDensityCurve) InterpolatedDefaultDensityCurve<Linear>;

%shared_ptr(InterpolatedSurvivalProbabilityCurve<Linear>)
template <class Interpolator>
class InterpolatedSurvivalProbabilityCurve : public DefaultProbabilityTermStructure {
  public:
    InterpolatedSurvivalProbabilityCurve(
        const std::vector<Date>& dates,
        const std::vector<Probability>& probabilities,
        const DayCounter& dayCounter,
        const Calendar& calendar = Calendar(),
        const std::vector<Handle<Quote>>& jumps = std::vector<Handle<Quote>>(),
        const std::vector<Date>& jumpDates = std::vector<Date>(),
        const Interpolator& interpolator = Interpolator());
    InterpolatedSurvivalProbabilityCurve(
        const std::vector<Date>& dates,
        const std::vector<Probability>& probabilities,
        const DayCounter& dayCounter,
        const Calendar& calendar,
        const Interpolator& interpolator);
    InterpolatedSurvivalProbabilityCurve(
        const std::vector<Date>& dates,
        const std::vector<Probability>& probabilities,
        const DayCounter& dayCounter,
        const Interpolator& interpolator);
    const std::vector<Time>& times() const;
    const std::vector<Date>& dates() const;
    const std::vector<Real>& data() const;
    const std::vector<Probability>& survivalProbabilities() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(SurvivalProbabilityCurve) InterpolatedSurvivalProbabilityCurve<Linear>;

%define export_piecewise_default_curve(Name,Traits,Interpolator)
%{
typedef PiecewiseDefaultCurve<Traits, Interpolator> Name;
%}

%shared_ptr(Name)
class Name : public DefaultProbabilityTermStructure, public LazyObject {
  public:
    %extend {
        Name(const Date& referenceDate,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const std::vector<Handle<Quote>>& jumps,
             const std::vector<Date>& jumpDates,
             const Interpolator& i,
             const IterativeBootstrap& b = IterativeBootstrap()) {
            return new Name(
                referenceDate, instruments, dayCounter, jumps, jumpDates, i,
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue,
                    b.maxAttempts, b.maxFactor, b.minFactor,
                    b.dontThrow, b.dontThrowSteps));
        }
        Name(const Date& referenceDate,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const Interpolator& i,
             const IterativeBootstrap& b = IterativeBootstrap()) {
            return new Name(
                referenceDate, instruments, dayCounter, i,
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue,
                    b.maxAttempts, b.maxFactor, b.minFactor,
                    b.dontThrow, b.dontThrowSteps));
        }
        Name(Integer settlementDays,
             const Calendar& calendar,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const std::vector<Handle<Quote>>& jumps,
             const std::vector<Date>& jumpDates,
             const Interpolator& i,
             const IterativeBootstrap& b = IterativeBootstrap()) {
            return new Name(
                settlementDays, calendar, instruments, dayCounter, jumps, jumpDates, i,
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue,
                    b.maxAttempts, b.maxFactor, b.minFactor,
                    b.dontThrow, b.dontThrowSteps));
        }
        Name(Integer settlementDays,
             const Calendar& calendar,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const Interpolator& i,
             const IterativeBootstrap& b = IterativeBootstrap()) {
            return new Name(
                settlementDays, calendar, instruments, dayCounter, i,
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue,
                    b.maxAttempts, b.maxFactor, b.minFactor,
                    b.dontThrow, b.dontThrowSteps));
        }
    }
    const std::vector<Time>& times() const;
    const std::vector<Date>& dates() const;
    const std::vector<Real>& data() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%enddef

// HazardRate
export_piecewise_default_curve(PiecewiseLinearFlatHazard,          HazardRate,    LinearFlat);
export_piecewise_default_curve(PiecewiseBackwardFlatHazard,        HazardRate,    BackwardFlat);
export_piecewise_default_curve(PiecewiseConvexMonotoneHazard,      HazardRate,    ConvexMonotone);
export_piecewise_default_curve(PiecewiseCubicHazard,               HazardRate,    Cubic);
export_piecewise_default_curve(PiecewiseForwardFlatHazard,         HazardRate,    ForwardFlat);
export_piecewise_default_curve(PiecewiseLinearHazard,              HazardRate,    Linear);
export_piecewise_default_curve(PiecewiseLogLinearHazard,           HazardRate,    LogLinear);
export_piecewise_default_curve(PiecewiseLogCubicHazard,            HazardRate,    LogCubic);
export_piecewise_default_curve(PiecewiseLogMixedLinearCubicHazard, HazardRate,    LogMixedLinearCubic);
export_piecewise_default_curve(PiecewiseMixedLinearCubicHazard,    HazardRate,    MixedLinearCubic);
export_piecewise_default_curve(PiecewiseDefaultLogCubicHazard,     HazardRate,    DefaultLogCubic);
export_piecewise_default_curve(PiecewiseMonotonicLogCubicHazard,   HazardRate,    MonotonicLogCubic);
export_piecewise_default_curve(PiecewiseKrugerLogHazard,           HazardRate,    KrugerLog);

// DefaultDensity
export_piecewise_default_curve(PiecewiseLinearFlatDefault,          DefaultDensity,    LinearFlat);
export_piecewise_default_curve(PiecewiseBackwardFlatDefault,        DefaultDensity,    BackwardFlat);
export_piecewise_default_curve(PiecewiseConvexMonotoneDefault,      DefaultDensity,    ConvexMonotone);
export_piecewise_default_curve(PiecewiseCubicDefault,               DefaultDensity,    Cubic);
export_piecewise_default_curve(PiecewiseForwardFlatDefault,         DefaultDensity,    ForwardFlat);
export_piecewise_default_curve(PiecewiseLinearDefault,              DefaultDensity,    Linear);
export_piecewise_default_curve(PiecewiseLogLinearDefault,           DefaultDensity,    LogLinear);
export_piecewise_default_curve(PiecewiseLogCubicDefault,            DefaultDensity,    LogCubic);
export_piecewise_default_curve(PiecewiseLogMixedLinearCubicDefault, DefaultDensity,    LogMixedLinearCubic);
export_piecewise_default_curve(PiecewiseMixedLinearCubicDefault,    DefaultDensity,    MixedLinearCubic);
export_piecewise_default_curve(PiecewiseDefaultLogCubicDefault,     DefaultDensity,    DefaultLogCubic);
export_piecewise_default_curve(PiecewiseMonotonicLogCubicDefault,   DefaultDensity,    MonotonicLogCubic);
export_piecewise_default_curve(PiecewiseKrugerLogDefault,           DefaultDensity,    KrugerLog);

// SurvivalProbability
export_piecewise_default_curve(PiecewiseLinearFlatSurvival,         SurvivalProbability,    LinearFlat);
export_piecewise_default_curve(PiecewiseBackwardFlatSurvival,       SurvivalProbability,    BackwardFlat);
export_piecewise_default_curve(PiecewiseConvexMonotoneSurvival,     SurvivalProbability,    ConvexMonotone);
export_piecewise_default_curve(PiecewiseCubicSurvival,              SurvivalProbability,    Cubic);
export_piecewise_default_curve(PiecewiseForwardFlatSurvival,        SurvivalProbability,    ForwardFlat);
export_piecewise_default_curve(PiecewiseLinearSurvival,             SurvivalProbability,    Linear);
export_piecewise_default_curve(PiecewiseLogLinearSurvival,          SurvivalProbability,    LogLinear);
export_piecewise_default_curve(PiecewiseLogCubicSurvival,           SurvivalProbability,    LogCubic);
export_piecewise_default_curve(PiecewiseLogMixedLinearCubicSurvival,SurvivalProbability,    LogMixedLinearCubic);
export_piecewise_default_curve(PiecewiseMixedLinearCubicSurvival,   SurvivalProbability,    MixedLinearCubic);
export_piecewise_default_curve(PiecewiseDefaultLogCubicSurvival,    SurvivalProbability,    DefaultLogCubic);
export_piecewise_default_curve(PiecewiseMonotonicLogCubicSurvival,  SurvivalProbability,    MonotonicLogCubic);
export_piecewise_default_curve(PiecewiseKrugerLogSurvival,          SurvivalProbability,    KrugerLog);

#endif
