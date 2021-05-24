#ifndef ql_instruments_capfloors_all_i
#define ql_instruments_capfloors_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/CapFloor.i

%{
using QuantLib::Cap;
using QuantLib::Floor;
using QuantLib::Collar;
%}

%shared_ptr(Cap)
class Cap : public CapFloor {
  public:
    Cap(const std::vector<ext::shared_ptr<CashFlow> >& leg,
        const std::vector<Rate>& capRates);
};

%shared_ptr(Floor)
class Floor : public CapFloor {
  public:
    Floor(
        const std::vector<ext::shared_ptr<CashFlow> >& leg,
        const std::vector<Rate>& floorRates);
};

%shared_ptr(Collar)
class Collar : public CapFloor {
  public:
    Collar(
        const std::vector<ext::shared_ptr<CashFlow> >& leg,
        const std::vector<Rate>& capRates,
        const std::vector<Rate>& floorRates);
};

#endif
