#include <ql/pricingengines/swap/discountingswapengine.hpp>
#include <ql/utilities/null_deleter.hpp>
#include <qlex/indexes/ChinaFixingRepo.hpp>
#include <qlex/instruments/MakeChinaFixingRepoSwap.hpp>
#include <qlex/termstructures/yield/ChinaFixingRepoSwapRateHelper.hpp>
#include <utility>

namespace QuantLib {
ChinaFixingRepoSwapRateHelper::ChinaFixingRepoSwapRateHelper(Natural settlementDays,
                                                             const Period& tenor,    // swap maturity
                                                             const Handle<Quote>& fixedRate,
                                                             ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo,
                                                             Handle<YieldTermStructure> discount,
                                                             Natural paymentLag,
                                                             BusinessDayConvention paymentConvention,
                                                             Frequency paymentFrequency,
                                                             Calendar paymentCalendar,
                                                             const Period& forwardStart,
                                                             Real gearing,
                                                             Spread spread,
                                                             Pillar::Choice pillar,
                                                             Date customPillarDate)
    : RelativeDateRateHelper(fixedRate),
      pillarChoice_(pillar),
      settlementDays_(settlementDays),
      tenor_(tenor),
      chinaFixingRepo_(std::move(chinaFixingRepo)),
      discountHandle_(std::move(discount)),
      paymentLag_(paymentLag),
      paymentConvention_(paymentConvention),
      paymentFrequency_(paymentFrequency),
      paymentCalendar_(std::move(paymentCalendar)),
      forwardStart_(forwardStart),
      gearing_(gearing),
      spread_(spread) {
    registerWith(chinaFixingRepo_);
    registerWith(discountHandle_);

    pillarDate_ = customPillarDate;
    initializeDates();
}

void ChinaFixingRepoSwapRateHelper::initializeDates() {

    // dummy ChinaFixingRepo with curve/swap arguments
    // review here
    ext::shared_ptr<IborIndex> clonedIborIndex =
        chinaFixingRepo_->clone(termStructureHandle_);
    ext::shared_ptr<ChinaFixingRepo> clonedChinaFixingRepo =
        ext::dynamic_pointer_cast<ChinaFixingRepo>(clonedIborIndex);

    // input discount curve Handle might be empty now but it could
    // be assigned a curve later; use a RelinkableHandle here
    swap_ = MakeChinaFixingRepoSwap(
                tenor_, clonedChinaFixingRepo, 0.0, forwardStart_)
                .withDiscountingTermStructure(discountRelinkableHandle_)
                .withSettlementDays(settlementDays_)
                .withPaymentLag(paymentLag_)
                .withPaymentAdjustment(paymentConvention_)
                .withPaymentFrequency(paymentFrequency_)
                .withPaymentCalendar(paymentCalendar_)
                .withFloatingLegGearing(gearing_)
                .withFloatingLegSpread(spread_);

    earliestDate_ = swap_->startDate();
    maturityDate_ = swap_->maturityDate();

    Date lastPaymentDate = std::max(
        swap_->floatingLeg().back()->date(),
        swap_->fixedLeg().back()->date());
    latestRelevantDate_ = std::max(maturityDate_, lastPaymentDate);

    switch (pillarChoice_) {
    case Pillar::MaturityDate:
        pillarDate_ = maturityDate_;
        break;
    case Pillar::LastRelevantDate:
        pillarDate_ = latestRelevantDate_;
        break;
    case Pillar::CustomDate:
        // pillarDate_ already assigned at construction time
        QL_REQUIRE(pillarDate_ >= earliestDate_,
                   "pillar date ("
                       << pillarDate_ << ") must be later than or equal to the instrument's earliest date ("
                       << earliestDate_ << ")");
        QL_REQUIRE(pillarDate_ <= latestRelevantDate_,
                   "pillar date ("
                       << pillarDate_ << ") must be before or equal to the instrument's latest relevant date ("
                       << latestRelevantDate_ << ")");
        break;
    default:
        QL_FAIL("unknown Pillar::Choice(" << Integer(pillarChoice_) << ")");
    }

    latestDate_ = std::max(swap_->maturityDate(), lastPaymentDate);
}

void ChinaFixingRepoSwapRateHelper::setTermStructure(YieldTermStructure* t) {
    // do not set the relinkable handle as an observer -
    // force recalculation when needed
    bool observer = false;

    ext::shared_ptr<YieldTermStructure> temp(t, null_deleter());
    termStructureHandle_.linkTo(temp, observer);

    if (discountHandle_.empty())
        discountRelinkableHandle_.linkTo(temp, observer);
    else
        discountRelinkableHandle_.linkTo(*discountHandle_, observer);

    RelativeDateRateHelper::setTermStructure(t);
}

Real ChinaFixingRepoSwapRateHelper::impliedQuote() const {
    QL_REQUIRE(termStructure_ != nullptr, "term structure not set");
    // we didn't register as observers - force calculation
    swap_->recalculate();
    return swap_->fairRate();
}

void ChinaFixingRepoSwapRateHelper::accept(AcyclicVisitor& v) {
    auto* v1 = dynamic_cast<Visitor<ChinaFixingRepoSwapRateHelper>*>(&v);
    if (v1 != nullptr)
        v1->visit(*this);
    else
        RateHelper::accept(v);
}

}    // namespace QuantLib
