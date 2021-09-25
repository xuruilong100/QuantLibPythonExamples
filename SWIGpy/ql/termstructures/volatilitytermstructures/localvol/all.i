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

%shared_ptr(LocalConstantVol);
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

%shared_ptr(LocalVolSurface);
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

%shared_ptr(NoExceptLocalVolSurface);
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
            Matrix& localVolMatrix,
            const DayCounter& dayCounter,
            Extrapolation lowerExtrapolation = ConstantExtrapolation,
            Extrapolation upperExtrapolation = ConstantExtrapolation) {
                ext::shared_ptr<Matrix> ptr(&localVolMatrix);
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
            Matrix& localVolMatrix,
            const DayCounter& dayCounter,
            Extrapolation lowerExtrapolation = ConstantExtrapolation,
            Extrapolation upperExtrapolation = ConstantExtrapolation) {
                ext::shared_ptr<Matrix> ptr(&localVolMatrix);
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
            std::vector<std::vector<Real> >& strikes,
            Matrix& localVolMatrix,
            const DayCounter& dayCounter,
            Extrapolation lowerExtrapolation = ConstantExtrapolation,
            Extrapolation upperExtrapolation = ConstantExtrapolation) {
                ext::shared_ptr<Matrix> ptr(&localVolMatrix);
                std::vector<ext::shared_ptr<std::vector<Real> > > table;
                for (Size i = 0; i < strikes.size(); ++i) {
                    table.push_back(
                        ext::shared_ptr<std::vector<Real>>(
                            &(strikes[i])));
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
        const std::vector<ext::shared_ptr<std::vector<Real> > >& strikes,
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
namespace {
    Date time2Date(
        const Date referenceDate,
        const DayCounter& dc,
        Time t) {
        t -= 1e4*QL_EPSILON; // add a small buffer for rounding errors
        Date d(referenceDate);
        while (dc.yearFraction(referenceDate, d+=Period(1, Years)) < t);
        d -= Period(1, Years);
        while (dc.yearFraction(referenceDate, d+=Period(1, Months)) < t);
        d -= Period(1, Months);
        while (dc.yearFraction(referenceDate, d++) < t);
        return d;
    }
    std::vector<ext::shared_ptr<std::vector<Real>>> vector2Ptr(
        std::vector<std::vector<Real>>& v) {
            std::vector<ext::shared_ptr<std::vector<Real>>> ptr;
            for (Size i = 0; i < v.size(); ++i) {
                ptr.push_back(
                    ext::shared_ptr<std::vector<Real>>(
                        &(v[i])));
            }

            return ptr;
        }
}

class SafeFixedLocalVolSurface : public LocalVolTermStructure {
  public:
    typedef FixedLocalVolSurface::Extrapolation Extrapolation;
    SafeFixedLocalVolSurface(
        const Date& referenceDate,
        const std::vector<Date>& dates,
        const std::vector<Real>& strikes,
        const Matrix& localVolMatrix,
        const DayCounter& dayCounter,
        Extrapolation lowerExtrapolation = FixedLocalVolSurface::ConstantExtrapolation,
        Extrapolation upperExtrapolation = FixedLocalVolSurface::ConstantExtrapolation) :
        LocalVolTermStructure(
            referenceDate, NullCalendar(), Following, dayCounter),
        maxDate_(dates.back()),
        safeLocalVolMatrix_(localVolMatrix),
        safeStrikes_(dates.size(), strikes),
        localVolInterpol_(dates.size()),
        lowerExtrapolation_(lowerExtrapolation),
        upperExtrapolation_(upperExtrapolation),
        surface_(
            referenceDate,
            dates,
            safeStrikes_.front(),
            ext::shared_ptr<Matrix>(&safeLocalVolMatrix_),
            dayCounter,
            lowerExtrapolation_,
            upperExtrapolation_) { }
    SafeFixedLocalVolSurface(
        const Date& referenceDate,
        const std::vector<Time>& times,
        const std::vector<Real>& strikes,
        const Matrix& localVolMatrix,
        const DayCounter& dayCounter,
        Extrapolation lowerExtrapolation = FixedLocalVolSurface::ConstantExtrapolation,
        Extrapolation upperExtrapolation = FixedLocalVolSurface::ConstantExtrapolation) :
        LocalVolTermStructure(
            referenceDate, NullCalendar(), Following, dayCounter),
        maxDate_(time2Date(referenceDate, dayCounter, times.back())),
        times_(times),
        safeLocalVolMatrix_(localVolMatrix),
        safeStrikes_(times.size(), strikes),
        localVolInterpol_(times.size()),
        lowerExtrapolation_(lowerExtrapolation),
        upperExtrapolation_(upperExtrapolation),
        surface_(
            referenceDate,
            times_,
            safeStrikes_.front(),
            ext::shared_ptr<Matrix>(&safeLocalVolMatrix_),
            dayCounter,
            lowerExtrapolation_,
            upperExtrapolation_) { }
    SafeFixedLocalVolSurface(
        const Date& referenceDate,
        const std::vector<Time>& times,
        const std::vector<std::vector<Real>>& strikes,
        const Matrix& localVolMatrix,
        const DayCounter& dayCounter,
        Extrapolation lowerExtrapolation = FixedLocalVolSurface::ConstantExtrapolation,
        Extrapolation upperExtrapolation = FixedLocalVolSurface::ConstantExtrapolation) :
        LocalVolTermStructure(
            referenceDate, NullCalendar(), Following, dayCounter),
        maxDate_(time2Date(referenceDate, dayCounter, times.back())),
        times_(times),
        safeLocalVolMatrix_(localVolMatrix),
        safeStrikes_(strikes),
        localVolInterpol_(times.size()),
        lowerExtrapolation_(lowerExtrapolation),
        upperExtrapolation_(upperExtrapolation),
        surface_(
            referenceDate,
            times_,
            vector2Ptr(safeStrikes_),
            ext::shared_ptr<Matrix>(&safeLocalVolMatrix_),
            dayCounter,
            lowerExtrapolation_,
            upperExtrapolation_) { }

    Date maxDate() const override {
        return surface_.maxDate();
    }
    Time maxTime() const override {
        return surface_.maxTime();
    }
    Real minStrike() const override {
        return surface_.minStrike();
    }
    Real maxStrike() const override {
        return surface_.maxStrike();
    }
    template <class Interpolator>
    void setInterpolation(const Interpolator& i = Interpolator()) {
        surface_.setInterpolation(i);
        notifyObservers();
    }

  protected:
    Volatility localVolImpl(Time t, Real strike) const override {
        return surface_.localVol(t, strike, true);
    }
  private:
    Date maxDate_;
    std::vector<Time> times_;
    Matrix safeLocalVolMatrix_;
    std::vector<std::vector<Real>> safeStrikes_;

    std::vector<Interpolation> localVolInterpol_;
    Extrapolation lowerExtrapolation_, upperExtrapolation_;

    FixedLocalVolSurface surface_;
};
%}

%shared_ptr(SafeFixedLocalVolSurface)
class SafeFixedLocalVolSurface : public LocalVolTermStructure {
  public:
    typedef FixedLocalVolSurface::Extrapolation Extrapolation;
    SafeFixedLocalVolSurface(
        const Date& referenceDate,
        const std::vector<Date>& dates,
        const std::vector<Real>& strikes,
        const Matrix& localVolMatrix,
        const DayCounter& dayCounter,
        Extrapolation lowerExtrapolation = FixedLocalVolSurface::ConstantExtrapolation,
        Extrapolation upperExtrapolation = FixedLocalVolSurface::ConstantExtrapolation);
    SafeFixedLocalVolSurface(
        const Date& referenceDate,
        const std::vector<Time>& times,
        const std::vector<Real>& strikes,
        const Matrix& localVolMatrix,
        const DayCounter& dayCounter,
        Extrapolation lowerExtrapolation = FixedLocalVolSurface::ConstantExtrapolation,
        Extrapolation upperExtrapolation = FixedLocalVolSurface::ConstantExtrapolation);
    SafeFixedLocalVolSurface(
        const Date& referenceDate,
        const std::vector<Time>& times,
        const std::vector<std::vector<Real>>& strikes,
        const Matrix& localVolMatrix,
        const DayCounter& dayCounter,
        Extrapolation lowerExtrapolation = FixedLocalVolSurface::ConstantExtrapolation,
        Extrapolation upperExtrapolation = FixedLocalVolSurface::ConstantExtrapolation);

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

#endif
