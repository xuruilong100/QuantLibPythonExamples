#ifndef ql_fdms_FdmBoundaryCondition_i
#define ql_fdms_FdmBoundaryCondition_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmLinearOp;
using QuantLib::BoundaryCondition;
typedef BoundaryCondition<FdmLinearOp> FdmBoundaryCondition;
typedef std::vector<ext::shared_ptr<FdmBoundaryCondition> > FdmBoundaryConditionSet;
%}

%shared_ptr(FdmBoundaryCondition);
class FdmBoundaryCondition {
   %rename(NoSide) None;
  public:
    enum Side { None, Upper, Lower };

    virtual void applyBeforeApplying(FdmLinearOp&) const;
    virtual void applyAfterApplying(Array&) const;
    virtual void applyBeforeSolving(FdmLinearOp&, Array& rhs) const;
    virtual void applyAfterSolving(Array&) const;
    virtual void setTime(Time t);

  private:
    FdmBoundaryCondition();
};

typedef std::vector<ext::shared_ptr<FdmBoundaryCondition> > FdmBoundaryConditionSet;
%template(FdmBoundaryConditionSet) std::vector<ext::shared_ptr<FdmBoundaryCondition> >;


#endif
