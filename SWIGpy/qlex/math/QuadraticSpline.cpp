#include <cmath>
#include <qlex/math/QuadraticSpline.hpp>

namespace QuantLib {

QuadraticSpline::QuadraticSpline(const std::vector<Real>& knots)
    : n_(knots.size()), knots_ex_(knots) {
    knots_ex_.insert(knots_ex_.begin(), 0.0);
}

QuadraticSpline::~QuadraticSpline() {}

Real QuadraticSpline::operator()(Natural i, Real x) const {
    using namespace std;

    if (i == 1) {
        if (x <= knots_ex_[2]) {
            return x - 1.0 / (2 * knots_ex_[2]) * pow(x, 2);
        } else {
            return 1.0 / 2 * knots_ex_[2];
        }
    } else if (i == n_) {
        if (x <= knots_ex_[i - 1]) {
            return 0.0;
        } else {
            return pow(x - knots_ex_[i - 1], 2) / (2.0 * (knots_ex_[n_] - knots_ex_[i - 1]));
        }
    } else {
        Real q = knots_ex_[i], q_minus = knots_ex_[i - 1], q_plus = knots_ex_[i + 1];

        if (x < q_minus) {
            return 0.0;
        } else if (q_minus <= x and x < q) {
            return pow(x - q_minus, 2) / (2.0 * (q - q_minus));
        } else if (q <= x and x < q_plus) {
            return (q - q_minus) / 2.0
                   + (x - q)
                   - pow(x - q, 2) / (2.0 * (q_plus - q));
        } else {
            return (q_plus - q_minus) / 2.0;
        }
    }
}

}    // namespace QuantLib
