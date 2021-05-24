#ifndef ql_black_formula_i
#define ql_black_formula_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::bachelierBlackFormula;
using QuantLib::bachelierBlackFormulaAssetItmProbability;
using QuantLib::bachelierBlackFormulaImpliedVol;
using QuantLib::blackFormula;
using QuantLib::blackFormulaAssetItmProbability;
using QuantLib::blackFormulaCashItmProbability;
using QuantLib::blackFormulaImpliedStdDev;
using QuantLib::blackFormulaImpliedStdDevLiRS;
using QuantLib::BlackCalculator;
using QuantLib::BlackDeltaCalculator;
%}

Real bachelierBlackFormula(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real stdDev,
    Real discount = 1.0);

Real bachelierBlackFormulaAssetItmProbability(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev);

Real bachelierBlackFormulaAssetItmProbability(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real stdDev);

Real bachelierBlackFormulaImpliedVol(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real tte,
    Real bachelierPrice,
    Real discount = 1.0);

Real blackFormula(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real stdDev,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaAssetItmProbability(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real displacement = 0.0);

Real blackFormulaAssetItmProbability(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real stdDev,
    Real displacement = 0.0);

Real blackFormulaCashItmProbability(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real displacement = 0.0);

Real blackFormulaCashItmProbability(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real stdDev,
    Real displacement = 0.0);

Real blackFormulaImpliedStdDev(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real blackPrice,
    Real discount = 1.0,
    Real displacement = 0.0,
    Real guess = Null<Real>(),
    Real accuracy = 1.0e-6,
    Natural maxIterations = 100);


Real blackFormulaImpliedStdDevLiRS(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real blackPrice,
    Real discount = 1.0,
    Real displacement = 0.0,
    Real guess = Null<Real>(),
    Real omega = 1.0,
    Real accuracy = 1.0e-6,
    Natural maxIterations = 100);

Real blackFormulaImpliedStdDevLiRS(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real blackPrice,
    Real discount = 1.0,
    Real displacement = 0.0,
    Real guess = Null<Real>(),
    Real omega = 1.0,
    Real accuracy = 1.0e-6,
    Natural maxIterations = 100);

class BlackCalculator {
  public:
    BlackCalculator(
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        Real forward,
        Real stdDev,
        Real discount = 1.0);
    Real value() const;
    Real deltaForward() const;
    Real delta(Real spot) const;
    Real elasticityForward() const;
    Real elasticity(Real spot) const;
    Real gammaForward() const;
    Real gamma(Real spot) const;
    Real theta(Real spot, Time maturity) const;
    Real thetaPerDay(Real spot, Time maturity) const;
    Real vega(Time maturity) const;
    Real rho(Time maturity) const;
    Real dividendRho(Time maturity) const;
    Real itmCashProbability() const;
    Real itmAssetProbability() const;
    Real strikeSensitivity() const;
    Real alpha() const;
    Real beta() const;
};

class BlackDeltaCalculator {
  public:
    BlackDeltaCalculator(
        Option::Type ot,
        DeltaVolQuote::DeltaType dt,
        Real spot,
        DiscountFactor dDiscount,
        DiscountFactor fDiscount,
        Real stDev);

    Real deltaFromStrike(Real strike) const;
    Real strikeFromDelta(Real delta) const;
    Real atmStrike(DeltaVolQuote::AtmType atmT) const;
};

#endif
