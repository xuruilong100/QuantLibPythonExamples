#ifndef ql_instruments_Forward_i
#define ql_instruments_Forward_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Forward;
%}

%shared_ptr(Forward)
class Forward : public Instrument{
public:
    Date settlementDate() const;
    bool isExpired() const;
    const Calendar& calendar() const;
    BusinessDayConvention businessDayConvention() const;
    const DayCounter& dayCounter() const;
    Handle<YieldTermStructure> discountCurve() const;
    Handle<YieldTermStructure> incomeDiscountCurve() const;
    Real spotValue() const;
    Real spotIncome(const Handle<YieldTermStructure>& incomeDiscountCurve) const;

    Real forwardValue();
    InterestRate impliedYield(
        Real underlyingSpotValue,
        Real forwardValue,
        Date settlementDate,
        Compounding compoundingConvention,
        DayCounter dayCounter);
private:
    Forward();
};

#endif
