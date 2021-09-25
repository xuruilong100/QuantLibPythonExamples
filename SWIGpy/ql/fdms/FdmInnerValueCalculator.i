#ifndef ql_fdms_FdmInnerValueCalculator_i
#define ql_fdms_FdmInnerValueCalculator_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmInnerValueCalculator;
%}

%shared_ptr(FdmInnerValueCalculator)
class FdmInnerValueCalculator {
  private:
    FdmInnerValueCalculator();
  public:
    Real innerValue(
        const FdmLinearOpIterator& iter, Time t);
    Real avgInnerValue(
        const FdmLinearOpIterator& iter, Time t);
};

#endif
