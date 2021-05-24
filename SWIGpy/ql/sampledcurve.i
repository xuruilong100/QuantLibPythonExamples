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
    SampledCurve();
    SampledCurve(const Array&);
    Array& grid();
    Array& values();
    Real gridValue(Size i);
    Real value(Size i);
    Size size() const;
    bool empty() const;
    void setGrid(const Array&);
    void setValues(const Array&);
    void swap(SampledCurve&);
    void setLogGrid(Real min, Real max);
    void regridLogGrid(Real min, Real max);
    void shiftGrid(Real s);
    void scaleGrid(Real s);
    void regrid(const Array &);
};

#endif
