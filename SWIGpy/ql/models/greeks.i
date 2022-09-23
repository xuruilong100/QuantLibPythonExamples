#ifndef ql_models_greeks_i
#define ql_models_greeks_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::SwaptionPseudoDerivative;
using QuantLib::CapPseudoDerivative;
using QuantLib::RatePseudoRootJacobian;
using QuantLib::RatePseudoRootJacobianAllElements;
using QuantLib::RatePseudoRootJacobianNumerical;
using QuantLib::VolatilityBumpInstrumentJacobian;
using QuantLib::VegaBumpCollection;
using QuantLib::OrthogonalizedBumpFinder;
typedef VolatilityBumpInstrumentJacobian::Swaption VolatilityBumpInstrumentJacobianSwaption;
typedef VolatilityBumpInstrumentJacobian::Cap VolatilityBumpInstrumentJacobianCap;
%}

class SwaptionPseudoDerivative {
  public:
    SwaptionPseudoDerivative(
        const ext::shared_ptr<MarketModel>& inputModel,
        Size startIndex,
        Size endIndex);

      const Matrix& varianceDerivative(Size i) const;
      const Matrix& volatilityDerivative(Size i) const;

      Real impliedVolatility() const;
      Real variance() const;
      Real expiry() const;
};

class CapPseudoDerivative {
  public:
    CapPseudoDerivative(
        const ext::shared_ptr<MarketModel>& inputModel,
        Real strike,
        Size startIndex,
        Size endIndex,
        Real firstDF);

    const Matrix& volatilityDerivative(Size i) const;
    const Matrix& priceDerivative(Size i) const;
    Real impliedVolatility() const;
};

class RatePseudoRootJacobian {
  public:
    RatePseudoRootJacobian(
        const Matrix& pseudoRoot,
        Size aliveIndex,
        Size numeraire,
        const std::vector<Time>& taus,
        const std::vector<Matrix>& pseudoBumps,
        std::vector<Spread> displacements);

    void getBumps(
        const std::vector<Rate>& oldRates,
        const std::vector<Real>& oneStepDFs,
        const std::vector<Rate>& newRates,
        const std::vector<Real>& gaussians,
        Matrix& B);
};

class RatePseudoRootJacobianAllElements {
  public:
    RatePseudoRootJacobianAllElements(
        const Matrix& pseudoRoot,
        Size aliveIndex,
        Size numeraire,
        const std::vector<Time>& taus,
        std::vector<Spread> displacements);

    void getBumps(
        const std::vector<Rate>& oldRates,
        const std::vector<Real>& oneStepDFs,
        const std::vector<Rate>& newRates,  
        const std::vector<Real>& gaussians,
        std::vector<Matrix>& B);
};

class RatePseudoRootJacobianNumerical {
  public:
    RatePseudoRootJacobianNumerical(
        const Matrix& pseudoRoot,
        Size aliveIndex,
        Size numeraire,
        const std::vector<Time>& taus,
        const std::vector<Matrix>& pseudoBumps,
        const std::vector<Spread>& displacements);

    void getBumps(
        const std::vector<Rate>& oldRates,
        const std::vector<Real>& oneStepDFs, 
        const std::vector<Rate>& newRates,   
        const std::vector<Real>& gaussians,
        Matrix& B);
};

struct VolatilityBumpInstrumentJacobianSwaption {
    Size startIndex_;
    Size endIndex_;
    %extend {
        void startIndex(Size startIndex) {
            self->startIndex_ = startIndex;
        }
        void endIndex(Size endIndex) {
            self->endIndex_ = endIndex;
        }
    }
};

typedef VolatilityBumpInstrumentJacobian::Swaption VolatilityBumpInstrumentJacobianSwaption;
%template(VolatilityBumpInstrumentJacobianSwaptionVector) std::vector<VolatilityBumpInstrumentJacobianSwaption>;

struct VolatilityBumpInstrumentJacobianCap {
    Size startIndex_;
    Size endIndex_;
    Real strike_;
    %extend {
        void startIndex(Size startIndex) {
            self->startIndex_ = startIndex;
        }
        void endIndex(Size endIndex) {
            self->endIndex_ = endIndex;
        }
        void strike(Real strike) {
            self->strike_ = strike;
        }
    }
};

typedef VolatilityBumpInstrumentJacobian::Cap VolatilityBumpInstrumentJacobianCap;
%template(VolatilityBumpInstrumentJacobianCapVector) std::vector<VolatilityBumpInstrumentJacobianCap>;

class VolatilityBumpInstrumentJacobian {
  public:
    VolatilityBumpInstrumentJacobian(
        const VegaBumpCollection& bumps,
        const std::vector<VolatilityBumpInstrumentJacobianSwaption>& swaptions,
        const std::vector<VolatilityBumpInstrumentJacobianCap>& caps);
    const VegaBumpCollection& getInputBumps() const;
    std::vector<Real> derivativesVolatility(Size j) const;
    std::vector<Real> onePercentBump(Size j) const;
    const Matrix& getAllOnePercentBumps() const;
};

class VegaBumpCollection {
public:
    VegaBumpCollection(
        const ext::shared_ptr<MarketModel>& volStructure,
        bool allowFactorwiseBumping = true);

    Size numberBumps() const;
    const ext::shared_ptr<MarketModel>& associatedModel() const;

    bool isFull() const;
    bool isNonOverlapping() const; 
    bool isSensible() const;
};

class OrthogonalizedBumpFinder {
  public:
    OrthogonalizedBumpFinder(
        const VegaBumpCollection& bumps,
        const std::vector<VolatilityBumpInstrumentJacobianSwaption>& swaptions,
        const std::vector<VolatilityBumpInstrumentJacobianCap>& caps,
        Real multiplierCutOff, 
        Real tolerance);      

    void GetVegaBumps(std::vector<std::vector<Matrix>>& theBumps) const; 
};

#endif
