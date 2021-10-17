#ifndef ql_fdms_StepCondition_i
#define ql_fdms_StepCondition_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::StepCondition;
typedef StepCondition<Array> FdmStepCondition;
%}

%shared_ptr(StepCondition<Array>)
template <class array_type>
class StepCondition {
  private:
    StepCondition();
  public:
    void applyTo(array_type& a, Time t) const;
};

%template(FdmStepCondition) StepCondition<Array>;
%template(FdmStepConditionVector) std::vector<ext::shared_ptr<StepCondition<Array>>> ;

typedef StepCondition<Array> FdmStepCondition;

#endif
