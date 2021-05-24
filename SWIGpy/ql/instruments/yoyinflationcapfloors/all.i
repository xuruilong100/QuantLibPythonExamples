#ifndef ql_yoy_inflation_cap_floor_i
#define ql_yoy_inflation_cap_floor_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/YoYInflationCapFloor.i

%{
using QuantLib::YoYInflationCap;
using QuantLib::YoYInflationFloor;
using QuantLib::YoYInflationCollar;
%}

%shared_ptr(YoYInflationCap)
class YoYInflationCap : public YoYInflationCapFloor {
  public:
    YoYInflationCap(
        const std::vector<ext::shared_ptr<CashFlow> >& leg,
        const std::vector<Rate>& capRates);
};

%shared_ptr(YoYInflationFloor)
class YoYInflationFloor : public YoYInflationCapFloor {
  public:
    YoYInflationFloor(
        const std::vector<ext::shared_ptr<CashFlow> >& leg,
        const std::vector<Rate>& floorRates);
};

%shared_ptr(YoYInflationCollar)
class YoYInflationCollar : public YoYInflationCapFloor {
  public:
    YoYInflationCollar(
        const std::vector<ext::shared_ptr<CashFlow> >& leg,
        const std::vector<Rate>& capRates,
        const std::vector<Rate>& floorRates);
};

#endif
