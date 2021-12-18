#include <qlex/termstructures/yield/DieboldLiFitting.hpp>

namespace QuantLib {

DieboldLiFitting::DieboldLiFitting(Real kappa,
                                   const Array& weights,
                                   ext::shared_ptr<OptimizationMethod> optimizationMethod,
                                   const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        true, weights, optimizationMethod, l2),
      kappa_(kappa) {}

DieboldLiFitting::DieboldLiFitting(Real kappa,
                                   const Array& weights,
                                   const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        true, weights, ext::shared_ptr<OptimizationMethod>(), l2),
      kappa_(kappa) {}

QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod> DieboldLiFitting::clone() const {
    return QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod>(
        new DieboldLiFitting(*this));
}

Size DieboldLiFitting::size() const {
    return 3;
}

DiscountFactor DieboldLiFitting::discountFunction(const Array& x,
                                                  Time t) const {
    Real zeroRate =
        x[0]
        + (x[1] + x[2]) * (1.0 - std::exp(-kappa_ * t)) / ((kappa_ + QL_EPSILON) * (t + QL_EPSILON))
        - (x[2]) * std::exp(-kappa_ * t);
    DiscountFactor d = std::exp(-zeroRate * t);
    return d;
}

}    // namespace QuantLib
