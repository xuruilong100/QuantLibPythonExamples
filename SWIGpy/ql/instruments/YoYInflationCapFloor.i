#ifndef ql_instruments_YoYInflationCapFloor_i
#define ql_instruments_YoYInflationCapFloor_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::YoYInflationCapFloor;
%}

%shared_ptr(YoYInflationCapFloor)
class YoYInflationCapFloor : public Instrument {
  public:
    enum Type { Cap, Floor, Collar };
    YoYInflationCapFloor(
        YoYInflationCapFloor::Type type,
        const Leg& yoyLeg,
        const std::vector<Rate>& strikes);
    Volatility impliedVolatility(
        Real price,
        const Handle<YoYInflationTermStructure>& curve,
        Volatility guess,
        Real accuracy = 1.0e-4,
        Size maxEvaluations = 100,
        Volatility minVol = 1.0e-7,
        Volatility maxVol = 4.0) const;
    %extend {
        std::vector<Real> optionletPrices() {
            return self->result<std::vector<Real> >("optionletsPrice");
        }
    }
};

#endif
