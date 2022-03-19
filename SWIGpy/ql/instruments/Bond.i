#ifndef ql_instruments_Bond_i
#define ql_instruments_Bond_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Bond;
typedef Bond::Price BondPrice;
%}

class BondPrice {
  public:
    enum Type { Dirty, Clean };
    BondPrice(Real amount, Type type);
    Real amount() const;
    Type type() const;
};

%shared_ptr(Bond)
class Bond : public Instrument {
    %rename(bondYield) yield;
  public:
    Bond(Natural settlementDays,
         const Calendar& calendar,
         Real faceAmount,
         const Date& maturityDate,
         const Date& issueDate = Date(),
         const Leg& cashflows = Leg());
    Bond(Natural settlementDays,
         const Calendar& calendar,
         const Date& issueDate = Date(),
        const Leg& coupons = Leg());
    Natural settlementDays() const;
    const Calendar& calendar() const;
    const std::vector<Real>& notionals() const;
    Real notional(Date d = Date()) const;
    const Leg& cashflows() const;
    const Leg& redemptions() const;
    const ext::shared_ptr<CashFlow>& redemption() const;
    Date startDate() const;
    Date maturityDate() const;
    Date issueDate() const;
    bool isTradable(Date d = Date()) const;
    Date settlementDate(Date d = Date()) const;
    Real cleanPrice() const;
    Real dirtyPrice() const;
    Real settlementValue() const;
    Rate yield(const DayCounter& dc,
               Compounding comp,
               Frequency freq,
               Real accuracy = 1.0e-8,
               Size maxEvaluations = 100,
               Real guess = 0.05,
               BondPrice::Type priceType = BondPrice::Clean) const;
    Real cleanPrice(Rate yield,
                    const DayCounter& dc,
                    Compounding comp,
                    Frequency freq,
                    Date settlementDate = Date()) const;
    Real dirtyPrice(Rate yield,
                    const DayCounter& dc,
                    Compounding comp,
                    Frequency freq,
                    Date settlementDate = Date()) const;
    Real settlementValue(Real cleanPrice) const;
    Rate yield(Real cleanPrice,
               const DayCounter& dc,
               Compounding comp,
               Frequency freq,
               Date settlementDate = Date(),
               Real accuracy = 1.0e-8,
               Size maxEvaluations = 100,
               Real guess = 0.05,
               BondPrice::Type priceType = BondPrice::Clean) const;
    Real accruedAmount(Date d = Date()) const;
    Rate nextCouponRate(Date d = Date()) const;
    Rate previousCouponRate(Date d = Date()) const;
    Date nextCashFlowDate(Date d = Date()) const;
    Date previousCashFlowDate(Date d = Date()) const;
};

%inline %{
    Real cleanPriceFromZSpread(
        const Bond& bond,
        const ext::shared_ptr<YieldTermStructure>& discountCurve,
        Spread zSpread,
        const DayCounter& dc,
        Compounding compounding,
        Frequency freq,
        const Date& settlementDate = Date()) {
            return QuantLib::BondFunctions::cleanPrice(
                bond,
                discountCurve,
                zSpread, dc, compounding,
                freq, settlementDate);
    }
%}

#endif
