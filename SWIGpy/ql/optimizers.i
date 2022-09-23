#ifndef ql_optimizers_i
#define ql_optimizers_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Constraint;
using QuantLib::BoundaryConstraint;
using QuantLib::CompositeConstraint;
using QuantLib::NoConstraint;
using QuantLib::NonhomogeneousBoundaryConstraint;
using QuantLib::PositiveConstraint;
using QuantLib::EndCriteria;
using QuantLib::LineSearch;
using QuantLib::ArmijoLineSearch;
using QuantLib::GoldsteinLineSearch;
using QuantLib::OptimizationMethod;
using QuantLib::LineSearchBasedMethod;
using QuantLib::BFGS;
using QuantLib::ConjugateGradient;
using QuantLib::SteepestDescent;
using QuantLib::Simplex;
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
using QuantLib::SphereCylinderOptimizer;
using QuantLib::sphereCylinderOptimizerClosest;
typedef QuantLib::HestonModel::FellerConstraint FellerConstraint;
%}

%shared_ptr(Constraint)
class Constraint {
  public:
    Constraint();
    bool empty() const;
    bool test(const Array& p) const;
    Array upperBound(const Array& params);
    Array lowerBound(const Array& params);
    Real update(Array& p, const Array& direction, Real beta) const;
};

%shared_ptr(BoundaryConstraint)
class BoundaryConstraint : public Constraint {
  public:
    BoundaryConstraint(
        Real lower, 
        Real upper);
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
        const Constraint& c1,
        const Constraint& c2);
};

%shared_ptr(NonhomogeneousBoundaryConstraint)
class NonhomogeneousBoundaryConstraint : public Constraint {
  public:
    NonhomogeneousBoundaryConstraint(
        const Array& l, 
        const Array& u);
};

%shared_ptr(FellerConstraint)
class FellerConstraint : public Constraint {
  public:
    FellerConstraint();
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
    Size maxIterations() const;
    Size maxStationaryStateIterations() const;
    Real rootEpsilon() const;
    Real functionEpsilon() const;
    Real gradientNormEpsilon() const;
    bool operator()(
        Size iteration,
        Size& statState,
        const bool positiveOptimization,
        const Real fold,
        const Real normgold,
        const Real fnew,
        const Real normgnewx,
        EndCriteria::Type& ecType) const;
    bool checkMaxIterations(
        Size iteration,
        EndCriteria::Type& ecType) const;
    bool checkStationaryPoint(
        Real xOld, Real xNew,
        Size& statStateIterations,
        EndCriteria::Type& ecType) const;
    bool checkStationaryFunctionValue(
        Real fxOld, Real fxNew,
        Size& statStateIterations,
        EndCriteria::Type& ecType) const;
    bool checkStationaryFunctionAccuracy(
        Real f,
        bool positiveOptimization,
        EndCriteria::Type& ecType) const;
    bool checkZeroGradientNorm(
        Real gNorm,
        EndCriteria::Type& ecType) const;
    %extend {
        
    }
};

%shared_ptr(LineSearch)
class LineSearch {
  private:
    LineSearch();
  public:
    const Array& lastX();
    Real lastFunctionValue() const;
    const Array& lastGradient();
    Real lastGradientNorm2() const;
    bool succeed() const;
    const Array& searchDirection() const;
    Array& searchDirection();
};

%shared_ptr(ArmijoLineSearch)
class ArmijoLineSearch : public LineSearch {
  public:
    ArmijoLineSearch(
        Real eps = 1e-8,
        Real alpha = 0.05,
        Real beta = 0.65);
};

%shared_ptr(GoldsteinLineSearch)
class GoldsteinLineSearch : public LineSearch {
  public:
    GoldsteinLineSearch(
        Real eps = 1e-8,
        Real alpha = 0.05,
        Real beta = 0.65,
        Real extrapolation = 1.5);
};

%shared_ptr(OptimizationMethod)
class OptimizationMethod {
  private:
    OptimizationMethod();
  public:
    EndCriteria::Type minimize(
        Problem& P,
        const EndCriteria& endCriteria);
};

%shared_ptr(LineSearchBasedMethod)
class LineSearchBasedMethod : public OptimizationMethod {
  private:
    LineSearchBasedMethod(
        ext::shared_ptr<LineSearch> lSearch = ext::shared_ptr<LineSearch>());
};

%shared_ptr(BFGS)
class BFGS : public LineSearchBasedMethod {
  public:
    BFGS(
        const ext::shared_ptr<LineSearch> lSearch = ext::shared_ptr<LineSearch>());
};

%shared_ptr(ConjugateGradient)
class ConjugateGradient : public LineSearchBasedMethod {
  public:
    ConjugateGradient(
        const ext::shared_ptr<LineSearch> lSearch = ext::shared_ptr<LineSearch>());
};

%shared_ptr(SteepestDescent)
class SteepestDescent : public LineSearchBasedMethod {
  public:
    SteepestDescent(
        const ext::shared_ptr<LineSearch> lSearch = ext::shared_ptr<LineSearch>());
};

%shared_ptr(Simplex)
class Simplex : public OptimizationMethod {
    %rename(getLambda) lambda;
  public:
    Simplex(
        Real lambda);
    Real lambda();
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

%rename (DifferentialEvolutionConfiguration) DifferentialEvolution::Configuration;
%feature ("flatnested") DifferentialEvolution::Configuration;
%rename (DifferentialEvolutionCandidate) DifferentialEvolution::Candidate;
%feature ("flatnested") DifferentialEvolution::Candidate;
%shared_ptr(DifferentialEvolution)
class DifferentialEvolution : public OptimizationMethod {
  public:
    enum Strategy {
        Rand1Standard,
        BestMemberWithJitter,
        CurrentToBest2Diffs,
        Rand1DiffWithPerVectorDither,
        Rand1DiffWithDither,
        EitherOrWithOptimalRecombination,
        Rand1SelfadaptiveWithRotation
    };
    enum CrossoverType {
        Normal,
        Binomial,
        Exponential
    };
    struct Candidate {
        Array values;
        Real cost = 0.0;
        %extend {
            Candidate(Size size = 0) {
                DifferentialEvolution::Candidate candidate = {size};
                return new DifferentialEvolution::Candidate(
                    candidate);
            }
        }
    };

    class Configuration {
      public:
        Strategy strategy = BestMemberWithJitter;
        CrossoverType crossoverType = Normal;
        Size populationMembers = 100;
        Real stepsizeWeight = 0.2, crossoverProbability = 0.9;
        unsigned long seed = 0;
        bool applyBounds = true, crossoverIsAdaptive = false;
        std::vector<Array> initialPopulation;
        Array upperBound, lowerBound;

        Configuration();

        Configuration& withBounds(bool b = true);
        Configuration& withCrossoverProbability(Real p);
        Configuration& withPopulationMembers(Size n);
        Configuration& withInitialPopulation(const std::vector<Array>& c);
        Configuration& withUpperBound(const Array& u);
        Configuration& withLowerBound(const Array& l);
        Configuration& withSeed(unsigned long s);
        Configuration& withAdaptiveCrossover(bool b = true);
        Configuration& withStepsizeWeight(Real w);
        Configuration& withCrossoverType(CrossoverType t);
        Configuration& withStrategy(Strategy s);
    };

    DifferentialEvolution(
        const Configuration& configuration = Configuration());
    const Configuration& configuration() const;
};

class SamplerGaussian{
  public:
    SamplerGaussian(
        unsigned long seed = 0);
};

class SamplerLogNormal{
  public:
    SamplerLogNormal(
        unsigned long seed = 0);
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

class SphereCylinderOptimizer {
  public:
    SphereCylinderOptimizer(
        Real r,
        Real s,
        Real alpha,
        Real z1,
        Real z2,
        Real z3,
        Real zweight = 1.0);
    bool isIntersectionNonEmpty() const;
    %extend {
        void findClosest(
            Size maxIterations,
            Real tolerance,
            Value& yq1,
            Value& yq2,
            Value& yq3) const {
                Real y1, y2, y3;
                self->findClosest(maxIterations, tolerance, y1, y2, y3);
                yq1.setValue(y1);
                yq2.setValue(y2);
                yq3.setValue(y3);
            }
        bool findByProjection(
            Value& yq1,
            Value& yq2,
            Value& yq3) const {
                Real y1, y2, y3;
                bool b;
                b = self->findByProjection(y1, y2, y3);
                yq1.setValue(y1);
                yq2.setValue(y2);
                yq3.setValue(y3);
                return b;
            }
    }
};

std::vector<Real> sphereCylinderOptimizerClosest(
    Real r,
    Real s,
    Real alpha,
    Real z1,
    Real z2,
    Real z3,
    Natural maxIterations,
    Real tolerance,
    Real finalWeight = 1.0);



class Problem {
  public:
    Problem(
        CostFunction& costFunction,
        Constraint& constraint,
        Array initialValue = Array());

    void reset();
    Real value(const Array& x);
    Array values(const Array& x);
    void gradient(Array& grad_f,
                  const Array& x);
    Real valueAndGradient(Array& grad_f,
                          const Array& x);
    Constraint& constraint() const;
    CostFunction& costFunction() const;
    void setCurrentValue(const Array& currentValue);
    const Array& currentValue() const;
    void setFunctionValue(Real functionValue);
    Real functionValue() const;
    void setGradientNormValue(Real squaredNorm);
    Real gradientNormValue() const;
    Integer functionEvaluation() const;
    Integer gradientEvaluation() const;
};

#endif
