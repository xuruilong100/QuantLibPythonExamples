#ifndef ql_calibratedmodels_others_all_i
#define ql_calibratedmodels_others_all_i

%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/common.i
%include ../ql/types.i

%{
using QuantLib::GJRGARCHModel;
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
    ext::shared_ptr<GJRGARCHProcess> process() const;
};

%shared_ptr(VarianceGammaModel)
class VarianceGammaModel : public CalibratedModel {
  public:
    VarianceGammaModel(
        const ext::shared_ptr<VarianceGammaProcess>& process);

    Real sigma() const;
    Real nu() const;
    Real theta() const;
    ext::shared_ptr<VarianceGammaProcess> process() const;
};

#endif
