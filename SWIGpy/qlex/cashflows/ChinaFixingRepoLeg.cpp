#include <qlex/cashflows/ChinaFixingRepoCoupon.hpp>
#include <qlex/cashflows/ChinaFixingRepoLeg.hpp>

namespace QuantLib {

ChinaFixingRepoLeg::ChinaFixingRepoLeg(const Schedule& schedule,
                                       ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo)
    : schedule_(schedule),
      chinaFixingRepo_(std::move(chinaFixingRepo)),
      notional_(Null<Real>()),
      paymentCalendar_(schedule.calendar()),
      paymentConvention_(ModifiedFollowing),
      paymentLag_(0),
      gearing_(1.0),
      spread_(0.0) {}

ChinaFixingRepoLeg& ChinaFixingRepoLeg::withNotional(Real notional) {
    notional_ = notional;
    return *this;
}

ChinaFixingRepoLeg& ChinaFixingRepoLeg::withPaymentDayCounter(const DayCounter& dc) {
    paymentDayCounter_ = dc;
    return *this;
}

ChinaFixingRepoLeg& ChinaFixingRepoLeg::withPaymentAdjustment(BusinessDayConvention convention) {
    paymentConvention_ = convention;
    return *this;
}

ChinaFixingRepoLeg& ChinaFixingRepoLeg::withPaymentCalendar(const Calendar& cal) {
    paymentCalendar_ = cal;
    return *this;
}

ChinaFixingRepoLeg& ChinaFixingRepoLeg::withPaymentLag(Natural lag) {
    paymentLag_ = lag;
    return *this;
}

ChinaFixingRepoLeg& ChinaFixingRepoLeg::withGearing(Real gearing) {
    gearing_ = gearing;
    return *this;
}

ChinaFixingRepoLeg& ChinaFixingRepoLeg::withSpread(Spread spread) {
    spread_ = spread;
    return *this;
}

ChinaFixingRepoLeg::operator Leg() const {

    QL_REQUIRE(notional_ != Null<Real>(), "no notional given");

    Leg cashflows;

    Calendar calendar = schedule_.calendar();

    Date refStart, start, refEnd, end;
    Date paymentDate;

    Size n = schedule_.size() - 1;
    for (Size i = 0; i < n; ++i) {
        refStart = start = schedule_.date(i);
        refEnd = end = schedule_.date(i + 1);
        paymentDate = paymentCalendar_.advance(
            end, paymentLag_, Days, paymentConvention_);

        if (i == 0 && schedule_.hasIsRegular() && !schedule_.isRegular(i + 1)) {
            refStart = calendar.adjust(
                end - schedule_.tenor(),
                paymentConvention_);
        }
        if (i == n - 1 && schedule_.hasIsRegular() && !schedule_.isRegular(i + 1)) {
            refEnd = calendar.adjust(
                start + schedule_.tenor(),
                paymentConvention_);
        }

        cashflows.push_back(
            ext::shared_ptr<CashFlow>(
                new ChinaFixingRepoCoupon(
                    paymentDate,
                    notional_,
                    start,
                    end,
                    chinaFixingRepo_,
                    gearing_,
                    spread_,
                    refStart,
                    refEnd,
                    paymentDayCounter_)));
    }
    return cashflows;
}

}    // namespace QuantLib
