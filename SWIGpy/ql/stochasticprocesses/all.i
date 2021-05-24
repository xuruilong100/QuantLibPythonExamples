#ifndef ql_stochasticprocesses_all_i
#define ql_stochasticprocesses_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::StochasticProcess1D;
using QuantLib::StochasticProcessArray;
using QuantLib::HestonProcess;
using QuantLib::G2Process;
using QuantLib::G2ForwardProcess;
using QuantLib::ExtOUWithJumpsProcess;
using QuantLib::KlugeExtOUProcess;
using QuantLib::GJRGARCHProcess;
using QuantLib::HestonSLVProcess;
using QuantLib::GeneralizedBlackScholesProcess;
using QuantLib::Merton76Process;
using QuantLib::GeometricBrownianMotionProcess;
using QuantLib::VarianceGammaProcess;
using QuantLib::HullWhiteProcess;
using QuantLib::HullWhiteForwardProcess;
using QuantLib::GsrProcess;
using QuantLib::OrnsteinUhlenbeckProcess;
using QuantLib::ExtendedOrnsteinUhlenbeckProcess;
using QuantLib::BlackScholesProcess;
using QuantLib::BlackScholesMertonProcess;
using QuantLib::BlackProcess;
using QuantLib::GarmanKohlagenProcess;
using QuantLib::BatesProcess;
%}

%shared_ptr(StochasticProcess1D)
class StochasticProcess1D : public StochasticProcess {
  public:
      Real x0() const;
      Real drift(Time t, Real x) const;
      Real diffusion(Time t, Real x) const;
      Real expectation(Time t0, Real x0, Time dt) const;
      Real stdDeviation(Time t0, Real x0, Time dt) const;
      Real variance(Time t0, Real x0, Time dt) const;
      Real evolve(Time t0, Real x0, Time dt, Real dw) const;
      Real apply(Real x0, Real dx) const;
};

%template(StochasticProcess1DVector) std::vector<ext::shared_ptr<StochasticProcess1D> >;

%shared_ptr(StochasticProcessArray)
class StochasticProcessArray : public StochasticProcess {
  public:
    StochasticProcessArray(
        const std::vector<ext::shared_ptr<StochasticProcess1D> >&array,
        const Matrix &correlation);
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
        Real v0, Real kappa,
        Real theta, Real sigma, Real rho,
        Discretization d = QuadraticExponentialMartingale);

    Handle<Quote> s0();
    Handle<YieldTermStructure> dividendYield();
    Handle<YieldTermStructure> riskFreeRate();
};

%shared_ptr(G2Process)
class G2Process : public StochasticProcess {
  public:
    G2Process(
        Real a, Real sigma, Real b,
        Real eta, Real rho);
};

%shared_ptr(G2ForwardProcess)
class G2ForwardProcess : public StochasticProcess {
  public:
    G2ForwardProcess(
        Real a, Real sigma, Real b, Real eta, Real rho);
    void setForwardMeasureTime(Time t);
};

%shared_ptr(ExtOUWithJumpsProcess)
class ExtOUWithJumpsProcess : public StochasticProcess {
  public:
    ExtOUWithJumpsProcess(
        const ext::shared_ptr<ExtendedOrnsteinUhlenbeckProcess>& process,
        Real Y0, Real beta, Real jumpIntensity, Real eta);/* {

		return new ExtOUWithJumpsProcess(
			new ExtOUWithJumpsProcess(
				process, Y0, beta, jumpIntensity, eta));
    }*/
};

%shared_ptr(KlugeExtOUProcess)
class KlugeExtOUProcess : public StochasticProcess {
  public:
    KlugeExtOUProcess(
        Real rho,
        const ext::shared_ptr<ExtOUWithJumpsProcess>& kluge,
        const ext::shared_ptr<ExtendedOrnsteinUhlenbeckProcess>& extOU);/* {

        return new KlugeExtOUProcess(new KlugeExtOUProcess(
        	rho, kluge, extOU));
    }*/
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
        const Handle<YieldTermStructure>& riskFreeRate,
        const Handle<YieldTermStructure>& dividendYield,
        const Handle<Quote>& s0,
        Real v0, Real omega, Real alpha, Real beta,
        Real gamma, Real lambda, Real daysPerYear = 252.0,
        Discretization d = FullTruncation);

    Handle<Quote> s0();
    Handle<YieldTermStructure> dividendYield();
    Handle<YieldTermStructure> riskFreeRate();
};

%shared_ptr(HestonSLVProcess);
class HestonSLVProcess : public StochasticProcess {
  public:
    HestonSLVProcess(const ext::shared_ptr<HestonProcess>& hestonProcess,
                     const ext::shared_ptr<LocalVolTermStructure>& leverageFct,
                     const Real mixingFactor = 1.0);
};

%shared_ptr(GeneralizedBlackScholesProcess)
class GeneralizedBlackScholesProcess : public StochasticProcess1D {
  public:
    GeneralizedBlackScholesProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& volTS);

    GeneralizedBlackScholesProcess(
        const Handle<Quote>& x0,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& blackVolTS,
        const Handle<LocalVolTermStructure>& localVolTS);

    Handle<Quote> stateVariable();
    Handle<YieldTermStructure> dividendYield();
    Handle<YieldTermStructure> riskFreeRate();
    Handle<BlackVolTermStructure> blackVolatility();
    Handle<LocalVolTermStructure> localVolatility();
};

%shared_ptr(Merton76Process)
class Merton76Process : public StochasticProcess1D {
  public:
    Merton76Process(
        const Handle<Quote>& stateVariable,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& volTS,
        const Handle<Quote>& jumpIntensity,
        const Handle<Quote>& meanLogJump,
        const Handle<Quote>& jumpVolatility);
};

%shared_ptr(GeometricBrownianMotionProcess)
class GeometricBrownianMotionProcess : public StochasticProcess1D {
  public:
    GeometricBrownianMotionProcess(
        Real initialValue,
        Real mu,
        Real sigma);
};

%shared_ptr(VarianceGammaProcess)
class VarianceGammaProcess : public StochasticProcess1D {
  public:
    VarianceGammaProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& dividendYield,
        const Handle<YieldTermStructure>& riskFreeRate,
        Real sigma, Real nu, Real theta);
};

%shared_ptr(HullWhiteProcess)
class HullWhiteProcess : public StochasticProcess1D {
  public:
    HullWhiteProcess(
        const Handle<YieldTermStructure>& riskFreeTS,
        Real a, Real sigma);
};

%shared_ptr(HullWhiteForwardProcess)
class HullWhiteForwardProcess : public StochasticProcess1D {
  public:
    HullWhiteForwardProcess(
        const Handle<YieldTermStructure>& riskFreeTS,
        Real a,
        Real sigma);
    Real alpha(Time t) const;
    Real M_T(Real s, Real t, Real T) const;
    Real B(Time t, Time T) const;
    void setForwardMeasureTime(Time t);
};

%shared_ptr(GsrProcess)
class GsrProcess : public StochasticProcess1D {
    public:
    GsrProcess(
        const Array &times, const Array &vols,
        const Array &reversions, const Real T = 60.0);
    Real sigma(Time t);
    Real reversion(Time t);
    Real y(Time t);
    Real G(Time t, Time T, Real x);
    void setForwardMeasureTime(Time t);
};

%inline %{
    const ext::shared_ptr<GsrProcess> as_gsr_process(
        const ext::shared_ptr<StochasticProcess>& proc) {
        return ext::dynamic_pointer_cast<GsrProcess>(proc);
    }
%}

%shared_ptr(OrnsteinUhlenbeckProcess)
class OrnsteinUhlenbeckProcess : public StochasticProcess1D {
  public:
    OrnsteinUhlenbeckProcess(
    	Real speed, Volatility vol,
        Real x0 = 0.0, Real level = 0.0);

    Real speed() const;
    Real volatility() const;
    Real level() const;
};

%shared_ptr(ExtendedOrnsteinUhlenbeckProcess)
class ExtendedOrnsteinUhlenbeckProcess : public StochasticProcess1D {
  public:
    enum Discretization {
        MidPoint,
        Trapezodial,
        GaussLobatto
    };

    ExtendedOrnsteinUhlenbeckProcess(
        Real speed, Volatility sigma, Real x0,
        const ext::function<Real(Real)>& b,
        Discretization discretization = MidPoint,
        Real intEps = 1e-4);
    %extend {

        ExtendedOrnsteinUhlenbeckProcess(
            Real speed, Volatility sigma, Real x0,
            PyObject * function,
            Real intEps = 1e-4) {

            const UnaryFunction f(function);
            return new ExtendedOrnsteinUhlenbeckProcess(
                speed, sigma, x0, f,
                ExtendedOrnsteinUhlenbeckProcess::MidPoint,
                intEps);
        }
    }
};

%shared_ptr(BlackScholesProcess)
class BlackScholesProcess : public GeneralizedBlackScholesProcess {
  public:
    BlackScholesProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& volTS);
};

%shared_ptr(BlackScholesMertonProcess)
class BlackScholesMertonProcess : public GeneralizedBlackScholesProcess {
  public:
    BlackScholesMertonProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& volTS);
};

%shared_ptr(BlackProcess)
class BlackProcess : public GeneralizedBlackScholesProcess {
  public:
    BlackProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& volTS);
};

%shared_ptr(GarmanKohlagenProcess)
class GarmanKohlagenProcess : public GeneralizedBlackScholesProcess {
  public:
    GarmanKohlagenProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& foreignRiskFreeTS,
        const Handle<YieldTermStructure>& domesticRiskFreeTS,
        const Handle<BlackVolTermStructure>& volTS);
};

%shared_ptr(BatesProcess)
class BatesProcess : public HestonProcess {
  public:
    BatesProcess(
        const Handle<YieldTermStructure>& riskFreeRate,
        const Handle<YieldTermStructure>& dividendYield,
        const Handle<Quote>& s0,
        Real v0, Real kappa,
        Real theta, Real sigma, Real rho,
        Real lambda, Real nu, Real delta);
};

#endif
