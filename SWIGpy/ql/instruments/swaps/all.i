#ifndef ql_instruments_swaps_all_i
#define ql_instruments_swaps_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/Swap.i

%{
using QuantLib::ArithmeticAverageOIS;
using QuantLib::BMASwap;
using QuantLib::AssetSwap;
using QuantLib::CPISwap;
using QuantLib::FloatFloatSwap;
using QuantLib::IrregularSwap;
using QuantLib::NonstandardSwap;
using QuantLib::OvernightIndexedSwap;
using QuantLib::VanillaSwap;
using QuantLib::YearOnYearInflationSwap;
using QuantLib::ZeroCouponInflationSwap;
using QuantLib::ZeroCouponSwap;
using QuantLib::MakeOIS;
using QuantLib::MakeVanillaSwap;
%}

%shared_ptr(ArithmeticAverageOIS)
class ArithmeticAverageOIS : public Swap {
  public:
    enum Type { Receiver = -1, Payer = 1 };
    ArithmeticAverageOIS(
        ArithmeticAverageOIS::Type type,
        Real nominal,
        const Schedule& fixedLegSchedule,
        Rate fixedRate,
        const DayCounter& fixedDC,
        const ext::shared_ptr<OvernightIndex>& overnightIndex,
        const Schedule& overnightLegSchedule,
        Spread spread = 0.0,
        Real meanReversionSpeed = 0.03,
        Real volatility = 0.00,
        bool byApprox = false);
    ArithmeticAverageOIS(
        ArithmeticAverageOIS::Type type,
        const std::vector<Real>& nominals,
        const Schedule& fixedLegSchedule,
        Rate fixedRate,
        const DayCounter& fixedDC,
        const ext::shared_ptr<OvernightIndex>& overnightIndex,
        const Schedule& overnightLegSchedule,
        Spread spread = 0.0,
        Real meanReversionSpeed = 0.03,
        Real volatility = 0.00,
        bool byApprox = false);

    ArithmeticAverageOIS::Type type() const;
    Real nominal() const;
    std::vector<Real> nominals() const;
    Frequency fixedLegPaymentFrequency();
    Frequency overnightLegPaymentFrequency();
    Rate fixedRate() const;
    const DayCounter& fixedDayCount();
    const ext::shared_ptr<OvernightIndex>& overnightIndex();
    Spread spread() const;
    const Leg& fixedLeg() const;
    const Leg& overnightLeg() const;
    Real fixedLegBPS() const;
    Real fixedLegNPV() const;
    Real fairRate() const;
    Real overnightLegBPS() const;
    Real overnightLegNPV() const;
    Spread fairSpread() const;
};

%shared_ptr(BMASwap)
class BMASwap : public Swap {
  public:
    enum Type { Receiver = -1, Payer = 1 };
    BMASwap(
        BMASwap::Type type,
        Real nominal,
        const Schedule& liborSchedule,
        Rate liborFraction,
        Rate liborSpread,
        const ext::shared_ptr<IborIndex>& liborIndex,
        const DayCounter& liborDayCount,
        const Schedule& bmaSchedule,
        const ext::shared_ptr<BMAIndex>& bmaIndex,
        const DayCounter& bmaDayCount);

    Real liborFraction() const;
    Spread liborSpread() const;
    Real nominal() const;
    BMASwap::Type type() const;
    const Leg& bmaLeg() const;
    const Leg& liborLeg() const;
    Real liborLegBPS() const;
    Real liborLegNPV() const;
    Rate fairLiborFraction() const;
    Spread fairLiborSpread() const;
    Real bmaLegBPS() const;
    Real bmaLegNPV() const;
};

%shared_ptr(AssetSwap)
class AssetSwap : public Swap {
  public:
    AssetSwap(bool payBondCoupon,
              const ext::shared_ptr<Bond>& bond,
              Real bondCleanPrice,
              const ext::shared_ptr<IborIndex>& iborIndex,
              Spread spread,
              const Schedule& floatSchedule = Schedule(),
              const DayCounter& floatingDayCount = DayCounter(),
              bool parAssetSwap = true);
    AssetSwap(bool parAssetSwap,
              const ext::shared_ptr<Bond>& bond,
              Real bondCleanPrice,
              Real nonParRepayment,
              Real gearing,
              const ext::shared_ptr<IborIndex>& iborIndex,
              Spread spread = 0.0,
              const DayCounter& floatingDayCount = DayCounter(),
              Date dealMaturity = Date(),
              bool payBondCoupon = false);

    Spread fairSpread() const;
    Real floatingLegBPS() const;
    Real floatingLegNPV() const;
    Real fairCleanPrice() const;
    Real fairNonParRepayment() const;
    bool parSwap() const;
    Spread spread() const;
    Real cleanPrice() const;
    Real nonParRepayment() const;
    const ext::shared_ptr<Bond>& bond() const;
    bool payBondCoupon() const;
    const Leg& bondLeg() const;
    const Leg& floatingLeg() const;
};

%shared_ptr(CPISwap)
class CPISwap : public Swap {
  public:
    enum Type { Receiver = -1, Payer = 1 };
    CPISwap(
        CPISwap::Type type,
        Real nominal,
        bool subtractInflationNominal,
        Spread spread,
        const DayCounter& floatDayCount,
        const Schedule& floatSchedule,
        const BusinessDayConvention& floatRoll,
        Natural fixingDays,
        const ext::shared_ptr<IborIndex>& floatIndex,
        Rate fixedRate,
        Real baseCPI,
        const DayCounter& fixedDayCount,
        const Schedule& fixedSchedule,
        const BusinessDayConvention& fixedRoll,
        const Period& observationLag,
        const ext::shared_ptr<ZeroInflationIndex>& fixedIndex,
        CPI::InterpolationType observationInterpolation = CPI::AsIndex,
        Real inflationNominal = Null<Real>() );

    Real floatLegNPV() const;
    Spread fairSpread() const;
    Real fixedLegNPV() const;
    Rate fairRate() const;
    CPISwap::Type type() const;
    Real nominal() const;
    bool subtractInflationNominal() const;
    Spread spread() const;
    const DayCounter& floatDayCount() const;
    const Schedule& floatSchedule() const;
    const BusinessDayConvention& floatPaymentRoll() const;
    Natural fixingDays() const;
    const ext::shared_ptr<IborIndex>& floatIndex() const;
    Rate fixedRate() const;
    Real baseCPI() const;
    const DayCounter& fixedDayCount() const;
    const Schedule& fixedSchedule() const;
    const BusinessDayConvention& fixedPaymentRoll() const;
    Period observationLag() const;
    const ext::shared_ptr<ZeroInflationIndex>& fixedIndex() const;
    CPI::InterpolationType observationInterpolation() const;
    Real inflationNominal() const;
    const Leg& cpiLeg() const;
    const Leg& floatLeg() const;
};

%shared_ptr(FloatFloatSwap)
class FloatFloatSwap : public Swap {
  public:
    FloatFloatSwap(
        Swap::Type type,
        Real nominal1,
        Real nominal2,
        const Schedule& schedule1,
        const ext::shared_ptr<InterestRateIndex>& index1,
        const DayCounter& dayCount1,
        const Schedule& schedule2,
        const ext::shared_ptr<InterestRateIndex>& index2,
        const DayCounter& dayCount2,
        bool intermediateCapitalExchange = false,
        bool finalCapitalExchange = false,
        Real gearing1 = 1.0,
        Real spread1 = 0.0,
        Real cappedRate1 = Null<Real>(),
        Real flooredRate1 = Null<Real>(),
        Real gearing2 = 1.0,
        Real spread2 = 0.0,
        Real cappedRate2 = Null<Real>(),
        Real flooredRate2 = Null<Real>(),
        const boost::optional<BusinessDayConvention>& paymentConvention1 = boost::none,
        const boost::optional<BusinessDayConvention>& paymentConvention2 = boost::none);
     FloatFloatSwap(
        Swap::Type type,
        const std::vector<Real>& nominal1,
        const std::vector<Real>& nominal2,
        const Schedule& schedule1,
        const ext::shared_ptr<InterestRateIndex>& index1,
        const DayCounter& dayCount1,
        const Schedule& schedule2,
        const ext::shared_ptr<InterestRateIndex>& index2,
        const DayCounter& dayCount2,
        bool intermediateCapitalExchange = false,
        bool finalCapitalExchange = false,
        const std::vector<Real>& gearing1 = std::vector<Real>(),
        const std::vector<Real>& spread1 = std::vector<Real>(),
        const std::vector<Real>& cappedRate1 = std::vector<Real>(),
        const std::vector<Real>& flooredRate1 = std::vector<Real>(),
        const std::vector<Real>& gearing2 = std::vector<Real>(),
        const std::vector<Real>& spread2 = std::vector<Real>(),
        const std::vector<Real>& cappedRate2 = std::vector<Real>(),
        const std::vector<Real>& flooredRate2 = std::vector<Real>(),
        const boost::optional<BusinessDayConvention>& paymentConvention1 = boost::none,
        const boost::optional<BusinessDayConvention>& paymentConvention2 = boost::none);

    Swap::Type type() const;
    const std::vector<Real>& nominal1() const;
    const std::vector<Real>& nominal2() const;
    const Schedule& schedule1() const;
    const Schedule& schedule2() const;
    const ext::shared_ptr<InterestRateIndex>& index1() const;
    const ext::shared_ptr<InterestRateIndex>& index2() const;
    std::vector<Real> spread1() const;
    std::vector<Real> spread2() const;
    std::vector<Real> gearing1() const;
    std::vector<Real> gearing2() const;
    std::vector<Rate> cappedRate1() const;
    std::vector<Rate> flooredRate1() const;
    std::vector<Rate> cappedRate2() const;
    std::vector<Rate> flooredRate2() const;
    const DayCounter& dayCount1() const;
    const DayCounter& dayCount2() const;
    BusinessDayConvention paymentConvention1() const;
    BusinessDayConvention paymentConvention2() const;
    const Leg& leg1() const;
    const Leg& leg2() const;
};

%shared_ptr(IrregularSwap)
class IrregularSwap : public Swap {
  public:
    enum Type { Receiver = -1, Payer = 1 };
    class arguments;
    class results;
    class engine;
    IrregularSwap(
        IrregularSwap::Type type,
        const Leg& fixLeg,
        const Leg& floatLeg);

    IrregularSwap::Type type() const;
    const Leg& fixedLeg() const;
    const Leg& floatingLeg() const;
    Real fixedLegBPS() const;
    Real fixedLegNPV() const;
    Rate fairRate() const;
    Real floatingLegBPS() const;
    Real floatingLegNPV() const;
    Spread fairSpread() const;
};

%shared_ptr(OvernightIndexedSwap)
class OvernightIndexedSwap : public Swap {
  public:
    enum Type { Receiver = -1, Payer = 1 };

    OvernightIndexedSwap(
        OvernightIndexedSwap::Type type,
        Real nominal,
        const Schedule& schedule,
        Rate fixedRate,
        const DayCounter& fixedDC,
        const ext::shared_ptr<OvernightIndex>& index,
        Spread spread = 0.0,
        Natural paymentLag = 0,
        BusinessDayConvention paymentAdjustment = Following,
        Calendar paymentCalendar = Calendar(),
        bool telescopicValueDates = false,
        RateAveraging::Type averagingMethod = RateAveraging::Compound);
    OvernightIndexedSwap(
        OvernightIndexedSwap::Type type,
        std::vector<Real> nominals,
        const Schedule& schedule,
        Rate fixedRate,
        const DayCounter& fixedDC,
        const ext::shared_ptr<OvernightIndex>& index,
        Spread spread = 0.0,
        Natural paymentLag = 0,
        BusinessDayConvention paymentAdjustment = Following,
        Calendar paymentCalendar = Calendar(),
        bool telescopicValueDates = false,
        RateAveraging::Type averagingMethod = RateAveraging::Compound);

    OvernightIndexedSwap::Type type() const;
    Real nominal() const;
    std::vector<Real> nominals() const;
    Frequency paymentFrequency();
    Rate fixedRate() const;
    const DayCounter& fixedDayCount();
    const ext::shared_ptr<OvernightIndex>& overnightIndex();
    RateAveraging::Type averagingMethod();
    Spread spread() const;
    const Leg& fixedLeg() const;
    const Leg& overnightLeg() const;
    Real fixedLegBPS() const;
    Real fixedLegNPV() const;
    Real fairRate() const;
    Real overnightLegBPS() const;
    Real overnightLegNPV() const;
    Spread fairSpread() const;
};

%shared_ptr(VanillaSwap)
class VanillaSwap : public Swap {
  public:
    enum Type { Receiver = -1, Payer = 1 };
    VanillaSwap(
        VanillaSwap::Type type, Real nominal,
        const Schedule& fixedSchedule, Rate fixedRate,
        const DayCounter& fixedDayCount,
        const Schedule& floatSchedule,
        const ext::shared_ptr<IborIndex>& index,
        Spread spread,
        const DayCounter& floatingDayCount,
        boost::optional<BusinessDayConvention> paymentConvention = boost::none);

    VanillaSwap::Type type() const;
    Real nominal() const;
    const Schedule& fixedSchedule() const;
    Rate fixedRate() const;
    const DayCounter& fixedDayCount() const;
    const Schedule& floatingSchedule() const;
    const ext::shared_ptr<IborIndex>& iborIndex() const;
    Spread spread() const;
    const DayCounter& floatingDayCount() const;
    BusinessDayConvention paymentConvention() const;
    const Leg& fixedLeg() const;
    const Leg& floatingLeg() const;
    Real fixedLegBPS() const;
    Real fixedLegNPV() const;
    Rate fairRate() const;
    Real floatingLegBPS() const;
    Real floatingLegNPV() const;
    Spread fairSpread() const;
};

%shared_ptr(NonstandardSwap)
class NonstandardSwap : public Swap {
  public:
    NonstandardSwap(const VanillaSwap& fromVanilla);
    NonstandardSwap(
        VanillaSwap::Type type,
        const std::vector<Real>& fixedNominal,
        const std::vector<Real>& floatingNominal,
        const Schedule& fixedSchedule,
        const std::vector<Real>& fixedRate,
        const DayCounter& fixedDayCount,
        const Schedule& floatingSchedule,
        const ext::shared_ptr<IborIndex>& iborIndex,
        Real gearing,
        Spread spread,
        const DayCounter& floatingDayCount,
        bool intermediateCapitalExchange = false,
        bool finalCapitalExchange = false,
        boost::optional<BusinessDayConvention> paymentConvention = boost::none);
    NonstandardSwap(
        VanillaSwap::Type type,
        const std::vector<Real>& fixedNominal,
        const std::vector<Real>& floatingNominal,
        const Schedule& fixedSchedule,
        const std::vector<Real>& fixedRate,
        const DayCounter& fixedDayCount,
        const Schedule& floatingSchedule,
        const ext::shared_ptr<IborIndex>& iborIndex,
        const std::vector<Real>& gearing,
        const std::vector<Spread>& spread,
        const DayCounter& floatingDayCount,
        bool intermediateCapitalExchange = false,
        bool finalCapitalExchange = false,
        boost::optional<BusinessDayConvention> paymentConvention = boost::none);
    VanillaSwap::Type type() const;
    const std::vector<Real>& fixedNominal() const;
    const std::vector<Real>& floatingNominal() const;
    const Schedule& fixedSchedule() const;
    const std::vector<Real>& fixedRate() const;
    const DayCounter& fixedDayCount() const;
    const Schedule& floatingSchedule() const;
    const ext::shared_ptr<IborIndex>& iborIndex() const;
    Spread spread() const;
    Real gearing() const;
    const std::vector<Spread>& spreads() const;
    const std::vector<Real>& gearings() const;
    const DayCounter& floatingDayCount() const;
    BusinessDayConvention paymentConvention() const;
    const Leg& fixedLeg() const;
    const Leg& floatingLeg() const;
};

%shared_ptr(YearOnYearInflationSwap)
class YearOnYearInflationSwap : public Swap {
  public:
    enum Type { Receiver = -1, Payer = 1 };
    YearOnYearInflationSwap(
        YearOnYearInflationSwap::Type type,
        Real nominal,
        const Schedule& fixedSchedule,
        Rate fixedRate,
        const DayCounter& fixedDayCounter,
        const Schedule& yoySchedule,
        const ext::shared_ptr<YoYInflationIndex>& index,
        const Period& lag,
        Spread spread,
        const DayCounter& yoyDayCounter,
        const Calendar& paymentCalendar,
        BusinessDayConvention paymentConvention = Following);

    Real fixedLegNPV() const;
    Rate fairRate() const;
    Real yoyLegNPV() const;
    Spread fairSpread() const;
    YearOnYearInflationSwap::Type type() const;
    Real nominal() const;
    const Schedule& fixedSchedule() const;
    Rate fixedRate() const;
    const DayCounter& fixedDayCount() const;
    const Schedule& yoySchedule() const;
    const ext::shared_ptr<YoYInflationIndex>& yoyInflationIndex() const;
    Period observationLag() const;
    Spread spread() const;
    const DayCounter& yoyDayCount() const;
    Calendar paymentCalendar() const;
    BusinessDayConvention paymentConvention() const;
    const Leg& fixedLeg() const;
    const Leg& yoyLeg() const;
};

%shared_ptr(ZeroCouponInflationSwap)
class ZeroCouponInflationSwap : public Swap {
  public:
    enum Type { Receiver = -1, Payer = 1 };
    ZeroCouponInflationSwap(
        ZeroCouponInflationSwap::Type type,
        Real nominal,
        const Date& start,
        const Date& maturity,
        const Calendar& calendar,
        BusinessDayConvention convention,
        const DayCounter& dayCounter,
        Rate fixedRate,
        const ext::shared_ptr<ZeroInflationIndex>& index,
        const Period& lag,
        bool adjustInfObsDates = false,
        Calendar infCalendar = Calendar(),
        BusinessDayConvention infConvention = Following);

    ZeroCouponInflationSwap::Type type() const;
    Real nominal() const;
    Date startDate() const;
    Date maturityDate() const;
    Calendar fixedCalendar() const;
    BusinessDayConvention fixedConvention() const;
    DayCounter dayCounter() const;
    Rate fixedRate() const;
    ext::shared_ptr<ZeroInflationIndex> inflationIndex() const;
    Period observationLag() const;
    bool adjustObservationDates() const;
    Calendar inflationCalendar() const;
    BusinessDayConvention inflationConvention() const;
    const Leg& fixedLeg() const;
    const Leg& inflationLeg() const;

    Real fixedLegNPV() const;
    Real inflationLegNPV() const;
    Real fairRate() const;
};

%shared_ptr(ZeroCouponSwap)
class ZeroCouponSwap : public Swap {
  public:
    ZeroCouponSwap(Type type,
                   Real baseNominal,
                   const Date& startDate,
                   const Date& maturityDate,
                   Real fixedPayment,
                   ext::shared_ptr<IborIndex> iborIndex,
                   const Calendar& paymentCalendar,
                   BusinessDayConvention paymentConvention = Following,
                   Natural paymentDelay = 0);
    ZeroCouponSwap(Type type,
                   Real baseNominal,
                   const Date& startDate,
                   const Date& maturityDate,
                   Rate fixedRate,
                   const DayCounter& fixedDayCounter,
                   ext::shared_ptr<IborIndex> iborIndex,
                   const Calendar& paymentCalendar,
                   BusinessDayConvention paymentConvention = Following,
                   Natural paymentDelay = 0);

    Type type() const { return type_; }
    Real baseNominal() const { return baseNominal_; }
    Date startDate() const { return startDate_; }
    Date maturityDate() const { return maturityDate_; }
    const ext::shared_ptr<IborIndex>& iborIndex() const { return iborIndex_; }
    const Leg& fixedLeg() const;
    const Leg& floatingLeg() const;
    Real fixedPayment() const;
    Real fixedLegNPV() const;
    Real floatingLegNPV() const;
    Real fairFixedPayment() const;
    Rate fairFixedRate(const DayCounter& dayCounter) const;
};

class MakeOIS {
  public:
    MakeOIS(
        const Period& swapTenor,
        const ext::shared_ptr<OvernightIndex>& overnightIndex,
        Rate fixedRate = Null<Rate>(),
        const Period& fwdStart = 0*Days);

    %extend{
        ext::shared_ptr<OvernightIndexedSwap> makeOIS(){
            return (ext::shared_ptr<OvernightIndexedSwap>)(*$self);
        }
    }

    MakeOIS& receiveFixed(bool flag = true);
    MakeOIS& withType(OvernightIndexedSwap::Type type);
    MakeOIS& withNominal(Real n);
    MakeOIS& withSettlementDays(Natural settlementDays);
    MakeOIS& withEffectiveDate(const Date&);
    MakeOIS& withTerminationDate(const Date&);
    MakeOIS& withRule(DateGeneration::Rule r);
    MakeOIS& withPaymentFrequency(Frequency f);
    MakeOIS& withPaymentAdjustment(BusinessDayConvention convention);
    MakeOIS& withPaymentLag(Natural lag);
    MakeOIS& withPaymentCalendar(const Calendar& cal);
    MakeOIS& withEndOfMonth(bool flag = true);
    MakeOIS& withFixedLegDayCount(const DayCounter& dc);
    MakeOIS& withOvernightLegSpread(Spread sp);
    MakeOIS& withDiscountingTermStructure(
        const Handle<YieldTermStructure>& discountingTermStructure);
    MakeOIS& withTelescopicValueDates(bool telescopicValueDates);
    MakeOIS& withAveragingMethod(RateAveraging::Type averagingMethod);
    MakeOIS& withPricingEngine(
        const ext::shared_ptr<PricingEngine>& engine);
};

%pythoncode{
def MakeOIS(
        swapTenor,
        overnightIndex,
        fixedRate=None,
        fwdStart=Period(0, Days),
        receiveFixed=True,
        swapType=OvernightIndexedSwap.Payer,
        nominal=1.0,
        settlementDays=2,
        effectiveDate=None,
        terminationDate=None,
        dateGenerationRule=DateGeneration.Backward,
        paymentFrequency=Annual,
        paymentAdjustmentConvention=Following,
        paymentLag=0,
        paymentCalendar=None,
        endOfMonth=True,
        fixedLegDayCount=None,
        overnightLegSpread=0.0,
        discountingTermStructure=None,
        telescopicValueDates=False,
        pricingEngine=None,
        averagingMethod=None):
    mv = MakeOIS(
        swapTenor, overnightIndex, fixedRate, fwdStart)

    if not receiveFixed:
        mv.receiveFixed(receiveFixed)
    if swapType != OvernightIndexedSwap.Payer:
        mv.withType(swapType)
    if nominal != 1.0:
        mv.withNominal(nominal)
    if settlementDays != 2:
        mv.withSettlementDays(settlementDays)
    if effectiveDate is not None:
        mv.withEffectiveDate(effectiveDate)
    if terminationDate is not None:
        mv.withTerminationDate(terminationDate)
    if dateGenerationRule != DateGeneration.Backward:
        mv.withRule(dateGenerationRule)
    if paymentFrequency != Annual:
        mv.withPaymentFrequency(paymentFrequency)
    if paymentAdjustmentConvention != Following:
        mv.withPaymentAdjustment(paymentAdjustmentConvention)
    if paymentLag != 0:
        mv.withPaymentLag(paymentLag)
    if paymentCalendar is not None:
        mv.withPaymentCalendar(paymentCalendar)
    if not endOfMonth:
        mv.withEndOfMonth(endOfMonth)
    if fixedLegDayCount is not None:
        mv.withFixedLegDayCount(fixedLegDayCount)
    else:
        mv.withFixedLegDayCount(overnightIndex.dayCounter())
    if overnightLegSpread != 0.0:
        mv.withOvernightLegSpread(overnightLegSpread)
    if discountingTermStructure is not None:
        mv.withDiscountingTermStructure(discountingTermStructure)
    if telescopicValueDates:
        mv.withTelescopicValueDates(telescopicValueDates)
    if averagingMethod is not None:
        mv.withAveragingMethod(averagingMethod)
    if pricingEngine is not None:
        mv.withPricingEngine(pricingEngine)

    return mv.makeOIS()
}

class MakeVanillaSwap {
  public:
    MakeVanillaSwap(
        const Period& swapTenor,
        const ext::shared_ptr<IborIndex>& index,
        Rate fixedRate,
        const Period& forwardStart);
    %extend{
        ext::shared_ptr<VanillaSwap> makeVanillaSwap(){
            return (ext::shared_ptr<VanillaSwap>)(* $self);
        }
    }

    MakeVanillaSwap& receiveFixed(bool flag = true);
    MakeVanillaSwap& withType(VanillaSwap::Type type);
    MakeVanillaSwap& withNominal(Real n);
    MakeVanillaSwap& withSettlementDays(Natural settlementDays);
    MakeVanillaSwap& withEffectiveDate(const Date&);
    MakeVanillaSwap& withTerminationDate(const Date&);
    MakeVanillaSwap& withRule(DateGeneration::Rule r);
    MakeVanillaSwap& withFixedLegTenor(const Period& t);
    MakeVanillaSwap& withFixedLegCalendar(const Calendar& cal);
    MakeVanillaSwap& withFixedLegConvention(BusinessDayConvention bdc);
    MakeVanillaSwap& withFixedLegTerminationDateConvention(BusinessDayConvention bdc);
    MakeVanillaSwap& withFixedLegRule(DateGeneration::Rule r);
    MakeVanillaSwap& withFixedLegEndOfMonth(bool flag = true);
    MakeVanillaSwap& withFixedLegFirstDate(const Date& d);
    MakeVanillaSwap& withFixedLegNextToLastDate(const Date& d);
    MakeVanillaSwap& withFixedLegDayCount(const DayCounter& dc);
    MakeVanillaSwap& withFloatingLegTenor(const Period& t);
    MakeVanillaSwap& withFloatingLegCalendar(const Calendar& cal);
    MakeVanillaSwap& withFloatingLegConvention(BusinessDayConvention bdc);
    MakeVanillaSwap& withFloatingLegTerminationDateConvention(BusinessDayConvention bdc);
    MakeVanillaSwap& withFloatingLegRule(DateGeneration::Rule r);
    MakeVanillaSwap& withFloatingLegEndOfMonth(bool flag = true);
    MakeVanillaSwap& withFloatingLegFirstDate(const Date& d);
    MakeVanillaSwap& withFloatingLegNextToLastDate(const Date& d);
    MakeVanillaSwap& withFloatingLegDayCount(const DayCounter& dc);
    MakeVanillaSwap& withFloatingLegSpread(Spread sp);
    MakeVanillaSwap& withDiscountingTermStructure(const Handle<YieldTermStructure>& discountCurve);
    MakeVanillaSwap& withPricingEngine(const ext::shared_ptr<PricingEngine>& engine);
};

%pythoncode{
def MakeVanillaSwap(
        swapTenor, iborIndex, fixedRate, forwardStart,
        receiveFixed=None, swapType=None, Nominal=None, settlementDays=None,
        effectiveDate=None, terminationDate=None, dateGenerationRule=None,
        fixedLegTenor=None, fixedLegCalendar=None, fixedLegConvention=None,
        fixedLegDayCount=None, floatingLegTenor=None, floatingLegCalendar=None,
        floatingLegConvention=None, floatingLegDayCount=None, floatingLegSpread=None,
        discountingTermStructure=None, pricingEngine=None,
        fixedLegTerminationDateConvention=None,  fixedLegDateGenRule=None,
        fixedLegEndOfMonth=None, fixedLegFirstDate=None, fixedLegNextToLastDate=None,
        floatingLegTerminationDateConvention=None,  floatingLegDateGenRule=None,
        floatingLegEndOfMonth=None, floatingLegFirstDate=None, floatingLegNextToLastDate=None):
    mv = MakeVanillaSwap(swapTenor, iborIndex, fixedRate, forwardStart)
    if receiveFixed is not None:
        mv.receiveFixed(receiveFixed)
    if swapType is not None:
        mv.withType(swapType)
    if Nominal is not None:
        mv.withNominal(Nominal)
    if settlementDays is not None:
        mv.withSettlementDays(settlementDays)
    if effectiveDate is not None:
        mv.withEffectiveDate(effectiveDate)
    if terminationDate is not None:
        mv.withTerminationDate(terminationDate)
    if dateGenerationRule is not None:
        mv.withRule(dateGenerationRule)
    if fixedLegTenor is not None:
        mv.withFixedLegTenor(fixedLegTenor)
    if fixedLegCalendar is not None:
        mv.withFixedLegCalendar(fixedLegCalendar)
    if fixedLegConvention is not None:
        mv.withFixedLegConvention(fixedLegConvention)
    if fixedLegDayCount is not None:
        mv.withFixedLegDayCount(fixedLegDayCount)
    if floatingLegTenor is not None:
        mv.withFloatingLegTenor(floatingLegTenor)
    if floatingLegCalendar is not None:
        mv.withFloatingLegCalendar(floatingLegCalendar)
    if floatingLegConvention is not None:
        mv.withFloatingLegConvention(floatingLegConvention)
    if floatingLegDayCount is not None:
        mv.withFloatingLegDayCount(floatingLegDayCount)
    if floatingLegSpread is not None:
        mv.withFloatingLegSpread(floatingLegSpread)
    if discountingTermStructure is not None:
        mv.withDiscountingTermStructure(discountingTermStructure)
    if pricingEngine is not None:
        mv.withPricingEngine(pricingEngine)
    if fixedLegTerminationDateConvention is not None:
        mv.withFixedLegTerminationDateConvention(fixedLegTerminationDateConvention)
    if fixedLegDateGenRule is not None:
        mv.withFixedLegRule(fixedLegDateGenRule)
    if fixedLegEndOfMonth is not None:
        mv.withFixedLegEndOfMonth(fixedLegEndOfMonth)
    if fixedLegFirstDate is not None:
        mv.withFixedLegFirstDate(fixedLegFirstDate)
    if fixedLegNextToLastDate is not None:
        mv.withFixedLegNextToLastDate(fixedLegNextToLastDate)
    if floatingLegTerminationDateConvention is not None:
        mv.withFloatingLegTerminationDateConvention(floatingLegTerminationDateConvention)
    if floatingLegDateGenRule is not None:
        mv.withFloatingLegRule(floatingLegDateGenRule)
    if floatingLegEndOfMonth is not None:
        mv.withFloatingLegEndOfMonth(floatingLegEndOfMonth)
    if floatingLegFirstDate is not None:
        mv.withFloatingLegFirstDate(floatingLegFirstDate)
    if floatingLegNextToLastDate is not None:
        mv.withFloatingLegNextToLastDate(floatingLegNextToLastDate)
    return mv.makeVanillaSwap()
}

#endif
