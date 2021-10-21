#ifndef ql_termstructures_volatilitytermstructures_swaptionvol_all_i
#define ql_termstructures_volatilitytermstructures_swaptionvol_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/volatilitytermstructures/SwaptionVolatilityStructure.i

%{
using QuantLib::ConstantSwaptionVolatility;
using QuantLib::Gaussian1dSwaptionVolatility;
using QuantLib::SpreadedSwaptionVolatility;
using QuantLib::TenorSwaptionVTS;
%}

%{
using QuantLib::SwaptionVolCubeSabrModel;
using QuantLib::SwaptionVolatilityDiscrete;
using QuantLib::SwaptionVolatilityCube;
using QuantLib::SwaptionVolatilityMatrix;
using QuantLib::SwaptionVolCube1x;
using QuantLib::SwaptionVolCube2;
%}

%shared_ptr(ConstantSwaptionVolatility)
class ConstantSwaptionVolatility : public SwaptionVolatilityStructure {
  public:
    ConstantSwaptionVolatility(
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc,
        const Handle<Quote>& volatility,
        const DayCounter& dc,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantSwaptionVolatility(
        const Date& referenceDate,
        const Calendar& cal,
        BusinessDayConvention bdc,
        const Handle<Quote>& volatility,
        const DayCounter& dc,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantSwaptionVolatility(
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Volatility volatility,
        const DayCounter& dc,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
    ConstantSwaptionVolatility(
        const Date& referenceDate,
        const Calendar& cal,
        BusinessDayConvention bdc,
        Volatility volatility,
        const DayCounter& dc,
        const VolatilityType type = ShiftedLognormal,
        const Real shift = 0.0);
};

%shared_ptr(Gaussian1dSwaptionVolatility)
class Gaussian1dSwaptionVolatility : public SwaptionVolatilityStructure {
  public:
    Gaussian1dSwaptionVolatility(
        const Calendar& cal,
        BusinessDayConvention bdc,
        ext::shared_ptr<SwapIndex> indexBase,
        const ext::shared_ptr<Gaussian1dModel>& model,
        const DayCounter& dc,
        ext::shared_ptr<Gaussian1dSwaptionEngine> swaptionEngine = ext::shared_ptr<Gaussian1dSwaptionEngine>());
};

%shared_ptr(SpreadedSwaptionVolatility)
class SpreadedSwaptionVolatility : public SwaptionVolatilityStructure {
  public:
    SpreadedSwaptionVolatility(
        const Handle<SwaptionVolatilityStructure>&,
        Handle<Quote> spread);
};

%shared_ptr(TenorSwaptionVTS)
class TenorSwaptionVTS : public SwaptionVolatilityStructure {
  public:
    TenorSwaptionVTS(const Handle<SwaptionVolatilityStructure>& baseVTS,
                     Handle<YieldTermStructure> discountCurve,
                     ext::shared_ptr<IborIndex> baseIndex,
                     ext::shared_ptr<IborIndex> targIndex,
                     const Period& baseFixedFreq,
                     const Period& targFixedFreq,
                     DayCounter baseFixedDC,
                     DayCounter targFixedDC);
};

%shared_ptr(SwaptionVolatilityDiscrete)
class SwaptionVolatilityDiscrete : public SwaptionVolatilityStructure {
    private:
        SwaptionVolatilityDiscrete();
    public:
        const std::vector<Period>& optionTenors() const;
        const std::vector<Date>& optionDates() const;
        const std::vector<Time>& optionTimes() const;
        const std::vector<Period>& swapTenors() const;
        const std::vector<Time>& swapLengths() const;
        const Date optionDateFromTime(Time optionTime) const;
};

%shared_ptr(SwaptionVolatilityMatrix)
class SwaptionVolatilityMatrix : public SwaptionVolatilityDiscrete {
  public:
    SwaptionVolatilityMatrix(
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const std::vector<std::vector<Handle<Quote>>>& vols,
        const DayCounter& dayCounter,
        bool flatExtrapolation = false,
        VolatilityType type = ShiftedLognormal,
        const std::vector<std::vector<Real>>& shifts = std::vector<std::vector<Real>>());
    SwaptionVolatilityMatrix(
        const Date& referenceDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const std::vector<std::vector<Handle<Quote>>>& vols,
        const DayCounter& dayCounter,
        bool flatExtrapolation = false,
        VolatilityType type = ShiftedLognormal,
        const std::vector<std::vector<Real>>& shifts = std::vector<std::vector<Real>>());
    SwaptionVolatilityMatrix(
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const Matrix& volatilities,
        const DayCounter& dayCounter,
        bool flatExtrapolation = false,
        VolatilityType type = ShiftedLognormal,
        const Matrix& shifts = Matrix());
    SwaptionVolatilityMatrix(
        const Date& referenceDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const Matrix& volatilities,
        const DayCounter& dayCounter,
        bool flatExtrapolation = false,
        VolatilityType type = ShiftedLognormal,
        const Matrix& shifts = Matrix());
    SwaptionVolatilityMatrix(
        const Date& referenceDate,
        const Calendar& calendar,
        BusinessDayConvention bdc,
        const std::vector<Date>& optionDates,
        const std::vector<Period>& swapTenors,
        const Matrix& volatilities,
        const DayCounter& dayCounter,
        bool flatExtrapolation = false,
        VolatilityType type = ShiftedLognormal,
        const Matrix& shifts = Matrix());

    std::pair<Size, Size> locate(
        const Date& optionDate,
        const Period& swapTenor) const;
    std::pair<Size, Size> locate(
        Time optionTime,
        Time swapLength) const;
};

%shared_ptr(SwaptionVolatilityCube)
class SwaptionVolatilityCube : public SwaptionVolatilityDiscrete {
  private:
    SwaptionVolatilityCube();
  public:
    Rate atmStrike(
        const Date& optionDate,
        const Period& swapTenor) const;
    Rate atmStrike(
        const Period& optionTenor,
        const Period& swapTenor) const;
    Handle<SwaptionVolatilityStructure> atmVol() const;
    const std::vector<Spread>& strikeSpreads() const;
    const std::vector<std::vector<Handle<Quote>>>& volSpreads() const;
    ext::shared_ptr<SwapIndex> swapIndexBase() const;
    ext::shared_ptr<SwapIndex> shortSwapIndexBase() const;
    bool vegaWeightedSmileFit() const;
};

struct SwaptionVolCubeSabrModel { };

%shared_ptr(SwaptionVolCube1x<SwaptionVolCubeSabrModel>)
template<class Model>
class SwaptionVolCube1x : public SwaptionVolatilityCube {
  public:
    SwaptionVolCube1x(
        const Handle<SwaptionVolatilityStructure>& atmVolStructure,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const std::vector<Spread>& strikeSpreads,
        const std::vector<std::vector<Handle<Quote>>>& volSpreads,
        const ext::shared_ptr<SwapIndex>& swapIndexBase,
        const ext::shared_ptr<SwapIndex>& shortSwapIndexBase,
        bool vegaWeightedSmileFit,
        std::vector<std::vector<Handle<Quote>>> parametersGuess,
        std::vector<bool> isParameterFixed,
        bool isAtmCalibrated,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        Real maxErrorTolerance = Null<Real>(),
        ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>(),
        Real errorAccept = Null<Real>(),
        bool useMaxError = false,
        Size maxGuesses = 50,
        bool backwardFlat = false,
        Real cutoffStrike = 0.0001);
    ext::shared_ptr<SmileSection> smileSectionImpl(
        Time optionTime,
        Time swapLength) const;
    const Matrix& marketVolCube(Size i) const;
    Matrix sparseSabrParameters()const;
    Matrix denseSabrParameters() const;
    Matrix marketVolCube() const;
    Matrix volCubeAtmCalibrated() const;
    void recalibration(Real beta,
                       const Period& swapTenor);
    void recalibration(const std::vector<Real>& beta,
                       const Period& swapTenor);
    void recalibration(const std::vector<Period>& swapLengths,
                       const std::vector<Real>& beta,
                       const Period& swapTenor);
    void updateAfterRecalibration();
};

%template(SwaptionVolCube1) SwaptionVolCube1x<SwaptionVolCubeSabrModel>;

%shared_ptr(SwaptionVolCube2)
class SwaptionVolCube2 : public SwaptionVolatilityCube {
  public:
    SwaptionVolCube2(
        const Handle<SwaptionVolatilityStructure>& atmVolStructure,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const std::vector<Spread>& strikeSpreads,
        const std::vector<std::vector<Handle<Quote>>>& volSpreads,
        const ext::shared_ptr<SwapIndex>& swapIndex,
        const ext::shared_ptr<SwapIndex>& shortSwapIndex,
        bool vegaWeightedSmileFit);
    const Matrix& volSpreads(Size i) const;
};

#endif
