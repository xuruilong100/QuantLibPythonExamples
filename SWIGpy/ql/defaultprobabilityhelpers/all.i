#ifndef ql_defaultprobabilityhelpers_all_i
#define ql_defaultprobabilityhelpers_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::SpreadCdsHelper;
using QuantLib::UpfrontCdsHelper;
%}

%shared_ptr(SpreadCdsHelper)
class SpreadCdsHelper : public DefaultProbabilityHelper {
  public:
    SpreadCdsHelper(
        const Handle<Quote>& spread,
        const Period& tenor,
        Integer settlementDays,
        const Calendar& calendar,
        Frequency frequency,
        BusinessDayConvention convention,
        DateGeneration::Rule rule,
        const DayCounter& dayCounter,
        Real recoveryRate,
        const Handle<YieldTermStructure>& discountCurve,
        bool settlesAccrual = true,
        bool paysAtDefaultTime = true,
        const Date& startDate = Date(),
        const DayCounter& lastPeriodDayCounter = DayCounter(),
        bool rebatesAccrual = true,
        CreditDefaultSwap::PricingModel model = CreditDefaultSwap::Midpoint);
    SpreadCdsHelper(
        Rate spread,
        const Period& tenor,
        Integer settlementDays,
        const Calendar& calendar,
        Frequency frequency,
        BusinessDayConvention convention,
        DateGeneration::Rule rule,
        const DayCounter& dayCounter,
        Real recoveryRate,
        const Handle<YieldTermStructure>& discountCurve,
        bool settlesAccrual = true,
        bool paysAtDefaultTime = true,
        const Date& startDate = Date(),
        const DayCounter& lastPeriodDayCounter = DayCounter(),
        bool rebatesAccrual = true,
        CreditDefaultSwap::PricingModel model = CreditDefaultSwap::Midpoint);
};

%shared_ptr(UpfrontCdsHelper)
class UpfrontCdsHelper : public DefaultProbabilityHelper {
  public:
    UpfrontCdsHelper(
        const Handle<Quote>& upfront,
        Rate spread,
        const Period& tenor,
        Integer settlementDays,
        const Calendar& calendar,
        Frequency frequency,
        BusinessDayConvention convention,
        DateGeneration::Rule rule,
        const DayCounter& dayCounter,
        Real recoveryRate,
        const Handle<YieldTermStructure>& discountCurve,
        Natural upfrontSettlementDays=0,
        bool settlesAccrual = true,
        bool paysAtDefaultTime = true,
        const Date& startDate = Date(),
        const DayCounter& lastPeriodDayCounter = DayCounter(),
        bool rebatesAccrual = true,
        CreditDefaultSwap::PricingModel model = CreditDefaultSwap::Midpoint);
    UpfrontCdsHelper(
        Rate upfront,
        Rate spread,
        const Period& tenor,
        Integer settlementDays,
        const Calendar& calendar,
        Frequency frequency,
        BusinessDayConvention convention,
        DateGeneration::Rule rule,
        const DayCounter& dayCounter,
        Real recoveryRate,
        const Handle<YieldTermStructure>& discountCurve,
        Natural upfrontSettlementDays=0,
        bool settlesAccrual = true,
        bool paysAtDefaultTime = true,
        const Date& startDate = Date(),
        const DayCounter& lastPeriodDayCounter = DayCounter(),
        bool rebatesAccrual = true,
        CreditDefaultSwap::PricingModel model = CreditDefaultSwap::Midpoint);
};

#endif
