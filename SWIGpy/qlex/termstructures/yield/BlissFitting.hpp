#ifndef BlissFitting_HPP
#define BlissFitting_HPP

#include <ql/auto_ptr.hpp>
#include <ql/termstructures/yield/fittedbonddiscountcurve.hpp>

namespace QuantLib {

//! Bliss Fitting method
/*! Fits a discount function to the form
    \f$ d(t) = \exp^{-r t}, \f$ where the zero rate \f$r\f$ is defined as
    
    \f[
    r \equiv c_0 + c_1 \frac{1 - exp^{-\kappa t}}{\kappa t} +
    c_2(\frac{1 - exp^{-\kappa_1 t}}{\kappa_1 t} - exp^{ - \kappa_1 t}).
    \f]
    
    See: De Pooter M (2007). Examining the Nelson-Siegel Class of Term
    Structure Models: In-Sample Fit versus Out-of-Sample Forecasting Performance.
    SSRN eLibrary. http://ssrn.com/paper=992748.

*/
class BlissFitting : public FittedBondDiscountCurve::FittingMethod {
  public:
    BlissFitting(const Array& weights = Array(),
                 ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
                 const Array& l2 = Array());
    BlissFitting(const Array& weights, const Array& l2);
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

#endif    // BlissFitting_HPP
