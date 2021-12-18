#ifndef AdjustedSvenssonFitting_HPP
#define AdjustedSvenssonFitting_HPP

#include <ql/auto_ptr.hpp>
#include <ql/termstructures/yield/fittedbonddiscountcurve.hpp>

namespace QuantLib {

//! Adjusted Svensson Fitting method
/*! Fits a discount function to the form
    \f$ d(t) = \exp^{-r t}, \f$ where the zero rate \f$r\f$ is defined as
    
    \f[
    r \equiv c_0 + (c_1 + c_2)(\frac {1 - exp^{-\kappa t}}{\kappa t})
    - c_2exp^{ - \kappa t}
    + c_3{(\frac{1 - exp^{-\kappa_1 t}}{\kappa_1 t} -exp^{-2\kappa_1 t})}.
    \f]
    
    See: Ferstl R, Hayden J (2010). Zero-Coupon Yield Curve Estimation with
    the Package termstrc. Journal of Statistical Software, Volume 36, Issue 1.
*/
class AdjustedSvenssonFitting : public FittedBondDiscountCurve::FittingMethod {
  public:
    AdjustedSvenssonFitting(const Array& weights = Array(),
                            ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
                            const Array& l2 = Array());
    AdjustedSvenssonFitting(const Array& weights, const Array& l2);
#if defined(QL_USE_STD_UNIQUE_PTR)
    std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const;
#else
    std::auto_ptr<FittedBondDiscountCurve::FittingMethod> clone() const;
#endif
  private:
    Size size() const;
    DiscountFactor discountFunction(const Array& x, Time t) const;
};

}    // namespace QuantLib

#endif    // AdjustedSvenssonFitting_HPP
