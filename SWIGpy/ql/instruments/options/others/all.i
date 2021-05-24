#ifndef ql_instruments_options_others_all_i
#define ql_instruments_options_others_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/instruments/Option.i

%{
using QuantLib::CdsOption;
%}

%shared_ptr(CdsOption)
class CdsOption : public Option {
  public:
    CdsOption(
        const ext::shared_ptr<CreditDefaultSwap>& swap,
        const ext::shared_ptr<Exercise>& exercise,
        bool knocksOut = true);
    Rate atmRate() const;
    Real riskyAnnuity() const;
    Volatility impliedVolatility(
        Real price,
        const Handle<YieldTermStructure>& termStructure,
        const Handle<DefaultProbabilityTermStructure>&,
        Real recoveryRate,
        Real accuracy = 1.e-4,
        Size maxEvaluations = 100,
        Volatility minVol = 1.0e-7,
        Volatility maxVol = 4.0) const;
};

#endif
