#include <ql/pricingengines/swap/discountingswapengine.hpp>
#include <ql/time/schedule.hpp>
#include <qlex/indexes/ChinaFixingRepo.hpp>
#include <qlex/instruments/MakeChinaFixingRepoSwap.hpp>

namespace QuantLib {

MakeChinaFixingRepoSwap::MakeChinaFixingRepoSwap(const Period& swapTenor,
                                                 const ext::shared_ptr<ChinaFixingRepo>& chinaFixingRepo,
                                                 Rate fixedRate,
                                                 const Period& forwardStart)
    : swapTenor_(swapTenor),
      chinaFixingRepo_(chinaFixingRepo),
      fixedRate_(fixedRate),
      forwardStart_(forwardStart),
      settlementDays_(1),
      calendar_(chinaFixingRepo->fixingCalendar()),
      paymentFrequency_(Quarterly),
      paymentCalendar_(Calendar()),
      paymentConvention_(ModifiedFollowing),
      paymentLag_(0),
      rule_(DateGeneration::Forward),
      isDefaultEOM_(false),
      type_(ChinaFixingRepoSwap::Payer),
      nominal_(100.0),
      gearing_(1.0),
      spread_(0.0),
      fixedDayCount_(chinaFixingRepo->dayCounter()) {}

MakeChinaFixingRepoSwap::operator ChinaFixingRepoSwap() const {
    ext::shared_ptr<ChinaFixingRepoSwap> swap = *this;
    return *swap;
}

MakeChinaFixingRepoSwap::operator ext::shared_ptr<ChinaFixingRepoSwap>() const {

    Date startDate;
    if (effectiveDate_ != Date())
        startDate = effectiveDate_;
    else {
        Date refDate = Settings::instance().evaluationDate();
        // if the evaluation date is not a business day
        // then move to the next business day
        refDate = calendar_.adjust(refDate);
        Date spotDate = calendar_.advance(
            refDate, settlementDays_ * Days);
        startDate = spotDate + forwardStart_;
        if (forwardStart_.length() < 0)
            startDate = calendar_.adjust(startDate, Preceding);
        else
            startDate = calendar_.adjust(startDate, Following);
    }

    // OIS end of month default
    bool usedEndOfMonth = isDefaultEOM_ ? calendar_.isEndOfMonth(startDate) : endOfMonth_;

    Date endDate = terminationDate_;
    if (endDate == Date()) {
        if (usedEndOfMonth) {
            endDate = calendar_.advance(
                startDate,
                swapTenor_,
                ModifiedFollowing,
                usedEndOfMonth);
        } else {
            endDate = startDate + swapTenor_;
        }
    }

    Schedule schedule(
        startDate,
        endDate,
        Period(paymentFrequency_),
        calendar_,
        ModifiedFollowing,
        ModifiedFollowing,
        rule_,
        usedEndOfMonth);

    Rate usedFixedRate = fixedRate_;
    if (fixedRate_ == Null<Rate>()) {
        ChinaFixingRepoSwap temp(
            type_,
            nominal_,
            schedule,
            0.0,    // fixed rate
            fixedDayCount_,
            chinaFixingRepo_,
            gearing_,
            spread_,
            paymentLag_,
            paymentConvention_,
            paymentCalendar_);
        if (engine_ == nullptr) {
            Handle<YieldTermStructure> disc =
                chinaFixingRepo_->forwardingTermStructure();
            QL_REQUIRE(!disc.empty(),
                       "null term structure set to this instance of " << chinaFixingRepo_->name());
            bool includeSettlementDateFlows = false;
            ext::shared_ptr<PricingEngine> engine(
                new DiscountingSwapEngine(
                    disc, includeSettlementDateFlows));
            temp.setPricingEngine(engine);
        } else
            temp.setPricingEngine(engine_);

        usedFixedRate = temp.fairRate();
    }

    ext::shared_ptr<ChinaFixingRepoSwap> swap(
        new ChinaFixingRepoSwap(
            type_,
            nominal_,
            schedule,
            usedFixedRate,
            fixedDayCount_,
            chinaFixingRepo_,
            gearing_,
            spread_,
            paymentLag_,
            paymentConvention_,
            paymentCalendar_));

    if (engine_ == nullptr) {
        Handle<YieldTermStructure> disc =
            chinaFixingRepo_->forwardingTermStructure();
        bool includeSettlementDateFlows = false;
        ext::shared_ptr<PricingEngine> engine(
            new DiscountingSwapEngine(
                disc, includeSettlementDateFlows));
        swap->setPricingEngine(engine);
    } else
        swap->setPricingEngine(engine_);

    return swap;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::receiveFixed(bool flag) {
    type_ = flag ? ChinaFixingRepoSwap::Receiver : ChinaFixingRepoSwap::Payer;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withType(ChinaFixingRepoSwap::Type type) {
    type_ = type;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withNominal(Real n) {
    nominal_ = n;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withSettlementDays(Natural settlementDays) {
    settlementDays_ = settlementDays;
    effectiveDate_ = Date();
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withEffectiveDate(const Date& effectiveDate) {
    effectiveDate_ = effectiveDate;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withTerminationDate(const Date& terminationDate) {
    terminationDate_ = terminationDate;
    swapTenor_ = Period();
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withPaymentFrequency(Frequency f) {
    paymentFrequency_ = f;
    if (paymentFrequency_ == Once)
        rule_ = DateGeneration::Zero;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withPaymentAdjustment(BusinessDayConvention convention) {
    paymentConvention_ = convention;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withPaymentLag(Natural lag) {
    paymentLag_ = lag;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withPaymentCalendar(const Calendar& cal) {
    paymentCalendar_ = cal;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withRule(DateGeneration::Rule r) {
    rule_ = r;
    if (r == DateGeneration::Zero)
        paymentFrequency_ = Once;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withDiscountingTermStructure(const Handle<YieldTermStructure>& d) {
    bool includeSettlementDateFlows = false;
    engine_ = ext::shared_ptr<PricingEngine>(
        new DiscountingSwapEngine(d, includeSettlementDateFlows));
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withPricingEngine(const ext::shared_ptr<PricingEngine>& engine) {
    engine_ = engine;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withFixedLegDayCount(const DayCounter& dc) {
    fixedDayCount_ = dc;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withEndOfMonth(bool flag) {
    endOfMonth_ = flag;
    isDefaultEOM_ = false;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withFloatingLegGearing(Real gearing) {
    gearing_ = gearing;
    return *this;
}

MakeChinaFixingRepoSwap& MakeChinaFixingRepoSwap::withFloatingLegSpread(Spread sp) {
    spread_ = sp;
    return *this;
}

}    // namespace QuantLib
