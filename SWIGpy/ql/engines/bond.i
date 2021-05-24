#ifndef ql_engines_bond_i
#define ql_engines_bond_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::DiscountingBondEngine;
using QuantLib::TreeCallableFixedRateBondEngine;
using QuantLib::BlackCallableFixedRateBondEngine;
using QuantLib::BinomialConvertibleEngine;
%}

%shared_ptr(DiscountingBondEngine)
class DiscountingBondEngine : public PricingEngine {
  public:
    DiscountingBondEngine(
        const Handle<YieldTermStructure>& discountCurve);
};

%shared_ptr(TreeCallableFixedRateBondEngine)
class TreeCallableFixedRateBondEngine : public PricingEngine {
  public:
    TreeCallableFixedRateBondEngine(
        const ext::shared_ptr<ShortRateModel>& model,
        Size timeSteps,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
    TreeCallableFixedRateBondEngine(
        const ext::shared_ptr<ShortRateModel>& model,
        const TimeGrid& grid,
        const Handle<YieldTermStructure>& termStructure = Handle<YieldTermStructure>());
};

%shared_ptr(BlackCallableFixedRateBondEngine)
class BlackCallableFixedRateBondEngine : public PricingEngine {
  public:
    BlackCallableFixedRateBondEngine(
        const Handle<Quote>& fwdYieldVol,
        const Handle<YieldTermStructure>& discountCurve);
};

%shared_ptr(BinomialConvertibleEngine<CoxRossRubinstein>)
%shared_ptr(BinomialConvertibleEngine<JarrowRudd>)
%shared_ptr(BinomialConvertibleEngine<AdditiveEQPBinomialTree>)
%shared_ptr(BinomialConvertibleEngine<Trigeorgis>)
%shared_ptr(BinomialConvertibleEngine<Tian>)
%shared_ptr(BinomialConvertibleEngine<LeisenReimer>)
%shared_ptr(BinomialConvertibleEngine<Joshi4>)
template <class T>
class BinomialConvertibleEngine : public PricingEngine {
  public:
    BinomialConvertibleEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
        Size steps);
};

%template(BinomialCRRConvertibleEngine) BinomialConvertibleEngine<CoxRossRubinstein>;
%template(BinomialJRConvertibleEngine) BinomialConvertibleEngine<JarrowRudd>;
%template(BinomialEQPConvertibleEngine) BinomialConvertibleEngine<AdditiveEQPBinomialTree>;
%template(BinomialTrigeorgisConvertibleEngine) BinomialConvertibleEngine<Trigeorgis>;
%template(BinomialTianConvertibleEngine) BinomialConvertibleEngine<Tian>;
%template(BinomialLRConvertibleEngine) BinomialConvertibleEngine<LeisenReimer>;
%template(BinomialJ4ConvertibleEngine) BinomialConvertibleEngine<Joshi4>;

%pythoncode %{
def BinomialConvertibleEngine(
        process,
        type,
        steps):
    type = type.lower()
    if type == "crr" or type == "coxrossrubinstein":
        cls = BinomialCRRConvertibleEngine
    elif type == "jr" or type == "jarrowrudd":
        cls = BinomialJRConvertibleEngine
    elif type == "eqp":
        cls = BinomialEQPConvertibleEngine
    elif type == "trigeorgis":
        cls = BinomialTrigeorgisConvertibleEngine
    elif type == "tian":
        cls = BinomialTianConvertibleEngine
    elif type == "lr" or type == "leisenreimer":
        cls = BinomialLRConvertibleEngine
    elif type == "j4" or type == "joshi4":
        cls = BinomialJ4ConvertibleEngine
    else:
        raise RuntimeError("unknown binomial engine type: %s" % type);
    return cls(process, steps)
%}

#endif
