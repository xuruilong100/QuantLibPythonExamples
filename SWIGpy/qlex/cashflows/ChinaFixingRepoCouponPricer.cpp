#include <qlex/cashflows/ChinaFixingRepoCoupon.hpp>
#include <qlex/cashflows/ChinaFixingRepoCouponPricer.hpp>
#include <qlex/indexes/ChinaFixingRepo.hpp>

namespace QuantLib {

void ChinaFixingRepoCouponPricer::initialize(const FloatingRateCoupon& coupon) {
    coupon_ = dynamic_cast<const ChinaFixingRepoCoupon*>(&coupon);
    QL_ENSURE(coupon_, "wrong coupon type");
}

Rate ChinaFixingRepoCouponPricer::swapletRate() const {
    using namespace std;

    ext::shared_ptr<ChinaFixingRepo> index =
        ext::dynamic_pointer_cast<ChinaFixingRepo>(coupon_->index());

    const vector<Date>& fixingDates = coupon_->fixingDates();
    const vector<Time>& dt = coupon_->dt();

    Size n = dt.size(), i = 0;

    Real compoundFactor = 1.0;

    // already fixed part
    Date today = Settings::instance().evaluationDate();
    while (i < n && fixingDates[i] < today) {
        // rate must have been fixed
        Rate pastFixing = IndexManager::instance()
                              .getHistory(index->name())[fixingDates[i]];
        QL_REQUIRE(pastFixing != Null<Real>(),
                   "Missing " << index->name() << " fixing for " << fixingDates[i]);
        compoundFactor *= (1.0 + pastFixing * dt[i]);
        ++i;
    }

    // today is a border case
    if (i < n && fixingDates[i] == today) {
        // might have been fixed
        try {
            Rate pastFixing = IndexManager::instance()
                                  .getHistory(index->name())[fixingDates[i]];
            if (pastFixing != Null<Real>()) {
                compoundFactor *= (1.0 + pastFixing * dt[i]);
                ++i;
            } else {
                ;    // fall through and forecast
            }
        } catch (Error&) {
            ;    // fall through and forecast
        }
    }

    // forward part using telescopic property in order
    // to avoid the evaluation of multiple forward fixings
    if (i < n) {
        Handle<YieldTermStructure> curve = index->forwardingTermStructure();
        QL_REQUIRE(!curve.empty(),
                   "null term structure set to this instance of " << index->name());

        const vector<Date>& dates = coupon_->valueDates();
        DiscountFactor startDiscount = curve->discount(dates[i]);
        DiscountFactor endDiscount = curve->discount(dates[n]);

        compoundFactor *= startDiscount / endDiscount;
    }

    Rate rate = (compoundFactor - 1.0) / coupon_->accrualPeriod();
    return coupon_->gearing() * rate + coupon_->spread();
}

}    // namespace QuantLib
