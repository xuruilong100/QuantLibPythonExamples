#ifndef ql_segment_integral_i
#define ql_segment_integral_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Default;
using QuantLib::MidPoint;
using QuantLib::SegmentIntegral;
using QuantLib::SimpsonIntegral;
using QuantLib::TrapezoidIntegral;
using QuantLib::GaussChebyshev2ndIntegration;
using QuantLib::GaussChebyshevIntegration;
using QuantLib::GaussGegenbauerIntegration;
using QuantLib::GaussHermiteIntegration;
using QuantLib::GaussHyperbolicIntegration;
using QuantLib::GaussJacobiIntegration;
using QuantLib::GaussKronrodAdaptive;
using QuantLib::GaussKronrodNonAdaptive;
using QuantLib::GaussLaguerreIntegration;
using QuantLib::GaussLegendreIntegration;
using QuantLib::GaussLobattoIntegral;
%}

%define INTEGRATION_METHODS
%extend {
    Real __call__(
        PyObject* pyFunction, Real a, Real b) {
        UnaryFunction f(pyFunction);
        return (*self)(f, a, b);    }

}
%enddef

%define GAUSSIAN_QUADRATURE_METHODS
%extend {
    Real __call__(PyObject* pyFunction) {
        UnaryFunction f(pyFunction);
        return (*self)(f);
    }
}
%enddef

class SegmentIntegral {
  public:
    SegmentIntegral(Size intervals);
    INTEGRATION_METHODS;
};

template <class IntegrationPolicy>
class TrapezoidIntegral {
  public:
    TrapezoidIntegral(Real accuracy, Size maxIterations);
    INTEGRATION_METHODS;
};

%template(TrapezoidIntegralDefault) TrapezoidIntegral<Default>;
%template(TrapezoidIntegralMidPoint) TrapezoidIntegral<MidPoint>;

class SimpsonIntegral {
  public:
    SimpsonIntegral(Real accuracy, Size maxIterations);
    INTEGRATION_METHODS;
};

class GaussKronrodAdaptive {
  public:
    GaussKronrodAdaptive(Real tolerance,
                         Size maxFunctionEvaluations = Null<Size>());
    INTEGRATION_METHODS;
};

class GaussKronrodNonAdaptive {
  public:
    GaussKronrodNonAdaptive(Real absoluteAccuracy,
                            Size maxEvaluations,
                            Real relativeAccuracy);
    INTEGRATION_METHODS;
};

class GaussLobattoIntegral {
  public:
    GaussLobattoIntegral(Size maxIterations,
                         Real absAccuracy,
                         Real relAccuracy = Null<Real>(),
                         bool useConvergenceEstimate = true);
    INTEGRATION_METHODS;
};

class GaussLaguerreIntegration {
  public:
    GaussLaguerreIntegration(Size n, Real s = 0.0);
    GAUSSIAN_QUADRATURE_METHODS;
};

class GaussHermiteIntegration {
  public:
    GaussHermiteIntegration(Size n, Real mu = 0.0);
    GAUSSIAN_QUADRATURE_METHODS;
};

class GaussJacobiIntegration {
  public:
    GaussJacobiIntegration(Size n, Real alpha, Real beta);
    GAUSSIAN_QUADRATURE_METHODS;
};

class GaussHyperbolicIntegration {
  public:
    GaussHyperbolicIntegration(Size n);
    GAUSSIAN_QUADRATURE_METHODS;
};

class GaussLegendreIntegration {
  public:
    GaussLegendreIntegration(Size n);
    GAUSSIAN_QUADRATURE_METHODS;
};

class GaussChebyshevIntegration {
  public:
    GaussChebyshevIntegration(Size n);
    GAUSSIAN_QUADRATURE_METHODS;
};

class GaussChebyshev2ndIntegration {
  public:
    GaussChebyshev2ndIntegration(Size n);
    GAUSSIAN_QUADRATURE_METHODS;
};

class GaussGegenbauerIntegration {
  public:
    GaussGegenbauerIntegration(Size n, Real lambda);
    GAUSSIAN_QUADRATURE_METHODS;
};


#endif
