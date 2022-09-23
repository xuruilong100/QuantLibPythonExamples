#ifndef ql_models_pathwisemultiproduct_i
#define ql_models_pathwisemultiproduct_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/models/curvestates.i

%{
using QuantLib::MarketModelPathwiseMultiProduct;
using QuantLib::CallSpecifiedPathwiseMultiProduct;
using QuantLib::MarketModelPathwiseCashRebate;
using QuantLib::MarketModelPathwiseCoterminalSwaptionsDeflated;
using QuantLib::MarketModelPathwiseCoterminalSwaptionsNumericalDeflated;
using QuantLib::MarketModelPathwiseInverseFloater;
using QuantLib::MarketModelPathwiseMultiCaplet;
using QuantLib::MarketModelPathwiseMultiDeflatedCap;
using QuantLib::MarketModelPathwiseMultiDeflatedCaplet;
using QuantLib::MarketModelPathwiseSwap;
typedef MarketModelPathwiseMultiProduct::CashFlow MarketModelPathwiseMultiProductCashFlow;
%}

struct MarketModelPathwiseMultiProductCashFlow {
    // Size timeIndex;
    // std::vector<Real> amount;
    %extend {
        void timeIndex(Size i) {
            self->timeIndex = i;
        }
        void amount(const std::vector<Real>& a) {
            self->amount = a;
        }
        Size timeIndex() const {
            return self->timeIndex;
        }
        const std::vector<Real>& amount() const {
            return self->amount;
        }
    }
};

typedef MarketModelPathwiseMultiProduct::CashFlow MarketModelPathwiseMultiProductCashFlow;
%template(MarketModelPathwiseMultiProductCashFlowVector) std::vector<MarketModelPathwiseMultiProductCashFlow>;
%template(MarketModelPathwiseMultiProductCashFlowVectorVector) std::vector<std::vector<MarketModelPathwiseMultiProductCashFlow>>;

class MarketModelPathwiseMultiProduct {
  private:
    MarketModelPathwiseMultiProduct();
  public:
    std::vector<Size> suggestedNumeraires() const;
    const EvolutionDescription& evolution() const;
    std::vector<Time> possibleCashFlowTimes() const;
    Size numberOfProducts() const;
    Size maxNumberOfCashFlowsPerProductPerStep() const;
    bool alreadyDeflated() const;
    void reset();
    bool nextTimeStep(
        const CurveState& currentState,
        std::vector<Size>& numberCashFlowsThisStep,
        std::vector<std::vector<MarketModelPathwiseMultiProductCashFlow>>& cashFlowsGenerated);
};

%template(CloneMarketModelPathwiseMultiProduct) Clone<MarketModelPathwiseMultiProduct>;

class CallSpecifiedPathwiseMultiProduct : public MarketModelPathwiseMultiProduct {
  public:
    CallSpecifiedPathwiseMultiProduct(
        const Clone<MarketModelPathwiseMultiProduct>& underlying,
        const Clone<ExerciseStrategy<CurveState>>&,
        Clone<MarketModelPathwiseMultiProduct> rebate = Clone<MarketModelPathwiseMultiProduct>());

    const MarketModelPathwiseMultiProduct& underlying() const;
    const ExerciseStrategy<CurveState>& strategy() const;
    const MarketModelPathwiseMultiProduct& rebate() const;
    void enableCallability();
    void disableCallability();
};

class MarketModelPathwiseCashRebate : public MarketModelPathwiseMultiProduct {
  public:
    MarketModelPathwiseCashRebate(
        EvolutionDescription evolution,
        const std::vector<Time>& paymentTimes,
        Matrix amounts,
        Size numberOfProducts);
};

class MarketModelPathwiseCoterminalSwaptionsDeflated : public MarketModelPathwiseMultiProduct {
  public:
    MarketModelPathwiseCoterminalSwaptionsDeflated(
        const std::vector<Time>& rateTimes,
        const std::vector<Rate>& strikes);
};

class MarketModelPathwiseCoterminalSwaptionsNumericalDeflated : public MarketModelPathwiseMultiProduct {
  public:
    MarketModelPathwiseCoterminalSwaptionsNumericalDeflated(
        const std::vector<Time>& rateTimes,
        const std::vector<Rate>& strikes,
        Real bumpSize_);
};

class MarketModelPathwiseInverseFloater : public MarketModelPathwiseMultiProduct {
  public:
    MarketModelPathwiseInverseFloater(
        const std::vector<Time>& rateTimes,
        std::vector<Real> fixedAccruals,
        const std::vector<Real>& floatingAccruals,
        const std::vector<Real>& fixedStrikes,
        const std::vector<Real>& fixedMultipliers,
        const std::vector<Real>& floatingSpreads,
        const std::vector<Time>& paymentTimes,
        bool payer = true);
};

class MarketModelPathwiseMultiCaplet : public MarketModelPathwiseMultiProduct {
  public:
    MarketModelPathwiseMultiCaplet(
        const std::vector<Time>& rateTimes,
        const std::vector<Real>& accruals,
        const std::vector<Time>& paymentTimes,
        const std::vector<Rate>& strikes);
};

class MarketModelPathwiseMultiDeflatedCap : public MarketModelPathwiseMultiProduct {
  public:
    MarketModelPathwiseMultiDeflatedCap(
        const std::vector<Time>& rateTimes,
        const std::vector<Real>& accruals,
        const std::vector<Time>& paymentTimes,
        Rate strike,
        std::vector<std::pair<Size, Size>> startsAndEnds);
};

class MarketModelPathwiseMultiDeflatedCaplet : public MarketModelPathwiseMultiProduct {
  public:
    MarketModelPathwiseMultiDeflatedCaplet(
        const std::vector<Time>& rateTimes,
        const std::vector<Real>& accruals,
        const std::vector<Time>& paymentTimes,
        const std::vector<Rate>& strikes);

    MarketModelPathwiseMultiDeflatedCaplet(
        const std::vector<Time>& rateTimes,
        const std::vector<Real>& accruals,
        const std::vector<Time>& paymentTimes,
        Rate strike);
};

class MarketModelPathwiseSwap : public MarketModelPathwiseMultiProduct {
  public:
    MarketModelPathwiseSwap(
        const std::vector<Time>& rateTimes,
        const std::vector<Time>& accruals,
        const std::vector<Rate>& strikes,
        Real multiplier = 1.0);
};
#endif
