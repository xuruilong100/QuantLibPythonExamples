#ifndef ql_integral_i
#define ql_integral_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Default;
using QuantLib::MidPoint;
using QuantLib::Integrator;
using QuantLib::DiscreteTrapezoidIntegral;
using QuantLib::DiscreteSimpsonIntegral;
using QuantLib::DiscreteTrapezoidIntegrator;
using QuantLib::DiscreteSimpsonIntegrator;
using QuantLib::FilonIntegral;
using QuantLib::GaussKronrodAdaptive;
using QuantLib::GaussKronrodNonAdaptive;
using QuantLib::GaussLobattoIntegral;
using QuantLib::PiecewiseIntegral;
using QuantLib::SegmentIntegral;
using QuantLib::TrapezoidIntegral;
using QuantLib::SimpsonIntegral;
%}

%{
using QuantLib::GaussianOrthogonalPolynomial;
using QuantLib::GaussLaguerrePolynomial;
using QuantLib::GaussHermitePolynomial;
using QuantLib::GaussJacobiPolynomial;
using QuantLib::GaussLegendrePolynomial;
using QuantLib::GaussChebyshevPolynomial;
using QuantLib::GaussChebyshev2ndPolynomial;
using QuantLib::GaussGegenbauerPolynomial;
using QuantLib::GaussHyperbolicPolynomial;
using QuantLib::GaussNonCentralChiSquaredPolynomial;
%}

%{
using QuantLib::GaussianQuadrature;
using QuantLib::GaussLaguerreIntegration;
using QuantLib::GaussHermiteIntegration;
using QuantLib::GaussJacobiIntegration;
using QuantLib::GaussHyperbolicIntegration;
using QuantLib::GaussLegendreIntegration;
using QuantLib::GaussChebyshev2ndIntegration;
using QuantLib::GaussChebyshevIntegration;
using QuantLib::GaussGegenbauerIntegration;
%}

%shared_ptr(Integrator)
class Integrator{
  private:
    Integrator();
  public:
    %extend {
        Real __call__(
          PyObject* pyFunction, Real a, Real b) {
          UnaryFunction f(pyFunction);
          return (*self)(f, a, b);
        }
    }

    void setAbsoluteAccuracy(Real);
    void setMaxEvaluations(Size);
    Real absoluteAccuracy() const;
    Size maxEvaluations() const;
    Real absoluteError() const ;
    Size numberOfEvaluations() const;
    bool integrationSuccess() const;
};

class DiscreteTrapezoidIntegral {
  public:
    Real operator()(const Array& x, const Array& f) const;
};

class DiscreteSimpsonIntegral {
  public:
    Real operator()(const Array& x, const Array& f) const;
};

%shared_ptr(DiscreteTrapezoidIntegrator)
class DiscreteTrapezoidIntegrator: public Integrator {
  public:
    explicit DiscreteTrapezoidIntegrator(Size evaluations);
};

%shared_ptr(DiscreteSimpsonIntegrator)
class DiscreteSimpsonIntegrator: public Integrator {
  public:
    explicit DiscreteSimpsonIntegrator(Size evaluations);
};

%shared_ptr(FilonIntegral)
class FilonIntegral : public Integrator {
  public:
    enum Type { Sine, Cosine };
    FilonIntegral(Type type, Real t, Size intervals);
};

%shared_ptr(GaussKronrodAdaptive)
class GaussKronrodAdaptive : public Integrator {
  public:
    GaussKronrodAdaptive(
        Real tolerance,
        Size maxFunctionEvaluations = Null<Size>());
};

%shared_ptr(GaussKronrodNonAdaptive)
class GaussKronrodNonAdaptive : public Integrator {
  public:
    GaussKronrodNonAdaptive(
        Real absoluteAccuracy,
        Size maxEvaluations,
        Real relativeAccuracy);
    void setRelativeAccuracy(Real);
    Real relativeAccuracy() const;
};

%shared_ptr(GaussLobattoIntegral)
class GaussLobattoIntegral : public Integrator {
  public:
    GaussLobattoIntegral(
        Size maxIterations,
        Real absAccuracy,
        Real relAccuracy = Null<Real>(),
        bool useConvergenceEstimate = true);
};

%shared_ptr(PiecewiseIntegral)
class PiecewiseIntegral : public Integrator {
  public:
    PiecewiseIntegral(
        ext::shared_ptr<Integrator> integrator,
        std::vector<Real> criticalPoints,
        bool avoidCriticalPoints = true);
};

%shared_ptr(SegmentIntegral)
class SegmentIntegral : public Integrator {
  public:
    SegmentIntegral(Size intervals);
};

%shared_ptr(TrapezoidIntegral<Default>)
%shared_ptr(TrapezoidIntegral<MidPoint>)
template <class IntegrationPolicy>
class TrapezoidIntegral : public Integrator {
  public:
    TrapezoidIntegral(Real accuracy, Size maxIterations);
};

%template(TrapezoidIntegralDefault) TrapezoidIntegral<Default>;
%template(TrapezoidIntegralMidPoint) TrapezoidIntegral<MidPoint>;

%shared_ptr(SimpsonIntegral)
class SimpsonIntegral : public TrapezoidIntegral<Default> {
  public:
    SimpsonIntegral(Real accuracy, Size maxIterations);
};

class GaussianOrthogonalPolynomial {
  private:
    GaussianOrthogonalPolynomial();
  public:
    Real mu_0()        const;
    Real alpha(Size i) const;
    Real beta(Size i)  const;
    Real w(Real x)     const;
    Real value(Size i, Real x) const;
    Real weightedValue(Size i, Real x) const;
};

class GaussLaguerrePolynomial : public GaussianOrthogonalPolynomial {
  public:
    explicit GaussLaguerrePolynomial(Real s = 0.0);
};

class GaussHermitePolynomial : public GaussianOrthogonalPolynomial {
  public:
    explicit GaussHermitePolynomial(Real mu = 0.0);
};

class GaussJacobiPolynomial : public GaussianOrthogonalPolynomial {
  public:
    explicit GaussJacobiPolynomial(Real alpha, Real beta);
};

class GaussLegendrePolynomial : public GaussJacobiPolynomial {
  public:
    GaussLegendrePolynomial();
};

class GaussChebyshevPolynomial : public GaussJacobiPolynomial {
  public:
    GaussChebyshevPolynomial();
};

class GaussChebyshev2ndPolynomial : public GaussJacobiPolynomial {
  public:
    GaussChebyshev2ndPolynomial();
};

class GaussGegenbauerPolynomial : public GaussJacobiPolynomial {
  public:
    explicit GaussGegenbauerPolynomial(Real lambda);
};

class GaussHyperbolicPolynomial : public GaussianOrthogonalPolynomial {
};

class GaussNonCentralChiSquaredPolynomial : public GaussianOrthogonalPolynomial {
  public:
    GaussNonCentralChiSquaredPolynomial(Real nu, Real lambda);
};

class GaussianQuadrature {
  public:
    GaussianQuadrature(
        Size n,
        const GaussianOrthogonalPolynomial& p);

    %extend {
        Real __call__(PyObject* pyFunction) {
            UnaryFunction f(pyFunction);
            return (*self)(f);
        }
    }
    Size order() const;
    const Array& weights();
    const Array& x();
};

class GaussLaguerreIntegration : public GaussianQuadrature {
  public:
    explicit GaussLaguerreIntegration(Size n, Real s = 0.0);
};

class GaussHermiteIntegration : public GaussianQuadrature {
  public:
    explicit GaussHermiteIntegration(Size n, Real mu = 0.0);
};

class GaussJacobiIntegration : public GaussianQuadrature {
  public:
    GaussJacobiIntegration(Size n, Real alpha, Real beta);
};

class GaussHyperbolicIntegration : public GaussianQuadrature {
  public:
    explicit GaussHyperbolicIntegration(Size n);
};

class GaussLegendreIntegration : public GaussianQuadrature {
  public:
    explicit GaussLegendreIntegration(Size n);
};

class GaussChebyshevIntegration : public GaussianQuadrature {
  public:
    explicit GaussChebyshevIntegration(Size n);
};

class GaussChebyshev2ndIntegration : public GaussianQuadrature {
  public:
    explicit GaussChebyshev2ndIntegration(Size n);
};

class GaussGegenbauerIntegration : public GaussianQuadrature {
  public:
    GaussGegenbauerIntegration(Size n, Real lambda);
};

#endif
