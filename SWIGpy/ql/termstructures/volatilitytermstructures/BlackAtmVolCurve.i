#ifndef ql_termstructures_volatilitytermstructures_BlackAtmVolCurve_i
#define ql_termstructures_volatilitytermstructures_BlackAtmVolCurve_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/VolatilityTermStructure.i

%{
using QuantLib::BlackAtmVolCurve;
%}

%shared_ptr(BlackAtmVolCurve)
class BlackAtmVolCurve : public VolatilityTermStructure {
  private:
    BlackAtmVolCurve();
    Volatility atmVol(const Period& optionTenor,
                      bool extrapolate = false) const;
    Volatility atmVol(const Date& maturity,
                      bool extrapolate = false) const;
    Volatility atmVol(Time maturity,
                      bool extrapolate = false) const;
    Real atmVariance(const Period& optionTenor,
                     bool extrapolate = false) const;
    Real atmVariance(const Date& maturity,
                     bool extrapolate = false) const;
    Real atmVariance(Time maturity,
                     bool extrapolate = false) const;
};

%template(BlackAtmVolCurveHandle) Handle<BlackAtmVolCurve>;
%template(RelinkableBlackAtmVolCurveHandle) RelinkableHandle<BlackAtmVolCurve>;

#endif
