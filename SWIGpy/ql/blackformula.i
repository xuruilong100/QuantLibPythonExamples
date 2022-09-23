#ifndef ql_black_formula_i
#define ql_black_formula_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::blackFormula;
using QuantLib::blackFormulaForwardDerivative;
using QuantLib::blackFormulaImpliedStdDevApproximation;
using QuantLib::blackFormulaImpliedStdDevChambers;
using QuantLib::blackFormulaImpliedStdDevApproximationRS;
using QuantLib::blackFormulaImpliedStdDev;
using QuantLib::blackFormulaImpliedStdDevLiRS;
using QuantLib::blackFormulaCashItmProbability;
using QuantLib::blackFormulaAssetItmProbability;
using QuantLib::blackFormulaStdDevDerivative;
using QuantLib::blackFormulaVolDerivative;
using QuantLib::blackFormulaStdDevSecondDerivative;
using QuantLib::bachelierBlackFormula;
using QuantLib::bachelierBlackFormulaForwardDerivative;
using QuantLib::bachelierBlackFormulaImpliedVol;
using QuantLib::bachelierBlackFormulaStdDevDerivative;
using QuantLib::bachelierBlackFormulaAssetItmProbability;
%}

Real blackFormula(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real stdDev,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormula(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaForwardDerivative(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real stdDev,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaForwardDerivative(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaImpliedStdDevApproximation(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real blackPrice,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaImpliedStdDevApproximation(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real blackPrice,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaImpliedStdDevChambers(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real blackPrice,
    Real blackAtmPrice,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaImpliedStdDevChambers(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real blackPrice,
    Real blackAtmPrice,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaImpliedStdDevApproximationRS(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real blackPrice,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaImpliedStdDevApproximationRS(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real blackPrice,
    Real discount = 1.0,
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

Real blackFormulaImpliedStdDev(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real blackPrice,
    Real discount = 1.0,
    Real displacement = 0.0,
    Real guess = Null<Real>(),
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

Real blackFormulaCashItmProbability(
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

Real blackFormulaAssetItmProbability(
    Option::Type optionType, 
    Real strike, 
    Real forward, 
    Real stdDev, 
    Real displacement = 0.0);

Real blackFormulaAssetItmProbability(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real displacement = 0.0);

Real blackFormulaStdDevDerivative(
    Real strike, 
    Real forward, 
    Real stdDev, 
    Real discount = 1.0, 
    Real displacement = 0.0);

Real blackFormulaVolDerivative(
    Real strike,
    Real forward,
    Real stdDev,
    Real expiry,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaStdDevDerivative(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real discount = 1.0,
    Real displacement = 0.0);

Real blackFormulaStdDevSecondDerivative(
    Rate strike, 
    Rate forward, 
    Real stdDev, 
    Real discount, 
    Real displacement);

Real blackFormulaStdDevSecondDerivative(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real discount = 1.0,
    Real displacement = 0.0);

Real bachelierBlackFormula(
    Option::Type optionType, 
    Real strike, 
    Real forward, 
    Real stdDev, 
    Real discount = 1.0);

Real bachelierBlackFormula(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real discount = 1.0);

Real bachelierBlackFormulaForwardDerivative(
    Option::Type optionType, 
    Real strike, 
    Real forward, 
    Real stdDev, 
    Real discount = 1.0);

Real bachelierBlackFormulaForwardDerivative(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real discount = 1.0);

Real bachelierBlackFormulaImpliedVol(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real tte,
    Real bachelierPrice,
    Real discount = 1.0);

Real bachelierBlackFormulaStdDevDerivative(
    Real strike,
    Real forward,
    Real stdDev,
    Real discount = 1.0);

Real bachelierBlackFormulaStdDevDerivative(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev,
    Real discount = 1.0);

Real bachelierBlackFormulaAssetItmProbability(
    Option::Type optionType,
    Real strike,
    Real forward,
    Real stdDev);

Real bachelierBlackFormulaAssetItmProbability(
    const ext::shared_ptr<PlainVanillaPayoff>& payoff,
    Real forward,
    Real stdDev);

#endif
