#ifndef ql_custom_all_i
#define ql_custom_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/volatilitytermstructures/LocalVolTermStructure.i
%include ../ql/termstructures/volatilitytermstructures/blackvol/all.i

%{
class CustomLocalVolatility : public LocalVolTermStructure {
  public:
    CustomLocalVolatility(
        PyObject* localVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(bdc, dc),
        localVolImpl_(localVolImpl) {}
    CustomLocalVolatility(
        PyObject* localVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(referenceDate, cal, bdc, dc),
        localVolImpl_(localVolImpl) {}
    CustomLocalVolatility(
        PyObject* localVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(settlementDays, cal, bdc, dc),
        localVolImpl_(localVolImpl) {}

    Date maxDate() const override {return Date::maxDate(); }
    Real minStrike() const override { return 0.0; }
    Real maxStrike() const override { return QL_MAX_REAL; }

  protected:
    Volatility localVolImpl(Time t, Real strike) const override {
        return localVolImpl_(t, strike);
    }
  private:
    BinaryFunction localVolImpl_;
};
%}

%shared_ptr(CustomLocalVolatility)
class CustomLocalVolatility : public LocalVolTermStructure {
  public:
    CustomLocalVolatility(
        PyObject* localVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
    CustomLocalVolatility(
        PyObject* localVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
    CustomLocalVolatility(
        PyObject* localVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
};

%{
class CustomBlackVolatility : public BlackVolatilityTermStructure {
  public:
    CustomBlackVolatility(
        PyObject* blackVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        BlackVolatilityTermStructure(bdc, dc),
        blackVolImpl_(blackVolImpl) {}

    CustomBlackVolatility(
        PyObject* blackVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        BlackVolatilityTermStructure(
            referenceDate, cal, bdc, dc),
        blackVolImpl_(blackVolImpl) {}

    CustomBlackVolatility(
        PyObject* blackVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        BlackVolatilityTermStructure(
            settlementDays, cal, bdc, dc),
        blackVolImpl_(blackVolImpl) {}

    Date maxDate() const override { return Date::maxDate(); }
    Rate minStrike() const override { return 0.0; }
    Rate maxStrike() const override { return QL_MAX_REAL; }

  protected:
    Real blackVolImpl(
        Time maturity, Real strike) const override {
        return blackVolImpl_(maturity, strike);
    }
  private:
    BinaryFunction blackVolImpl_;
};
%}

%shared_ptr(CustomBlackVolatility)
class CustomBlackVolatility : public BlackVolatilityTermStructure {
  public:
    CustomBlackVolatility(
        PyObject* blackVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());

    CustomBlackVolatility(
        PyObject* blackVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());

    CustomBlackVolatility(
        PyObject* blackVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
};

#endif
