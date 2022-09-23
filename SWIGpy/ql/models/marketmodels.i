#ifndef ql_models_marketmodels_i
#define ql_models_marketmodels_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/models/curvestates.i

%{
using QuantLib::AlphaForm;
using QuantLib::AlphaFormInverseLinear;
using QuantLib::AlphaFormLinearHyperbolic;
using QuantLib::MarketModel;
using QuantLib::AbcdVol;
using QuantLib::CotSwapToFwdAdapter;
using QuantLib::FlatVol;
using QuantLib::FwdPeriodAdapter;
using QuantLib::FwdToCotSwapAdapter;
using QuantLib::PseudoRootFacade;
using QuantLib::MarketModelFactory;
using QuantLib::CotSwapToFwdAdapterFactory;
using QuantLib::FlatVolFactory;
using QuantLib::FwdToCotSwapAdapterFactory;
%}

%{
using QuantLib::PiecewiseConstantCorrelation;
using QuantLib::CotSwapFromFwdCorrelation;
using QuantLib::ExponentialForwardCorrelation;
using QuantLib::TimeHomogeneousForwardCorrelation;
using QuantLib::exponentialCorrelations;
using QuantLib::PiecewiseConstantVariance;
using QuantLib::PiecewiseConstantAbcdVariance;
using QuantLib::CTSMMCapletCalibration;
using QuantLib::CTSMMCapletAlphaFormCalibration;
using QuantLib::CTSMMCapletMaxHomogeneityCalibration;
using QuantLib::CTSMMCapletOriginalCalibration;
using QuantLib::VolatilityInterpolationSpecifier;
using QuantLib::VolatilityInterpolationSpecifierabcd;
using QuantLib::capletSwaptionPeriodicCalibration;
using QuantLib::SwapForwardMappings;
%}

%shared_ptr(AlphaForm)
class AlphaForm {
  private:
    AlphaForm();
  public:
    Real operator()(Integer i) const;
    void setAlpha(Real alpha);
};

%shared_ptr(AlphaFormInverseLinear)
class AlphaFormInverseLinear : public AlphaForm {
  public:
    AlphaFormInverseLinear(
        std::vector<Time> times, 
        Real alpha = 0.0);
};

%shared_ptr(AlphaFormLinearHyperbolic)
class AlphaFormLinearHyperbolic : public AlphaForm {
  public:
    AlphaFormLinearHyperbolic(
        std::vector<Time> times, 
        Real alpha = 0.0);
};

%shared_ptr(PiecewiseConstantCorrelation)
class PiecewiseConstantCorrelation {
  private:
    PiecewiseConstantCorrelation();
  public:
    const std::vector<Time>& times() const;
    const std::vector<Time>& rateTimes() const;
    const std::vector<Matrix>& correlations() const;
    const Matrix& correlation(Size i) const;
    Size numberOfRates() const;
};

%shared_ptr(CotSwapFromFwdCorrelation)
class CotSwapFromFwdCorrelation : public PiecewiseConstantCorrelation {
  public:
    CotSwapFromFwdCorrelation(
        const ext::shared_ptr<PiecewiseConstantCorrelation>& fwdCorr,
        const CurveState& curveState,
        Spread displacement);
};

%shared_ptr(ExponentialForwardCorrelation)
class ExponentialForwardCorrelation : public PiecewiseConstantCorrelation {
  public:
    ExponentialForwardCorrelation(
        const std::vector<Time>& rateTimes,
        Real longTermCorr = 0.5,
        Real beta = 0.2,
        Real gamma = 1.0,
        std::vector<Time> times = std::vector<Time>());
};

%shared_ptr(TimeHomogeneousForwardCorrelation)
class TimeHomogeneousForwardCorrelation : public PiecewiseConstantCorrelation {
  public:
    TimeHomogeneousForwardCorrelation(
        const Matrix& fwdCorrelation,
        const std::vector<Time>& rateTimes);
    static std::vector<Matrix> evolvedMatrices(
        const Matrix& fwdCorrelation);
};

Matrix exponentialCorrelations(
    const std::vector<Time>& rateTimes,
    Real longTermCorr = 0.5,
    Real beta = 0.2,
    Real gamma = 1.0,
    Time t = 0.0);

%shared_ptr(PiecewiseConstantVariance)
class PiecewiseConstantVariance {
  private:
    PiecewiseConstantVariance();
  public:
    const std::vector<Real>& variances() const;
    const std::vector<Volatility>& volatilities() const;
    const std::vector<Time>& rateTimes() const;
    Real variance(Size i) const;
    Volatility volatility(Size i) const;
    Real totalVariance(Size i) const;
    Volatility totalVolatility(Size i) const;
};

%template(PiecewiseConstantVarianceVector) std::vector<ext::shared_ptr<PiecewiseConstantVariance>>;

%shared_ptr(PiecewiseConstantAbcdVariance)
class PiecewiseConstantAbcdVariance : public PiecewiseConstantVariance {
  public:
    PiecewiseConstantAbcdVariance(
        Real a, 
        Real b, 
        Real c, 
        Real d,
        Size resetIndex,
        const std::vector<Time>& rateTimes);    
    %extend {
      void getABCD(
          Value& aq, Value& bq, 
          Value& cq, Value& dq) const {
          Real a, b, c, d;
          self->getABCD(a, b, c, d);
          aq.setValue(a);
          bq.setValue(b);
          cq.setValue(c);
          dq.setValue(d);
          }
    }
};

%template(PiecewiseConstantAbcdVarianceVector) std::vector<ext::shared_ptr<PiecewiseConstantAbcdVariance>>;

class CTSMMCapletCalibration {
  private:
    CTSMMCapletCalibration();
  public:
    bool calibrate(
        Natural numberOfFactors,
        Natural maxIterations,
        Real tolerance,
        Natural innerMaxIterations = 100,
        Real innerTolerance = 1e-8);
    Natural failures() const;
    Real deformationSize() const;

    Real capletRmsError() const;
    Real capletMaxError() const;
    Real swaptionRmsError() const;
    Real swaptionMaxError() const;

    const std::vector<Matrix>& swapPseudoRoots() const;
    const Matrix& swapPseudoRoot(Size i) const;

    const std::vector<Volatility>& mktCapletVols() const;
    const std::vector<Volatility>& mdlCapletVols() const;
    const std::vector<Volatility>& mktSwaptionVols() const;
    const std::vector<Volatility>& mdlSwaptionVols() const;
    const std::vector<Volatility>& timeDependentCalibratedSwaptionVols(Size i) const;
    const std::vector<Volatility>& timeDependentUnCalibratedSwaptionVols(Size i) const;

    static void performChecks(
        const EvolutionDescription& evolution,
        const PiecewiseConstantCorrelation& corr,
        const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& displacedSwapVariances,
        const std::vector<Volatility>& mktCapletVols,
        const CurveState& cs);

    const ext::shared_ptr<CurveState>& curveState() const;
    std::vector<Spread> displacements() const;
};

class CTSMMCapletAlphaFormCalibration : public CTSMMCapletCalibration {
  public:
    CTSMMCapletAlphaFormCalibration(
        const EvolutionDescription& evolution,
        const ext::shared_ptr<PiecewiseConstantCorrelation>& corr,
        const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& displacedSwapVariances,
        const std::vector<Volatility>& capletVols,
        const ext::shared_ptr<CurveState>& cs,
        Spread displacement,
        const std::vector<Real>& alphaInitial,
        const std::vector<Real>& alphaMax,
        const std::vector<Real>& alphaMin,
        bool maximizeHomogeneity,
        ext::shared_ptr<AlphaForm> parametricForm = ext::shared_ptr<AlphaForm>());

    const std::vector<Real>& alpha() const;

    static Natural capletAlphaFormCalibration(
        const EvolutionDescription& evolution,
        const PiecewiseConstantCorrelation& corr,
        const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& displacedSwapVariances,
        const std::vector<Volatility>& capletVols,
        const CurveState& cs,
        Spread displacement,
        const std::vector<Real>& alphaInitial,
        const std::vector<Real>& alphaMax,
        const std::vector<Real>& alphaMin,
        bool maximizeHomogeneity,
        const ext::shared_ptr<AlphaForm>& parametricForm,
        Size numberOfFactors,
        Integer steps,
        Real toleranceForAlphaSolving,
        std::vector<Real>& alpha,
        std::vector<Real>& a,
        std::vector<Real>& b,
        std::vector<Matrix>& swapCovariancePseudoRoots);
};

class CTSMMCapletMaxHomogeneityCalibration : public CTSMMCapletCalibration {
  public:
    CTSMMCapletMaxHomogeneityCalibration(
        const EvolutionDescription& evolution,
        const ext::shared_ptr<PiecewiseConstantCorrelation>& corr,
        const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& displacedSwapVariances,
        const std::vector<Volatility>& capletVols,
        const ext::shared_ptr<CurveState>& cs,
        Spread displacement,
        Real caplet0Swaption1Priority = 1.0);

    %extend {        
        static Natural capletMaxHomogeneityCalibration(
            const EvolutionDescription& evolution,
            const PiecewiseConstantCorrelation& corr,
            const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& displacedSwapVariances,
            const std::vector<Volatility>& capletVols,
            const CurveState& cs,
            Spread displacement,
            Real caplet0Swaption1Priority,
            Size numberOfFactors,
            Size maxIterations,
            Real tolerance,
            Value& deformationSizeq,
            Value& totalSwaptionErrorq,
            std::vector<Matrix>& swapCovariancePseudoRoots) {
                Real deformationSize, totalSwaptionError;
                Natural n;
                n = CTSMMCapletMaxHomogeneityCalibration::capletMaxHomogeneityCalibration(
                    evolution,
                    corr,
                    displacedSwapVariances,
                    capletVols,
                    cs,
                    displacement,
                    caplet0Swaption1Priority,
                    numberOfFactors,
                    maxIterations,
                    tolerance,
                    deformationSize,
                    totalSwaptionError,
                    swapCovariancePseudoRoots);
                deformationSizeq.setValue(deformationSize);
                totalSwaptionErrorq.setValue(totalSwaptionError);
                return n;
            }
    }
};

class CTSMMCapletOriginalCalibration : public CTSMMCapletCalibration {
  public:
    CTSMMCapletOriginalCalibration(
        const EvolutionDescription& evolution,
        const ext::shared_ptr<PiecewiseConstantCorrelation>& corr,
        const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& displacedSwapVariances,
        const std::vector<Volatility>& capletVols,
        const ext::shared_ptr<CurveState>& cs,
        Spread displacement,
        const std::vector<Real>& alpha,
        bool lowestRoot,
        bool useFullApprox);
    static Natural calibrationFunction(
        const EvolutionDescription& evolution,
        const PiecewiseConstantCorrelation& corr,
        const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& displacedSwapVariances,
        const std::vector<Volatility>& capletVols,
        const CurveState& cs,
        Spread displacement,
        const std::vector<Real>& alpha,
        bool lowestRoot,
        bool useFullApprox,
        Size numberOfFactors,
        std::vector<Matrix>& swapCovariancePseudoRoots);
};

class VolatilityInterpolationSpecifier {
  private:
    VolatilityInterpolationSpecifier();
  public:
    void setScalingFactors(const std::vector<Real>& scales);
    void setLastCapletVol(Real vol);
    const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& interpolatedVariances() const;
    const std::vector<ext::shared_ptr<PiecewiseConstantVariance>>& originalVariances() const;
    Size getPeriod() const;
    Size getOffset() const;
    Size getNoBigRates() const;
    Size getNoSmallRates() const;
};

class VolatilityInterpolationSpecifierabcd : public VolatilityInterpolationSpecifier {
  public:    
    %extend {
        VolatilityInterpolationSpecifierabcd(
            Size period,
            Size offset,
            const std::vector<ext::shared_ptr<PiecewiseConstantAbcdVariance>>& originalVariances,
            const std::vector<Time>& timesForSmallRates,
            Real lastCapletVol = 0.0) {
                std::vector<PiecewiseConstantAbcdVariance> ov;
                for (const auto& i : originalVariances) {
                    ov.push_back(*i);
                }
                return new VolatilityInterpolationSpecifierabcd(
                    period,
                    offset,
                    ov,
                    timesForSmallRates,
                    lastCapletVol);
            }
    }
};

%inline {
namespace QuantLib {
    Integer capletSwaptionPeriodicCalibration(
        const EvolutionDescription& evolution,
        const ext::shared_ptr<PiecewiseConstantCorrelation>& corr,
        VolatilityInterpolationSpecifier& displacedSwapVariances,
        const std::vector<Volatility>& capletVols,
        const ext::shared_ptr<CurveState>& cs,
        const Spread displacement,
        Real caplet0Swaption1Priority,
        Size numberOfFactors,
        Size period,
        Size max1dIterations,
        Real tolerance1d,
        Size maxUnperiodicIterations,
        Real toleranceUnperiodic,
        Size maxPeriodIterations,
        Real periodTolerance,
        Value& deformationSizeq, 
        Value& totalSwaptionErrorq,
        std::vector<Matrix>& swapCovariancePseudoRoots,
        std::vector<Real>& finalScales,  
        Value& iterationsDoneq, 
        Value& errorImprovementq,
        Matrix& modelSwaptionVolsMatrix) {
            Integer i;
            Real deformationSize, totalSwaptionError, errorImprovement;
            Size iterationsDone;
            i = capletSwaptionPeriodicCalibration(
                evolution,
                corr,
                displacedSwapVariances,
                capletVols,
                cs,
                displacement,
                caplet0Swaption1Priority,
                numberOfFactors,
                period,
                max1dIterations,
                tolerance1d,
                maxUnperiodicIterations,
                toleranceUnperiodic,
                maxPeriodIterations,
                periodTolerance,
                deformationSize,
                totalSwaptionError,
                swapCovariancePseudoRoots,
                finalScales,
                iterationsDone,
                errorImprovement,
                modelSwaptionVolsMatrix);
            deformationSizeq.setValue(deformationSize);
            totalSwaptionErrorq.setValue(totalSwaptionError);
            errorImprovementq.setValue(errorImprovement);
            iterationsDoneq.setValue(iterationsDone);
            return i;
        }
}    
}

%shared_ptr(MarketModel)
class MarketModel {
  private:
    MarketModel();
  public:
    const std::vector<Rate>& initialRates() const;
    const std::vector<Spread>& displacements() const;
    const EvolutionDescription& evolution() const;
    Size numberOfRates() const;
    Size numberOfFactors() const;
    Size numberOfSteps() const;
    const Matrix& pseudoRoot(Size i) const;
    const Matrix& covariance(Size i) const;
    const Matrix& totalCovariance(Size endIndex) const;
    std::vector<Volatility> timeDependentVolatility(Size i) const;
};

%shared_ptr(MarketModelFactory)
class MarketModelFactory : public Observable {
  public:
    ext::shared_ptr<MarketModel> create(
        const EvolutionDescription&,
        Size numberOfFactors) const;
};

%shared_ptr(AbcdVol)
class AbcdVol : public MarketModel {
  public:
    AbcdVol(
        Real a,
        Real b,
        Real c,
        Real d,
        const std::vector<Real>& ks,
        const ext::shared_ptr<PiecewiseConstantCorrelation>& corr,
        const EvolutionDescription& evolution,
        Size numberOfFactors,
        const std::vector<Rate>& initialRates,
        const std::vector<Spread>& displacements);
};

%shared_ptr(CotSwapToFwdAdapter)
class CotSwapToFwdAdapter : public MarketModel {
  public:
    CotSwapToFwdAdapter(
        const ext::shared_ptr<MarketModel>& coterminalModel);
};

%shared_ptr(CotSwapToFwdAdapterFactory)
class CotSwapToFwdAdapterFactory : public MarketModelFactory, public Observer {
  public:
    CotSwapToFwdAdapterFactory(
        const ext::shared_ptr<MarketModelFactory>& coterminalFactory);
};

%shared_ptr(FlatVol)
class FlatVol : public MarketModel {
  public:
    FlatVol(
        const std::vector<Volatility>& volatilities,
        const ext::shared_ptr<PiecewiseConstantCorrelation>& corr,
        const EvolutionDescription& evolution,
        Size numberOfFactors,
        const std::vector<Rate>& initialRates,
        const std::vector<Spread>& displacements);
};

%shared_ptr(FlatVolFactory)
class FlatVolFactory : public MarketModelFactory, public Observer {
  public:
    FlatVolFactory(
        Real longTermCorrelation,
        Real beta,
        std::vector<Time> times,
        std::vector<Volatility> vols,
        Handle<YieldTermStructure> yieldCurve,
        Spread displacement);
};

%shared_ptr(FwdPeriodAdapter)
class FwdPeriodAdapter : public MarketModel {
  public:
    FwdPeriodAdapter(
        const ext::shared_ptr<MarketModel>& largeModel,
        Size period,
        Size offset,
        std::vector<Spread> newDisplacements_);
};

%shared_ptr(FwdToCotSwapAdapter)
class FwdToCotSwapAdapter : public MarketModel {
  public:
    FwdToCotSwapAdapter(
        const ext::shared_ptr<MarketModel>& forwardModel);
};

%shared_ptr(FwdToCotSwapAdapterFactory)
class FwdToCotSwapAdapterFactory : public MarketModelFactory, public Observer {
  public:
    FwdToCotSwapAdapterFactory(
          const ext::shared_ptr<MarketModelFactory>& forwardFactory);
};

%shared_ptr(PseudoRootFacade)
class PseudoRootFacade : public MarketModel {
  public:
    PseudoRootFacade(
        const ext::shared_ptr<CTSMMCapletCalibration>& calibrator);
    PseudoRootFacade(
        const std::vector<Matrix>& covariancePseudoRoots,
        const std::vector<Rate>& rateTimes,
        std::vector<Rate> initialRates,
        const std::vector<Spread>& displacements);
};

class SwapForwardMappings {
  public:
    static Real annuity(const CurveState& cs,
                        Size startIndex,
                        Size endIndex,
                        Size numeraireIndex);
    static Real swapDerivative(const CurveState& cs,
                               Size startIndex,
                               Size endIndex,
                               Size forwardIndex);
    static Matrix coterminalSwapForwardJacobian(const CurveState& cs);
    static Matrix coterminalSwapZedMatrix(
        const CurveState& cs, Spread displacement);
    static Matrix coinitialSwapForwardJacobian(const CurveState& cs);
    static Matrix coinitialSwapZedMatrix(
      const CurveState& cs, Spread displacement);
    static Matrix cmSwapForwardJacobian(
      const CurveState& cs, Size spanningForwards);
    static Matrix cmSwapZedMatrix(
      const CurveState& cs, Size spanningForwards, Spread displacement);
    static Real swaptionImpliedVolatility(
        const MarketModel& volStructure, Size startIndex, Size endIndex);

};


#endif
