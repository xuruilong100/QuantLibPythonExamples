#include <ql/time/schedule.hpp>
#include <qlex/cashflows/ChinaFixingRepoCoupon.hpp>
#include <qlex/cashflows/ChinaFixingRepoCouponPricer.hpp>
#include <qlex/indexes/ChinaFixingRepo.hpp>
#include <vector>

namespace QuantLib {

ChinaFixingRepoCoupon::ChinaFixingRepoCoupon(
    const Date& paymentDate,
    Real nominal,
    const Date& startDate,
    const Date& endDate,
    const ext::shared_ptr<ChinaFixingRepo>& chinaFixingRepo,
    Real gearing,
    Spread spread,
    const Date& refPeriodStart,
    const Date& refPeriodEnd,
    const DayCounter& dayCounter)
    : FloatingRateCoupon(
        paymentDate,
        nominal,
        startDate,
        endDate,
        chinaFixingRepo->fixingDays(),
        chinaFixingRepo,
        gearing,
        spread,
        refPeriodStart,
        refPeriodEnd,
        dayCounter,
        false) {
    using namespace std;

    Schedule sch = MakeSchedule()
                       .from(startDate)
                       .to(endDate)
                       .withTenor(chinaFixingRepo->tenor())
                       .withCalendar(chinaFixingRepo->fixingCalendar())
                       .withConvention(chinaFixingRepo->businessDayConvention())
                       .forwards();

    valueDates_ = sch.dates();

    QL_ENSURE(valueDates_.size() >= 2, "degenerate schedule");

    n_ = valueDates_.size() - 1;
    if (chinaFixingRepo->fixingDays() == 0) {
        fixingDates_ = vector<Date>(
            valueDates_.begin(), valueDates_.end() - 1);
    } else {
        fixingDates_.resize(n_);
        for (Size i = 0; i < n_; ++i) {
            fixingDates_[i] = chinaFixingRepo->fixingDate(valueDates_[i]);
        }
    }

    dt_.resize(n_);
    const DayCounter& dc = chinaFixingRepo->dayCounter();
    for (Size i = 0; i < n_; ++i) {
        dt_[i] = dc.yearFraction(
            valueDates_[i], valueDates_[i + 1]);
    }

    setPricer(
        ext::shared_ptr<FloatingRateCouponPricer>(
            new ChinaFixingRepoCouponPricer));
}

const std::vector<Rate>& ChinaFixingRepoCoupon::indexFixings() const {
    fixings_.resize(n_);
    for (Size i = 0; i < n_; ++i) {
        fixings_[i] = index_->fixing(fixingDates_[i]);
    }
    return fixings_;
}

void ChinaFixingRepoCoupon::accept(AcyclicVisitor& v) {
    auto* v1 = dynamic_cast<Visitor<ChinaFixingRepoCoupon>*>(&v);
    if (v1 != nullptr) {
        v1->visit(*this);
    } else {
        FloatingRateCoupon::accept(v);
    }
}

}    // namespace QuantLib
