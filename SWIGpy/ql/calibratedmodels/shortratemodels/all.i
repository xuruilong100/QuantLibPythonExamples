#ifndef ql_calibratedmodels_shortratemodels_all_i
#define ql_calibratedmodels_shortratemodels_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/calibratedmodels/ShortRateModel.i

%{
using QuantLib::OneFactorModel;
using QuantLib::TwoFactorModel;
using QuantLib::BlackKarasinski;
using QuantLib::CoxIngersollRoss;
using QuantLib::ExtendedCoxIngersollRoss;
using QuantLib::OneFactorAffineModel;
using QuantLib::G2;
using QuantLib::Vasicek;
using QuantLib::HullWhite;
%}

%shared_ptr(OneFactorModel)
class OneFactorModel : public ShortRateModel {
  private:
    OneFactorModel();
};

%shared_ptr(TwoFactorModel)
class TwoFactorModel : public ShortRateModel {
  private:
    TwoFactorModel();
};

%shared_ptr(BlackKarasinski)
class BlackKarasinski : public OneFactorModel, public TermStructureConsistentModel {
  public:
    BlackKarasinski(
        const Handle<YieldTermStructure>& termStructure,
        Real a = 0.1, 
        Real sigma = 0.1);
};

%shared_ptr(OneFactorAffineModel)
class OneFactorAffineModel : public OneFactorModel, public AffineModel {
  private:
    OneFactorAffineModel();

  public:
    Real discountBond(
        Time now, 
        Time maturity,
        Rate rate) const;
};

%shared_ptr(CoxIngersollRoss)
class CoxIngersollRoss : public OneFactorAffineModel {
  public:
    CoxIngersollRoss(
        Rate r0 = 0.01, 
        Real theta = 0.1, 
        Real k = 0.1,
        Real sigma = 0.1);
};

%shared_ptr(Vasicek)
class Vasicek : public OneFactorAffineModel {
    %rename(lambdaParameter) lambda;
  public:
    Vasicek(
        Rate r0 = 0.05,
        Real a = 0.1,
        Real b = 0.05,
        Real sigma = 0.01,
        Real lamda = 0.0);

    Real a() const;
    Real b() const;
    Real lambda() const;
    Real sigma() const;
    Real r0() const;
};

%shared_ptr(ExtendedCoxIngersollRoss)
class ExtendedCoxIngersollRoss : public CoxIngersollRoss, public TermStructureConsistentModel {
  public:
    ExtendedCoxIngersollRoss(
        const Handle<YieldTermStructure>& termStructure,
        Real theta = 0.1, 
        Real k = 0.1,
        Real sigma = 0.1, 
        Real x0 = 0.05);
};

%shared_ptr(HullWhite)
class HullWhite : public Vasicek, public TermStructureConsistentModel {
  public:
    HullWhite(
        const Handle<YieldTermStructure>& termStructure,
        Real a = 0.1, 
        Real sigma = 0.01);

    static Rate convexityBias(
        Real futurePrice, 
        Time t, 
        Time T,
        Real sigma, 
        Real a);
    static std::vector<bool> FixedReversion();
};

%shared_ptr(G2)
class G2 : public TwoFactorModel, public AffineModel, public TermStructureConsistentModel {
  public:
    G2(const Handle<YieldTermStructure>& termStructure,
       Real a = 0.1, 
       Real sigma = 0.01, 
       Real b = 0.1,
       Real eta = 0.01, 
       Real rho = -0.75);
};

#endif
