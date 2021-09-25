#ifndef ql_defaultprobabilityhelpers_all_i
#define ql_defaultprobabilityhelpers_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CdsHelper;
using QuantLib::SpreadCdsHelper;
using QuantLib::UpfrontCdsHelper;
%}

%shared_ptr(CdsHelper)
class CdsHelper : public BootstrapHelper<DefaultProbabilityTermStructure> {
  private:
    CdsHelper();
  public:
    ext::shared_ptr<CreditDefaultSwap> swap() const;
};

%shared_ptr(SpreadCdsHelper)
class SpreadCdsHelper : public CdsHelper {
  public:
    SpreadCdsHelper(
        const Handle<Quote>& runningSpread,
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
        Rate runningSpread,
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
class UpfrontCdsHelper : public CdsHelper {
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
