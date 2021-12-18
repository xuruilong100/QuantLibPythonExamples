#include <qlex/termstructures/yield/BlissFitting.hpp>

namespace QuantLib {

BlissFitting::BlissFitting(const Array& weights,
                           ext::shared_ptr<OptimizationMethod> optimizationMethod,
                           const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        true, weights, optimizationMethod, l2) {}

BlissFitting::BlissFitting(const Array& weights,
                           const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        true, weights, ext::shared_ptr<OptimizationMethod>(), l2) {}

QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod> BlissFitting::clone() const {
    return QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod>(
        new BlissFitting(*this));
}

Size BlissFitting::size() const {
    return 5;
}

DiscountFactor BlissFitting::discountFunction(const Array& x,
                                              Time t) const {
    Real kappa = x[size() - 2];
    Real kappa_1 = x[size() - 1];

    Real zeroRate =
        x[0]
        + x[1] * (1.0 - std::exp(-kappa * t)) / ((kappa + QL_EPSILON) * (t + QL_EPSILON))
        + x[2] * (1.0 - std::exp(-kappa_1 * t)) / ((kappa_1 + QL_EPSILON) * (t + QL_EPSILON))
        - x[2] * std::exp(-kappa_1 * t);

    DiscountFactor d = std::exp(-zeroRate * t);
    return d;
}

}    // namespace QuantLib
