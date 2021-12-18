#include <qlex/termstructures/yield/AdjustedSvenssonFitting.hpp>

namespace QuantLib {

AdjustedSvenssonFitting::AdjustedSvenssonFitting(const Array& weights,
                                                 ext::shared_ptr<OptimizationMethod> optimizationMethod,
                                                 const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        true, weights, optimizationMethod, l2) {}

AdjustedSvenssonFitting::AdjustedSvenssonFitting(const Array& weights,
                                                 const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        true, weights, ext::shared_ptr<OptimizationMethod>(), l2) {}

QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod> AdjustedSvenssonFitting::clone() const {
    return QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod>(
        new AdjustedSvenssonFitting(*this));
}

Size AdjustedSvenssonFitting::size() const {
    return 6;
}

DiscountFactor AdjustedSvenssonFitting::discountFunction(const Array& x,
                                                         Time t) const {
    Real kappa = x[size() - 2];
    Real kappa_1 = x[size() - 1];

    Real zeroRate =
        x[0]
        + (x[1] + x[2]) * (1.0 - std::exp(-kappa * t)) / ((kappa + QL_EPSILON) * (t + QL_EPSILON))
        - (x[2]) * std::exp(-kappa * t)
        + x[3] * (((1.0 - std::exp(-kappa_1 * t)) / ((kappa_1 + QL_EPSILON) * (t + QL_EPSILON))) - std::exp(-kappa_1 * t * 2.0));
    DiscountFactor d = std::exp(-zeroRate * t);
    return d;
}

}    // namespace QuantLib
