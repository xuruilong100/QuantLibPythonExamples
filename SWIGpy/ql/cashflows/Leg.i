#ifndef ql_cashflows_Leg_i
#define ql_cashflows_Leg_i

%define QL_TYPECHECK_BOOL                        7220    %enddef

%typemap(in) boost::optional<bool> {
	if($input == Py_None)
		$1 = boost::none;
	else if ($input == Py_True)
		$1 = true;
	else
		$1 = false;
}

%typecheck (QL_TYPECHECK_BOOL) boost::optional<bool> {
    if (PyBool_Check($input) || Py_None == $input)
    	$1 = 1;
    else
    	$1 = 0;
}

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CmsLeg;
using QuantLib::CmsSpreadLeg;
using QuantLib::FixedRateLeg;
using QuantLib::IborLeg;
using QuantLib::OvernightLeg;
using QuantLib::yoyInflationLeg;
using QuantLib::SubPeriodsLeg;
%}

class FixedRateLeg {
  public:
    FixedRateLeg(const Schedule& schedule);
    FixedRateLeg& withNotionals(Real);
    FixedRateLeg& withNotionals(const std::vector<Real>&);
    FixedRateLeg& withCouponRates(
        Rate,
        const DayCounter& paymentDayCounter,
        Compounding comp = Simple,
        Frequency freq = Annual);
    FixedRateLeg& withCouponRates(
        const std::vector<Rate>&,
        const DayCounter& paymentDayCounter,
        Compounding comp = Simple,
        Frequency freq = Annual);
    FixedRateLeg& withCouponRates(const InterestRate&);
    FixedRateLeg& withCouponRates(const std::vector<InterestRate>&);
    FixedRateLeg& withPaymentAdjustment(BusinessDayConvention);
    FixedRateLeg& withFirstPeriodDayCounter(const DayCounter&);
    FixedRateLeg& withLastPeriodDayCounter(const DayCounter&);
    FixedRateLeg& withPaymentCalendar(const Calendar&);
    FixedRateLeg& withPaymentLag(Natural lag);
    FixedRateLeg& withExCouponPeriod(
        const Period&,
        const Calendar&,
        BusinessDayConvention,
        bool endOfMonth = false);
    %extend {
        Leg makeLeg() const {
            return (Leg)(*self);
        }
    }
};

class IborLeg {
  public:
    IborLeg(Schedule schedule, ext::shared_ptr<IborIndex> index);
    IborLeg& withNotionals(Real notional);
    IborLeg& withNotionals(const std::vector<Real>& notionals);
    IborLeg& withPaymentDayCounter(const DayCounter&);
    IborLeg& withPaymentAdjustment(BusinessDayConvention);
    IborLeg& withPaymentLag(Natural lag);
    IborLeg& withPaymentCalendar(const Calendar&);
    IborLeg& withFixingDays(Natural fixingDays);
    IborLeg& withFixingDays(const std::vector<Natural>& fixingDays);
    IborLeg& withGearings(Real gearing);
    IborLeg& withGearings(const std::vector<Real>& gearings);
    IborLeg& withSpreads(Spread spread);
    IborLeg& withSpreads(const std::vector<Spread>& spreads);
    IborLeg& withCaps(Rate cap);
    IborLeg& withCaps(const std::vector<Rate>& caps);
    IborLeg& withFloors(Rate floor);
    IborLeg& withFloors(const std::vector<Rate>& floors);
    IborLeg& inArrears(bool flag = true);
    IborLeg& withZeroPayments(bool flag = true);
    IborLeg& withExCouponPeriod(
        const Period&,
        const Calendar&,
        BusinessDayConvention,
        bool endOfMonth = false);
    IborLeg& withIndexedCoupons(boost::optional<bool> b = true);
    IborLeg& withAtParCoupons(bool b = true);

    %extend {
        Leg makeLeg() const {
            return (Leg)(*self);
        }
    }
};

class OvernightLeg {
  public:
    OvernightLeg(
        const Schedule& schedule, 
        ext::shared_ptr<OvernightIndex> overnightIndex);
    OvernightLeg& withNotionals(Real notional);
    OvernightLeg& withNotionals(const std::vector<Real>& notionals);
    OvernightLeg& withPaymentDayCounter(const DayCounter&);
    OvernightLeg& withPaymentAdjustment(BusinessDayConvention);
    OvernightLeg& withPaymentCalendar(const Calendar&);
    OvernightLeg& withPaymentLag(Natural lag);
    OvernightLeg& withGearings(Real gearing);
    OvernightLeg& withGearings(const std::vector<Real>& gearings);
    OvernightLeg& withSpreads(Spread spread);
    OvernightLeg& withSpreads(const std::vector<Spread>& spreads);
    OvernightLeg& withTelescopicValueDates(bool telescopicValueDates);
    OvernightLeg& withAveragingMethod(RateAveraging::Type averagingMethod);
    %extend {
        Leg makeLeg() const {
            return (Leg)(*self);
        }
    }
};

class CmsLeg {
  public:
    CmsLeg(
        Schedule schedule, 
        ext::shared_ptr<SwapIndex> swapIndex);
    CmsLeg& withNotionals(Real notional);
    CmsLeg& withNotionals(const std::vector<Real>& notionals);
    CmsLeg& withPaymentDayCounter(const DayCounter&);
    CmsLeg& withPaymentAdjustment(BusinessDayConvention);
    CmsLeg& withFixingDays(Natural fixingDays);
    CmsLeg& withFixingDays(const std::vector<Natural>& fixingDays);
    CmsLeg& withGearings(Real gearing);
    CmsLeg& withGearings(const std::vector<Real>& gearings);
    CmsLeg& withSpreads(Spread spread);
    CmsLeg& withSpreads(const std::vector<Spread>& spreads);
    CmsLeg& withCaps(Rate cap);
    CmsLeg& withCaps(const std::vector<Rate>& caps);
    CmsLeg& withFloors(Rate floor);
    CmsLeg& withFloors(const std::vector<Rate>& floors);
    CmsLeg& inArrears(bool flag = true);
    CmsLeg& withZeroPayments(bool flag = true);
    CmsLeg& withExCouponPeriod(
        const Period&,
        const Calendar&,
        BusinessDayConvention,
        bool endOfMonth);

    %extend {
        Leg makeLeg() const {
            return (Leg)(*self);
        }
    }
};

class CmsSpreadLeg {
  public:
    CmsSpreadLeg(
        Schedule schedule, 
        ext::shared_ptr<SwapSpreadIndex> swapSpreadIndex);
    CmsSpreadLeg& withNotionals(Real notional);
    CmsSpreadLeg& withNotionals(const std::vector<Real>& notionals);
    CmsSpreadLeg& withPaymentDayCounter(const DayCounter&);
    CmsSpreadLeg& withPaymentAdjustment(BusinessDayConvention);
    CmsSpreadLeg& withFixingDays(Natural fixingDays);
    CmsSpreadLeg& withFixingDays(const std::vector<Natural>& fixingDays);
    CmsSpreadLeg& withGearings(Real gearing);
    CmsSpreadLeg& withGearings(const std::vector<Real>& gearings);
    CmsSpreadLeg& withSpreads(Spread spread);
    CmsSpreadLeg& withSpreads(const std::vector<Spread>& spreads);
    CmsSpreadLeg& withCaps(Rate cap);
    CmsSpreadLeg& withCaps(const std::vector<Rate>& caps);
    CmsSpreadLeg& withFloors(Rate floor);
    CmsSpreadLeg& withFloors(const std::vector<Rate>& floors);
    CmsSpreadLeg& inArrears(bool flag = true);
    CmsSpreadLeg& withZeroPayments(bool flag = true);

    %extend {
        Leg makeLeg() const {
            return (Leg)(*self);
        }
    }
};

class yoyInflationLeg {
  public:
    yoyInflationLeg(
        Schedule schedule,
        Calendar cal,
        ext::shared_ptr<YoYInflationIndex> index,
        const Period& observationLag);
    yoyInflationLeg& withNotionals(Real notional);
    yoyInflationLeg& withNotionals(const std::vector<Real>& notionals);
    yoyInflationLeg& withPaymentDayCounter(const DayCounter&);
    yoyInflationLeg& withPaymentAdjustment(BusinessDayConvention);
    yoyInflationLeg& withFixingDays(Natural fixingDays);
    yoyInflationLeg& withFixingDays(const std::vector<Natural>& fixingDays);
    yoyInflationLeg& withGearings(Real gearing);
    yoyInflationLeg& withGearings(const std::vector<Real>& gearings);
    yoyInflationLeg& withSpreads(Spread spread);
    yoyInflationLeg& withSpreads(const std::vector<Spread>& spreads);
    yoyInflationLeg& withCaps(Rate cap);
    yoyInflationLeg& withCaps(const std::vector<Rate>& caps);
    yoyInflationLeg& withFloors(Rate floor);
    yoyInflationLeg& withFloors(const std::vector<Rate>& floors);

    %extend {
        Leg makeLeg() const {
            return (Leg)(*self);
        }
    }
};

class SubPeriodsLeg {
  public:
    SubPeriodsLeg(
        const Schedule& schedule,
        ext::shared_ptr<IborIndex> index);
    SubPeriodsLeg& withNotionals(Real notional);
    SubPeriodsLeg& withNotionals(const std::vector<Real>& notionals);
    SubPeriodsLeg& withPaymentDayCounter(const DayCounter&);
    SubPeriodsLeg& withPaymentAdjustment(BusinessDayConvention);
    SubPeriodsLeg& withPaymentCalendar(const Calendar&);
    SubPeriodsLeg& withPaymentLag(Natural lag);
    SubPeriodsLeg& withFixingDays(Natural fixingDays);
    SubPeriodsLeg& withFixingDays(const std::vector<Natural>& fixingDays);
    SubPeriodsLeg& withGearings(Real gearing);
    SubPeriodsLeg& withGearings(const std::vector<Real>& gearings);
    SubPeriodsLeg& withCouponSpreads(Spread spread);
    SubPeriodsLeg& withCouponSpreads(const std::vector<Spread>& spreads);
    SubPeriodsLeg& withRateSpreads(Spread spread);
    SubPeriodsLeg& withRateSpreads(const std::vector<Spread>& spreads);
    SubPeriodsLeg& withExCouponPeriod(
        const Period&,
        const Calendar&,
        BusinessDayConvention,
        bool endOfMonth = false);
    SubPeriodsLeg& withAveragingMethod(RateAveraging::Type averagingMethod);

    %extend {
        Leg makeLeg() const {
            return (Leg)(*self);
        }
    }
};

#endif
