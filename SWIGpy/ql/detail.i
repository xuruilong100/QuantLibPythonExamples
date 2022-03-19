#ifndef ql_detail_i
#define ql_detail_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/quotes/all.i

%{
using QuantLib::detail::D0Interpolator;
using QuantLib::detail::ImpliedVolatilityHelper;
%}

class D0Interpolator {
  public:
    D0Interpolator(
        Real forward, Real expiryTime, Real alpha, Real beta, Real nu, Real rho);
    Real operator()() const;
};

class ImpliedVolatilityHelper {
  public:
    static Volatility calculate(
        const Instrument& instrument,
        const PricingEngine& engine,
        SimpleQuote& volQuote,
        Real targetValue,
        Real accuracy,
        Natural maxEvaluations,
        Volatility minVol,
        Volatility maxVol);
    static ext::shared_ptr<GeneralizedBlackScholesProcess> clone(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
        const ext::shared_ptr<SimpleQuote>&);
};

#endif
