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
    const Date& accrualStartDate() const;
    const Date& accrualEndDate() const;
    const Date& referencePeriodStart() const;
    const Date& referencePeriodEnd() const;
    Time accrualPeriod() const;
    BigInteger accrualDays() const;
    Real rate() const;
    DayCounter dayCounter() const;
    Time accruedPeriod(const Date &) const;
    BigInteger accruedDays(const Date &) const;
    Real accruedAmount(const Date& date) const;
};

%inline %{
    ext::shared_ptr<Coupon> as_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<Coupon>(cf);
    }
%}

#endif
