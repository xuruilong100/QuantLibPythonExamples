#ifndef ql_instruments_options_multiassetoptions_all_i
#define ql_instruments_options_multiassetoptions_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/options/MultiAssetOption.i

%{
using QuantLib::BasketOption;
using QuantLib::EverestOption;
using QuantLib::HimalayaOption;
using QuantLib::MargrabeOption;
using QuantLib::PagodaOption;
using QuantLib::TwoAssetCorrelationOption;
using QuantLib::VanillaVPPOption;
using QuantLib::SpreadOption;
%}

%shared_ptr(BasketOption)
class BasketOption : public MultiAssetOption {
  public:
    BasketOption(
        const ext::shared_ptr<BasketPayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(EverestOption)
class EverestOption : public MultiAssetOption {
    %rename(optionYield) yield;
  public:
    EverestOption(
        Real notional,
        Rate guarantee,
        const ext::shared_ptr<Exercise>& exercise);
    Rate yield() const;;
};

%shared_ptr(HimalayaOption)
class HimalayaOption : public MultiAssetOption {
  public:
    HimalayaOption(
        const std::vector<Date>& fixingDates,
        Real strike);
};

%shared_ptr(MargrabeOption)
class MargrabeOption : public MultiAssetOption {
  public:
    MargrabeOption(
        Integer Q1,
        Integer Q2,
        const ext::shared_ptr<Exercise>&);
    Real delta1() const;
    Real delta2() const;
    Real gamma1() const;
    Real gamma2() const;
};

%shared_ptr(PagodaOption)
class PagodaOption : public MultiAssetOption {
  public:
    PagodaOption(
        const std::vector<Date>& fixingDates,
        Real roof,
        Real fraction);
};

%shared_ptr(SpreadOption)
class SpreadOption : public MultiAssetOption {
public:
  SpreadOption(
      const ext::shared_ptr<PlainVanillaPayoff>& payoff,
      const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(TwoAssetCorrelationOption)
class TwoAssetCorrelationOption : public MultiAssetOption {
  public:
    TwoAssetCorrelationOption(
        Option::Type type,
        Real strike1,
        Real strike2,
        const ext::shared_ptr<Exercise>&);
};

%shared_ptr(VanillaVPPOption)
class VanillaVPPOption : public MultiAssetOption {
  public:
    VanillaVPPOption(
        Real heatRate,
        Real pMin,
        Real pMax,
        Size tMinUp, 
        Size tMinDown,
        Real startUpFuel, 
        Real startUpFixCost,
        const ext::shared_ptr<SwingExercise>& exercise,
        Size nStarts = Null<Size>(),
        Size nRunningHours = Null<Size>());
};

#endif
