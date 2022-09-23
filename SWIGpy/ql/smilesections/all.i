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

using QuantLib::NoArbSabrModel;
using QuantLib::NoArbSabrSmileSection;
using QuantLib::NoArbSabrInterpolatedSmileSection;

using QuantLib::sabrVolatility;
using QuantLib::shiftedSabrVolatility;
using QuantLib::sabrFlochKennedyVolatility;
using QuantLib::AtmAdjustedSmileSection;
using QuantLib::AtmSmileSection;
using QuantLib::Gaussian1dSmileSection;
using QuantLib::AtmSmileSection;
using QuantLib::SabrInterpolatedSmileSection;
using QuantLib::SpreadedSmileSection;
using QuantLib::SviInterpolatedSmileSection;
using QuantLib::SviSmileSection;
%}

%shared_ptr(AtmAdjustedSmileSection)
class AtmAdjustedSmileSection : public SmileSection {
  public:
    AtmAdjustedSmileSection(
        const ext::shared_ptr<SmileSection>& source,
        Real atm = Null<Real>(),
        bool recenterSmile = false);
};

%shared_ptr(AtmSmileSection)
class AtmSmileSection : public SmileSection {
  public:
    AtmSmileSection(
        const ext::shared_ptr<SmileSection>& source,
        Real atm = Null<Real>());
};

%shared_ptr(FlatSmileSection)
class FlatSmileSection : public SmileSection {
  public:
    FlatSmileSection(
        const Date& d,
        Volatility vol,
        const DayCounter& dc,
        const Date& referenceDate = Date(),
        Real atmLevel = Null<Rate>(),
        VolatilityType type = ShiftedLognormal,
        Real shift = 0.0);
    FlatSmileSection(
        Time exerciseTime,
        Volatility vol,
        const DayCounter& dc,
        Real atmLevel = Null<Rate>(),
        VolatilityType type = ShiftedLognormal,
        Real shift = 0.0);
};

%shared_ptr(Gaussian1dSmileSection)
class Gaussian1dSmileSection : public SmileSection {
  public:
    Gaussian1dSmileSection(
        const Date& fixingDate,
        ext::shared_ptr<SwapIndex> swapIndex,
        const ext::shared_ptr<Gaussian1dModel>& model,
        const DayCounter& dc,
        const ext::shared_ptr<Gaussian1dSwaptionEngine>& swaptionEngine = ext::shared_ptr<Gaussian1dSwaptionEngine>());
    Gaussian1dSmileSection(
        const Date& fixingDate,
        ext::shared_ptr<IborIndex> swapIndex,
        const ext::shared_ptr<Gaussian1dModel>& model,
        const DayCounter& dc,
        const ext::shared_ptr<Gaussian1dCapFloorEngine>& capEngine = ext::shared_ptr<Gaussian1dCapFloorEngine>());
};

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
        Real leftCoreStrike() const;
        Real rightCoreStrike() const;
        std::pair<Size, Size> coreIndices() const;
};

%shared_ptr(NoArbSabrModel)
class NoArbSabrModel {
  public:
    NoArbSabrModel(
        Real expiryTime, 
        Real forward,
        Real alpha, 
        Real beta,
        Real nu, 
        Real rho);

    Real optionPrice(Real strike) const;
    Real digitalOptionPrice(Real strike) const;
    Real density(const Real strike) const;
    Real forward() const;
    Real numericalForward() const;
    Real expiryTime() const;
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real absorptionProbability() const;
};

%shared_ptr(NoArbSabrSmileSection)
class NoArbSabrSmileSection : public SmileSection {
  public:
    NoArbSabrSmileSection(
        Time timeToExpiry,
        Rate forward,
        std::vector<Real> sabrParameters,
        const Real shift = 0.0);
    NoArbSabrSmileSection(
        const Date& d,
        Rate forward,
        std::vector<Real> sabrParameters,
        const DayCounter& dc = Actual365Fixed(),
        const Real shift = 0.0);
    ext::shared_ptr<NoArbSabrModel> model();
};

%shared_ptr(NoArbSabrInterpolatedSmileSection)
class NoArbSabrInterpolatedSmileSection : public SmileSection {
  public:
    NoArbSabrInterpolatedSmileSection(
        const Date& optionDate,
        Handle<Quote> forward,
        const std::vector<Rate>& strikes,
        bool hasFloatingStrikes,
        Handle<Quote> atmVolatility,
        const std::vector<Handle<Quote>>& volHandles,
        Real alpha,
        Real beta,
        Real nu,
        Real rho,
        bool isAlphaFixed = false,
        bool isBetaFixed = false,
        bool isNuFixed = false,
        bool isRhoFixed = false,
        bool vegaWeighted = true,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    NoArbSabrInterpolatedSmileSection(
        const Date& optionDate,
        const Rate& forward,
        const std::vector<Rate>& strikes,
        bool hasFloatingStrikes,
        const Volatility& atmVolatility,
        const std::vector<Volatility>& vols,
        Real alpha,
        Real beta,
        Real nu,
        Real rho,
        bool isAlphaFixed = false,
        bool isBetaFixed = false,
        bool isNuFixed = false,
        bool isRhoFixed = false,
        bool vegaWeighted = true,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real rmsError() const;
    Real maxError() const;
    EndCriteria::Type endCriteria() const;
};

%shared_ptr(SabrSmileSection)
class SabrSmileSection : public SmileSection {
  public:
    SabrSmileSection(
        const Date& d,
        Rate forward,
        const std::vector<Real>& sabrParameters,
        const DayCounter& dc = Actual365Fixed(),
        Real shift = 0.0);
    SabrSmileSection(
        Time timeToExpiry,
        Rate forward,
        const std::vector<Real>& sabrParameters,
        Real shift = 0.0);
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
};

%inline %{
    ext::shared_ptr<SabrSmileSection> as_sabr_smile_section(
        const ext::shared_ptr<SmileSection>& cf) {
        return ext::dynamic_pointer_cast<SabrSmileSection>(cf);
    }
%}

%shared_ptr(SabrInterpolatedSmileSection)
class SabrInterpolatedSmileSection : public SmileSection, public LazyObject {
  public:
    SabrInterpolatedSmileSection(
        const Date& optionDate,
        Handle<Quote> forward,
        const std::vector<Rate>& strikes,
        bool hasFloatingStrikes,
        Handle<Quote> atmVolatility,
        const std::vector<Handle<Quote>>& volHandles,
        Real alpha,
        Real beta,
        Real nu,
        Real rho,
        bool isAlphaFixed = false,
        bool isBetaFixed = false,
        bool isNuFixed = false,
        bool isRhoFixed = false,
        bool vegaWeighted = true,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed(),
        Real shift = 0.0);
    SabrInterpolatedSmileSection(
        const Date& optionDate,
        const Rate& forward,
        const std::vector<Rate>& strikes,
        bool hasFloatingStrikes,
        const Volatility& atmVolatility,
        const std::vector<Volatility>& vols,
        Real alpha,
        Real beta,
        Real nu,
        Real rho,
        bool isAlphaFixed = false,
        bool isBetaFixed = false,
        bool isNuFixed = false,
        bool isRhoFixed = false,
        bool vegaWeighted = true,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed(),
        Real shift = 0.0);

    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real rmsError() const;
    Real maxError() const;
    EndCriteria::Type endCriteria() const;
};

%shared_ptr(SpreadedSmileSection)
class SpreadedSmileSection : public SmileSection {
  public:
    SpreadedSmileSection(
        ext::shared_ptr<SmileSection>,
        Handle<Quote> spread);
};

%shared_ptr(SviInterpolatedSmileSection)
class SviInterpolatedSmileSection : public SmileSection, public LazyObject {
  public:
    SviInterpolatedSmileSection(
        const Date& optionDate,
        Handle<Quote> forward,
        const std::vector<Rate>& strikes,
        bool hasFloatingStrikes,
        Handle<Quote> atmVolatility,
        const std::vector<Handle<Quote>>& volHandles,
        Real a,
        Real b,
        Real sigma,
        Real rho,
        Real m,
        bool aIsFixed,
        bool bIsFixed,
        bool sigmaIsFixed,
        bool rhoIsFixed,
        bool mIsFixed,
        bool vegaWeighted = true,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    SviInterpolatedSmileSection(
        const Date& optionDate,
        const Rate& forward,
        const std::vector<Rate>& strikes,
        bool hasFloatingStrikes,
        const Volatility& atmVolatility,
        const std::vector<Volatility>& vols,
        Real a,
        Real b,
        Real sigma,
        Real rho,
        Real m,
        bool isAFixed,
        bool isBFixed,
        bool isSigmaFixed,
        bool isRhoFixed,
        bool isMFixed,
        bool vegaWeighted = true,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());

    Real a() const;
    Real b() const;
    Real sigma() const;
    Real rho() const;
    Real m() const;
    Real rmsError() const;
    Real maxError() const;
    EndCriteria::Type endCriteria() const;
};

%shared_ptr(SviSmileSection)
class SviSmileSection : public SmileSection {
  public:
    SviSmileSection(
        Time timeToExpiry,
        Rate forward,
        std::vector<Real> sviParameters);
    SviSmileSection(
        const Date& d,
        Rate forward,
        std::vector<Real> sviParameters,
        const DayCounter& dc = Actual365Fixed());
};

template<class Interpolator>
class InterpolatedSmileSection : public SmileSection {
  public:
    InterpolatedSmileSection(
        Time expiryTime,
        std::vector<Rate> strikes,
        const std::vector<Handle<Quote>>& stdDevHandles,
        Handle<Quote> atmLevel,
        const Interpolator& interpolator = Interpolator(),
        const DayCounter& dc = Actual365Fixed(),
        VolatilityType type = ShiftedLognormal,
        Real shift = 0.0);
    InterpolatedSmileSection(
        Time expiryTime,
        std::vector<Rate> strikes,
        const std::vector<Real>& stdDevs,
        Real atmLevel,
        const Interpolator& interpolator = Interpolator(),
        const DayCounter& dc = Actual365Fixed(),
        VolatilityType type = ShiftedLognormal,
        Real shift = 0.0);
    InterpolatedSmileSection(
        const Date& d,
        std::vector<Rate> strikes,
        const std::vector<Handle<Quote>>& stdDevHandles,
        Handle<Quote> atmLevel,
        const DayCounter& dc = Actual365Fixed(),
        const Interpolator& interpolator = Interpolator(),
        const Date& referenceDate = Date(),
        VolatilityType type = ShiftedLognormal,
        Real shift = 0.0);
    InterpolatedSmileSection(
        const Date& d,
        std::vector<Rate> strikes,
        const std::vector<Real>& stdDevs,
        Real atmLevel,
        const DayCounter& dc = Actual365Fixed(),
        const Interpolator& interpolator = Interpolator(),
        const Date& referenceDate = Date(),
        VolatilityType type = ShiftedLognormal,
        Real shift = 0.0);
};

%define export_smileinterpolation_curve(Name,Interpolator)
%shared_ptr(InterpolatedSmileSection<Interpolator>)
%template(Name) InterpolatedSmileSection<Interpolator>;
%enddef

export_smileinterpolation_curve(LinearInterpolatedSmileSection, Linear);
export_smileinterpolation_curve(CubicInterpolatedSmileSection, Cubic);
export_smileinterpolation_curve(MonotonicCubicInterpolatedSmileSection, MonotonicCubic);
export_smileinterpolation_curve(SplineCubicInterpolatedSmileSection, SplineCubic);

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
        const Date& optionDate, 
        const Handle<Quote>& forward,
        const std::vector<Rate>& strikes, 
        bool hasFloatingStrikes,
        const Handle<Quote>& atmVolatility,
        const std::vector<Handle<Quote>>& volHandles, 
        Real alpha, 
        Real beta,
        Real nu,
        Real rho, 
        Real gamma, 
        bool isAlphaFixed = false,
        bool isBetaFixed = false, 
        bool isNuFixed = false,
        bool isRhoFixed = false, 
        bool isGammaFixed = false,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria>& endCriteria = ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod>& method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    ZabrInterpolatedSmileSection(
        const Date& optionDate, 
        const Rate& forward,
        const std::vector<Rate>& strikes, 
        bool hasFloatingStrikes,
        const Volatility& atmVolatility, 
        const std::vector<Volatility>& vols,
        Real alpha, 
        Real beta, 
        Real nu, 
        Real rho, 
        Real gamma,
        bool isAlphaFixed = false, 
        bool isBetaFixed = false,
        bool isNuFixed = false, 
        bool isRhoFixed = false,
        bool isGammaFixed = false, 
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

%define export_zabrinterpolatedsmilesection_curve(Name,Evaluation)
%shared_ptr(ZabrInterpolatedSmileSection<Evaluation>)
%template(Name) ZabrInterpolatedSmileSection<Evaluation>;
%enddef

export_zabrinterpolatedsmilesection_curve(ZabrShortMaturityLognormalInterpolatedSmileSection, ZabrShortMaturityLognormal);
export_zabrinterpolatedsmilesection_curve(ZabrShortMaturityNormalInterpolatedSmileSection, ZabrShortMaturityNormal);
export_zabrinterpolatedsmilesection_curve(ZabrLocalVolatilityInterpolatedSmileSection, ZabrLocalVolatility);
export_zabrinterpolatedsmilesection_curve(ZabrFullFdInterpolatedSmileSection, ZabrFullFd);

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
