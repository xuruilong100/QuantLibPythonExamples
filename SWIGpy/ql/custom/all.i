#ifndef ql_custom_all_i
#define ql_custom_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/volatilitytermstructures/LocalVolTermStructure.i

%{
class CustomicLocalVolatility : public LocalVolTermStructure {
  public:
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(bdc, dc),
        localVolImpl_(localVolImpl) {}
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(referenceDate, cal, bdc, dc),
        localVolImpl_(localVolImpl) {}
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(settlementDays, cal, bdc, dc),
        localVolImpl_(localVolImpl) {}

    Date maxDate() const override {return Date::maxDate(); }
    Real minStrike() const override { return 0.0; }
    Real maxStrike() const override { return std::numeric_limits<Real>::max(); }

  protected:
    Volatility localVolImpl(Time t, Real strike) const override {
        return localVolImpl_(t, strike);
    }
  private:
    BinaryFunction localVolImpl_;
};
%}

%shared_ptr(CustomicLocalVolatility)
class CustomicLocalVolatility : public LocalVolTermStructure {
  public:
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
};

#endif
