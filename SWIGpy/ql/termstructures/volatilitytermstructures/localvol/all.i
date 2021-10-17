#ifndef ql_termstructures_volatilitytermstructures_localvol_all_i
#define ql_termstructures_volatilitytermstructures_localvol_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/volatilitytermstructures/LocalVolTermStructure.i

%{
using QuantLib::AndreasenHugeLocalVolAdapter;
using QuantLib::LocalConstantVol;
using QuantLib::LocalVolSurface;
using QuantLib::NoExceptLocalVolSurface;
using QuantLib::FixedLocalVolSurface;
using QuantLib::GridModelLocalVolSurface;
using QuantLib::LocalVolCurve;
%}

%shared_ptr(AndreasenHugeLocalVolAdapter)
class AndreasenHugeLocalVolAdapter : public LocalVolTermStructure {
  public:
    explicit AndreasenHugeLocalVolAdapter(
        ext::shared_ptr<AndreasenHugeVolatilityInterpl> localVol);
};

%shared_ptr(LocalConstantVol)
class LocalConstantVol : public LocalVolTermStructure {
  public:
    LocalConstantVol(
        const Date& referenceDate,
        Volatility volatility,
        const DayCounter& dayCounter);
    LocalConstantVol(
        const Date& referenceDate,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter);
    LocalConstantVol(
        Integer settlementDays,
        const Calendar& calendar,
        Volatility volatility,
        const DayCounter& dayCounter);
    LocalConstantVol(
        Integer settlementDays,
        const Calendar& calendar,
        const Handle<Quote>& volatility,
        const DayCounter& dayCounter);
};

%shared_ptr(LocalVolSurface)
class LocalVolSurface : public LocalVolTermStructure {
  public:
    LocalVolSurface(
        const Handle<BlackVolTermStructure>& blackTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<Quote>& underlying);
    LocalVolSurface(
        const Handle<BlackVolTermStructure>& blackTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        Real underlying);
};

%shared_ptr(NoExceptLocalVolSurface)
class NoExceptLocalVolSurface : public LocalVolSurface {
  public:
    NoExceptLocalVolSurface(
        const Handle<BlackVolTermStructure>& blackTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<Quote>& underlying,
        Real illegalLocalVolOverwrite);
    NoExceptLocalVolSurface(
        const Handle<BlackVolTermStructure>& blackTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        Real underlying,
        Real illegalLocalVolOverwrite);
};

%shared_ptr(FixedLocalVolSurface)
class FixedLocalVolSurface : public LocalVolTermStructure {
  public:
    enum Extrapolation {
        ConstantExtrapolation,
        InterpolatorDefaultExtrapolation
    };
    %extend {
        FixedLocalVolSurface(
            const Date& referenceDate,
            const std::vector<Date>& dates,
            const std::vector<Real>& strikes,
            const Matrix& localVolMatrix,
            const DayCounter& dayCounter,
            Extrapolation lowerExtrapolation = ConstantExtrapolation,
            Extrapolation upperExtrapolation = ConstantExtrapolation) {
                ext::shared_ptr<Matrix> ptr(new Matrix(localVolMatrix));
                return new FixedLocalVolSurface(
                    referenceDate,
                    dates,
                    strikes,
                    ptr,
                    dayCounter,
                    lowerExtrapolation,
                    upperExtrapolation);
            }
        FixedLocalVolSurface(
            const Date& referenceDate,
            const std::vector<Time>& times,
            const std::vector<Real>& strikes,
            const Matrix& localVolMatrix,
            const DayCounter& dayCounter,
            Extrapolation lowerExtrapolation = ConstantExtrapolation,
            Extrapolation upperExtrapolation = ConstantExtrapolation) {
                ext::shared_ptr<Matrix> ptr(new Matrix(localVolMatrix));
                return new FixedLocalVolSurface(
                    referenceDate,
                    times,
                    strikes,
                    ptr,
                    dayCounter,
                    lowerExtrapolation,
                    upperExtrapolation);
            }
        FixedLocalVolSurface(
            const Date& referenceDate,
            const std::vector<Time>& times,
            const std::vector<std::vector<Real>>& strikes,
            const Matrix& localVolMatrix,
            const DayCounter& dayCounter,
            Extrapolation lowerExtrapolation = ConstantExtrapolation,
            Extrapolation upperExtrapolation = ConstantExtrapolation) {
                ext::shared_ptr<Matrix> ptr(new Matrix(localVolMatrix));
                std::vector<ext::shared_ptr<std::vector<Real>>> table;
                for (Size i = 0; i < strikes.size(); ++i) {
                    table.push_back(
                        ext::shared_ptr<std::vector<Real>>(
                            new std::vector<Real>(strikes[i])));
                }
                return new FixedLocalVolSurface(
                    referenceDate,
                    times,
                    table,
                    ptr,
                    dayCounter,
                    lowerExtrapolation,
                    upperExtrapolation);
            }

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

%shared_ptr(GridModelLocalVolSurface)
class GridModelLocalVolSurface : public LocalVolTermStructure, public CalibratedModel {
  public:
    typedef FixedLocalVolSurface::Extrapolation Extrapolation;

    GridModelLocalVolSurface(
        const Date& referenceDate,
        const std::vector<Date>& dates,
        const std::vector<ext::shared_ptr<std::vector<Real>>>& strikes,
        const DayCounter& dayCounter,
        Extrapolation lowerExtrapolation
            = FixedLocalVolSurface::ConstantExtrapolation,
        Extrapolation upperExtrapolation
            = FixedLocalVolSurface::ConstantExtrapolation);
};

%shared_ptr(LocalVolCurve)
class LocalVolCurve : public LocalVolTermStructure {
  public:
    LocalVolCurve(const Handle<BlackVarianceCurve>& curve);
};

%{
class CustomicLocalVolatility : public LocalVolTermStructure {
  public:
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(bdc, dc),
        localVolImpl_(localVolImpl) {}
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(referenceDate, cal, bdc, dc),
        localVolImpl_(localVolImpl) {}
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(settlementDays, cal, bdc, dc),
        localVolImpl_(localVolImpl) {}

    Date maxDate() const override {return Date::maxDate(); }
    Real minStrike() const override { return 0.0; }
    Real maxStrike() const override { return std::numeric_limits<Real>::max(); }

  protected:
    Volatility localVolImpl(Time t, Real strike) const override {
        return localVolImpl_(t, strike);
    }
  private:
    BinaryFunction localVolImpl_;
};
%}

%shared_ptr(CustomicLocalVolatility)
class CustomicLocalVolatility : public LocalVolTermStructure {
  public:
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
    CustomicLocalVolatility(
        PyObject* localVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
};

#endif
