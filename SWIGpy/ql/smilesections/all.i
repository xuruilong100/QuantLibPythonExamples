#ifndef ql_smilesections_all_i
#define ql_smilesections_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::SabrSmileSection;
using QuantLib::FlatSmileSection;
using QuantLib::InterpolatedSmileSection;
using QuantLib::KahaleSmileSection;

using QuantLib::ZabrShortMaturityLognormal;
using QuantLib::ZabrShortMaturityNormal;
using QuantLib::ZabrLocalVolatility;
using QuantLib::ZabrFullFd;

using QuantLib::ZabrSmileSection;
using QuantLib::ZabrInterpolatedSmileSection;
using QuantLib::NoArbSabrSmileSection;
using QuantLib::NoArbSabrInterpolatedSmileSection;

using QuantLib::sabrVolatility;
using QuantLib::shiftedSabrVolatility;
using QuantLib::sabrFlochKennedyVolatility;
%}

%shared_ptr(SabrSmileSection)
class SabrSmileSection : public SmileSection {
  public:
    SabrSmileSection(const Date& d,
                     Rate forward,
                     const std::vector<Real>& sabrParameters,
                     const DayCounter& dc = Actual365Fixed(),
                     Real shift = 0.0);
    SabrSmileSection(Time timeToExpiry,
                     Rate forward,
                     const std::vector<Real>& sabrParameters,
                     Real shift = 0.0);
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
};

%shared_ptr(FlatSmileSection)
class FlatSmileSection : public SmileSection {
  public:
    FlatSmileSection(const Date& d,
                     Volatility vol,
                     const DayCounter& dc,
                     const Date& referenceDate = Date(),
                     Real atmLevel = Null<Rate>(),
                     VolatilityType type = ShiftedLognormal,
                     Real shift = 0.0);
    FlatSmileSection(Time exerciseTime,
                     Volatility vol,
                     const DayCounter& dc,
                     Real atmLevel = Null<Rate>(),
                     VolatilityType type = ShiftedLognormal,
                     Real shift = 0.0);
};

template<class Interpolator>
class InterpolatedSmileSection : public SmileSection {
  public:
    InterpolatedSmileSection(
        Time expiryTime,
        const std::vector<Rate>& strikes,
        const std::vector<Handle<Quote>>& stdDevHandles,
        const Handle<Quote>& atmLevel,
        const Interpolator& interpolator = Interpolator(),
        const DayCounter& dc = Actual365Fixed(),
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    InterpolatedSmileSection(
        Time expiryTime,
        const std::vector<Rate>& strikes,
        const std::vector<Real>& stdDevs,
        Real atmLevel,
        const Interpolator& interpolator = Interpolator(),
        const DayCounter& dc = Actual365Fixed(),
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    InterpolatedSmileSection(
        const Date& d,
        const std::vector<Rate>& strikes,
        const std::vector<Handle<Quote>>& stdDevHandles,
        const Handle<Quote>& atmLevel,
        const DayCounter& dc = Actual365Fixed(),
        const Interpolator& interpolator = Interpolator(),
        const Date& referenceDate = Date(),
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    InterpolatedSmileSection(
        const Date& d,
        const std::vector<Rate>& strikes,
        const std::vector<Real>& stdDevs,
        Real atmLevel,
        const DayCounter& dc = Actual365Fixed(),
        const Interpolator& interpolator = Interpolator(),
        const Date& referenceDate = Date(),
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
};

%define export_smileinterpolation_curve(Name,Interpolator)
%shared_ptr(InterpolatedSmileSection<Interpolator>)
%template(Name) InterpolatedSmileSection<Interpolator>;
%enddef

export_smileinterpolation_curve(LinearInterpolatedSmileSection, Linear);
export_smileinterpolation_curve(CubicInterpolatedSmileSection, Cubic);
export_smileinterpolation_curve(MonotonicCubicInterpolatedSmileSection, MonotonicCubic);
export_smileinterpolation_curve(SplineCubicInterpolatedSmileSection, SplineCubic);

%shared_ptr(KahaleSmileSection)
class KahaleSmileSection : public SmileSection {
  public:
    KahaleSmileSection(
        const ext::shared_ptr<SmileSection> source,
        const Real atm = Null<Real>(),
        const bool interpolate = false,
        const bool exponentialExtrapolation = false,
        const bool deleteArbitragePoints = false,
        const std::vector<Real>& moneynessGrid = std::vector<Real>(),
        const Real gap = 1.0E-5,
        const int forcedLeftIndex = -1,
        const int forcedRightIndex = QL_MAX_INTEGER);
};

struct ZabrShortMaturityLognormal {};
struct ZabrShortMaturityNormal {};
struct ZabrLocalVolatility {};
struct ZabrFullFd {};

template <class Evaluation>
class ZabrSmileSection : public SmileSection {
  public:
    ZabrSmileSection(
        Time timeToExpiry,
        Rate forward,
        const std::vector<Real>& zabrParameters,
        const std::vector<Real>& moneyness = std::vector<Real>(),
        const Size fdRefinement = 5);
    ZabrSmileSection(
        const Date& d,
        Rate forward,
        const std::vector<Real>& zabrParameters,
        const DayCounter& dc = Actual365Fixed(),
        const std::vector<Real>& moneyness = std::vector<Real>(),
        const Size fdRefinement = 5);
};

%define export_zabrsmilesection_curve(Name,Evaluation)
%shared_ptr(ZabrSmileSection<Evaluation>)
%template(Name) ZabrSmileSection<Evaluation>;
%enddef

export_zabrsmilesection_curve(ZabrShortMaturityLognormalSmileSection, ZabrShortMaturityLognormal);
export_zabrsmilesection_curve(ZabrShortMaturityNormalSmileSection, ZabrShortMaturityNormal);
export_zabrsmilesection_curve(ZabrLocalVolatilitySmileSection, ZabrLocalVolatility);
export_zabrsmilesection_curve(ZabrFullFdSmileSection, ZabrFullFd);

template <class Evaluation>
class ZabrInterpolatedSmileSection : public SmileSection {
  public:
    ZabrInterpolatedSmileSection(
        const Date& optionDate, const Handle<Quote>& forward,
        const std::vector<Rate>& strikes, bool hasFloatingStrikes,
        const Handle<Quote>& atmVolatility,
        const std::vector<Handle<Quote>>& volHandles, Real alpha, Real beta,
        Real nu, Real rho, Real gamma, bool isAlphaFixed = false,
        bool isBetaFixed = false, bool isNuFixed = false,
        bool isRhoFixed = false, bool isGammaFixed = false,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod>& method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    ZabrInterpolatedSmileSection(
        const Date& optionDate, const Rate& forward,
        const std::vector<Rate>& strikes, bool hasFloatingStrikes,
        const Volatility& atmVolatility, const std::vector<Volatility>& vols,
        Real alpha, Real beta, Real nu, Real rho, Real gamma,
        bool isAlphaFixed = false, bool isBetaFixed = false,
        bool isNuFixed = false, bool isRhoFixed = false,
        bool isGammaFixed = false, bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod>& method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real rmsError() const;
    Real maxError() const;
    EndCriteria::Type endCriteria() const;
};

%define export_zabrinterpolatedsmilesection_curve(Name,Evaluation)
%shared_ptr(ZabrInterpolatedSmileSection<Evaluation>)
%template(Name) ZabrInterpolatedSmileSection<Evaluation>;
%enddef

export_zabrinterpolatedsmilesection_curve(ZabrShortMaturityLognormalInterpolatedSmileSection, ZabrShortMaturityLognormal);
export_zabrinterpolatedsmilesection_curve(ZabrShortMaturityNormalInterpolatedSmileSection, ZabrShortMaturityNormal);
export_zabrinterpolatedsmilesection_curve(ZabrLocalVolatilityInterpolatedSmileSection, ZabrLocalVolatility);
export_zabrinterpolatedsmilesection_curve(ZabrFullFdInterpolatedSmileSection, ZabrFullFd);

%shared_ptr(NoArbSabrSmileSection)
class NoArbSabrSmileSection : public SmileSection {
  public:
    NoArbSabrSmileSection(
        Time timeToExpiry,
        Rate forward,
        const std::vector<Real>& sabrParameters,
        const Real shift = 0.0);
    NoArbSabrSmileSection(
        const Date& d,
        Rate forward,
        const std::vector<Real>& sabrParameters,
        const DayCounter& dc = Actual365Fixed(),
        const Real shift = 0.0);
};

%shared_ptr(NoArbSabrInterpolatedSmileSection)
class NoArbSabrInterpolatedSmileSection : public SmileSection {
  public:
    NoArbSabrInterpolatedSmileSection(
        const Date& optionDate, const Handle<Quote>& forward,
        const std::vector<Rate>& strikes, bool hasFloatingStrikes,
        const Handle<Quote>& atmVolatility,
        const std::vector<Handle<Quote>>& volHandles, Real alpha, Real beta,
        Real nu, Real rho, bool isAlphaFixed = false,
        bool isBetaFixed = false, bool isNuFixed = false,
        bool isRhoFixed = false,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod>& method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    NoArbSabrInterpolatedSmileSection(
        const Date& optionDate, const Rate& forward,
        const std::vector<Rate>& strikes, bool hasFloatingStrikes,
        const Volatility& atmVolatility, const std::vector<Volatility>& vols,
        Real alpha, Real beta, Real nu, Real rho,
        bool isAlphaFixed = false, bool isBetaFixed = false,
        bool isNuFixed = false, bool isRhoFixed = false,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod>& method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real rmsError() const;
    Real maxError() const;
    EndCriteria::Type endCriteria() const;
};

Real sabrVolatility(
    Rate strike,
    Rate forward,
    Time expiryTime,
    Real alpha,
    Real beta,
    Real nu,
    Real rho);

Real shiftedSabrVolatility(
    Rate strike,
    Rate forward,
    Time expiryTime,
    Real alpha,
    Real beta,
    Real nu,
    Real rho,
    Real shift);

Real sabrFlochKennedyVolatility(
    Rate strike,
    Rate forward,
    Time expiryTime,
    Real alpha,
    Real beta,
    Real nu,
    Real rho);

#endif
