#include <algorithm>
#include <qlex/termstructures/yield/CubicSplinesFitting.hpp>

namespace QuantLib {

CubicSplinesFitting::CubicSplinesFitting(const std::vector<Time>& knotVector,
                                         const Array& weights,
                                         ext::shared_ptr<OptimizationMethod> optimizationMethod,
                                         const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        false, weights, optimizationMethod, l2),
      splines_(knotVector) {

    Size basisFunctions = knotVector.size() + 1;

    size_ = basisFunctions;
}

CubicSplinesFitting::CubicSplinesFitting(const std::vector<Time>& knotVector,
                                         const Array& weights,
                                         const Array& l2)
    : FittedBondDiscountCurve::FittingMethod(
        false, weights, ext::shared_ptr<OptimizationMethod>(), l2),
      splines_(knotVector) {

    Size basisFunctions = knotVector.size() + 1;

    size_ = basisFunctions;
}

Real CubicSplinesFitting::basisFunction(Integer i,
                                        Time t) const {
    return splines_(i, t);
}

QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod> CubicSplinesFitting::clone() const {
    return QL_UNIQUE_OR_AUTO_PTR<FittedBondDiscountCurve::FittingMethod>(
        new CubicSplinesFitting(*this));
}

Size CubicSplinesFitting::size() const {
    return size_;
}

DiscountFactor CubicSplinesFitting::discountFunction(const Array& x,
                                                     Time t) const {
    DiscountFactor d = 1.0;

    for (Size i = 0; i < size_; ++i) {
        d += x[i] * splines_(i + 1, t);
    }

    return d;
}

std::vector<Time> CubicSplinesFitting::autoKnots(const std::vector<Time>& maturities) {
    using namespace std;

    vector<Time> m(maturities);
    sort(m.begin(), m.end());

    Size k = m.size();
    Size n(floor(sqrt(k) + 0.5));

    vector<Time> knots(n - 1);

    knots[0] = 0.0;
    knots[n - 1] = m.back();

    for (Size l = 1; l < n - 1; ++l) {
        Size h(ceil(Real(l * k) / Real(n - 2)));
        Real theta = Real(l * k) / Real(n - 2) - h;
        knots[l] = m[h - 1] + theta * (m[h] - m[h - 1]);
    }

    return knots;
}

}    // namespace QuantLib
