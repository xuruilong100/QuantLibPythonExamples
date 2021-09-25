#ifndef ql_slv_i
#define ql_slv_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::BrownianGenerator;
using QuantLib::MTBrownianGenerator;
using QuantLib::SobolBrownianGenerator;
using QuantLib::BrownianGeneratorFactory;
using QuantLib::MTBrownianGeneratorFactory;
using QuantLib::SobolBrownianGeneratorFactory;
using QuantLib::HestonSLVMCModel;
using QuantLib::HestonSLVFDMModel;
using QuantLib::HestonSLVFokkerPlanckFdmParams;
%}

class BrownianGenerator {
  private:
    BrownianGenerator();
  public:
    Real nextStep(std::vector<Real>&);
    Real nextPath();
    Size numberOfFactors() const;
    Size numberOfSteps() const;
};

class MTBrownianGenerator : public BrownianGenerator {
  public:
    MTBrownianGenerator(
        Size factors,
        Size steps,
        unsigned long seed = 0);
};

class SobolBrownianGenerator : public BrownianGenerator {
  public:
    enum Ordering {
        Factors,
        Steps,
        Diagonal
    };
    SobolBrownianGenerator(
        Size factors,
        Size steps,
        Ordering ordering,
        unsigned long seed = 0,
        SobolRsg::DirectionIntegers directionIntegers = SobolRsg::Jaeckel);
    // test interface
    const std::vector<std::vector<Size>>& orderedIndices() const;
    std::vector<std::vector<Real>> transform(
        const std::vector<std::vector<Real>>& variates);
};

%shared_ptr(BrownianGeneratorFactory);
class BrownianGeneratorFactory {
  private:
    BrownianGeneratorFactory();
  public:
    ext::shared_ptr<BrownianGenerator> create(
        Size factors, Size steps);
};

%shared_ptr(MTBrownianGeneratorFactory);
class MTBrownianGeneratorFactory : public BrownianGeneratorFactory {
  public:
    MTBrownianGeneratorFactory(unsigned long seed = 0);
};

%shared_ptr(SobolBrownianGeneratorFactory);
class SobolBrownianGeneratorFactory : public BrownianGeneratorFactory {
  public:
    SobolBrownianGeneratorFactory(
            SobolBrownianGenerator::Ordering ordering,
            unsigned long seed = 0,
            SobolRsg::DirectionIntegers directionIntegers = SobolRsg::Jaeckel);
};

%shared_ptr(HestonSLVMCModel)
class HestonSLVMCModel : public LazyObject {
  public:
    HestonSLVMCModel(
        const Handle<LocalVolTermStructure>& localVol,
        const Handle<HestonModel>& hestonModel,
        const ext::shared_ptr<BrownianGeneratorFactory>& brownianGeneratorFactory,
        const Date& endDate,
        Size timeStepsPerYear = 365,
        Size nBins = 201,
        Size calibrationPaths = (1 << 15),
        const std::vector<Date>& mandatoryDates = std::vector<Date>(),
        Real mixingFactor = 1.0);
    ext::shared_ptr<HestonProcess> hestonProcess() const;
    ext::shared_ptr<LocalVolTermStructure> localVol() const;
    ext::shared_ptr<LocalVolTermStructure> leverageFunction() const;
};

class HestonSLVFokkerPlanckFdmParams {
  public:
    %extend {
        HestonSLVFokkerPlanckFdmParams(
            Size xGrid, Size vGrid,
            Size tMaxStepsPerYear, Size tMinStepsPerYear,
            Real tStepNumberDecay,
            Size nRannacherTimeSteps,
            Size predictionCorretionSteps,
            Real x0Density, Real localVolEpsProb,
            Size maxIntegrationIterations,
            Real vLowerEps, Real vUpperEps, Real vMin,
            Real v0Density, Real vLowerBoundDensity, Real vUpperBoundDensity,
            Real leverageFctPropEps,
            FdmHestonGreensFct::Algorithm greensAlgorithm,
            FdmSquareRootFwdOp::TransformationType trafoType,
            FdmSchemeDesc schemeDesc) {

                const HestonSLVFokkerPlanckFdmParams params = {
                    xGrid, vGrid,
                    tMaxStepsPerYear, tMinStepsPerYear,
                    tStepNumberDecay,
                    nRannacherTimeSteps,
                    predictionCorretionSteps,
                    x0Density,
                    localVolEpsProb,
                    maxIntegrationIterations,
                    vLowerEps,
                    vUpperEps,
                    vMin,
                    v0Density,
                    vLowerBoundDensity,
                    vUpperBoundDensity,
                    leverageFctPropEps,
                    greensAlgorithm,
                    trafoType,
                    schemeDesc };

                return new HestonSLVFokkerPlanckFdmParams(params);
        }
    }
};

%{
struct LogEntryStruct {
    Time t;
    Array prob;
    ext::shared_ptr<FdmMesherComposite> mesher;
};
%}

struct LogEntryStruct {
    Time t;
    Array prob;
    ext::shared_ptr<FdmMesherComposite> mesher;
};

%shared_ptr(HestonSLVFDMModel)
class HestonSLVFDMModel : public LazyObject {
  public:
    HestonSLVFDMModel(
        const Handle<LocalVolTermStructure>& localVol,
        const Handle<HestonModel>& hestonModel,
        const Date& endDate,
        const HestonSLVFokkerPlanckFdmParams& params,
        bool logging = false,
        const std::vector<Date>& mandatoryDates = std::vector<Date>(),
        Real mixingFactor = 1.0);

    ext::shared_ptr<HestonProcess> hestonProcess() const;
    ext::shared_ptr<LocalVolTermStructure> localVol() const;
    ext::shared_ptr<LocalVolTermStructure> leverageFunction() const;

    %extend {
        std::vector<LogEntryStruct> logEntryVector() const {
            const std::list<HestonSLVFDMModel::LogEntry>& logEntries = self->logEntries();
            std::vector<LogEntryStruct> logEntryVector;
            for (std::list<HestonSLVFDMModel::LogEntry>::const_iterator i = logEntries.begin();
                 i != logEntries.end();
                 ++i) {
                LogEntryStruct logEntryStruct = {
                    i->t, *(i->prob), i->mesher};
                logEntryVector.push_back(logEntryStruct);
            }
            return logEntryVector;
        }
    }
};

%template(LogEntryVector) std::vector<LogEntryStruct>;

#endif
