#ifndef ChinaFixingRepoCoupon_HPP
#define ChinaFixingRepoCoupon_HPP

#include <ql/cashflows/floatingratecoupon.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>

namespace QuantLib {

class ChinaFixingRepo;

class ChinaFixingRepoCoupon : public FloatingRateCoupon {
  public:
    ChinaFixingRepoCoupon(
        const Date& paymentDate,
        Real nominal,
        const Date& startDate,
        const Date& endDate,
        const ext::shared_ptr<ChinaFixingRepo>& chinaFixingRepo,
        Real gearing = 1.0,
        Spread spread = 0.0,
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const DayCounter& dayCounter = Actual365Fixed(Actual365Fixed::Standard));

    const std::vector<Date>& fixingDates() const { return fixingDates_; }
    const std::vector<Time>& dt() const { return dt_; }
    const std::vector<Rate>& indexFixings() const;
    const std::vector<Date>& valueDates() const { return valueDates_; }

    Date fixingDate() const override { return fixingDates_.back(); }

    void accept(AcyclicVisitor&) override;

  private:
    std::vector<Date> valueDates_, fixingDates_;
    mutable std::vector<Rate> fixings_;
    Size n_;
    std::vector<Time> dt_;
};

}    // namespace QuantLib

#endif    // ChinaFixingRepoCoupon_HPP
