#ifndef ql_instruments_CapFloor_i
#define ql_instruments_CapFloor_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/termstructures/YieldTermStructure.i

%{
using QuantLib::CapFloor;
using QuantLib::MakeCapFloor;
%}

%shared_ptr(CapFloor)
class CapFloor : public Instrument {
  public:
    enum Type { Cap , Floor , Collar };
    CapFloor(
        Type type,
        Leg floatingLeg,
        std::vector<Rate> capRates,
        std::vector<Rate> floorRates);
    CapFloor(
        Type type,
        Leg floatingLeg,
        const std::vector<Rate>& strikes);;
    Type type() const;
    const std::vector<Rate>& capRates();
    const std::vector<Rate>& floorRates();
    const Leg& floatingLeg() const;
    Date startDate() const;
    Date maturityDate() const;
    ext::shared_ptr<FloatingRateCoupon> lastFloatingRateCoupon() const;
    ext::shared_ptr<CapFloor> optionlet(Size n) const;
    Rate atmRate(const YieldTermStructure& discountCurve) const;
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
    %extend {
        const Real vega() {
            return self->result<Real>("vega");
        }
        const std::vector<Real> optionletsPrice() {
            return self->result<std::vector<Real>>("optionletsPrice");
        }
        const std::vector<Real> optionletsVega() {
            return self->result<std::vector<Real>>("optionletsVega");
        }
        const std::vector<Real> optionletsDelta() {
            return self->result<std::vector<Real>>("optionletsDelta");
        }
        const std::vector<DiscountFactor> optionletsDiscountFactor() {
            return self->result<std::vector<DiscountFactor>>("optionletsDiscountFactor");
        }
        const std::vector<Rate> optionletsAtmForward(){
            return self->result<std::vector<Real>>("optionletsAtmForward");
        }
        const std::vector<Rate> optionletsStdDev(){
            return self->result<std::vector<Real>>("optionletsStdDev");
        }
    }
};

class MakeCapFloor {
  public:
    MakeCapFloor(
        CapFloor::Type capFloorType,
        const Period& capFloorTenor,
        const ext::shared_ptr<IborIndex>& iborIndex,
        Rate strike = Null<Rate>(),
        const Period& forwardStart = 0*Days);

    %extend {
        ext::shared_ptr<CapFloor> makeCapFloor() const {
            return (ext::shared_ptr<CapFloor>)(*self);
        }
    }

    MakeCapFloor& withNominal(Real n);
    MakeCapFloor& withEffectiveDate(
        const Date& effectiveDate, bool firstCapletExcluded);
    MakeCapFloor& withTenor(const Period& t);
    MakeCapFloor& withCalendar(const Calendar& cal);
    MakeCapFloor& withConvention(BusinessDayConvention bdc);
    MakeCapFloor& withTerminationDateConvention(BusinessDayConvention bdc);
    MakeCapFloor& withRule(DateGeneration::Rule r);
    MakeCapFloor& withEndOfMonth(bool flag = true);
    MakeCapFloor& withFirstDate(const Date& d);
    MakeCapFloor& withNextToLastDate(const Date& d);
    MakeCapFloor& withDayCount(const DayCounter& dc);
    MakeCapFloor& asOptionlet(bool b = true);
    MakeCapFloor& withPricingEngine(
        const ext::shared_ptr<PricingEngine>& engine);
};

#endif
