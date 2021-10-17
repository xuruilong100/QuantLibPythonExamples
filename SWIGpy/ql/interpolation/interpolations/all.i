#ifndef ql_interpolation_interpolation_all_i
#define ql_interpolation_interpolation_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/Interpolation.i

%{
using QuantLib::AbcdInterpolation;
using QuantLib::BackwardFlatInterpolation;
using QuantLib::ForwardFlatInterpolation;
using QuantLib::LagrangeInterpolation;
using QuantLib::LinearFlatInterpolation;
using QuantLib::LinearInterpolation;
using QuantLib::LogLinearInterpolation;
using QuantLib::NoArbSabrInterpolation;
using QuantLib::SABRInterpolation;
using QuantLib::SviInterpolation;
using QuantLib::VannaVolgaInterpolation;
using QuantLib::CubicInterpolation;
using QuantLib::LogMixedLinearCubicInterpolation;
using QuantLib::LogCubicInterpolation;
using QuantLib::MixedLinearCubicInterpolation;
using QuantLib::AkimaCubicInterpolation;
using QuantLib::CubicNaturalSpline;
using QuantLib::CubicSplineOvershootingMinimization1;
using QuantLib::CubicSplineOvershootingMinimization2;
using QuantLib::FritschButlandCubic;
using QuantLib::HarmonicCubic;
using QuantLib::KrugerCubic;
using QuantLib::MonotonicCubicNaturalSpline;
using QuantLib::MonotonicParabolic;
using QuantLib::Parabolic;
using QuantLib::LogMixedLinearCubicNaturalSpline;
using QuantLib::FritschButlandLogCubic;
using QuantLib::HarmonicLogCubic;
using QuantLib::KrugerLogCubic;
using QuantLib::LogCubicNaturalSpline;
using QuantLib::LogParabolic;
using QuantLib::MonotonicLogCubicNaturalSpline;
using QuantLib::MonotonicLogParabolic;
using QuantLib::MixedLinearCubicNaturalSpline;
using QuantLib::MixedLinearFritschButlandCubic;
using QuantLib::MixedLinearKrugerCubic;
using QuantLib::MixedLinearMonotonicCubicNaturalSpline;
using QuantLib::MixedLinearMonotonicParabolic;
using QuantLib::MixedLinearParabolic;
%}

%shared_ptr(AbcdInterpolation)
class AbcdInterpolation : public Interpolation {
  public:
    %extend {
    AbcdInterpolation(
        const Array& x, const Array& y,
        Real a = -0.06,
        Real b =  0.17,
        Real c =  0.54,
        Real d =  0.17,
        bool aIsFixed = false,
        bool bIsFixed = false,
        bool cIsFixed = false,
        bool dIsFixed = false,
        bool vegaWeighted = false,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod>& optMethod = ext::shared_ptr<OptimizationMethod>()) {
                return new AbcdInterpolation(
                    x.begin(), x.end(), y.begin(),
                    a, b, c, d,
                    aIsFixed, bIsFixed, cIsFixed, dIsFixed,
                    vegaWeighted, endCriteria, optMethod);
            }
    }

    Real a() const;
    Real b() const;
    Real c() const;
    Real d() const;
    std::vector<Real> k() const;
    Real rmsError() const;
    Real maxError() const;
    EndCriteria::Type endCriteria();
    template <class I1>
    Real k(Time t, const I1& xBegin, const I1& xEnd) const;
};

%shared_ptr(BackwardFlatInterpolation)
class BackwardFlatInterpolation : public Interpolation {
  public:
    %extend {
        BackwardFlatInterpolation(const Array& x, const Array& y) {
            return new BackwardFlatInterpolation(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(ForwardFlatInterpolation)
class ForwardFlatInterpolation : public Interpolation {
  public:
    %extend {
        ForwardFlatInterpolation(const Array& x, const Array& y) {
            return new ForwardFlatInterpolation(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(LagrangeInterpolation)
class LagrangeInterpolation : public Interpolation {
  public:
    %extend {
        LagrangeInterpolation(const Array& x, const Array& y) {
            return new LagrangeInterpolation(
                x.begin(), x.end(), y.begin());
        }
    }
    Real value(const Array& y, Real x) const;
};

%shared_ptr(LinearFlatInterpolation)
class LinearFlatInterpolation : public Interpolation {
  public:
    %extend {
        LinearFlatInterpolation(const Array& x, const Array& y) {
            return new LinearFlatInterpolation(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(LinearInterpolation)
class LinearInterpolation : public Interpolation {
  public:
    %extend {
        LinearInterpolation(const Array& x, const Array& y) {
            return new LinearInterpolation(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(LogLinearInterpolation)
class LogLinearInterpolation : public Interpolation {
  public:
    %extend {
        LogLinearInterpolation(const Array& x, const Array& y) {
            return new LogLinearInterpolation(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(NoArbSabrInterpolation)
class NoArbSabrInterpolation : public Interpolation {
  public:
    %extend {
        NoArbSabrInterpolation(
            const Array& x, // x = strikes
            const Array& y, // y = volatilities
            Time t,         // option expiry
            const Real& forward,
            Real alpha, Real beta, Real nu, Real rho,
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
            const Real shift = 0.0) {
            return new NoArbSabrInterpolation(
                x.begin(), x.end(), y.begin(),
                t,
                forward,
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
                shift);
        }
    }

    Real expiry() const;
    Real forward() const;
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real rmsError() const;
    Real maxError() const;
    const std::vector<Real>& interpolationWeights() const;
    EndCriteria::Type endCriteria();
};

%shared_ptr(SABRInterpolation)
class SABRInterpolation : public Interpolation {
  public:
    %extend {
        SABRInterpolation(
            const Array& x, // x = strikes
            const Array& y, // y = volatilities
            Time t,         // option expiry
            const Real& forward,
            Real alpha, Real beta, Real nu, Real rho,
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
            const Real shift = 0.0) {
            return new SABRInterpolation(
                x.begin(), x.end(), y.begin(),
                t, forward,
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
                shift);
        }
    }

    Real expiry() const;
    Real forward() const;
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real rmsError() const;
    Real maxError() const;
    const std::vector<Real>& interpolationWeights() const;
    EndCriteria::Type endCriteria();
};

%shared_ptr(SviInterpolation)
class SviInterpolation : public Interpolation {
  public:
    %extend {
        SviInterpolation(
            const Array& x, // x = strikes
            const Array& y, // y = volatilities
            Time t,         // option expiry
            const Real& forward,
            Real a, Real b, Real sigma, Real rho, Real m,
            bool aIsFixed, bool bIsFixed, bool sigmaIsFixed,
            bool rhoIsFixed,
            bool mIsFixed,
            bool vegaWeighted = true,
            const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
            const ext::shared_ptr<OptimizationMethod>& optMethod = ext::shared_ptr<OptimizationMethod>(),
            const Real errorAccept = 0.0020,
            const bool useMaxError = false,
            const Size maxGuesses = 50) {
            return new SviInterpolation(
                x.begin(), x.end(), y.begin(),
                t, forward,
                a, b, sigma, rho, m,
                aIsFixed, bIsFixed, sigmaIsFixed,
                rhoIsFixed, mIsFixed,
                vegaWeighted ,
                endCriteria,
                optMethod,
                errorAccept,
                useMaxError,
                maxGuesses);
        }
    }

    Real expiry() const;
    Real forward() const;
    Real a() const;
    Real b() const;
    Real sigma() const;
    Real rho() const;
    Real m() const;
    Real rmsError() const;
    Real maxError() const;
    const std::vector<Real>& interpolationWeights() const;
    EndCriteria::Type endCriteria();
};

%shared_ptr(VannaVolgaInterpolation)
class VannaVolgaInterpolation : public Interpolation {
  public:
    %extend {
        VannaVolgaInterpolation(
            const Array& x, const Array& y,
            Real spot,
            DiscountFactor dDiscount,
            DiscountFactor fDiscount,
            Time T) {
            return new VannaVolgaInterpolation(
                x.begin(), x.end(), y.begin(),
                spot, dDiscount, fDiscount, T);
        }
    }
};

%shared_ptr(CubicInterpolation)
class CubicInterpolation : public Interpolation {
  public:
    enum DerivativeApprox {
        Spline,
        SplineOM1,
        SplineOM2,
        FourthOrder,
        Parabolic,
        FritschButland,
        Akima,
        Kruger,
        Harmonic,
    };
    enum BoundaryCondition {
        NotAKnot,
        FirstDerivative,
        SecondDerivative,
        Periodic,
        Lagrange
    };
    %extend {
        CubicInterpolation(
            const Array& x, const Array& y,
            CubicInterpolation::DerivativeApprox da,
            bool monotonic,
            CubicInterpolation::BoundaryCondition leftCond,
            Real leftConditionValue,
            CubicInterpolation::BoundaryCondition rightCond,
            Real rightConditionValue) {
            return new CubicInterpolation(
                x.begin(), x.end(), y.begin(),
                da,
                monotonic,
                leftCond,
                leftConditionValue,
                rightCond,
                rightConditionValue);
        }
    }

    const std::vector<Real>& primitiveConstants() const;
    const std::vector<Real>& aCoefficients() const;
    const std::vector<Real>& bCoefficients() const;
    const std::vector<Real>& cCoefficients() const;
    const std::vector<bool>& monotonicityAdjustments() const;
};

%shared_ptr(LogMixedLinearCubicInterpolation)
class LogMixedLinearCubicInterpolation : public Interpolation {
  public:
    %extend {
        LogMixedLinearCubicInterpolation(
            const Array& x, const Array& y,
            const Size n,
            MixedInterpolation::Behavior behavior,
            CubicInterpolation::DerivativeApprox da,
            bool monotonic,
            CubicInterpolation::BoundaryCondition leftC,
            Real leftConditionValue,
            CubicInterpolation::BoundaryCondition rightC,
            Real rightConditionValue) {
            return new LogMixedLinearCubicInterpolation(
                x.begin(), x.end(), y.begin(),
                n,
                behavior,
                da,
                monotonic,
                leftC,
                leftConditionValue,
                rightC,
                rightConditionValue);
        }
    }
};

%shared_ptr(LogCubicInterpolation)
class LogCubicInterpolation : public Interpolation {
  public:
    %extend {
        LogCubicInterpolation(
            const Array& x, const Array& y,
            CubicInterpolation::DerivativeApprox da,
            bool monotonic,
            CubicInterpolation::BoundaryCondition leftC,
            Real leftConditionValue,
            CubicInterpolation::BoundaryCondition rightC,
            Real rightConditionValue) {
            return new LogCubicInterpolation(
                x.begin(), x.end(), y.begin(),
                da,
                monotonic,
                leftC,
                leftConditionValue,
                rightC,
                rightConditionValue);
        }
    }
};

%shared_ptr(MixedLinearCubicInterpolation)
class MixedLinearCubicInterpolation : public Interpolation {
  public:
    %extend {
        MixedLinearCubicInterpolation(
            const Array& x, const Array& y,
            const Size n,
            MixedInterpolation::Behavior behavior,
            CubicInterpolation::DerivativeApprox da,
            bool monotonic,
            CubicInterpolation::BoundaryCondition leftC,
            Real leftConditionValue,
            CubicInterpolation::BoundaryCondition rightC,
            Real rightConditionValue) {
            return new MixedLinearCubicInterpolation(
                x.begin(), x.end(), y.begin(),
                n,
                behavior,
                da,
                monotonic,
                leftC,
                leftConditionValue,
                rightC,
                rightConditionValue);
        }
    }
};

%shared_ptr(AkimaCubicInterpolation)
class AkimaCubicInterpolation : public CubicInterpolation {
  public:
    %extend {
        AkimaCubicInterpolation(const Array& x, const Array& y) {
            return new AkimaCubicInterpolation(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(CubicNaturalSpline)
class CubicNaturalSpline : public CubicInterpolation {
  public:
    %extend {
        CubicNaturalSpline(const Array& x, const Array& y) {
            return new CubicNaturalSpline(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(CubicSplineOvershootingMinimization1)
class CubicSplineOvershootingMinimization1 : public CubicInterpolation {
  public:
    %extend {
        CubicSplineOvershootingMinimization1(
            const Array& x, const Array& y) {
            return new CubicSplineOvershootingMinimization1(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(CubicSplineOvershootingMinimization2)
class CubicSplineOvershootingMinimization2 : public CubicInterpolation {
  public:
    %extend {
        CubicSplineOvershootingMinimization2(
            const Array& x, const Array& y) {
            return new CubicSplineOvershootingMinimization2(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(FritschButlandCubic)
class FritschButlandCubic : public CubicInterpolation {
  public:
    %extend {
        FritschButlandCubic(
            const Array& x, const Array& y) {
            return new FritschButlandCubic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(HarmonicCubic)
class HarmonicCubic : public CubicInterpolation {
  public:
    %extend {
        HarmonicCubic(
            const Array& x, const Array& y) {
            return new HarmonicCubic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(KrugerCubic)
class KrugerCubic : public CubicInterpolation {
  public:
    %extend {
        KrugerCubic(
            const Array& x, const Array& y) {
            return new KrugerCubic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(MonotonicCubicNaturalSpline)
class MonotonicCubicNaturalSpline : public CubicInterpolation {
  public:
    %extend {
        MonotonicCubicNaturalSpline(
            const Array& x, const Array& y) {
            return new MonotonicCubicNaturalSpline(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(MonotonicParabolic)
class MonotonicParabolic : public CubicInterpolation {
  public:
    %extend {
        MonotonicParabolic(
            const Array& x, const Array& y) {
            return new MonotonicParabolic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(Parabolic)
class Parabolic : public CubicInterpolation {
  public:
    %extend {
        Parabolic(
            const Array& x, const Array& y) {
            return new Parabolic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(LogMixedLinearCubicNaturalSpline)
class LogMixedLinearCubicNaturalSpline : public LogMixedLinearCubicInterpolation {
  public:
    %extend {
        LogMixedLinearCubicNaturalSpline(
            const Array& x, const Array& y,
            const Size n,
            MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) {
            return new LogMixedLinearCubicNaturalSpline(
                x.begin(), x.end(), y.begin(),
                n, behavior);
        }
    }
};

%shared_ptr(FritschButlandLogCubic)
class FritschButlandLogCubic : public LogCubicInterpolation {
  public:
    %extend {
        FritschButlandLogCubic(
            const Array& x, const Array& y) {
            return new FritschButlandLogCubic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(HarmonicLogCubic)
class HarmonicLogCubic : public LogCubicInterpolation {
  public:
    %extend {
        HarmonicLogCubic(
            const Array& x, const Array& y) {
            return new HarmonicLogCubic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(KrugerLogCubic)
class KrugerLogCubic : public LogCubicInterpolation {
  public:
    %extend {
        KrugerLogCubic(
            const Array& x, const Array& y) {
            return new KrugerLogCubic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(LogCubicNaturalSpline)
class LogCubicNaturalSpline : public LogCubicInterpolation {
  public:
    %extend {
        LogCubicNaturalSpline(
            const Array& x, const Array& y) {
            return new LogCubicNaturalSpline(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(LogParabolic)
class LogParabolic : public LogCubicInterpolation {
  public:
    %extend {
        LogParabolic(
            const Array& x, const Array& y) {
            return new LogParabolic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(MonotonicLogCubicNaturalSpline)
class MonotonicLogCubicNaturalSpline : public LogCubicInterpolation {
  public:
    %extend {
        MonotonicLogCubicNaturalSpline(
            const Array& x, const Array& y) {
            return new MonotonicLogCubicNaturalSpline(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(MonotonicLogParabolic)
class MonotonicLogParabolic : public LogCubicInterpolation {
  public:
    %extend {
        MonotonicLogParabolic(
            const Array& x, const Array& y) {
            return new MonotonicLogParabolic(
                x.begin(), x.end(), y.begin());
        }
    }
};

%shared_ptr(MixedLinearCubicNaturalSpline)
class MixedLinearCubicNaturalSpline : public MixedLinearCubicInterpolation {
  public:
    %extend {
        MixedLinearCubicNaturalSpline(
            const Array& x, const Array& y,
            MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) {
            return new MixedLinearCubicNaturalSpline(
                x.begin(), x.end(), y.begin(),
                behavior);
        }
    }
};

%shared_ptr(MixedLinearFritschButlandCubic)
class MixedLinearFritschButlandCubic : public MixedLinearCubicInterpolation {
  public:
    %extend {
        MixedLinearFritschButlandCubic(
            const Array& x, const Array& y,
            MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) {
            return new MixedLinearFritschButlandCubic(
                x.begin(), x.end(), y.begin(),
                behavior);
        }
    }
};

%shared_ptr(MixedLinearKrugerCubic)
class MixedLinearKrugerCubic : public MixedLinearCubicInterpolation {
  public:
    %extend {
        MixedLinearKrugerCubic(
            const Array& x, const Array& y,
            MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) {
            return new MixedLinearKrugerCubic(
                x.begin(), x.end(), y.begin(),
                behavior);
        }
    }
};

%shared_ptr(MixedLinearMonotonicCubicNaturalSpline)
class MixedLinearMonotonicCubicNaturalSpline : public MixedLinearCubicInterpolation {
  public:
    %extend {
        MixedLinearMonotonicCubicNaturalSpline(
            const Array& x, const Array& y,
            MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) {
            return new MixedLinearMonotonicCubicNaturalSpline(
                x.begin(), x.end(), y.begin(),
                behavior);
        }
    }
};

%shared_ptr(MixedLinearMonotonicParabolic)
class MixedLinearMonotonicParabolic : public MixedLinearCubicInterpolation {
  public:
    %extend {
        MixedLinearMonotonicParabolic(
            const Array& x, const Array& y,
            MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) {
            return new MixedLinearMonotonicParabolic(
                x.begin(), x.end(), y.begin(),
                behavior);
        }
    }
};

%shared_ptr(MixedLinearParabolic)
class MixedLinearParabolic : public MixedLinearCubicInterpolation {
  public:
    %extend {
        MixedLinearParabolic(
            const Array& x, const Array& y,
            MixedInterpolation::Behavior behavior = MixedInterpolation::ShareRanges) {
            return new MixedLinearParabolic(
                x.begin(), x.end(), y.begin(),
                behavior);
        }
    }
};

#endif
