#ifndef ql_instruments_Bond_i
#define ql_instruments_Bond_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Bond;
%}

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
    // public functions
    Rate nextCouponRate(const Date& d = Date());
    Rate previousCouponRate(const Date& d = Date());
    // inspectors
    Natural settlementDays() const;
    Date settlementDate(Date d = Date());
    Date startDate() const;
    Date maturityDate() const;
    Date issueDate() const;
    std::vector<ext::shared_ptr<CashFlow> > cashflows() const;
    std::vector<ext::shared_ptr<CashFlow> > redemptions() const;
    ext::shared_ptr<CashFlow> redemption() const;
    Calendar calendar() const;
    std::vector<Real> notionals() const;
    Real notional(Date d = Date()) const;
    // calculations
    Real cleanPrice();
    Real cleanPrice(Rate yield,
                    const DayCounter &dc,
                    Compounding compounding,
                    Frequency frequency,
                    const Date& settlement = Date());
    Real dirtyPrice();
    Real dirtyPrice(Rate yield,
                    const DayCounter &dc,
                    Compounding compounding,
                    Frequency frequency,
                    const Date& settlement = Date());
    Real yield(const DayCounter& dc,
               Compounding compounding,
               Frequency freq,
               Real accuracy = 1.0e-8,
               Size maxEvaluations = 100);
    Real yield(Real cleanPrice,
               const DayCounter& dc,
               Compounding compounding,
               Frequency freq,
               const Date& settlement = Date(),
               Real accuracy = 1.0e-8,
               Size maxEvaluations = 100);
    Real accruedAmount(const Date& settlement = Date());
    Real settlementValue() const;
    Real settlementValue(Real cleanPrice) const;
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
