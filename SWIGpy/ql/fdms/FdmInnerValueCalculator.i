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
  public:
    virtual Real innerValue(
        const FdmLinearOpIterator& iter, Time t);
    virtual Real avgInnerValue(
        const FdmLinearOpIterator& iter, Time t);

  private:
    FdmInnerValueCalculator();
};

#endif
