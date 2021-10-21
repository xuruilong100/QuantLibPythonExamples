#ifndef ql_termstructures_defaultprobabilitytermstructures_all_i
#define ql_termstructures_defaultprobabilitytermstructures_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/DefaultProbabilityTermStructure.i

%{
using QuantLib::HazardRate;
using QuantLib::DefaultDensity;
%}

struct HazardRate {};
struct DefaultDensity {};

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
class Name : public DefaultProbabilityTermStructure {
  public:
    %extend {
        Name(const Date& referenceDate,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const std::vector<Handle<Quote>>& jumps = std::vector<Handle<Quote>>(),
             const std::vector<Date>& jumpDates = std::vector<Date>(),
             const Interpolator& i = Interpolator(),
             const IterativeBootstrap& b = IterativeBootstrap()) {
            return new Name(
                referenceDate, instruments,
                dayCounter,
                jumps, jumpDates,
                i,
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
                referenceDate,
                instruments,
                dayCounter,
                i,
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue,
                    b.maxAttempts, b.maxFactor, b.minFactor,
                    b.dontThrow, b.dontThrowSteps));
        }
        Name(Integer settlementDays,
             const Calendar& calendar,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const std::vector<Handle<Quote>>& jumps = std::vector<Handle<Quote>>(),
             const std::vector<Date>& jumpDates = std::vector<Date>(),
             const Interpolator& i = Interpolator(),
             const IterativeBootstrap& b = IterativeBootstrap()) {
            return new Name(
                settlementDays, calendar,
                instruments, dayCounter,
                jumps, jumpDates,
                i,
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
                settlementDays, calendar,
                instruments,
                dayCounter,
                i,
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

export_piecewise_default_curve(PiecewiseFlatHazardRate,HazardRate,BackwardFlat);

#endif
