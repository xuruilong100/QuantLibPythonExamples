#ifndef ql_engines_dividend_i
#define ql_engines_dividend_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::AnalyticDividendEuropeanEngine;
using QuantLib::FDDividendEuropeanEngine;
using QuantLib::FDDividendAmericanEngine;
using QuantLib::FdOrnsteinUhlenbeckVanillaEngine;
%}

%shared_ptr(AnalyticDividendEuropeanEngine)
class AnalyticDividendEuropeanEngine : public PricingEngine {
  public:
    AnalyticDividendEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process);
};

%shared_ptr(FDDividendEuropeanEngine<CrankNicolson>)
%rename(FDDividendEuropeanEngineT) FDDividendEuropeanEngine;
template <class S>
class FDDividendEuropeanEngine : public PricingEngine {
  public:
    FDDividendEuropeanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size timeSteps = 100,
        Size gridPoints = 100,
        bool timeDependent = false);
};

%template(FDDividendEuropeanEngine) FDDividendEuropeanEngine<CrankNicolson>;

%shared_ptr(FDDividendAmericanEngine<CrankNicolson>)
%rename(FDDividendAmericanEngineT) FDDividendAmericanEngine;
template <class S>
class FDDividendAmericanEngine : public PricingEngine {
  public:
    FDDividendAmericanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size timeSteps = 100,
        Size gridPoints = 100,
        bool timeDependent = false);
};

%template(FDDividendAmericanEngine) FDDividendAmericanEngine<CrankNicolson>;

%shared_ptr(FdOrnsteinUhlenbeckVanillaEngine)
class FdOrnsteinUhlenbeckVanillaEngine : public PricingEngine {
  public:
    %feature("kwargs") FdOrnsteinUhlenbeckVanillaEngine;
    FdOrnsteinUhlenbeckVanillaEngine(
        const ext::shared_ptr<OrnsteinUhlenbeckProcess>&,
        const ext::shared_ptr<YieldTermStructure>& rTS,
        Size tGrid = 100,
        Size xGrid = 100,
        Size dampingSteps = 0,
        Real epsilon = 0.0001,
        const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Douglas());
};

#endif
