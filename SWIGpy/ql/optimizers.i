#ifndef ql_optimizers_i
#define ql_optimizers_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include stl.i

%{
using QuantLib::Constraint;
using QuantLib::BoundaryConstraint;
using QuantLib::CompositeConstraint;
using QuantLib::NoConstraint;
using QuantLib::NonhomogeneousBoundaryConstraint;
using QuantLib::PositiveConstraint;
using QuantLib::EndCriteria;
using QuantLib::OptimizationMethod;
using QuantLib::ConjugateGradient;
using QuantLib::Simplex;
using QuantLib::SteepestDescent;
using QuantLib::BFGS;
using QuantLib::LevenbergMarquardt;
using QuantLib::DifferentialEvolution;
using QuantLib::SamplerGaussian;
using QuantLib::SamplerLogNormal;
using QuantLib::SamplerMirrorGaussian;
using QuantLib::ProbabilityBoltzmannDownhill;
using QuantLib::TemperatureExponential;
using QuantLib::ReannealingTrivial;
using QuantLib::GaussianSimulatedAnnealing;
using QuantLib::MirrorGaussianSimulatedAnnealing;
using QuantLib::LogNormalSimulatedAnnealing;
using QuantLib::Problem;
%}

%shared_ptr(Constraint)
class Constraint {
    // prevent direct instantiation
  private:
    Constraint();
  public:
    bool empty() const;
    bool test(const Array& p) const;
    Array upperBound(const Array& params);
    Array lowerBound(const Array& params);
    Real update(Array& p, const Array& direction, Real beta) const;
};

%shared_ptr(BoundaryConstraint)
class BoundaryConstraint : public Constraint {
  public:
    BoundaryConstraint(Real lower, Real upper);
};

%shared_ptr(NoConstraint)
class NoConstraint : public Constraint {
  public:
    NoConstraint();
};

%shared_ptr(PositiveConstraint)
class PositiveConstraint : public Constraint {
  public:
    PositiveConstraint();
};

%shared_ptr(CompositeConstraint)
class CompositeConstraint : public Constraint {
  public:
    CompositeConstraint(
        const Constraint& c1, const Constraint& c2);
};

%shared_ptr(NonhomogeneousBoundaryConstraint)
class NonhomogeneousBoundaryConstraint : public Constraint {
  public:
    NonhomogeneousBoundaryConstraint(
        const Array& l, const Array& u);
};

%shared_ptr(EndCriteria)
class EndCriteria {
    %rename(NoCriteria) None;

  public:
    enum Type {
        None,
        MaxIterations,
        StationaryPoint,
        StationaryFunctionValue,
        StationaryFunctionAccuracy,
        ZeroGradientNorm,
        Unknown
    };
    EndCriteria(
        Size maxIteration,
        Size maxStationaryStateIterations,
        Real rootEpsilon,
        Real functionEpsilon,
        Real gradientNormEpsilon);
    bool operator()(
        Size iteration,
        Size& statState,
        const bool positiveOptimization,
        const Real fold,
        const Real normgold,
        const Real fnew,
        const Real normgnewx,
        EndCriteria::Type& ecType) const;
};

%shared_ptr(OptimizationMethod)
class OptimizationMethod {
  private:
    // prevent direct instantiation
    OptimizationMethod();
};

%shared_ptr(ConjugateGradient)
class ConjugateGradient : public OptimizationMethod {
  public:
    ConjugateGradient();
};

%shared_ptr(Simplex)
class Simplex : public OptimizationMethod {
    %rename(getLambda) lambda;
  public:
    Simplex(Real lambda);
    Real lambda();
};

%shared_ptr(SteepestDescent)
class SteepestDescent : public OptimizationMethod {
  public:
    SteepestDescent();
};

%shared_ptr(BFGS)
class BFGS : public OptimizationMethod {
  public:
    BFGS();
};

%shared_ptr(LevenbergMarquardt)
class LevenbergMarquardt : public OptimizationMethod {
  public:
    LevenbergMarquardt(
        Real epsfcn = 1.0e-8,
        Real xtol = 1.0e-8,
        Real gtol = 1.0e-8,
        bool useCostFunctionsJacobian = false);
};

%shared_ptr(DifferentialEvolution)
class DifferentialEvolution : public OptimizationMethod {
  public:
    DifferentialEvolution();
};

class SamplerGaussian{
  public:
    SamplerGaussian(unsigned long seed = 0);
};

class SamplerLogNormal{
  public:
    SamplerLogNormal(unsigned long seed = 0);
};

class SamplerMirrorGaussian{
  public:
    SamplerMirrorGaussian(
        const Array& lower,
        const Array& upper,
        unsigned long seed = 0);
};

class ProbabilityBoltzmannDownhill{
  public:
    ProbabilityBoltzmannDownhill(
        unsigned long seed = 0);
};

class TemperatureExponential {
  public:
    TemperatureExponential(
        Real initialTemp,
        Size dimension,
        Real power = 0.95);
};

class ReannealingTrivial {
  public:
    ReannealingTrivial();
};

%shared_ptr(GaussianSimulatedAnnealing)
class GaussianSimulatedAnnealing : public OptimizationMethod {
  public:
    enum ResetScheme {
        NoResetScheme,
        ResetToBestPoint,
        ResetToOrigin
    };
    GaussianSimulatedAnnealing(
        const SamplerGaussian& sampler,
        const ProbabilityBoltzmannDownhill& probability,
        const TemperatureExponential& temperature,
        const ReannealingTrivial& reannealing = ReannealingTrivial(),
        Real startTemperature = 200.0,
        Real endTemperature = 0.01,
        Size reAnnealSteps = 50,
        ResetScheme resetScheme = ResetToBestPoint,
        Size resetSteps = 150);
};

%shared_ptr(MirrorGaussianSimulatedAnnealing)
class MirrorGaussianSimulatedAnnealing : public OptimizationMethod {
  public:
    enum ResetScheme {
        NoResetScheme,
        ResetToBestPoint,
        ResetToOrigin
    };
    MirrorGaussianSimulatedAnnealing(
        const SamplerMirrorGaussian& sampler,
        const ProbabilityBoltzmannDownhill& probability,
        const TemperatureExponential& temperature,
        const ReannealingTrivial& reannealing = ReannealingTrivial(),
        Real startTemperature = 200.0,
        Real endTemperature = 0.01,
        Size reAnnealSteps = 50,
        ResetScheme resetScheme = ResetToBestPoint,
        Size resetSteps = 150);
};

%shared_ptr(LogNormalSimulatedAnnealing)
class LogNormalSimulatedAnnealing : public OptimizationMethod {
  public:
    enum ResetScheme {
        NoResetScheme,
        ResetToBestPoint,
        ResetToOrigin
    };
    LogNormalSimulatedAnnealing(
        const SamplerLogNormal& sampler,
        const ProbabilityBoltzmannDownhill& probability,
        const TemperatureExponential& temperature,
        const ReannealingTrivial& reannealing = ReannealingTrivial(),
        Real startTemperature = 10.0,
        Real endTemperature = 0.01,
        Size reAnnealSteps = 50,
        ResetScheme resetScheme = ResetToBestPoint,
        Size resetSteps = 150);
};

%inline %{
    class Optimizer {};
%}

%extend Optimizer {
    Array solve(
        PyObject* function, Constraint& c,
        OptimizationMethod& m, EndCriteria& e,
        Array& iv) {
        PyCostFunction f(function);
        Problem p(f, c, iv);
        m.minimize(p, e);
        return p.currentValue();
    }
}

#endif
