#ifndef ql_interpolation_i
#define ql_interpolation_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::RichardsonExtrapolation;
%}

class RichardsonExtrapolation {
  public:
    Real operator()(Real t = 2.0) const;
    Real operator()(Real t, Real s) const;

    %extend {
        RichardsonExtrapolation(
            PyObject* fct,
            Real delta_h,
            Real n = Null<Real>()) {
            UnaryFunction f(fct);
            return new RichardsonExtrapolation(
                f, delta_h, n);
        }
    }
};

#endif
