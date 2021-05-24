#ifndef ql_fdms_FdmSolver_i
#define ql_fdms_FdmSolver_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmSolverDesc;
using QuantLib::Fdm1DimSolver;
using QuantLib::FdmBackwardSolver;
using QuantLib::Fdm2dBlackScholesSolver;
using QuantLib::Fdm2DimSolver;
using QuantLib::Fdm3DimSolver;
using QuantLib::FdmG2Solver;
using QuantLib::FdmHestonHullWhiteSolver;
using QuantLib::FdmHestonSolver;
using QuantLib::FdmHullWhiteSolver;
using QuantLib::FdmNdimSolver;
%}

struct FdmSolverDesc {
  public:
    %extend {
        FdmSolverDesc(
            const ext::shared_ptr<FdmMesher>& mesher,
            const FdmBoundaryConditionSet& bcSet,
            const ext::shared_ptr<FdmStepConditionComposite>& condition,
            const ext::shared_ptr<FdmInnerValueCalculator>& calculator,
            Time maturity,
            Size timeSteps,
            Size dampingSteps) {

            const FdmSolverDesc desc = {
                mesher, bcSet, condition, calculator,
                maturity, timeSteps, dampingSteps };

            return new FdmSolverDesc(desc);
        }

        ext::shared_ptr<FdmMesher> getMesher() const { return self->mesher; }
        const FdmBoundaryConditionSet& getBcSet() const { return self->bcSet; }
        ext::shared_ptr<FdmStepConditionComposite> getStepConditions() const { return self->condition; }
        ext::shared_ptr<FdmInnerValueCalculator> getCalculator() const { return self->calculator; }
        Time getMaturity() const { return self->maturity; }
        Size getTimeSteps() const { return self->timeSteps; }
        Size getDampingSteps() const { return self->dampingSteps; }
    }
};

%shared_ptr(Fdm1DimSolver)
class Fdm1DimSolver {
  public:
    Fdm1DimSolver(
        const FdmSolverDesc& solverDesc,
        const FdmSchemeDesc& schemeDesc,
        const ext::shared_ptr<FdmLinearOpComposite>& op);

    Real interpolateAt(Real x) const;
    Real thetaAt(Real x) const;

    Real derivativeX(Real x) const;
    Real derivativeXX(Real x) const;
};

%shared_ptr(FdmBackwardSolver)
class FdmBackwardSolver {
  public:
    FdmBackwardSolver(
        const ext::shared_ptr<FdmLinearOpComposite>& map,
        const FdmBoundaryConditionSet& bcSet,
        const ext::shared_ptr<FdmStepConditionComposite> condition,
        const FdmSchemeDesc& schemeDesc);

    void rollback(
        Array& a, Time from, Time to,
        Size steps, Size dampingSteps);
};

%shared_ptr(Fdm2dBlackScholesSolver)
class Fdm2dBlackScholesSolver {
  public:
    %feature("kwargs") Fdm2dBlackScholesSolver;
    %extend {
        Fdm2dBlackScholesSolver(
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& p1,
            const ext::shared_ptr<GeneralizedBlackScholesProcess>& p2,
            const Real correlation,
            const FdmSolverDesc& solverDesc,
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
            bool localVol = false,
            Real illegalLocalVolOverwrite = -Null<Real>()) {
            return new Fdm2dBlackScholesSolver(
                Handle<GeneralizedBlackScholesProcess>(p1),
                Handle<GeneralizedBlackScholesProcess>(p2),
                correlation, solverDesc, schemeDesc,
                localVol, illegalLocalVolOverwrite);
        }
    }

    Real valueAt(Real x, Real y) const;
    Real thetaAt(Real x, Real y) const;

    Real deltaXat(Real x, Real y) const;
    Real deltaYat(Real x, Real y) const;
    Real gammaXat(Real x, Real y) const;
    Real gammaYat(Real x, Real y) const;
    Real gammaXYat(Real x, Real y) const;
};

%shared_ptr(Fdm2DimSolver)
class Fdm2DimSolver {
  public:
    Fdm2DimSolver(
        const FdmSolverDesc& solverDesc,
        const FdmSchemeDesc& schemeDesc,
        const ext::shared_ptr<FdmLinearOpComposite>& op);

    Real interpolateAt(Real x, Real y) const;
    Real thetaAt(Real x, Real y) const;

    Real derivativeX(Real x, Real y) const;
    Real derivativeY(Real x, Real y) const;
    Real derivativeXX(Real x, Real y) const;
    Real derivativeYY(Real x, Real y) const;
    Real derivativeXY(Real x, Real y) const;
};

%shared_ptr(Fdm3DimSolver)
class Fdm3DimSolver {
  public:
    Fdm3DimSolver(
        const FdmSolverDesc& solverDesc,
        const FdmSchemeDesc& schemeDesc,
        const ext::shared_ptr<FdmLinearOpComposite>& op);

    void performCalculations() const;

    Real interpolateAt(Real x, Real y, Rate z) const;
    Real thetaAt(Real x, Real y, Rate z) const;
};

%shared_ptr(FdmG2Solver)
class FdmG2Solver {
  public:
    %extend {
        FdmG2Solver(
            const ext::shared_ptr<G2>& model,
            const FdmSolverDesc& solverDesc,
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer()) {
                return new FdmG2Solver(
                    Handle<G2>(model), solverDesc, schemeDesc);
        }
    }
    Real valueAt(Real x, Real y) const;
};

%shared_ptr(FdmHestonHullWhiteSolver)
class FdmHestonHullWhiteSolver {
  public:
    %extend {
        FdmHestonHullWhiteSolver(
            const ext::shared_ptr<HestonProcess>& hestonProcess,
            const ext::shared_ptr<HullWhiteProcess>& hwProcess,
            Rate corrEquityShortRate,
            const FdmSolverDesc& solverDesc,
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer()) {
                return new FdmHestonHullWhiteSolver(
                    Handle<HestonProcess>(hestonProcess),
                    Handle<HullWhiteProcess>(hwProcess),
                    corrEquityShortRate,
                    solverDesc, schemeDesc);
        }
    }

    Real valueAt(Real s, Real v, Rate r) const;
    Real thetaAt(Real s, Real v, Rate r) const;

    Real deltaAt(Real s, Real v, Rate r, Real eps) const;
    Real gammaAt(Real s, Real v, Rate r, Real eps) const;
};

%shared_ptr(FdmHestonSolver)
class FdmHestonSolver {
  public:
    %feature("kwargs") FdmHestonSolver;
    %extend {
        FdmHestonSolver(
            const ext::shared_ptr<HestonProcess>& process,
            const FdmSolverDesc& solverDesc,
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
            const ext::shared_ptr<FdmQuantoHelper>& quantoHelper = ext::shared_ptr<FdmQuantoHelper>(),
            const ext::shared_ptr<LocalVolTermStructure>& leverageFct = ext::shared_ptr<LocalVolTermStructure>()) {
                return new FdmHestonSolver(
                    Handle<HestonProcess>(process),
                    solverDesc, schemeDesc,
                    Handle<FdmQuantoHelper>(quantoHelper),
                    leverageFct);
        }
    }

    Real valueAt(Real s, Real v) const;
    Real thetaAt(Real s, Real v) const;

    Real deltaAt(Real s, Real v) const;
    Real gammaAt(Real s, Real v) const;

    Real meanVarianceDeltaAt(Real s, Real v) const;
    Real meanVarianceGammaAt(Real s, Real v) const;
};

%shared_ptr(FdmHullWhiteSolver)
class FdmHullWhiteSolver {
  public:
    %extend {
        FdmHullWhiteSolver(
            const ext::shared_ptr<HullWhite>& model,
            const FdmSolverDesc& solverDesc,
            const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer()) {
                return new FdmHullWhiteSolver(
                    Handle<HullWhite>(model), solverDesc, schemeDesc);
        }
    }
    Real valueAt(Real r) const;
};

%shared_ptr(FdmNdimSolver<4>);
%shared_ptr(FdmNdimSolver<5>);
%shared_ptr(FdmNdimSolver<6>);
template <Size N>
class FdmNdimSolver {
  public:
    FdmNdimSolver(
        const FdmSolverDesc& solverDesc,
        const FdmSchemeDesc& schemeDesc,
        const ext::shared_ptr<FdmLinearOpComposite>& op);

    Real interpolateAt(const std::vector<Real>& x) const;
    Real thetaAt(const std::vector<Real>& x) const;
};

%template(Fdm4dimSolver) FdmNdimSolver<4>;
%template(Fdm5dimSolver) FdmNdimSolver<5>;
%template(Fdm6dimSolver) FdmNdimSolver<6>;

#endif
