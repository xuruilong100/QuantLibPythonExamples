#ifndef ql_fdms_StepCondition_i
#define ql_fdms_StepCondition_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::StepCondition;    
%}

%shared_ptr(StepCondition<Array>);
template <class array_type>
class StepCondition {
  public:
    virtual void applyTo(array_type& a, Time t) const;

  private:
    StepCondition();
};

%template(FdmStepCondition) StepCondition<Array>;


#endif
