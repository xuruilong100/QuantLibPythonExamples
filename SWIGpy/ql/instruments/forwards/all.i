#ifndef ql_instruments_forwards_all_i
#define ql_instruments_forwards_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/Forward.i

%{
using QuantLib::FixedRateBondForward;
%}

%shared_ptr(FixedRateBondForward)
class FixedRateBondForward : public Forward {
  public:
    FixedRateBondForward(
        const Date& valueDate,
        const Date& maturityDate,
        Position::Type type,
        Real strike,
        Natural settlementDays,
        const DayCounter& dayCounter,
        const Calendar& calendar,
        BusinessDayConvention businessDayConvention,
        const ext::shared_ptr<FixedRateBond>& fixedBond,
        const Handle<YieldTermStructure>& discountCurve = Handle<YieldTermStructure>(),
        const Handle<YieldTermStructure>& incomeDiscountCurve = Handle<YieldTermStructure>());
    Real forwardPrice();
    Real cleanForwardPrice();
};

#endif
