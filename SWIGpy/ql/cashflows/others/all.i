#ifndef ql_cashflows_others_all_i
#define ql_cashflows_others_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::SimpleCashFlow;
using QuantLib::IndexedCashFlow;
using QuantLib::Redemption;
using QuantLib::AmortizingPayment;
%}

%shared_ptr(SimpleCashFlow)
class SimpleCashFlow : public CashFlow {
  public:
    SimpleCashFlow(Real amount, const Date& date);
};

%shared_ptr(Redemption)
class Redemption : public SimpleCashFlow {
  public:
    Redemption(Real amount, const Date& date);
};

%shared_ptr(AmortizingPayment)
class AmortizingPayment : public SimpleCashFlow {
  public:
    AmortizingPayment(Real amount, const Date& date);
};

%shared_ptr(IndexedCashFlow)
class IndexedCashFlow : public CashFlow {
  public:
    IndexedCashFlow(Real notional,
                    const ext::shared_ptr<Index>& index,
                    const Date& baseDate,
                    const Date& fixingDate,
                    const Date& paymentDate,
                    bool growthOnly = false);
    Real notional() const;
    Date baseDate() const;
    Date fixingDate() const;
    ext::shared_ptr<Index> index() const;
    bool growthOnly() const;
};

%inline %{
    ext::shared_ptr<IndexedCashFlow> as_indexed_cashflow(
        const ext::shared_ptr<CashFlow>& cf) {
        return ext::dynamic_pointer_cast<IndexedCashFlow>(cf);
    }
%}



#endif
