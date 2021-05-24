#ifndef ql_RiskNeutralDensityCalculator_i
#define ql_RiskNeutralDensityCalculator_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::RiskNeutralDensityCalculator;
using QuantLib::BSMRNDCalculator;
using QuantLib::CEVRNDCalculator;
using QuantLib::GBSMRNDCalculator;
using QuantLib::HestonRNDCalculator;
using QuantLib::LocalVolRNDCalculator;
using QuantLib::SquareRootProcessRNDCalculator;
%}

%shared_ptr(RiskNeutralDensityCalculator)
class RiskNeutralDensityCalculator {
  public:
    virtual Real pdf(Real x, Time t) const;
    virtual Real cdf(Real x, Time t) const;
    virtual Real invcdf(Real p, Time t) const;

  private:
    RiskNeutralDensityCalculator();
};

%shared_ptr(BSMRNDCalculator)
class BSMRNDCalculator : public RiskNeutralDensityCalculator {
  public:
    explicit BSMRNDCalculator(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(CEVRNDCalculator)
class CEVRNDCalculator : public RiskNeutralDensityCalculator {
  public:
    CEVRNDCalculator(Real f0, Real alpha, Real beta);

    Real massAtZero(Time t) const;
};

%shared_ptr(GBSMRNDCalculator)
class GBSMRNDCalculator : public RiskNeutralDensityCalculator {
public:
    explicit GBSMRNDCalculator(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(HestonRNDCalculator)
class HestonRNDCalculator : public RiskNeutralDensityCalculator {
public:
    HestonRNDCalculator(
        const ext::shared_ptr<HestonProcess>& hestonProcess,
        Real integrationEps= 1e-6,
        Size maxIntegrationIterations = 10000ul);
};

%shared_ptr(LocalVolRNDCalculator)
class LocalVolRNDCalculator : public RiskNeutralDensityCalculator {
    %feature("kwargs") LocalVolRNDCalculator;
  public:
    LocalVolRNDCalculator(
        const ext::shared_ptr<Quote>& spot,
        const ext::shared_ptr<YieldTermStructure>& rTS,
        const ext::shared_ptr<YieldTermStructure>& qTS,
        const ext::shared_ptr<LocalVolTermStructure>& localVol,
        Size xGrid = 101, Size tGrid = 51,
        Real x0Density = 0.1,
        Real localVolProbEps = 1e-6,
        Size maxIter = 10000,
        Time gaussianStepSize = -Null<Time>());

    ext::shared_ptr<Fdm1dMesher> mesher(Time t) const;
    %extend {
        std::vector<unsigned int> rescaleTimeSteps() const {
            return to_vector<unsigned int>($self->rescaleTimeSteps());
        }
    }
};

%shared_ptr(SquareRootProcessRNDCalculator)
class SquareRootProcessRNDCalculator : public RiskNeutralDensityCalculator {
  public:
    SquareRootProcessRNDCalculator(
        Real v0, Real kappa, Real theta, Real sigma);

    Real stationary_pdf(Real v) const;
    Real stationary_cdf(Real v) const;
    Real stationary_invcdf(Real q) const;
};

#endif
