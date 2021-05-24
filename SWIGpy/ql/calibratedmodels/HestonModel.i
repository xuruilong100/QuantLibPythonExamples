#ifndef ql_calibratedmodels_HestonModel_i
#define ql_calibratedmodels_HestonModel_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::HestonModel;
%}

%shared_ptr(HestonModel)
class HestonModel : public CalibratedModel {
  public:
    HestonModel(
        const ext::shared_ptr<HestonProcess>&  process);
    Real theta() const;
    Real kappa() const;
    Real sigma() const;
    Real rho() const;
    Real v0() const;
    ext::shared_ptr<HestonProcess> process() const;
};

%template(HestonModelHandle) Handle<HestonModel>;

#endif
