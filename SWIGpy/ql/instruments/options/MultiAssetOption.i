#ifndef ql_instruments_options_MultiAssetOption_i
#define ql_instruments_options_MultiAssetOption_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/Option.i

%{
using QuantLib::MultiAssetOption;
%}

%shared_ptr(MultiAssetOption)
class MultiAssetOption : public Option {
  public:
    Real delta();
    Real gamma();
    Real theta();
    Real vega();
    Real rho();
    Real dividendRho();
};

#endif
