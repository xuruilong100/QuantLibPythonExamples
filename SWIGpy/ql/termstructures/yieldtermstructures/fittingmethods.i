#ifndef ql_termstructures_yieldtermstructures_fittingmethods_i
#define ql_termstructures_yieldtermstructures_fittingmethods_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FittedBondDiscountCurve;
typedef QuantLib::FittedBondDiscountCurve::FittingMethod FittingMethod;
%}

%{
using QuantLib::ExponentialSplinesFitting;
using QuantLib::NelsonSiegelFitting;
using QuantLib::SvenssonFitting;
using QuantLib::CubicBSplinesFitting;
using QuantLib::SimplePolynomialFitting;
using QuantLib::SpreadFittingMethod;
%}

class FittingMethod {
  private:
    FittingMethod();
  public:
    Size size() const;
    Array solution() const;
    Integer numberOfIterations() const;
    Real minimumCostValue() const;
    EndCriteria::Type errorCode() const;
    bool constrainAtZero() const;
    Array weights() const;
    Array l2() const;
    ext::shared_ptr<OptimizationMethod> optimizationMethod() const;
    DiscountFactor discount(
        const Array& x, Time t) const;
};

class ExponentialSplinesFitting : public FittingMethod {
  public:
    ExponentialSplinesFitting(
        bool constrainAtZero = true,
        const Array& weights = Array(),
        const ext::shared_ptr<OptimizationMethod>& optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array(),
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL,
        Size numCoeffs = 9,
        Real fixedKappa = Null<Real>());
    ExponentialSplinesFitting(
        bool constrainAtZero,
        const Array& weights,
        const Array& l2,
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL,
        Size numCoeffs = 9,
        Real fixedKappa = Null<Real>());
    ExponentialSplinesFitting(
        bool constrainAtZero,
        Size numCoeffs,
        Real fixedKappa,
        const Array& weights = Array());
};

class NelsonSiegelFitting : public FittingMethod {
  public:
    NelsonSiegelFitting(
        const Array& weights = Array(),
        const ext::shared_ptr<OptimizationMethod>& optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array(),
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
    NelsonSiegelFitting(
        const Array& weights,
        const Array& l2,
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
};

class SvenssonFitting : public FittingMethod {
  public:
    SvenssonFitting(
        const Array& weights = Array(),
        const ext::shared_ptr<OptimizationMethod>& optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array(),
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
    SvenssonFitting(
        const Array& weights,
        const Array& l2,
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
};

class CubicBSplinesFitting : public FittingMethod {
  public:
    CubicBSplinesFitting(
        const std::vector<Time>& knotVector,
        bool constrainAtZero = true,
        const Array& weights = Array(),
        const ext::shared_ptr<OptimizationMethod>& optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array(),
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
    CubicBSplinesFitting(
        const std::vector<Time>& knotVector,
        bool constrainAtZero,
        const Array& weights,
        const Array& l2,
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
    Real basisFunction(Integer i, Time t) const;
};

class SimplePolynomialFitting : public FittingMethod {
  public:
    SimplePolynomialFitting(
        Natural degree,
        bool constrainAtZero = true,
        const Array& weights = Array(),
        const ext::shared_ptr<OptimizationMethod>& optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array(),
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
    SimplePolynomialFitting(
        Natural degree,
        bool constrainAtZero,
        const Array& weights,
        const Array& l2,
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
};

class SpreadFittingMethod : public FittingMethod {
  public:
    SpreadFittingMethod(
        const ext::shared_ptr<FittingMethod>& method,
        Handle<YieldTermStructure> discountCurve,
        Real minCutoffTime = 0.0,
        Real maxCutoffTime = QL_MAX_REAL);
};

#endif
