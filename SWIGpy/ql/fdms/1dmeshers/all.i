#ifndef ql_fdms_1dmeshers_all_i
#define ql_fdms_1dmeshers_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/fdms/Fdm1dMesher.i

%{
using QuantLib::Concentrating1dMesher;
using QuantLib::ExponentialJump1dMesher;
using QuantLib::FdmBlackScholesMesher;
using QuantLib::FdmCEV1dMesher;
using QuantLib::FdmHestonVarianceMesher;
using QuantLib::FdmHestonLocalVolatilityVarianceMesher;
using QuantLib::Uniform1dMesher;
using QuantLib::FdmSimpleProcess1dMesher;
using QuantLib::Predefined1dMesher;
using QuantLib::Glued1dMesher;
using QuantLib::FdmBlackScholesMultiStrikeMesher;
%}

%template(Concentrating1dMesherPoint) ext::tuple<Real, Real, bool>;
%template(Concentrating1dMesherPointVector) std::vector<ext::tuple<Real, Real, bool>>;

%shared_ptr(Concentrating1dMesher)
class Concentrating1dMesher : public Fdm1dMesher {
  public:
    Concentrating1dMesher(
        Real start, Real end, Size size,
        const std::pair<Real, Real>& cPoints = (std::pair<Real, Real>(Null<Real>(), Null<Real>())),
        const bool requireCPoint = false);

    Concentrating1dMesher(
        Real start, Real end, Size size,
        const std::vector<ext::tuple<Real, Real, bool>>& cPoints,
        Real tol = 1e-8);
};

%shared_ptr(ExponentialJump1dMesher)
class ExponentialJump1dMesher : public Fdm1dMesher {
   public:
     ExponentialJump1dMesher(
        Size steps, Real beta, Real jumpIntensity,
        Real eta, Real eps = 1e-3);
    Real jumpSizeDensity(Real x) const;
    Real jumpSizeDensity(Real x, Time t) const;
    Real jumpSizeDistribution(Real x) const;
    Real jumpSizeDistribution(Real x, Time t) const;
};

%shared_ptr(FdmBlackScholesMesher)
class FdmBlackScholesMesher : public Fdm1dMesher {
  public:
    %feature("kwargs") FdmBlackScholesMesher;
    FdmBlackScholesMesher(
        Size size,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Time maturity, Real strike,
        Real xMinConstraint = Null<Real>(),
        Real xMaxConstraint = Null<Real>(),
        Real eps = 0.0001,
        Real scaleFactor = 1.5,
        const std::pair<Real, Real>& cPoint = (std::pair<Real, Real>(Null<Real>(), Null<Real>())),
        const std::vector<ext::shared_ptr<Dividend>>& dividendSchedule = std::vector<ext::shared_ptr<Dividend>>(),
        const ext::shared_ptr<FdmQuantoHelper>& fdmQuantoHelper = ext::shared_ptr<FdmQuantoHelper>(),
        Real spotAdjustment = 0.0);

    static ext::shared_ptr<GeneralizedBlackScholesProcess> processHelper(
         const Handle<Quote>& s0,
         const Handle<YieldTermStructure>& rTS,
         const Handle<YieldTermStructure>& qTS,
         Volatility vol);
};

%shared_ptr(FdmBlackScholesMultiStrikeMesher)
class FdmBlackScholesMultiStrikeMesher : public Fdm1dMesher {
  public:
    FdmBlackScholesMultiStrikeMesher(
        Size size,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Time maturity, const std::vector<Real>& strikes,
        Real eps = 0.0001,
        Real scaleFactor = 1.5,
        const std::pair<Real, Real>& cPoint = (std::pair<Real, Real>(Null<Real>(), Null<Real>())));
};

%shared_ptr(FdmCEV1dMesher)
class FdmCEV1dMesher : public Fdm1dMesher {
  public:
    %feature("kwargs") FdmCEV1dMesher;
    FdmCEV1dMesher(
        Size size,
        Real f0, Real alpha, Real beta,
        Time maturity,
        Real eps = 0.0001,
        Real scaleFactor = 1.5,
        const std::pair<Real, Real>& cPoint = (std::pair<Real, Real>(Null<Real>(), Null<Real>())));
};

%shared_ptr(FdmHestonVarianceMesher)
class FdmHestonVarianceMesher : public Fdm1dMesher {
  public:
    FdmHestonVarianceMesher(
        Size size,
        const ext::shared_ptr<HestonProcess>& process,
        Time maturity,
        Size tAvgSteps = 10,
        Real epsilon = 0.0001,
        Real mixingFactor = 1.0);

    Real volaEstimate() const;
};

%shared_ptr(FdmHestonLocalVolatilityVarianceMesher)
class FdmHestonLocalVolatilityVarianceMesher : public Fdm1dMesher {
  public:
    FdmHestonLocalVolatilityVarianceMesher(
        Size size,
        const ext::shared_ptr<HestonProcess>& process,
        const ext::shared_ptr<LocalVolTermStructure>& leverageFct,
        Time maturity,
        Size tAvgSteps = 10,
        Real epsilon = 0.0001,
        Real mixingFactor = 1.0);

    Real volaEstimate() const;
};

%shared_ptr(FdmSimpleProcess1dMesher)
class FdmSimpleProcess1dMesher : public Fdm1dMesher {
  public:
      FdmSimpleProcess1dMesher(
        Size size,
        const ext::shared_ptr<StochasticProcess1D>& process,
        Time maturity,
        Size tAvgSteps = 10,
        Real epsilon = 0.0001,
        Real mandatoryPoint = Null<Real>());
};

%shared_ptr(Glued1dMesher)
class Glued1dMesher : public Fdm1dMesher {
  public:
    Glued1dMesher(
        const Fdm1dMesher& leftMesher,
        const Fdm1dMesher& rightMesher);
};

%shared_ptr(Predefined1dMesher)
class Predefined1dMesher : public Fdm1dMesher {
  public:
    explicit Predefined1dMesher(
        const std::vector<Real>& x);
};

%shared_ptr(Uniform1dMesher)
class Uniform1dMesher : public Fdm1dMesher {
  public:
    Uniform1dMesher(Real start, Real end, Size size);
};

#endif
