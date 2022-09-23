#ifndef ql_calculator_i
#define ql_calculator_i

%{
using QuantLib::BlackCalculator;
using QuantLib::BlackScholesCalculator;
using QuantLib::BlackDeltaCalculator;
using QuantLib::CEVCalculator;
%}

class BlackCalculator {
  public:
    BlackCalculator(
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        Real forward,
        Real stdDev,
        Real discount = 1.0);
    BlackCalculator(
        Option::Type optionType,
        Real strike,
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

class BlackScholesCalculator : public BlackCalculator {
  public:
    BlackScholesCalculator(
        const ext::shared_ptr<StrikedTypePayoff>& payoff,
        Real spot,
        DiscountFactor growth,
        Real stdDev,
        DiscountFactor discount);
    BlackScholesCalculator(
        Option::Type optionType,
        Real strike,
        Real spot,
        DiscountFactor growth,
        Real stdDev,
        DiscountFactor discount);
    Real delta() const;
    Real elasticity() const;
    Real gamma() const;
    Real theta(Time maturity) const;
    Real thetaPerDay(Time maturity) const;
    using BlackCalculator::delta;
    using BlackCalculator::elasticity;
    using BlackCalculator::gamma;
    using BlackCalculator::theta;
    using BlackCalculator::thetaPerDay;
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
    Real cumD1(Real strike) const;
    Real cumD2(Real strike) const;
    Real nD1(Real strike) const;
    Real nD2(Real strike) const;
    void setDeltaType(DeltaVolQuote::DeltaType dt);
    void setOptionType(Option::Type ot);
    Real atmStrike(DeltaVolQuote::AtmType atmT) const;
};

class CEVCalculator {
  public:
    CEVCalculator(
      Real f0, 
      Real alpha, 
      Real beta);
    Real value(Option::Type optionType, Real strike, Time t) const;
    Real f0()    const;
    Real alpha() const;
    Real beta()  const;
};


#endif
