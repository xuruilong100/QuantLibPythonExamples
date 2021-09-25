#ifndef ql_cashflows_Leg_i
#define ql_cashflows_Leg_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
Leg _FixedRateLeg(
    const Schedule& schedule,
    const DayCounter& dayCount,
    const std::vector<Real>& nominals,
    const std::vector<Rate>& couponRates,
    BusinessDayConvention paymentAdjustment = Following,
    const DayCounter& firstPeriodDayCount = DayCounter(),
    const Period& exCouponPeriod = Period(),
    const Calendar& exCouponCalendar = Calendar(),
    BusinessDayConvention exCouponConvention = Unadjusted,
    bool exCouponEndOfMonth = false,
    const Calendar& paymentCalendar = Calendar(),
    const Natural paymentLag = 0) {
    return QuantLib::FixedRateLeg(schedule)
        .withNotionals(nominals)
        .withCouponRates(couponRates, dayCount)
        .withPaymentAdjustment(paymentAdjustment)
        .withPaymentCalendar(paymentCalendar.empty() ? schedule.calendar() : paymentCalendar)
        .withPaymentLag(paymentLag)
        .withFirstPeriodDayCounter(firstPeriodDayCount)
        .withExCouponPeriod(exCouponPeriod,
                            exCouponCalendar,
                            exCouponConvention,
                            exCouponEndOfMonth);
}
%}

%feature("kwargs") _FixedRateLeg;
%rename(FixedRateLeg) _FixedRateLeg;
Leg _FixedRateLeg(
    const Schedule& schedule,
    const DayCounter& dayCount,
    const std::vector<Real>& nominals,
    const std::vector<Rate>& couponRates,
    BusinessDayConvention paymentAdjustment = Following,
    const DayCounter& firstPeriodDayCount = DayCounter(),
    const Period& exCouponPeriod = Period(),
    const Calendar& exCouponCalendar = Calendar(),
    BusinessDayConvention exCouponConvention = Unadjusted,
    bool exCouponEndOfMonth = false,
    const Calendar& paymentCalendar = Calendar(),
    const Natural paymentLag = 0);

%{
Leg _IborLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<IborIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Natural>& fixingDays = std::vector<Natural>(),
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>(),
    bool isInArrears = false,
    const Period& exCouponPeriod = Period(),
    const Calendar& exCouponCalendar = Calendar(),
    BusinessDayConvention exCouponConvention = Unadjusted,
    bool exCouponEndOfMonth = false,
    const Calendar& paymentCalendar = Calendar(),
    const Natural paymentLag = 0) {
    return QuantLib::IborLeg(schedule, index)
        .withNotionals(nominals)
        .withPaymentDayCounter(paymentDayCounter)
        .withPaymentAdjustment(paymentConvention)
        .withPaymentCalendar(paymentCalendar.empty() ? schedule.calendar() : paymentCalendar)
        .withPaymentLag(paymentLag)
        .withFixingDays(fixingDays)
        .withGearings(gearings)
        .withSpreads(spreads)
        .withCaps(caps)
        .withFloors(floors)
        .inArrears(isInArrears)
        .withExCouponPeriod(
            exCouponPeriod,
            exCouponCalendar,
            exCouponConvention,
            exCouponEndOfMonth);
}
%}

%feature("kwargs") _IborLeg;
%rename(IborLeg) _IborLeg;
Leg _IborLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<IborIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Natural>& fixingDays = std::vector<Natural>(),
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>(),
    bool isInArrears = false,
    const Period& exCouponPeriod = Period(),
    const Calendar& exCouponCalendar = Calendar(),
    BusinessDayConvention exCouponConvention = Unadjusted,
    bool exCouponEndOfMonth = false,
    const Calendar& paymentCalendar = Calendar(),
    const Natural paymentLag = 0);

%{
Leg _OvernightLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<OvernightIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    bool telescopicValueDates = false,
    RateAveraging::Type averagingMethod = RateAveraging::Compound,
    const Calendar& paymentCalendar = Calendar(),
    const Natural paymentLag = 0) {
    return QuantLib::OvernightLeg(schedule, index)
        .withNotionals(nominals)
        .withPaymentDayCounter(paymentDayCounter)
        .withPaymentAdjustment(paymentConvention)
        .withPaymentCalendar(paymentCalendar.empty() ? schedule.calendar() : paymentCalendar)
        .withPaymentLag(paymentLag)
        .withGearings(gearings)
        .withSpreads(spreads)
        .withTelescopicValueDates(telescopicValueDates)
        .withAveragingMethod(averagingMethod);
}
%}

%feature("kwargs") _OvernightLeg;
%rename(OvernightLeg) _OvernightLeg;
Leg _OvernightLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<OvernightIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    bool telescopicValueDates = false,
    RateAveraging::Type averagingMethod = RateAveraging::Compound,
    const Calendar& paymentCalendar = Calendar(),
    const Natural paymentLag = 0);

%{
Leg _CmsLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<SwapIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Natural>& fixingDays = std::vector<Natural>(),
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>(),
    bool isInArrears = false,
    const Period& exCouponPeriod = Period(),
    const Calendar& exCouponCalendar = Calendar(),
    const BusinessDayConvention exCouponConvention = Unadjusted,
    bool exCouponEndOfMonth = false) {
    return QuantLib::CmsLeg(schedule, index)
        .withNotionals(nominals)
        .withPaymentDayCounter(paymentDayCounter)
        .withPaymentAdjustment(paymentConvention)
        .withFixingDays(fixingDays)
        .withGearings(gearings)
        .withSpreads(spreads)
        .withCaps(caps)
        .withFloors(floors)
        .withExCouponPeriod(
            exCouponPeriod, exCouponCalendar,
            exCouponConvention, exCouponEndOfMonth)
        .inArrears(isInArrears);
}
%}

%feature("kwargs") _CmsLeg;
%rename(CmsLeg) _CmsLeg;
Leg _CmsLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<SwapIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Natural>& fixingDays = std::vector<Natural>(),
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>(),
    bool isInArrears = false,
    const Period& exCouponPeriod = Period(),
    const Calendar& exCouponCalendar = Calendar(),
    const BusinessDayConvention exCouponConvention = Unadjusted,
    bool exCouponEndOfMonth = false);

%{
Leg _CmsZeroLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<SwapIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Natural>& fixingDays = std::vector<Natural>(),
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>(),
    const Period& exCouponPeriod = Period(),
    const Calendar& exCouponCalendar = Calendar(),
    const BusinessDayConvention exCouponConvention = Unadjusted,
    bool exCouponEndOfMonth = false) {
    return QuantLib::CmsLeg(schedule, index)
        .withNotionals(nominals)
        .withPaymentDayCounter(paymentDayCounter)
        .withPaymentAdjustment(paymentConvention)
        .withFixingDays(fixingDays)
        .withGearings(gearings)
        .withSpreads(spreads)
        .withCaps(caps)
        .withFloors(floors)
        .withExCouponPeriod(
            exCouponPeriod, exCouponCalendar,
            exCouponConvention, exCouponEndOfMonth)
        .withZeroPayments();
}
%}

%feature("kwargs") _CmsZeroLeg;
%rename(CmsZeroLeg) _CmsZeroLeg;
Leg _CmsZeroLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<SwapIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Natural>& fixingDays = std::vector<Natural>(),
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>(),
    const Period& exCouponPeriod = Period(),
    const Calendar& exCouponCalendar = Calendar(),
    const BusinessDayConvention exCouponConvention = Unadjusted,
    bool exCouponEndOfMonth = false);

%{
Leg _CmsSpreadLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<SwapSpreadIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Natural>& fixingDays = std::vector<Natural>(),
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>(),
    bool isInArrears = false) {
    return QuantLib::CmsSpreadLeg(schedule, index)
        .withNotionals(nominals)
        .withPaymentDayCounter(paymentDayCounter)
        .withPaymentAdjustment(paymentConvention)
        .withFixingDays(fixingDays)
        .withGearings(gearings)
        .withSpreads(spreads)
        .withCaps(caps)
        .withFloors(floors)
        .inArrears(isInArrears);
}
%}

%feature("kwargs") _CmsSpreadLeg;
%rename(CmsSpreadLeg) _CmsSpreadLeg;
Leg _CmsSpreadLeg(
    const std::vector<Real>& nominals,
    const Schedule& schedule,
    const ext::shared_ptr<SwapSpreadIndex>& index,
    const DayCounter& paymentDayCounter = DayCounter(),
    const BusinessDayConvention paymentConvention = Following,
    const std::vector<Natural>& fixingDays = std::vector<Natural>(),
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>(),
    bool isInArrears = false);

%{
Leg _yoyInflationLeg(
    const Schedule& schedule,
    const Calendar& calendar,
    const ext::shared_ptr<YoYInflationIndex>& index,
    const Period& observationLag,
    const std::vector<Real>& notionals,
    const DayCounter& paymentDayCounter,
    BusinessDayConvention paymentAdjustment = Following,
    Natural fixingDays = 0,
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>()) {
    return QuantLib::yoyInflationLeg(
        schedule, calendar,
        index, observationLag)
        .withNotionals(notionals)
        .withPaymentDayCounter(paymentDayCounter)
        .withPaymentAdjustment(paymentAdjustment)
        .withFixingDays(fixingDays)
        .withGearings(gearings)
        .withSpreads(spreads)
        .withCaps(caps)
        .withFloors(floors);
}
%}

%feature("kwargs") _yoyInflationLeg;
%rename(yoyInflationLeg) _yoyInflationLeg;
Leg _yoyInflationLeg(
    const Schedule& schedule,
    const Calendar& calendar,
    const ext::shared_ptr<YoYInflationIndex>& index,
    const Period& observationLag,
    const std::vector<Real>& notionals,
    const DayCounter& paymentDayCounter,
    BusinessDayConvention paymentAdjustment = Following,
    Natural fixingDays = 0,
    const std::vector<Real>& gearings = std::vector<Real>(),
    const std::vector<Spread>& spreads = std::vector<Spread>(),
    const std::vector<Rate>& caps = std::vector<Rate>(),
    const std::vector<Rate>& floors = std::vector<Rate>());

%{
Leg _SubPeriodsLeg(const std::vector<Real>& nominals,
                   const Schedule& schedule,
                   const ext::shared_ptr<IborIndex>& index,
                   const DayCounter& paymentDayCounter = DayCounter(),
                   const BusinessDayConvention paymentConvention = Following,
                   const Calendar& paymentCalendar = Calendar(),
                   Natural paymentLag = 0,
                   const std::vector<Natural>& fixingDays = std::vector<Natural>(),
                   const std::vector<Real>& gearings = std::vector<Real>(),
                   const std::vector<Spread>& couponSpreads = std::vector<Spread>(),
                   const std::vector<Spread>& rateSpreads = std::vector<Spread>(),
                   const Period& exCouponPeriod = Period(),
                   const Calendar& exCouponCalendar = Calendar(),
                   BusinessDayConvention exCouponConvention = Unadjusted,
                   bool exCouponEndOfMonth = false,
                   RateAveraging::Type averagingMethod = RateAveraging::Compound) {
    return QuantLib::SubPeriodsLeg(schedule, index)
        .withNotionals(nominals)
        .withPaymentDayCounter(paymentDayCounter)
        .withPaymentAdjustment(paymentConvention)
        .withPaymentCalendar(paymentCalendar.empty() ? schedule.calendar() : paymentCalendar)
        .withPaymentLag(paymentLag)
        .withFixingDays(fixingDays)
        .withGearings(gearings)
        .withCouponSpreads(couponSpreads)
        .withRateSpreads(rateSpreads)
        .withExCouponPeriod(exCouponPeriod,
                            exCouponCalendar,
                            exCouponConvention,
                            exCouponEndOfMonth)
        .withAveragingMethod(averagingMethod);
}
%}

%feature("kwargs") _SubPeriodsLeg;
%rename(SubPeriodsLeg) _SubPeriodsLeg;
Leg _SubPeriodsLeg(const std::vector<Real>& nominals,
                   const Schedule& schedule,
                   const ext::shared_ptr<IborIndex>& index,
                   const DayCounter& paymentDayCounter = DayCounter(),
                   const BusinessDayConvention paymentConvention = Following,
                   const Calendar& paymentCalendar = Calendar(),
                   Natural paymentLag = 0,
                   const std::vector<Natural>& fixingDays = std::vector<Natural>(),
                   const std::vector<Real>& gearings = std::vector<Real>(),
                   const std::vector<Spread>& couponSpreads = std::vector<Spread>(),
                   const std::vector<Spread>& rateSpreads = std::vector<Spread>(),
                   const Period& exCouponPeriod = Period(),
                   const Calendar& exCouponCalendar = Calendar(),
                   BusinessDayConvention exCouponConvention = Unadjusted,
                   bool exCouponEndOfMonth = false,
                   RateAveraging::Type averagingMethod = RateAveraging::Compound);

#endif
