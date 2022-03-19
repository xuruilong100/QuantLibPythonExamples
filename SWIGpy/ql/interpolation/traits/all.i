#ifndef ql_interpolation_traits_all_i
#define ql_interpolation_traits_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/Interpolation.i

// 1D interpolation traits

%{
using QuantLib::LinearFlat;
using QuantLib::BackwardFlat;
using QuantLib::ConvexMonotone;
using QuantLib::Cubic;
using QuantLib::ForwardFlat;
using QuantLib::Linear;
using QuantLib::LogLinear;
using QuantLib::LogCubic;
using QuantLib::LogMixedLinearCubic;
using QuantLib::MixedLinearCubic;
using QuantLib::DefaultLogCubic;
using QuantLib::MonotonicLogCubic;
using QuantLib::KrugerLog;
using QuantLib::SABR;
using QuantLib::Abcd;
%}

class LinearFlat {
  public:
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return LinearFlat::global; }
        Size requiredPoints() const { return LinearFlat::requiredPoints; }
    }
};

class BackwardFlat {
  public:
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return BackwardFlat::global; }
        Size requiredPoints() const { return BackwardFlat::requiredPoints; }
    }
};

class ConvexMonotone {
  public:
    explicit ConvexMonotone(
        Real quadraticity = 0.3,
        Real monotonicity = 0.7,
        bool forcePositive = true);

    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return ConvexMonotone::global; }
        Size requiredPoints() const { return ConvexMonotone::requiredPoints; }
        Size dataSizeAdjustment() const { return ConvexMonotone::dataSizeAdjustment; }
    }
};

class Cubic {
  public:
    Cubic(CubicInterpolation::DerivativeApprox da = CubicInterpolation::Kruger,
          bool monotonic = false,
          CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
          Real leftConditionValue = 0.0,
          CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
          Real rightConditionValue = 0.0);

    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return Cubic::global; }
        Size requiredPoints() const { return Cubic::requiredPoints; }
    }
};

class ForwardFlat {
  public:
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return ForwardFlat::global; }
        Size requiredPoints() const { return ForwardFlat::requiredPoints; }
    }
};

class Linear {
  public:
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return Linear::global; }
        Size requiredPoints() const { return Linear::requiredPoints; }
    }
};

class LogLinear {
  public:
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return LogLinear::global; }
        Size requiredPoints() const { return LogLinear::requiredPoints; }
    }
};

class LogCubic {
  public:
    LogCubic(
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0);
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return LogCubic::global; }
        Size requiredPoints() const { return LogCubic::requiredPoints; }
    }
};

class LogMixedLinearCubic {
  public:
    LogMixedLinearCubic(
        const Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0);
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return LogMixedLinearCubic::global; }
        Size requiredPoints() const { return LogMixedLinearCubic::requiredPoints; }
    }
};

class MixedLinearCubic {
  public:
    MixedLinearCubic(
        Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0);
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return MixedLinearCubic::global; }
        Size requiredPoints() const { return MixedLinearCubic::requiredPoints; }
    }
};

class DefaultLogCubic : public LogCubic {
  public:
    DefaultLogCubic();
};

class MonotonicLogCubic : public LogCubic {
  public:
    MonotonicLogCubic();
};

class KrugerLog : public LogCubic {
  public:
    KrugerLog();
};

class SABR {
  public:
    SABR(Time t,
         Real forward,
         Real alpha,
         Real beta,
         Real nu,
         Real rho,
         bool alphaIsFixed,
         bool betaIsFixed,
         bool nuIsFixed,
         bool rhoIsFixed,
         bool vegaWeighted = false,
         ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
         ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>(),
         const Real errorAccept = 0.0020,
         const bool useMaxError = false,
         const Size maxGuesses = 50,
         const Real shift = 0.0);

    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return SABR::global; }
    }
};

class Abcd {
  public:
    Abcd(Real a,
         Real b,
         Real c,
         Real d,
         bool aIsFixed,
         bool bIsFixed,
         bool cIsFixed,
         bool dIsFixed,
         bool vegaWeighted = false,
         ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
         ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>());
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        bool isGlobal() const { return Abcd::global; }
    }
};

%{
class MonotonicCubic : public Cubic {
  public:
    MonotonicCubic() : Cubic(
        QuantLib::CubicInterpolation::Spline, true,
        QuantLib::CubicInterpolation::SecondDerivative, 0.0,
        QuantLib::CubicInterpolation::SecondDerivative, 0.0) {}
};

class SplineCubic : public Cubic {
  public:
    SplineCubic() : Cubic(
        QuantLib::CubicInterpolation::Spline, false,
        QuantLib::CubicInterpolation::SecondDerivative, 0.0,
        QuantLib::CubicInterpolation::SecondDerivative, 0.0) {}
};

class Kruger : public Cubic {
  public:
    Kruger() : Cubic(
        QuantLib::CubicInterpolation::Kruger) {}
};
%}

#endif
