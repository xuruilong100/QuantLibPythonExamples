#ifndef ql_models_curvestates_i
#define ql_models_curvestates_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CurveState;
using QuantLib::CMSwapCurveState;
using QuantLib::CoterminalSwapCurveState;
using QuantLib::LMMCurveState;
using QuantLib::LMMDriftCalculator;
using QuantLib::CMSMMDriftCalculator;
using QuantLib::ForwardForwardMappings::ForwardForwardJacobian;
using QuantLib::ForwardForwardMappings::YMatrix;
using QuantLib::ForwardForwardMappings::RestrictCurveState;
%}

%shared_ptr(CurveState)
class CurveState {
  private:
    CurveState();
  public:
    Size numberOfRates() const;
    const std::vector<Time>& rateTimes() const;
    const std::vector<Time>& rateTaus() const;

    Real discountRatio(Size i, Size j) const;
    Rate forwardRate(Size i) const;
    Rate coterminalSwapAnnuity(Size numeraire, Size i) const;
    Rate coterminalSwapRate(Size i) const;
    Rate cmSwapAnnuity(Size numeraire, Size i, Size spanningForwards) const;
    Rate cmSwapRate(Size i, Size spanningForwards) const;
    const std::vector<Rate>& forwardRates() const;
    const std::vector<Rate>& coterminalSwapRates() const;
    const std::vector<Rate>& cmSwapRates(Size spanningForwards) const;
    Rate swapRate(Size begin, Size end) const;
};

%shared_ptr(CMSwapCurveState)
class CMSwapCurveState : public CurveState {
  public:
    CMSwapCurveState(
        const std::vector<Time>& rateTimes,
        Size spanningForwards);
    void setOnCMSwapRates(
        const std::vector<Rate>& cmSwapRates,
        Size firstValidIndex = 0);
};

%shared_ptr(CoterminalSwapCurveState)
class CoterminalSwapCurveState : public CurveState {
  public:
    CoterminalSwapCurveState(
        const std::vector<Time>& rateTimes);
    void setOnCoterminalSwapRates(
        const std::vector<Rate>& swapRates,
        Size firstValidIndex = 0);
};

%shared_ptr(LMMCurveState)
class LMMCurveState : public CurveState {
  public:
    LMMCurveState(
      const std::vector<Time>& rateTimes);
    void setOnForwardRates(
        const std::vector<Rate>& fwdRates,
        Size firstValidIndex = 0);
    void setOnDiscountRatios(
        const std::vector<DiscountFactor>& discRatios,
        Size firstValidIndex = 0);
};

Matrix ForwardForwardJacobian(
    const CurveState& cs,
    Size multiplier,
    Size offset);

Matrix YMatrix(
    const CurveState& cs,
    const std::vector<Spread>& shortDisplacements,
    const std::vector<Spread>& longDisplacements,
    Size Multiplier,
    Size offset);

LMMCurveState RestrictCurveState(
    const CurveState& cs,
    Size multiplier,
    Size offSet);

class CMSMMDriftCalculator {
  public:
    CMSMMDriftCalculator(
        const Matrix& pseudo,
        const std::vector<Spread>& displacements,
        const std::vector<Time>& taus,
        Size numeraire,
        Size alive,
        Size spanningFwds);
    void compute(
        const CMSwapCurveState& cs,
        std::vector<Real>& drifts) const;
};

class LMMDriftCalculator {
  public:
    LMMDriftCalculator(
        const Matrix& pseudo,
        const std::vector<Spread>& displacements,
        const std::vector<Time>& taus,
        Size numeraire,
        Size alive);

    void compute(const LMMCurveState& cs,
                 std::vector<Real>& drifts) const;
    void compute(const std::vector<Rate>& fwds,
                 std::vector<Real>& drifts) const;

    void computePlain(const LMMCurveState& cs,
                      std::vector<Real>& drifts) const;
    void computePlain(const std::vector<Rate>& fwds,
                      std::vector<Real>& drifts) const;
    void computeReduced(const LMMCurveState& cs,
                        std::vector<Real>& drifts) const;
    void computeReduced(const std::vector<Rate>& fwds,
                        std::vector<Real>& drifts) const;
};

#endif
