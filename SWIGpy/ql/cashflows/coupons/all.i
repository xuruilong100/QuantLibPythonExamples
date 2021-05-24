#ifndef ql_cashflows_coupons_all_i
#define ql_cashflows_coupons_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/cashflows/Coupon.i

%{
using QuantLib::FixedRateCoupon;
using QuantLib::FloatingRateCoupon;
using QuantLib::InflationCoupon;
using QuantLib::OvernightIndexedCoupon;
using QuantLib::CappedFlooredCoupon;
using QuantLib::IborCoupon;
using QuantLib::CmsCoupon;
using QuantLib::CmsSpreadCoupon;
using QuantLib::CPICoupon;
using QuantLib::CappedFlooredIborCoupon;
using QuantLib::CappedFlooredCmsCoupon;
using QuantLib::CappedFlooredCmsSpreadCoupon;
%}

%shared_ptr(FixedRateCoupon)
class FixedRateCoupon : public Coupon {
    %feature("kwargs") FixedRateCoupon;
  public:
    FixedRateCoupon(const Date& paymentDate, Real nominal,
                    Rate rate, const DayCounter& dayCounter,
                    const Date& startDate, const Date& endDate,
                    const Date& refPeriodStart = Date(),
                    const Date& refPeriodEnd = Date(),
                    const Date& exCouponDate = Date());
    InterestRate interestRate() const;
};

%inline %{
    ext::shared_ptr<FixedRateCoupon> as_fixed_rate_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<FixedRateCoupon>(cf);
    }
%}

%shared_ptr(FloatingRateCoupon)
class FloatingRateCoupon : public Coupon {
  private:
    FloatingRateCoupon();
  public:
    Date fixingDate() const;
    Integer fixingDays() const;
    bool isInArrears() const;
    Real gearing() const;
    Rate spread() const;
    Rate indexFixing() const;
    Rate adjustedFixing() const;
    Rate convexityAdjustment() const;
    Real price(const Handle<YieldTermStructure>& discountCurve) const;
    ext::shared_ptr<InterestRateIndex> index() const;
    void setPricer(const ext::shared_ptr<FloatingRateCouponPricer>& p);
};

%inline %{
    ext::shared_ptr<FloatingRateCoupon> as_floating_rate_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<FloatingRateCoupon>(cf);
    }
%}

%shared_ptr(InflationCoupon)
class InflationCoupon : public Coupon {
  private:
    InflationCoupon();
  public:
    Date fixingDate() const;
    Integer fixingDays() const;
    Period observationLag() const;
    Rate indexFixing() const;
    ext::shared_ptr<InflationIndex> index() const;
};

%inline %{
    ext::shared_ptr<InflationCoupon> as_inflation_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<InflationCoupon>(cf);
    }
%}

%shared_ptr(OvernightIndexedCoupon)
class OvernightIndexedCoupon : public FloatingRateCoupon {
  public:
    OvernightIndexedCoupon(
        const Date& paymentDate,
        Real nominal,
        const Date& startDate,
        const Date& endDate,
        const ext::shared_ptr<OvernightIndex>& overnightIndex,
        Real gearing = 1.0,
        Spread spread = 0.0,
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const DayCounter& dayCounter = DayCounter(),
        bool telescopicValueDates = false);
    const std::vector<Date>& fixingDates() const;
    const std::vector<Time>& dt() const;
    const std::vector<Rate>& indexFixings() const;
    const std::vector<Date>& valueDates() const;
};

%shared_ptr(IborCoupon)
class IborCoupon : public FloatingRateCoupon {
    %feature("kwargs") IborCoupon;
  public:
    IborCoupon(const Date& paymentDate, Real nominal,
               const Date& startDate, const Date& endDate,
               Integer fixingDays,
               ext::shared_ptr<IborIndex>& index,
               Real gearing = 1.0, Spread spread = 0.0,
               const Date& refPeriodStart = Date(),
               const Date& refPeriodEnd = Date(),
               const DayCounter& dayCounter = DayCounter(),
               bool isInArrears = false,
               const Date& exCouponDate = Date());
    static void createAtParCoupons();
    static void createIndexedCoupons();
    static bool usingAtParCoupons();
};

%shared_ptr(CappedFlooredCoupon)
class CappedFlooredCoupon : public FloatingRateCoupon {
    %feature("kwargs") CappedFlooredCoupon;
  public:
    CappedFlooredCoupon(const ext::shared_ptr<FloatingRateCoupon>& underlying,
                        Rate cap = Null<Rate>(),
                        Rate floor = Null<Rate>());
    Rate cap() const;
    Rate floor() const;
    Rate effectiveCap() const;
    Rate effectiveFloor() const;
    bool isCapped() const;
    bool isFloored() const;
    void setPricer(const ext::shared_ptr<FloatingRateCouponPricer>& p);
};

%shared_ptr(CmsCoupon)
class CmsCoupon : public FloatingRateCoupon {
    %feature("kwargs") CmsCoupon;
  public:
    CmsCoupon(const Date& paymentDate, Real nominal,
              const Date& startDate, const Date& endDate,
              Integer fixingDays, const ext::shared_ptr<SwapIndex>& index,
              Real gearing = 1.0, Spread spread = 0.0,
              const Date& refPeriodStart = Date(),
              const Date& refPeriodEnd = Date(),
              const DayCounter& dayCounter = DayCounter(),
              bool isInArrears = false,
              const Date& exCouponDate = Date());
};

%shared_ptr(CmsSpreadCoupon)
class CmsSpreadCoupon : public FloatingRateCoupon {
    %feature("kwargs") CmsSpreadCoupon;
  public:
    CmsSpreadCoupon(const Date& paymentDate,
                    Real nominal,
                    const Date& startDate,
                    const Date& endDate,
                    Natural fixingDays,
                    const ext::shared_ptr<SwapSpreadIndex>& index,
                    Real gearing = 1.0,
                    Spread spread = 0.0,
                    const Date& refPeriodStart = Date(),
                    const Date& refPeriodEnd = Date(),
                    const DayCounter& dayCounter = DayCounter(),
                    bool isInArrears = false,
                    const Date& exCouponDate = Date());
};

%shared_ptr(CPICoupon)
class CPICoupon : public InflationCoupon {
  private:
    CPICoupon();
  public:
    Rate fixedRate() const;
    Spread spread() const;
    Rate adjustedFixing() const;
    Rate baseCPI() const;
    CPI::InterpolationType observationInterpolation() const;
    ext::shared_ptr<ZeroInflationIndex> cpiIndex() const;
};

%inline %{
    ext::shared_ptr<CPICoupon> as_cpi_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<CPICoupon>(cf);
    }
%}

%shared_ptr(CappedFlooredIborCoupon)
class CappedFlooredIborCoupon : public CappedFlooredCoupon {
    %feature("kwargs") CappedFlooredIborCoupon;
  public:
    CappedFlooredIborCoupon(const Date& paymentDate, Real nominal,
                            const Date& startDate, const Date& endDate,
                            Integer fixingDays,
                            ext::shared_ptr<IborIndex>& index,
                            Real gearing = 1.0, Spread spread = 0.0,
                            const Rate cap = Null<Rate>(),
                            const Rate floor = Null<Rate>(),
                            const Date& refPeriodStart = Date(),
                            const Date& refPeriodEnd = Date(),
                            const DayCounter& dayCounter = DayCounter(),
                            bool isInArrears = false,
                            const Date& exCouponDate = Date());
};

%shared_ptr(CappedFlooredCmsCoupon)
class CappedFlooredCmsCoupon: public CappedFlooredCoupon {
    %feature("kwargs") CappedFlooredCoupon;
  public:
    CappedFlooredCmsCoupon(
        const Date& paymentDate, Real nominal,
        const Date& startDate, const Date& endDate,
        Natural fixingDays, const ext::shared_ptr<SwapIndex>& index,
        Real gearing = 1.0, Spread spread = 0.0,
        const Rate cap = Null<Rate>(),
        const Rate floor = Null<Rate>(),
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const DayCounter& dayCounter = DayCounter(),
        bool isInArrears = false,
        const Date& exCouponDate = Date());
};

%shared_ptr(CappedFlooredCmsSpreadCoupon)
class CappedFlooredCmsSpreadCoupon: public CappedFlooredCoupon {
    %feature("kwargs") CappedFlooredCoupon;
  public:
    CappedFlooredCmsSpreadCoupon(
        const Date& paymentDate, Real nominal,
        const Date& startDate, const Date& endDate,
        Natural fixingDays,
        const ext::shared_ptr<SwapSpreadIndex>& index,
        Real gearing = 1.0, Spread spread = 0.0,
        const Rate cap = Null<Rate>(),
        const Rate floor = Null<Rate>(),
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const DayCounter& dayCounter = DayCounter(),
        bool isInArrears = false,
        const Date& exCouponDate = Date());
};

#endif
