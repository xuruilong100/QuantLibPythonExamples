#ifndef ql_fdms_Scheme_i
#define ql_fdms_Scheme_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::CraigSneydScheme;
using QuantLib::CrankNicolsonScheme;
using QuantLib::ImplicitEulerScheme;
using QuantLib::DouglasScheme;
using QuantLib::ExplicitEulerScheme;
using QuantLib::HundsdorferScheme;
using QuantLib::MethodOfLinesScheme;
using QuantLib::ModifiedCraigSneydScheme;
%}

%shared_ptr(CraigSneydScheme)
class CraigSneydScheme  {
  public:
    CraigSneydScheme(Real theta, Real mu,
        const ext::shared_ptr<FdmLinearOpComposite> & map,
        const FdmBoundaryConditionSet& bcSet = FdmBoundaryConditionSet());

    void step(Array& a, Time t);
    void setStep(Time dt);
};

%shared_ptr(ImplicitEulerScheme)
class ImplicitEulerScheme {
    %feature("kwargs") ImplicitEulerScheme;
  public:
    enum SolverType { BiCGstab, GMRES };
    ImplicitEulerScheme(
        const ext::shared_ptr<FdmLinearOpComposite>& map,
        const FdmBoundaryConditionSet& bcSet = FdmBoundaryConditionSet(),
        Real relTol = 1e-8,
        SolverType solverType = BiCGstab);

    void step(Array& a, Time t);
    void setStep(Time dt);

    Size numberOfIterations() const;
};

%shared_ptr(CrankNicolsonScheme)
class CrankNicolsonScheme  {
    %feature("kwargs") CrankNicolsonScheme;
  public:
    CrankNicolsonScheme(
        Real theta,
        const ext::shared_ptr<FdmLinearOpComposite>& map,
        const FdmBoundaryConditionSet& bcSet = FdmBoundaryConditionSet(),
        Real relTol = 1e-8,
        ImplicitEulerScheme::SolverType solverType = ImplicitEulerScheme::BiCGstab);

    void step(Array& a, Time t);
    void setStep(Time dt);

    Size numberOfIterations() const;
};

%shared_ptr(DouglasScheme)
class DouglasScheme  {
  public:
    DouglasScheme(
        Real theta,
        const ext::shared_ptr<FdmLinearOpComposite> & map,
        const FdmBoundaryConditionSet& bcSet = FdmBoundaryConditionSet());

    void step(Array& a, Time t);
    void setStep(Time dt);
};

%shared_ptr(ExplicitEulerScheme)
class ExplicitEulerScheme  {
  public:
    ExplicitEulerScheme(
        const ext::shared_ptr<FdmLinearOpComposite>& map,
        const FdmBoundaryConditionSet& bcSet = FdmBoundaryConditionSet());

    void step(Array& a, Time t);
    void setStep(Time dt);
};

%shared_ptr(HundsdorferScheme)
class HundsdorferScheme  {
  public:
    HundsdorferScheme(
        Real theta, Real mu,
        const ext::shared_ptr<FdmLinearOpComposite> & map,
        const FdmBoundaryConditionSet& bcSet = FdmBoundaryConditionSet());

    void step(Array& a, Time t);
    void setStep(Time dt);
};

%shared_ptr(MethodOfLinesScheme)
class MethodOfLinesScheme  {
  public:
    MethodOfLinesScheme(
        const Real eps, const Real relInitStepSize,
        const ext::shared_ptr<FdmLinearOpComposite>& map,
        const FdmBoundaryConditionSet& bcSet = FdmBoundaryConditionSet());

    void step(Array& a, Time t);
    void setStep(Time dt);
};

%shared_ptr(ModifiedCraigSneydScheme)
class ModifiedCraigSneydScheme  {
  public:
    ModifiedCraigSneydScheme(Real theta, Real mu,
        const ext::shared_ptr<FdmLinearOpComposite> & map,
        const FdmBoundaryConditionSet& bcSet = FdmBoundaryConditionSet());

    void step(Array& a, Time t);
    void setStep(Time dt);
};

#endif
