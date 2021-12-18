#ifndef CubicSpline_HPP
#define CubicSpline_HPP

#include <ql/types.hpp>
#include <vector>

namespace QuantLib {

//! Cubic spline basis functions
/*! Follows treatment from:
    Ferstl R, Hayden J (2010). Zero-Coupon Yield Curve Estimation with
    the Package termstrc. Journal of Statistical Software, Volume 36, Issue 1.
    
    For a \f$n\f$-parameter spline, client should offer \f$n-1\f$ knot points \f$k_l(1 \le l < n)\f$,
    and set \f$k_0 = k_1 = 0\f$, \f$k_{n-1} = k_n = M\f$, \f$M\f$ is the maximum maturity.
        
    The set of basis functions(\f$1 \le l \le n\f$) is defined by
    
    \f[
    \begin{cases}
     & \text{ if } l=n, c_l(t)=t\\
     & \text{ else }, c_{l}\left(t\right)=
    \left\{\begin{array}{ll}
    0 & {t<k_{l-1}} \\
    {\frac{\left(t-k_{l-1}\right)^{3}}{6\left(k_{l}-k_{l-1}\right)}} & {k_{l-1} \leq t<k_{l}} \\
    {\frac{\left(k_{l}-k_{l-1}\right)^{2}}{6}+\frac{\left(k_{l}-k_{l-1}\right)\left(t-k_{l}\right)}{2}+\frac{(t-k_l)^2}{2} -\frac{\left(t-k_{l}\right)^{3}}{6\left(k_{l+1}-k_{l}\right)}} & {k_{l} \leq t<k_{l+1}} \\
    {\left(k_{l+1}-k_{l-1}\right)\left[\frac{2 k_{l+1}-k_{l}-k_{l-1}}{6}+\frac{t-k_{l+1}}{2}\right]} & {k_{l+1} \leq t}
    \end{array}\right.
    \end{cases}
    \f]
*/
class CubicSpline {
  public:
    CubicSpline(const std::vector<Real>& knots);
    ~CubicSpline();
    Real operator()(Natural i, Real x) const;

  private:
    Size n_;
    std::vector<Real> knots_ex_;
};

}    // namespace QuantLib

#endif    // CubicSpline_HPP
