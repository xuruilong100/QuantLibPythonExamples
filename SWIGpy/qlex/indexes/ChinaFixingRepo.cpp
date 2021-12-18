#include <ql/currencies/asia.hpp>
#include <ql/time/calendars/china.hpp>
#include <qlex/indexes/ChinaFixingRepo.hpp>

namespace QuantLib {

ChinaFixingRepo::ChinaFixingRepo(const Period& tenor,
                                 Natural fixingDays,
                                 const Handle<YieldTermStructure>& h)
    : IborIndex("ChinaFixingRepo",
                tenor,
                fixingDays,
                CNYCurrency(),
                China(China::IB),
                Unadjusted,
                false,
                Actual365Fixed(Actual365Fixed::Standard),
                h) {}

ext::shared_ptr<IborIndex> ChinaFixingRepo::clone(const Handle<YieldTermStructure>& h) const {
    return ext::shared_ptr<IborIndex>(
        new ChinaFixingRepo(
            tenor(),
            fixingDays(),
            h));
}
}    // namespace QuantLib
