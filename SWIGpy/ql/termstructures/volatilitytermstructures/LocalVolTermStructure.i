#ifndef ql_termstructures_volatilitytermstructures_LocalVolTermStructure_i
#define ql_termstructures_volatilitytermstructures_LocalVolTermStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/VolatilityTermStructure.i

%{
using QuantLib::LocalVolTermStructure;
%}

%shared_ptr(LocalVolTermStructure);
class LocalVolTermStructure : public VolatilityTermStructure {
  private:
    LocalVolTermStructure();
  public:
    Volatility localVol(const Date&, Real u,
                        bool extrapolate = false) const;
    Volatility localVol(Time, Real u,
                        bool extrapolate = false) const;
};

%template(LocalVolTermStructureHandle) Handle<LocalVolTermStructure>;
%template(RelinkableLocalVolTermStructureHandle) RelinkableHandle<LocalVolTermStructure>;

#endif
