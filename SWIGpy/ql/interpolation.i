#ifndef ql_interpolation_i
#define ql_interpolation_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
// safe versions which copy their arguments
template <class I>
class SafeInterpolation {
  public:
    SafeInterpolation(
        const Array& x, const Array& y)
        : x_(x), y_(y),
          f_(x_.begin(), x_.end(), y_.begin()) {}
    Real operator()(
        Real x, bool allowExtrapolation = false) {
        return f_(x, allowExtrapolation);
    }
    Array x_, y_;
    I f_;
};
%}

%define make_safe_interpolation(T,Alias)
%{
typedef SafeInterpolation<QuantLib::T> Safe##T;
%}
//%rename(Alias) Safe##T;
class Safe##T {
  public:
    Safe##T(
        const Array& x, const Array& y);
    Real operator()(
        Real x, bool allowExtrapolation=false);
};
%enddef

make_safe_interpolation(BackwardFlatInterpolation, BackwardFlatInterpolation);
make_safe_interpolation(CubicNaturalSpline, CubicNaturalSpline);
make_safe_interpolation(ForwardFlatInterpolation, ForwardFlatInterpolation);
make_safe_interpolation(FritschButlandCubic, FritschButlandCubic);
make_safe_interpolation(FritschButlandLogCubic, FritschButlandLogCubic);
make_safe_interpolation(KrugerCubic, KrugerCubic);
make_safe_interpolation(KrugerLogCubic, KrugerLogCubic);
make_safe_interpolation(LinearInterpolation, LinearInterpolation);
make_safe_interpolation(LogCubicNaturalSpline, LogCubicNaturalSpline);
make_safe_interpolation(LogLinearInterpolation, LogLinearInterpolation);
make_safe_interpolation(LogParabolic, LogParabolic);
make_safe_interpolation(MonotonicCubicNaturalSpline, MonotonicCubicNaturalSpline);
make_safe_interpolation(MonotonicLogCubicNaturalSpline, MonotonicLogCubicNaturalSpline);
make_safe_interpolation(MonotonicLogParabolic, MonotonicLogParabolic);
make_safe_interpolation(MonotonicParabolic, MonotonicParabolic);
make_safe_interpolation(Parabolic, Parabolic);

%define extend_spline(T)
%extend Safe##T {
    Real derivative(
        Real x, bool extrapolate = false) {
        return self->f_.derivative(x, extrapolate);
    }
    Real secondDerivative(
        Real x, bool extrapolate = false) {
        return self->f_.secondDerivative(
            x, extrapolate);
    }
    Real primitive(
        Real x, bool extrapolate = false) {
        return self->f_.primitive(x, extrapolate);
    }
}
%enddef

extend_spline(CubicNaturalSpline);
extend_spline(FritschButlandCubic);
extend_spline(FritschButlandLogCubic);
extend_spline(KrugerCubic);
extend_spline(KrugerLogCubic);
extend_spline(LogCubicNaturalSpline);
extend_spline(LogParabolic);
extend_spline(MonotonicCubicNaturalSpline);
extend_spline(MonotonicLogCubicNaturalSpline);
extend_spline(MonotonicLogParabolic);
extend_spline(MonotonicParabolic);
extend_spline(Parabolic);

%{
// safe versions which copy their arguments
template <class I>
class SafeInterpolation2D {
  public:
    SafeInterpolation2D(
        const Array& x,
        const Array& y,
        const Matrix& m)
        : x_(x), y_(y), m_(m),
          f_(x_.begin(), x_.end(),
             y_.begin(), y_.end(), m_) {}
    Real operator()(
        Real x, Real y,
        bool allowExtrapolation = false) {
        return f_(x, y, allowExtrapolation);
    }

  protected:
    Array x_, y_;
    Matrix m_;
    I f_;
};
%}

%define make_safe_interpolation2d(T,Alias)
%{
typedef SafeInterpolation2D<QuantLib::T> Safe##T;
%}
//%rename(Alias) Safe##T;
class Safe##T {
  public:
    Safe##T(
        const Array& x,
        const Array& y,
        const Matrix& m);
    Real operator()(
        Real x, Real y,
        bool allowExtrapolation = false);
};
%enddef

make_safe_interpolation2d(BicubicSpline, BicubicSpline);
make_safe_interpolation2d(BilinearInterpolation, BilinearInterpolation);

%{
// safe version which copies its arguments
class SafeSABRInterpolation {
  public:
    SafeSABRInterpolation(
        const Array& x, const Array& y,
        Time t,
        Real forward,
        Real alpha,
        Real beta,
        Real nu,
        Real rho,
        bool alphaIsFixed,
        bool betaIsFixed,
        bool nuIsFixed,
        bool rhoIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod>& optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const Real shift = 0.0)
        : x_(x), y_(y), forward_(forward),
          f_(x_.begin(), x_.end(), y_.begin(),
             t, forward_, alpha, beta, nu, rho,
             alphaIsFixed, betaIsFixed,
             nuIsFixed, rhoIsFixed,
             vegaWeighted, endCriteria, optMethod,
             errorAccept, useMaxError, maxGuesses, shift) { f_.update(); }
    Real operator()(
        Real x, bool allowExtrapolation = false) const {
        return f_(x, allowExtrapolation);
    }
    Real alpha() const { return f_.alpha(); }
    Real beta() const { return f_.beta(); }
    Real rho() const { return f_.rho(); }
    Real nu() const { return f_.nu(); }

  private:
    Array x_, y_;     // passed via iterators, need to stay alive
    Real forward_;    // passed by reference, same
    QuantLib::SABRInterpolation f_;
};
%}

//%rename(SABRInterpolation) SafeSABRInterpolation;
class SafeSABRInterpolation {
  public:
    SafeSABRInterpolation(
        const Array& x, const Array& y,
        Time t,
        Real forward,
        Real alpha,
        Real beta,
        Real nu,
        Real rho,
        bool alphaIsFixed,
        bool betaIsFixed,
        bool nuIsFixed,
        bool rhoIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod>& optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const Real shift = 0.0);
    Real operator()(
        Real x, bool allowExtrapolation = false) const;
    Real alpha() const;
    Real beta() const;
    Real rho() const;
    Real nu() const;
};

%{
using QuantLib::RichardsonExtrapolation;
%}

class RichardsonExtrapolation {
  public:
    Real operator()(Real t=2.0) const;
    Real operator()(Real t, Real s) const;

    %extend {
        RichardsonExtrapolation(
            PyObject* fct,
            Real delta_h,
            Real n = Null<Real>()) {
            UnaryFunction f(fct);
            return new RichardsonExtrapolation(
                f, delta_h, n);
        }
    }
};


%{
class SafeConvexMonotoneInterpolation {
  public:
    SafeConvexMonotoneInterpolation(
        const Array& x, const Array& y,
        Real quadraticity = 0.3,
        Real monotonicity = 0.7,
        bool forcePositive = true)
        : x_(x), y_(y),
          f_(x_.begin(), x_.end(), y_.begin(),
             quadraticity, monotonicity, forcePositive) {}
    Real operator()(
        Real x, bool allowExtrapolation = false) {
        return f_(x, allowExtrapolation);
    }
    Array x_, y_;
    QuantLib::ConvexMonotoneInterpolation<Array::const_iterator, Array::const_iterator> f_;
};
%}

//%rename(ConvexMonotoneInterpolation) SafeConvexMonotoneInterpolation;
class SafeConvexMonotoneInterpolation {
  public:
    SafeConvexMonotoneInterpolation(
        const Array& x, const Array& y,
        Real quadraticity = 0.3,
        Real monotonicity = 0.7,
        bool forcePositive = true);
    Real operator()(
        Real x, bool allowExtrapolation = false);
};

#endif
