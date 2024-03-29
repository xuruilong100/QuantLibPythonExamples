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
using QuantLib::BSMOperator;
typedef QuantLib::BoundaryCondition<QuantLib::TridiagonalOperator> DefaultBoundaryCondition;
using QuantLib::NeumannBC;
using QuantLib::DirichletBC;
%}

%{
using QuantLib::PdeSecondOrderParabolic;  
using QuantLib::PdeBSM;
using QuantLib::PdeOperator;
%}

class PdeSecondOrderParabolic {
  private:
    PdeSecondOrderParabolic();
  public:
    Real diffusion(Time t, Real x) const;
    Real drift(Time t, Real x) const;
    Real discount(Time t, Real x) const;
    void generateOperator(
        Time t, const TransformedGrid& tg, TridiagonalOperator& L) const;
};

class PdeBSM : public PdeSecondOrderParabolic {
  public:
    PdeBSM(ext::shared_ptr<GeneralizedBlackScholesProcess> process);
};

class TridiagonalOperator {
  public:
    TridiagonalOperator(
        Size size = 0);
    TridiagonalOperator(
        const Array& low,
        const Array& mid,
        const Array& high);

    Array solveFor(const Array& rhs) const;
    void solveFor(const Array& rhs,
                  Array& result) const;
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
    DPlus(
        Size gridPoints, 
        Real h);
};

class DPlusDMinus : public TridiagonalOperator {
  public:
    DPlusDMinus(
        Size gridPoints, 
        Real h);
};

class DMinus : public TridiagonalOperator {
  public:
    DMinus(
        Size gridPoints, 
        Real h);
};

class DZero : public TridiagonalOperator {
  public:
    DZero(Size gridPoints, Real h);
};

class BSMOperator : public TridiagonalOperator {
  public:
    BSMOperator();
    BSMOperator(
        Size size,
        Real dx, 
        Rate r, 
        Rate q, 
        Volatility sigma);
    BSMOperator(
        const Array& grid, 
        Rate r, 
        Rate q, 
        Volatility sigma);
};

template <class PdeClass>
class PdeOperator : public TridiagonalOperator {
public:
    %extend {
        PdeOperator(
        const Array& grid,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Time residualTime = 0.0) {
        return new PdeOperator<PdeClass>(
            grid, process, residualTime);
        }
    }    
};

%template(BSMTermOperator) PdeOperator<PdeBSM>;

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
