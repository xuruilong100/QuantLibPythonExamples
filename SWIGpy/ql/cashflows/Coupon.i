#ifndef ql_cashflows_Coupon_i
#define ql_cashflows_Coupon_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Coupon;
%}

%shared_ptr(Coupon)
class Coupon : public CashFlow {
  private:
    Coupon();
  public:
    Real nominal() const;
    Date accrualStartDate() const;
    Date accrualEndDate() const;
    Date referencePeriodStart() const;
    Date referencePeriodEnd() const;
    Date exCouponDate() const;
    Real rate() const;
    Time accrualPeriod() const;
    BigInteger accrualDays() const;
    DayCounter dayCounter() const;
    Real accruedAmount(const Date& date) const;
};

%inline %{
    ext::shared_ptr<Coupon> as_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<Coupon>(cf);
    }
%}

#endif
