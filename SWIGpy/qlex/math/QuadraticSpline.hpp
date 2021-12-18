#ifndef QuadraticSpline_HPP
#define QuadraticSpline_HPP

#include <ql/types.hpp>
#include <vector>

namespace QuantLib {

//! Quadratic spline basis functions
/*! Follows treatment from:
    McCulloch JH (1971). Measuring the Term Structure of Interest Rates. The Journal of
    Business, 44(1), 19-31.
    
    For a \f$n\f$-parameter spline, client should offer \f$n\f$ knot points \f$k_l(1 \le l \le n)\f$,
    and set \f$k_1 = 0\f$, \f$k_n = M\f$, \f$M\f$ is the maximum maturity.
        
    The set of basis functions(\f$1 \le l \le n\f$) is defined by
    
    \f[
    \begin{cases}
    & \text{ if } l=1, c_l(t)=\begin{cases}
        t-\frac{1}{2k_2}t^2, &0=k_1 \le t \le k_2\\
        \frac{1}{2}k_2, &k_2 \le t \le k_n\\
    \end{cases}\\
    & \text{ if } l=n, c_l(t)=\begin{cases}
        0, &0 \le t \le k_{l-1}\\
        \frac{(t-k_{l-1})^2}{2(k_n - k_{l-1})}, &k_{l-1} \le t \le k_n\\
    \end{cases}\\
    & \text{ else}, c_{l}=\begin{cases}
        0 & {t<k_{l-1}} \\
        {\frac{\left(t-k_{l-1}\right)^2}{2\left(k_{l}-k_{l-1}\right)}} & {k_{l-1} \le t<k_{l}} \\
        {\frac{\left(k_{l}-k_{l-1}\right)}{2}+(t-k_l)^2 -\frac{\left(t-k_{l}\right)^2}{2\left(k_{l+1}-k_{l}\right)}} & {k_{l} \le t<k_{l+1}} \\
        \frac{k_{l+1}-k_{l-1}}{2} & k_{l+1} \le t
    \end{cases}
    \end{cases}
    \f]
*/

class QuadraticSpline {
  public:
    QuadraticSpline(const std::vector<Real>& knots);
    ~QuadraticSpline();
    Real operator()(Natural i, Real x) const;

  private:
    Size n_;
    std::vector<Real> knots_ex_;
};

}    // namespace QuantLib

#endif    // QuadraticSpline_HPP
