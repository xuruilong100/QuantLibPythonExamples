#ifndef ql_cashflows_IborLegCashFlows_i
#define ql_cashflows_IborLegCashFlows_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::IborLegCashFlows;
using QuantLib::SwapCashFlows;
using QuantLib::SwaptionCashFlows;
%}

class IborLegCashFlows {
  public:
    IborLegCashFlows(
        const Leg& iborLeg,
        const Handle<YieldTermStructure>& discountCurve,
        bool contTenorSpread = true);
    IborLegCashFlows();
    const Leg& floatLeg() const;
    const std::vector<Real>& floatTimes() const;
    const std::vector<Real>& floatWeights() const;
};

class SwapCashFlows : public IborLegCashFlows {
  public:
    SwapCashFlows(
        const ext::shared_ptr<VanillaSwap>& swap,
        const Handle<YieldTermStructure>& discountCurve,
        bool contTenorSpread = true);
    SwapCashFlows();
    const Leg& fixedLeg() const;
    const std::vector<Real>& fixedTimes() const;
    const std::vector<Real>& fixedWeights() const;
    const std::vector<Real>& annuityWeights() const;
};

class SwaptionCashFlows : public SwapCashFlows {
  public:
    SwaptionCashFlows(
        const ext::shared_ptr<Swaption>& swaption,
        const Handle<YieldTermStructure>& discountCurve,
        bool contTenorSpread = true);
    SwaptionCashFlows() = default;
    ext::shared_ptr<Swaption> swaption() const;
    const std::vector<Real>& exerciseTimes() const;
};

#endif
