#ifndef ql_instruments_forwards_all_i
#define ql_instruments_forwards_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/Forward.i

%{
using QuantLib::BondForward;
%}

%shared_ptr(BondForward)
class BondForward : public Forward {
  public:
    BondForward(
        const Date& valueDate,
        const Date& maturityDate,
        Position::Type type,
        Real strike,
        Natural settlementDays,
        const DayCounter& dayCounter,
        const Calendar& calendar,
        BusinessDayConvention businessDayConvention,
        const ext::shared_ptr<Bond>& bond,
        const Handle<YieldTermStructure>& discountCurve = Handle<YieldTermStructure>(),
        const Handle<YieldTermStructure>& incomeDiscountCurve = Handle<YieldTermStructure>());

    Real forwardPrice() const;
    Real cleanForwardPrice() const;
};

#endif
