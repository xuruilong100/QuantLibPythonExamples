#ifndef ChinaFixingRepoSwapRateHelper_HPP
#define ChinaFixingRepoSwapRateHelper_HPP

#include <ql/termstructures/yield/ratehelpers.hpp>
#include <ql/time/calendars/china.hpp>
#include <qlex/instruments/ChinaFixingRepoSwap.hpp>

namespace QuantLib {

class ChinaFixingRepoSwapRateHelper : public RelativeDateRateHelper {
  public:
    ChinaFixingRepoSwapRateHelper(Natural settlementDays,
                                  const Period& tenor,    // swap maturity
                                  const Handle<Quote>& fixedRate,
                                  ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo,
                                  // exogenous discounting curve
                                  Handle<YieldTermStructure> discountingCurve = Handle<YieldTermStructure>(),
                                  Natural paymentLag = 0,
                                  BusinessDayConvention paymentConvention = Following,
                                  Frequency paymentFrequency = Annual,
                                  Calendar paymentCalendar = China(China::IB),
                                  const Period& forwardStart = 0 * Days,
                                  Real gearing = 1.0,
                                  Spread spread = 0.0,
                                  Pillar::Choice pillar = Pillar::LastRelevantDate,
                                  Date customPillarDate = Date());

    Real impliedQuote() const override;
    void setTermStructure(YieldTermStructure*) override;
    ext::shared_ptr<ChinaFixingRepoSwap> swap() const { return swap_; }

    void accept(AcyclicVisitor&) override;

  protected:
    void initializeDates() override;
    Pillar::Choice pillarChoice_;

    Natural settlementDays_;
    Period tenor_;
    ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo_;

    ext::shared_ptr<ChinaFixingRepoSwap> swap_;
    RelinkableHandle<YieldTermStructure> termStructureHandle_;

    Handle<YieldTermStructure> discountHandle_;
    RelinkableHandle<YieldTermStructure> discountRelinkableHandle_;

    Natural paymentLag_;
    BusinessDayConvention paymentConvention_;
    Frequency paymentFrequency_;
    Calendar paymentCalendar_;
    Period forwardStart_;
    Real gearing_;
    Spread spread_;
};

}    // namespace QuantLib

#endif    // ChinaFixingRepoSwapRateHelper_HPP
