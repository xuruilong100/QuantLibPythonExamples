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
  private:
    RiskNeutralDensityCalculator();
  public:
    Real pdf(Real x, Time t) const;
    Real cdf(Real x, Time t) const;
    Real invcdf(Real p, Time t) const;
};

%shared_ptr(BSMRNDCalculator)
class BSMRNDCalculator : public RiskNeutralDensityCalculator {
  public:
    explicit BSMRNDCalculator(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
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
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(HestonRNDCalculator)
class HestonRNDCalculator : public RiskNeutralDensityCalculator {
public:
    HestonRNDCalculator(
        ext::shared_ptr<HestonProcess> hestonProcess,
        Real integrationEps= 1e-6,
        Size maxIntegrationIterations = 10000ul);
};

%shared_ptr(LocalVolRNDCalculator)
class LocalVolRNDCalculator : public RiskNeutralDensityCalculator {
  public:
    LocalVolRNDCalculator(
        ext::shared_ptr<Quote> spot,
        ext::shared_ptr<YieldTermStructure> rTS,
        ext::shared_ptr<YieldTermStructure> qTS,
        const ext::shared_ptr<LocalVolTermStructure>& localVol,
        Size xGrid = 101,
        Size tGrid = 51,
        Real x0Density = 0.1,
        Real localVolProbEps = 1e-6,
        Size maxIter = 10000,
        Time gaussianStepSize = -Null<Time>());
    %extend {
        LocalVolRNDCalculator(
            ext::shared_ptr<Quote> spot,
            ext::shared_ptr<YieldTermStructure> rTS,
            ext::shared_ptr<YieldTermStructure> qTS,
            ext::shared_ptr<LocalVolTermStructure> localVol,
            TimeGrid& timeGrid,
            Size xGrid = 101,
            Real x0Density = 0.1,
            Real eps = 1e-6,
            Size maxIter = 10000,
            Time gaussianStepSize = -Null<Time>()) {
                ext::shared_ptr<TimeGrid> ptr(&timeGrid);
                return new LocalVolRNDCalculator(
                    spot, rTS, qTS, localVol, ptr,
                    xGrid, x0Density, eps, maxIter,
                    gaussianStepSize);
            }
            const TimeGrid& timeGrid() const {
                return *(self->timeGrid());
            }
    }

    //ext::shared_ptr<TimeGrid> timeGrid() const;
    ext::shared_ptr<Fdm1dMesher> mesher(Time t) const;
    std::vector<Size> rescaleTimeSteps() const;
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
