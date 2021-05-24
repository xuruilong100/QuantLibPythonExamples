#ifndef ql_calibratedmodels_hestonmodels_all_i
#define ql_calibratedmodels_hestonmodels_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/calibratedmodels/HestonModel.i

%{
using QuantLib::BatesModel;
using QuantLib::BatesDetJumpModel;
using QuantLib::BatesDoubleExpModel;
using QuantLib::BatesDoubleExpDetJumpModel;
%}

%shared_ptr(BatesModel)
class BatesModel : public HestonModel {
    %rename(lambdaParameter) lambda;
  public:
    BatesModel(
        const ext::shared_ptr<BatesProcess>&  process);
    Real nu() const;
    Real delta() const;
    Real lambda() const;
};

%shared_ptr(BatesDoubleExpModel)
class BatesDoubleExpModel : public HestonModel {
    %feature("kwargs") BatesDoubleExpModel;
    %rename(lambdaParameter) lambda;
  public:
    explicit BatesDoubleExpModel(
        const ext::shared_ptr<HestonProcess> & process,
        Real lamda = 0.1,
        Real nuUp = 0.1,
        Real nuDown = 0.1,
        Real p = 0.5);

    Real p()      const;
    Real nuDown() const;
    Real nuUp()   const;
    Real lambda() const;
};

%shared_ptr(BatesDetJumpModel)
class BatesDetJumpModel : public BatesModel {
  public:
    explicit BatesDetJumpModel(
        const ext::shared_ptr<BatesProcess> & process,
        Real kappaLambda = 1.0,
        Real thetaLambda = 0.1);

    Real kappaLambda() const;
    Real thetaLambda() const;
};

%shared_ptr(BatesDoubleExpDetJumpModel)
class BatesDoubleExpDetJumpModel : public BatesDoubleExpModel {
    %feature("kwargs") BatesDoubleExpDetJumpModel;
  public:
    explicit BatesDoubleExpDetJumpModel(
        const ext::shared_ptr<HestonProcess> & process,
        Real lamda = 0.1,
        Real nuUp = 0.1,
        Real nuDown = 0.1,
        Real p = 0.5,
        Real kappaLambda = 1.0,
        Real thetaLambda = 0.1);

    Real kappaLambda() const;
    Real thetaLambda() const;
};


#endif
