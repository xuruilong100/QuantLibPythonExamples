#ifndef qlex_instruments_all
#define qlex_instruments_all

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/instruments/Swap.i

%{
using QuantLib::ChinaFixingRepoSwap;
using QuantLib::MakeChinaFixingRepoSwap;
%}

%shared_ptr(ChinaFixingRepoSwap)
class ChinaFixingRepoSwap : public Swap {
  public:
    ChinaFixingRepoSwap(Type type,
                        Real nominal,
                        const Schedule& schedule,
                        Rate fixedRate,
                        DayCounter fixedDC,
                        ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo,
                        Real gearing = 1.0,
                        Spread spread = 0.0,
                        Natural paymentLag = 0,
                        BusinessDayConvention paymentAdjustment = ModifiedFollowing,
                        const Calendar& paymentCalendar = China(China::IB));

    Type type() const;
    Real nominal() const;
    Frequency paymentFrequency();
    const Schedule& schedule() const;
    Rate fixedRate() const;
    const DayCounter& dayCount();
    const ext::shared_ptr<ChinaFixingRepo>& chinaFixingRepo();
    Real gearing() const;
    Spread spread() const;
    BusinessDayConvention paymentConvention() const;
    const Leg& fixedLeg() const;
    const Leg& floatingLeg() const;

    Real fixedLegBPS() const;
    Real fixedLegNPV() const;
    Real fairRate() const;

    Real floatingLegBPS() const;
    Real floatingLegNPV() const;
    Spread fairSpread() const;
};

class MakeChinaFixingRepoSwap {
  public:
    MakeChinaFixingRepoSwap(const Period& swapTenor,
                            const ext::shared_ptr<ChinaFixingRepo>& chinaFixingRepo,
                            Rate fixedRate = Null<Rate>(),
                            const Period& fwdStart = 0 * Days);

    %extend{
        ext::shared_ptr<ChinaFixingRepoSwap> makeChinaFixingRepoSwap(){
            return (ext::shared_ptr<ChinaFixingRepoSwap>)(*self);
        }
    }

    MakeChinaFixingRepoSwap& receiveFixed(bool flag = true);
    MakeChinaFixingRepoSwap& withType(ChinaFixingRepoSwap::Type type);
    MakeChinaFixingRepoSwap& withNominal(Real n);
    MakeChinaFixingRepoSwap& withSettlementDays(Natural settlementDays);
    MakeChinaFixingRepoSwap& withEffectiveDate(const Date&);
    MakeChinaFixingRepoSwap& withTerminationDate(const Date&);
    MakeChinaFixingRepoSwap& withRule(DateGeneration::Rule r);
    MakeChinaFixingRepoSwap& withPaymentFrequency(Frequency f);
    MakeChinaFixingRepoSwap& withPaymentAdjustment(BusinessDayConvention convention);
    MakeChinaFixingRepoSwap& withPaymentLag(Natural lag);
    MakeChinaFixingRepoSwap& withPaymentCalendar(const Calendar& cal);
    MakeChinaFixingRepoSwap& withEndOfMonth(bool flag = true);
    MakeChinaFixingRepoSwap& withFixedLegDayCount(const DayCounter& dc);
    MakeChinaFixingRepoSwap& withFloatingLegGearing(Real gearing);
    MakeChinaFixingRepoSwap& withFloatingLegSpread(Spread sp);
    MakeChinaFixingRepoSwap& withDiscountingTermStructure(
        const Handle<YieldTermStructure>& discountingTermStructure);
    MakeChinaFixingRepoSwap& withPricingEngine(
        const ext::shared_ptr<PricingEngine>& engine);
};

#endif
