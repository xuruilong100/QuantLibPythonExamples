#ifndef ql_termstructures_DefaultProbabilityTermStructure_i
#define ql_termstructures_DefaultProbabilityTermStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::DefaultProbabilityTermStructure;
%}

%shared_ptr(DefaultProbabilityTermStructure)
class DefaultProbabilityTermStructure : public TermStructure {
  private:
    DefaultProbabilityTermStructure();

  public:
    Probability defaultProbability(
        const Date&, bool extrapolate = false);
    Probability defaultProbability(
        Time, bool extrapolate = false);
    Probability defaultProbability(
        const Date&, const Date&,
        bool extrapolate = false);
    Probability defaultProbability(
        Time, Time, bool extrapolate = false);
    Probability survivalProbability(
        const Date&, bool extrapolate = false);
    Probability survivalProbability(
        Time, bool extrapolate = false);
    Real defaultDensity(
        const Date&, bool extrapolate = false);
    Real defaultDensity(Time, bool extrapolate = false);
    Real hazardRate(
        const Date&, bool extrapolate = false);
    Real hazardRate(
        Time, bool extrapolate = false);
    const std::vector<Date>& jumpDates() const;
    const std::vector<Time>& jumpTimes() const;
};


%template(DefaultProbabilityTermStructureHandle) Handle<DefaultProbabilityTermStructure>;
%template(RelinkableDefaultProbabilityTermStructureHandle) RelinkableHandle<DefaultProbabilityTermStructure>;

#endif
