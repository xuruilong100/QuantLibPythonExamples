#ifndef ql_operators_i
#define ql_operators_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::TridiagonalOperator;
using QuantLib::DPlus;
using QuantLib::DPlusDMinus;
using QuantLib::DMinus;
using QuantLib::DZero;
typedef QuantLib::BoundaryCondition<QuantLib::TridiagonalOperator> DefaultBoundaryCondition;
using QuantLib::NeumannBC;
using QuantLib::DirichletBC;
%}

class TridiagonalOperator {
  public:
    TridiagonalOperator(Size size=0);
    TridiagonalOperator(
        const Array& low,
        const Array& mid,
        const Array& high);

    Array solveFor(const Array& rhs) const;
    Array applyTo(const Array& v) const;
    Array SOR(const Array& rhs, Real tol) const;
    Size size() const;
    bool isTimeDependent() const;
    const Array& lowerDiagonal() const;
    const Array& diagonal() const;
    const Array& upperDiagonal() const;
    void setFirstRow(Real, Real);
    void setMidRow(Size, Real, Real, Real);
    void setMidRows(Real, Real, Real);
    void setLastRow(Real, Real);
    void setTime(Time t);
    static TridiagonalOperator identity(Size size);

    %extend {
        TridiagonalOperator __add__(
            const TridiagonalOperator& O) {
            return *self+O;
        }
        TridiagonalOperator __sub__(
            const TridiagonalOperator& O) {
            return *self-O;
        }
        TridiagonalOperator __mul__(Real a) {
            return *self*a;
        }
        TridiagonalOperator __div__(Real a) {
            return *self/a;
        }
        TridiagonalOperator __iadd__(
            const TridiagonalOperator& O) {
            return *self+O;
        }
        TridiagonalOperator __isub__(
            const TridiagonalOperator& O) {
            return *self-O;
        }
        TridiagonalOperator __imul__(Real a) {
            return *self*a;
        }
        TridiagonalOperator __rmul__(Real a) {
            return *self*a;
        }
        TridiagonalOperator __idiv__(Real a) {
            return *self/a;
        }
    }
};

class DPlus : public TridiagonalOperator {
  public:
    DPlus(Size gridPoints, Real h);
};

class DPlusDMinus : public TridiagonalOperator {
  public:
    DPlusDMinus(Size gridPoints, Real h);
};

class DMinus : public TridiagonalOperator {
  public:
    DMinus(Size gridPoints, Real h);
};

class DZero : public TridiagonalOperator {
  public:
    DZero(Size gridPoints, Real h);
};

%shared_ptr(DefaultBoundaryCondition)
class DefaultBoundaryCondition {
    %rename(NoSide) None;
  private:
    DefaultBoundaryCondition();
  public:
    enum Side { None, Upper, Lower };
};

%shared_ptr(NeumannBC)
class NeumannBC : public DefaultBoundaryCondition {
  public:
    NeumannBC(
        Real value,
        DefaultBoundaryCondition::Side side);
};

%shared_ptr(DirichletBC)
class DirichletBC : public DefaultBoundaryCondition {
  public:
    DirichletBC(
        Real value,
        DefaultBoundaryCondition::Side side);
};

#endif
