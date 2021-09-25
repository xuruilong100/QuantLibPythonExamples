#ifndef ql_cashflows_dividends_all_i
#define ql_cashflows_dividends_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/cashflows/Dividend.i

%{
using QuantLib::FixedDividend;
using QuantLib::FractionalDividend;
using QuantLib::DividendSchedule;
%}

%shared_ptr(FixedDividend)
class FixedDividend : public Dividend {
  public:
    FixedDividend(Real amount, const Date& date);
};

%shared_ptr(FractionalDividend)
class FractionalDividend : public Dividend {
  public:
    FractionalDividend(Rate rate, const Date& date);
    FractionalDividend(Real rate, Real nominal, const Date &date);
    Real amount() const;
    Real amount(Real underlying) const;
};

%template(DividendSchedule) std::vector<ext::shared_ptr<Dividend> >;

#endif
