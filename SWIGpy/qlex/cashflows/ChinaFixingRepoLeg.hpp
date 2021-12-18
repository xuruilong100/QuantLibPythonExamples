#ifndef ChinaFixingRepoLeg_HPP
#define ChinaFixingRepoLeg_HPP

#include <ql/cashflow.hpp>
#include <ql/time/businessdayconvention.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>

namespace QuantLib {

class ChinaFixingRepo;

class ChinaFixingRepoLeg {
  public:
    ChinaFixingRepoLeg(const Schedule& schedule,
                       ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo);

    ChinaFixingRepoLeg& withNotional(Real notional);
    ChinaFixingRepoLeg& withPaymentDayCounter(const DayCounter&);
    ChinaFixingRepoLeg& withPaymentAdjustment(BusinessDayConvention);
    ChinaFixingRepoLeg& withPaymentCalendar(const Calendar&);
    ChinaFixingRepoLeg& withPaymentLag(Natural lag);
    ChinaFixingRepoLeg& withGearing(Real gearing);
    ChinaFixingRepoLeg& withSpread(Spread spread);
    operator Leg() const;

  private:
    Schedule schedule_;
    ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo_;
    Real notional_;
    DayCounter paymentDayCounter_;
    Calendar paymentCalendar_;
    BusinessDayConvention paymentConvention_;
    Natural paymentLag_;
    Real gearing_;
    Spread spread_;
};

}    // namespace QuantLib

#endif    // ChinaFixingRepoLeg_HPP
