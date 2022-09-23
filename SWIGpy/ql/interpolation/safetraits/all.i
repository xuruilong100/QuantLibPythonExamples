#ifndef ql_interpolation_safetraits_all_i
#define ql_interpolation_safetraits_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/safeinterpolations/all.i


%{
class SafeLinearFlat {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeLinearFlatInterpolation(x, y);
    }
    static const bool global = false;
    static const Size requiredPoints = 1;
};

class SafeBackwardFlat {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeBackwardFlatInterpolation(x, y);
    }
    static const bool global = false;
    static const Size requiredPoints = 1;
};

class SafeConvexMonotone {
  private:
    Real quadraticity_, monotonicity_;
    bool forcePositive_;
  public:
    static const bool global = true;
    static const Size requiredPoints = 2;
    static const Size dataSizeAdjustment = 1;

    SafeConvexMonotone(
        Real quadraticity = 0.3,
        Real monotonicity = 0.7,
        bool forcePositive = true) :
        quadraticity_(quadraticity),
        monotonicity_(monotonicity),
        forcePositive_(forcePositive) {}

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeConvexMonotoneInterpolation(
                x, y,
                quadraticity_,
                monotonicity_,
                forcePositive_);
    }
};

class SafeCubic {
  private:
    CubicInterpolation::DerivativeApprox da_;
    bool monotonic_;
    CubicInterpolation::BoundaryCondition leftType_, rightType_;
    Real leftValue_, rightValue_;
  public:
    SafeCubic(
        CubicInterpolation::DerivativeApprox da = CubicInterpolation::Kruger,
        bool monotonic = false,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0) :
        da_(da), monotonic_(monotonic),
        leftType_(leftCondition), rightType_(rightCondition),
        leftValue_(leftConditionValue), rightValue_(rightConditionValue) {}

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeCubicInterpolation(x, y,
                da_, monotonic_,
                leftType_, leftValue_,
                rightType_, rightValue_);
    }

    static const bool global = true;
    static const Size requiredPoints = 2;
};

class SafeForwardFlat {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeForwardFlatInterpolation(x, y);
    }
    static const bool global = false;
    static const Size requiredPoints = 2;
};

class SafeLinear {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeLinearInterpolation(x, y);
    }
    static const bool global = false;
    static const Size requiredPoints = 2;
};

class SafeLogLinear {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeLogLinearInterpolation(x, y);
    }
    static const bool global = false;
    static const Size requiredPoints = 2;
};

class SafeLogCubic {
  private:
    CubicInterpolation::DerivativeApprox da_;
    bool monotonic_;
    CubicInterpolation::BoundaryCondition leftType_, rightType_;
    Real leftValue_, rightValue_;
  public:
    SafeLogCubic(
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0) :
        da_(da), monotonic_(monotonic),
        leftType_(leftCondition), rightType_(rightCondition),
        leftValue_(leftConditionValue), rightValue_(rightConditionValue) {}

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeLogCubicInterpolation(
                x, y,
                da_, monotonic_,
                leftType_, leftValue_,
                rightType_, rightValue_);
    }
    static const bool global = true;
    static const Size requiredPoints = 2;
};

class SafeLogMixedLinearCubic {
  private:
    Size n_;
    MixedInterpolation::Behavior behavior_;
    CubicInterpolation::DerivativeApprox da_;
    bool monotonic_;
    CubicInterpolation::BoundaryCondition leftType_, rightType_;
    Real leftValue_, rightValue_;
  public:
    SafeLogMixedLinearCubic(
        const Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0):
        n_(n), behavior_(behavior), da_(da), monotonic_(monotonic),
        leftType_(leftCondition), rightType_(rightCondition),
        leftValue_(leftConditionValue), rightValue_(rightConditionValue) {}
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeLogMixedLinearCubicInterpolation(
                x, y,
                n_, behavior_,
                da_, monotonic_,
                leftType_, leftValue_,
                rightType_, rightValue_);
    }
    static const bool global = true;
    static const Size requiredPoints = 3;
};

class SafeMixedLinearCubic {
  private:
    Size n_;
    MixedInterpolation::Behavior behavior_;
    CubicInterpolation::DerivativeApprox da_;
    bool monotonic_;
    CubicInterpolation::BoundaryCondition leftType_, rightType_;
    Real leftValue_, rightValue_;
  public:
    SafeMixedLinearCubic(
        Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0):
        n_(n), behavior_(behavior), da_(da), monotonic_(monotonic),
        leftType_(leftCondition), rightType_(rightCondition),
        leftValue_(leftConditionValue), rightValue_(rightConditionValue) {}
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeMixedLinearCubicInterpolation(
                x, y, n_, behavior_,
                da_, monotonic_,
                leftType_, leftValue_,
                rightType_, rightValue_);
    }
    static const bool global = true;
    static const Size requiredPoints = 3;
};

class SafeDefaultLogCubic : public SafeLogCubic {
  public:
    SafeDefaultLogCubic() : SafeLogCubic(CubicInterpolation::Kruger) {}
};

class SafeMonotonicLogCubic : public SafeLogCubic {
  public:
    SafeMonotonicLogCubic() :
    SafeLogCubic(
        CubicInterpolation::Spline, true,
        CubicInterpolation::SecondDerivative, 0.0,
        CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeKrugerLog : public SafeLogCubic {
  public:
    SafeKrugerLog() :
    SafeLogCubic(
        CubicInterpolation::Kruger, false,
        CubicInterpolation::SecondDerivative, 0.0,
        CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeSABR {
  private:
    Time t_;
    Real forward_;
    Real alpha_, beta_, nu_, rho_;
    bool alphaIsFixed_, betaIsFixed_, nuIsFixed_, rhoIsFixed_;
    bool vegaWeighted_;
    const ext::shared_ptr<EndCriteria> endCriteria_;
    const ext::shared_ptr<OptimizationMethod> optMethod_;
    const Real errorAccept_;
    const bool useMaxError_;
    const Size maxGuesses_;
    const Real shift_;
  public:
    SafeSABR(
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
        bool vegaWeighted = false,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const Real shift = 0.0) :
        t_(t), forward_(forward), alpha_(alpha), beta_(beta), nu_(nu), rho_(rho),
        alphaIsFixed_(alphaIsFixed), betaIsFixed_(betaIsFixed), nuIsFixed_(nuIsFixed),
        rhoIsFixed_(rhoIsFixed), vegaWeighted_(vegaWeighted), endCriteria_(std::move(endCriteria)),
        optMethod_(std::move(optMethod)), errorAccept_(errorAccept), useMaxError_(useMaxError),
        maxGuesses_(maxGuesses), shift_(shift) {}

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeSABRInterpolation(
                x, y,
                t_, forward_, alpha_,
                beta_, nu_, rho_, alphaIsFixed_, betaIsFixed_,
                nuIsFixed_, rhoIsFixed_, vegaWeighted_,
                endCriteria_, optMethod_, errorAccept_,
                useMaxError_, maxGuesses_, shift_);
    }

    static const bool global = true;
};

class SafeAbcd {
  private:
    Real a_, b_, c_, d_;
    bool aIsFixed_, bIsFixed_, cIsFixed_, dIsFixed_;
    bool vegaWeighted_;
    const ext::shared_ptr<EndCriteria> endCriteria_;
    const ext::shared_ptr<OptimizationMethod> optMethod_;
  public:

    SafeAbcd(
        Real a,
        Real b,
        Real c,
        Real d,
        bool aIsFixed,
        bool bIsFixed,
        bool cIsFixed,
        bool dIsFixed,
        bool vegaWeighted = false,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>()) :
        a_(a), b_(b), c_(c), d_(d), aIsFixed_(aIsFixed), bIsFixed_(bIsFixed), cIsFixed_(cIsFixed),
        dIsFixed_(dIsFixed), vegaWeighted_(vegaWeighted), endCriteria_(std::move(endCriteria)),
        optMethod_(std::move(optMethod)) {}

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const {
            return SafeAbcdInterpolation(
                x, y,
                a_, b_, c_, d_,
                aIsFixed_, bIsFixed_,
                cIsFixed_, dIsFixed_,
                vegaWeighted_,
                endCriteria_, optMethod_);
    }
    static const bool global = true;
};

class SafeMonotonicCubic : public SafeCubic {
  public:
    SafeMonotonicCubic() : SafeCubic(
        CubicInterpolation::Spline, true,
        CubicInterpolation::SecondDerivative, 0.0,
        CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeSplineCubic : public SafeCubic {
  public:
    SafeSplineCubic() : SafeCubic(
        CubicInterpolation::Spline, false,
        CubicInterpolation::SecondDerivative, 0.0,
        CubicInterpolation::SecondDerivative, 0.0) {}
};

class SafeKruger : public SafeCubic {
  public:
    SafeKruger() : SafeCubic(
        CubicInterpolation::Kruger) {}
};
%}

class SafeLinearFlat {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeLinearFlat::global; }
        Size requiredPoints() const { return SafeLinearFlat::requiredPoints; }
    }
};

class SafeBackwardFlat {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeBackwardFlat::global; }
        Size requiredPoints() const { return SafeBackwardFlat::requiredPoints; }
    }
};

class SafeConvexMonotone {
  public:
    SafeConvexMonotone(
        Real quadraticity = 0.3,
        Real monotonicity = 0.7,
        bool forcePositive = true);

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeConvexMonotone::global; }
        Size requiredPoints() const { return SafeConvexMonotone::requiredPoints; }
        Size dataSizeAdjustment() const { return SafeConvexMonotone::dataSizeAdjustment; }
    }
};

class SafeCubic {
  public:
    SafeCubic(
        CubicInterpolation::DerivativeApprox da = CubicInterpolation::Kruger,
        bool monotonic = false,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0);

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeCubic::global; }
        Size requiredPoints() const { return SafeCubic::requiredPoints; }
    }
};

class SafeForwardFlat {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeForwardFlat::global; }
        Size requiredPoints() const { return SafeForwardFlat::requiredPoints; }
    }
};

class SafeLinear {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeLinear::global; }
        Size requiredPoints() const { return SafeLinear::requiredPoints; }
    }
};

class SafeLogLinear {
  public:
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeLogLinear::global; }
        Size requiredPoints() const { return SafeLogLinear::requiredPoints; }
    }
};

class SafeLogCubic {
  public:
    SafeLogCubic(
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0);

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeLogCubic::global; }
        Size requiredPoints() const { return SafeLogCubic::requiredPoints; }
    }
};

class SafeLogMixedLinearCubic {
  public:
    SafeLogMixedLinearCubic(
        const Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0);
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeLogMixedLinearCubic::global; }
        Size requiredPoints() const { return SafeLogMixedLinearCubic::requiredPoints; }
    }
};

class SafeMixedLinearCubic {
  public:
    SafeMixedLinearCubic(
        Size n,
        MixedInterpolation::Behavior behavior,
        CubicInterpolation::DerivativeApprox da,
        bool monotonic = true,
        CubicInterpolation::BoundaryCondition leftCondition = CubicInterpolation::SecondDerivative,
        Real leftConditionValue = 0.0,
        CubicInterpolation::BoundaryCondition rightCondition = CubicInterpolation::SecondDerivative,
        Real rightConditionValue = 0.0);
    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeMixedLinearCubic::global; }
        Size requiredPoints() const { return SafeMixedLinearCubic::requiredPoints; }
    }
};

class SafeDefaultLogCubic : public SafeLogCubic {
  public:
    SafeDefaultLogCubic();
};

class SafeMonotonicLogCubic : public SafeLogCubic {
  public:
    SafeMonotonicLogCubic();
};

class SafeKrugerLog : public SafeLogCubic {
  public:
    SafeKrugerLog();
};

class SafeSABR {
  public:
    SafeSABR(
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
        bool vegaWeighted = false,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50,
        const Real shift = 0.0);

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeSABR::global; }
    }
};

class SafeAbcd {
  public:
    SafeAbcd(
        Real a,
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

    SafeInterpolation interpolate(
        const Array& x, const Array& y) const;
    %extend {
        bool isGlobal() const { return SafeAbcd::global; }
    }
};

class SafeMonotonicCubic : public SafeCubic {
  public:
    SafeMonotonicCubic();
};

class SafeSplineCubic : public SafeCubic {
  public:
    SafeSplineCubic();
};

class SafeKruger : public SafeCubic {
  public:
    SafeKruger();
};

#endif
