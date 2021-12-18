#ifndef QuadraticSplinesFitting_HPP
#define QuadraticSplinesFitting_HPP

#include <ql/auto_ptr.hpp>
#include <ql/termstructures/yield/fittedbonddiscountcurve.hpp>
#include <qlex/math/QuadraticSpline.hpp>

namespace QuantLib {

//! Quadratic splines fitting method
/*! Fits a discount function to a set of quadratic splines
    \f$ c_l(t) \f$, i.e.,
    
    \f[
    d(t) = 1 + \sum_{l=1}^n \beta_l c_l(t)
    \f]
    
    See: McCulloch JH (1971). Measuring the Term Structure of Interest Rates. The Journal of
    Business, 44(1), 19-31.
*/

class QuadraticSplinesFitting : public FittedBondDiscountCurve::FittingMethod {
  public:
    QuadraticSplinesFitting(const std::vector<Time>& knotVector,
                            const Array& weights = Array(),
                            ext::shared_ptr<OptimizationMethod>
                                optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
                            const Array& l2 = Array());
    QuadraticSplinesFitting(const std::vector<Time>& knotVector,
                            const Array& weights,
                            const Array& l2);
    //! quadratic spline basis functions
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
    QuadraticSpline splines_;
    Size size_;
};

}    // namespace QuantLib

#endif    // QuadraticSplinesFitting_HPP
