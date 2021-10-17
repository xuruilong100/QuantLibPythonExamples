#ifndef ql_instruments_others_all_i
#define ql_instruments_others_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Claim;
using QuantLib::FaceValueClaim;
using QuantLib::FaceValueAccrualClaim;
using QuantLib::CompositeInstrument;
using QuantLib::CreditDefaultSwap;
using QuantLib::Stock;
%}

%shared_ptr(Claim)
class Claim : public Observer, public Observable {
  private:
    Claim();
  public:
    Real amount(
        const Date& defaultDate,
        Real notional,
        Real recoveryRate) const;
};

%shared_ptr(FaceValueClaim)
class FaceValueClaim : public Claim {
  public:
    FaceValueClaim();
};

%shared_ptr(FaceValueAccrualClaim)
class FaceValueAccrualClaim : public Claim {
  public:
    FaceValueAccrualClaim(
        const ext::shared_ptr<Bond>& bond);
};

%shared_ptr(CompositeInstrument)
class CompositeInstrument : public Instrument {
  public:
    CompositeInstrument();
    void add(const ext::shared_ptr<Instrument>& instrument,
             Real multiplier = 1.0);
    void subtract(const ext::shared_ptr<Instrument>& instrument,
                  Real multiplier = 1.0);
};

%shared_ptr(CreditDefaultSwap)
class CreditDefaultSwap : public Instrument {
  public:
    enum PricingModel {
        Midpoint,
        ISDA
    };

    CreditDefaultSwap(
        Protection::Side side,
        Real notional,
        Rate spread,
        const Schedule& schedule,
        BusinessDayConvention paymentConvention,
        const DayCounter& dayCounter,
        bool settlesAccrual = true,
        bool paysAtDefaultTime = true,
        const Date& protectionStart = Date(),
        ext::shared_ptr<Claim> = ext::shared_ptr<Claim>(),
        const DayCounter& lastPeriodDayCounter = DayCounter(),
        bool rebatesAccrual = true,
        const Date& tradeDate = Date(),
        Natural cashSettlementDays = 3);
    CreditDefaultSwap(
        Protection::Side side,
        Real notional,
        Rate upfront,
        Rate spread,
        const Schedule& schedule,
        BusinessDayConvention paymentConvention,
        const DayCounter& dayCounter,
        bool settlesAccrual = true,
        bool paysAtDefaultTime = true,
        const Date& protectionStart = Date(),
        const Date& upfrontDate = Date(),
        ext::shared_ptr<Claim> = ext::shared_ptr<Claim>(),
        const DayCounter& lastPeriodDayCounter = DayCounter(),
        bool rebatesAccrual = true,
        const Date& tradeDate = Date(),
        Natural cashSettlementDays = 3);

    Protection::Side side() const;
    Real notional() const;
    Rate runningSpread() const;
    boost::optional<Rate> upfront() const;
    /* %extend {
        Real upfront() const {
            boost::optional<Rate> result =
                self->upfront();
            if (result)
                return *result;
            else
                return Null<double>();
        }
    } */
    bool settlesAccrual() const;
    bool paysAtDefaultTime() const;
    const Leg& coupons() const;
    const Date& protectionStartDate() const;
    const Date& protectionEndDate() const;
    bool rebatesAccrual() const;
    const ext::shared_ptr<SimpleCashFlow>& upfrontPayment() const;
    const ext::shared_ptr<SimpleCashFlow>& accrualRebate() const;
    const Date& tradeDate() const;
    Natural cashSettlementDays() const;
    Rate fairUpfront() const;
    Rate fairSpread() const;
    Real couponLegBPS() const;
    Real upfrontBPS() const;
    Real couponLegNPV() const;
    Real defaultLegNPV() const;
    Real upfrontNPV() const;
    Real accrualRebateNPV() const;
    Rate impliedHazardRate(
        Real targetNPV,
        const Handle<YieldTermStructure>& discountCurve,
        const DayCounter& dayCounter,
        Real recoveryRate = 0.4,
        Real accuracy = 1.0e-8,
        PricingModel model = Midpoint) const;
    Rate conventionalSpread(
        Real conventionalRecovery,
        const Handle<YieldTermStructure>& discountCurve,
        const DayCounter& dayCounter,
        PricingModel model = Midpoint) const;
};

%shared_ptr(Stock)
class Stock : public Instrument {
  public:
    Stock(Handle<Quote> quote);
};

#endif
