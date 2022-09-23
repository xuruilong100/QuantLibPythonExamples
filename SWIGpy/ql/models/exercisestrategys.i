#ifndef ql_models_exercisestrategys_i
#define ql_models_exercisestrategys_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/models/curvestates.i

%{
using QuantLib::ExerciseStrategy;
using QuantLib::LongstaffSchwartzExerciseStrategy;
using QuantLib::ParametricExerciseAdapter;
using QuantLib::SwapRateTrigger;
%}

template <class State>
class ExerciseStrategy {
  private:
    ExerciseStrategy();
  public:
    std::vector<Time> exerciseTimes() const;
    std::vector<Time> relevantTimes() const;
    void reset();
    bool exercise(const State& currentState) const;
    void nextStep(const State& currentState);
};

typedef ExerciseStrategy<CurveState> CurveStateExerciseStrategy;
%template(CurveStateExerciseStrategy) ExerciseStrategy<CurveState>;
%template(CloneCurveStateExerciseStrategy) Clone<ExerciseStrategy<CurveState>>;

class LongstaffSchwartzExerciseStrategy : public ExerciseStrategy<CurveState> {
  public:
    LongstaffSchwartzExerciseStrategy(
        Clone<MarketModelBasisSystem> basisSystem,
        std::vector<std::vector<Real>> basisCoefficients,
        const EvolutionDescription& evolution,
        const std::vector<Size>& numeraires,
        Clone<MarketModelExerciseValue> exercise,
        Clone<MarketModelExerciseValue> control);
};

class ParametricExerciseAdapter : public ExerciseStrategy<CurveState> {
  public:
    ParametricExerciseAdapter(
        const MarketModelParametricExercise& exercise,
        std::vector<std::vector<Real>> parameters);
};

class SwapRateTrigger : public ExerciseStrategy<CurveState> {
  public:
    SwapRateTrigger(
        const std::vector<Time>& rateTimes,
        std::vector<Rate> swapTriggers,
        const std::vector<Time>& exerciseTimes);
};

#endif
