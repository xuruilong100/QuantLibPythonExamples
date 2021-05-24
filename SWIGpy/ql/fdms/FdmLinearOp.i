#ifndef ql_fdms_FdmMesher_i
#define ql_fdms_FdmMesher_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmLinearOp;
%}

%shared_ptr(FdmLinearOp)
class FdmLinearOp {
  public:
    virtual Array apply(const Array& r) const;

  private:
    FdmLinearOp();
};

#endif
