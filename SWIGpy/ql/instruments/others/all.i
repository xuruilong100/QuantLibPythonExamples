#ifndef ql_instruments_others_all_i
#define ql_instruments_others_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::BasketGeneratingEngine;
using QuantLib::Claim;
using QuantLib::FaceValueClaim;
using QuantLib::FaceValueAccrualClaim;
using QuantLib::CompositeInstrument;
using QuantLib::CreditDefaultSwap;
using QuantLib::Stock;
using QuantLib::FloatFloatSwaption;
using QuantLib::NonstandardSwaption;
using QuantLib::Swaption;
%}

%pythoncode %{
class BasketGeneratingEngine(object):
    class CalibrationBasketType(object):
        Naive = 'Naive'
        MaturityStrikeByDeltaGamma = 'MaturityStrikeByDeltaGamma'
%}

%shared_ptr(Claim);
class Claim {
  private:
    Claim();
  public:
    Real amount(
        const Date& defaultDate,
        Real notional,
        Real recoveryRate) const;
};

%shared_ptr(FaceValueClaim)
class FaceValueClaim : public Claim {
  public:
    FaceValueClaim();
};

%shared_ptr(FaceValueAccrualClaim)
class FaceValueAccrualClaim : public Claim {
  public:
    FaceValueAccrualClaim(
        const ext::shared_ptr<Bond>& bond);
};

%shared_ptr(CompositeInstrument)
class CompositeInstrument : public Instrument {
  public:
    CompositeInstrument();
    void add(const ext::shared_ptr<Instrument>& instrument,
             Real multiplier = 1.0);
    void subtract(const ext::shared_ptr<Instrument>& instrument,
                  Real multiplier = 1.0);
};

%shared_ptr(CreditDefaultSwap)
class CreditDefaultSwap : public Instrument {
  public:
    enum PricingModel {
        Midpoint,
        ISDA
    };

    CreditDefaultSwap(
        Protection::Side side,
        Real notional,
        Rate spread,
        const Schedule& schedule,
        BusinessDayConvention paymentConvention,
        const DayCounter& dayCounter,
        bool settlesAccrual = true,
        bool paysAtDefaultTime = true,
        const Date& protectionStart = Date());
    CreditDefaultSwap(
        Protection::Side side,
        Real notional,
        Rate upfront,
        Rate spread,
        const Schedule& schedule,
        BusinessDayConvention paymentConvention,
        const DayCounter& dayCounter,
        bool settlesAccrual = true,
        bool paysAtDefaultTime = true,
        const Date& protectionStart = Date(),
        const Date& upfrontDate = Date(),
        const ext::shared_ptr<Claim>& claim = ext::shared_ptr<Claim>(),
        const DayCounter& lastPeriodDayCounter = DayCounter(),
        const bool rebatesAccrual = true);
    Protection::Side side() const;
    Real notional() const;
    Rate runningSpread() const;
    %extend {
        doubleOrNull upfront() const {
            boost::optional<Rate> result =
                self->upfront();
            if (result)
                return *result;
            else
                return Null<double>();
        }
    }
    bool settlesAccrual() const;
    bool paysAtDefaultTime() const;
    Rate fairSpread() const;
    Rate fairUpfront() const;
    Real couponLegBPS() const;
    Real couponLegNPV() const;
    Real defaultLegNPV() const;
    Real upfrontBPS() const;
    Real upfrontNPV() const;
    Rate impliedHazardRate(
        Real targetNPV,
        const Handle<YieldTermStructure>& discountCurve,
        const DayCounter& dayCounter,
        Real recoveryRate = 0.4,
        Real accuracy = 1.0e-6,
        CreditDefaultSwap::PricingModel model = CreditDefaultSwap::Midpoint) const;
    Rate conventionalSpread(
        Real conventionalRecovery,
        const Handle<YieldTermStructure>& discountCurve,
        const DayCounter& dayCounter) const;
    std::vector<ext::shared_ptr<CashFlow>> coupons();
};

%shared_ptr(Stock)
class Stock : public Instrument {
  public:
    Stock(const Handle<Quote>& quote);
};

%shared_ptr(FloatFloatSwaption)
class FloatFloatSwaption : public Instrument {
  public:
    FloatFloatSwaption(
        const ext::shared_ptr<FloatFloatSwap>& swap,
        const ext::shared_ptr<Exercise>& exercise,
        Settlement::Type delivery = Settlement::Physical,
        Settlement::Method settlementMethod = Settlement::PhysicalOTC);

    bool isExpired() const;
    Settlement::Type settlementType() const;
    Settlement::Method settlementMethod() const;
    VanillaSwap::Type type() const;
    const ext::shared_ptr<FloatFloatSwap>& underlyingSwap() const;

    %extend {
        std::vector<ext::shared_ptr<BlackCalibrationHelper>> calibrationBasket(
            ext::shared_ptr<SwapIndex> swapIndex,
            ext::shared_ptr<SwaptionVolatilityStructure> swaptionVolatility,
            std::string typeStr) const {

            BasketGeneratingEngine::CalibrationBasketType type;
            if (typeStr == "Naive")
                type = BasketGeneratingEngine::Naive;
            else if (typeStr == "MaturityStrikeByDeltaGamma")
                type = BasketGeneratingEngine::MaturityStrikeByDeltaGamma;
            else
                QL_FAIL("type " << typeStr << "unknown.");

            std::vector<ext::shared_ptr<BlackCalibrationHelper>> hs = self->calibrationBasket(
                swapIndex, swaptionVolatility, type);
            std::vector<ext::shared_ptr<BlackCalibrationHelper>> helpers(hs.size());
            for (Size i = 0; i < hs.size(); ++i)
                helpers[i] = hs[i];
            return helpers;
        }

        Real underlyingValue() {
            return self->result<Real>("underlyingValue");
        }

        std::vector<Real> probabilities() {
            return self->result<std::vector<Real>>("probabilities");
        }
    }
};

%shared_ptr(NonstandardSwaption)
class NonstandardSwaption : public Instrument {
  public:
    NonstandardSwaption(
        const ext::shared_ptr<NonstandardSwap>& swap,
        const ext::shared_ptr<Exercise>& exercise,
        Settlement::Type type = Settlement::Physical,
        Settlement::Method settlementMethod = Settlement::PhysicalOTC);

    const ext::shared_ptr<NonstandardSwap>& underlyingSwap() const;

    %extend {
        std::vector<ext::shared_ptr<BlackCalibrationHelper>> calibrationBasket(
            ext::shared_ptr<SwapIndex> swapIndex,
            ext::shared_ptr<SwaptionVolatilityStructure> swaptionVolatility,
            std::string typeStr) const {

            BasketGeneratingEngine::CalibrationBasketType type;
            if (typeStr == "Naive")
                type = BasketGeneratingEngine::Naive;
            else if (typeStr == "MaturityStrikeByDeltaGamma")
                type = BasketGeneratingEngine::MaturityStrikeByDeltaGamma;
            else
                QL_FAIL("type " << typeStr << "unknown.");

            std::vector<ext::shared_ptr<BlackCalibrationHelper>> hs = self->calibrationBasket(
                swapIndex, swaptionVolatility, type);
            std::vector<ext::shared_ptr<BlackCalibrationHelper>> helpers(hs.size());
            for (Size i = 0; i < hs.size(); ++i)
                helpers[i] = hs[i];
            return helpers;
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
        const ext::shared_ptr<VanillaSwap>& swap,
        const ext::shared_ptr<Exercise>& exercise,
        Settlement::Type type = Settlement::Physical,
        Settlement::Method settlementMethod = Settlement::PhysicalOTC);

    Settlement::Type settlementType() const;
    Settlement::Method settlementMethod() const;
    VanillaSwap::Type type() const;
    const ext::shared_ptr<VanillaSwap>& underlyingSwap() const;

    //! implied volatility
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

#endif
