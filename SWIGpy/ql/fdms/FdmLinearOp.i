#ifndef ql_fdms_FdmLinearOp_i
#define ql_fdms_FdmLinearOp_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmLinearOp;
%}

%shared_ptr(FdmLinearOp)
class FdmLinearOp {
  public:
    Array apply(const Array& r) const;
    //SparseMatrix toMatrix() const;

  private:
    FdmLinearOp();
};

#endif
