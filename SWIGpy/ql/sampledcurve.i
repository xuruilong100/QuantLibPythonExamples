#ifndef ql_sampled_curve_i
#define ql_sampled_curve_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::SampledCurve;
%}

class SampledCurve {
  public:
    SampledCurve(Size gridSize = 0);
    SampledCurve(const Array& grid);
    const Array& grid() const;
    const Array& values() const;
    Real gridValue(Size i) const;
    Real value(Size i) const;
    Size size() const;
    bool empty() const;
    void setGrid(const Array&);
    void setValues(const Array&);
    Real valueAtCenter() const;
    Real firstDerivativeAtCenter() const;
    Real secondDerivativeAtCenter() const;
    void swap(SampledCurve&);
    void setLogGrid(Real min, Real max);
    void regridLogGrid(Real min, Real max);
    void shiftGrid(Real s);
    void scaleGrid(Real s);
    void regrid(const Array& new_grid);
    %extend {
        void setValue(Size i, Real v) {
            self->value(i) = v;
        }
        void sample(PyObject *func) {
            const UnaryFunction f(func);
            self->sample(f);
        }
        void regrid(const Array& new_grid, PyObject *func) {
            const UnaryFunction f(func);
            self->regrid(new_grid, f);
        }
        const SampledCurve& transform(PyObject *x) {
            const UnaryFunction f(x);
            return self->transform(f);
        }
        const SampledCurve& transformGrid(PyObject *x) {
            const UnaryFunction f(x);
            return self->transformGrid(f);
        }
    }
};

#endif
