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
%}

%shared_ptr(AnalyticSimpleChooserEngine)
class AnalyticSimpleChooserEngine : public PricingEngine {
  public:
    explicit AnalyticSimpleChooserEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticComplexChooserEngine)
class AnalyticComplexChooserEngine : public PricingEngine {
  public:
    explicit AnalyticComplexChooserEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticCompoundOptionEngine)
class AnalyticCompoundOptionEngine : public PricingEngine {
  public:
    explicit AnalyticCompoundOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticHolderExtensibleOptionEngine)
class AnalyticHolderExtensibleOptionEngine : public PricingEngine {
  public:
    explicit AnalyticHolderExtensibleOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

%shared_ptr(AnalyticWriterExtensibleOptionEngine)
class AnalyticWriterExtensibleOptionEngine : public PricingEngine {
  public:
    explicit AnalyticWriterExtensibleOptionEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

#endif
