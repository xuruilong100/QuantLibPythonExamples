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
        const ext::shared_ptr<BlackProcess>& process1,
        const ext::shared_ptr<BlackProcess>& process2,
        const Handle<Quote>& correlation);
};

#endif
