#ifndef ql_fdms_FdmBoundaryCondition_i
#define ql_fdms_FdmBoundaryCondition_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmLinearOp;
using QuantLib::BoundaryCondition;
typedef BoundaryCondition<FdmLinearOp> FdmBoundaryCondition;
typedef std::vector<ext::shared_ptr<FdmBoundaryCondition>> FdmBoundaryConditionSet;
%}

%shared_ptr(FdmBoundaryCondition)
class FdmBoundaryCondition {
   %rename(NoSide) None;
  private:
    FdmBoundaryCondition();
  public:
    enum Side { None, Upper, Lower };

    void applyBeforeApplying(FdmLinearOp&) const;
    void applyAfterApplying(Array&) const;
    void applyBeforeSolving(FdmLinearOp&, Array& rhs) const;
    void applyAfterSolving(Array&) const;
    void setTime(Time t);
};

typedef std::vector<ext::shared_ptr<FdmBoundaryCondition>> FdmBoundaryConditionSet;
%template(FdmBoundaryConditionSet) std::vector<ext::shared_ptr<FdmBoundaryCondition>>;


#endif
