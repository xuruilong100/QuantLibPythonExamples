#ifndef ql_models_evolver_i
#define ql_models_evolver_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/slv.i
%include ../ql/models/curvestates.i

%{
using QuantLib::MarketModelEvolver;
using QuantLib::ConstrainedEvolver;
using QuantLib::LogNormalCmSwapRatePc;
using QuantLib::LogNormalCotSwapRatePc;
using QuantLib::LogNormalFwdRateBalland;
using QuantLib::LogNormalFwdRateEuler;
using QuantLib::LogNormalFwdRateIpc;
using QuantLib::LogNormalFwdRatePc;
using QuantLib::LogNormalFwdRateiBalland;
using QuantLib::NormalFwdRatePc;
using QuantLib::SVDDFwdRatePc;
using QuantLib::LogNormalFwdRateEulerConstrained;
using QuantLib::AccountingEngine;
using QuantLib::UpperBoundEngine;
using QuantLib::ProxyGreekEngine;
using QuantLib::PathwiseAccountingEngine;
using QuantLib::PathwiseVegasAccountingEngine;
using QuantLib::PathwiseVegasOuterAccountingEngine;
%}

%shared_ptr(MarketModelEvolver)
class MarketModelEvolver {
  private:
    MarketModelEvolver();
  public:
    const std::vector<Size>& numeraires() const;
    Real startNewPath();
    Real advanceStep();
    Size currentStep() const;
    const CurveState& currentState() const;
    void setInitialState(const CurveState&);
};

%template(MarketModelEvolverVector) std::vector<ext::shared_ptr<MarketModelEvolver>>;

%shared_ptr(ConstrainedEvolver)
class ConstrainedEvolver : public MarketModelEvolver {
  private:
    ConstrainedEvolver();
  public:
    void setConstraintType(
        const std::vector<Size>& startIndexOfSwapRate,
        const std::vector<Size>& EndIndexOfSwapRate);
    %extend {
        void setThisConstraint(
            const std::vector<Rate>& rateConstraints,
            const std::vector<bool>& isConstraintActive) {
                std::valarray<bool> c(isConstraintActive.size());
                std::copy(isConstraintActive.begin(), isConstraintActive.end(), std::begin(c));
                self->setThisConstraint(rateConstraints, c);
            }
    }
};

%template(ConstrainedEvolverVector) std::vector<ext::shared_ptr<ConstrainedEvolver>>;
%template(ConstrainedEvolverVectorVector) std::vector<std::vector<ext::shared_ptr<ConstrainedEvolver>>>;

%shared_ptr(LogNormalCmSwapRatePc)
class LogNormalCmSwapRatePc : public MarketModelEvolver {
  public:
    LogNormalCmSwapRatePc(
        Size spanningForwards,
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

%shared_ptr(LogNormalCotSwapRatePc)
class LogNormalCotSwapRatePc : public MarketModelEvolver {
  public:
    LogNormalCotSwapRatePc(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

%shared_ptr(LogNormalFwdRateBalland)
class LogNormalFwdRateBalland : public MarketModelEvolver {
  public:
    LogNormalFwdRateBalland(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

%shared_ptr(LogNormalFwdRateEuler)
class LogNormalFwdRateEuler : public MarketModelEvolver {
  public:
    LogNormalFwdRateEuler(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
    const std::vector<Real>& browniansThisStep() const;
};

%shared_ptr(LogNormalFwdRateIpc)
class LogNormalFwdRateIpc : public MarketModelEvolver {
  public:
    LogNormalFwdRateIpc(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

%shared_ptr(LogNormalFwdRatePc)
class LogNormalFwdRatePc : public MarketModelEvolver {
  public:
    LogNormalFwdRatePc(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

%shared_ptr(LogNormalFwdRateiBalland)
class LogNormalFwdRateiBalland : public MarketModelEvolver {
  public:
    LogNormalFwdRateiBalland(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

%shared_ptr(NormalFwdRatePc)
class NormalFwdRatePc : public MarketModelEvolver {
  public:
    NormalFwdRatePc(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

%shared_ptr(SVDDFwdRatePc)
class SVDDFwdRatePc : public MarketModelEvolver {
  public:
    SVDDFwdRatePc(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const ext::shared_ptr<MarketModelVolProcess>& volProcess,
        Size firstVolatilityFactor,
        Size volatilityFactorStep,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

%shared_ptr(LogNormalFwdRateEulerConstrained)
class LogNormalFwdRateEulerConstrained : public ConstrainedEvolver {
  public:
    LogNormalFwdRateEulerConstrained(
        const ext::shared_ptr<MarketModel>&,
        const BrownianGeneratorFactory&,
        const std::vector<Size>& numeraires,
        Size initialStep = 0);
};

class AccountingEngine {
  public:
    AccountingEngine(
        ext::shared_ptr<MarketModelEvolver> evolver,
        const Clone<MarketModelMultiProduct>& product,
        Real initialNumeraireValue);
    void multiplePathValues(SequenceStatisticsInc& stats, Size numberOfPaths);
};

class UpperBoundEngine {
  public:
    UpperBoundEngine(
        ext::shared_ptr<MarketModelEvolver> evolver,
        std::vector<ext::shared_ptr<MarketModelEvolver>> innerEvolvers,
        const MarketModelMultiProduct& underlying,
        const MarketModelExerciseValue& rebate,
        const MarketModelMultiProduct& hedge,
        const MarketModelExerciseValue& hedgeRebate,
        const ExerciseStrategy<CurveState>& hedgeStrategy,
        Real initialNumeraireValue);
    std::pair<Real,Real> singlePathValue(Size innerPaths);
    void multiplePathValues(Statistics& stats, Size outerPaths, Size innerPaths);
};

class ProxyGreekEngine {
  public:
    ProxyGreekEngine(
        ext::shared_ptr<MarketModelEvolver> evolver,
        std::vector<std::vector<ext::shared_ptr<ConstrainedEvolver>> > constrainedEvolvers,
        std::vector<std::vector<std::vector<Real>> > diffWeights,
        std::vector<Size> startIndexOfConstraint,
        std::vector<Size> endIndexOfConstraint,
        const Clone<MarketModelMultiProduct>& product,
        Real initialNumeraireValue);
    void multiplePathValues(
              SequenceStatisticsInc& stats,
              std::vector<std::vector<SequenceStatisticsInc>>& modifiedStats,
              Size numberOfPaths);
    void singlePathValues(
            std::vector<Real>& values,
            std::vector<std::vector<std::vector<Real>> >& modifiedValues);
};

class PathwiseAccountingEngine {
  public:
    PathwiseAccountingEngine(
        ext::shared_ptr<LogNormalFwdRateEuler> evolver,
        const Clone<MarketModelPathwiseMultiProduct>& product,
        ext::shared_ptr<MarketModel> pseudoRootStructure,
        Real initialNumeraireValue);
    void multiplePathValues(
        SequenceStatisticsInc& stats,
        Size numberOfPaths);
};

class PathwiseVegasAccountingEngine {
  public:
    PathwiseVegasAccountingEngine(
        ext::shared_ptr<LogNormalFwdRateEuler> evolver,
        const Clone<MarketModelPathwiseMultiProduct>& product,
        ext::shared_ptr<MarketModel> pseudoRootStructure,
        const std::vector<std::vector<Matrix>>& VegaBumps,
        Real initialNumeraireValue);
    void multiplePathValues(
        std::vector<Real>& means,
        std::vector<Real>& errors,
        Size numberOfPaths);
};

class PathwiseVegasOuterAccountingEngine {
  public:
    PathwiseVegasOuterAccountingEngine(
        ext::shared_ptr<LogNormalFwdRateEuler> evolver,
        const Clone<MarketModelPathwiseMultiProduct>& product,
        ext::shared_ptr<MarketModel> pseudoRootStructure,
        const std::vector<std::vector<Matrix>>& VegaBumps,
        Real initialNumeraireValue);
    void multiplePathValues(
        std::vector<Real>& means,
        std::vector<Real>& errors,
        Size numberOfPaths);
    void multiplePathValuesElementary(
        std::vector<Real>& means,
        std::vector<Real>& errors,
        Size numberOfPaths);
};

#endif
