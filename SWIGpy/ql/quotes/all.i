#ifndef ql_quotes_all_i
#define ql_quotes_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::SimpleQuote;
using QuantLib::DerivedQuote;
using QuantLib::CompositeQuote;
using QuantLib::DeltaVolQuote;
using QuantLib::EurodollarFuturesImpliedStdDevQuote;
using QuantLib::ForwardSwapQuote;
using QuantLib::ForwardValueQuote;
using QuantLib::FuturesConvAdjustmentQuote;
using QuantLib::ImpliedStdDevQuote;
using QuantLib::LastFixingQuote;
using QuantLib::RecoveryRateQuote;
using QuantLib::Seniority;
using QuantLib::SecDom;
using QuantLib::SnrFor;
using QuantLib::SubLT2;
using QuantLib::JrSubT2;
using QuantLib::PrefT1;
using QuantLib::NoSeniority;
using QuantLib::SeniorSec;
using QuantLib::SeniorUnSec;
using QuantLib::SubTier1;
using QuantLib::SubUpperTier2;
using QuantLib::SubLoweTier2;
%}

enum Seniority {
    SecDom = 0,
    SnrFor,
    SubLT2,
    JrSubT2,
    PrefT1,
    NoSeniority,
    SeniorSec     = SecDom,
    SeniorUnSec   = SnrFor,
    SubTier1      = PrefT1,
    SubUpperTier2 = JrSubT2,
    SubLoweTier2  = SubLT2
};

%shared_ptr(CompositeQuote<BinaryFunction>)
template <class F>
class CompositeQuote : public Quote, public Observer {
  public:
    %extend {
        CompositeQuote(
            const Handle<Quote>& h1,
            const Handle<Quote>& h2,
            PyObject* function) {
            return new CompositeQuote<F>(h1,h2,F(function));
        }
    }
    Real value1() const;
    Real value2() const;
};

%template(CompositeBFQuote) CompositeQuote<BinaryFunction>;

%shared_ptr(DeltaVolQuote)
class DeltaVolQuote : public Quote, public Observer {
  public:
    enum DeltaType { Spot, Fwd, PaSpot, PaFwd };
    enum AtmType { AtmNull, AtmSpot, AtmFwd, AtmDeltaNeutral,
                   AtmVegaMax, AtmGammaMax, AtmPutCall50 };
    DeltaVolQuote(Real delta,
                  const Handle<Quote>& vol,
                  Time maturity,
                  DeltaVolQuote::DeltaType deltaType);
    DeltaVolQuote(const Handle<Quote>& vol,
                  DeltaVolQuote::DeltaType deltaType,
                  Time maturity,
                  DeltaVolQuote::AtmType atmType);

    Real delta() const;
    Time maturity() const;
    AtmType atmType() const;
    DeltaType deltaType() const;
};

%template(DeltaVolQuoteHandle) Handle<DeltaVolQuote>;
%template(RelinkableDeltaVolQuoteHandle) RelinkableHandle<DeltaVolQuote>;

%shared_ptr(DerivedQuote<UnaryFunction>)
template <class F>
class DerivedQuote : public Quote, public Observer {
  public:
    %extend {
        DerivedQuote(
            const Handle<Quote>& h,
            PyObject* function) {
            return new DerivedQuote<F>(h,F(function));
        }
    }
};

%template(DerivedUFQuote) DerivedQuote<UnaryFunction>;

%shared_ptr(EurodollarFuturesImpliedStdDevQuote)
class EurodollarFuturesImpliedStdDevQuote : public Quote, public LazyObject {
  public:
    EurodollarFuturesImpliedStdDevQuote(Handle<Quote> forward,
                                        Handle<Quote> callPrice,
                                        Handle<Quote> putPrice,
                                        Real strike,
                                        Real guess = .15,
                                        Real accuracy = 1.0e-6,
                                        Natural maxIter = 100);
};

%shared_ptr(ForwardSwapQuote)
class ForwardSwapQuote : public Quote, public LazyObject {
  public:
    ForwardSwapQuote(ext::shared_ptr<SwapIndex> swapIndex,
                     Handle<Quote> spread,
                     const Period& fwdStart);

    const Date& valueDate() const;
    const Date& startDate() const;
    const Date& fixingDate() const;
};

%shared_ptr(ForwardValueQuote)
class ForwardValueQuote : public Quote, public Observer {
  public:
    ForwardValueQuote(
        ext::shared_ptr<Index> index, const Date& fixingDate);
};

%shared_ptr(FuturesConvAdjustmentQuote)
class FuturesConvAdjustmentQuote : public Quote, public Observer {
  public:
    FuturesConvAdjustmentQuote(const ext::shared_ptr<IborIndex>& index,
                               const Date& futuresDate,
                               Handle<Quote> futuresQuote,
                               Handle<Quote> volatility,
                               Handle<Quote> meanReversion);
    FuturesConvAdjustmentQuote(const ext::shared_ptr<IborIndex>& index,
                               const std::string& immCode,
                               Handle<Quote> futuresQuote,
                               Handle<Quote> volatility,
                               Handle<Quote> meanReversion);

    Real futuresValue() const;
    Real volatility() const;
    Real meanReversion() const;
    Date immDate() const;
};

%shared_ptr(ImpliedStdDevQuote)
class ImpliedStdDevQuote : public Quote, public LazyObject {
  public:
    ImpliedStdDevQuote(Option::Type optionType,
                       Handle<Quote> forward,
                       Handle<Quote> price,
                       Real strike,
                       Real guess,
                       Real accuracy = 1.0e-6,
                       Natural maxIter = 100);
};

%shared_ptr(LastFixingQuote)
class LastFixingQuote : public Quote, public Observer {
  public:
    LastFixingQuote(ext::shared_ptr<Index> index);
    const ext::shared_ptr<Index>& index() const;
    Date referenceDate() const;
};

%shared_ptr(RecoveryRateQuote)
class RecoveryRateQuote : public Quote {
  public:
    static Real conventionalRecovery(Seniority sen);
    RecoveryRateQuote(Real value = Null<Real>(),
                      Seniority seniority = NoSeniority);

    Seniority seniority() const;
    Real setValue(Real value = Null<Real>());
    void reset();
};

%shared_ptr(SimpleQuote)
class SimpleQuote : public Quote {
  public:
    SimpleQuote(Real value);
    void setValue(Real value);
};

%inline %{
    ext::shared_ptr<SimpleQuote> as_simple_quote(
        const ext::shared_ptr<Quote>& q) {
        return ext::dynamic_pointer_cast<SimpleQuote>(q);
    }
%}

#endif
