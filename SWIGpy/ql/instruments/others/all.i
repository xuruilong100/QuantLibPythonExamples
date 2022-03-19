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
using QuantLib::ForwardRateAgreement;
using QuantLib::Stock;
using QuantLib::cdsMaturity;
using QuantLib::VarianceOption;
using QuantLib::VarianceSwap;
using QuantLib::MakeCreditDefaultSwap;
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
    %extend {
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
            const DayCounter& lastPeriodDayCounter = DayCounter(),
            bool rebatesAccrual = true,
            const Date& tradeDate = Date(),
            Natural cashSettlementDays = 3,
            ext::shared_ptr<Claim> claim = ext::shared_ptr<Claim>()) {
                return new CreditDefaultSwap(
                    side,
                    notional,
                    spread,
                    schedule,
                    paymentConvention,
                    dayCounter,
                    settlesAccrual,
                    paysAtDefaultTime,
                    protectionStart,
                    claim,
                    lastPeriodDayCounter,
                    rebatesAccrual,
                    tradeDate,
                    cashSettlementDays);
            }
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
            const DayCounter& lastPeriodDayCounter = DayCounter(),
            bool rebatesAccrual = true,
            const Date& tradeDate = Date(),
            Natural cashSettlementDays = 3,
            ext::shared_ptr<Claim> claim = ext::shared_ptr<Claim>()) {
                return new CreditDefaultSwap(
                    side,
                    notional,
                    upfront,
                    spread,
                    schedule,
                    paymentConvention,
                    dayCounter,
                    settlesAccrual,
                    paysAtDefaultTime,
                    protectionStart,
                    upfrontDate,
                    claim,
                    lastPeriodDayCounter,
                    rebatesAccrual,
                    tradeDate,
                    cashSettlementDays);
            }
    }

    Protection::Side side() const;
    Real notional() const;
    Rate runningSpread() const;
    // boost::optional<Rate> upfront() const;
    %extend {
        Real upfront() const {
            boost::optional<Rate> result = self->upfront();
            if (result)
                return *result;
            else
                return Null<Rate>();
        }
    }
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

%shared_ptr(ForwardRateAgreement)
class ForwardRateAgreement : public Instrument {
  public:
    ForwardRateAgreement(
        const Date& valueDate,
        const Date& maturityDate,
        Position::Type type,
        Rate strikeForwardRate,
        Real notionalAmount,
        const ext::shared_ptr<IborIndex>& index,
        Handle<YieldTermStructure> discountCurve = Handle<YieldTermStructure>(),
        bool useIndexedCoupon = true);
    ForwardRateAgreement(
        const Date& valueDate,
        Position::Type type,
        Rate strikeForwardRate,
        Real notionalAmount,
        const ext::shared_ptr<IborIndex>& index,
        Handle<YieldTermStructure> discountCurve = Handle<YieldTermStructure>());

    Real amount() const;
    const Calendar& calendar() const;
    BusinessDayConvention businessDayConvention() const;
    const DayCounter& dayCounter() const;
    Handle<YieldTermStructure> discountCurve() const;
    Date fixingDate() const;
    InterestRate forwardRate() const;
};

Date cdsMaturity(
    const Date& tradeDate, const Period& tenor, DateGeneration::Rule rule);

class MakeCreditDefaultSwap {
  public:
    MakeCreditDefaultSwap(const Period& tenor, Real couponRate);
    MakeCreditDefaultSwap(const Date& termDate, Real couponRate);

    MakeCreditDefaultSwap& withUpfrontRate(Real);
    MakeCreditDefaultSwap& withSide(Protection::Side);
    MakeCreditDefaultSwap& withNominal(Real);
    MakeCreditDefaultSwap& withCouponTenor(Period);
    MakeCreditDefaultSwap& withDayCounter(DayCounter&);
    MakeCreditDefaultSwap& withLastPeriodDayCounter(DayCounter&);
    MakeCreditDefaultSwap& withDateGenerationRule(DateGeneration::Rule rule);
    MakeCreditDefaultSwap& withCashSettlementDays(Natural cashSettlementDays);
    MakeCreditDefaultSwap& withPricingEngine(const ext::shared_ptr<PricingEngine>&);

    %extend {
        ext::shared_ptr<CreditDefaultSwap> makeCDS() const {
            return (ext::shared_ptr<CreditDefaultSwap>)(*self);
        }
    }
};

%shared_ptr(Stock)
class Stock : public Instrument {
  public:
    Stock(Handle<Quote> quote);
};

%shared_ptr(VarianceOption)
class VarianceOption : public Instrument {
  public:
    VarianceOption(
        ext::shared_ptr<Payoff> payoff,
        Real notional,
        const Date& startDate,
        const Date& maturityDate);
    Date startDate() const;
    Date maturityDate() const;
    Real notional() const;
    ext::shared_ptr<Payoff> payoff() const;
};

%shared_ptr(VarianceSwap)
class VarianceSwap : public Instrument {
  public:
    VarianceSwap(
        Position::Type position,
        Real strike,
        Real notional,
        const Date& startDate,
        const Date& maturityDate);
    Real strike() const;
    Position::Type position() const;
    Date startDate() const;
    Date maturityDate() const;
    Real notional() const;
    Real variance() const;
};

#endif
