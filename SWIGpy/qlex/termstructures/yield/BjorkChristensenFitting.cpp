#include <qlex/termstructures/yield/BjorkChristensenFitting.hpp>

namespace QuantLib {

BjorkChristensenFitting::BjorkChristensenFitting(const Array& weights,
                                                 ext::shared_ptr<OptimizationMethod> optimizationMethod,
                                                 const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        true, weights, optimizationMethod, l2) {}

BjorkChristensenFitting::BjorkChristensenFitting(const Array& weights,
                                                 const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        true, weights, ext::shared_ptr<OptimizationMethod>(), l2) {}

QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod> BjorkChristensenFitting::clone() const {
    return QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod>(
        new BjorkChristensenFitting(*this));
}

Size BjorkChristensenFitting::size() const {
    return 5;
}

DiscountFactor BjorkChristensenFitting::discountFunction(const Array& x,
                                                         Time t) const {
    Real kappa = x[size() - 1];

    Real zeroRate =
        x[0]
        + (x[1] + x[2]) * (1.0 - std::exp(-kappa * t)) / ((kappa + QL_EPSILON) * (t + QL_EPSILON))
        - x[2] * std::exp(-kappa * t)
        + x[3] * (1.0 - std::exp(-kappa * t * 2.0)) / ((kappa + QL_EPSILON) * (t + QL_EPSILON) * 2.0);

    DiscountFactor d = std::exp(-zeroRate * t);
    return d;
}

}    // namespace QuantLib
