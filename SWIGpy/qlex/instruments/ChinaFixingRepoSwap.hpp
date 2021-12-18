#ifndef ChinaFixingRepoSwap_HPP
#define ChinaFixingRepoSwap_HPP

#include <ql/instruments/swap.hpp>
#include <ql/time/businessdayconvention.hpp>
#include <ql/time/calendars/china.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>

namespace QuantLib {

class ChinaFixingRepo;

class ChinaFixingRepoSwap : public Swap {
  public:
    ChinaFixingRepoSwap(Type type,
                        Real nominal,
                        const Schedule& schedule,
                        Rate fixedRate,
                        DayCounter fixedDC,
                        ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo,
                        Real gearing = 1.0,
                        Spread spread = 0.0,
                        Natural paymentLag = 0,
                        BusinessDayConvention paymentAdjustment = ModifiedFollowing,
                        const Calendar& paymentCalendar = China(China::IB));

    Type type() const { return type_; }
    Real nominal() const {
        QL_REQUIRE(nominal_ != Null<Real>(), "no notional given");
        return nominal_;
    }

    Frequency paymentFrequency() { return paymentFrequency_; }

    const Schedule& schedule() const { return schedule_; }

    Rate fixedRate() const { return fixedRate_; }
    const DayCounter& dayCount() { return fixedDC_; }
    const ext::shared_ptr<ChinaFixingRepo>& chinaFixingRepo() { return chinaFixingRepo_; }
    Real gearing() const { return gearing_; }
    Spread spread() const { return spread_; }
    BusinessDayConvention paymentConvention() const { return paymentConvention_; }

    const Leg& fixedLeg() const { return legs_[0]; }
    const Leg& floatingLeg() const { return legs_[1]; }

    Real fixedLegBPS() const;
    Real fixedLegNPV() const;
    Real fairRate() const;

    Real floatingLegBPS() const;
    Real floatingLegNPV() const;
    Spread fairSpread() const;

  private:
    void initialize(const Schedule& schedule);
    Type type_;
    Real nominal_;

    Frequency paymentFrequency_;
    Calendar paymentCalendar_;
    BusinessDayConvention paymentConvention_;
    Natural paymentLag_;

    Schedule schedule_;

    Rate fixedRate_;
    DayCounter fixedDC_;

    ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo_;
    Real gearing_;
    Spread spread_;
};

}    // namespace QuantLib

#endif    // ChinaFixingRepoSwap_HPP
