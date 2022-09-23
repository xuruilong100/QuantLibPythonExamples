#ifndef ql_engines_others_i
#define ql_engines_others_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticSimpleChooserEngine;
using QuantLib::AnalyticComplexChooserEngine;
using QuantLib::AnalyticCompoundOptionEngine;
using QuantLib::AnalyticHolderExtensibleOptionEngine;
using QuantLib::AnalyticWriterExtensibleOptionEngine;
using QuantLib::IntegralHestonVarianceOptionEngine;
using QuantLib::ReplicatingVarianceSwapEngine;
using QuantLib::MCVarianceSwapEngine;
using QuantLib::MakeMCVarianceSwapEngine;
using QuantLib::InterpolatingCPICapFloorEngine;
using QuantLib::FdSimpleExtOUStorageEngine;
using QuantLib::FdKlugeExtOUSpreadEngine;
%}

%shared_ptr(AnalyticSimpleChooserEngine)
class AnalyticSimpleChooserEngine : public PricingEngine {
  public:
    AnalyticSimpleChooserEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticComplexChooserEngine)
class AnalyticComplexChooserEngine : public PricingEngine {
  public:
    AnalyticComplexChooserEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticCompoundOptionEngine)
class AnalyticCompoundOptionEngine : public PricingEngine {
  public:
    AnalyticCompoundOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticHolderExtensibleOptionEngine)
class AnalyticHolderExtensibleOptionEngine : public PricingEngine {
  public:
    AnalyticHolderExtensibleOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticWriterExtensibleOptionEngine)
class AnalyticWriterExtensibleOptionEngine : public PricingEngine {
  public:
    AnalyticWriterExtensibleOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(IntegralHestonVarianceOptionEngine)
class IntegralHestonVarianceOptionEngine : public PricingEngine {
  public:
    IntegralHestonVarianceOptionEngine(
        ext::shared_ptr<HestonProcess>);
};

%shared_ptr(ReplicatingVarianceSwapEngine)
class ReplicatingVarianceSwapEngine : public PricingEngine {
  public:
    ReplicatingVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Real dk = 5.0,
        const std::vector<Real>& callStrikes = std::vector<Real>(),
        const std::vector<Real>& putStrikes = std::vector<Real>());
};

%shared_ptr(MCVarianceSwapEngine<PseudoRandom>)
%shared_ptr(MCVarianceSwapEngine<LowDiscrepancy>)
template <class RNG>
class MCVarianceSwapEngine : public PricingEngine {
  public:
    MCVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed);
};

%template(MCPRVarianceSwapEngine) MCVarianceSwapEngine<PseudoRandom>;
%template(MCLDVarianceSwapEngine) MCVarianceSwapEngine<LowDiscrepancy>;

%shared_ptr(MakeMCVarianceSwapEngine<PseudoRandom>)
%shared_ptr(MakeMCVarianceSwapEngine<LowDiscrepancy>)
template <class RNG>
class MakeMCVarianceSwapEngine {
  public:
    MakeMCVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
    
    MakeMCVarianceSwapEngine& withSteps(Size steps);
    MakeMCVarianceSwapEngine& withStepsPerYear(Size steps);
    MakeMCVarianceSwapEngine& withBrownianBridge(bool b = true);
    MakeMCVarianceSwapEngine& withSamples(Size samples);
    MakeMCVarianceSwapEngine& withAbsoluteTolerance(Real tolerance);
    MakeMCVarianceSwapEngine& withMaxSamples(Size samples);
    MakeMCVarianceSwapEngine& withSeed(BigNatural seed);
    MakeMCVarianceSwapEngine& withAntitheticVariate(bool b = true);
    
    %extend {
        ext::shared_ptr<PricingEngine> makeEngine() const {
            return (ext::shared_ptr<PricingEngine>)(*self);
        }
    }
};

%template(MakeMCPRVarianceSwapEngine) MakeMCVarianceSwapEngine<PseudoRandom>;
%template(MakeMCLDVarianceSwapEngine) MakeMCVarianceSwapEngine<LowDiscrepancy>;

%shared_ptr(InterpolatingCPICapFloorEngine)
class InterpolatingCPICapFloorEngine : public PricingEngine {
    public:
      InterpolatingCPICapFloorEngine(
          Handle<CPICapFloorTermPriceSurface>);
      std::string name() const;
};

%shared_ptr(FdSimpleExtOUStorageEngine)
class FdSimpleExtOUStorageEngine : public PricingEngine {
  public:    
    %extend {
        FdSimpleExtOUStorageEngine(
            ext::shared_ptr<ExtendedOrnsteinUhlenbeckProcess> p,
            ext::shared_ptr<YieldTermStructure> rTS,
            Size tGrid = 50,
            Size xGrid = 100,
            Size yGrid = Null<Size>(),
            std::vector<std::pair<Time, Real>> shape = std::vector<std::pair<Time, Real>>(),
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas()) {
                typedef std::vector<std::pair<Time, Real>> Shape;
                ext::shared_ptr<Shape> shape_;
                if (!shape.empty())
                    shape_.reset(new Shape(shape));
                return new FdSimpleExtOUStorageEngine(
                    p, rTS, tGrid, xGrid, yGrid, shape_, schemeDesc);
            }
    }
};

%shared_ptr(FdKlugeExtOUSpreadEngine)
class FdKlugeExtOUSpreadEngine : public PricingEngine {
  public:      
    %extend {
        FdKlugeExtOUSpreadEngine(
            ext::shared_ptr<KlugeExtOUProcess> klugeOUProcess,
            ext::shared_ptr<YieldTermStructure> rTS,
            Size tGrid = 25,
            Size xGrid = 50,
            Size yGrid = 10,
            Size uGrid = 25,
            std::vector<std::pair<Time, Real>> gasShape = std::vector<std::pair<Time, Real>>(),
            std::vector<std::pair<Time, Real>> powerShape = std::vector<std::pair<Time, Real>>(),
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer()) {
                typedef std::vector<std::pair<Time, Real>> GasShape;
                typedef std::vector<std::pair<Time, Real>> PowerShape;
                ext::shared_ptr<GasShape> gasShape_;
                ext::shared_ptr<PowerShape> powerShape_;

                if (!gasShape.empty())
                    gasShape_.reset(new GasShape(gasShape));
                if (!powerShape.empty())
                    powerShape_.reset(new PowerShape(powerShape));
                
                return new FdKlugeExtOUSpreadEngine(
                    klugeOUProcess, rTS,
                    tGrid, xGrid, yGrid, uGrid,
                    gasShape_, powerShape_, schemeDesc);
            }
    }
};

#endif
