#ifndef ql_calibration_helpers_i
#define ql_calibration_helpers_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CalibrationHelper;
using QuantLib::BlackCalibrationHelper;
using QuantLib::SwaptionHelper;
using QuantLib::CapHelper;
using QuantLib::HestonModelHelper;
%}

%shared_ptr(CalibrationHelper)
class CalibrationHelper {
  private:
    CalibrationHelper();
  public:
    Real calibrationError();
};

%shared_ptr(BlackCalibrationHelper)
class BlackCalibrationHelper : public CalibrationHelper {
  private:
    BlackCalibrationHelper();
  public:
    enum CalibrationErrorType {
        RelativePriceError,
        PriceError,
        ImpliedVolError };

    Handle<Quote> volatility() const;
    VolatilityType volatilityType() const;
    Real marketValue() const;
    Real modelValue() const;
    Real calibrationError();
    Volatility impliedVolatility(
        Real targetValue,
        Real accuracy,
        Size maxEvaluations,
        Volatility minVol,
        Volatility maxVol);
    Real blackPrice(Volatility volatility) const;
    void setPricingEngine(
        const ext::shared_ptr<PricingEngine>& engine);
    %extend {
        std::vector<Time> times() {
            std::list<Time> l;
            self->addTimesTo(l);
            std::vector<Time> v;
            std::copy(l.begin(), l.end(), std::back_inserter(v));
            return v;
        }
    }
};

%inline %{
    ext::shared_ptr<BlackCalibrationHelper> as_black_helper(
        const ext::shared_ptr<CalibrationHelper>& h) {
        return ext::dynamic_pointer_cast<BlackCalibrationHelper>(h);
    }
    ext::shared_ptr<SwaptionHelper> as_swaption_helper(
        const ext::shared_ptr<BlackCalibrationHelper>& h) {
        return ext::dynamic_pointer_cast<SwaptionHelper>(h);
    }
%}

%template(CalibrationHelperVector) std::vector<ext::shared_ptr<CalibrationHelper> >;
%template(BlackCalibrationHelperVector) std::vector<ext::shared_ptr<BlackCalibrationHelper> >;

%shared_ptr(CapHelper)
class CapHelper : public BlackCalibrationHelper {
  public:
    CapHelper(
        const Period& length,
        const Handle<Quote>& volatility,
        const ext::shared_ptr<IborIndex>& index,
        Frequency fixedLegFrequency,
        const DayCounter& fixedLegDayCounter,
        bool includeFirstSwaplet,
        const Handle<YieldTermStructure>& termStructure,
        BlackCalibrationHelper::CalibrationErrorType errorType = BlackCalibrationHelper::RelativePriceError,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
};

%shared_ptr(HestonModelHelper)
class HestonModelHelper : public BlackCalibrationHelper {
  public:
    HestonModelHelper(
        const Period& maturity,
        const Calendar& calendar,
        const Real s0,
        const Real strikePrice,
        const Handle<Quote>& volatility,
        const Handle<YieldTermStructure>& riskFreeRate,
        const Handle<YieldTermStructure>& dividendYield,
        BlackCalibrationHelper::CalibrationErrorType errorType = BlackCalibrationHelper::RelativePriceError);
    HestonModelHelper(
        const Period& maturity,
        const Calendar& calendar,
        const Handle<Quote>& s0,
        Real strikePrice,
        const Handle<Quote>& volatility,
        const Handle<YieldTermStructure>& riskFreeRate,
        const Handle<YieldTermStructure>& dividendYield,
        BlackCalibrationHelper::CalibrationErrorType errorType = BlackCalibrationHelper::RelativePriceError);
    Time maturity() const;
};

%shared_ptr(SwaptionHelper)
class SwaptionHelper : public BlackCalibrationHelper {
  public:
    SwaptionHelper(
        const Period& maturity, const Period& length,
        const Handle<Quote>& volatility,
        const ext::shared_ptr<IborIndex>& index,
        const Period& fixedLegTenor,
        const DayCounter& fixedLegDayCounter,
        const DayCounter& floatingLegDayCounter,
        const Handle<YieldTermStructure>& termStructure,
        BlackCalibrationHelper::CalibrationErrorType errorType = BlackCalibrationHelper::RelativePriceError,
        const Real strike = Null<Real>(),
        const Real nominal = 1.0,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    SwaptionHelper(
        const Date& exerciseDate, const Period& length,
        const Handle<Quote>& volatility,
        const ext::shared_ptr<IborIndex>& index,
        const Period& fixedLegTenor,
        const DayCounter& fixedLegDayCounter,
        const DayCounter& floatingLegDayCounter,
        const Handle<YieldTermStructure>& termStructure,
        BlackCalibrationHelper::CalibrationErrorType errorType = BlackCalibrationHelper::RelativePriceError,
        const Real strike = Null<Real>(),
        const Real nominal = 1.0,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    SwaptionHelper(
        const Date& exerciseDate, const Date& endDate,
        const Handle<Quote>& volatility,
        const ext::shared_ptr<IborIndex>& index,
        const Period& fixedLegTenor,
        const DayCounter& fixedLegDayCounter,
        const DayCounter& floatingLegDayCounter,
        const Handle<YieldTermStructure>& termStructure,
        BlackCalibrationHelper::CalibrationErrorType errorType = BlackCalibrationHelper::RelativePriceError,
        const Real strike = Null<Real>(),
        const Real nominal = 1.0,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);

    ext::shared_ptr<VanillaSwap> underlyingSwap() const;
    ext::shared_ptr<Swaption> swaption() const;

    %extend {
        Date swaptionExpiryDate() {
            return self->swaption()->exercise()->date(0);
        }
        Real swaptionStrike() {
            return self->swaption()->underlyingSwap()->fixedRate();
        }
        Real swaptionNominal() {
            return self->swaption()->underlyingSwap()->nominal();
        }
        Date swaptionMaturityDate() {
            return self->swaption()->underlyingSwap()->fixedSchedule().dates().back();
        }
    }
};

#endif
