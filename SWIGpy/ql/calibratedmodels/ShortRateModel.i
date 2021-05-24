#ifndef ql_calibratedmodels_ShortRateModel_i
#define ql_calibratedmodels_ShortRateModel_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::ShortRateModel;
%}

%shared_ptr(ShortRateModel)
class ShortRateModel : public CalibratedModel {
  private:
    ShortRateModel();
};

%template(ShortRateModelHandle) Handle<ShortRateModel>;
%template(RelinkableShortRateModelHandle) RelinkableHandle<ShortRateModel>;

#endif
