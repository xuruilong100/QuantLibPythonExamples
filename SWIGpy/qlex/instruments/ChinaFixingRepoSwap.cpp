#include <ql/cashflows/fixedratecoupon.hpp>
#include <qlex/cashflows/ChinaFixingRepoLeg.hpp>
#include <qlex/indexes/ChinaFixingRepo.hpp>
#include <qlex/instruments/ChinaFixingRepoSwap.hpp>
#include <utility>

namespace QuantLib {

ChinaFixingRepoSwap::ChinaFixingRepoSwap(Type type,
                                         Real nominal,
                                         const Schedule& schedule,
                                         Rate fixedRate,
                                         DayCounter fixedDC,
                                         ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo,
                                         Real gearing,
                                         Spread spread,
                                         Natural paymentLag,
                                         BusinessDayConvention paymentAdjustment,
                                         const Calendar& paymentCalendar)
    : Swap(2),
      type_(type),
      nominal_(nominal),
      paymentFrequency_(schedule.tenor().frequency()),
      paymentCalendar_(paymentCalendar.empty() ? schedule.calendar() : paymentCalendar),
      paymentConvention_(paymentAdjustment),
      paymentLag_(paymentLag),
      schedule_(schedule),
      fixedRate_(fixedRate),
      fixedDC_(std::move(fixedDC)),
      chinaFixingRepo_(std::move(chinaFixingRepo)),
      gearing_(gearing),
      spread_(spread) {

    initialize(schedule);
}

void ChinaFixingRepoSwap::initialize(const Schedule& schedule) {
    if (fixedDC_ == DayCounter()) {
        fixedDC_ = chinaFixingRepo_->dayCounter();
    }

    legs_[0] = FixedRateLeg(schedule)
                   .withNotionals(nominal_)
                   .withCouponRates(fixedRate_, fixedDC_)
                   .withPaymentLag(paymentLag_)
                   .withPaymentAdjustment(paymentConvention_)
                   .withPaymentCalendar(paymentCalendar_);

    legs_[1] = ChinaFixingRepoLeg(schedule, chinaFixingRepo_)
                   .withNotional(nominal_)
                   .withSpread(spread_)
                   .withPaymentLag(paymentLag_)
                   .withPaymentAdjustment(paymentConvention_)
                   .withPaymentCalendar(paymentCalendar_);

    for (Size j = 0; j < 2; ++j) {
        for (auto& i : legs_[j])
            registerWith(i);
    }

    switch (type_) {
    case Payer:
        payer_[0] = -1.0;
        payer_[1] = +1.0;
        break;
    case Receiver:
        payer_[0] = +1.0;
        payer_[1] = -1.0;
        break;
    default:
        QL_FAIL("Unknown overnight-swap type");
    }
}

Real ChinaFixingRepoSwap::fairRate() const {
    static Spread basisPoint = 1.0e-4;
    calculate();
    return fixedRate_ - NPV_ / (fixedLegBPS() / basisPoint);
}

Spread ChinaFixingRepoSwap::fairSpread() const {
    static Spread basisPoint = 1.0e-4;
    calculate();
    return spread_ - NPV_ / (floatingLegBPS() / basisPoint);
}

Real ChinaFixingRepoSwap::fixedLegBPS() const {
    calculate();
    QL_REQUIRE(legBPS_[0] != Null<Real>(), "result not available");
    return legBPS_[0];
}

Real ChinaFixingRepoSwap::floatingLegBPS() const {
    calculate();
    QL_REQUIRE(legBPS_[1] != Null<Real>(), "result not available");
    return legBPS_[1];
}

Real ChinaFixingRepoSwap::fixedLegNPV() const {
    calculate();
    QL_REQUIRE(legNPV_[0] != Null<Real>(), "result not available");
    return legNPV_[0];
}

Real ChinaFixingRepoSwap::floatingLegNPV() const {
    calculate();
    QL_REQUIRE(legNPV_[1] != Null<Real>(), "result not available");
    return legNPV_[1];
}

}    // namespace QuantLib
