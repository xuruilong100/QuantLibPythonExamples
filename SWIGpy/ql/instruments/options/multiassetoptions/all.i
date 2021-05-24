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
  public:
    EverestOption(
        Real notional,
        Rate guarantee,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(HimalayaOption)
class HimalayaOption : public MultiAssetOption {
  public:
    HimalayaOption(
        const std::vector<Date>& fixingDates,
        Real strike);
};

%shared_ptr(SpreadOption);
class SpreadOption : public MultiAssetOption {
public:
  SpreadOption(
      const ext::shared_ptr<PlainVanillaPayoff>& payoff,
      const ext::shared_ptr<Exercise>& exercise);
};

#endif
