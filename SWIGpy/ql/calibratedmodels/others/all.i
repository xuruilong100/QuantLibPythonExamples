#ifndef ql_calibratedmodels_others_all_i
#define ql_calibratedmodels_others_all_i

%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/common.i
%include ../ql/types.i

%{
using QuantLib::GJRGARCHModel;
using QuantLib::PiecewiseTimeDependentHestonModel;
%}

%shared_ptr(GJRGARCHModel)
class GJRGARCHModel : public CalibratedModel {
    %rename(lambdaParameter) lambda;

  public:
    GJRGARCHModel(
        const ext::shared_ptr<GJRGARCHProcess>& process);
    Real omega() const;
    Real alpha() const;
    Real beta() const;
    Real gamma() const;
    Real lambda() const;
    Real v0() const;
};

%shared_ptr(PiecewiseTimeDependentHestonModel)
class PiecewiseTimeDependentHestonModel : public CalibratedModel {
  public:
    PiecewiseTimeDependentHestonModel(
        const Handle<YieldTermStructure>& riskFreeRate,
        const Handle<YieldTermStructure>& dividendYield,
        const Handle<Quote>& s0,
        Real v0,
        const Parameter& theta,
        const Parameter& kappa,
        const Parameter& sigma,
        const Parameter& rho,
        const TimeGrid& timeGrid);

    Real theta(Time t) const;
    Real kappa(Time t) const;
    Real sigma(Time t) const;
    Real rho(Time t) const;
    Real v0() const;
    Real s0() const;
    const TimeGrid& timeGrid() const;
    const Handle<YieldTermStructure>& dividendYield() const;
    const Handle<YieldTermStructure>& riskFreeRate() const;
};

%shared_ptr(VarianceGammaModel)
class VarianceGammaModel : public CalibratedModel {
  public:
    explicit VarianceGammaModel(
        const ext::shared_ptr<VarianceGammaProcess>& process);

    Real sigma() const;
    Real nu() const;
    Real theta() const;

    ext::shared_ptr<VarianceGammaProcess> process() const;
};

#endif
