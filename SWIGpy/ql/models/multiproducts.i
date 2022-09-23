#ifndef ql_models_multiproduct_i
#define ql_models_multiproduct_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/models/curvestates.i

%{
using QuantLib::MarketModelMultiProduct;
using QuantLib::MarketModelComposite;
using QuantLib::CallSpecifiedMultiProduct;
using QuantLib::MultiProductMultiStep;
using QuantLib::MarketModelCashRebate;
using QuantLib::MultiProductOneStep;
using QuantLib::MultiProductPathwiseWrapper;
using QuantLib::MultiProductComposite;
using QuantLib::SingleProductComposite;
using QuantLib::ExerciseAdapter;
using QuantLib::MultiStepCoinitialSwaps;
using QuantLib::MultiStepCoterminalSwaps;
using QuantLib::MultiStepCoterminalSwaptions;
using QuantLib::MultiStepForwards;
using QuantLib::MultiStepInverseFloater;
using QuantLib::MultiStepNothing;
using QuantLib::MultiStepOptionlets;
using QuantLib::MultiStepPeriodCapletSwaptions;
using QuantLib::MultiStepRatchet;
using QuantLib::MultiStepSwap;
using QuantLib::MultiStepSwaption;
using QuantLib::MultiStepTarn;
using QuantLib::OneStepCoinitialSwaps;
using QuantLib::OneStepCoterminalSwaps;
using QuantLib::OneStepForwards;
using QuantLib::OneStepOptionlets;
typedef QuantLib::MarketModelMultiProduct::CashFlow MarketModelMultiProductCashFlow;
%}

%{
using QuantLib::MarketModelExerciseValue;
using QuantLib::BermudanSwaptionExerciseValue;
using QuantLib::NothingExerciseValue;
%}

struct MarketModelMultiProductCashFlow {
    // Size timeIndex;
    // Real amount;
    %extend {
        void timeIndex(Size i) {
            self->timeIndex = i;
        }
        void amount(Real a) {
            self->amount = a;
        }
        Size timeIndex() {
            return self->timeIndex;
        }
        Real amount() {
            return self->amount;
        }
    }
};

typedef QuantLib::MarketModelMultiProduct::CashFlow MarketModelMultiProductCashFlow;
%template(MarketModelMultiProductCashFlowVector) std::vector<MarketModelMultiProductCashFlow>;
%template(MarketModelMultiProductCashFlowVectorVector) std::vector<std::vector<MarketModelMultiProductCashFlow>>;

class MarketModelMultiProduct {
  private:
    MarketModelMultiProduct();
  public:
    std::vector<Size> suggestedNumeraires() const;
    const EvolutionDescription& evolution() const;
    std::vector<Time> possibleCashFlowTimes() const;
    Size numberOfProducts() const;
    Size maxNumberOfCashFlowsPerProductPerStep() const;
    void reset();
    bool nextTimeStep(
        const CurveState& currentState,
        std::vector<Size>& numberCashFlowsThisStep,
        std::vector<std::vector<MarketModelMultiProductCashFlow>>& cashFlowsGenerated);
};

%template(CloneMarketModelMultiProduct) Clone<MarketModelMultiProduct>;

class MarketModelComposite : public MarketModelMultiProduct {
  private:
    MarketModelComposite();
  public:
    void add(const Clone<MarketModelMultiProduct>&,
             Real multiplier = 1.0);
    void subtract(const Clone<MarketModelMultiProduct>&,
                  Real multiplier = 1.0);
    void finalize();
    Size size() const;
    const MarketModelMultiProduct& item(Size i) const;
    MarketModelMultiProduct& item(Size i);
    Real multiplier(Size i) const;
};

class CallSpecifiedMultiProduct : public MarketModelMultiProduct {
 public:
   CallSpecifiedMultiProduct(
       const Clone<MarketModelMultiProduct>& underlying,
       const Clone<ExerciseStrategy<CurveState>>&,
       Clone<MarketModelMultiProduct> rebate = Clone<MarketModelMultiProduct>());

    const MarketModelMultiProduct& underlying() const;
    const ExerciseStrategy<CurveState>& strategy() const;
    const MarketModelMultiProduct& rebate() const;
    void enableCallability();
    void disableCallability();
};

class MultiProductMultiStep : public MarketModelMultiProduct {
  private:
    MultiProductMultiStep();
};

class MarketModelCashRebate : public MarketModelMultiProduct {
  public:
    MarketModelCashRebate(
      EvolutionDescription evolution,
      const std::vector<Time>& paymentTimes,
      Matrix amounts,
      Size numberOfProducts);
};

class MultiProductOneStep : public MarketModelMultiProduct {
  private:
    MultiProductOneStep();
};

class MultiProductPathwiseWrapper : public MarketModelMultiProduct {
  public:
    MultiProductPathwiseWrapper(
        const MarketModelPathwiseMultiProduct& innerProduct_);
};

class MultiProductComposite : public MarketModelComposite {
  public:
    MultiProductComposite();
};

class SingleProductComposite : public MarketModelComposite {
  public:
    SingleProductComposite();
};

class ExerciseAdapter : public MultiProductMultiStep {
  public:
    ExerciseAdapter(
        const Clone<MarketModelExerciseValue>& exercise,
        Size numberOfProducts = 1);
    const MarketModelExerciseValue& exerciseValue() const;
};

class MultiStepCoinitialSwaps : public MultiProductMultiStep {
  public:
    MultiStepCoinitialSwaps(
        const std::vector<Time>& rateTimes,
        std::vector<Real> fixedAccruals,
        std::vector<Real> floatingAccruals,
        const std::vector<Time>& paymentTimes,
        double fixedRate);
};

class MultiStepCoterminalSwaps : public MultiProductMultiStep {
  public:
    MultiStepCoterminalSwaps(
        const std::vector<Time>& rateTimes,
        std::vector<Real> fixedAccruals,
        std::vector<Real> floatingAccruals,
        const std::vector<Time>& paymentTimes,
        Real fixedRate);
};

class MultiStepCoterminalSwaptions : public MultiProductMultiStep {
  public:
    MultiStepCoterminalSwaptions(
        const std::vector<Time>& rateTimes,
        const std::vector<Time>& paymentTimes,
        std::vector<ext::shared_ptr<StrikedTypePayoff>>);
};

class MultiStepForwards : public MultiProductMultiStep {
  public:
    MultiStepForwards(
        const std::vector<Time>& rateTimes,
        std::vector<Real> accruals,
        const std::vector<Time>& paymentTimes,
        std::vector<Rate> strikes);
};

class MultiStepInverseFloater : public MultiProductMultiStep {
  public:
    MultiStepInverseFloater(
        const std::vector<Time>& rateTimes,
        std::vector<Real> fixedAccruals,
        const std::vector<Real>& floatingAccruals,
        const std::vector<Real>& fixedStrikes,
        const std::vector<Real>& fixedMultipliers,
        const std::vector<Real>& floatingSpreads,
        const std::vector<Time>& paymentTimes,
        bool payer = true);
};

class MultiStepNothing : public MultiProductMultiStep {
  public:
    MultiStepNothing(
        const EvolutionDescription& evolution,
        Size numberOfProducts = 1,
        Size doneIndex = 0);
};

class MultiStepOptionlets : public MultiProductMultiStep {
  public:
    MultiStepOptionlets(
        const std::vector<Time>& rateTimes,
        std::vector<Real> accruals,
        const std::vector<Time>& paymentTimes,
        std::vector<ext::shared_ptr<Payoff>>);
};

class MultiStepPeriodCapletSwaptions : public MultiProductMultiStep {
  public:
    MultiStepPeriodCapletSwaptions(
        const std::vector<Time>& rateTimes,
        const std::vector<Time>& forwardOptionPaymentTimes,
        const std::vector<Time>& swaptionPaymentTimes,
        std::vector<ext::shared_ptr<StrikedTypePayoff>> forwardPayOffs,
        std::vector<ext::shared_ptr<StrikedTypePayoff>> swapPayOffs,
        Size period,
        Size offset);
};

class MultiStepRatchet : public MultiProductMultiStep {
  public:
    MultiStepRatchet(
        const std::vector<Time>& rateTimes,
        std::vector<Real> accruals,
        const std::vector<Time>& paymentTimes,
        Real gearingOfFloor,
        Real gearingOfFixing,
        Rate spreadOfFloor,
        Rate spreadOfFixing,
        Real initialFloor,
        bool payer = true);
};

class MultiStepSwap : public MultiProductMultiStep {
  public:
    MultiStepSwap(
        const std::vector<Time>& rateTimes,
        std::vector<Real> fixedAccruals,
        std::vector<Real> floatingAccruals,
        const std::vector<Time>& paymentTimes,
        Rate fixedRate,
        bool payer = true);
};

class MultiStepSwaption : public MultiProductMultiStep {
  public:
    MultiStepSwaption(
        const std::vector<Time>& rateTimes,
        Size startIndex,
        Size endIndex,
        ext::shared_ptr<StrikedTypePayoff> &);
};

class MultiStepTarn : public MultiProductMultiStep {
  public:
    MultiStepTarn(
        const std::vector<Time>& rateTimes,
        const std::vector<Real>& accruals,
        const std::vector<Real>& accrualsFloating,
        const std::vector<Time>& paymentTimes,
        const std::vector<Time>& paymentTimesFloating,
        Real totalCoupon,
        const std::vector<Real>& strikes,
        std::vector<Real> multipliers,
        const std::vector<Real>& floatingSpreads);
};

class OneStepCoinitialSwaps : public MultiProductOneStep {
  public:
    OneStepCoinitialSwaps(
        const std::vector<Time>& rateTimes,
        std::vector<Real> fixedAccruals,
        std::vector<Real> floatingAccruals,
        const std::vector<Time>& paymentTimes,
        double fixedRate);
};

class OneStepCoterminalSwaps : public MultiProductOneStep {
  public:
    OneStepCoterminalSwaps(
        const std::vector<Time>& rateTimes,
        std::vector<Real> fixedAccruals,
        std::vector<Real> floatingAccruals,
        const std::vector<Time>& paymentTimes,
        double fixedRate);
};

class OneStepForwards : public MultiProductOneStep {
  public:
    OneStepForwards(
        const std::vector<Time>& rateTimes,
        std::vector<Real> accruals,
        const std::vector<Time>& paymentTimes,
        std::vector<Rate> strikes);
};

class OneStepOptionlets : public MultiProductOneStep {
  public:
    OneStepOptionlets(
        const std::vector<Time>& rateTimes,
        std::vector<Real> accruals,
        const std::vector<Time>& paymentTimes,
        std::vector<ext::shared_ptr<Payoff>>);
};

class MarketModelExerciseValue {
  private:
    MarketModelExerciseValue();
  public:
    Size numberOfExercises() const;
    const EvolutionDescription& evolution() const;
    std::vector<Time> possibleCashFlowTimes() const;
    void nextStep(const CurveState&);
    void reset();
    MarketModelMultiProductCashFlow value(const CurveState&) const;
    %extend {
        std::vector<bool> isExerciseTime() const {
            std::valarray<bool> iet = self->isExerciseTime();
            std::vector<bool> rst(std::begin(iet), std::end(iet));
            return rst;
        }
    }
};

%template(CloneMarketModelExerciseValue) Clone<MarketModelExerciseValue>;

class BermudanSwaptionExerciseValue : public MarketModelExerciseValue {
  public:
    BermudanSwaptionExerciseValue(
        const std::vector<Time>& rateTimes,
        std::vector<ext::shared_ptr<Payoff>>);
};

class NothingExerciseValue : public MarketModelExerciseValue {
  public:
    NothingExerciseValue(
        const std::vector<Time>& rateTimes,
        std::valarray<bool> isExerciseTime = std::valarray<bool>());
};

#endif
