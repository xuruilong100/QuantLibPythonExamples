#ifndef ql_stochasticprocesses_1d_all_i
#define ql_stochasticprocesses_1d_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/stochasticprocesses/StochasticProcess1D.i

%{
using QuantLib::CoxIngersollRossProcess;
using QuantLib::ExtendedOrnsteinUhlenbeckProcess;
using QuantLib::ForwardMeasureProcess1D;
using QuantLib::GemanRoncoroniProcess;
using QuantLib::GeneralizedOrnsteinUhlenbeckProcess;
using QuantLib::GeometricBrownianMotionProcess;
using QuantLib::GeneralizedBlackScholesProcess;
using QuantLib::HullWhiteProcess;
using QuantLib::Merton76Process;
using QuantLib::MfStateProcess;
using QuantLib::OrnsteinUhlenbeckProcess;
using QuantLib::SquareRootProcess;
using QuantLib::VarianceGammaProcess;
%}
%{
using QuantLib::GsrProcess;
using QuantLib::HullWhiteForwardProcess;
using QuantLib::BlackScholesProcess;
using QuantLib::BlackScholesMertonProcess;
using QuantLib::BlackProcess;
using QuantLib::GarmanKohlagenProcess;
using QuantLib::VegaStressedBlackScholesProcess;
using QuantLib::ExtendedBlackScholesMertonProcess;
%}

%shared_ptr(CoxIngersollRossProcess)
class CoxIngersollRossProcess : public StochasticProcess1D {
  public:
    CoxIngersollRossProcess(
        Real speed,
        Volatility vol,
        Real x0 = 0.0,
        Real level = 0.0);
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
    %extend {
        ExtendedOrnsteinUhlenbeckProcess(
            Real speed, 
            Volatility sigma, 
            Real x0,
            PyObject * function,
            Discretization discretization = MidPoint,
            Real intEps = 1e-4) {
            const UnaryFunction f(function);
            return new ExtendedOrnsteinUhlenbeckProcess(
                speed, sigma, x0, f,
                discretization,
                intEps);
        }
    }
};

%shared_ptr(ForwardMeasureProcess1D)
class ForwardMeasureProcess1D : public StochasticProcess1D {
  public:
    void setForwardMeasureTime(Time);
    Time getForwardMeasureTime() const;
};

%shared_ptr(GemanRoncoroniProcess)
class GemanRoncoroniProcess : public StochasticProcess1D {
  public:
    GemanRoncoroniProcess(
        Real x0,
        Real alpha, 
        Real beta,
        Real gamma, 
        Real delta,
        Real eps, 
        Real zeta, 
        Real d,
        Real k, 
        Real tau,
        Real sig2, 
        Real a, 
        Real b,
        Real theta1,
        Real theta2, 
        Real theta3,
        Real psi);
    Real evolve(
        Time t0, Real x0, Time dt, Real dw, const Array& du) const;
};

%shared_ptr(GeometricBrownianMotionProcess)
class GeometricBrownianMotionProcess : public StochasticProcess1D {
  public:
    GeometricBrownianMotionProcess(
        Real initialValue,
        Real mu,
        Real sigma);
};

%shared_ptr(GeneralizedBlackScholesProcess)
class GeneralizedBlackScholesProcess : public StochasticProcess1D {
  public:
    GeneralizedBlackScholesProcess(
        Handle<Quote> x0,
        Handle<YieldTermStructure> dividendTS,
        Handle<YieldTermStructure> riskFreeTS,
        Handle<BlackVolTermStructure> blackVolTS,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization),
        bool forceDiscretization = false);
  GeneralizedBlackScholesProcess(
        Handle<Quote> x0,
        Handle<YieldTermStructure> dividendTS,
        Handle<YieldTermStructure> riskFreeTS,
        Handle<BlackVolTermStructure> blackVolTS,
        Handle<LocalVolTermStructure> localVolTS);

    const Handle<Quote>& stateVariable();
    const Handle<YieldTermStructure>& dividendYield();
    const Handle<YieldTermStructure>& riskFreeRate();
    const Handle<BlackVolTermStructure>& blackVolatility();
    const Handle<LocalVolTermStructure>& localVolatility();
};

%shared_ptr(GeneralizedOrnsteinUhlenbeckProcess)
class GeneralizedOrnsteinUhlenbeckProcess : public StochasticProcess1D {
  public:
    %extend {
        GeneralizedOrnsteinUhlenbeckProcess(
            PyObject * speed,
            PyObject * vol,
            Real x0 = 0.0,
            Real level = 0.0) {
            const ext::function<Real(Real)> s = UnaryFunction(speed);
            const ext::function<Real(Real)> v = UnaryFunction(vol);
            return new GeneralizedOrnsteinUhlenbeckProcess(
                s, v, x0, level);
        }
    }
    Real speed(Time t) const;
    Real volatility(Time t) const;
    Real level() const;
};

%shared_ptr(HullWhiteProcess)
class HullWhiteProcess : public StochasticProcess1D {
  public:
    HullWhiteProcess(
        const Handle<YieldTermStructure>& riskFreeTS,
        Real a, 
        Real sigma);
    Real a() const;
    Real sigma() const;
    Real alpha(Time t) const;
};

%shared_ptr(Merton76Process)
class Merton76Process : public StochasticProcess1D {
  public:
    Merton76Process(
        const Handle<Quote>& stateVariable,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& blackVolTS,
        Handle<Quote> jumpInt,
        Handle<Quote> logJMean,
        Handle<Quote> logJVol,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization));

    const Handle<Quote>& stateVariable() const;
    const Handle<YieldTermStructure>& dividendYield() const;
    const Handle<YieldTermStructure>& riskFreeRate() const;
    const Handle<BlackVolTermStructure>& blackVolatility() const;
    const Handle<Quote>& jumpIntensity() const;
    const Handle<Quote>& logMeanJump() const;
    const Handle<Quote>& logJumpVolatility() const;
};

%shared_ptr(MfStateProcess)
class MfStateProcess : public StochasticProcess1D {
  public:
    MfStateProcess(
        Real reversion,
        const Array& times,
        const Array& vols);
};

%shared_ptr(OrnsteinUhlenbeckProcess)
class OrnsteinUhlenbeckProcess : public StochasticProcess1D {
  public:
    OrnsteinUhlenbeckProcess(
    	  Real speed, 
        Volatility vol,
        Real x0 = 0.0, 
        Real level = 0.0);

    Real speed() const;
    Real volatility() const;
    Real level() const;
};

%shared_ptr(SquareRootProcess)
class SquareRootProcess : public StochasticProcess1D {
  public:
    SquareRootProcess(
        Real b,
        Real a,
        Volatility sigma,
        Real x0 = 0.0,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization));

    Real a() const;
    Real b() const;
    Real sigma() const;
};

%shared_ptr(VarianceGammaProcess)
class VarianceGammaProcess : public StochasticProcess1D {
  public:
    VarianceGammaProcess(
        Handle<Quote> s0,
        Handle<YieldTermStructure> dividendYield,
        Handle<YieldTermStructure> riskFreeRate,
        Real sigma, 
        Real nu, 
        Real theta);
    Real sigma() const;
    Real nu() const;
    Real theta() const;
    const Handle<Quote>& s0() const;
    const Handle<YieldTermStructure>& dividendYield() const;
    const Handle<YieldTermStructure>& riskFreeRate() const;
};

%shared_ptr(GsrProcess)
class GsrProcess : public ForwardMeasureProcess1D {
  public:
    GsrProcess(
        const Array& times, 
        const Array& vols,
        const Array& reversions, 
        const Real T = 60.0);
    Real sigma(Time t);
    Real reversion(Time t);
    Real y(Time t);
    Real G(Time t, Time T, Real x);
};

%inline %{
    const ext::shared_ptr<GsrProcess> as_gsr_process(
        const ext::shared_ptr<StochasticProcess>& proc) {
        return ext::dynamic_pointer_cast<GsrProcess>(proc);
    }
%}

%shared_ptr(HullWhiteForwardProcess)
class HullWhiteForwardProcess : public ForwardMeasureProcess1D {
  public:
    HullWhiteForwardProcess(
        const Handle<YieldTermStructure>& riskFreeTS,
        Real a,
        Real sigma);
    Real a() const;
    Real sigma() const;
    Real alpha(Time t) const;
    Real M_T(Real s, Real t, Real T) const;
    Real B(Time t, Time T) const;
};

%shared_ptr(BlackScholesProcess)
class BlackScholesProcess : public GeneralizedBlackScholesProcess {
  public:
    BlackScholesProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& blackVolTS,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization),
        bool forceDiscretization = false);
};

%shared_ptr(BlackScholesMertonProcess)
class BlackScholesMertonProcess : public GeneralizedBlackScholesProcess {
  public:
    BlackScholesMertonProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& blackVolTS,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization),
        bool forceDiscretization = false);
};

%shared_ptr(BlackProcess)
class BlackProcess : public GeneralizedBlackScholesProcess {
  public:
    BlackProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& blackVolTS,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization),
        bool forceDiscretization = false);
};

%shared_ptr(GarmanKohlagenProcess)
class GarmanKohlagenProcess : public GeneralizedBlackScholesProcess {
  public:
    GarmanKohlagenProcess(
        const Handle<Quote>& s0,
        const Handle<YieldTermStructure>& foreignRiskFreeTS,
        const Handle<YieldTermStructure>& domesticRiskFreeTS,
        const Handle<BlackVolTermStructure>& blackVolTS,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization),
        bool forceDiscretization = false);
};

%shared_ptr(VegaStressedBlackScholesProcess)
class VegaStressedBlackScholesProcess : public GeneralizedBlackScholesProcess {
  public:
    VegaStressedBlackScholesProcess(
        const Handle<Quote>& x0,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& blackVolTS,
        Time lowerTimeBorderForStressTest = 0,
        Time upperTimeBorderForStressTest = 1000000,
        Real lowerAssetBorderForStressTest = 0,
        Real upperAssetBorderForStressTest = 1000000,
        Real stressLevel = 0,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization));

    Real getLowerTimeBorderForStressTest() const;
    void setLowerTimeBorderForStressTest(Time LTB);
    Real getUpperTimeBorderForStressTest() const;
    void setUpperTimeBorderForStressTest(Time UTB);
    Real getLowerAssetBorderForStressTest() const;
    void setLowerAssetBorderForStressTest(Real LAB);
    Real getUpperAssetBorderForStressTest() const;
    void setUpperAssetBorderForStressTest(Real UBA);
    Real getStressLevel() const;
    void setStressLevel(Real SL);
};

%shared_ptr(ExtendedBlackScholesMertonProcess)
class ExtendedBlackScholesMertonProcess : public GeneralizedBlackScholesProcess {
  public:
    enum Discretization {
        Euler,
        Milstein,
        PredictorCorrector };
    ExtendedBlackScholesMertonProcess(
        const Handle<Quote>& x0,
        const Handle<YieldTermStructure>& dividendTS,
        const Handle<YieldTermStructure>& riskFreeTS,
        const Handle<BlackVolTermStructure>& blackVolTS,
        const ext::shared_ptr<discretization1D>& d = ext::shared_ptr<discretization1D>(new EulerDiscretization),
        Discretization evolDisc = Milstein);
};

#endif
