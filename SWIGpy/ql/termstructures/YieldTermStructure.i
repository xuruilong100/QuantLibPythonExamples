#ifndef ql_termstructures_YieldTermStructure_i
#define ql_termstructures_YieldTermStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::YieldTermStructure;
%}

%shared_ptr(YieldTermStructure)
class YieldTermStructure : public TermStructure {
  private:
    YieldTermStructure();

  public:
    DiscountFactor discount(
        const Date&, bool extrapolate = false) const;
    DiscountFactor discount(
        Time, bool extrapolate = false) const;
    InterestRate zeroRate(
        const Date& d,
        const DayCounter&, Compounding, Frequency f = Annual,
        bool extrapolate = false) const;
    InterestRate zeroRate(
        Time t,
        Compounding, Frequency f = Annual,
        bool extrapolate = false) const;
    InterestRate forwardRate(
        const Date& d1, const Date& d2,
        const DayCounter&, Compounding,
        Frequency f = Annual,
        bool extrapolate = false) const;
    InterestRate forwardRate(
        const Date& d, const Period& p,
        const DayCounter& resultDayCounter,
        Compounding comp, Frequency freq = Annual,
        bool extrapolate = false) const;
    InterestRate forwardRate(
        Time t1, Time t2,
        Compounding, Frequency f = Annual,
        bool extrapolate = false) const;
    const std::vector<Date>& jumpDates() const;
    const std::vector<Time>& jumpTimes() const;
};

%template(YieldTermStructureHandle) Handle<YieldTermStructure>;
%template(RelinkableYieldTermStructureHandle) RelinkableHandle<YieldTermStructure>;

#endif
