#ifndef ql_slv_i
#define ql_slv_i

%include stl.i
%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

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

class HestonSLVMCModel {
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


/*
class HestonSLVFDMModel {
  public:
    %extend {
        HestonSLVFDMModel(
            const ext::shared_ptr<LocalVolTermStructure>& localVol,
            const ext::shared_ptr<HestonModel>& model,
            const Date& endDate,
            const HestonSLVFokkerPlanckFdmParams& params,
            const bool logging = false,
            const std::vector<Date>& mandatoryDates = std::vector<Date>(),
            Real mixingFactor = 1.0) {
            return new HestonSLVFDMModel(
                Handle<LocalVolTermStructure>(localVol), Handle<HestonModel>(model),
                endDate, params, logging, mandatoryDates, mixingFactor);
        }
    }
    ext::shared_ptr<HestonProcess> hestonProcess() const;
    ext::shared_ptr<LocalVolTermStructure> localVol() const;
    ext::shared_ptr<LocalVolTermStructure> leverageFunction() const;
};
*/

%rename (HestonSLVFDMModelLogEntry) HestonSLVFDMModel::LogEntry;
%feature ("flatnested") LogEntry;
class HestonSLVFDMModel {
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

    struct LogEntry {
        const Time t;
        const ext::shared_ptr<Array> prob;
        const ext::shared_ptr<FdmMesherComposite> mesher;
        %extend {
            LogEntry() {
                const HestonSLVFDMModel::LogEntry entry = {
                    0.0, ext::shared_ptr<Array>(),
                    ext::shared_ptr<FdmMesherComposite>() };
                return new HestonSLVFDMModel::LogEntry(entry);
            }
        }
    };

    const std::list<LogEntry>& logEntries() const;
};


#endif
