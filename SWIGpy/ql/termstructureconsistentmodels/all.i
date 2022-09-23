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
class Gaussian1dModel : public TermStructureConsistentModel, public LazyObject {
  public:
    ext::shared_ptr<StochasticProcess1D> stateProcess() const;
    Real numeraire(
        Time t, Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;
    Real zerobond(
        Time T, Time t = 0.0, Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;
    Real numeraire(
        const Date& referenceDate, Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;
    Real zerobond(
        const Date& maturity,
        const Date& referenceDate = Null<Date>(), Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;
    Real zerobondOption(
        const Option::Type& type, const Date& expiry,
        const Date& valueDate, const Date& maturity, Rate strike,
        const Date& referenceDate = Null<Date>(), Real y = 0.0,
        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>(),
        Real yStdDevs = 7.0, Size yGridPoints = 64,
        bool extrapolatePayoff = true,
        bool flatPayoffExtrapolation = false) const;
    Real forwardRate(
        const Date& fixing,
        const Date& referenceDate = Null<Date>(),
        Real y = 0.0,
        const ext::shared_ptr<IborIndex>& iborIdx = ext::shared_ptr<IborIndex>()) const;
    Real swapRate(
        const Date& fixing, const Period& tenor,
        const Date& referenceDate = Null<Date>(), Real y = 0.0,
        const ext::shared_ptr<SwapIndex>& swapIdx = ext::shared_ptr<SwapIndex>()) const;
    Real swapAnnuity(
        const Date& fixing, const Period& tenor,
        const Date& referenceDate = Null<Date>(), Real y = 0.0,
        const ext::shared_ptr<SwapIndex>& swapIdx = ext::shared_ptr<SwapIndex>()) const;
    Array yGrid(
        Real yStdDevs, int gridPoints,
        Real T = 1.0, Real t = 0, Real y = 0) const;
    static Real gaussianPolynomialIntegral(
        Real a, Real b, Real c, Real d, Real e, Real x0, Real x1);
    static Real gaussianShiftedPolynomialIntegral(
        Real a, Real b, Real c, Real d, Real e, Real h, Real x0, Real x1);
};

%shared_ptr(Gsr)
class Gsr : public Gaussian1dModel, public CalibratedModel {
  public:
    Gsr(const Handle<YieldTermStructure>& termStructure,
        std::vector<Date> volstepdates,
        const std::vector<Real>& volatilities,
        Real reversion,
        Real T = 60.0);
    Gsr(const Handle<YieldTermStructure>& termStructure,
        std::vector<Date> volstepdates,
        const std::vector<Real>& volatilities,
        const std::vector<Real>& reversions,
        Real T = 60.0);
    Gsr(const Handle<YieldTermStructure>& termStructure,
        std::vector<Date> volstepdates,
        std::vector<Handle<Quote>> volatilities,
        const Handle<Quote>& reversion,
        Real T = 60.0);
    Gsr(const Handle<YieldTermStructure>& termStructure,
        std::vector<Date> volstepdates,
        std::vector<Handle<Quote>> volatilities,
        std::vector<Handle<Quote>> reversions,
        Real T = 60.0);

    Real numeraireTime() const;
    void numeraireTime(Real T);
    const Array& reversion() const;
    const Array& volatility() const;
    std::vector<bool> FixedReversions();
    std::vector<bool> FixedVolatilities();
    std::vector<bool> MoveVolatility(Size i);
    std::vector<bool> MoveReversion(Size i);
    void calibrateVolatilitiesIterative(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper>>& helpers,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>());
    void calibrateReversionsIterative(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper>>& instruments,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>());
};

%rename (MarkovFunctionalSettings) MarkovFunctional::ModelSettings;
%rename (MarkovFunctionalOutputs) MarkovFunctional::ModelOutputs;
%feature ("flatnested") ModelSettings;
%feature ("flatnested") ModelOutputs;
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

        ModelSettings& withYGridPoints(Size n);
        ModelSettings& withYStdDevs(Real s);
        ModelSettings& withGaussHermitePoints(Size n);
        ModelSettings& withDigitalGap(Real d);
        ModelSettings& withMarketRateAccuracy(Real a);
        ModelSettings& withUpperRateBound(Real u);
        ModelSettings& withLowerRateBound(Real l);
        ModelSettings& withAdjustments(int a);
        ModelSettings& addAdjustment(int a);
        ModelSettings& removeAdjustment(int a);
        ModelSettings& withSmileMoneynessCheckpoints(const std::vector<Real>& m);

        Size yGridPoints_ = 64;
        Real yStdDevs_ = 7.0;
        Size gaussHermitePoints_ = 32;
        Real digitalGap_ = 1E-5, marketRateAccuracy_ = 1E-7;
        Real lowerRateBound_ = 0.0, upperRateBound_ = 2.0;
        int adjustments_;
        std::vector<Real> smileMoneynessCheckpoints_;
        //ext::shared_ptr<CustomSmileFactory> customSmileFactory_;
    };

    struct ModelOutputs {
        bool dirty_;
        ModelSettings settings_;
        std::vector<Date> expiries_;
        std::vector<Period> tenors_;
        std::vector<Real> atm_;
        std::vector<Real> annuity_;
        std::vector<Real> adjustmentFactors_;
        std::vector<Real> digitalsAdjustmentFactors_;
        std::vector<std::string> messages_;
        std::vector<std::vector<Real>> smileStrikes_;
        std::vector<std::vector<Real>> marketRawCallPremium_;
        std::vector<std::vector<Real>> marketRawPutPremium_;
        std::vector<std::vector<Real>> marketCallPremium_;
        std::vector<std::vector<Real>> marketPutPremium_;
        std::vector<std::vector<Real>> modelCallPremium_;
        std::vector<std::vector<Real>> modelPutPremium_;
        std::vector<std::vector<Real>> marketVega_;
        std::vector<Real> marketZerorate_;
        std::vector<Real> modelZerorate_;
    };

    MarkovFunctional(
        const Handle<YieldTermStructure>& termStructure,
        Real reversion,
        std::vector<Date> volstepdates,
        std::vector<Real> volatilities,
        const Handle<SwaptionVolatilityStructure>& swaptionVol,
        const std::vector<Date>& swaptionExpiries,
        const std::vector<Period>& swaptionTenors,
        const ext::shared_ptr<SwapIndex>& swapIndexBase,
        MarkovFunctional::ModelSettings modelSettings = ModelSettings());
    MarkovFunctional(
        const Handle<YieldTermStructure>& termStructure,
        Real reversion,
        std::vector<Date> volstepdates,
        std::vector<Real> volatilities,
        const Handle<OptionletVolatilityStructure>& capletVol,
        const std::vector<Date>& capletExpiries,
        ext::shared_ptr<IborIndex> iborIndex,
        MarkovFunctional::ModelSettings modelSettings = ModelSettings());

    const ModelSettings& modelSettings() const;
    const ModelOutputs& modelOutputs() const;
    const Date& numeraireDate() const;
    const Time& numeraireTime() const;
    const Array& volatility();

    void calibrate(
        const std::vector<ext::shared_ptr<CalibrationHelper>>& helper,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>(),
        const std::vector<bool>& fixParameters = std::vector<bool>());
    void calibrate(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper>>& helper,
        OptimizationMethod& method,
        const EndCriteria& endCriteria,
        const Constraint& constraint = Constraint(),
        const std::vector<Real>& weights = std::vector<Real>(),
        const std::vector<bool>& fixParameters = std::vector<bool>());

    std::vector<std::pair<Size, Size>> arbitrageIndices() const;
    void forceArbitrageIndices(
        const std::vector<std::pair<Size,Size>>& indices);
};

#endif
