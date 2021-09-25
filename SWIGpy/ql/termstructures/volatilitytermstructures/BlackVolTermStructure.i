#ifndef ql_termstructures_volatilitytermstructures_BlackVolTermStructure_i
#define ql_termstructures_volatilitytermstructures_BlackVolTermStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/VolatilityTermStructure.i

%{
using QuantLib::BlackVolTermStructure;
%}

%shared_ptr(BlackVolTermStructure);
class BlackVolTermStructure : public VolatilityTermStructure {
  private:
    BlackVolTermStructure();
  public:
    Volatility blackVol(const Date&, Real strike,
                        bool extrapolate = false) const;
    Volatility blackVol(Time, Real strike,
                        bool extrapolate = false) const;
    Real blackVariance(const Date&, Real strike,
                       bool extrapolate = false) const;
    Real blackVariance(Time, Real strike,
                       bool extrapolate = false) const;
    Volatility blackForwardVol(const Date&, const Date&,
                               Real strike, bool extrapolate = false) const;
    Volatility blackForwardVol(Time, Time, Real strike,
                               bool extrapolate = false) const;
    Real blackForwardVariance(const Date&, const Date&,
                              Real strike, bool extrapolate = false) const;
    Real blackForwardVariance(Time, Time, Real strike,
                              bool extrapolate = false) const;
};

%template(BlackVolTermStructureHandle) Handle<BlackVolTermStructure>;
%template(RelinkableBlackVolTermStructureHandle) RelinkableHandle<BlackVolTermStructure>;

#endif
