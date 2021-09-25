#ifndef ql_instruments_bonds_all_i
#define ql_instruments_bonds_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/Bond.i

%{
using QuantLib::AmortizingCmsRateBond;
using QuantLib::AmortizingFixedRateBond;
using QuantLib::AmortizingFloatingRateBond;
using QuantLib::CPIBond;
using QuantLib::CmsRateBond;
using QuantLib::ZeroCouponBond;
using QuantLib::CallableBond;
using QuantLib::FixedRateBond;
using QuantLib::FloatingRateBond;
using QuantLib::CallableFixedRateBond;
using QuantLib::CallableZeroCouponBond;
using QuantLib::ConvertibleBond;
using QuantLib::ConvertibleFixedCouponBond;
using QuantLib::ConvertibleFloatingRateBond;
using QuantLib::ConvertibleZeroCouponBond;
%}

%shared_ptr(AmortizingCmsRateBond)
class AmortizingCmsRateBond : public Bond {
    %feature("kwargs") AmortizingCmsRateBond;
  public:
    AmortizingCmsRateBond(
        Natural settlementDays,
        const std::vector<Real>& notionals,
        const Schedule& schedule,
        const ext::shared_ptr<SwapIndex>& index,
        const DayCounter& paymentDayCounter,
        BusinessDayConvention paymentConvention = Following,
        Natural fixingDays = Null<Natural>(),
        const std::vector<Real>& gearings = std::vector<Real>(1, 1.0),
        const std::vector<Spread>& spreads = std::vector<Spread>(1, 0.0),
        const std::vector<Rate>& caps = std::vector<Rate>(),
        const std::vector<Rate>& floors = std::vector<Rate>(),
        bool inArrears = false,
        const Date& issueDate = Date());
};

%shared_ptr(AmortizingFixedRateBond)
class AmortizingFixedRateBond : public Bond {
  public:
    AmortizingFixedRateBond(
        Natural settlementDays,
        const std::vector<Real>& notionals,
        const Schedule& schedule,
        const std::vector<Rate>& coupons,
        const DayCounter& accrualDayCounter,
        BusinessDayConvention paymentConvention = QuantLib::Following,
        Date issueDate = Date(),
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        const BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
    AmortizingFixedRateBond(
        Natural settlementDays,
        const Calendar& paymentCalendar,
        Real faceAmount,
        Date startDate,
        const Period& bondTenor,
        const Frequency& sinkingFrequency,
        Real coupon,
        const DayCounter& accrualDayCounter,
        BusinessDayConvention paymentConvention = QuantLib::Following,
        Date issueDate = Date());
    AmortizingFixedRateBond(
        Natural settlementDays,
        const std::vector<Real>& notionals,
        const Schedule& schedule,
        const std::vector<InterestRate>& coupons,
        BusinessDayConvention paymentConvention = QuantLib::Following,
        Date issueDate = Date(),
        const Calendar& paymentCalendar = Calendar(),
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        const BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
    Frequency frequency() const;
    DayCounter dayCounter() const;
};

%shared_ptr(AmortizingFloatingRateBond)
class AmortizingFloatingRateBond : public Bond {
    %feature("kwargs") AmortizingFloatingRateBond;
  public:
    AmortizingFloatingRateBond(
        Size settlementDays,
        const std::vector<Real>& notional,
        const Schedule& schedule,
        const ext::shared_ptr<IborIndex>& index,
        const DayCounter& accrualDayCounter,
        BusinessDayConvention paymentConvention = Following,
        Size fixingDays = Null<Size>(),
        const std::vector<Real>& gearings = std::vector<Real>(1, 1.0),
        const std::vector<Spread>& spreads = std::vector<Spread>(1, 0.0),
        const std::vector<Rate>& caps = std::vector<Rate>(),
        const std::vector<Rate>& floors = std::vector<Rate>(),
        bool inArrears = false,
        const Date& issueDate = Date(),
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        const BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
};

%shared_ptr(CPIBond)
class CPIBond : public Bond {
    %feature("kwargs") CPIBond;
  public:
    CPIBond(
        Natural settlementDays,
        Real faceAmount,
        bool growthOnly,
        Real baseCPI,
        const Period& observationLag,
        const ext::shared_ptr<ZeroInflationIndex>& cpiIndex,
        CPI::InterpolationType observationInterpolation,
        const Schedule& schedule,
        const std::vector<Rate>& coupons,
        const DayCounter& accrualDayCounter,
        BusinessDayConvention paymentConvention = ModifiedFollowing,
        const Date& issueDate = Date(),
        const Calendar& paymentCalendar = Calendar(),
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
    Frequency frequency() const;
    const DayCounter& dayCounter() const;
    bool growthOnly() const;
    Real baseCPI() const;
    Period observationLag() const;
    const ext::shared_ptr<ZeroInflationIndex>& cpiIndex() const;
    CPI::InterpolationType observationInterpolation() const;
};

%shared_ptr(CmsRateBond)
class CmsRateBond : public Bond {
    %feature("kwargs") CmsRateBond;
  public:
    CmsRateBond(
        Size settlementDays,
        Real faceAmount,
        const Schedule& schedule,
        const ext::shared_ptr<SwapIndex>& index,
        const DayCounter& paymentDayCounter,
        BusinessDayConvention paymentConvention,
        Natural fixingDays,
        const std::vector<Real>& gearings,
        const std::vector<Spread>& spreads,
        const std::vector<Rate>& caps,
        const std::vector<Rate>& floors,
        bool inArrears = false,
        Real redemption = 100.0,
        const Date& issueDate = Date());
};

%shared_ptr(CallableBond)
class CallableBond : public Bond {
  private:
    CallableBond();

  public:
    const CallabilitySchedule& callability() const;
    Volatility impliedVolatility(
        Real targetValue,
        const Handle<YieldTermStructure>& discountCurve,
        Real accuracy,
        Size maxEvaluations,
        Volatility minVol,
        Volatility maxVol) const;
    Real OAS(
        Real cleanPrice,
        const Handle<YieldTermStructure>& engineTS,
        const DayCounter& dc,
        Compounding compounding,
        Frequency freq,
        const Date& settlementDate = Date(),
        Real accuracy = 1e-10,
        Size maxIterations = 100,
        Spread guess = 0.0);
    Real cleanPriceOAS(
        Real oas,
        const Handle<YieldTermStructure>& engineTS,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Date settlementDate = Date());
    Real effectiveDuration(
        Real oas,
        const Handle<YieldTermStructure>& engineTS,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Real bump = 2e-4);
    Real effectiveConvexity(
        Real oas,
        const Handle<YieldTermStructure>& engineTS,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Real bump = 2e-4);
};

%shared_ptr(FixedRateBond)
class FixedRateBond : public Bond {
  public:
    FixedRateBond(
        Natural settlementDays,
        Real faceAmount,
        const Schedule& schedule,
        const std::vector<Rate>& coupons,
        const DayCounter& paymentDayCounter,
        BusinessDayConvention paymentConvention = QuantLib::Following,
        Real redemption = 100.0,
        Date issueDate = Date(),
        const Calendar& paymentCalendar = Calendar(),
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
    FixedRateBond(
        Natural settlementDays,
        Real faceAmount,
        const Schedule& schedule,
        const std::vector<InterestRate>& coupons,
        BusinessDayConvention paymentConvention = Following,
        Real redemption = 100.0,
        const Date& issueDate = Date(),
        const Calendar& paymentCalendar = Calendar(),
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
    FixedRateBond(
        Natural settlementDays,
        const Calendar& couponCalendar,
        Real faceAmount,
        const Date& startDate,
        const Date& maturityDate,
        const Period& tenor,
        const std::vector<Rate>& coupons,
        const DayCounter& accrualDayCounter,
        BusinessDayConvention accrualConvention = QuantLib::Following,
        BusinessDayConvention paymentConvention = QuantLib::Following,
        Real redemption = 100.0,
        const Date& issueDate = Date(),
        const Date& stubDate = Date(),
        DateGeneration::Rule rule = QuantLib::DateGeneration::Backward,
        bool endOfMonth = false,
        const Calendar& paymentCalendar = Calendar(),
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        const BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);

    Frequency frequency() const;
    const DayCounter& dayCounter() const;
    const DayCounter& firstPeriodDayCounter() const;
};

%shared_ptr(FloatingRateBond)
class FloatingRateBond : public Bond {
    public:
    FloatingRateBond(Natural settlementDays,
                     Real faceAmount,
                     const Schedule& schedule,
                     const ext::shared_ptr<IborIndex>& iborIndex,
                     const DayCounter& accrualDayCounter,
                     BusinessDayConvention paymentConvention = Following,
                     Natural fixingDays = Null<Natural>(),
                     const std::vector<Real>& gearings = std::vector<Real>(1, 1.0),
                     const std::vector<Spread>& spreads = std::vector<Spread>(1, 0.0),
                     const std::vector<Rate>& caps = std::vector<Rate>(),
                     const std::vector<Rate>& floors = std::vector<Rate>(),
                     bool inArrears = false,
                     Real redemption = 100.0,
                     const Date& issueDate = Date(),
                     const Period& exCouponPeriod = Period(),
                     const Calendar& exCouponCalendar = Calendar(),
                     BusinessDayConvention exCouponConvention = Unadjusted,
                     bool exCouponEndOfMonth = false);
    FloatingRateBond(Natural settlementDays,
                     Real faceAmount,
                     const Date& startDate,
                     const Date& maturityDate,
                     Frequency couponFrequency,
                     const Calendar& calendar,
                     const ext::shared_ptr<IborIndex>& iborIndex,
                     const DayCounter& accrualDayCounter,
                     BusinessDayConvention accrualConvention = Following,
                     BusinessDayConvention paymentConvention = Following,
                     Natural fixingDays = Null<Natural>(),
                     const std::vector<Real>& gearings = std::vector<Real>(1, 1.0),
                     const std::vector<Spread>& spreads = std::vector<Spread>(1, 0.0),
                     const std::vector<Rate>& caps = std::vector<Rate>(),
                     const std::vector<Rate>& floors = std::vector<Rate>(),
                     bool inArrears = false,
                     Real redemption = 100.0,
                     const Date& issueDate = Date(),
                     const Date& stubDate = Date(),
                     DateGeneration::Rule rule = DateGeneration::Backward,
                     bool endOfMonth = false,
                     const Period& exCouponPeriod = Period(),
                     const Calendar& exCouponCalendar = Calendar(),
                     BusinessDayConvention exCouponConvention = Unadjusted,
                     bool exCouponEndOfMonth = false);
};

%shared_ptr(CallableFixedRateBond)
class CallableFixedRateBond : public CallableBond {
    %feature("kwargs") CallableFixedRateBond;
  public:
    CallableFixedRateBond(
        Natural settlementDays,
        Real faceAmount,
        const Schedule &schedule,
        const std::vector<Rate>& coupons,
        const DayCounter& accrualDayCounter,
        BusinessDayConvention paymentConvention,
        Real redemption,
        Date issueDate,
        const std::vector<ext::shared_ptr<Callability> >& putCallSchedule,
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
};

%shared_ptr(CallableZeroCouponBond)
class CallableZeroCouponBond : public CallableBond {
    %feature("kwargs") CallableZeroCouponBond;
  public:
    CallableZeroCouponBond(
        Natural settlementDays,
        Real faceAmount,
        const Calendar& calendar,
        const Date& maturityDate,
        const DayCounter& dayCounter,
        BusinessDayConvention paymentConvention = Following,
        Real redemption = 100.0,
        const Date& issueDate = Date(),
        const std::vector<ext::shared_ptr<Callability> >& putCallSchedule = std::vector<ext::shared_ptr<Callability> >());
};

%shared_ptr(ConvertibleBond)
class ConvertibleBond : public Bond {
  private:
    ConvertibleBond();
  public:
    Real conversionRatio() const;
    const DividendSchedule& dividends() const;
    const CallabilitySchedule& callability() const;
    const Handle<Quote>& creditSpread() const;
};

%shared_ptr(ConvertibleFixedCouponBond)
class ConvertibleFixedCouponBond : public ConvertibleBond {
  public:
    ConvertibleFixedCouponBond(
        const ext::shared_ptr<Exercise>& exercise,
        Real conversionRatio,
        const std::vector<ext::shared_ptr<Dividend> >& dividends,
        const std::vector<ext::shared_ptr<Callability> >& callability,
        const Handle<Quote>& creditSpread,
        const Date& issueDate,
        Natural settlementDays,
        const std::vector<Rate>& coupons,
        const DayCounter& dayCounter,
        const Schedule& schedule,
        Real redemption = 100.0,
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        const BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
};

%shared_ptr(ConvertibleFloatingRateBond)
class ConvertibleFloatingRateBond : public ConvertibleBond {
  public:
    ConvertibleFloatingRateBond(
        const ext::shared_ptr<Exercise>& exercise,
        Real conversionRatio,
        const std::vector<ext::shared_ptr<Dividend> >& dividends,
        const std::vector<ext::shared_ptr<Callability> >& callability,
        const Handle<Quote>& creditSpread,
        const Date& issueDate,
        Natural settlementDays,
        const ext::shared_ptr<IborIndex>& index,
        Integer fixingDays,
        const std::vector<Spread>& spreads,
        const DayCounter& dayCounter,
        const Schedule& schedule,
        Real redemption = 100.0,
        const Period& exCouponPeriod = Period(),
        const Calendar& exCouponCalendar = Calendar(),
        const BusinessDayConvention exCouponConvention = Unadjusted,
        bool exCouponEndOfMonth = false);
};

%shared_ptr(ConvertibleZeroCouponBond)
class ConvertibleZeroCouponBond : public ConvertibleBond {
  public:
    ConvertibleZeroCouponBond(
        const ext::shared_ptr<Exercise>& exercise,
        Real conversionRatio,
        const std::vector<ext::shared_ptr<Dividend> >& dividends,
        const std::vector<ext::shared_ptr<Callability> >& callability,
        const Handle<Quote>& creditSpread,
        const Date& issueDate,
        Natural settlementDays,
        const DayCounter& dayCounter,
        const Schedule& schedule,
        Real redemption = 100.0);
};

%shared_ptr(ZeroCouponBond)
class ZeroCouponBond : public Bond {
    %feature("kwargs") ZeroCouponBond;
  public:
    ZeroCouponBond(
        Natural settlementDays,
        const Calendar &calendar,
        Real faceAmount,
        const Date & maturityDate,
        BusinessDayConvention paymentConvention = QuantLib::Following,
        Real redemption = 100.0,
        const Date& issueDate = Date());
};

#endif
