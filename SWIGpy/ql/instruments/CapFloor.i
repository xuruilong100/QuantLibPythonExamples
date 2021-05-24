#ifndef ql_instruments_CapFloor_i
#define ql_instruments_CapFloor_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CapFloor;
%}

%shared_ptr(CapFloor)
class CapFloor : public Instrument {
  public:
    Volatility impliedVolatility(
        Real price,
        const Handle<YieldTermStructure>& disc,
        Volatility guess,
        Real accuracy = 1.0e-4,
        Natural maxEvaluations = 100,
        Volatility minVol = 1.0e-7,
        Volatility maxVol = 4.0,
        VolatilityType type = ShiftedLognormal,
        Real displacement = 0.0) const;
    enum Type { Cap, Floor, Collar };
    const Leg& floatingLeg() const;
    const std::vector<Rate>& capRates();
    const std::vector<Rate>& floorRates();
    Date startDate() const;
    Date maturityDate() const;
    Type type() const;
    Rate atmRate(const YieldTermStructure& discountCurve) const;
    %extend {
        const Real vega() {
            return self->result<Real>("vega");
        }
        const std::vector<Real> optionletsPrice() {
            return self->result<std::vector<Real> >("optionletsPrice");
        }
        const std::vector<Real> optionletsVega() {
            return self->result<std::vector<Real> >("optionletsVega");
        }
        const std::vector<Real> optionletsDelta() {
            return self->result<std::vector<Real> >("optionletsDelta");
        }
        const std::vector<DiscountFactor> optionletsDiscountFactor() {
            return self->result<std::vector<DiscountFactor> >("optionletsDiscountFactor");
        }
        const std::vector<Rate> optionletsAtmForward(){
            return self->result<std::vector<Real> >("optionletsAtmForward");
        }
        const std::vector<Rate> optionletsStdDev(){
            return self->result<std::vector<Real> >("optionletsStdDev");
        }
    }
};

#endif
