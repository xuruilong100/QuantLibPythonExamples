#ifndef DieboldLiFitting_HPP
#define DieboldLiFitting_HPP

#include <ql/auto_ptr.hpp>
#include <ql/termstructures/yield/fittedbonddiscountcurve.hpp>

namespace QuantLib {

//! Diebold-Li Fitting method
/*! Fits a discount function to the form
    \f$ d(t) = \exp^{-r t}, \f$ where the zero rate \f$r\f$ is defined as
    
    \f[
    r \equiv c_0 + (c_1 + c_2)*(1 - exp^{-\kappa t})/(\kappa t) -
    c_2 exp^{ - \kappa t},
    \f]
    
    \f$\kappa\f$ is a prespecified value.
    
    See: Ferstl R, Hayden J (2010). Zero-Coupon Yield Curve Estimation with
    the Package termstrc. Journal of Statistical Software, Volume 36, Issue 1.
*/
class DieboldLiFitting : public FittedBondDiscountCurve::FittingMethod {
  public:
    DieboldLiFitting(Real kappa,
                     const Array& weights = Array(),
                     ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
                     const Array& l2 = Array());
    DieboldLiFitting(Real kappa,
                     const Array& weights,
                     const Array& l2);
#if defined(QL_USE_STD_UNIQUE_PTR)
    std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const;
#else
    std::auto_ptr<FittedBondDiscountCurve::FittingMethod> clone() const;
#endif

    Real kappa() const { return kappa_; }

  private:
    Size size() const;
    DiscountFactor discountFunction(const Array& x, Time t) const;
    Real kappa_;
};

}    // namespace QuantLib

#endif    // DieboldLiFitting_HPP
