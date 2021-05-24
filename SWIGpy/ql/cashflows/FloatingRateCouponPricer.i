#ifndef ql_cashflows_FloatingRateCouponPricer_i
#define ql_cashflows_FloatingRateCouponPricer_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::FloatingRateCouponPricer;
%}

%shared_ptr(FloatingRateCouponPricer)
class FloatingRateCouponPricer {
  private:
    FloatingRateCouponPricer();
  public:
    virtual Real swapletPrice() const;
    virtual Rate swapletRate() const;
    virtual Real capletPrice(Rate effectiveCap) const;
    virtual Rate capletRate(Rate effectiveCap) const;
    virtual Real floorletPrice(Rate effectiveFloor) const;
    virtual Rate floorletRate(Rate effectiveFloor) const;
};

void setCouponPricer(
    const Leg&,
    const ext::shared_ptr<FloatingRateCouponPricer>&);

#endif
