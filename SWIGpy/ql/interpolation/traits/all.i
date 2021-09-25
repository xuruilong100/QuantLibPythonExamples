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
    %rename(globalInterpolate) global;
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
    }
    static const bool global = false;
    static const Size requiredPoints = 1;
};

class BackwardFlat {
  public:
    %rename(globalInterpolate) global;
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
    }
    static const bool global = false;
    static const Size requiredPoints = 1;
};

class ConvexMonotone {
  public:
    %rename(globalInterpolate) global;
    static const bool global = true;
    static const Size requiredPoints = 2;
    static const Size dataSizeAdjustment = 1;

    explicit ConvexMonotone(Real quadraticity = 0.3,
                            Real monotonicity = 0.7,
                            bool forcePositive = true);

    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
        Interpolation localInterpolate(
            const Array& x, const Array& y,
            Size localisation,
            Interpolation& prevInterpolation,
            Size finalSize) const {
                return self->localInterpolate(
                    x.begin(), x.end(), y.begin(),
                    localisation,
                    prevInterpolation,
                    finalSize);
        }
    }
};

class Cubic {
  public:
    %rename(globalInterpolate) global;
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
    }
    static const bool global = true;
    static const Size requiredPoints = 2;
};

class ForwardFlat {
  public:
    %rename(globalInterpolate) global;
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
    }
    static const bool global = false;
    static const Size requiredPoints = 2;
};

class Linear {
  public:
    %rename(globalInterpolate) global;
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
    }
    static const bool global = false;
    static const Size requiredPoints = 2;
};

class LogLinear {
  public:
    %rename(globalInterpolate) global;
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
    }
    static const bool global = false;
    static const Size requiredPoints = 2;
};

class LogCubic {
  public:
    %rename(globalInterpolate) global;
    LogCubic(CubicInterpolation::DerivativeApprox da,
              bool monotonic = true,
              CubicInterpolation::BoundaryCondition leftCondition
                  = CubicInterpolation::SecondDerivative,
              Real leftConditionValue = 0.0,
              CubicInterpolation::BoundaryCondition rightCondition
                  = CubicInterpolation::SecondDerivative,
              Real rightConditionValue = 0.0);
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
    }
    static const bool global = true;
    static const Size requiredPoints = 2;
};

class LogMixedLinearCubic {
  public:
    %rename(globalInterpolate) global;
    LogMixedLinearCubic(const Size n,
                        MixedInterpolation::Behavior behavior,
                        CubicInterpolation::DerivativeApprox da,
                        bool monotonic = true,
                        CubicInterpolation::BoundaryCondition leftCondition
                            = CubicInterpolation::SecondDerivative,
                        Real leftConditionValue = 0.0,
                        CubicInterpolation::BoundaryCondition rightCondition
                            = CubicInterpolation::SecondDerivative,
                        Real rightConditionValue = 0.0);
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
    }
    static const bool global = true;
    static const Size requiredPoints = 3;
};

class MixedLinearCubic {
  public:
    %rename(globalInterpolate) global;
    MixedLinearCubic(Size n,
                     MixedInterpolation::Behavior behavior,
                     CubicInterpolation::DerivativeApprox da,
                     bool monotonic = true,
                     CubicInterpolation::BoundaryCondition leftCondition
                         = CubicInterpolation::SecondDerivative,
                     Real leftConditionValue = 0.0,
                     CubicInterpolation::BoundaryCondition rightCondition
                         = CubicInterpolation::SecondDerivative,
                     Real rightConditionValue = 0.0);
    %extend {
        Interpolation interpolate(
            const Array& x, const Array& y) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin());
        }
    }
    static const bool global = true;
    static const Size requiredPoints = 3;
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
    %rename(globalInterpolate) global;
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
    }
    static const bool global = true;
};

class Abcd {
  public:
    %rename(globalInterpolate) global;
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
    }
    static const bool global = true;
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
