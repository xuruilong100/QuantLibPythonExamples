#ifndef ql_instruments_forwards_all_i
#define ql_instruments_forwards_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/Forward.i

%{
using QuantLib::FixedRateBondForward;
using QuantLib::ForwardRateAgreement;
using QuantLib::OvernightIndexFuture;
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

%shared_ptr(ForwardRateAgreement)
class ForwardRateAgreement : public Forward {
  public:
    ForwardRateAgreement(
        const Date& valueDate,
        const Date& maturityDate,
        Position::Type type,
        Rate strikeForwardRate,
        Real notionalAmount,
        const ext::shared_ptr<IborIndex>& index,
        const Handle<YieldTermStructure>& discountCurve = Handle<YieldTermStructure>(),
        bool useIndexedCoupon = true);

    Date fixingDate() const;
    Real spotIncome(const Handle<YieldTermStructure>& discount) const;
    Real spotValue() const;
    InterestRate forwardRate() const;
};

%shared_ptr(OvernightIndexFuture)
class OvernightIndexFuture : public Forward {
  public:
    enum NettingType { Averaging, Compounding };

    %extend {
        OvernightIndexFuture(
            const ext::shared_ptr<OvernightIndex>& overnightIndex,
            const Date& valueDate,
            const Date& maturityDate,
            const Handle<YieldTermStructure>& discountCurve,
            const Handle<Quote>& convexityAdjustment = Handle<Quote>(),
            NettingType subPeriodsNettingType = Compounding) {
            return new OvernightIndexFuture(
                overnightIndex, ext::shared_ptr<Payoff>(),
                valueDate, maturityDate, discountCurve,
                convexityAdjustment, subPeriodsNettingType);
        }
    }

    Real convexityAdjustment() const;
};

#endif
