#ifndef ql_solvers_i
#define ql_solvers_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

// 1D Solvers

%{
using QuantLib::Bisection;
using QuantLib::Brent;
using QuantLib::FalsePosition;
using QuantLib::Newton;
using QuantLib::NewtonSafe;
using QuantLib::Ridder;
using QuantLib::Secant;
%}

%define DeclareSolver(SolverName)
class SolverName {
  public:
    void setMaxEvaluations(Size evaluations);
    void setLowerBound(Real lowerBound);
    void setUpperBound(Real upperBound);
    %extend {
        Real solve(
            PyObject* function, Real xAccuracy,
            Real guess, Real step) {
            UnaryFunction f(function);
            return self->solve(
                f, xAccuracy, guess, step);
        }
        Real solve(
            PyObject* function, Real xAccuracy,
            Real guess, Real xMin, Real xMax) {
            UnaryFunction f(function);
            return self->solve(
                f, xAccuracy, guess, xMin, xMax);
        }
    }
};
%enddef

// Keep this list in sync with bondfunctions.i yield solvers.

// Actual solvers
DeclareSolver(Brent);
DeclareSolver(Bisection);
DeclareSolver(FalsePosition);
DeclareSolver(Ridder);
DeclareSolver(Secant);

// these two need f.derivative()
DeclareSolver(Newton);
DeclareSolver(NewtonSafe);

#endif
