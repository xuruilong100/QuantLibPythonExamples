#include <algorithm>
#include <qlex/termstructures/yield/QuadraticSplinesFitting.hpp>

namespace QuantLib {

QuadraticSplinesFitting::QuadraticSplinesFitting(const std::vector<Time>& knotVector,
                                                 const Array& weights,
                                                 ext::shared_ptr<OptimizationMethod> optimizationMethod,
                                                 const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        false, weights, optimizationMethod, l2),
      splines_(knotVector), size_(knotVector.size()) {}

QuadraticSplinesFitting::QuadraticSplinesFitting(const std::vector<Time>& knotVector,
                                                 const Array& weights,
                                                 const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        false, weights, ext::shared_ptr<OptimizationMethod>(), l2),
      splines_(knotVector), size_(knotVector.size()) {}

Real QuadraticSplinesFitting::basisFunction(Integer i,
                                            Time t) const {
    return splines_(i, t);
}

QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod> QuadraticSplinesFitting::clone() const {
    return QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod>(
        new QuadraticSplinesFitting(*this));
}

Size QuadraticSplinesFitting::size() const {
    return size_;
}

DiscountFactor QuadraticSplinesFitting::discountFunction(const Array& x,
                                                         Time t) const {
    DiscountFactor d = 1.0;

    for (Size i = 0; i < size_; ++i) {
        d += x[i] * splines_(i + 1, t);
    }

    return d;
}

std::vector<Time> QuadraticSplinesFitting::autoKnots(const std::vector<Time>& maturities) {
    using namespace std;

    vector<Time> m(maturities);
    sort(m.begin(), m.end());

    Size n = m.size();
    Size k(ceil(sqrt(n)));

    vector<Time> knots(k);

    knots[0] = 0.0;
    knots[k - 1] = m.back();

    for (Size j = 1; j < k - 1; ++j) {
        Size l(ceil(Real(j * n) / Real(k - 1)));
        Real theta = Real(j * n) / Real(k - 1) - l;
        knots[j] = m[l - 1] + theta * (m[l] - m[l - 1]);
    }

    return knots;
}

}    // namespace QuantLib
