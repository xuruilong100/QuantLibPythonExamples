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
%}

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

%shared_ptr(DerivedQuote<UnaryFunction>)
template <class F>
class DerivedQuote : public Quote {
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

%shared_ptr(CompositeQuote<BinaryFunction>)
template <class F>
class CompositeQuote : public Quote {
  public:
    %extend {
        CompositeQuote(
            const Handle<Quote>& h1,
            const Handle<Quote>& h2,
            PyObject* function) {
            return new CompositeQuote<F>(h1,h2,F(function));
        }
    }
};

%template(CompositeBFQuote) CompositeQuote<BinaryFunction>;

%shared_ptr(DeltaVolQuote)
class DeltaVolQuote : public Quote {
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

namespace std {
    %template(QuoteVector) vector<ext::shared_ptr<Quote> >;
    %template(QuoteVectorVector) vector<vector<ext::shared_ptr<Quote> > >;
    %template(QuoteHandleVector) vector<Handle<Quote> >;
    %template(QuoteHandleVectorVector) vector<vector<Handle<Quote> > >;
    %template(RelinkableQuoteHandleVector) vector<RelinkableHandle<Quote> >;
    %template(RelinkableQuoteHandleVectorVector) vector<vector<RelinkableHandle<Quote> > >;
}

#endif
