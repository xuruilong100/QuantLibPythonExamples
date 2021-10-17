#ifndef ql_instruments_Swap_i
#define ql_instruments_Swap_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Swap;
%}

%shared_ptr(Swap)
class Swap : public Instrument {
  public:
    enum Type { Receiver = -1 , Payer = 1 };
    Swap(const std::vector<ext::shared_ptr<CashFlow>>& firstLeg,
         const std::vector<ext::shared_ptr<CashFlow>>& secondLeg);
    Swap(const std::vector<Leg>& legs,
         const std::vector<bool>& payer);
    Size numberOfLegs() const;
    Date startDate();
    Date maturityDate();
    const Leg& leg(Size i);
    Real legNPV(Size j) const;
    Real legBPS(Size k) const;
    DiscountFactor startDiscounts(Size j) const;
    DiscountFactor endDiscounts(Size j) const;
    DiscountFactor npvDateDiscount() const;
    bool payer(Size j) const;
};

#endif
