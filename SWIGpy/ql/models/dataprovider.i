#ifndef ql_models_dataproviders_i
#define ql_models_dataproviders_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/models/curvestates.i

%{
using QuantLib::MarketModelNodeDataProvider;
using QuantLib::MarketModelBasisSystem;
using QuantLib::MarketModelParametricExercise;
using QuantLib::SwapForwardBasisSystem;
using QuantLib::SwapBasisSystem;
using QuantLib::TriggeredSwapExercise;
using QuantLib::ParametricExercise;
using QuantLib::genericEarlyExerciseOptimization;
using QuantLib::NodeData;
%}

struct NodeData {
    Real exerciseValue;
    Real cumulatedCashFlows;
    std::vector<Real> values;
    Real controlValue;
    bool isValid;
};

%template(NodeDataVector) std::vector<NodeData>;
%template(NodeDataVectorVector) std::vector<std::vector<NodeData>>;

class ParametricExercise {
  private:
    ParametricExercise();
  public:
    std::vector<Size> numberOfVariables() const;
    std::vector<Size> numberOfParameters() const;
    bool exercise(Size exerciseNumber,
                  const std::vector<Real>& parameters,
                  const std::vector<Real>& variables) const;
    void guess(Size exerciseNumber, std::vector<Real>& parameters) const;
};

Real genericEarlyExerciseOptimization(
    std::vector<std::vector<NodeData>>& simulationData,
    const ParametricExercise& exercise,
    std::vector<std::vector<Real>>& parameters,
    const EndCriteria& endCriteria,
    OptimizationMethod& method);

class MarketModelNodeDataProvider {
  private:
    MarketModelNodeDataProvider();
  public:
    Size numberOfExercises() const;
    std::vector<Size> numberOfData() const;
    const EvolutionDescription& evolution() const;
    void nextStep(const CurveState&);
    void reset();
    void values(const CurveState&, std::vector<Real>& results) const;
    %extend {
        std::vector<bool> isExerciseTime() const {
            std::valarray<bool> iet = self->isExerciseTime();
            std::vector<bool> rst(std::begin(iet), std::end(iet));
            return rst;
        }
    }
};

class MarketModelBasisSystem : public MarketModelNodeDataProvider {
  private:
    MarketModelBasisSystem();
  public:
    std::vector<Size> numberOfFunctions() const;
};

%template(CloneMarketModelBasisSystem) Clone<MarketModelBasisSystem>;

class MarketModelParametricExercise : public MarketModelNodeDataProvider, public ParametricExercise {
  private:
    MarketModelParametricExercise();
};

class SwapForwardBasisSystem : public MarketModelBasisSystem {
  public:
    SwapForwardBasisSystem(
        const std::vector<Time>& rateTimes,
        const std::vector<Time>& exerciseTimes);
};

class SwapBasisSystem : public MarketModelBasisSystem {
  public:
    SwapBasisSystem(
        const std::vector<Time>& rateTimes,
        const std::vector<Time>& exerciseTimes);
};

class TriggeredSwapExercise : public MarketModelParametricExercise {
  public:
    TriggeredSwapExercise(
        const std::vector<Time>& rateTimes,
        const std::vector<Time>& exerciseTimes,
        std::vector<Rate> strikes);
};

#endif
