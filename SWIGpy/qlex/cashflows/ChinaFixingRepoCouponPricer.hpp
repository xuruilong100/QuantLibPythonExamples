#ifndef ChinaFixingRepoCouponPricer_HPP
#define ChinaFixingRepoCouponPricer_HPP

#include <ql/cashflows/couponpricer.hpp>

namespace QuantLib {

class ChinaFixingRepoCoupon;

class ChinaFixingRepoCouponPricer : public FloatingRateCouponPricer {
  public:
    void initialize(const FloatingRateCoupon& coupon) override;

    Rate swapletRate() const override;

    Real swapletPrice() const override { QL_FAIL("swapletPrice not available"); }
    Real capletPrice(Rate) const override { QL_FAIL("capletPrice not available"); }
    Rate capletRate(Rate) const override { QL_FAIL("capletRate not available"); }
    Real floorletPrice(Rate) const override { QL_FAIL("floorletPrice not available"); }
    Rate floorletRate(Rate) const override { QL_FAIL("floorletRate not available"); }

  protected:
    const ChinaFixingRepoCoupon* coupon_;
};
}    // namespace QuantLib

#endif    // ChinaFixingRepoCouponPricer_HPP
