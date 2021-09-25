#ifndef ql_payoffs_i
#define ql_payoffs_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Payoff;
using QuantLib::TypePayoff;
using QuantLib::BasketPayoff;
using QuantLib::MinBasketPayoff;
using QuantLib::MaxBasketPayoff;
using QuantLib::AverageBasketPayoff;
using QuantLib::SpreadBasketPayoff;
using QuantLib::FloatingTypePayoff;
using QuantLib::StrikedTypePayoff;
using QuantLib::PlainVanillaPayoff;
using QuantLib::PercentageStrikePayoff;
using QuantLib::CashOrNothingPayoff;
using QuantLib::AssetOrNothingPayoff;
using QuantLib::SuperSharePayoff;
using QuantLib::GapPayoff;
using QuantLib::VanillaForwardPayoff;
%}

%shared_ptr(Payoff);
class Payoff {
  private:
    Payoff();
  public:
    std::string name() const;
    std::string description() const;
    Real operator()(Real price) const;
};

%shared_ptr(TypePayoff)
class TypePayoff : public Payoff {
  private:
    TypePayoff();
  public:
    Option::Type optionType();
};

%shared_ptr(BasketPayoff)
class BasketPayoff : public Payoff {
  private:
    BasketPayoff();
  public:
    Real operator()(const Array &a) const;
    Real accumulate(const Array &a) const;
    ext::shared_ptr<Payoff> basePayoff();
};

%shared_ptr(MinBasketPayoff)
class MinBasketPayoff : public BasketPayoff  {
  public:
    MinBasketPayoff(
        const ext::shared_ptr<Payoff> p);
};

%shared_ptr(MaxBasketPayoff)
class MaxBasketPayoff : public BasketPayoff  {
  public:
    MaxBasketPayoff(
        const ext::shared_ptr<Payoff> p);
};

%shared_ptr(AverageBasketPayoff)
class AverageBasketPayoff : public BasketPayoff {
  public:
    AverageBasketPayoff(
        const ext::shared_ptr<Payoff> p, const Array& a);
    AverageBasketPayoff(
        const ext::shared_ptr<Payoff> p, Size n);
};

%shared_ptr(SpreadBasketPayoff)
class SpreadBasketPayoff : public BasketPayoff  {
  public:
    SpreadBasketPayoff(
        const ext::shared_ptr<Payoff> p);
};

%shared_ptr(FloatingTypePayoff)
class FloatingTypePayoff : public TypePayoff {
  public:
    FloatingTypePayoff(Option::Type type);
};

%shared_ptr(StrikedTypePayoff)
class StrikedTypePayoff : public TypePayoff {
  private:
    StrikedTypePayoff();
  public:
    Real strike();
};

%shared_ptr(PlainVanillaPayoff)
class PlainVanillaPayoff : public StrikedTypePayoff {
  public:
    PlainVanillaPayoff(
        Option::Type type, Real strike);
};

%inline %{
    const ext::shared_ptr<PlainVanillaPayoff> as_plain_vanilla_payoff(
        const ext::shared_ptr<Payoff>& payoff) {
        return ext::dynamic_pointer_cast<PlainVanillaPayoff>(payoff);
    }
%}

%shared_ptr(PercentageStrikePayoff)
class PercentageStrikePayoff : public StrikedTypePayoff {
  public:
    PercentageStrikePayoff(
        Option::Type type, Real moneyness);
};

%shared_ptr(CashOrNothingPayoff)
class CashOrNothingPayoff : public StrikedTypePayoff {
  public:
    CashOrNothingPayoff(
        Option::Type type, Real strike, Real payoff);
};

%shared_ptr(AssetOrNothingPayoff)
class AssetOrNothingPayoff : public StrikedTypePayoff {
  public:
    AssetOrNothingPayoff(
        Option::Type type, Real strike);
};

%shared_ptr(SuperSharePayoff)
class SuperSharePayoff : public StrikedTypePayoff {
  public:
    SuperSharePayoff(
        Option::Type type, Real strike, Real increment);
};

%shared_ptr(GapPayoff)
class GapPayoff : public StrikedTypePayoff {
  public:
    GapPayoff(
        Option::Type type, Real strike, Real strikePayoff);
};

%shared_ptr(VanillaForwardPayoff)
class VanillaForwardPayoff : public StrikedTypePayoff {
  public:
    VanillaForwardPayoff(
        Option::Type type, Real strike);
};

#endif
