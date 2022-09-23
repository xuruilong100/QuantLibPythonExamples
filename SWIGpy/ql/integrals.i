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
using QuantLib::MomentBasedGaussianPolynomial;
using QuantLib::GaussNonCentralChiSquaredPolynomial;
using QuantLib::GaussLaguerreTrigonometricBase;
using QuantLib::GaussLaguerreCosinePolynomial;
using QuantLib::GaussLaguerreSinePolynomial;
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
using QuantLib::TabulatedGaussLegendre;
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
    DiscreteTrapezoidIntegrator(
        Size evaluations);
};

%shared_ptr(DiscreteSimpsonIntegrator)
class DiscreteSimpsonIntegrator: public Integrator {
  public:
    DiscreteSimpsonIntegrator(
        Size evaluations);
};

%shared_ptr(FilonIntegral)
class FilonIntegral : public Integrator {
  public:
    enum Type { Sine, Cosine };
    FilonIntegral(
        Type type, 
        Real t, 
        Size intervals);
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
    SegmentIntegral(
        Size intervals);
};

%shared_ptr(TrapezoidIntegral<Default>)
%shared_ptr(TrapezoidIntegral<MidPoint>)
template <class IntegrationPolicy>
class TrapezoidIntegral : public Integrator {
  public:
    TrapezoidIntegral(
        Real accuracy, 
        Size maxIterations);
};

%template(TrapezoidIntegralDefault) TrapezoidIntegral<Default>;
%template(TrapezoidIntegralMidPoint) TrapezoidIntegral<MidPoint>;

%shared_ptr(SimpsonIntegral)
class SimpsonIntegral : public TrapezoidIntegral<Default> {
  public:
    SimpsonIntegral(
        Real accuracy, 
        Size maxIterations);
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
    GaussLaguerrePolynomial(
        Real s = 0.0);
};

class GaussHermitePolynomial : public GaussianOrthogonalPolynomial {
  public:
    GaussHermitePolynomial(
        Real mu = 0.0);
};

class GaussJacobiPolynomial : public GaussianOrthogonalPolynomial {
  public:
    GaussJacobiPolynomial(
        Real alpha, 
        Real beta);
};

class GaussHyperbolicPolynomial : public GaussianOrthogonalPolynomial {
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
    GaussGegenbauerPolynomial(
        Real lambda);
};

template <class mp_real>
class MomentBasedGaussianPolynomial : public GaussianOrthogonalPolynomial {
  private:
    MomentBasedGaussianPolynomial();
  public:
    mp_real moment(Size i) const;
};

%template(MomentBasedRealGaussianPolynomial) MomentBasedGaussianPolynomial<Real>;
typedef MomentBasedGaussianPolynomial<Real> MomentBasedRealGaussianPolynomial;

class GaussNonCentralChiSquaredPolynomial : public MomentBasedGaussianPolynomial<Real> {
  public:
    GaussNonCentralChiSquaredPolynomial(
        Real nu, 
        Real lambda);
};

template <class mp_real>
class GaussLaguerreTrigonometricBase : public MomentBasedGaussianPolynomial<mp_real> {
  private:
    GaussLaguerreTrigonometricBase();
};

%template(GaussLaguerreTrigonometricBaseReal) GaussLaguerreTrigonometricBase<Real>;
typedef GaussLaguerreTrigonometricBase<Real> GaussLaguerreTrigonometricBaseReal;

template <class mp_real>
class GaussLaguerreCosinePolynomial : public GaussLaguerreTrigonometricBase<mp_real> {
  public:
    GaussLaguerreCosinePolynomial(
        Real u);
};

%template(GaussLaguerreCosineRealPolynomial) GaussLaguerreCosinePolynomial<Real>;

template <class mp_real>
class GaussLaguerreSinePolynomial : public GaussLaguerreTrigonometricBase<mp_real> {
  public:
    GaussLaguerreSinePolynomial(
        Real u);
};

%template(GaussLaguerreSineRealPolynomial) GaussLaguerreSinePolynomial<Real>;

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
    GaussLaguerreIntegration(
        Size n, 
        Real s = 0.0);
};

class GaussHermiteIntegration : public GaussianQuadrature {
  public:
    GaussHermiteIntegration(
        Size n, 
        Real mu = 0.0);
};

class GaussJacobiIntegration : public GaussianQuadrature {
  public:
    GaussJacobiIntegration(
        Size n, 
        Real alpha, 
        Real beta);
};

class GaussHyperbolicIntegration : public GaussianQuadrature {
  public:
    GaussHyperbolicIntegration(
        Size n);
};

class GaussLegendreIntegration : public GaussianQuadrature {
  public:
    GaussLegendreIntegration(
        Size n);
};

class GaussChebyshevIntegration : public GaussianQuadrature {
  public:
    GaussChebyshevIntegration(
        Size n);
};

class GaussChebyshev2ndIntegration : public GaussianQuadrature {
  public:
    GaussChebyshev2ndIntegration(
        Size n);
};

class GaussGegenbauerIntegration : public GaussianQuadrature {
  public:
    GaussGegenbauerIntegration(
        Size n, 
        Real lambda);
};

class TabulatedGaussLegendre {
  public:
    TabulatedGaussLegendre(
        Size n = 20);
    %extend {
        Real operator() (PyObject* f) const {
            return (*self)(UnaryFunction(f));
        }
    }
    
    void order(Size);
    Size order() const;
};

#endif
