#ifndef qlex_termstructures_yield_all
#define qlex_termstructures_yield_all

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/termstructures/yieldtermstructures/fittingmethods.i

%{
using QuantLib::AdjustedSvenssonFitting;
using QuantLib::BjorkChristensenFitting;
using QuantLib::BlissFitting;
using QuantLib::CubicSplinesFitting;
using QuantLib::DieboldLiFitting;
using QuantLib::QuadraticSplinesFitting;
using QuantLib::ChinaFixingRepoSwapRateHelper;
%}

class AdjustedSvenssonFitting : public FittingMethod {
  public:
    AdjustedSvenssonFitting(
        const Array& weights = Array(),
        ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array());
    AdjustedSvenssonFitting(const Array& weights, const Array& l2);
};

class BjorkChristensenFitting : public FittingMethod {
  public:
    BjorkChristensenFitting(
        const Array& weights = Array(),
        ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array());
    BjorkChristensenFitting(const Array& weights, const Array& l2);
};

class BlissFitting : public FittingMethod {
  public:
    BlissFitting(
        const Array& weights = Array(),
        ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array());
    BlissFitting(const Array& weights, const Array& l2);
};

class CubicSplinesFitting : public FittingMethod {
  public:
    CubicSplinesFitting(
        const std::vector<Time>& knotVector,
        const Array& weights = Array(),
        ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array());
    CubicSplinesFitting(
        const std::vector<Time>& knotVector,
        const Array& weights,
        const Array& l2);
    Real basisFunction(Integer i, Time t) const;
    static std::vector<Time> autoKnots(const std::vector<Time>& maturities);
};

class DieboldLiFitting : public FittingMethod {
  public:
    DieboldLiFitting(
        Real kappa,
        const Array& weights = Array(),
        ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array());
    DieboldLiFitting(
        Real kappa,
        const Array& weights,
        const Array& l2);
    Real kappa() const;
};

class QuadraticSplinesFitting : public FittingMethod {
  public:
    QuadraticSplinesFitting(
        const std::vector<Time>& knotVector,
        const Array& weights = Array(),
        ext::shared_ptr<OptimizationMethod> optimizationMethod = ext::shared_ptr<OptimizationMethod>(),
        const Array& l2 = Array());
    QuadraticSplinesFitting(
        const std::vector<Time>& knotVector,
        const Array& weights,
        const Array& l2);
    Real basisFunction(Integer i, Time t) const;
    static std::vector<Time> autoKnots(const std::vector<Time>& maturities);
};

%shared_ptr(ChinaFixingRepoSwapRateHelper)
class ChinaFixingRepoSwapRateHelper : public BootstrapHelper<YieldTermStructure> {
  public:
    ChinaFixingRepoSwapRateHelper(
        Natural settlementDays,
        const Period& tenor,
        const Handle<Quote>& fixedRate,
        ext::shared_ptr<ChinaFixingRepo> chinaFixingRepo,
        Handle<YieldTermStructure> discountingCurve = Handle<YieldTermStructure>(),
        Natural paymentLag = 0,
        BusinessDayConvention paymentConvention = Following,
        Frequency paymentFrequency = Annual,
        Calendar paymentCalendar = China(China::IB),
        const Period& forwardStart = 0 * Days,
        Real gearing = 1.0,
        Spread spread = 0.0,
        Pillar::Choice pillar = Pillar::LastRelevantDate,
        Date customPillarDate = Date());

    ext::shared_ptr<ChinaFixingRepoSwap> swap() const;
};

#endif
