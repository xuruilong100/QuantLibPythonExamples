#ifndef ql_base_i
#define ql_base_i

%include ../ql/common.i
%include ../ql/optimizers.i

%{
using QuantLib::Observable;
using QuantLib::Observer;
// C++ wrapper for Python observer
class PyObserver : public Observer {
  public:
    PyObserver(PyObject* callback)
        : callback_(callback) {
        /* make sure the Python object stays alive
           as long as we need it */
        Py_XINCREF(callback_);
    }
    PyObserver(const PyObserver& o)
        : callback_(o.callback_) {
        /* make sure the Python object stays alive
           as long as we need it */
        Py_XINCREF(callback_);
    }
    PyObserver& operator=(const PyObserver& o) {
        if ((this != &o) && (callback_ != o.callback_)) {
            Py_XDECREF(callback_);
            callback_ = o.callback_;
            Py_XINCREF(callback_);
        }
        return *this;
    }
    ~PyObserver() {
        // now it can go as far as we are concerned
        Py_XDECREF(callback_);
    }
    void update() {
        PyObject* pyResult = PyObject_CallFunction(
            callback_, NULL);
        QL_ENSURE(
            pyResult != NULL,
            "failed to notify Python observer");
        Py_XDECREF(pyResult);
    }

  private:
    PyObject* callback_;
};
%}
%{
using QuantLib::PricingEngine;
using QuantLib::Instrument;
using QuantLib::TermStructure;
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
%}

%shared_ptr(Observable);
class Observable {};

%extend Handle {
    ext::shared_ptr<Observable> asObservable() {
        return ext::shared_ptr<Observable>(*self);
    }
}

// Python wrapper
%rename(Observer) PyObserver;
class PyObserver {
    %rename(_registerWith) registerWith;
    %rename(_unregisterWith) unregisterWith;
  public:
    PyObserver(PyObject* callback);
    void registerWith(
        const ext::shared_ptr<Observable>&);
    void unregisterWith(
        const ext::shared_ptr<Observable>&);
    %pythoncode %{
        def registerWith(self,x):
            if hasattr(x, "asObservable"):
                self._registerWith(x.asObservable())
            else:
                self._registerWith(x)
        def unregisterWith(self,x):
            if hasattr(x, "asObservable"):
                self._unregisterWith(x.asObservable())
            else:
                self._unregisterWith(x)
    %}
};

%shared_ptr(PricingEngine)
class PricingEngine : public Observable {
  private:
    PricingEngine();
};

%shared_ptr(Instrument)
class Instrument : public Observable {
  public:
    Real NPV() const;
    Real errorEstimate() const;
    bool isExpired() const;
    void setPricingEngine(
        const ext::shared_ptr<PricingEngine>&);
    void recalculate();
    void freeze();
    void unfreeze();
  private:
    Instrument();
};

%template(InstrumentVector) std::vector<ext::shared_ptr<Instrument> >;

%shared_ptr(TermStructure);
class TermStructure : public Observable {
  private:
    TermStructure();
  public:
    DayCounter dayCounter() const;
    Time timeFromReference(const Date& date) const;
    Calendar calendar() const;
    Date referenceDate() const;
    Date maxDate() const;
    Time maxTime() const;
    // from Extrapolator, since we can't use multiple inheritance
    // and we're already inheriting from Observable
    void enableExtrapolation();
    void disableExtrapolation();
    bool allowsExtrapolation();
};

%shared_ptr(CashFlow)
class CashFlow : public Observable {
  private:
    CashFlow();
  public:
    Real amount() const;
    Date date() const;
    bool hasOccurred(const Date& refDate = Date()) const;
};

%template(Leg) std::vector<ext::shared_ptr<CashFlow> >;
typedef std::vector<ext::shared_ptr<CashFlow> > Leg;
%template(LegVector) std::vector<Leg>;

%shared_ptr(CalibratedModel)
class CalibratedModel : public virtual Observable {
  public:
    Array params() const;
    void setParams(const Array& params);

    virtual void calibrate(
        const std::vector<ext::shared_ptr<CalibrationHelper> >& helper,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>(),
        const std::vector<bool>& fixParameters = std::vector<bool>());
    virtual void calibrate(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper> >& helper,
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
    Integer functionEvaluation() const;

  private:
    CalibratedModel();
};

%shared_ptr(TermStructureConsistentModel)
class TermStructureConsistentModel : public virtual Observable{
  public:
    const Handle<YieldTermStructure>& termStructure() const;
  private:
    TermStructureConsistentModel();
};

%shared_ptr(Index)
class Index : public Observable {
  private:
    Index();

  public:
    std::string name() const;
    Calendar fixingCalendar() const;
    bool isValidFixingDate(
        const Date& fixingDate) const;
    Real fixing(
        const Date& fixingDate,
        bool forecastTodaysFixing = false) const;
    bool allowsNativeFixings();
    void addFixing(
        const Date& fixingDate, Rate fixing,
        bool forceOverwrite = false);
    void addFixings(
        const TimeSeries<Real>& t,
        bool forceOverwrite = false);
    const TimeSeries<Real>& timeSeries() const;
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
class SmileSection : public Observable {
  private:
    SmileSection();

  public:
    Real minStrike() const;
    Real maxStrike() const;
    Real atmLevel() const;
    Real variance(Rate strike) const;
    Volatility volatility(Rate strike) const;
    virtual const Date& exerciseDate() const;
    virtual VolatilityType volatilityType() const;
    virtual Rate shift() const;
    virtual const Date& referenceDate() const;
    virtual Time exerciseTime() const;
    virtual const DayCounter& dayCounter();
    virtual Real optionPrice(
        Rate strike,
        Option::Type type = Option::Call,
        Real discount = 1.0) const;
    virtual Real digitalOptionPrice(
        Rate strike,
        Option::Type type = Option::Call,
        Real discount = 1.0,
        Real gap = 1.0e-5) const;
    virtual Real vega(
        Rate strike,
        Real discount = 1.0) const;
    virtual Real density(
        Rate strike,
        Real discount = 1.0,
        Real gap = 1.0E-4) const;
    Volatility volatility(
        Rate strike,
        VolatilityType type,
        Real shift = 0.0) const;
};

%template(SmileSectionVector) std::vector<ext::shared_ptr<SmileSection> >;

%shared_ptr(DefaultProbabilityHelper)
class DefaultProbabilityHelper : public Observable {
  public:
    Handle<Quote> quote() const;
    Date latestDate() const;
    Date earliestDate() const;
    Date maturityDate() const;
    Date latestRelevantDate() const;
    Date pillarDate() const;
    Real impliedQuote() const;
    Real quoteError() const;
  private:
    DefaultProbabilityHelper();
};

%template(DefaultProbabilityHelperVector) std::vector<ext::shared_ptr<DefaultProbabilityHelper> >;

%shared_ptr(BootstrapHelper<ZeroInflationTermStructure>)
%shared_ptr(BootstrapHelper<YoYInflationTermStructure>)
%shared_ptr(BootstrapHelper<YoYOptionletVolatilitySurface>)
template <class TS>
class BootstrapHelper : public Observable {
  public:
    Handle<Quote> quote() const;
    Date latestDate() const;
	Date earliestDate() const;
	Date maturityDate() const;
	Date latestRelevantDate() const;
	Date pillarDate() const;
	Real impliedQuote() const;
	Real quoteError() const;
  private:
    BootstrapHelper();
};

%template(ZeroHelper) BootstrapHelper<ZeroInflationTermStructure>;
%template(YoYHelper) BootstrapHelper<YoYInflationTermStructure>;
%template(YoYOptionHelper) BootstrapHelper<YoYOptionletVolatilitySurface>;

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

%shared_ptr(RateHelper)
class RateHelper : public Observable {
  public:
    const Handle<Quote>& quote() const;
    Date latestDate() const;
	Date earliestDate() const;
	Date maturityDate() const;
	Date latestRelevantDate() const;
	Date pillarDate() const;
	Real impliedQuote() const;
	Real quoteError() const;
  private:
    RateHelper();
};

%shared_ptr(StochasticProcess)
class StochasticProcess : public Observable {
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
};

%template(StochasticProcessVector) std::vector<ext::shared_ptr<StochasticProcess> >;

%template(CalibrationErrorTuple) ext::tuple<Real, Real, Real>;
%template(CalibrationPair) std::pair< ext::shared_ptr<VanillaOption>, ext::shared_ptr<Quote> >;
%template(CalibrationSet) std::vector<std::pair< ext::shared_ptr<VanillaOption>, ext::shared_ptr<Quote> > >;

%shared_ptr(AndreasenHugeVolatilityInterpl)
class AndreasenHugeVolatilityInterpl : public Observable {
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

    // returns min, max and average error in volatility units
    ext::tuple<Real, Real, Real> calibrationError() const;

    // returns the option price of the calibration type. In case
    // of CallPut it return the call option price
    Real optionPrice(
        Time t, Real strike,
        Option::Type optionType) const;

    Volatility localVol(Time t, Real strike) const;
};

%shared_ptr(AffineModel)
class AffineModel : public virtual Observable {
  private:
    AffineModel();
  public:
    //! Implied discount curve
    virtual DiscountFactor discount(Time t) const;

    virtual Real discountBond(
        Time now,
        Time maturity,
        Array factors) const;

    virtual Real discountBondOption(
        Option::Type type,
        Real strike,
        Time maturity,
        Time bondMaturity) const;

    virtual Real discountBondOption(
        Option::Type type,
        Real strike,
        Time maturity,
        Time bondStart,
        Time bondMaturity) const;
};

#endif
