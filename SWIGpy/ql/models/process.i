#ifndef ql_models_process_i
#define ql_models_process_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::MarketModelVolProcess;
using QuantLib::SquareRootAndersen;
%}

%shared_ptr(MarketModelVolProcess)
class MarketModelVolProcess {
  private:
    MarketModelVolProcess();
  public:
      Size variatesPerStep();
      Size numberSteps();
      void nextPath();
      Real nextstep(const std::vector<Real>& variates);
      Real stepSd() const;
      const std::vector<Real>& stateVariables() const;
      Size numberStateVariables() const;
};

%shared_ptr(SquareRootAndersen)
class SquareRootAndersen : public MarketModelVolProcess {
  public:
    SquareRootAndersen(
        Real meanLevel,
        Real reversionSpeed,
        Real volVar,
        Real v0,
        const std::vector<Real>& evolutionTimes,
        Size numberSubSteps_,
        Real w1,
        Real w2,
        Real cutPoint = 1.5);
};

#endif
