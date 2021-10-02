#ifndef ql_base_i
#define ql_base_i

%include ../ql/common.i
%include ../ql/optimizers.i

%{
using QuantLib::Observable;
using QuantLib::Observer;
using QuantLib::LazyObject;
%}
%{
using QuantLib::Extrapolator;
using QuantLib::PricingEngine;
using QuantLib::Instrument;
using QuantLib::TermStructure;
using QuantLib::Event;
using QuantLib::CashFlow;
using QuantLib::Leg;
using QuantLib::CalibratedModel;
using QuantLib::TermStructureConsistentModel;
using QuantLib::Index;
using QuantLib::SmileSection;
using QuantLib::DefaultProbabilityHelper;
using QuantLib::BootstrapHelper;
using QuantLib::Quote;
using QuantLib::RateHelper;
using QuantLib::StochasticProcess;
using QuantLib::AndreasenHugeVolatilityInterpl;
using QuantLib::AffineModel;
using QuantLib::FloatingRateCouponPricer;
using QuantLib::InflationCouponPricer;
%}

%{
typedef StochasticProcess::discretization discretization;
typedef PricingEngine::arguments arguments;
typedef PricingEngine::results results;
%}

%shared_ptr(Observable)
class Observable {
  private:
    Observable();
  public:
    void notifyObservers();
};

%shared_ptr(Observer);
class Observer {
  private:
    Observer();
  public:
    void registerWithObservables(
        const ext::shared_ptr<Observer>&);
    Size unregisterWith(
        const ext::shared_ptr<Observable>&);
    void unregisterWithAll();
    void update();
    void deepUpdate();
};

%shared_ptr(LazyObject);
class LazyObject : public Observer, public Observable {
  private:
    LazyObject();
  public:
    void recalculate();
    void freeze();
    void unfreeze();
    void alwaysForwardNotifications();
};

%shared_ptr(PricingEngine)
class PricingEngine : public Observable {
  private:
    PricingEngine();
  public:
    arguments* getArguments() const;
    const results* getResults() const;
};

class arguments {
  private:
    arguments();
};

class results {
  private:
    results();
};

%shared_ptr(Instrument)
class Instrument : public LazyObject {
  private:
    Instrument();
  public:
    Real NPV() const;
    Real errorEstimate() const;
    Date valuationDate() const;
    bool isExpired() const;
    void setPricingEngine(
        const ext::shared_ptr<PricingEngine>&);
    void setupArguments(PricingEngine::arguments*) const;
    void fetchResults(const PricingEngine::results*) const;
};

%template(InstrumentVector) std::vector<ext::shared_ptr<Instrument> >;

%shared_ptr(Extrapolator)
class Extrapolator {
  private:
    Extrapolator();
  public:
    void enableExtrapolation(bool b = true);
    void disableExtrapolation(bool b = true);
    bool allowsExtrapolation() const;
};

%shared_ptr(TermStructure)
class TermStructure : public Observer, public Observable, public Extrapolator {
  private:
    TermStructure();
  public:
    DayCounter dayCounter() const;
    Time timeFromReference(const Date& date) const;
    Date maxDate() const;
    Time maxTime() const;
    Date referenceDate() const;
    Calendar calendar() const;
    Natural settlementDays() const;
};

%shared_ptr(Event)
class Event : public Observable {
  private:
    Event();
  public:
    Date date() const;
    bool hasOccurred(
            const Date& refDate = Date(),
            boost::optional<bool> includeRefDate = boost::none) const;
};

%shared_ptr(CashFlow)
class CashFlow : public Event {
  private:
    CashFlow();
  public:
    Real amount() const;
    Date exCouponDate() const;
    bool tradingExCoupon(const Date &refDate=Date()) const;
};

%template(Leg) std::vector<ext::shared_ptr<CashFlow> >;
typedef std::vector<ext::shared_ptr<CashFlow> > Leg;
%template(LegVector) std::vector<Leg>;

%shared_ptr(CalibratedModel)
class CalibratedModel : public Observer, public Observable {
  private:
    CalibratedModel();
  public:
    void calibrate(
        const std::vector<ext::shared_ptr<CalibrationHelper> >& helper,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>(),
        const std::vector<bool>& fixParameters = std::vector<bool>());
    Real value(
        const Array& params,
        const std::vector<ext::shared_ptr<CalibrationHelper> >& helpers);
    const ext::shared_ptr<Constraint>& constraint() const;
    EndCriteria::Type endCriteria() const;
    const Array& problemValues() const;
    Array params() const;
    void setParams(const Array &params);
    Integer functionEvaluation() const;
};

%shared_ptr(TermStructureConsistentModel)
class TermStructureConsistentModel : public Observable{
  private:
    TermStructureConsistentModel();
  public:
    const Handle<YieldTermStructure>& termStructure() const;
};

%shared_ptr(Index)
class Index : public Observable {
  private:
    Index();

  public:
    std::string name() const;
    Calendar fixingCalendar() const;
    bool isValidFixingDate(const Date& fixingDate) const;
    bool hasHistoricalFixing(const Date& fixingDate) const;
    Real fixing(
        const Date& fixingDate,
        bool forecastTodaysFixing = false) const;
    const TimeSeries<Real>& timeSeries() const;
    bool allowsNativeFixings();
    void addFixing(
        const Date& fixingDate, Rate fixing,
        bool forceOverwrite = false);
    void addFixings(
        const TimeSeries<Real>& t,
        bool forceOverwrite = false);
    void clearFixings();
    %extend {
        void addFixings(
            const std::vector<Date>& fixingDates,
            const std::vector<Rate>& fixings,
            bool forceOverwrite = false) {
            self->addFixings(
                fixingDates.begin(), fixingDates.end(),
                fixings.begin(), forceOverwrite);
        }
        std::string __str__() {
            return self->name() + " index";
        }
    }
};

%shared_ptr(SmileSection);
class SmileSection : public Observer, public Observable {
  private:
    SmileSection();

  public:
    Real minStrike() const;
    Real maxStrike() const;
    Real variance(Rate strike) const;
    Volatility volatility(Rate strike) const;
    Real atmLevel() const;
    const Date& exerciseDate() const;
    VolatilityType volatilityType() const;
    Rate shift() const;
    const Date& referenceDate() const;
    Time exerciseTime() const;
    const DayCounter& dayCounter();
    Real optionPrice(
        Rate strike,
        Option::Type type = Option::Call,
        Real discount = 1.0) const;
    Real digitalOptionPrice(
        Rate strike,
        Option::Type type = Option::Call,
        Real discount = 1.0,
        Real gap = 1.0e-5) const;
    Real vega(
        Rate strike,
        Real discount = 1.0) const;
    Real density(
        Rate strike,
        Real discount = 1.0,
        Real gap = 1.0E-4) const;
    Volatility volatility(
        Rate strike,
        VolatilityType type,
        Real shift = 0.0) const;
};

%template(SmileSectionVector) std::vector<ext::shared_ptr<SmileSection> >;

%shared_ptr(BootstrapHelper<YieldTermStructure>)
%shared_ptr(BootstrapHelper<DefaultProbabilityTermStructure>)
%shared_ptr(BootstrapHelper<ZeroInflationTermStructure>)
%shared_ptr(BootstrapHelper<YoYInflationTermStructure>)
%shared_ptr(BootstrapHelper<YoYOptionletVolatilitySurface>)
template <class TS>
class BootstrapHelper : public Observer, public Observable {
  private:
    BootstrapHelper();
  public:
    const Handle<Quote>& quote() const;
    Real impliedQuote() const;
    Real quoteError() const;
    void setTermStructure(TS *);
    Date earliestDate() const;
    Date maturityDate() const;
    Date latestRelevantDate() const;
    Date pillarDate() const;
    Date latestDate() const;
};

%template(RateHelper) BootstrapHelper<YieldTermStructure>;
%template(DefaultProbabilityHelper) BootstrapHelper<DefaultProbabilityTermStructure>;
%template(ZeroHelper) BootstrapHelper<ZeroInflationTermStructure>;
%template(YoYHelper) BootstrapHelper<YoYInflationTermStructure>;
%template(YoYOptionHelper) BootstrapHelper<YoYOptionletVolatilitySurface>;

%template(RateHelperVector) std::vector<ext::shared_ptr<BootstrapHelper<YieldTermStructure> > >;
%template(DefaultProbabilityHelperVector) std::vector<ext::shared_ptr<BootstrapHelper<DefaultProbabilityTermStructure> > >;
%template(ZeroHelperVector) std::vector<ext::shared_ptr<BootstrapHelper<ZeroInflationTermStructure> > >;
%template(YoYHelperVector) std::vector<ext::shared_ptr<BootstrapHelper<YoYInflationTermStructure> > >;
%template(YoYOptionHelperVector) std::vector<ext::shared_ptr<BootstrapHelper<YoYOptionletVolatilitySurface> > >;

%shared_ptr(Quote)
class Quote : public Observable {
  private:
    Quote();
  public:
    Real value() const;
    bool isValid() const;
};

%template(QuoteHandle) Handle<Quote>;
%template(RelinkableQuoteHandle) RelinkableHandle<Quote>;

// typedef BootstrapHelper<YieldTermStructure> RateHelper;
/* %shared_ptr(RateHelper)
class RateHelper : public Observer, public Observable {
  private:
    RateHelper();
  public:
    const Handle<Quote>& quote() const;
    Date latestDate() const;
    Date earliestDate() const;
    Date maturityDate() const;
    Date latestRelevantDate() const;
    Date pillarDate() const;
    Real impliedQuote() const;
    Real quoteError() const;
}; */

%shared_ptr(discretization)
class discretization {
  private:
    discretization();
  public:
    Array drift(
        const StochasticProcess&,
        Time t0, const Array& x0,
        Time dt) const;
    Matrix diffusion(
        const StochasticProcess&,
        Time t0, const Array& x0,
        Time dt) const;
    Matrix covariance(
        const StochasticProcess&,
        Time t0, const Array& x0,
        Time dt) const;
};

%shared_ptr(StochasticProcess)
class StochasticProcess : public Observer, public Observable {
  private:
    StochasticProcess();

  public:
    Size size() const;
    Size factors() const;
    Array initialValues() const;
    Array drift(Time t, const Array& x) const;
    Matrix diffusion(Time t, const Array& x) const;
    Array expectation(
        Time t0, const Array& x0, Time dt) const;
    Matrix stdDeviation(
        Time t0, const Array& x0, Time dt) const;
    Matrix covariance(
        Time t0, const Array& x0, Time dt) const;
    Array evolve(
        Time t0, const Array& x0,
        Time dt, const Array& dw) const;
    Array apply(
        const Array& x0,
        const Array& dx) const;
    Time time(const Date&) const;
};

%template(StochasticProcessVector) std::vector<ext::shared_ptr<StochasticProcess> >;

%template(CalibrationErrorTuple) ext::tuple<Real, Real, Real>;
%template(CalibrationPair) std::pair< ext::shared_ptr<VanillaOption>, ext::shared_ptr<Quote> >;
%template(CalibrationSet) std::vector<std::pair< ext::shared_ptr<VanillaOption>, ext::shared_ptr<Quote> > >;

%shared_ptr(AndreasenHugeVolatilityInterpl)
class AndreasenHugeVolatilityInterpl : public LazyObject {
  public:
    enum InterpolationType {
        PiecewiseConstant,
        Linear,
        CubicSpline
    };
    enum CalibrationType {
        Call = 1,    // Option::Call,
        Put = -1,    // Option::Put,
        CallPut
    };

    typedef std::vector<std::pair<ext::shared_ptr<VanillaOption>, ext::shared_ptr<Quote>>> CalibrationSet;

    AndreasenHugeVolatilityInterpl(
        const CalibrationSet& calibrationSet,
        const Handle<Quote>& spot,
        const Handle<YieldTermStructure>& rTS,
        const Handle<YieldTermStructure>& qTS,
        InterpolationType interpolationType = CubicSpline,
        CalibrationType calibrationType = Call,
        Size nGridPoints = 500,
        Real minStrike = Null<Real>(),
        Real maxStrike = Null<Real>(),
        const ext::shared_ptr<OptimizationMethod>& optimizationMethod =
            ext::shared_ptr<OptimizationMethod>(new LevenbergMarquardt),
        const EndCriteria& endCriteria = EndCriteria(
            500, 100, 1e-12, 1e-10, 1e-10));

    Date maxDate() const;
    Real minStrike() const;
    Real maxStrike() const;
    Real fwd(Time t) const;
    const Handle<YieldTermStructure>& riskFreeRate() const;
    ext::tuple<Real, Real, Real> calibrationError() const;
    Real optionPrice(
        Time t, Real strike,
        Option::Type optionType) const;
    Volatility localVol(Time t, Real strike) const;
};

%shared_ptr(AffineModel)
class AffineModel : public Observable {
  private:
    AffineModel();
  public:
    //! Implied discount curve
    DiscountFactor discount(Time t) const;
    Real discountBond(
        Time now,
        Time maturity,
        Array factors) const;
    Real discountBondOption(
        Option::Type type,
        Real strike,
        Time maturity,
        Time bondMaturity) const;
    Real discountBondOption(
        Option::Type type,
        Real strike,
        Time maturity,
        Time bondStart,
        Time bondMaturity) const;
};

%shared_ptr(FloatingRateCouponPricer)
class FloatingRateCouponPricer : public Observer, public Observable {
  private:
    FloatingRateCouponPricer();
  public:
    Real swapletPrice() const;
    Rate swapletRate() const;
    Real capletPrice(Rate effectiveCap) const;
    Rate capletRate(Rate effectiveCap) const;
    Real floorletPrice(Rate effectiveFloor) const;
    Rate floorletRate(Rate effectiveFloor) const;
    void initialize(const FloatingRateCoupon &coupon);
};

%template(FloatingRateCouponPricerVector) std::vector<ext::shared_ptr<FloatingRateCouponPricer> >;

void setCouponPricer(
    const Leg&,
    const ext::shared_ptr<FloatingRateCouponPricer>&);

void setCouponPricers(
    const Leg& leg,
    const std::vector<ext::shared_ptr<FloatingRateCouponPricer> >&);

void setCouponPricers(
    const Leg& leg,
    const ext::shared_ptr<FloatingRateCouponPricer>&,
    const ext::shared_ptr<FloatingRateCouponPricer>&);

void setCouponPricers(
    const Leg& leg,
    const ext::shared_ptr<FloatingRateCouponPricer>&,
    const ext::shared_ptr<FloatingRateCouponPricer>&,
    const ext::shared_ptr<FloatingRateCouponPricer>&);

void setCouponPricers(
    const Leg& leg,
    const ext::shared_ptr<FloatingRateCouponPricer>&,
    const ext::shared_ptr<FloatingRateCouponPricer>&,
    const ext::shared_ptr<FloatingRateCouponPricer>&,
    const ext::shared_ptr<FloatingRateCouponPricer>&);

%shared_ptr(InflationCouponPricer)
class InflationCouponPricer: public Observer, public Observable {
  private:
    InflationCouponPricer();
  public:
    Real swapletPrice() const;
    Rate swapletRate() const;
    Real capletPrice(Rate effectiveCap) const;
    Rate capletRate(Rate effectiveCap) const;
    Real floorletPrice(Rate effectiveFloor) const;
    Rate floorletRate(Rate effectiveFloor) const;
    void initialize(const InflationCoupon&);
};


%{
struct IterativeBootstrap {
    Real accuracy;
    Real minValue, maxValue;
    Size maxAttempts;
    Real maxFactor, minFactor;
    bool dontThrow;
    Size dontThrowSteps;
    IterativeBootstrap(
        Real accuracy = Null<Real>(),
        Real minValue = Null<Real>(),
        Real maxValue = Null<Real>(),
        Size maxAttempts = 1,
        Real maxFactor = 2.0,
        Real minFactor = 2.0,
        bool dontThrow = false,
        Size dontThrowSteps = 10)
        : accuracy(accuracy),
          minValue(minValue),
          maxValue(maxValue),
          maxAttempts(maxAttempts),
          maxFactor(maxFactor),
          minFactor(minFactor),
          dontThrow(dontThrow),
          dontThrowSteps(dontThrowSteps) {}
};

struct GlobalBootstrap {
    std::vector<ext::shared_ptr<RateHelper>> additionalHelpers;
    std::vector<Date> additionalDates;
    double accuracy;
    GlobalBootstrap(double accur = Null<double>())
        : accuracy(accur) {}
    GlobalBootstrap(
        const std::vector<ext::shared_ptr<RateHelper>>& additionHelpers,
        const std::vector<Date>& additionDates,
        double accur = Null<double>())
        : additionalHelpers(additionHelpers),
          additionalDates(additionDates),
          accuracy(accur) {}
};
%}

struct IterativeBootstrap {
    %feature("kwargs") IterativeBootstrap;
    IterativeBootstrap(
        Real accuracy = Null<Real>(),
        Real minValue = Null<Real>(),
        Real maxValue = Null<Real>(),
        Size maxAttempts = 1,
        Real maxFactor = 2.0,
        Real minFactor = 2.0,
        bool dontThrow = false,
        Size dontThrowSteps = 10);
};

struct GlobalBootstrap {
    GlobalBootstrap(
        Real accuracy = Null<double>());
    GlobalBootstrap(
        const std::vector<ext::shared_ptr<RateHelper> >& additionalHelpers,
        const std::vector<Date>& additionalDates,
        Real accuracy = Null<double>());
};

#endif
