#ifndef ql_cashflows_coupons_all_i
#define ql_cashflows_coupons_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/cashflows/Coupon.i

%{
using QuantLib::RateAveraging;
using QuantLib::Replication;
using QuantLib::DigitalReplication;
%}

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
using QuantLib::YoYInflationCoupon;
using QuantLib::CappedFlooredYoYInflationCoupon;
using QuantLib::CappedFlooredIborCoupon;
using QuantLib::CappedFlooredCmsCoupon;
using QuantLib::CappedFlooredCmsSpreadCoupon;
using QuantLib::DigitalCoupon;
using QuantLib::SubPeriodsCoupon;
using QuantLib::RangeAccrualFloatersCoupon;
typedef IborCoupon::Settings IborCouponSettings;
%}

struct RateAveraging {
    enum Type { Simple, Compound };
};

struct Replication {
    enum Type { Sub, Central, Super };
};

%shared_ptr(DigitalReplication)
class DigitalReplication {
  public:
    DigitalReplication(
        Replication::Type t = Replication::Central,
        Real gap = 1e-4);
    Replication::Type replicationType() const;
    Real gap() const;
};

%shared_ptr(FixedRateCoupon)
class FixedRateCoupon : public Coupon {
  public:
    FixedRateCoupon(
        const Date& paymentDate,
        Real nominal,
        Rate rate,
        const DayCounter& dayCounter,
        const Date& accrualStartDate,
        const Date& accrualEndDate,
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const Date& exCouponDate = Date());
    FixedRateCoupon(
        const Date& paymentDate,
        Real nominal,
        InterestRate interestRate,
        const Date& accrualStartDate,
        const Date& accrualEndDate,
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
class FloatingRateCoupon : public Coupon, public Observer {
  public:
    FloatingRateCoupon(
        const Date& paymentDate,
        Real nominal,
        const Date& startDate,
        const Date& endDate,
        Natural fixingDays,
        const ext::shared_ptr<InterestRateIndex>& index,
        Real gearing = 1.0,
        Spread spread = 0.0,
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        DayCounter dayCounter = DayCounter(),
        bool isInArrears = false,
        const Date& exCouponDate = Date());
    Real price(const Handle<YieldTermStructure>& discountingCurve) const;
    const ext::shared_ptr<InterestRateIndex>& index() const;
    Natural fixingDays() const;
    Date fixingDate() const;
    Real gearing() const;
    Spread spread() const;
    Rate indexFixing() const;
    Rate convexityAdjustment() const;;
    Rate adjustedFixing() const;
    bool isInArrears() const;
    void setPricer(const ext::shared_ptr<FloatingRateCouponPricer>&);
    ext::shared_ptr<FloatingRateCouponPricer> pricer() const;
};

%inline %{
    ext::shared_ptr<FloatingRateCoupon> as_floating_rate_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<FloatingRateCoupon>(cf);
    }
%}

%shared_ptr(InflationCoupon)
class InflationCoupon : public Coupon, public Observer {
  private:
    InflationCoupon();
  public:
    Real price(const Handle<YieldTermStructure>& discountingCurve) const;
    const ext::shared_ptr<InflationIndex>& index() const;
    Period observationLag() const;
    Natural fixingDays() const;
    Date fixingDate() const;
    Rate indexFixing() const;
    void setPricer(const ext::shared_ptr<InflationCouponPricer>&);
    ext::shared_ptr<InflationCouponPricer> pricer() const;
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
        bool telescopicValueDates = false,
        RateAveraging::Type averagingMethod = RateAveraging::Compound);
    const std::vector<Date>& fixingDates() const;
    const std::vector<Time>& dt() const;
    const std::vector<Rate>& indexFixings() const;
    const std::vector<Date>& valueDates() const;
};

%shared_ptr(IborCoupon)
class IborCoupon : public FloatingRateCoupon {
    %feature("kwargs") IborCoupon;
  public:
    IborCoupon(
        const Date& paymentDate, 
        Real nominal,
        const Date& startDate,
        const Date& endDate,
        Integer fixingDays,
        ext::shared_ptr<IborIndex>& index,
        Real gearing = 1.0, 
        Spread spread = 0.0,
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const DayCounter& dayCounter = DayCounter(),
        bool isInArrears = false,
        const Date& exCouponDate = Date());

    const ext::shared_ptr<IborIndex>& iborIndex() const;
    const Date& fixingEndDate() const;
};

%inline %{
    ext::shared_ptr<IborCoupon> as_ibor_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<IborCoupon>(cf);
    }
%}

class IborCouponSettings {
  private:
    IborCouponSettings();
  public:
    static IborCouponSettings& instance();
    void createAtParCoupons();
    void createIndexedCoupons();
    bool usingAtParCoupons() const;
};

%shared_ptr(CappedFlooredCoupon)
class CappedFlooredCoupon : public FloatingRateCoupon {
    %feature("kwargs") CappedFlooredCoupon;
  public:
    CappedFlooredCoupon(
        const ext::shared_ptr<FloatingRateCoupon>& underlying,
        Rate cap = Null<Rate>(),
        Rate floor = Null<Rate>());
    Rate cap() const;
    Rate floor() const;
    Rate effectiveCap() const;
    Rate effectiveFloor() const;
    bool isCapped() const;
    bool isFloored() const;
};

%shared_ptr(CmsCoupon)
class CmsCoupon : public FloatingRateCoupon {
    %feature("kwargs") CmsCoupon;
  public:
    CmsCoupon(
        const Date& paymentDate, 
        Real nominal,
        const Date& startDate, 
        const Date& endDate,
        Integer fixingDays, 
        const ext::shared_ptr<SwapIndex>& index,
        Real gearing = 1.0, 
        Spread spread = 0.0,
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const DayCounter& dayCounter = DayCounter(),
        bool isInArrears = false,
        const Date& exCouponDate = Date());
   const ext::shared_ptr<SwapIndex>& swapIndex() const;
};

%shared_ptr(CmsSpreadCoupon)
class CmsSpreadCoupon : public FloatingRateCoupon {
    %feature("kwargs") CmsSpreadCoupon;
  public:
    CmsSpreadCoupon(
        const Date& paymentDate,
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
    const ext::shared_ptr<SwapSpreadIndex>& swapSpreadIndex() const;
};

%shared_ptr(CPICoupon)
class CPICoupon : public InflationCoupon {
  private:
    CPICoupon();
  public:
    Rate fixedRate() const;
    Spread spread() const;
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

%shared_ptr(YoYInflationCoupon)
class YoYInflationCoupon : public InflationCoupon {
  public:
    YoYInflationCoupon(
        const Date& paymentDate,
        Real nominal,
        const Date& startDate,
        const Date& endDate,
        Natural fixingDays,
        const ext::shared_ptr<YoYInflationIndex>& index,
        const Period& observationLag,
        const DayCounter& dayCounter,
        Real gearing = 1.0,
        Spread spread = 0.0,
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date());
    Real gearing() const;
    Spread spread() const;
    Rate adjustedFixing() const;
    const ext::shared_ptr<YoYInflationIndex>& yoyIndex() const;
};

%inline %{
    ext::shared_ptr<YoYInflationCoupon> as_yoy_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<YoYInflationCoupon>(cf);
    }
%}

%shared_ptr(CappedFlooredYoYInflationCoupon)
class CappedFlooredYoYInflationCoupon : public YoYInflationCoupon {
  public:
    CappedFlooredYoYInflationCoupon(
        const ext::shared_ptr<YoYInflationCoupon>& underlying,
        Rate cap = Null<Rate>(),
        Rate floor = Null<Rate>());
    CappedFlooredYoYInflationCoupon(
        const Date& paymentDate,
        Real nominal,
        const Date& startDate,
        const Date& endDate,
        Natural fixingDays,
        const ext::shared_ptr<YoYInflationIndex>& index,
        const Period& observationLag,
        const DayCounter& dayCounter,
        Real gearing = 1.0,
        Spread spread = 0.0,
        const Rate cap = Null<Rate>(),
        const Rate floor = Null<Rate>(),
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date());

    Rate cap() const;
    Rate floor() const;
    Rate effectiveCap() const;
    Rate effectiveFloor() const;
    bool isCapped() const;
    bool isFloored() const;
    void setPricer(const ext::shared_ptr<YoYInflationCouponPricer>&);
};

%shared_ptr(CappedFlooredIborCoupon)
class CappedFlooredIborCoupon : public CappedFlooredCoupon {
    %feature("kwargs") CappedFlooredIborCoupon;
  public:
    CappedFlooredIborCoupon(
        const Date& paymentDate, 
        Real nominal,
        const Date& startDate, 
        const Date& endDate,
        Integer fixingDays,
        ext::shared_ptr<IborIndex>& index,
        Real gearing = 1.0, 
        Spread spread = 0.0,
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
        const Date& paymentDate, 
        Real nominal,
        const Date& startDate, 
        const Date& endDate,
        Natural fixingDays, 
        const ext::shared_ptr<SwapIndex>& index,
        Real gearing = 1.0, 
        Spread spread = 0.0,
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
        const Date& paymentDate, 
        Real nominal,
        const Date& startDate, 
        const Date& endDate,
        Natural fixingDays,
        const ext::shared_ptr<SwapSpreadIndex>& index,
        Real gearing = 1.0, 
        Spread spread = 0.0,
        const Rate cap = Null<Rate>(),
        const Rate floor = Null<Rate>(),
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const DayCounter& dayCounter = DayCounter(),
        bool isInArrears = false,
        const Date& exCouponDate = Date());
};

%shared_ptr(DigitalCoupon)
class DigitalCoupon : public FloatingRateCoupon {
  public:
    DigitalCoupon(
        const ext::shared_ptr<FloatingRateCoupon>& underlying,
        Rate callStrike = Null<Rate>(),
        Position::Type callPosition = Position::Long,
        bool isCallITMIncluded = false,
        Rate callDigitalPayoff = Null<Rate>(),
        Rate putStrike = Null<Rate>(),
        Position::Type putPosition = Position::Long,
        bool isPutITMIncluded = false,
        Rate putDigitalPayoff = Null<Rate>(),
        const ext::shared_ptr<DigitalReplication>& replication = ext::shared_ptr<DigitalReplication>(),
        bool nakedOption = false);

    Rate callStrike() const;
    Rate putStrike() const;
    Rate callDigitalPayoff() const;
    Rate putDigitalPayoff() const;
    bool hasPut() const;
    bool hasCall() const;
    bool hasCollar() const;
    bool isLongPut() const;
    bool isLongCall() const;
    ext::shared_ptr<FloatingRateCoupon> underlying() const;
    Rate callOptionRate() const;
    Rate putOptionRate() const;
};

%shared_ptr(SubPeriodsCoupon)
class SubPeriodsCoupon: public FloatingRateCoupon {
    %feature("kwargs") SubPeriodsCoupon;
  public:
    SubPeriodsCoupon(
        const Date& paymentDate,
        Real nominal,
        const Date& startDate,
        const Date& endDate,
        Natural fixingDays,
        const ext::shared_ptr<IborIndex>& index,
        Real gearing = 1.0,
        Rate couponSpread = 0.0,
        Rate rateSpread = 0.0,
        const Date& refPeriodStart = Date(),
        const Date& refPeriodEnd = Date(),
        const DayCounter& dayCounter = DayCounter(),
        const Date& exCouponDate = Date());
    const std::vector<Date>& fixingDates() const;
    const std::vector<Time>& dt() const;
    const std::vector<Date>& valueDates() const;
    Spread rateSpread() const;
};

%inline %{
    ext::shared_ptr<SubPeriodsCoupon> as_sub_periods_coupon(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<SubPeriodsCoupon>(cf);
    }
%}

%shared_ptr(RangeAccrualFloatersCoupon)
class RangeAccrualFloatersCoupon: public FloatingRateCoupon {
  public:
    %extend {
        RangeAccrualFloatersCoupon(
            const Date& paymentDate,
            Real nominal,
            const ext::shared_ptr<IborIndex>& index,
            const Date& startDate,
            const Date& endDate,
            Natural fixingDays,
            const DayCounter& dayCounter,
            Real gearing,
            Rate spread,
            const Date& refPeriodStart,
            const Date& refPeriodEnd,
            const Schedule& observationsSchedule,
            Real lowerTrigger,
            Real upperTrigger) {
                ext::shared_ptr<Schedule> sch(new Schedule(
                    observationsSchedule.dates(),
                    observationsSchedule.calendar(),
                    observationsSchedule.businessDayConvention(),
                    observationsSchedule.terminationDateBusinessDayConvention(),
                    observationsSchedule.tenor(),
                    observationsSchedule.rule(),
                    observationsSchedule.endOfMonth(),
                    observationsSchedule.isRegular()));
                return new RangeAccrualFloatersCoupon(
                    paymentDate,
                    nominal,
                    index,
                    startDate,
                    endDate,
                    fixingDays,
                    dayCounter,
                    gearing,
                    spread,
                    refPeriodStart,
                    refPeriodEnd,
                    sch,
                    lowerTrigger,
                    upperTrigger);
            }
    }
    Real startTime() const;
    Real endTime() const;
    Real lowerTrigger() const;
    Real upperTrigger() const;
    Size observationsNo() const;
    const std::vector<Date>& observationDates() const;
    const std::vector<Real>& observationTimes() const;
    %extend {
        Schedule observationsSchedule() const {
            return *(self->observationsSchedule());
        }
    }
    Real priceWithoutOptionality(
        const Handle<YieldTermStructure>& discountCurve) const;
};

#endif
