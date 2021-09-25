#ifndef ql_engines_spread_i
#define ql_engines_spread_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::KirkSpreadOptionEngine;
%}

%shared_ptr(KirkSpreadOptionEngine);
class KirkSpreadOptionEngine : public PricingEngine {
  public:
    KirkSpreadOptionEngine(
        ext::shared_ptr<BlackProcess> process1,
        ext::shared_ptr<BlackProcess> process2,
        Handle<Quote> correlation);
};

#endif
