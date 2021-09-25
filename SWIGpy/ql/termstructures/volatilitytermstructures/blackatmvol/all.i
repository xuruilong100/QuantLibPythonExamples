#ifndef ql_termstructures_volatilitytermstructures_blackatmvol_all_i
#define ql_termstructures_volatilitytermstructures_blackatmvol_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/volatilitytermstructures/BlackAtmVolCurve.i

%{
using QuantLib::AbcdAtmVolCurve;
using QuantLib::BlackVolSurface;
using QuantLib::InterestRateVolSurface;
using QuantLib::EquityFXVolSurface;
using QuantLib::SabrVolSurface;
%}

%shared_ptr(AbcdAtmVolCurve)
class AbcdAtmVolCurve : public BlackAtmVolCurve, public LazyObject {
  public:
    AbcdAtmVolCurve(
        Natural settlementDays,
        const Calendar& cal,
        const std::vector<Period>& optionTenors,
        const std::vector<Handle<Quote> >& volsHandles,
        std::vector<bool> inclusionInInterpolationFlag = std::vector<bool>(1, true),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = Actual365Fixed());

    std::vector<Real> k() const;
    Real k(Time t) const;
    Real a() const;
    Real b() const;
    Real c() const;
    Real d() const;
    Real rmsError() const;
    Real maxError() const;
    // EndCriteria::Type endCriteria() const;

    const std::vector<Period>& optionTenors() const;
    const std::vector<Period>& optionTenorsInInterpolation() const;
    const std::vector<Date>& optionDates() const;
    const std::vector<Time>& optionTimes() const;
};

%shared_ptr(BlackVolSurface)
class BlackVolSurface : public BlackAtmVolCurve {
  private:
    BlackVolSurface();
  public:
    ext::shared_ptr<SmileSection> smileSection(
        const Period&,
        bool extrapolate) const;
    ext::shared_ptr<SmileSection> smileSection(
        const Date&,
        bool extrapolate) const;
    ext::shared_ptr<SmileSection> smileSection(
        Time,
        bool extrapolate) const;
};

%shared_ptr(InterestRateVolSurface)
class InterestRateVolSurface : public BlackVolSurface {
  private:
    InterestRateVolSurface();
  public:
    Date optionDateFromTenor(const Period&) const;
    const ext::shared_ptr<InterestRateIndex>& index() const;
};

%shared_ptr(EquityFXVolSurface)
class EquityFXVolSurface : public BlackVolSurface {
  private:
    EquityFXVolSurface();
  public:
    Volatility atmForwardVol(
        const Date& date1,
        const Date& date2,
        bool extrapolate = false) const;
    Volatility atmForwardVol(
        Time time1,
        Time time2,
        bool extrapolate = false) const;
    Real atmForwardVariance(
        const Date& date1,
        const Date& date2,
        bool extrapolate = false) const;
    Real atmForwardVariance(
        Time time1,
        Time time2,
        bool extrapolate = false) const;
};

%shared_ptr(SabrVolSurface)
class SabrVolSurface : public InterestRateVolSurface {
  public:
    SabrVolSurface(
        const ext::shared_ptr<InterestRateIndex>&,
        Handle<BlackAtmVolCurve>,
        const std::vector<Period>& optionTenors,
        std::vector<Spread> atmRateSpreads,
        std::vector<std::vector<Handle<Quote> > > volSpreads);

    const Handle<BlackAtmVolCurve>& atmCurve() const;
    std::vector<Volatility> volatilitySpreads(const Period&) const;
    std::vector<Volatility> volatilitySpreads(const Date&) const;
};

#endif
