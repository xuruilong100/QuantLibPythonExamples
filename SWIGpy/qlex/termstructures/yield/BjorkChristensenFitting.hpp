#ifndef BjorkChristensenFitting_HPP
#define BjorkChristensenFitting_HPP

#include <ql/auto_ptr.hpp>
#include <ql/termstructures/yield/fittedbonddiscountcurve.hpp>

namespace QuantLib {

//! Bjork-Christensen Fitting method
/*! Fits a discount function to the form
    \f$ d(t) = \exp^{-r t}, \f$ where the zero rate \f$r\f$ is defined as
    
    \f[
    r \equiv c_0 + (c_1 + c_2)(\frac {1 - exp^{-\kappa t}}{\kappa t})
    - c_2exp^{ - \kappa t}
    + c_3{(\frac{1 - exp^{-2\kappa t}}{2\kappa t})}.
    \f]
    
    See: De Pooter M (2007). Examining the Nelson-Siegel Class of Term
    Structure Models: In-Sample Fit versus Out-of-Sample Forecasting Performance.
    SSRN eLibrary. http://ssrn.com/paper=992748.

*/
class BjorkChristensenFitting : public FittedBondDiscountCurve::FittingMethod {
  public:
    BjorkChristensenFitting(const Array& weights = Array(),
                            ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
                            const Array& l2 = Array());
    BjorkChristensenFitting(const Array& weights, const Array& l2);
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

#endif    // BjorkChristensenFitting_HPP
