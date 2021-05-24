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
%}

class FittingMethod {
  public:
    virtual ~FittingMethod() = 0;
    Size size() const;
    Array solution() const;
    Integer numberOfIterations() const;
    Real minimumCostValue() const;
    bool constrainAtZero() const;
    Array weights() const;
};

class ExponentialSplinesFitting : public FittingMethod {
  public:
    ExponentialSplinesFitting(
        bool constrainAtZero = true,
        const Array& weights = Array());
};

class NelsonSiegelFitting : public FittingMethod {
  public:
    NelsonSiegelFitting(
        const Array& weights = Array());
};

class SvenssonFitting : public FittingMethod {
  public:
    SvenssonFitting(
        const Array& weights = Array());
};

class CubicBSplinesFitting : public FittingMethod {
  public:
    CubicBSplinesFitting(
        const std::vector<Time>& knotVector,
        bool constrainAtZero = true,
        const Array& weights = Array());
    Real basisFunction(Integer i, Time t);
};

class SimplePolynomialFitting : public FittingMethod {
  public:
    SimplePolynomialFitting(
        Natural degree,
        bool constrainAtZero = true,
        const Array& weights = Array());
};

#endif
