#ifndef ql_cashflows_Dividend_i
#define ql_cashflows_Dividend_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Dividend;
%}

%shared_ptr(Dividend)
class Dividend : public CashFlow {
  private:
    Dividend();
  public:
    Real amount(Real underlying) const;
};

#endif
