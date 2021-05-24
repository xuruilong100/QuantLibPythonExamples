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

%shared_ptr(FlatHazardRate);
class FlatHazardRate : public DefaultProbabilityTermStructure {
  public:
    FlatHazardRate(
        Integer settlementDays,
        const Calendar& calendar,
        const Handle<Quote>& hazardRate,
        const DayCounter& dayCounter);
    FlatHazardRate(
        const Date& todaysDate,
        const Handle<Quote>& hazardRate,
        const DayCounter& dayCounter);
};

// add other instantiations both here and below the class
%shared_ptr(InterpolatedHazardRateCurve<BackwardFlat>);
template <class Interpolator>
class InterpolatedHazardRateCurve : public DefaultProbabilityTermStructure {
  public:
    InterpolatedHazardRateCurve(
        const std::vector<Date>& dates,
        const std::vector<Real>& hazardRates,
        const DayCounter& dayCounter,
        const Calendar& calendar = Calendar(),
        const Interpolator& i = Interpolator());
    const std::vector<Date>& dates() const;
    const std::vector<Real>& hazardRates() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(HazardRateCurve) InterpolatedHazardRateCurve<BackwardFlat>;

// add other instantiations both here and below the class
%shared_ptr(InterpolatedDefaultDensityCurve<Linear>);
template <class Interpolator>
class InterpolatedDefaultDensityCurve : public DefaultProbabilityTermStructure {
  public:
    InterpolatedDefaultDensityCurve(
        const std::vector<Date>& dates,
        const std::vector<Real>& densities,
        const DayCounter& dayCounter,
        const Calendar& calendar = Calendar(),
        const Interpolator& i = Interpolator());
    const std::vector<Date>& dates() const;
    const std::vector<Real>& defaultDensities() const;
    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(DefaultDensityCurve) InterpolatedDefaultDensityCurve<Linear>;

// add other instantiations both here and below the class
%shared_ptr(InterpolatedSurvivalProbabilityCurve<Linear>);
template <class Interpolator>
class InterpolatedSurvivalProbabilityCurve : public DefaultProbabilityTermStructure {
  public:
    InterpolatedSurvivalProbabilityCurve(
        const std::vector<Date>& dates,
        const std::vector<Probability>& probabilities,
        const DayCounter& dayCounter,
        const Calendar& calendar = Calendar(),
        const Interpolator& i = Interpolator());
    const std::vector<Date>& dates() const;
    const std::vector<Probability>& survivalProbabilities() const;

    std::vector<std::pair<Date, Real>> nodes() const;
};

%template(SurvivalProbabilityCurve) InterpolatedSurvivalProbabilityCurve<Linear>;

%define export_piecewise_default_curve(Name,Traits,Interpolator)
%{
typedef PiecewiseDefaultCurve<Traits, Interpolator> Name;
%}

%shared_ptr(Name);
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
        /* Name(const Date& referenceDate,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
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
        } */
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
        /* Name(Integer settlementDays,
             const Calendar& calendar,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const IterativeBootstrap& b) {
            return new Name(
                settlementDays, calendar,
                instruments,
                dayCounter,
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue,
                    b.maxAttempts, b.maxFactor, b.minFactor,
                    b.dontThrow, b.dontThrowSteps));
        } */
        //-----------
        /* Name(const Date& referenceDate,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             Real accuracy = 1.0e-12,
             const Interpolator& i = Interpolator(),
             const _IterativeBootstrap& b = _IterativeBootstrap()) {
            return new Name(
                referenceDate, instruments,
                dayCounter, accuracy, i,
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue));
        }
        Name(Integer settlementDays, const Calendar& calendar,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             Real accuracy = 1.0e-12,
             const Interpolator& i = Interpolator(),
             const _IterativeBootstrap& b = _IterativeBootstrap()) {
            return new Name(
                settlementDays, calendar,
                instruments, dayCounter,
                accuracy, i,
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue));
        }
        Name(const Date& referenceDate,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const _IterativeBootstrap& b) {
            return new Name(
                referenceDate, instruments,
                dayCounter, 1e-12,
                Interpolator(),
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue));
        }
        Name(Integer settlementDays, const Calendar& calendar,
             const std::vector<ext::shared_ptr<DefaultProbabilityHelper>>& instruments,
             const DayCounter& dayCounter,
             const _IterativeBootstrap& b) {
            return new Name(
                settlementDays, calendar,
                instruments, dayCounter, 1e-12,
                Interpolator(),
                Name::bootstrap_type(
                    b.accuracy, b.minValue, b.maxValue));
        } */
    }
    const std::vector<Date>& dates() const;
    const std::vector<Time>& times() const;

    std::vector<std::pair<Date, Real>> nodes() const;
};

%enddef

// add other instantiations if you need them
export_piecewise_default_curve(PiecewiseFlatHazardRate,HazardRate,BackwardFlat);

#endif
