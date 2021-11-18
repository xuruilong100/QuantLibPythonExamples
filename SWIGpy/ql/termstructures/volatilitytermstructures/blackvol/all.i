#ifndef ql_termstructures_volatilitytermstructures_blackvol_all_i
#define ql_termstructures_volatilitytermstructures_blackvol_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/volatilitytermstructures/BlackVolTermStructure.i

%{
using QuantLib::BlackVolatilityTermStructure;
using QuantLib::BlackVarianceTermStructure;
using QuantLib::HestonBlackVolSurface;
%}

%{
using QuantLib::BlackConstantVol;
using QuantLib::AndreasenHugeVolatilityAdapter;
using QuantLib::BlackVarianceCurve;
using QuantLib::BlackVarianceSurface;
using QuantLib::ExtendedBlackVarianceCurve;
using QuantLib::ExtendedBlackVarianceSurface;
%}

%shared_ptr(BlackVolatilityTermStructure)
class BlackVolatilityTermStructure : public BlackVolTermStructure {
  private:
    BlackVolatilityTermStructure();
};

%shared_ptr(BlackVarianceTermStructure)
class BlackVarianceTermStructure : public BlackVolTermStructure {
  private:
    BlackVarianceTermStructure();
};

%shared_ptr(HestonBlackVolSurface)
class HestonBlackVolSurface : public BlackVolTermStructure {
  public:
    HestonBlackVolSurface(
        const Handle<HestonModel>& hestonModel,
        const AnalyticHestonEngine::ComplexLogFormula cpxLogFormula = AnalyticHestonEngine::Gatheral,
        const AnalyticHestonEngine::Integration& integration = AnalyticHestonEngine::Integration::gaussLaguerre(164));
};

%shared_ptr(BlackConstantVol)
class BlackConstantVol : public BlackVolatilityTermStructure {
  public:
    BlackConstantVol(
        const Date& referenceDate,
        const Calendar& c,
        Volatility volatility,
        const DayCounter& dayCounter);
    BlackConstantVol(
        const Date& referenceDate,
        const Calendar& c,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter);
    BlackConstantVol(
        Natural settlementDays,
        const Calendar& calendar,
        Volatility volatility,
        const DayCounter& dayCounter);
    BlackConstantVol(
        Natural settlementDays,
        const Calendar& calendar,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter);
};

%shared_ptr(AndreasenHugeVolatilityAdapter)
class AndreasenHugeVolatilityAdapter : public BlackVolTermStructure {
  public:
    AndreasenHugeVolatilityAdapter(
        ext::shared_ptr<AndreasenHugeVolatilityInterpl> volInterpl,
        Real eps = 1e-6);
};

%shared_ptr(BlackVarianceCurve)
class BlackVarianceCurve : public BlackVolTermStructure {
  public:
    BlackVarianceCurve(
        const Date& referenceDate,
        const std::vector<Date>& dates,
        const std::vector<Real>& volatilities,
        const DayCounter& dayCounter,
        bool forceMonotoneVariance = true);
    %extend {
        %define DefineSetInterpolation(Interpolator)
        void setInterpolation ## Interpolator(
            const Interpolator& i = Interpolator()) {
            self->setInterpolation<Interpolator>(i);
        }
        %enddef

        // See traits/all.i for interpolator definitions.
        DefineSetInterpolation(LinearFlat);
        DefineSetInterpolation(BackwardFlat);
        DefineSetInterpolation(ConvexMonotone);
        DefineSetInterpolation(Cubic);
        DefineSetInterpolation(ForwardFlat);
        DefineSetInterpolation(Linear);
        DefineSetInterpolation(LogLinear);
        //DefineSetInterpolation(LogCubic);
        //DefineSetInterpolation(LogMixedLinearCubic);
        //DefineSetInterpolation(MixedLinearCubic);
        DefineSetInterpolation(DefaultLogCubic);
        DefineSetInterpolation(MonotonicLogCubic);
        DefineSetInterpolation(KrugerLog);
        //DefineSetInterpolation(SABR);
        //DefineSetInterpolation(Abcd);
    }
};

%shared_ptr(BlackVarianceSurface)
class BlackVarianceSurface : public BlackVolTermStructure {
    %feature("kwargs") BlackVarianceSurface;

  public:
    enum Extrapolation {
        ConstantExtrapolation,
        InterpolatorDefaultExtrapolation
    };
    BlackVarianceSurface(
        const Date& referenceDate,
        const Calendar& cal,
        const std::vector<Date>& dates,
        const std::vector<Real>& strikes,
        const Matrix& blackVols,
        const DayCounter& dayCounter,
        BlackVarianceSurface::Extrapolation lower =
            BlackVarianceSurface::InterpolatorDefaultExtrapolation,
        BlackVarianceSurface::Extrapolation upper =
            BlackVarianceSurface::InterpolatorDefaultExtrapolation);
    %extend {
        %define DefineSetInterpolation2D(Interpolator)
        void setInterpolation ## Interpolator(
            const Interpolator& i = Interpolator()) {
            self->setInterpolation<Interpolator>(i);
        }
        %enddef

        // See trait2ds/all.i for interpolator definitions.
        DefineSetInterpolation2D(Bicubic);
        DefineSetInterpolation2D(BackwardflatLinear);
        DefineSetInterpolation2D(Bilinear);
        DefineSetInterpolation2D(Polynomial);
    }
};

%shared_ptr(ExtendedBlackVarianceCurve)
class ExtendedBlackVarianceCurve : public BlackVarianceTermStructure {
  public:
    ExtendedBlackVarianceCurve(
        const Date& referenceDate,
        const std::vector<Date>& dates,
        std::vector<Handle<Quote>> volatilities,
        DayCounter dayCounter,
        bool forceMonotoneVariance = true);

    %extend {
        %define DefineSetInterpolation(Interpolator)
        void setInterpolation ## Interpolator(
            const Interpolator& i = Interpolator()) {
            self->setInterpolation<Interpolator>(i);
        }
        %enddef

        // See traits/all.i for interpolator definitions.
        DefineSetInterpolation(LinearFlat);
        DefineSetInterpolation(BackwardFlat);
        DefineSetInterpolation(ConvexMonotone);
        DefineSetInterpolation(Cubic);
        DefineSetInterpolation(ForwardFlat);
        DefineSetInterpolation(Linear);
        DefineSetInterpolation(LogLinear);
        //DefineSetInterpolation(LogCubic);
        //DefineSetInterpolation(LogMixedLinearCubic);
        //DefineSetInterpolation(MixedLinearCubic);
        DefineSetInterpolation(DefaultLogCubic);
        DefineSetInterpolation(MonotonicLogCubic);
        DefineSetInterpolation(KrugerLog);
        //DefineSetInterpolation(SABR);
        //DefineSetInterpolation(Abcd);
    }
};

%shared_ptr(ExtendedBlackVarianceSurface)
class ExtendedBlackVarianceSurface : public BlackVarianceTermStructure {
  public:
    enum Extrapolation {
        ConstantExtrapolation,
        InterpolatorDefaultExtrapolation
    };
    ExtendedBlackVarianceSurface(
        const Date& referenceDate,
        const Calendar& calendar,
        const std::vector<Date>& dates,
        std::vector<Real> strikes,
        const std::vector<Handle<Quote>>& volatilities,
        DayCounter dayCounter,
        Extrapolation lowerExtrapolation = InterpolatorDefaultExtrapolation,
        Extrapolation upperExtrapolation = InterpolatorDefaultExtrapolation);

    %extend {
        %define DefineSetInterpolation2D(Interpolator)
        void setInterpolation ## Interpolator(
            const Interpolator& i = Interpolator()) {
            self->setInterpolation<Interpolator>(i);
        }
        %enddef

        // See trait2ds/all.i for interpolator definitions.
        DefineSetInterpolation2D(Bicubic);
        DefineSetInterpolation2D(BackwardflatLinear);
        DefineSetInterpolation2D(Bilinear);
        DefineSetInterpolation2D(Polynomial);
    }
};

#endif
