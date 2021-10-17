#ifndef ql_termstructures_VolatilityTermStructure_i
#define ql_termstructures_VolatilityTermStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::VolatilityTermStructure;
%}

%shared_ptr(VolatilityTermStructure)
class VolatilityTermStructure : public TermStructure {
  private:
    VolatilityTermStructure();
  public:
    BusinessDayConvention businessDayConvention() const;
    Date optionDateFromTenor(const Period& ) const;
    Real minStrike() const;
    Real maxStrike() const;
};

#endif
