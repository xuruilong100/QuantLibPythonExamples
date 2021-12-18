#ifndef CubicSplinesFitting_HPP
#define CubicSplinesFitting_HPP

#include <ql/auto_ptr.hpp>
#include <ql/termstructures/yield/fittedbonddiscountcurve.hpp>
#include <qlex/math/CubicSpline.hpp>

namespace QuantLib {

//! Cubic splines fitting method
/*! Fits a discount function to a set of cubic splines
    \f$ c_l(t) \f$, i.e.,
    
    \f[
    d(t) = 1 + \sum_{l=1}^n \beta_l c_l(t)
    \f]
    
    See: Ferstl R, Hayden J (2010). Zero-Coupon Yield Curve Estimation with
    the Package termstrc. Journal of Statistical Software, Volume 36, Issue 1.
    
    McCulloch JH (1975). The Tax-Adjusted Yield Curve. The Journal of Finance, 30(3), 811–830.
*/
class CubicSplinesFitting : public FittedBondDiscountCurve::FittingMethod {
  public:
    CubicSplinesFitting(const std::vector<Time>& knotVector,
                        const Array& weights = Array(),
                        ext::shared_ptr<OptimizationMethod>
                            optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
                        const Array& l2 = Array());
    CubicSplinesFitting(const std::vector<Time>& knotVector,
                        const Array& weights,
                        const Array& l2);
    //! cubic spline basis functions
    Real basisFunction(Integer i, Time t) const;

    //! function that calculates knot points from maturities of bonds
    static std::vector<Time> autoKnots(const std::vector<Time>& maturities);
#if defined(QL_USE_STD_UNIQUE_PTR)
    std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const;
#else
    std::auto_ptr<FittedBondDiscountCurve::FittingMethod> clone() const;
#endif
  private:
    Size size() const;
    DiscountFactor discountFunction(const Array& x, Time t) const;
    CubicSpline splines_;
    Size size_;
};

}    // namespace QuantLib

#endif    // CubicSplinesFitting_HPP
