#include <cmath>
#include <qlex/math/CubicSpline.hpp>

namespace QuantLib {

CubicSpline::CubicSpline(const std::vector<Real>& knots)
    : n_(knots.size() + 1), knots_ex_(knots) {
    knots_ex_.insert(knots_ex_.begin(), 0.0);
    knots_ex_.insert(knots_ex_.end(), knots.back());
}

CubicSpline::~CubicSpline() {
}

Real CubicSpline::operator()(Natural i, Real x) const {
    using namespace std;

    if (i < n_) {
        Real q = knots_ex_[i], q_minus = knots_ex_[i - 1], q_plus = knots_ex_[i + 1];

        if (x < q_minus) {
            return 0.0;
        } else if (q_minus <= x and x < q) {
            return pow(x - q_minus, 3) / (6.0 * (q - q_minus));
        } else if (q <= x and x < q_plus) {
            return pow(q - q_minus, 2) / 6.0
                   + (q - q_minus) * (x - q) / 2.0
                   + pow(x - q, 2) / 2.0
                   - pow(x - q, 3) / (6.0 * (q_plus - q));
        } else {
            return (q_plus - q_minus)
                   * ((2.0 * q_plus - q - q_minus) / 6.0
                      + (x - q_plus) / 2.0);
        }
    } else {
        return x;
    }
}

}    // namespace QuantLib
