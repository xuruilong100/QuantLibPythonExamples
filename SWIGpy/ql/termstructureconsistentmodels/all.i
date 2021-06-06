#ifndef ql_termstructureconsistentmodels_all_i
#define ql_termstructureconsistentmodels_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Gaussian1dModel;
using QuantLib::Gsr;
using QuantLib::MarkovFunctional;
%}

%shared_ptr(Gaussian1dModel)
class Gaussian1dModel : public TermStructureConsistentModel {
  public:
    const ext::shared_ptr<StochasticProcess1D> stateProcess() const;

    const Real numeraire(
        const Time t, const Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;
    const Real zerobond(
        const Time T, const Time t = 0.0,
        const Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>());
    const Real numeraire(
        const Date& referenceDate, const Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;
    const Real zerobond(
        const Date& maturity,
        const Date& referenceDate = Null<Date>(),
        const Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;
    const Real zerobondOption(
        const Option::Type& type, const Date& expiry, const Date& valueDate,
        const Date& maturity, const Rate strike,
        const Date& referenceDate = Null<Date>(), const Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>(),
        const Real yStdDevs = 7.0, const Size yGridPoints = 64,
        const bool extrapolatePayoff = true,
        const bool flatPayoffExtrapolation = false) const;
    const Real forwardRate(
        const Date& fixing,
        const Date& referenceDate = Null<Date>(),
        const Real y = 0.0,
        ext::shared_ptr<IborIndex> iborIdx = ext::shared_ptr<IborIndex>()) const;
    const Real swapRate(
        const Date& fixing, const Period& tenor,
        const Date& referenceDate = Null<Date>(),
        const Real y = 0.0,
        ext::shared_ptr<SwapIndex> swapIdx = ext::shared_ptr<SwapIndex>()) const;
    const Real swapAnnuity(
        const Date& fixing, const Period& tenor,
        const Date& referenceDate = Null<Date>(),
        const Real y = 0.0,
        ext::shared_ptr<SwapIndex> swapIdx = ext::shared_ptr<SwapIndex>()) const;
};

%shared_ptr(Gsr)
class Gsr : public Gaussian1dModel, public CalibratedModel {
  public:
    // constant mean reversion
    Gsr(const Handle<YieldTermStructure>& termStructure,
        const std::vector<Date>& volstepdates,
        const std::vector<Real>& volatilities,
        Real reversion,
        Real T = 60.0);
    // piecewise mean reversion (with same step dates as volatilities)
    Gsr(const Handle<YieldTermStructure>& termStructure,
        const std::vector<Date>& volstepdates,
        const std::vector<Real>& volatilities,
        const std::vector<Real>& reversions,
        Real T = 60.0);
    // constant mean reversion with floating model data
    Gsr(const Handle<YieldTermStructure>& termStructure,
        const std::vector<Date>& volstepdates,
        const std::vector<Handle<Quote> >& volatilities,
        const Handle<Quote>& reversion,
        Real T = 60.0);
    // piecewise mean reversion with floating model data
    Gsr(const Handle<YieldTermStructure>& termStructure,
        const std::vector<Date>& volstepdates,
        const std::vector<Handle<Quote> >& volatilities,
        const std::vector<Handle<Quote> >& reversions,
        Real T = 60.0);

    void calibrateVolatilitiesIterative(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper>>& helpers,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>());

    Real numeraireTime() const;
    void numeraireTime(Real T);
    const Array& reversion() const;
    const Array& volatility() const;

    void calibrateReversionsIterative(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper>>& instruments,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>());

    /* Array params() const;
    void setParams(const Array& params);
    Real value(
        const Array& params,
        const std::vector<ext::shared_ptr<CalibrationHelper> >& instruments);
    const ext::shared_ptr<Constraint>& constraint() const;
    EndCriteria::Type endCriteria() const;
    const Array& problemValues() const;
    Integer functionEvaluation() const; */
};

%rename (MarkovFunctionalSettings) MarkovFunctional::ModelSettings;
%feature ("flatnested") ModelSettings;
%shared_ptr(MarkovFunctional)
class MarkovFunctional : public Gaussian1dModel, public CalibratedModel {
  public:
    struct ModelSettings {
        enum Adjustments {
            AdjustNone = 0,
            AdjustDigitals = 1 << 0,
            AdjustYts = 1 << 1,
            ExtrapolatePayoffFlat = 1 << 2,
            NoPayoffExtrapolation = 1 << 3,
            KahaleSmile = 1 << 4,
            SmileExponentialExtrapolation = 1 << 5,
            KahaleInterpolation = 1 << 6,
            SmileDeleteArbitragePoints = 1 << 7,
            SabrSmile = 1 << 8
        };

        ModelSettings();

        ModelSettings &withYGridPoints(Size n);
        ModelSettings &withYStdDevs(Real s);
        ModelSettings &withGaussHermitePoints(Size n);
        ModelSettings &withDigitalGap(Real d);
        ModelSettings &withMarketRateAccuracy(Real a);
        ModelSettings &withUpperRateBound(Real u);
        ModelSettings &withLowerRateBound(Real l);
        ModelSettings &withAdjustments(int a);
        ModelSettings &addAdjustment(int a);
        ModelSettings &removeAdjustment(int a);
        ModelSettings &withSmileMoneynessCheckpoints(const std::vector<Real>& m);

        /* %extend {
            ModelSettings toInstance() {
                return *$self;
            }
        } */
    };

    // Constructor for a swaption smile calibrated model
    MarkovFunctional(
        const Handle<YieldTermStructure>& termStructure,
        const Real reversion,
        const std::vector<Date>& volstepdates,
        const std::vector<Real>& volatilities,
        const Handle<SwaptionVolatilityStructure>& swaptionVol,
        const std::vector<Date>& swaptionExpiries,
        const std::vector<Period>& swaptionTenors,
        const ext::shared_ptr<SwapIndex>& swapIndexBase,
        const MarkovFunctional::ModelSettings& modelSettings = ModelSettings());

    // Constructor for a caplet smile calibrated model
    MarkovFunctional(
        const Handle<YieldTermStructure>& termStructure,
        const Real reversion,
        const std::vector<Date>& volstepdates,
        const std::vector<Real>& volatilities,
        const Handle<OptionletVolatilityStructure>& capletVol,
        const std::vector<Date>& capletExpiries,
        const ext::shared_ptr<IborIndex>& iborIndex,
        const MarkovFunctional::ModelSettings& modelSettings = ModelSettings());

    const Date &numeraireDate() const;
    const Time &numeraireTime() const;

    const Array& volatility();

    void calibrate(
        const std::vector<ext::shared_ptr<CalibrationHelper> >& helper,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>(),
        const std::vector<bool>& fixParameters = std::vector<bool>());
    void calibrate(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper> >& helper,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>(),
        const std::vector<bool>& fixParameters = std::vector<bool>());

    std::vector<std::pair<Size, Size> > arbitrageIndices() const;
    void forceArbitrageIndices(
        const std::vector<std::pair<Size,Size> >& indices);
};

/* %pythoncode{
def MarkovFunctionalSettings(
        yGridPoints = None,
        yStdDevs = None,
        gaussHermitePoints = None,
        digitalGap = None,
        marketRateAccuracy = None,
        lowerRateBound = None,
        upperRateBound = None,
        adjustments = None,
        smileMoneynessCheckpoints = None):

    ms = _MarkovFunctionalSettings()

    if yGridPoints is not None:
        ms.withYGridPoints(yGridPoints)
    if yStdDevs is not None:
        ms.withYStdDevs(yGridPoints)
    if gaussHermitePoints is not None:
        ms.withGaussHermitePoints(yGridPoints)
    if digitalGap is not None:
        ms.withDigitalGap(yGridPoints)
    if marketRateAccuracy is not None:
        ms.withMarketRateAccuracy(yGridPoints)
    if lowerRateBound is not None:
        ms.withLowerRateBound(yGridPoints)
    if upperRateBound is not None:
        ms.withUpperRateBound(yGridPoints)
    if adjustments is not None:
        ms.withAdjustments(yGridPoints)
    if smileMoneynessCheckpoints is not None:
        ms.withYStdDevs(yGridPoints)

    return ms.settings()
} */

#endif
