#ifndef ql_termstructures_CallableBondVolatilityStructure_i
#define ql_termstructures_CallableBondVolatilityStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CallableBondVolatilityStructure;
using QuantLib::CallableBondConstantVolatility;
%}

%shared_ptr(CallableBondVolatilityStructure)
class CallableBondVolatilityStructure : public TermStructure {
  private:
    CallableBondVolatilityStructure();
  public:
    Volatility volatility(
        Time optionTime,
        Time bondLength,
        Rate strike,
        bool extrapolate = false) const;
    Real blackVariance(
        Time optionTime,
        Time bondLength,
        Rate strike,
        bool extrapolate = false) const;
    Volatility volatility(
        const Date& optionDate,
        const Period& bondTenor,
        Rate strike,
        bool extrapolate = false) const;
    Real blackVariance(
        const Date& optionDate,
        const Period& bondTenor,
        Rate strike,
        bool extrapolate = false) const;
    ext::shared_ptr<SmileSection> smileSection(
        const Date& optionDate,
        const Period& bondTenor) const;
    Volatility volatility(
        const Period& optionTenor,
        const Period& bondTenor,
        Rate strike,
        bool extrapolate = false) const;
    Real blackVariance(
        const Period& optionTenor,
        const Period& bondTenor,
        Rate strike,
        bool extrapolate = false) const;
    ext::shared_ptr<SmileSection> smileSection(
        const Period& optionTenor,
        const Period& bondTenor) const;
    const Period& maxBondTenor() const;
    Time maxBondLength() const;
    Rate minStrike() const;
    Rate maxStrike() const;
    std::pair<Time,Time> convertDates(
        const Date& optionDate,
        const Period& bondTenor) const;
    BusinessDayConvention businessDayConvention() const;
    Date optionDateFromTenor(
        const Period& optionTenor) const;
};

%shared_ptr(CallableBondConstantVolatility)
class CallableBondConstantVolatility : public CallableBondVolatilityStructure {
  public:
    CallableBondConstantVolatility(
        const Date& referenceDate,
        Volatility volatility,
        DayCounter dayCounter);
    CallableBondConstantVolatility(
        const Date& referenceDate,
        Handle<Quote> volatility,
        DayCounter dayCounter);
    CallableBondConstantVolatility(
        Natural settlementDays,
        const Calendar&,
        Volatility volatility,
        DayCounter dayCounter);
    CallableBondConstantVolatility(
        Natural settlementDays,
        const Calendar&,
        Handle<Quote> volatility,
        DayCounter dayCounter);
};

#endif
