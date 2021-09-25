#ifndef ql_fdms_boundaryconditions_all_i
#define ql_fdms_boundaryconditions_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/fdms/FdmBoundaryCondition.i

%{
using QuantLib::FdmDiscountDirichletBoundary;
using QuantLib::FdmDirichletBoundary;
using QuantLib::FdmTimeDepDirichletBoundary;
%}

%shared_ptr(FdmDirichletBoundary)
class FdmDirichletBoundary : public FdmBoundaryCondition {
  public:
    typedef FdmBoundaryCondition::Side Side;

    FdmDirichletBoundary(
        const ext::shared_ptr<FdmMesher>& mesher,
        Real valueOnBoundary,
        Size direction, Side side);

    Real applyAfterApplying(Real x, Real value) const;
};

%shared_ptr(FdmDiscountDirichletBoundary)
class FdmDiscountDirichletBoundary : public FdmBoundaryCondition {
  public:
    typedef FdmBoundaryCondition::Side Side;

    FdmDiscountDirichletBoundary(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<YieldTermStructure>& rTS,
        Time maturityTime,
        Real valueOnBoundary,
        Size direction, Side side);
};

%shared_ptr(FdmTimeDepDirichletBoundary)
class FdmTimeDepDirichletBoundary : public FdmBoundaryCondition {
  public:
    %extend {
        FdmTimeDepDirichletBoundary(
            const ext::shared_ptr<FdmMesher>& mesher,
            PyObject* function,
            Size direction,
            FdmBoundaryCondition::Side side) {
            const ext::function<Real(Real)> f = UnaryFunction(function);
            return new FdmTimeDepDirichletBoundary(
                mesher, f, direction, side);
        }
    }
};

#endif
