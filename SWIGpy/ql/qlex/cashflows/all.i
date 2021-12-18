#ifndef qlex_cashflows_all
#define qlex_cashflows_all

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/cashflows/coupons/all.i

%{
using QuantLib::ChinaFixingRepoCoupon;
using QuantLib::ChinaFixingRepoCouponPricer;
%}

%shared_ptr(ChinaFixingRepoCoupon)
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

    const std::vector<Date>& fixingDates() const;
    const std::vector<Time>& dt() const;
    const std::vector<Rate>& indexFixings() const;
    const std::vector<Date>& valueDates() const;
};

%shared_ptr(ChinaFixingRepoCouponPricer)
class ChinaFixingRepoCouponPricer : public FloatingRateCouponPricer {
};

#endif
