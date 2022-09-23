#ifndef ql_stochasticprocesses_others_all_i
#define ql_stochasticprocesses_others_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::ExtOUWithJumpsProcess;
using QuantLib::ForwardMeasureProcess;
using QuantLib::GJRGARCHProcess;
using QuantLib::G2Process;
using QuantLib::HestonProcess;
using QuantLib::HestonSLVProcess;
using QuantLib::HybridHestonHullWhiteProcess;
using QuantLib::KlugeExtOUProcess;
using QuantLib::StochasticProcessArray;
using QuantLib::LiborForwardModelProcess;
%}

%{
using QuantLib::BatesProcess;
using QuantLib::G2ForwardProcess;
%}

%shared_ptr(ExtOUWithJumpsProcess)
class ExtOUWithJumpsProcess : public StochasticProcess {
  public:
    ExtOUWithJumpsProcess(
        const ext::shared_ptr<ExtendedOrnsteinUhlenbeckProcess>& process,
        Real Y0, 
        Real beta, 
        Real jumpIntensity, 
        Real eta);
    ext::shared_ptr<ExtendedOrnsteinUhlenbeckProcess> getExtendedOrnsteinUhlenbeckProcess() const;
    Real beta() const;
    Real eta() const;
    Real jumpIntensity() const;
};

%shared_ptr(ForwardMeasureProcess)
class ForwardMeasureProcess : public StochasticProcess {
  public:
    void setForwardMeasureTime(Time);
    Time getForwardMeasureTime() const;
};

%shared_ptr(GJRGARCHProcess)
class GJRGARCHProcess : public StochasticProcess {
  public:
    enum Discretization {
        PartialTruncation,
        FullTruncation,
        Reflection
    };

    GJRGARCHProcess(
        Handle<YieldTermStructure> riskFreeRate,
        Handle<YieldTermStructure> dividendYield,
        Handle<Quote> s0,
        Real v0, 
        Real omega, 
        Real alpha,
        Real beta,
        Real gamma, 
        Real lambda, 
        Real daysPerYear = 252.0,
        Discretization d = FullTruncation);

    const Handle<Quote>& s0();
    const Handle<YieldTermStructure>& dividendYield();
    const Handle<YieldTermStructure>& riskFreeRate();
};

%shared_ptr(G2Process)
class G2Process : public StochasticProcess {
  public:
    G2Process(
        Real a, 
        Real sigma, 
        Real b,
        Real eta, 
        Real rho);
    Real x0() const;
    Real y0() const;
    Real a() const;
    Real sigma() const;
    Real b() const;
    Real eta() const;
    Real rho() const;
};

%shared_ptr(HestonProcess)
class HestonProcess : public StochasticProcess {
  public:
    enum Discretization {
        PartialTruncation,
        FullTruncation,
        Reflection,
        NonCentralChiSquareVariance,
        QuadraticExponential,
        QuadraticExponentialMartingale,
        BroadieKayaExactSchemeLobatto,
        BroadieKayaExactSchemeLaguerre,
        BroadieKayaExactSchemeTrapezoidal
    };

    HestonProcess(
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<Quote>& s0,
        Real v0, 
        Real kappa,
        Real theta, 
        Real sigma, 
        Real rho,
        Discretization d = QuadraticExponentialMartingale);

    Real v0() const;
    Real rho() const;
    Real kappa() const;
    Real theta() const;
    Real sigma() const;
    const Handle<Quote>& s0() const;
    const Handle<YieldTermStructure>& dividendYield() const;
    const Handle<YieldTermStructure>& riskFreeRate() const;
    Real pdf(Real x, Real v, Time t, Real eps = 1e-3) const;
};

%template(HestonProcessHandle) Handle<HestonProcess>;
%template(RelinkableHestonProcessHandle) RelinkableHandle<HestonProcess>;

%shared_ptr(HestonSLVProcess)
class HestonSLVProcess : public StochasticProcess {
  public:
    HestonSLVProcess(
        const ext::shared_ptr<HestonProcess>& hestonProcess,
        ext::shared_ptr<LocalVolTermStructure> leverageFct,
        const Real mixingFactor = 1.0);
    Real v0()    const;
    Real rho()   const;
    Real kappa() const;
    Real theta() const;
    Real sigma() const;
    Real mixingFactor() const;
    ext::shared_ptr<LocalVolTermStructure> leverageFct() const;
    const Handle<Quote>& s0() const;
    const Handle<YieldTermStructure>& dividendYield() const;
    const Handle<YieldTermStructure>& riskFreeRate() const;
};

%shared_ptr(HybridHestonHullWhiteProcess)
class HybridHestonHullWhiteProcess : public StochasticProcess {
  public:
    enum Discretization { Euler, BSMHullWhite };

    HybridHestonHullWhiteProcess(
      const ext::shared_ptr<HestonProcess>& hestonProcess,
      const ext::shared_ptr<HullWhiteForwardProcess>& hullWhiteProcess,
      Real corrEquityShortRate,
      Discretization discretization = BSMHullWhite);

    DiscountFactor numeraire(Time t, const Array& x) const;
    const ext::shared_ptr<HestonProcess>& hestonProcess() const;
    const ext::shared_ptr<HullWhiteForwardProcess>& hullWhiteProcess() const;
    Real eta() const;
    Discretization discretization() const;
};

%shared_ptr(KlugeExtOUProcess)
class KlugeExtOUProcess : public StochasticProcess {
  public:
    KlugeExtOUProcess(
        Real rho,
        const ext::shared_ptr<ExtOUWithJumpsProcess>& kluge,
        const ext::shared_ptr<ExtendedOrnsteinUhlenbeckProcess>& extOU);
    ext::shared_ptr<ExtOUWithJumpsProcess> getKlugeProcess() const;
    ext::shared_ptr<ExtendedOrnsteinUhlenbeckProcess> getExtOUProcess() const;
    Real rho() const;
};

%shared_ptr(StochasticProcessArray)
class StochasticProcessArray : public StochasticProcess {
  public:
    StochasticProcessArray(
        const std::vector<ext::shared_ptr<StochasticProcess1D>>&array,
        const Matrix& correlation);
    const ext::shared_ptr<StochasticProcess1D>& process(Size i) const;
    Matrix correlation() const;
};

%shared_ptr(LiborForwardModelProcess)
class LiborForwardModelProcess : public StochasticProcess {
  public:
    LiborForwardModelProcess(Size size, ext::shared_ptr<IborIndex> index);
    ext::shared_ptr<IborIndex> index() const;
    Leg cashFlows(Real amount = 1.0) const;
    void setCovarParam(
           const ext::shared_ptr<LfmCovarianceParameterization>& param);
    ext::shared_ptr<LfmCovarianceParameterization> covarParam() const;
    Size nextIndexReset(Time t) const;
    const std::vector<Time>& fixingTimes() const;
    const std::vector<Date>& fixingDates() const;
    const std::vector<Time>& accrualStartTimes() const;
    const std::vector<Time>& accrualEndTimes() const;
    std::vector<DiscountFactor> discountBond(
        const std::vector<Rate>& rates) const;
};

%shared_ptr(G2ForwardProcess)
class G2ForwardProcess : public ForwardMeasureProcess {
  public:
    G2ForwardProcess(
        Real a, Real sigma, Real b, Real eta, Real rho);
};

%shared_ptr(BatesProcess)
class BatesProcess : public HestonProcess {
    %rename(lambdaParameter) lambda;
  public:
    BatesProcess(
        const Handle<YieldTermStructure>& riskFreeRate,
        const Handle<YieldTermStructure>& dividendYield,
        const Handle<Quote>& s0,
        Real v0, 
        Real kappa,
        Real theta, 
        Real sigma, 
        Real rho,
        Real lambda, 
        Real nu, 
        Real delta);
    Real lambda() const;
    Real nu() const;
    Real delta() const;
};

#endif
