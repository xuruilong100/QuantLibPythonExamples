#ifndef ql_interpolation_safeinterpolation_all_i
#define ql_interpolation_safeinterpolation_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/SafeInterpolation.i

%{
using QuantLib::KernelFunction;
using QuantLib::GaussianKernel;
%}

class KernelFunction {
  private:
    KernelFunction();
  public:
    Real operator()(Real x) const;
};

class GaussianKernel : public KernelFunction {
  public:
    GaussianKernel(Real average, Real sigma);
    Real derivative(Real x) const;
    Real primitive(Real x) const;
};

%{
class SafeAbcdInterpolation : public SafeInterpolation {
  public:
    SafeAbcdInterpolation(
        const Array &x,
        const Array &y,
        Real a = -0.06,
        Real b = 0.17,
        Real c = 0.54,
        Real d = 0.17,
        bool aIsFixed = false,
        bool bIsFixed = false,
        bool cIsFixed = false,
        bool dIsFixed = false,
        bool vegaWeighted = false,
        const ext::shared_ptr<EndCriteria> &endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod = ext::shared_ptr<OptimizationMethod>()) :
        SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new AbcdInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                a, b, c, d,
                aIsFixed, bIsFixed, cIsFixed, dIsFixed,
                vegaWeighted, endCriteria, optMethod));
    }

    Real a() const { return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->a(); }
    Real b() const { return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->b(); }
    Real c() const { return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->c(); }
    Real d() const { return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->d(); }
    std::vector<Real> k() const { return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->k(); }
    Real rmsError() const { return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->rmsError(); }
    Real maxError() const { return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->maxError(); }
    EndCriteria::Type endCriteria() { return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->endCriteria(); }
    Real k(Time t, const Array &x) const {
        return ext::dynamic_pointer_cast<AbcdInterpolation>(i_)->k(t, x_.begin(), x_.end());
    }
};

class SafeBackwardFlatInterpolation : public SafeInterpolation {
  public:
    SafeBackwardFlatInterpolation(
        const Array &x, const Array &y) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new BackwardFlatInterpolation(
                x_.begin(), x_.end(), y_.begin()));
    }
};

class SafeForwardFlatInterpolation : public SafeInterpolation {
  public:
    SafeForwardFlatInterpolation(
        const Array &x, const Array &y) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new ForwardFlatInterpolation(
                x_.begin(), x_.end(), y_.begin()));
    }
};

class SafeLagrangeInterpolation : public SafeInterpolation {
  public:
    SafeLagrangeInterpolation(
        const Array &x, const Array &y) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new LagrangeInterpolation(
                x_.begin(), x_.end(), y_.begin()));
    }
    Real value(const Array &y, Real x) const {
        return ext::dynamic_pointer_cast<LagrangeInterpolation>(i_)->value(y, x);
    }
};

class SafeLinearFlatInterpolation : public SafeInterpolation {
  public:
    SafeLinearFlatInterpolation(
        const Array &x, const Array &y) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new LinearFlatInterpolation(
                x_.begin(), x_.end(), y_.begin()));
    }
};

class SafeLinearInterpolation : public SafeInterpolation {
  public:
    SafeLinearInterpolation(
        const Array &x, const Array &y) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new LinearInterpolation(
                x_.begin(), x_.end(), y_.begin()));
    }
};

class SafeLogLinearInterpolation : public SafeInterpolation {
  public:
    SafeLogLinearInterpolation(
        const Array &x, const Array &y) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new LogLinearInterpolation(
                x_.begin(), x_.end(), y_.begin()));
    }
};

class SafeNoArbSabrInterpolation : public SafeInterpolation {
  public:
    SafeNoArbSabrInterpolation(
        const Array &x,
        const Array &y,
        Time t,
        const Real &forward,
        Real alpha, Real beta, Real nu, Real rho,
        bool alphaIsFixed,
        bool betaIsFixed,
        bool nuIsFixed,
        bool rhoIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria> &endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const Real shift = 0.0) : SafeInterpolation(x, y), forward_(forward) {
        i_ = ext::shared_ptr<Interpolation>(
            new NoArbSabrInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                t,
                forward_,
                alpha, beta, nu, rho,
                alphaIsFixed,
                betaIsFixed,
                nuIsFixed,
                rhoIsFixed,
                vegaWeighted,
                endCriteria,
                optMethod,
                errorAccept,
                useMaxError,
                maxGuesses,
                shift));
    }

    Real expiry() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->expiry(); }
    Real forward() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->forward(); }
    Real alpha() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->alpha(); }
    Real beta() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->beta(); }
    Real nu() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->nu(); }
    Real rho() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->rho(); }
    Real rmsError() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->rmsError(); }
    Real maxError() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->maxError(); }
    const std::vector<Real> &interpolationWeights() const { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->interpolationWeights(); }
    EndCriteria::Type endCriteria() { return ext::dynamic_pointer_cast<NoArbSabrInterpolation>(i_)->endCriteria(); }
  private:
    Real forward_;
};

class SafeSABRInterpolation : public SafeInterpolation {
  public:
    SafeSABRInterpolation(
        const Array &x,
        const Array &y,
        Time t,
        const Real &forward,
        Real alpha, Real beta, Real nu, Real rho,
        bool alphaIsFixed,
        bool betaIsFixed,
        bool nuIsFixed,
        bool rhoIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria> &endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const Real shift = 0.0) : SafeInterpolation(x, y), forward_(forward) {
        i_ = ext::shared_ptr<Interpolation>(
            new SABRInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                t, forward_,
                alpha, beta, nu, rho,
                alphaIsFixed,
                betaIsFixed,
                nuIsFixed,
                rhoIsFixed,
                vegaWeighted,
                endCriteria,
                optMethod,
                errorAccept,
                useMaxError,
                maxGuesses,
                shift));
    }

    Real expiry() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->expiry(); }
    Real forward() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->forward(); }
    Real alpha() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->alpha(); }
    Real beta() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->beta(); }
    Real nu() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->nu(); }
    Real rho() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->rho(); }
    Real rmsError() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->rmsError(); }
    Real maxError() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->maxError(); }
    const std::vector<Real> &interpolationWeights() const { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->interpolationWeights(); }
    EndCriteria::Type endCriteria() { return ext::dynamic_pointer_cast<SABRInterpolation>(i_)->endCriteria(); }
  private:
    Real forward_;
};

class SafeSviInterpolation : public SafeInterpolation {
  public:
    SafeSviInterpolation(
        const Array &x,
        const Array &y,
        Time t,
        const Real &forward,
        Real a, Real b, Real sigma, Real rho, Real m,
        bool aIsFixed, bool bIsFixed, bool sigmaIsFixed,
        bool rhoIsFixed,
        bool mIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria> &endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50) : SafeInterpolation(x, y), forward_(forward) {
        i_ = ext::shared_ptr<Interpolation>(
            new SviInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                t, forward_,
                a, b, sigma, rho, m,
                aIsFixed, bIsFixed, sigmaIsFixed,
                rhoIsFixed, mIsFixed,
                vegaWeighted,
                endCriteria,
                optMethod,
                errorAccept,
                useMaxError,
                maxGuesses));
    }

    Real expiry() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->expiry(); }
    Real forward() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->forward(); }
    Real a() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->a(); }
    Real b() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->b(); }
    Real sigma() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->sigma(); }
    Real rho() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->rho(); }
    Real m() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->m(); }
    Real rmsError() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->rmsError(); }
    Real maxError() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->maxError(); }
    const std::vector<Real> &interpolationWeights() const { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->interpolationWeights(); }
    EndCriteria::Type endCriteria() { return ext::dynamic_pointer_cast<SviInterpolation>(i_)->endCriteria(); }
  private:
    Real forward_;
};

class SafeVannaVolgaInterpolation : public SafeInterpolation {
  public:
    SafeVannaVolgaInterpolation(
        const Array &x, const Array &y,
        Real spot,
        DiscountFactor dDiscount,
        DiscountFactor fDiscount,
        Time T) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new VannaVolgaInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                spot, dDiscount, fDiscount, T));
    }
};

class SafeCubicInterpolation : public SafeInterpolation {
  public:
    SafeCubicInterpolation(
        const Array &x, const Array &y,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic,
        CubicInterpolation::BoundaryCondition leftCond,
        Real leftConditionValue,
        CubicInterpolation::BoundaryCondition rightCond,
        Real rightConditionValue) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new CubicInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                da,
                monotonic,
                leftCond,
                leftConditionValue,
                rightCond,
                rightConditionValue));
    }

    const std::vector<Real> &primitiveConstants() const { return ext::dynamic_pointer_cast<CubicInterpolation>(i_)->primitiveConstants(); }
    const std::vector<Real> &aCoefficients() const { return ext::dynamic_pointer_cast<CubicInterpolation>(i_)->aCoefficients(); }
    const std::vector<Real> &bCoefficients() const { return ext::dynamic_pointer_cast<CubicInterpolation>(i_)->bCoefficients(); }
    const std::vector<Real> &cCoefficients() const { return ext::dynamic_pointer_cast<CubicInterpolation>(i_)->cCoefficients(); }
    const std::vector<bool> &monotonicityAdjustments() const { return ext::dynamic_pointer_cast<CubicInterpolation>(i_)->monotonicityAdjustments(); }
};

class SafeLogMixedLinearCubicInterpolation : public SafeInterpolation {
  public:
    SafeLogMixedLinearCubicInterpolation(
        const Array &x, const Array &y,
        const Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic,
        CubicInterpolation::BoundaryCondition leftC,
        Real leftConditionValue,
        CubicInterpolation::BoundaryCondition rightC,
        Real rightConditionValue) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new LogMixedLinearCubicInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                n,
                behavior,
                da,
                monotonic,
                leftC,
                leftConditionValue,
                rightC,
                rightConditionValue));
    }
};

class SafeLogCubicInterpolation : public SafeInterpolation {
  public:
    SafeLogCubicInterpolation(
        const Array &x, const Array &y,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic,
        CubicInterpolation::BoundaryCondition leftC,
        Real leftConditionValue,
        CubicInterpolation::BoundaryCondition rightC,
        Real rightConditionValue) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new LogCubicInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                da,
                monotonic,
                leftC,
                leftConditionValue,
                rightC,
                rightConditionValue));
    }
};

class SafeMixedLinearCubicInterpolation : public SafeInterpolation {
  public:
    SafeMixedLinearCubicInterpolation(
        const Array &x, const Array &y,
        const Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic,
        CubicInterpolation::BoundaryCondition leftC,
        Real leftConditionValue,
        CubicInterpolation::BoundaryCondition rightC,
        Real rightConditionValue) :
        SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new MixedLinearCubicInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                n,
                behavior,
                da,
                monotonic,
                leftC,
                leftConditionValue,
                rightC,
                rightConditionValue));
    }
};

class SafeAkimaCubicInterpolation : public SafeCubicInterpolation {
  public:
    SafeAkimaCubicInterpolation(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::Akima, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeCubicNaturalSpline : public SafeCubicInterpolation {
  public:
    SafeCubicNaturalSpline(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::Spline, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeCubicSplineOvershootingMinimization1 : public SafeCubicInterpolation {
  public:
    SafeCubicSplineOvershootingMinimization1(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::SplineOM1, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeCubicSplineOvershootingMinimization2 : public SafeCubicInterpolation {
  public:
    SafeCubicSplineOvershootingMinimization2(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::SplineOM2, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeFritschButlandCubic : public SafeCubicInterpolation {
  public:
    SafeFritschButlandCubic(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::FritschButland, true,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeHarmonicCubic : public SafeCubicInterpolation {
  public:
    SafeHarmonicCubic(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::Harmonic, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeKrugerCubic : public SafeCubicInterpolation {
  public:
    SafeKrugerCubic(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::Kruger, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeMonotonicCubicNaturalSpline : public SafeCubicInterpolation {
  public:
    SafeMonotonicCubicNaturalSpline(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::Spline, true,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeMonotonicParabolic : public SafeCubicInterpolation {
  public:
    SafeMonotonicParabolic(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::Parabolic, true,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeParabolic : public SafeCubicInterpolation {
  public:
    SafeParabolic(
        const Array &x, const Array &y) :
        SafeCubicInterpolation(
            x, y,
            CubicInterpolation::Parabolic, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeLogMixedLinearCubicNaturalSpline : public SafeLogMixedLinearCubicInterpolation {
  public:
    SafeLogMixedLinearCubicNaturalSpline(
        const Array &x, const Array &y,
        const Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) :
        SafeLogMixedLinearCubicInterpolation(
            x, y, n, behavior,
            CubicInterpolation::Spline, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) { }
};

class SafeFritschButlandLogCubic : public SafeLogCubicInterpolation {
  public:
    SafeFritschButlandLogCubic(
        const Array &x, const Array &y) :
        SafeLogCubicInterpolation(
            x, y,
            CubicInterpolation::FritschButland, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeHarmonicLogCubic : public SafeLogCubicInterpolation {
  public:
    SafeHarmonicLogCubic(
        const Array &x, const Array &y) :
        SafeLogCubicInterpolation(
            x, y,
            CubicInterpolation::Harmonic, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeKrugerLogCubic : public SafeLogCubicInterpolation {
  public:
    SafeKrugerLogCubic(
        const Array &x, const Array &y) :
        SafeLogCubicInterpolation(
            x, y,
            CubicInterpolation::Kruger, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeLogCubicNaturalSpline : public SafeLogCubicInterpolation {
  public:
    SafeLogCubicNaturalSpline(
        const Array &x, const Array &y) :
        SafeLogCubicInterpolation(
            x, y,
            CubicInterpolation::Spline, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeLogParabolic : public SafeLogCubicInterpolation {
  public:
    SafeLogParabolic(
        const Array &x, const Array &y) :
        SafeLogCubicInterpolation(
            x, y,
            CubicInterpolation::Parabolic, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeMonotonicLogCubicNaturalSpline : public SafeLogCubicInterpolation {
  public:
    SafeMonotonicLogCubicNaturalSpline(
        const Array &x, const Array &y) :
        SafeLogCubicInterpolation(
            x, y,
            CubicInterpolation::Spline, true,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeMonotonicLogParabolic : public SafeLogCubicInterpolation {
  public:
    SafeMonotonicLogParabolic(
        const Array &x, const Array &y) :
        SafeLogCubicInterpolation(
            x, y,
            CubicInterpolation::Parabolic, true,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeMixedLinearCubicNaturalSpline : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearCubicNaturalSpline(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) :
        SafeMixedLinearCubicInterpolation(
            x, y, n, behavior,
            CubicInterpolation::Spline, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeMixedLinearFritschButlandCubic : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearFritschButlandCubic(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) :
        SafeMixedLinearCubicInterpolation(
            x, y, n, behavior,
            CubicInterpolation::FritschButland, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeMixedLinearKrugerCubic : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearKrugerCubic(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) :
        SafeMixedLinearCubicInterpolation(
            x, y, n, behavior,
            CubicInterpolation::Kruger, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeMixedLinearMonotonicCubicNaturalSpline : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearMonotonicCubicNaturalSpline(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) :
        SafeMixedLinearCubicInterpolation(
            x, y, n, behavior,
            CubicInterpolation::Spline, true,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeMixedLinearMonotonicParabolic : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearMonotonicParabolic(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) :
        SafeMixedLinearCubicInterpolation(
            x, y, n, behavior,
            CubicInterpolation::Parabolic, true,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeMixedLinearParabolic : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearParabolic(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) :
        SafeMixedLinearCubicInterpolation(
            x, y, n, behavior,
            CubicInterpolation::Parabolic, false,
            CubicInterpolation::SecondDerivative, 0.0,
            CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeKernelInterpolation : public SafeInterpolation {
  public:
    SafeKernelInterpolation(
        const Array &x,
        const Array &y,
        const GaussianKernel &kernel,
        double epsilon = 1.0E-7) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new KernelInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                kernel, epsilon));
    }
    SafeKernelInterpolation(
        const Array &x,
        const Array &y,
        PyObject* kernel,
        double epsilon = 1.0E-7) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new KernelInterpolation(
                x_.begin(), x_.end(), y_.begin(),
                UnaryFunction(kernel), epsilon));
    }
};

class SafeConvexMonotoneInterpolation : public SafeInterpolation {
  public:
    SafeConvexMonotoneInterpolation(
        const Array& x, const Array& y,
        Real quadraticity,
        Real monotonicity, bool forcePositive,
        bool flatFinalPeriod = false) : SafeInterpolation(x, y) {
        i_ = ext::shared_ptr<Interpolation>(
            new ConvexMonotoneInterpolation<Array::const_iterator, Array::const_iterator>(
                x_.begin(), x_.end(), y_.begin(),
                quadraticity, monotonicity,
                forcePositive, flatFinalPeriod));
    }
};
%}

%shared_ptr(SafeAbcdInterpolation)
class SafeAbcdInterpolation : public SafeInterpolation {
  public:
    SafeAbcdInterpolation(
        const Array &x,
        const Array &y,
        Real a = -0.06,
        Real b = 0.17,
        Real c = 0.54,
        Real d = 0.17,
        bool aIsFixed = false,
        bool bIsFixed = false,
        bool cIsFixed = false,
        bool dIsFixed = false,
        bool vegaWeighted = false,
        const ext::shared_ptr<EndCriteria> &endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod = ext::shared_ptr<OptimizationMethod>());

    Real a() const;
    Real b() const;
    Real c() const;
    Real d() const;
    std::vector<Real> k() const;
    Real rmsError() const;
    Real maxError() const;
    EndCriteria::Type endCriteria();
    Real k(Time t, const Array &x) const;
};

%shared_ptr(SafeBackwardFlatInterpolation)
class SafeBackwardFlatInterpolation : public SafeInterpolation {
  public:
    SafeBackwardFlatInterpolation(
        const Array &x, const Array &y);
};

%shared_ptr(SafeForwardFlatInterpolation)
class SafeForwardFlatInterpolation : public SafeInterpolation {
  public:
    SafeForwardFlatInterpolation(
        const Array &x, const Array &y);
};

%shared_ptr(SafeLagrangeInterpolation)
class SafeLagrangeInterpolation : public SafeInterpolation {
  public:
    SafeLagrangeInterpolation(
        const Array &x, const Array &y);
    Real value(const Array &y, Real x) const;
};

%shared_ptr(SafeLinearFlatInterpolation)
class SafeLinearFlatInterpolation : public SafeInterpolation {
  public:
    SafeLinearFlatInterpolation(
        const Array &x, const Array &y);
};

%shared_ptr(SafeLinearInterpolation)
class SafeLinearInterpolation : public SafeInterpolation {
  public:
    SafeLinearInterpolation(
        const Array &x, const Array &y);
};

%shared_ptr(SafeLogLinearInterpolation)
class SafeLogLinearInterpolation : public SafeInterpolation {
  public:
    SafeLogLinearInterpolation(
        const Array &x, const Array &y);
};

%shared_ptr(SafeNoArbSabrInterpolation)
class SafeNoArbSabrInterpolation : public SafeInterpolation {
  public:
    SafeNoArbSabrInterpolation(
        const Array &x,
        const Array &y,
        Time t,
        const Real &forward,
        Real alpha, Real beta, Real nu, Real rho,
        bool alphaIsFixed,
        bool betaIsFixed,
        bool nuIsFixed,
        bool rhoIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria> &endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const Real shift = 0.0);

    Real expiry() const;
    Real forward() const;
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real rmsError() const;
    Real maxError() const;
    const std::vector<Real> &interpolationWeights() const;
    EndCriteria::Type endCriteria();
};

%shared_ptr(SafeSABRInterpolation)
class SafeSABRInterpolation : public SafeInterpolation {
  public:
    SafeSABRInterpolation(
        const Array &x,
        const Array &y,
        Time t,
        const Real &forward,
        Real alpha, Real beta, Real nu, Real rho,
        bool alphaIsFixed,
        bool betaIsFixed,
        bool nuIsFixed,
        bool rhoIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria> &endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const Real shift = 0.0);

    Real expiry() const;
    Real forward() const;
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real rmsError() const;
    Real maxError() const;
    const std::vector<Real> &interpolationWeights() const;
    EndCriteria::Type endCriteria();
};

%shared_ptr(SafeSviInterpolation)
class SafeSviInterpolation : public SafeInterpolation {
  public:
    SafeSviInterpolation(
        const Array &x,
        const Array &y,
        Time t,
        const Real &forward,
        Real a, Real b, Real sigma, Real rho, Real m,
        bool aIsFixed, bool bIsFixed, bool sigmaIsFixed,
        bool rhoIsFixed,
        bool mIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria> &endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50);

    Real expiry() const;
    Real forward() const;
    Real a() const;
    Real b() const;
    Real sigma() const;
    Real rho() const;
    Real m() const;
    Real rmsError() const;
    Real maxError() const;
    const std::vector<Real> &interpolationWeights() const;
    EndCriteria::Type endCriteria();
};

%shared_ptr(SafeVannaVolgaInterpolation)
class SafeVannaVolgaInterpolation : public SafeInterpolation {
  public:
    SafeVannaVolgaInterpolation(
        const Array &x, const Array &y,
        Real spot,
        DiscountFactor dDiscount,
        DiscountFactor fDiscount,
        Time T);
};

%shared_ptr(SafeCubicInterpolation)
class SafeCubicInterpolation : public SafeInterpolation {
  public:
    SafeCubicInterpolation(
        const Array &x, const Array &y,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic,
        CubicInterpolation::BoundaryCondition leftCond,
        Real leftConditionValue,
        CubicInterpolation::BoundaryCondition rightCond,
        Real rightConditionValue);

    const std::vector<Real> &primitiveConstants() const;
    const std::vector<Real> &aCoefficients() const;
    const std::vector<Real> &bCoefficients() const;
    const std::vector<Real> &cCoefficients() const;
    const std::vector<bool> &monotonicityAdjustments() const;
};

%shared_ptr(SafeLogMixedLinearCubicInterpolation)
class SafeLogMixedLinearCubicInterpolation : public SafeInterpolation {
  public:
    SafeLogMixedLinearCubicInterpolation(
        const Array &x, const Array &y,
        const Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic,
        CubicInterpolation::BoundaryCondition leftC,
        Real leftConditionValue,
        CubicInterpolation::BoundaryCondition rightC,
        Real rightConditionValue);
};

%shared_ptr(SafeLogCubicInterpolation)
class SafeLogCubicInterpolation : public SafeInterpolation {
  public:
    SafeLogCubicInterpolation(
        const Array &x, const Array &y,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic,
        CubicInterpolation::BoundaryCondition leftC,
        Real leftConditionValue,
        CubicInterpolation::BoundaryCondition rightC,
        Real rightConditionValue);
};

%shared_ptr(SafeMixedLinearCubicInterpolation)
class SafeMixedLinearCubicInterpolation : public SafeInterpolation {
  public:
    SafeMixedLinearCubicInterpolation(
        const Array &x, const Array &y,
        const Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic,
        CubicInterpolation::BoundaryCondition leftC,
        Real leftConditionValue,
        CubicInterpolation::BoundaryCondition rightC,
        Real rightConditionValue);
};

%shared_ptr(SafeAkimaCubicInterpolation)
class SafeAkimaCubicInterpolation : public SafeCubicInterpolation {
  public:
    SafeAkimaCubicInterpolation(
        const Array &x, const Array &y);
};

%shared_ptr(SafeCubicNaturalSpline)
class SafeCubicNaturalSpline : public SafeCubicInterpolation {
  public:
    SafeCubicNaturalSpline(
        const Array &x, const Array &y);
};

%shared_ptr(SafeCubicSplineOvershootingMinimization1)
class SafeCubicSplineOvershootingMinimization1 : public SafeCubicInterpolation {
  public:
    SafeCubicSplineOvershootingMinimization1(
        const Array &x, const Array &y);
};

%shared_ptr(SafeCubicSplineOvershootingMinimization2)
class SafeCubicSplineOvershootingMinimization2 : public SafeCubicInterpolation {
  public:
    SafeCubicSplineOvershootingMinimization2(
        const Array &x, const Array &y);
};

%shared_ptr(SafeFritschButlandCubic)
class SafeFritschButlandCubic : public SafeCubicInterpolation {
  public:
    SafeFritschButlandCubic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeHarmonicCubic)
class SafeHarmonicCubic : public SafeCubicInterpolation {
  public:
    SafeHarmonicCubic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeKrugerCubic)
class SafeKrugerCubic : public SafeCubicInterpolation {
  public:
    SafeKrugerCubic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeMonotonicCubicNaturalSpline)
class SafeMonotonicCubicNaturalSpline : public SafeCubicInterpolation {
  public:
    SafeMonotonicCubicNaturalSpline(
        const Array &x, const Array &y);
};

%shared_ptr(SafeMonotonicParabolic)
class SafeMonotonicParabolic : public SafeCubicInterpolation {
  public:
    SafeMonotonicParabolic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeParabolic)
class SafeParabolic : public SafeCubicInterpolation {
  public:
    SafeParabolic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeLogMixedLinearCubicNaturalSpline)
class SafeLogMixedLinearCubicNaturalSpline : public SafeLogMixedLinearCubicInterpolation {
  public:
    SafeLogMixedLinearCubicNaturalSpline(
        const Array &x, const Array &y,
        const Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges);
};

%shared_ptr(SafeFritschButlandLogCubic)
class SafeFritschButlandLogCubic : public SafeLogCubicInterpolation {
  public:
    SafeFritschButlandLogCubic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeHarmonicLogCubic)
class SafeHarmonicLogCubic : public SafeLogCubicInterpolation {
  public:
    SafeHarmonicLogCubic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeKrugerLogCubic)
class SafeKrugerLogCubic : public SafeLogCubicInterpolation {
  public:
    SafeKrugerLogCubic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeLogCubicNaturalSpline)
class SafeLogCubicNaturalSpline : public SafeLogCubicInterpolation {
  public:
    SafeLogCubicNaturalSpline(
        const Array &x, const Array &y);
};

%shared_ptr(SafeLogParabolic)
class SafeLogParabolic : public SafeLogCubicInterpolation {
  public:
    SafeLogParabolic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeMonotonicLogCubicNaturalSpline)
class SafeMonotonicLogCubicNaturalSpline : public SafeLogCubicInterpolation {
  public:
    SafeMonotonicLogCubicNaturalSpline(
        const Array &x, const Array &y);
};

%shared_ptr(SafeMonotonicLogParabolic)
class SafeMonotonicLogParabolic : public SafeLogCubicInterpolation {
  public:
    SafeMonotonicLogParabolic(
        const Array &x, const Array &y);
};

%shared_ptr(SafeMixedLinearCubicNaturalSpline)
class SafeMixedLinearCubicNaturalSpline : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearCubicNaturalSpline(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges);
};

%shared_ptr(SafeMixedLinearFritschButlandCubic)
class SafeMixedLinearFritschButlandCubic : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearFritschButlandCubic(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges);
};

%shared_ptr(SafeMixedLinearKrugerCubic)
class SafeMixedLinearKrugerCubic : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearKrugerCubic(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges);
};

%shared_ptr(SafeMixedLinearMonotonicCubicNaturalSpline)
class SafeMixedLinearMonotonicCubicNaturalSpline : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearMonotonicCubicNaturalSpline(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges);
};

%shared_ptr(SafeMixedLinearMonotonicParabolic)
class SafeMixedLinearMonotonicParabolic : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearMonotonicParabolic(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges);
};

%shared_ptr(SafeMixedLinearParabolic)
class SafeMixedLinearParabolic : public SafeMixedLinearCubicInterpolation {
  public:
    SafeMixedLinearParabolic(
        const Array &x, const Array &y,
        Size n,
        MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges);
};

%shared_ptr(SafeKernelInterpolation)
class SafeKernelInterpolation : public SafeInterpolation {
  public:
    SafeKernelInterpolation(
        const Array &x,
        const Array &y,
        const GaussianKernel &kernel,
        double epsilon = 1.0E-7);
    SafeKernelInterpolation(
        const Array &x,
        const Array &y,
        PyObject* kernel,
        double epsilon = 1.0E-7);
};

%shared_ptr(SafeConvexMonotoneInterpolation)
class SafeConvexMonotoneInterpolation : public SafeInterpolation {
  public:
    SafeConvexMonotoneInterpolation(
        const Array& x, const Array& y,
        Real quadraticity,
        Real monotonicity, bool forcePositive,
        bool flatFinalPeriod = false);
};

#endif
