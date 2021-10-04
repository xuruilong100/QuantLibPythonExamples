#ifndef ql_instruments_options_others_all_i
#define ql_instruments_options_others_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/instruments/Option.i

%{
using QuantLib::CdsOption;
using QuantLib::FloatFloatSwaption;
using QuantLib::NonstandardSwaption;
using QuantLib::Swaption;
%}

%shared_ptr(CdsOption)
class CdsOption : public Option {
  public:
    CdsOption(
        const ext::shared_ptr<CreditDefaultSwap>& swap,
        const ext::shared_ptr<Exercise>& exercise,
        bool knocksOut = true);
    const ext::shared_ptr<CreditDefaultSwap>& underlyingSwap() const;
    Rate atmRate() const;
    Real riskyAnnuity() const;
    Volatility impliedVolatility(
        Real price,
        const Handle<YieldTermStructure>& termStructure,
        const Handle<DefaultProbabilityTermStructure>&,
        Real recoveryRate,
        Real accuracy = 1.e-4,
        Size maxEvaluations = 100,
        Volatility minVol = 1.0e-7,
        Volatility maxVol = 4.0) const;
};

%shared_ptr(FloatFloatSwaption)
class FloatFloatSwaption : public Option {
  public:
    FloatFloatSwaption(
        const ext::shared_ptr<FloatFloatSwap>& swap,
        const ext::shared_ptr<Exercise>& exercise,
        Settlement::Type delivery = Settlement::Physical,
        Settlement::Method settlementMethod = Settlement::PhysicalOTC);

    Settlement::Type settlementType() const;
    Settlement::Method settlementMethod() const;
    VanillaSwap::Type type() const;
    const ext::shared_ptr<FloatFloatSwap>& underlyingSwap() const;
    std::vector<ext::shared_ptr<BlackCalibrationHelper>> calibrationBasket(
        const ext::shared_ptr<SwapIndex>& standardSwapBase,
        const ext::shared_ptr<SwaptionVolatilityStructure>& swaptionVolatility,
        BasketGeneratingEngine::CalibrationBasketType basketType = BasketGeneratingEngine::MaturityStrikeByDeltaGamma) const;

    %extend {
        Real underlyingValue() {
            return self->result<Real>("underlyingValue");
        }
        std::vector<Real> probabilities() {
            return self->result<std::vector<Real>>("probabilities");
        }
    }
};

%shared_ptr(Swaption)
class Swaption : public Option {
  public:
    Swaption(
        ext::shared_ptr<VanillaSwap> swap,
        const ext::shared_ptr<Exercise>& exercise,
        Settlement::Type type = Settlement::Physical,
        Settlement::Method settlementMethod = Settlement::PhysicalOTC);

    Settlement::Type settlementType() const;
    Settlement::Method settlementMethod() const;
    Swap::Type type() const;
    const ext::shared_ptr<VanillaSwap>& underlyingSwap() const;
    Volatility impliedVolatility(
        Real price,
        const Handle<YieldTermStructure>& discountCurve,
        Volatility guess,
        Real accuracy = 1.0e-4,
        Natural maxEvaluations = 100,
        Volatility minVol = 1.0e-7,
        Volatility maxVol = 4.0,
        VolatilityType type = ShiftedLognormal,
        Real displacement = 0.0) const;
    %extend {
        Real vega() {
            return self->result<Real>("vega");
        }
        Real delta() {
            return self->result<Real>("delta");
        }
        Real annuity() {
            return self->result<Real>("annuity");
        }
    }
};

%shared_ptr(NonstandardSwaption)
class NonstandardSwaption : public Option {
  public:
    NonstandardSwaption(const Swaption& fromSwaption);
    NonstandardSwaption(
        const ext::shared_ptr<NonstandardSwap>& swap,
        const ext::shared_ptr<Exercise>& exercise,
        Settlement::Type type = Settlement::Physical,
        Settlement::Method settlementMethod = Settlement::PhysicalOTC);

    Settlement::Type settlementType() const;
    Settlement::Method settlementMethod() const;
    Swap::Type type() const;
    const ext::shared_ptr<NonstandardSwap>& underlyingSwap() const;
    std::vector<ext::shared_ptr<BlackCalibrationHelper>> calibrationBasket(
        const ext::shared_ptr<SwapIndex>& standardSwapBase,
        const ext::shared_ptr<SwaptionVolatilityStructure>& swaptionVolatility,
        BasketGeneratingEngine::CalibrationBasketType basketType = BasketGeneratingEngine::MaturityStrikeByDeltaGamma) const;

    %extend {
        std::vector<Real> probabilities() {
            return self->result<std::vector<Real>>("probabilities");
        }
    }
};



#endif
