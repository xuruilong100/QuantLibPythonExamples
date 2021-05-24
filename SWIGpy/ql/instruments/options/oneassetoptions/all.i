#ifndef ql_instruments_options_oneassetoptions_all_i
#define ql_instruments_options_oneassetoptions_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/instruments/options/OneAssetOption.i

%{
using QuantLib::Average;
using QuantLib::Barrier;
using QuantLib::DoubleBarrier;
using QuantLib::PartialBarrier;
using QuantLib::ContinuousAveragingAsianOption;

using QuantLib::CliquetOption;
using QuantLib::ComplexChooserOption;
using QuantLib::CompoundOption;
using QuantLib::HolderExtensibleOption;
using QuantLib::PartialTimeBarrierOption;
using QuantLib::SimpleChooserOption;
using QuantLib::VanillaStorageOption;
using QuantLib::WriterExtensibleOption;
using QuantLib::QuantoBarrierOption;

using QuantLib::DiscreteAveragingAsianOption;
using QuantLib::DividendVanillaOption;
using QuantLib::QuantoVanillaOption;
using QuantLib::VanillaSwingOption;
using QuantLib::VanillaOption;
using QuantLib::ContinuousFloatingLookbackOption;
using QuantLib::BarrierOption;
using QuantLib::ContinuousFixedLookbackOption;
using QuantLib::DoubleBarrierOption;
using QuantLib::ForwardVanillaOption;
using QuantLib::EuropeanOption;
using QuantLib::ContinuousPartialFloatingLookbackOption;
using QuantLib::DividendBarrierOption;
using QuantLib::ContinuousPartialFixedLookbackOption;
using QuantLib::QuantoDoubleBarrierOption;
using QuantLib::QuantoForwardVanillaOption;
%}

struct Average {
    enum Type { Arithmetic, Geometric };
};

struct Barrier {
    enum Type { DownIn, UpIn, DownOut, UpOut };
};

struct DoubleBarrier {
    enum Type { KnockIn, KnockOut, KIKO, KOKI };
};

struct PartialBarrier : public Barrier {
    enum Range { Start, End, EndB1, EndB2 };
};

%shared_ptr(ContinuousAveragingAsianOption)
class ContinuousAveragingAsianOption : public OneAssetOption {
  public:
    ContinuousAveragingAsianOption(
        Average::Type averageType,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(CliquetOption)
class CliquetOption : public OneAssetOption {
  public:
    CliquetOption(
        const ext::shared_ptr<PercentageStrikePayoff>&,
        const ext::shared_ptr<EuropeanExercise>& maturity,
        const std::vector<Date>& resetDates);
};

%shared_ptr(ComplexChooserOption)
class ComplexChooserOption : public OneAssetOption {
  public:
    ComplexChooserOption(
        Date choosingDate,
        Real strikeCall,
        Real strikePut,
        const ext::shared_ptr<Exercise>& exerciseCall,
        const ext::shared_ptr<Exercise>& exercisePut);
};

%shared_ptr(CompoundOption)
class CompoundOption : public OneAssetOption {
 public:
    CompoundOption(
        const ext::shared_ptr<StrikedTypePayoff>& motherPayoff,
        const ext::shared_ptr<Exercise>& motherExercise,
        const ext::shared_ptr<StrikedTypePayoff>& daughterPayoff,
        const ext::shared_ptr<Exercise>& daughterExercise);
};

%shared_ptr(DiscreteAveragingAsianOption)
class DiscreteAveragingAsianOption : public OneAssetOption {
  public:
    DiscreteAveragingAsianOption(
        Average::Type averageType,
        Real runningAccumulator,
        Size pastFixings,
        const std::vector<Date>& fixingDates,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
    %extend {
        TimeGrid timeGrid() {
            return self->result<TimeGrid>("TimeGrid");
        }
    }
};

%shared_ptr(DividendVanillaOption)
class DividendVanillaOption : public OneAssetOption {
  public:
    DividendVanillaOption(
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise,
        const std::vector<Date>& dividendDates,
        const std::vector<Real>& dividends);
    Volatility impliedVolatility(
        Real targetValue,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Real accuracy = 1.0e-4,
        Size maxEvaluations = 100,
        Volatility minVol = 1.0e-4,
        Volatility maxVol = 4.0);
};

%shared_ptr(QuantoVanillaOption)
class QuantoVanillaOption : public OneAssetOption {
  public:
    QuantoVanillaOption(
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
    Real qvega();
    Real qrho();
    Real qlambda();
};

%shared_ptr(HolderExtensibleOption)
class HolderExtensibleOption : public OneAssetOption {
  public:
    HolderExtensibleOption(
        Option::Type type,
        Real premium,
        Date secondExpiryDate,
        Real secondStrike,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(PartialTimeBarrierOption)
class PartialTimeBarrierOption : public OneAssetOption {
  public:
    PartialTimeBarrierOption(
        PartialBarrier::Type barrierType,
        PartialBarrier::Range barrierRange,
        Real barrier,
        Real rebate,
        Date coverEventDate,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(SimpleChooserOption)
class SimpleChooserOption : public OneAssetOption {
  public:
    SimpleChooserOption(
        Date choosingDate,
        Real strike,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(VanillaSwingOption)
class VanillaSwingOption : public OneAssetOption {
  public:
    VanillaSwingOption(
        const ext::shared_ptr<Payoff>& payoff,
        const ext::shared_ptr<SwingExercise>& ex,
        Size minExerciseRights, Size maxExerciseRights);
    bool isExpired() const;
};

%shared_ptr(VanillaStorageOption)
class VanillaStorageOption : public OneAssetOption {
  public:
    VanillaStorageOption(
        const ext::shared_ptr<BermudanExercise>& ex,
        Real capacity,
        Real load,
        Real changeRate);
    bool isExpired() const;
};

%shared_ptr(VanillaOption)
class VanillaOption : public OneAssetOption {
  public:
    VanillaOption(
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
    Volatility impliedVolatility(
        Real targetValue,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Real accuracy = 1.0e-4,
        Size maxEvaluations = 100,
        Volatility minVol = 1.0e-4,
        Volatility maxVol = 4.0);
    %extend{
        SampledCurve priceCurve() {
            return self->result<SampledCurve>("priceCurve");
        }
    }
};

%shared_ptr(WriterExtensibleOption)
class WriterExtensibleOption : public OneAssetOption {
  public:
    /*!
     \param payoff1    The first payoff
     \param exercise1  The first exercise date
     \param payoff2    The payoff of the extended option
     \param exercise2  The second exercise date
    */
    WriterExtensibleOption(
        const ext::shared_ptr<PlainVanillaPayoff>& payoff1,
        const ext::shared_ptr<Exercise>& exercise1,
        const ext::shared_ptr<PlainVanillaPayoff>& payoff2,
        const ext::shared_ptr<Exercise>& exercise2);
    ext::shared_ptr<Payoff> payoff2();
    ext::shared_ptr<Exercise> exercise2();
    bool isExpired() const;
};

%shared_ptr(ContinuousFloatingLookbackOption)
class ContinuousFloatingLookbackOption : public OneAssetOption {
  public:
    ContinuousFloatingLookbackOption(
        Real currentMinmax,
        const ext::shared_ptr<TypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(BarrierOption)
class BarrierOption : public OneAssetOption {
  public:
    BarrierOption(
        Barrier::Type barrierType,
        Real barrier,
        Real rebate,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
    Volatility impliedVolatility(
        Real targetValue,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Real accuracy = 1.0e-4,
        Size maxEvaluations = 100,
        Volatility minVol = 1.0e-4,
        Volatility maxVol = 4.0);
};

%shared_ptr(ContinuousFixedLookbackOption)
class ContinuousFixedLookbackOption : public OneAssetOption {
  public:
    ContinuousFixedLookbackOption(
        Real currentMinmax,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(DoubleBarrierOption)
class DoubleBarrierOption : public OneAssetOption {
  public:
    DoubleBarrierOption(
        DoubleBarrier::Type barrierType,
        Real barrier_lo,
        Real barrier_hi,
        Real rebate,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
    Volatility impliedVolatility(
        Real price,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Real accuracy = 1.0e-4,
        Size maxEvaluations = 100,
        Volatility minVol = 1.0e-7,
        Volatility maxVol = 4.0) const;
};

%shared_ptr(ForwardVanillaOption)
class ForwardVanillaOption : public OneAssetOption {
  public:
    ForwardVanillaOption(
        Real moneyness,
        Date resetDate,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(EuropeanOption)
class EuropeanOption : public VanillaOption {
  public:
    EuropeanOption(
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(ContinuousPartialFloatingLookbackOption)
class ContinuousPartialFloatingLookbackOption : public ContinuousFloatingLookbackOption {
  public:
    ContinuousPartialFloatingLookbackOption(
        Real currentMinmax,
        Real lambda,
        Date lookbackPeriodEnd,
        const ext::shared_ptr<TypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(DividendBarrierOption)
class DividendBarrierOption : public BarrierOption {
  public:
    DividendBarrierOption(
        Barrier::Type barrierType,
        Real barrier,
        Real rebate,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise,
        const std::vector<Date>& dividendDates,
        const std::vector<Real>& dividends);
};

%shared_ptr(QuantoBarrierOption)
class QuantoBarrierOption : public BarrierOption {
  public:
    QuantoBarrierOption(
        Barrier::Type barrierType,
        Real barrier,
        Real rebate,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
    Real qvega() const;
    Real qrho() const;
    Real qlambda() const;
};

%shared_ptr(ContinuousPartialFixedLookbackOption)
class ContinuousPartialFixedLookbackOption : public ContinuousFixedLookbackOption {
  public:
    ContinuousPartialFixedLookbackOption(
        Date lookbackPeriodStart,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

%shared_ptr(QuantoDoubleBarrierOption)
class QuantoDoubleBarrierOption : public DoubleBarrierOption {
  public:
    QuantoDoubleBarrierOption(
        DoubleBarrier::Type barrierType,
        Real barrier_lo,
        Real barrier_hi,
        Real rebate,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
    Real qvega();
    Real qrho();
    Real qlambda();
};

%shared_ptr(QuantoForwardVanillaOption)
class QuantoForwardVanillaOption : public ForwardVanillaOption {
  public:
    QuantoForwardVanillaOption(
        Real moneyness,
        Date resetDate,
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        const ext::shared_ptr<Exercise>& exercise);
};

#endif
