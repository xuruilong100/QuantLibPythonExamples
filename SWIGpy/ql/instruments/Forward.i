#ifndef ql_instruments_Forward_i
#define ql_instruments_Forward_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Forward;
using QuantLib::OvernightIndexFuture;
%}

%shared_ptr(Forward)
class Forward : public Instrument{
  private:
    Forward();
  public:
    Date settlementDate() const;
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
};

%shared_ptr(OvernightIndexFuture)
class OvernightIndexFuture : public Instrument {
  public:
    OvernightIndexFuture(
        ext::shared_ptr<OvernightIndex> overnightIndex,
        const Date& valueDate,
        const Date& maturityDate,
        Handle<Quote> convexityAdjustment = Handle<Quote>(),
        RateAveraging::Type averagingMethod = RateAveraging::Compound);

    Real convexityAdjustment() const;
};

#endif
