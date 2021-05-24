#ifndef ql_instruments_options_OneAssetOption_i
#define ql_instruments_options_OneAssetOption_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/Option.i

%{
using QuantLib::OneAssetOption;
%}

%shared_ptr(OneAssetOption)
class OneAssetOption : public Option {
  private:
    OneAssetOption();
  public:
    bool isExpired() const;
    Real delta() const;
    Real deltaForward() const;
    Real elasticity() const;
    Real gamma() const;
    Real theta() const;
    Real thetaPerDay() const;
    Real vega() const;
    Real rho() const;
    Real dividendRho() const;
    Real strikeSensitivity() const;
    Real itmCashProbability() const;
};

#endif
